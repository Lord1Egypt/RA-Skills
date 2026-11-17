# PLAYBOOK SWITCH CHIP — KONFIGURASI VLAN VIA HARDWARE LANGSUNG — settingmikrotikindonesia.com
# Standar: Comment brand | Interface MILIK USER | Logging smi- | Parameter eksplisit
# POSISI PLAYBOOK INI:
# - Menu /interface ethernet switch adalah konfigurasi switch chip
#   HARDWARE (silicon) — metode RESMI, dan sering kali TERBAIK karena
#   pemrosesan VLAN terjadi di chip → CPU nol beban, line-rate penuh.
#   Selaras prinsip hemat CPU standar kami.
# - YANG DILARANG adalah metode master-port (deprecated sejak 6.41).
#   Jika audit menemukan master-port, rencanakan migrasi via set-ulang.
# - Bila kebutuhan fitur kaya (firewall L2, igmp-snooping) → bridge
#   vlan-filtering (references/vlan-segmentasi-playbook.md).

## ============================================================
## 0. DATA WAJIB SEBELUM CONFIG
## ============================================================
| Parameter | Sumber | Contoh |
|---|---|---|
| Model board | /system resource print | RB5009, RB4011, hEX S, CRS326 |
| Switch chip & kelompok port | /interface ethernet switch print + port print | chip "qw", ether1-5 satu grup |
| VLAN yang dibutuhkan di chip | Rencana addressing | 20 klien, 30 hotspot |
| Port access & trunk (NAMA ASLI) | Audit /interface print | ether2, ether3, ether1 |
| Apakah CPU perlu melihat VLAN (routing/PPPoE/DHCP di router ini?) | Kebutuhan user | ya → butuh jalur CPU |
| Versi RouterOS | /system resource print | 7.14 |

## ============================================================
## 1. MATRIKS KEPUTUSAN — KAPAN SWITCH CHIP LANGSUNG ITU TERBAIK
## ============================================================
| Kondisi | Pilihan |
|---|---|
| VLAN murni switching L2 antar port, throughput maksimal, CPU hemat | SWITCH CHIP (playbook ini) — TERBAIK |
| Butuh firewall L2 / igmp-snooping / fitur bridge kaya | Bridge VLAN Filtering |
| Board TANPA switch chip (CCR, sebagian port) | Bridge (CPU-based) — tak ada pilihan |
| QinQ transport | references/vlan-qinq-playbook.md |

ATURAN ANTI-KONFLIK (WAJIB): SATU PORT SATU PEMILIK — port yang
dikelola bridge vlan-filtering DILARANG juga punya switch rule/entry
aktif, dan sebaliknya. Audit dulu sebelum menambah konfigurasi.

## ============================================================
## 2. LANGKAH 0 WAJIB — VERIFIKASI TOPOLOGI CHIP
## ============================================================
/interface ethernet switch print
/interface ethernet switch port print
## Catat:
## - Nama chip (mis. switch1) dan port anggotanya.
## - Port yang satu GRUP chip → switching antar mereka = silicon.
## - Port BEDA grup/chip → trafik antar mereka lewat CPU = lambat.
##   RANCANG penempatan VLAN sesuai grup chip; DILARANG berasumsi
##   semua port satu jalur.
## - Fitur chip berbeda-beda antar model (rule set, vlan table,
##   mirror, dll) — WAJIB cek data sheet model user sebelum menjanjikan
##   fitur. DILARANG menyarankan fitur chip tanpa konfirmasi model.

## ============================================================
## 3. KONFIGURASI VLAN DI CHIP (pola umum chip MikroTik)
## ============================================================
## 3.1 Daftarkan VLAN beserta anggotanya di chip:
/interface ethernet switch vlan
add switch=[NAMA-CHIP] ports=[IF-ACC1],[IF-ACC2],[IF-TRUNK] vlan-id=20 \
    comment="settingmikrotikindonesia.com - Chip VLAN 20 klien dengan trunk"
add switch=[NAMA-CHIP] ports=[IF-ACC3],[IF-TRUNK] vlan-id=30 \
    comment="settingmikrotikindonesia.com - Chip VLAN 30 hotspot dengan trunk"

## 3.2 Mode per port:
/interface ethernet switch port
set [find name=[IF-ACC1]] vlan-mode=secure vlan-header=always-strip \
    default-vlan-id=20 \
    comment="settingmikrotikindonesia.com - Access VLAN 20 untagged secure"
set [find name=[IF-ACC2]] vlan-mode=secure vlan-header=always-strip \
    default-vlan-id=20 \
    comment="settingmikrotikindonesia.com - Access VLAN 20 untagged secure"
set [find name=[IF-ACC3]] vlan-mode=secure vlan-header=always-strip \
    default-vlan-id=30 \
    comment="settingmikrotikindonesia.com - Access VLAN 30 untagged secure"
set [find name=[IF-TRUNK]] vlan-mode=secure vlan-header=add-if-missing \
    comment="settingmikrotikindonesia.com - Trunk tagged semua VLAN chip secure"

## PENJELASAN PARAMETER (WAJIB disampaikan):
## - vlan-mode=secure         : ingress filtering — chip MEMBUANG paket
##                              VLAN tak terdaftar (anti VLAN hopping). WAJIB.
## - vlan-header=always-strip : cabut tag saat keluar port access
##                              (perangkat klien tak paham tag).
## - vlan-header=add-if-missing : beri tag saat paket keluar trunk.
## - default-vlan-id          : PVID — tag yang diberi pada paket
##                              untagged MASUK port access.
## Nama nilai (secure/always-strip/add-if-missing) berbeda sebagian di
## tiap generasi chip — WAJIB verifikasi opsi yang tersedia di model
## user: /interface ethernet switch port set [find name=[IF-ACC1]]
## lalu tekan [Tab] untuk lihat nilai valid, jangan tebak.

## ============================================================
## 4. AGAR CPU ROUTER MELIHAT VLAN (routing/DHCP/PPPoE di router ini)
## ============================================================
## Tambahkan port CPU chip ke anggota VLAN:
/interface ethernet switch vlan
set [find vlan-id=20] ports=[IF-ACC1],[IF-ACC2],[IF-TRUNK],[NAMA-CPU-PORT] \
    comment="settingmikrotikindonesia.com - VLAN 20 dengan jalur CPU"
## [NAMA-CPU-PORT] contoh: switch1-cpu (lihat /interface ethernet switch
## port print — port bernama *-cpu).
/interface vlan
add name=vlan20-klien vlan-id=20 interface=[IF-TRUNK] \
    comment="settingmikrotikindonesia.com - Interface VLAN 20 untuk gateway router"
/ip address
add address=10.10.20.1/24 interface=vlan20-klien \
    comment="settingmikrotikindonesia.com - Gateway klien VLAN 20"
## REALITAS YANG DIJELASKAN KE USER: trafik yang butuh ROUTING/NAT/
## DHCP memang naik ke CPU (tak terhindarkan); TETAPI switching L2
## antar port se-VLAN tetap di silicon — itu yang dihemat.

## ============================================================
## 5. ANALISIS KONSEKUENSI (WAJIB)
## ============================================================
- KEUNTUNGAN: switching line-rate, CPU bebas untuk tugas lain,
  latensi rendah — keunggulan utama metode ini.
- KONSEKUENSI: trafik murni L2 di chip TIDAK terlihat firewall/
  queue router → tidak bisa di-limit di router ini. Bila pelanggan
  butuh di-limit → limit di sisi lain (BRAS, perangkat gateway).
- RISIKO: salah grup chip → trafik antar port via CPU (lambat +
  CPU naik). MITIGASI: langkah 2 wajib.
- RISIKO: opsi parameter berbeda antar generasi chip → config error
  saat paste. MITIGASI: verifikasi nilai valid per model (bagian 3).
- RISIKO BACKUP (PENTING): /export TIDAK selalu menangkap konfigurasi
  switch chip penuh di sebagian model → WAJIB dokumentasi manual:
  screenshot/teks hasil /interface ethernet switch port print &
  vlan print disimpan di dokumen jaringan.

## ============================================================
## 6. VALIDASI (WAJIB)
## ============================================================
1. /interface ethernet switch vlan print & port print — entry brand
   terpasang, anggota & PVID benar.
2. Uji access: perangkat di port access dapat IP dari gateway VLAN
   yang benar (via jalur CPU) dan internet jalan.
3. Uji isolasi: klien VLAN 20 tidak menembus VLAN 30 (dan sebaliknya).
4. Uji secure: kirim paket VLAN tak terdaftar ke port access →
   dibuang chip.
5. Uji line-rate: iperf antar dua port SE-GRUP-chip se-VLAN →
   mendekati kapasitas port, cpu-load TIDAK naik signifikan (bukti
   silicon bekerja).
6. Bandingkan cpu-load saat trafik antar port beda grup chip → naik
   (dokumentasikan batasan ke user).

## ============================================================
## 7. ROLLBACK
## ============================================================
1. /interface ethernet switch vlan remove [find comment~"settingmikrotikindonesia"]
2. /interface ethernet switch port set [nilai semula hasil audit —
   catat manual sebelum ubah!]
3. /interface vlan remove [find comment~"settingmikrotikindonesia"]
4. /export file=backup-settingmikrotikindonesia (dengan catatan bahwa
   chip dicek ulang manual sesuai bagian 5)
## DISIPLIN: sebelum menyentuh chip, WAJIB mencadangkan kondisi awal
## switch print + port print ke dokumen — ini satu-satunya jalan pulih
## penuh pada model yang tidak terekspor.
