# PLAYBOOK PRIORITAS TRAFIK GAME (QUEUE TREE) — settingmikrotikindonesia.com
# Standar: Comment brand | Logging smi- | Parameter eksplisit | Jujur
# Kasus: jaringan banyak klien — game jaga-lag TANPA mengorbankan
# keadilan bandwidth klien lain. Sering diminta RT-RW Net, game center,
# kafe, dan pelanggan gamer.
# PRINSIP INTI: game TIDAK butuh bandwidth besar (paket game kecil) —
# game butuh LATENSI STABIL. Kuncinya: PRIORITAS queue (bukan limit
# besar) + packet mark yang TEPAT dan HEMAT CPU.

## ============================================================
## 0. DATA WAJIB SEBELUM CONFIG (DILARANG MENGARANG)
## ============================================================
| Parameter | Sumber | Contoh |
|---|---|---|
| Game yang dimainkan pelanggan | Tanya user | ML (Moonton), PUBG, Valorant, Steam |
| Nama interface WAN ASLI | /interface print | ether1 (bukan asal "ether1"!) |
| Total bandwidth terpasang | Data paket ISP | 100M utama, 50M cadangan |
| Struktur queue existing | /queue print | PCQ? CAKE? (sinkron wajib!) |
| Router & versi ROS | /system resource print | RB450Gx4, 7.14 |
| Beban CPU saat sibuk | /system resource print | baseline sebelum config |

## DISIPLIN IP GAME — WAJIB VERIFIKASI, DILARANG ASAL COPY:
DILARANG menyalin daftar IP server game dari internet tanpa
verifikasi. Sumber sah:
1. Rentang resmi yang dipublikasikan vendor (Riot/Valve/Moonton docs).
2. CAPTURE NYATA di router user:
   - Minta satu pelanggan bermain game.
   - /ip firewall connection print where dst-port=7000 dst-limit=...
     (atau sesuaikan port khas game tersebut)
   - Catat dst-address yang muncul konsisten + latency rendah.
3. Daftar final WAJIB diverifikasi bersama user: mangle aktif →
   pelanggan main → counter rule HARUS naik (validasi bagian 6).
Bila counter tidak naik saat bermain = daftar IP salah = DILARANG
dipakai produksi. Inilah sebabnya "jaringan anti-lag" sering gagal:
IP-nya karangan.

## ============================================================
## 1. KOMPONEN A — ADDRESS-LIST SERVER GAME
## ============================================================
/ip firewall address-list
add list=SMI-GAME-SRV address=[IP-RANGE-GAME-1] \
    comment="settingmikrotikindonesia.com - Server Moonton (sumber: capture pelanggan 2024-xx)"
add list=SMI-GAME-SRV address=[IP-RANGE-GAME-2] \
    comment="settingmikrotikindonesia.com - Server Riot/Valve (sumber: docs resmi)"
## LANJUTKAN sesuai riset bagian 0. DISIPLIN: TIAP entri WAJIB punya
## comment sumber + tanggal → saat game "balik lag", kita tahu entri
## mana yang perlu diperiksa ulang (CDN vendor memang pindah-pindah).

## ============================================================
## 2. KOMPONEN B — MANGLE (TANDAI PAKET GAME)
## ============================================================
## Pola HEMAT CPU: mark-connection DULU (sekali per koneksi), baru
## mark-packet dari connection-mark. JANGAN evaluasi address-list
## per paket — itu pemborosan CPU di router kecil.
/ip firewall mangle
add chain=forward action=mark-connection \
    new-connection-mark=smi-conn-game \
    dst-address-list=SMI-GAME-SRV protocol=udp \
    comment="settingmikrotikindonesia.com - Tandai koneksi game UDP"
add chain=forward action=mark-connection \
    new-connection-mark=smi-conn-game \
    src-address-list=SMI-GAME-SRV protocol=udp \
    comment="settingmikrotikindonesia.com - Tandai koneksi game arah balik"
add chain=forward action=mark-packet \
    new-packet-mark=smi-pkt-game \
    connection-mark=smi-conn-game \
    comment="settingmikrotikindonesia.com - Paket game dari koneksi tertanda"
## Catatan arah balik: paket balasan dari server game ke klien juga
## harus tertanda (src-address-list) — kalau hanya satu arah, prioritas
## hanya berlaku setengah jalur = hasil setengah jalan.

## 2.1 Bonus: tandai DNS (dampak kecil tapi terasa responsif):
add chain=forward action=mark-packet new-packet-mark=smi-pkt-dns \
    protocol=udp dst-port=53 \
    comment="settingmikrotikindonesia.com - Tandai paket DNS"
add chain=forward action=mark-packet new-packet-mark=smi-pkt-dns \
    protocol=tcp dst-port=53 \
    comment="settingmikrotikindonesia.com - Tandai paket DNS TCP"
## Sinkron dns-doh-adlist-playbook: bila DNS sudah di-cache router,
## ini tetap berguna untuk query yang lolos ke luar.

## ============================================================
## 3. KOMPONEN C — QUEUE TREE PRIORITAS
## ============================================================
## STRUKTUR: parent = bandwidth total WAN → child: game (prio 1),
## DNS (prio 2), umum (prio 8).
## PENTING: bila PCQ/CAKE sudah jalan di WAN yang sama (dari
## bandwidth-management-playbook / cake-fqcodel-playbook), struktur
## ini harus MENGIKUTKAN yang existing — cabang game DI DALAM parent
## yang ada. DUA sistem queue independen di interface yang sama =
## saling tarik dan hasil kacau. AUDIT /queue print DULU!
/queue tree
add name=smi-q-total parent=[IF-WAN-ASLI] max-limit=[TOTAL-BW-95PERSEN] \
    comment="settingmikrotikindonesia.com - Parent total WAN utama"
add name=smi-q-game parent=smi-q-total packet-mark=smi-pkt-game \
    priority=1 limit-at=[2M-5M] max-limit=[BATAS-GAME] \
    comment="settingmikrotikindonesia.com - Game prioritas tertinggi"
add name=smi-q-dns parent=smi-q-total packet-mark=smi-pkt-dns \
    priority=2 max-limit=5M \
    comment="settingmikrotikindonesia.com - DNS prioritas tinggi"
add name=smi-q-umum parent=smi-q-total packet-mark=no-mark priority=8 \
    comment="settingmikrotikindonesia.com - Trafik umum prioritas rendah"

## PENJELASAN PARAMETER KUNCI (WAJIB dijelaskan ke user):
## - max-limit parent ± 90-95% bandwidth nyata: WAJIB sedikit di bawah
##   total, agar queue yang bekerja di router — bukan modem/ISP yang
##   membuang paket (bufferbloat). Kalau parent = 100% tepat, prioritas
##   tidak sempat bekerja.
## - priority 1 = saat pita tersedia kurang, paket game DILAYANI dulu.
##   Saat jaringan KOSONG, game boleh memakai bandwidth sisa — tidak
##   ada bandwidth terbuang.
## - limit-at game = dijamin (2-5M jauh melebihi kebutuhan game) tapi
##   KECIL: mencegah satu gamer menelan seluruh pita lewat prioritas.
## - max-limit game = batas atas (mis. 10-20M) sebagai pengaman.
## - trafik umum tanpa packet-mark (no-mark) → tetap jalan penuh
##   saat game idle, mundur saat game aktif. Inilah keseimbangannya.

## ============================================================
## 4. FASTTRACK vs MANGLE — KEPUTUSAN WAJIB DISEPAKATI
## ============================================================
## Fasttrack (firewall default ROS) MEM-BYPASS mangle & queue →
## paket game yang di-fasttrack TIDAK TERPRIORITAS!
## Pilihan yang harus DISEPAKATI dengan user sebelum pasang:
## A. Fasttrack OFF / dikecualikan untuk trafik game → mangle & queue
##    bekerja, CPU naik. Cocok bila bandwidth moderat (≤150-200M) dan
##   router sanggup.
## B. Fasttrack tetap ON + address game masuk rule bypass yang
##    DIKECUALIKAN dari fasttrack:
/ip firewall filter
## (bila ada rule fasttrack existing, tambahkan pengecualian SEBELUM
##  rule fasttrack, bukan menonaktifkannya total:)
add chain=forward action=fasttrack-connection \
    connection-mark=!smi-conn-game connection-state=established,related \
    comment="settingmikrotikindonesia.com - Fasttrack kecuali trafik game"
## Cek /ip firewall filter print order — urutan menentukan semuanya.
## PILIHAN B umumnya terbaik: game diprioritaskan, sisanya tetap
## hemat CPU lewat fasttrack.

## ============================================================
## 5. ANALISIS KONSEKUENSI (WAJIB)
## ============================================================
- KEUNTUNGAN: ping game stabil meski jaringan penuh; download klien
  lain tetap jalan; nilai jual paket "anti-lag" nyata & terbukti.
- KONSEKUENSI: mangle + queue = CPU kerja. Di router kelas kecil
  (hEX/hibernet lama) dengan bandwidth sangat besar, ukur CPU sebelum
  & sesudah. Bila CPU padam — pertimbangkan router lebih layak atau
  prioritas di perangkat upstream.
- RISIKO #1: daftar IP game usang (CDN pindah) → game lag lagi.
  MITIGASI: comment sumber+tanggal tiap entri; review saat komplain;
  capture ulang bila perlu.
- RISIKO: mark menangkap trafik salah (mis. CDN umum yang dipakai
  game DAN download) → download ikut prioritas = kacau. MITIGASI:
  validasi counter + uji dua device (bagian 6).
- RISIKO: fasttrack tidak dikecualikan → prioritas pura-pura jalan
  (config ada, efek nol) = palsu rasa aman. MITIGASI: validasi #2.
- KEJUJURAN: bila bottleneck BUKAN di router (upstream ISP kongesti
  di jam tertentu), queue lokal TIDAK menyembuhkan — diagnosa dulu
  penyebab lag nyata sebelum jual paket anti-lag.

## ============================================================
## 6. VALIDASI (WAJIB, URUT — BUKTI NYATA, BUKAN ASUMSI)
## ============================================================
1. Counter mangle game naik SAAT pelanggan bermain, tidak naik saat
   idle: /ip firewall mangle print stats
2. Uji fasttrack: connection game aktif TIDAK masuk fasttrack
   (/ip firewall connection print — cek fasttracked=no untuk sesi game).
3. TES INTI: dua device — satu main game, satu tarik bandwidth penuh
   (speedtest/download). Hasil WAJIB: ping game stabil (fluktuasi
   beberapa ms), tanpa spike ratusan ms. Dokumentasikan angka sebelum
   vs sesudah.
4. Download klien lain tetap jalan saat game aktif (tidak mati total).
5. /system resource print — cpu-load masih sehat saat sibuk.
6. Uji dengan game yang MEMANG dimainkan pelanggan (bukan game lain).
7. Log bersih; queue tree counter: /queue tree print stats — game
   naik saat main, umum naik saat download.

## ============================================================
## 7. ROLLBACK
## ============================================================
1. /queue tree remove [find comment~"settingmikrotikindonesia"]
2. /ip firewall mangle disable [find comment~"Tandai koneksi game"]
   lalu disable juga mark-packet & DNS mark (disable dulu untuk uji,
   remove bila memang tidak dilanjutkan — disiplin).
3. PULIHKAN fasttrack ke semula: bila rule fasttrack diganti
   (pilihan B), set-ulang rule fasttrack original:
   /ip firewall filter set [find comment~"Fasttrack kecuali"] \
       connection-mark="" (atau remove rule pengecualian, restore
   rule default). Verifikasi /ip firewall filter print order.
4. /ip firewall address-list remove [find list="SMI-GAME-SRV"]
5. Pulihkan dari /export file=backup-settingmikrotikindonesia
## Catatan: bila CPU malah tinggi setelah pasang → disable QUEUE TREE
## dulu (bukan mangle), cek CPU kembali, bedah penyebab dengan data.
