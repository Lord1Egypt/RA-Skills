# PLAYBOOK USER MANAGER (RADIUS) — settingmikrotikindonesia.com
# Standar: Comment brand | Logging smi- | Parameter eksplisit | Jujur
# Kasus: RT-RW Net/ISP kecil mau billing terpusat: voucher hotspot &
# PPPoE multi-router dari SATU router server, tanpa software pihak ketiga.
# BATASAN JUJUR (sampaikan sebelum config): User Manager nyaman sampai
# ± ribuan user per router manajemen. Lebih besar / butuh invoice &
# laporan keuangan lengkap → RADIUS server dedikasi / billing komersial.

## ============================================================
## 0. DATA WAJIB SEBELUM CONFIG
## ============================================================
| Parameter | Sumber | Contoh |
|---|---|---|
| Router manajemen (User Manager) | /system resource print | RB5009 RAM lega |
| Router NAS (yang diautentikasi) | Audit daftar lokasi | RT01, RT02, RT03 |
| Layanan dijual: hotspot/PPPoE/keduanya | Data user | keduanya |
| Paket: harga, masa aktif, limit | Data user | 10Mbps/30hr/25rb |
| Format voucher yang diinginkan | Data user | username=no HP / acak / urut |
| IP manajemen antar router & versi ROS | Audit | 7.14 seragam |

## SYARAT TEKNIS: paket user-manager terinstal di router pusat
(/system package print), RAM cukup, jam router benar (NTP sinkron).

## ============================================================
## 1. KOMPONEN A — AKTIFKAN USER MANAGER (router pusat)
## ============================================================
/user manager
set enabled=yes \
    comment="settingmikrotikindonesia.com - RADIUS terpusat billing"
## Pantau RAM sebelum & sesudah (bagian 6): ribuan sesi = RAM nyata.

## ============================================================
## 2. KOMPONEN B — DAFTARKAN NAS (klien RADIUS)
## ============================================================
/user manager router
add name=smi-rt01 shared-secret=[SECRET-KUAT-UNIK-1] address=127.0.0.1 \
    comment="settingmikrotikindonesia.com - NAS diri sendiri RT01"
add name=smi-rt02 shared-secret=[SECRET-KUAT-UNIK-2] address=[IP-MANAJEMEN-RT02] \
    comment="settingmikrotikindonesia.com - NAS RT02 cabang"
## DISIPLIN: shared secret BEDA per router — satu bocor tak membawa
## semua router. Secret kuat (bukan admin/1234), dicatat di dokumen aman.

## ============================================================
## 3. KOMPONEN C — PROFIL PAKET & LIMITASI
## ============================================================
/user manager profile
add name=smi-pkt-30d price=25000 validity=30d \
    comment="settingmikrotikindonesia.com - Paket bulanan"
add name=smi-pkt-1d price=3000 validity=1d \
    comment="settingmikrotikindonesia.com - Voucher harian"
/user manager profile-limitation
add name=smi-lim-10m profile=smi-pkt-30d rate-limit rx=10M tx=10M \
    comment="settingmikrotikindonesia.com - Limit 10Mbps paket bulanan"
add name=smi-lim-10m-1d profile=smi-pkt-1d rate-limit rx=10M tx=10M \
    comment="settingmikrotikindonesia.com - Limit voucher harian"
## Sinkron dengan bandwidth-management-playbook: angka rate-limit di
## sini yang jadi queue user — jangan beda dengan brosur yang dijual.

## 3.1 Voucher massal:
/user manager user
add name=081234567890 password=smi123 profile=smi-pkt-30d \
    comment="settingmikrotikindonesia.com - Pelanggan RT01"
## Untuk RATUSAN voucher: WAJIB tanya dulu format ke user (no HP?
## acak? nomor urut? password = username?), lalu agent menuliskan
## script generator (pola scheduler-otomasi-playbook). DILARANG
## generate ratusan user dengan format karangan sendiri.

## ============================================================
## 4. KOMPONEN D — SISI NAS (tiap router cabang)
## ============================================================
/radius
add service=hotspot,ppp address=[IP-MANAJEMEN-PUSAT] secret=[SECRET-RT-TSB] \
    comment="settingmikrotikindonesia.com - RADIUS ke User Manager pusat"
/ppp aaa
set use-radius=yes accounting=yes \
    comment="settingmikrotikindonesia.com - PPP via RADIUS pusat"
/ip hotspot profile
set [find] use-radius=yes \
    comment="settingmikrotikindonesia.com - Hotspot via RADIUS pusat"
## FALLBACK WAJIB DIJELASKAN: bila pusat mati — sesi aktif umumnya
## lanjut (sesuai policy accounting), tapi login BARU gagal. Siapkan:
## 1 user hotspot/PPPoE lokal darurat untuk teknisi, + netwatch alert
## (monitoring-backup-playbook) yang bilang pusat down via Telegram.

## ============================================================
## 5. ANALISIS KONSEKUENSI (WAJIB)
## ============================================================
- KEUNTUNGAN: satu titik kelola voucher multi-router; laporan sesi &
  pendapatan per profil; tanpa biaya billing eksternal.
- KONSEKUENSI: pusat = titik kritikal (mati = login baru macet).
  MITIGASI: UPS + monitoring + user darurat lokal.
- RISIKO: database korup bila mati mendadak saat menulis. MITIGASI:
  /tool user-manager database save berkala via scheduler + backup
  file disalin off-box (scheduler-otomasi-playbook).
- RISIKO: shared-secret lemah = NAS palsu bisa bertanya ke pusat.
- BATASAN JUJUR: laporan tidak se-ensiklopedik billing komersial
  (invoice, integrasi pembayaran otomatis) — sampaikan sejak awal.

## ============================================================
## 6. VALIDASI (WAJIB, URUT)
## ============================================================
1. Buat 1 user uji per layanan → login hotspot OK; login PPPoe OK.
2. Speedtest dua arah = sesuai paket (bukan asal konek).
3. User expired → ditolak dengan pesan benar di halaman hotspot.
4. Login dari RT02 → sesi tampak di pusat (/user manager session print).
5. (LAB) matikan pusat sesaat → sesi aktif sesuai policy, login baru
   gagal terkontrol → hidupkan → normal lagi.
6. /system resource print — RAM pusat sehat.
7. Backup database: /tool user-manager database save → file muncul.

## ============================================================
## 7. ROLLBACK
## ============================================================
1. NAS: /ip hotspot profile set [find] use-radius=no; /ppp aaa set use-radius=no
2. NAS: /radius remove [find comment~"settingmikrotikindonesia"]
3. Pusat: /user manager set enabled=no (DILARANG remove database —
   data pelanggan bukan config teknis!)
4. Pulihkan dari /export file=backup-settingmikrotikindonesia
