# PLAYBOOK CAKE / FQ-CODEL — settingmikrotikindonesia.com
# Alternatif bagi klien yang TIDAK MAU PCQ: queue discipline modern
# (CAKE / FQ_CODEL) yang dikonfigurasi sesuai topologi & kebutuhan.
# Standar: TANPA fasttrack | Comment brand | Interface MILIK USER
#          | Parameter eksplisit (SKILL.md bagian 6)

## ============================================================
## 0. PCQ vs CAKE vs FQ_CODEL — MATRIKS PEMILIHAN (WAJIB DIJELASKAN)
## ============================================================
| Aspek | PCQ | CAKE | FQ_CODEL |
|---|---|---|---|
| Model | Pembagi rata per-IP klien | Anti-bufferbloat + per-flow fairness + AQM cerdas | Anti-bufferbloat + per-flow fairness |
| Kekuatan utama | Fair-share ribuan klien sederhana | Latency stabil di bawah beban penuh, anti bulk hogging | Serupa CAKE, lebih ringan, opsi lebih sedikit |
| Paling cocok | ISP ribuan klien, limit per-klien | WAN kecil-menengah (≤300Mbps), RT-RW Net, link bufferbloat | WAN menengah, CPU terbatas |
| Kontrol granular | pcq-rate per klien | bandwidth, rtt, nat, diffserv, dual-srchost/dsthost | limit, target, flows |
| Kelemahan | Latency bisa naik saat bulk tanpa prioritas | CPU lebih tinggi dari PCQ/FQ_CODEL | Tanpa fitur NAT-aware & rtt preset |

ATURAN PEMILIHAN skill ini:
1. Klien minta "semua klien dapat jatah sama" + jumlah besar → PCQ
   (playbook bandwidth-management).
2. Keluhan utama "ping naik saat ada yang download" (bufferbloat) /
   topologi WAN single/dual link → CAKE (atau FQ_CODEL bila CPU tipis).
3. Selalu tawarkan FQ_CODEL sebagai pengganti CAKE ber-CPU rendah.
4. Keduanya TIDAK menggantikan fungsi PCC/PBR — queue ≠ routing.

## ============================================================
## 1. DATA WAJIB SEBELUM CONFIG
## ============================================================
| Parameter | Sumber | Contoh |
|---|---|---|
| Total bandwidth WAN (AKURAT! shaper CAKE butuh angka nyata) | Speedtest hasil sesungguhnya, bukan paket | 185Mbps down / 95Mbps up |
| Interface WAN & LAN (NAMA ASLI) | Audit /interface print | ether1, ether5 |
| Model board CPU | /system resource print | RB5009 (CAKE ok >300Mbps), hEX (pakai FQ_CODEL utk >100Mbps) |
| Keluhan utama user | Wawancara | "Ping game melonjak saat ada yang download" |
| Klien prioritas perlu garansi? | Data user | Ya (game/VOIP) |

## PENTING ANGKA SHAPER:
## CAKE/FQ_CODEL membentuk trafik dengan mengantre — jadi bandwidth
## di-set 85-95% dari kapasitas ASLI (bukan paket) agar shaper yang
## pegang kendali, BUKAN buffer modem/ONT (itu sumber bufferbloat).
## Contoh: paket 200Mbps → speedtest asli 185Mbps → set 160-175Mbps.

## ============================================================
## 2. CARA 1 — SIMPLE QUEUE DENGAN CAKE (topologi sederhana,
##    1-2 WAN, tanpa queue tree)
## ============================================================
/queue type
add name=smi-cake-down kind=cake cake-bandwidth=[DOWN_EFEKTIF] \
    cake-nat=yes cake-rtt=100ms cake-diffserv=diffserv4 \
    comment="settingmikrotikindonesia.com - CAKE download anti-bufferbloat nat aware"
add name=smi-cake-up kind=cake cake-bandwidth=[UP_EFEKTIF] \
    cake-nat=yes cake-rtt=100ms cake-diffserv=diffserv4 \
    comment="settingmikrotikindonesia.com - CAKE upload anti-bufferbloat nat aware"

## PENJELASAN PARAMETER (WAJIB disampaikan, jangan set buta):
## - cake-bandwidth  : batas kapasitas — WAJIB angka efektif 85-95%.
## - cake-nat=yes    : fairness berdasarkan IP asli klien di belakang
##                     NAT (flow per-HOST bukan per-koneksi) — WAJIB
##                     untuk RT-RW Net/klien banyak di 1 NAT.
## - cake-rtt        : tunning sesuai topologi:
##                     datacenter/IX lokal  → 20ms-50ms
##                     internet umum ID     → 100ms
##                     satelit/intl jauh    → 300ms
## - cake-diffserv   : diffserv4 = hormati marking prioritas
##                     (sinergi dgn mangle smi-prio bila ada).
##                     Wanita kosongkan diffserv bila trafik tanpa marking.

/queue simple
add name=smi-cake-shaper target=[SUBNET_LAN]/24 interface=[IF-LAN] \
    queue=smi-cake-up/smi-cake-down max-limit=[DOWN_EFEKTIF]/[UP_EFEKTIF] \
    comment="settingmikrotikindonesia.com - Shaper CAKE total jaringan anti-bufferbloat"

## ============================================================
## 3. CARA 2 — FQ_CODEL (alternatif CPU lebih ringan)
## ============================================================
/queue type
add name=smi-fqcodel-down kind=fq-codel limit=10240 target=5ms interval=100ms \
    comment="settingmikrotikindonesia.com - FQ CODEL download anti-bufferbloat hemat CPU"
add name=smi-fqcodel-up kind=fq-codel limit=10240 target=5ms interval=100ms \
    comment="settingmikrotikindonesia.com - FQ CODEL upload anti-bufferbloat hemat CPU"

## PENJELASAN PARAMETER:
## - target=5ms   : latensi antre maksimal per flow sebelum mulai
##                  drop — 5ms standar; koneksi buruk naikkan 10-20ms.
## - interval=100ms: siklus kontrol drop — 100ms standar internet ID.
## - limit=10240  : ukuran antre maks paket — default aman jaringan
##                  besar; jaringan kecil bisa 2048 hemat RAM.

/queue simple
add name=smi-fqcodel-shaper target=[SUBNET_LAN]/24 interface=[IF-LAN] \
    queue=smi-fqcodel-up/smi-fqcodel-down max-limit=[DOWN_EFEKTIF]/[UP_EFEKTIF] \
    comment="settingmikrotikindonesia.com - Shaper FQ CODEL total jaringan"

## ============================================================
## 4. CARA 3 — CAKE DI QUEUE TREE (topologi kompleks: multi-WAN /
##    sudah ada tree PBR) — CAKE sebagai leaf, prioritas tetap jalan
## ============================================================
/queue type
add name=smi-cake-leaf-down kind=cake cake-bandwidth=[DOWN_EFEKTIF] cake-nat=yes \
    comment="settingmikrotikindonesia.com - CAKE leaf download pengganti PCQ"
add name=smi-cake-leaf-up kind=cake cake-bandwidth=[UP_EFEKTIF] cake-nat=yes \
    comment="settingmikrotikindonesia.com - CAKE leaf upload pengganti PCQ"

/queue tree
add name=smi-root-down parent=[IF-LAN] max-limit=[DOWN_EFEKTIF] queue=default \
    comment="settingmikrotikindonesia.com - Root download total"
add name=smi-prio-down parent=smi-root-down packet-mark=smi-prio-down \
    priority=1 queue=default \
    comment="settingmikrotikindonesia.com - Prioritas interaktif TANPA CAKE anti jitter ekstra"
add name=smi-klien-down parent=smi-root-down packet-mark=smi-klien-down \
    priority=4 queue=smi-cake-leaf-down \
    comment="settingmikrotikindonesia.com - Klien umum via CAKE fairness per host"

## RAHASIA KOMPOSISI (jelaskan ke user):
## - Prioritas 1 diberi queue DEFAULT (fifo ringan) — trafik interaktif
##   sudah di-layani dulu, tak perlu AQM berat.
## - CAKE hanya di leaf trafik umum — di sinilah fairness per-host dan
##   anti-bufferbloat bekerja, tanpa membebani trafik prioritas.
## - Ini komposisi paling optimal utk RT-RW Net: latency prioritas
##   tetap rendah + bulk tidak saling membanting.

## ============================================================
## 5. CAKE MULTI-WAN (1 instance CAKE PER WAN — DILARANG 1 untuk semua)
## ============================================================
## CAKE shaper menghitung kapasitas SATU link — multi-WAN = CAKE
## terpisah per arah per-WAN via simple queue per-interface:
/queue simple
add name=smi-cake-wan1-up target=0.0.0.0/0 interface=[IF-WAN1] \
    queue=smi-cake-wan1up/default max-limit=[UP1_EFEKTIF] \
    comment="settingmikrotikindonesia.com - CAKE upload WAN1 sesuai kapasitas asli"
add name=smi-cake-wan2-up target=0.0.0.0/0 interface=[IF-WAN2] \
    queue=smi-cake-wan2up/default max-limit=[UP2_EFEKTIF] \
    comment="settingmikrotikindonesia.com - CAKE upload WAN2 sesuai kapasitas asli"
## Download dibentuk di sisi LAN (iface LAN) karena shaping ingress
## masuk akal dilakukan setelah paket masuk router:
add name=smi-cake-wan-down target=[SUBNET_LAN]/24 interface=[IF-LAN] \
    queue=smi-cake-wandown/default max-limit=[DOWN_TOTAL_EFEKTIF] \
    comment="settingmikrotikindonesia.com - CAKE download gabungan di sisi LAN"
## Sinergi PBR: mangle to-WAN1/WAN2 bekerja SEBELUM queue — routing
## tidak terganggu; queue hanya membentuk keluar per-interface.

## ============================================================
## 6. KAPAN TIDAK MENYARANKAN CAKE (JUJUR KE USER)
## ============================================================
- Router CPU lemah (hEX/rb750gr3) + bandwidth >150Mbps → sarankan
  FQ_CODEL (atau kembali PCQ).
- Butuh limit rate TETAP per klien (paket jualan 3Mbps/5Mbps per
  orang) → itu PCQ/simple-queue, bukan CAKE (CAKE fair per-host
  dinamis, bukan tarif tetap).
- RIBUAN klien (>800 host aktif) → PCQ lebih teruji skala besar;
  CAKE per-host fairness makin berat seiring jumlah host.

## ============================================================
## 7. ANALISIS KONSEKUENSI (WAJIB)
## ============================================================
- KONSEKUENSI: bandwidth dibentuk 85-95% → speedtest TIDAK akan
  menunjukkan angka paket penuh. INI MEMANG TUJUANNYA (shaper pegang
  kendali). Jelaskan AGAR USER TIDAK KAGET — kesalahpahaman #1!
- KEUNTUNGAN: ping stabil di bawah beban penuh (bufferbloat mati),
  1 klien download tak menghancurkan game klien lain.
- RISIKO: CPU naik vs tanpa shaper — pantau /system resource cpu-load.
- RISIKO: angka bandwidth kebesaran → bufferbloat kembali; kekecilan
  → bandwidth terbuang. MITIGASI: kalibrasi speedtest 2-3 kali jam
  berbeda, iterasi set cake-bandwidth.

## ============================================================
## 8. VALIDASI (WAJIB)
## ============================================================
1. BUFFERBLOAT TEST (kunci utama): speedtest saat ping monitor jalan:
   /ping address=8.8.8.8 — jalankan terus; lalu speedtest full.
   Ping HARUS tetap < 30-50ms di atas baseline. Naik > 100ms = angka
   shaper kebesaran → turunkan cake-bandwidth, ulangi.
2. /queue simple print stats & /queue tree print stats — rate & drop
   terlihat; drop tinggi di CAKE = AQM bekerja (normal saat penuh).
3. Fairness: 2 host download paralel → masing ~setara (bukan 1 membul).
4. /system resource print — cpu-load < 70% saat jaringan penuh;
   lebih → migrasi ke FQ_CODEL / turunkan fitur (matikan nat/diffserv).
5. Trafik prioritas: klien game ping stabil walau bulk berjalan.

## ============================================================
## 9. ROLLBACK
## ============================================================
1. /queue simple disable [find name~"smi-"] — nonaktif tanpa hapus.
2. /queue tree disable [find name~"smi-"] — bila pakai tree.
3. Pulihkan dari /export file=backup-settingmikrotikindonesia
4. Catat angka kalibrasi terakhir baik (bandwidth, target, interval)
   di dokumen jaringan untuk iterasi berikutnya.
