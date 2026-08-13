
import tkinter as tk
from tkinter import ttk, messagebox
import math
 
# Batas validasi input
SUHU_MIN, SUHU_MAX = 20, 55
WAKTU_MIN, WAKTU_MAX = 0, 24
LAG_PHASE = 1  # jam jeda sebelum bakteri aktif fermentasi
 
 
def hitung_k(suhu):
    """Menghitung konstanta laju fermentasi (k) berdasarkan suhu.
    Semakin tinggi suhu, semakin besar k -> pH turun lebih cepat.
    """
    return 0.05 * suhu - 1.2
 
 
def hitung_ph(suhu, waktu):
    """Menghitung prediksi pH menggunakan model logistik sederhana.
    pH akan turun dari sekitar 6.6 menuju sekitar 4.5 seiring waktu.
    """
    k = hitung_k(suhu)
    waktu_efektif = max(0, waktu - LAG_PHASE)
    ph = 6.6 - 2.1 / (1 + math.exp(-k * (waktu_efektif - 4)))
    return round(ph, 2)
 
 
def tentukan_status(ph):
    """Menentukan status yogurt berdasarkan nilai pH."""
    if ph < 4.0:
        return "terlalu asam", "#d03b3b"
    if ph > 4.6:
        return "belum matang", "#c98500"
    return "aman", "#0ca30c"
 
 
class YogurtPHApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Prediksi pH Fermentasi Yogurt")
        self.root.geometry("380x320")
        self.root.resizable(False, False)
 
        frame = ttk.Frame(root, padding=20)
        frame.pack(fill="both", expand=True)
 
        ttk.Label(frame, text="Prediksi pH Yogurt", font=("Segoe UI", 14, "bold")).grid(
            row=0, column=0, columnspan=2, pady=(0, 15)
        )
 
        # Input suhu
        ttk.Label(frame, text=f"Suhu (°C) [{SUHU_MIN}-{SUHU_MAX}]:").grid(
            row=1, column=0, sticky="w", pady=5
        )
        self.suhu_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.suhu_var, width=15).grid(
            row=1, column=1, pady=5
        )
 
        # Input waktu
        ttk.Label(frame, text=f"Waktu (jam) [{WAKTU_MIN}-{WAKTU_MAX}]:").grid(
            row=2, column=0, sticky="w", pady=5
        )
        self.waktu_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.waktu_var, width=15).grid(
            row=2, column=1, pady=5
        )
 
        # Tombol hitung
        ttk.Button(frame, text="Hitung pH", command=self.on_calculate).grid(
            row=3, column=0, columnspan=2, pady=15
        )
 
        # Hasil
        self.hasil_ph_label = ttk.Label(frame, text="", font=("Segoe UI", 20, "bold"))
        self.hasil_ph_label.grid(row=4, column=0, columnspan=2)
 
        self.hasil_status_label = ttk.Label(frame, text="", font=("Segoe UI", 12))
        self.hasil_status_label.grid(row=5, column=0, columnspan=2, pady=(5, 0))
 
    def on_calculate(self):
        # Validasi input berupa angka
        try:
            suhu = float(self.suhu_var.get())
            waktu = float(self.waktu_var.get())
        except ValueError:
            messagebox.showerror("Input tidak valid", "Suhu dan waktu harus berupa angka")
            return
 
        # Validasi rentang suhu
        if suhu < SUHU_MIN or suhu > SUHU_MAX:
            messagebox.showerror("Input tidak valid", f"Suhu harus antara {SUHU_MIN}-{SUHU_MAX}°C")
            return
 
        # Validasi rentang waktu
        if waktu < WAKTU_MIN or waktu > WAKTU_MAX:
            messagebox.showerror("Input tidak valid", f"Waktu harus antara {WAKTU_MIN}-{WAKTU_MAX} jam")
            return
 
        ph = hitung_ph(suhu, waktu)
        status, warna = tentukan_status(ph)
 
        self.hasil_ph_label.config(text=f"pH = {ph}")
        self.hasil_status_label.config(text=f"Status: {status}", foreground=warna)
 
 
if __name__ == "__main__":
    root = tk.Tk()
    app = YogurtPHApp(root)
    root.mainloop()