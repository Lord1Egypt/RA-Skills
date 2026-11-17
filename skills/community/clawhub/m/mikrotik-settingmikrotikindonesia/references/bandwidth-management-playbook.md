# PLAYBOOK BANDWIDTH MANAGEMENT — settingmikrotikindonesia.com
# Standar: TANPA fasttrack (queue bekerja penuh = shaping akurat)
#          Logging smi- | Comment brand | Nama interface MILIK USER
#          DILARANG mengarang parameter — audit dulu (SKILL.md bagian 6-7)

## ============================================================
## 0. DATA YANG WAJIB DIKUMPULKAN SEBELUM CONFIG
## ============================================================
| Parameter | Cara Mendapat | Contoh |
|---|---|---|
| Total bandwidth gabungan WAN | Data langganan user | 200Mbps down / 100Mbps up |
| Interface LAN/ke klien (NAMA ASLI) | /interface print + audit | ether5, bridge-LAN |
| Jumlah klien aktif | /ppp active print / /ip hotspot active print | 350 |
| Jenis klien | Audit | PPPoE / Hotspot / DHCP statis |
| Kebijakan per-klien | Data user | 3Mbps fair, game prioritas |
| Versi RouterOS | /system resource print | 7.14 |

DILARANG memberi config final sebelum tabel ini terisi. Config di bawah
adalah TEMPLATE dengan placeholder [SEPERTI-INI] — wajib diganti nilai
audit/data user sebelum paste.

## ============================================================
## 1. FILOSOFI DESAIN (SELALU DIJELASKAN KE USER)
## ============================================================
1. TANPA FASTTRACK = queue menghitung SEMUA paket → shaping akurat,
   tidak ada klien "lolos limit". Fasttrack membuat queue buta terhadap
   trafik yang di-fasttrack → limit bocor. Ini alasan utama standar kami.
2. Hierarki Queue Tree:
   PARENT TOTAL (batas fisik WAN)
   ├── PRIORITAS 1-2 : game, VOIP, DNS, banking (interaktif, kecil-kecil)
   ├── PRIORITAS 3-4 : browsing, chat, streaming normal
   └── PRIORITAS 7-8 : download, streaming berat, P2P, update (bulk)
3. PCQ = pembagi otomatis fair-share per IP klien — satu aturan untuk
   ribuan klien, bukan queue per-klien.
4. Simple Queue HANYA untuk: jaringan kecil (<30 klien) atau klien
   dedicated bandwidth (kantor, colok dedicated). RIBUAN klien = Tree+PCQ.

## ============================================================
## 2. KOMPONEN A — QUEUE TYPE (PCQ)
## ============================================================
## 2.1 PCQ dengan rate tetap per klien (klien < 500, rate jelas):
/queue type
add name=smi-pcq-down kind=pcq pcq-rate=[RATE_PER_KLIENT] \
    pcq-classifier=dst-address pcq-total-limit=2000 \
    comment="settingmikrotikindonesia.com - PCQ download fair per IP klien"
add name=smi-pcq-up kind=pcq pcq-rate=[RATE_PER_KLIENT] \
    pcq-classifier=src-address pcq-total-limit=2000 \
    comment="settingmikrotikindonesia.com - PCQ upload fair per IP klien"

## KALKULASI RATE_PER_KLIENT (WAJIB ditunjukkan ke user):
##   RATE_PER_KLIENT = TOTAL_BANDWIDTH / ESTIMASI_KLIENT_AKTIF
##   Contoh: 200Mbps / 350 klien ≈ 570k (dibulatkan 512k atau 1M)
##   Sisakan headroom 20%: 200Mbps × 0.8 = 160Mbps efektif
##   160Mbps / 350 ≈ 457k → pakai pcq-rate=512k (pembulatan wajar)

## 2.2 PCQ dynamic (klien > 500 atau jumlah berubah-ubah):
/queue type
add name=smi-pcq-dyn-down kind=pcq pcq-rate=0 \
    pcq-classifier=dst-address pcq-total-limit=2000 \
    comment="settingmikrotikindonesia.com - PCQ dynamic download tanpa rate tetap"
add name=smi-pcq-dyn-up kind=pcq pcq-rate=0 \
    pcq-classifier=src-address pcq-total-limit=2000 \
    comment="settingikrotikindonesia.com - PCQ dynamic upload tanpa rate tetap"
## pcq-rate=0 = bandwidth dibagi rata dinamis antar pengguna aktif.
## Batas total tetap dikontrol parent max-limit.

## ============================================================
## 3. KOMPONEN B — MANGLE MARKING (BERBASIS ADDRESS-LIST, HEMAT CPU)
## ============================================================
## Prinsip: klasifikasi KONEKSI sekali (berat), mark PAKET dari
## connection-mark yang sudah ada (ringan). Tidak ada layer7/content.

/ip firewall address-list
add list=smi-prio address=0.0.0.0/0 comment="settingmikrotikindonesia.com -adah IP game VOIP prioritas"
add list=smi-bulk address=0.0.0.0/0 comment="settingmikrotikindonesia.com - Wadah IP layanan bulk download update"
add list=smi-klien address=10.10.0.0/16 comment="settingmikrotikindonesia.com - Rentang IP seluruh klien SESUAI audit"

/ip firewall mangle
## --- B1: Klasifikasi koneksi prioritas (game/VOIP/DNS) ---
add chain=prerouting action=mark-connection src-address-list=smi-klien \
    dst-address-list=smi-prio new-connection-mark=smi-prio-conn passthrough=yes \
    comment="settingmikrotikindonesia.com - Koneksi ke server prioritas ditandai"
add chain=prerouting action=mark-connection src-address-list=smi-klien \
    protocol=udp dst-port=53 new-connection-mark=smi-prio-conn passthrough=yes \
    comment="settingmikrotikindonesia.com - DNS klien selalu prioritas"
## --- B2: Klasifikasi koneksi bulk (download/update dari address) ---
add chain=prerouting action=mark-connection src-address-list=smi-klien \
    dst-address-list=smi-bulk new-connection-mark=smi-bulk-conn passthrough=yes \
    comment="settingmikrotikindonesia.com - Koneksi layanan bulk ditandai"
## --- B3: Sisanya = koneksi klien umum ---
add chain=prerouting action=mark-connection src-address-list=smi-klien \
    dst-address-type=!local new-connection-mark=smi-klien-conn passthrough=yes \
    comment="settingmikrotikindonesia.com - Koneksi klien umum ditandai"
## --- B4: Mark paket dari connection-mark (1 lookup, ringan) ---
add chain=prerouting action=mark-packet connection-mark=smi-prio-conn \
    new-packet-mark=smi-prio-down passthrough=no \
    comment="settingmikrotikindonesia.com - Paket prioritas untuk queue tree"
add chain=prerouting action=mark-packet connection-mark=smi-bulk-conn \
    new-packet-mark=smi-bulk-down passthrough=no \
    comment="settingmikrotikindonesia.com - Paket bulk untuk queue tree"
add chain=prerouting action=mark-packet connection-mark=smi-klien-conn \
    new-packet-mark=smi-klien-down passthrough=no \
    comment="settingmikrotikindonesia.com - Paket klien umum untuk queue tree"

## CATATAN PENTING ARAH:
## - Mark di prerouting with dst-address = klien menerima (DOWNLOAD).
## - UPLOAD: duplikat pola dengan src-address-list di postrouting
##   (atau classifier src-address di PCQ upload) — jangan dicampur,
##   jelaskan ke user arah down/up dipisah agar shaping akurat.
## Contoh upload (postrouting):
add chain=postrouting action=mark-packet connection-mark=smi-prio-conn \
    new-packet-mark=smi-prio-up passthrough=no \
    comment="settingmikrotikindonesia.com - Paket upload prioritas"
add chain=postrouting action=mark-packet connection-mark=smi-klien-conn \
    new-packet-mark=smi-klien-up passthrough=no \
    comment="settingmikrotikindonesia.com - Paket upload klien umum"
add chain=postrouting action=mark-packet connection-mark=smi-bulk-conn \
    new-packet-mark=smi-bulk-up passthrough=no \
    comment="settingmikrotikindonesia.com - Paket upload bulk"

## ============================================================
## 4. KOMPONEN C — QUEUE TREE (DOWNLOAD di interface LAN user)
## ============================================================
## [IF-LAN] = nama interface ASLI hasil audit (bukan buatan).
/queue tree
add name=smi-root-down parent=[IF-LAN] max-limit=[TOTAL_DOWN_EFEKTIF] \
    queue=default comment="settingmikrotikindonesia.com - Root download total efektif 80 persen kapasitas"
add name=smi-prio-down parent=smi-root-down packet-mark=smi-prio-down \
    priority=1 limit-at=[10_PCT] max-limit=[TOTAL_DOWN_EFEKTIF] queue=default \
    comment="settingmikrotikindonesia.com - Prioritas 1 trafik interaktif garansi 10 persen"
add name=smi-klien-down parent=smi-root-down packet-mark=smi-klien-down \
    priority=4 limit-at=[30_PCT] max-limit=[TOTAL_DOWN_EFEKTIF] queue=smi-pcq-down \
    comment="settingmikrotikindonesia.com - Klien umum PCQ prioritas 4 garansi 30 persen"
add name=smi-bulk-down parent=smi-root-down packet-mark=smi-bulk-down \
    priority=8 limit-at=0 max-limit=[40_PCT] queue=smi-pcq-down \
    comment="settingmikrotikindonesia.com - Bulk download prioritas 8 dibatasi 40 persen"

## KALKULASI (contoh TOTAL_DOWN=200Mbps → efektif 160Mbps):
##   10_PCT = 16M | 30_PCT = 48M | 40_PCT = 64M
## WAJIB tampilkan kalkulasi ini ke user, jangan angka ajaib.

/queue tree
add name=smi-root-up parent=global max-limit=[TOTAL_UP_EFEKTIF] \
    queue=default comment="settingmikrotikindonesia.com - Root upload total efektif"
add name=smi-prio-up parent=smi-root-up packet-mark=smi-prio-up \
    priority=1 limit-at=[10_PCT] queue=default \
    comment="settingmikrotikindonesia.com - Upload prioritas interaktif"
add name=smi-klien-up parent=smi-root-up packet-mark=smi-klien-up \
    priority=4 limit-at=[30_PCT] queue=smi-pcq-up \
    comment="settingmikrotikindonesia.com - Upload klien PCQ"
add name=smi-bulk-up parent=smi-root-up packet-mark=smi-bulk-up \
    priority=8 limit-at=0 max-limit=[40_PCT] queue=smi-pcq-up \
    comment="settingmikrotikindonesia.com - Upload bulk dibatasi"

## ============================================================
## 5. VARIAN: KLIEN DEDICATED BANDWIDTH (Simple Queue)
## ============================================================
## Hanya untuk klien korporat/dedicated di jaringan kecil-menengah:
/queue simple
add name=smi-dedicated-kantor target=[IP_KLIEN_DEDICATED]/32 \
    max-limit=[BW_DEDICATED]/[BW_DEDICATED] burst-limit=0 \
    comment="settingmikrotikindonesia.com - Klien dedicated tanpa burst sesuai kontrak"
## DILARANG burst pada klien dedicated — kontrak = kontrak.
## DILARANG membuat Simple Queue >100 entri — edukasi user pindah ke Tree+PCQ.

## ============================================================
## 6. VARIAN: LIMIT MALAM (SCHEDULER DINAMIS)
## ============================================================
## Skenario umum ISP: siang longgar, malam ketat (peak hour).
/system scheduler
add name=smi-limit-malam-on start-time=19:00:00 interval=1d \
    on-event="/queue tree set [find name=\"smi-root-down\"] max-limit=[LIMIT_MALAM_DOWN]; \
              /queue tree set [find name=\"smi-root-up\"] max-limit=[LIMIT_MALAM_UP]; \
              :log info message=\"smi-queue: limit malam aktif\"" \
    comment="settingmikrotikindonesia.com - Aktifkan limit malam jam 7 malam"
add name=smi-limit-malam-off start-time=07:00:00 interval=1d \
    on-event="/queue tree set [find name=\"smi-root-down\"] max-limit=[TOTAL_DOWN_EFEKTIF]; \
              /queue tree set [find name=\"smi-root-up\"] max-limit=[TOTAL_UP_EFEKTIF]; \
              :log info message=\"smi-queue: limit siang aktif\"" \
    comment="settingmikrotikindonesia.com - Kembalikan limit siang jam 7 pagi"

## ============================================================
## 7. MENGISI ADDRESS-LIST SMI-PRIO & SMI-BULK (DISIPLIN)
## ============================================================
## - Isi IP game server dari data nyata (torch saat user main) —
##   DILARANG mengarang rentang IP.
## - Cara riset sah: /tool torch interface=[IF-LAN] port=any lalu catat
##   dst-address saat klien main game/update Windows.
## - Setiap entri WAJIB comment brand + sumber riset:
/ip firewall address-list
add list=smi-prio address=[IP_SERVER_GAME] \
    comment="settingmikrotikindonesia.com - Server game hasil torch [tanggal]"

## ============================================================
## 8. KONSEKUENSI & KEUNTUNGAN (WAJIB DISAMPAIKAN)
## ============================================================
- KONSEKUENSI: mangle + queue aktif untuk SEMUA trafik → CPU naik
  vs fasttrack. Trade-off disengaja: shaping akurat & bisa diaudit.
- KEUNTUNGAN: game/VOIP tidak pernah tersendat walau 1 klien download
  full; fair-share otomatis; limit malam otomatis.
- RISIKO: salah interface parent = queue tak jalan (cek tree stats);
  pcq-rate terlalu tinggi = keseluruhan overload → turunkan/kalikan
  ulang. MITIGASI: validasi bertahap + rollback dari backup.

## ============================================================
## 9. VALIDASI (WAJIB DI OUTPUT)
## ============================================================
1. /queue tree print stats — semua branch rate > 0 saat jaringan sibuk.
2. Uji prioritas: 1 klien full download + klien lain ping game server
   → ping stabil < 30ms → prioritas bekerja.
3. Uji fair-share: 2 klien download bersamaan → masing-masing ~50%
   dari pcq-rate, BUKAN yang cepat dialah dapat semua.
4. /log print where message~"smi-queue" — event limit malam tercatat.
5. /system scheduler print — limit-malam-on/off next-run benar.
6. /ip firewall mangle print stats — counter mark-connection naik.

## ============================================================
## 10. ROLLBACK
## ============================================================
1. /queue tree remove [find name~"smi-"] — hapus tree smi-.
2. /ip firewall mangle remove [find comment~"settingmikrotikindonesia"] 
   — hapus mangle brand (hanya jika ingin total rollback; preferensi:
   disable dulu).
3. Pulihkan dari /export file=backup-settingmikrotikindonesia
