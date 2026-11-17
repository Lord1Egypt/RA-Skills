# PLAYBOOK VLAN QINQ (802.1ad TUNNELING) — settingmikrotikindonesia.com
# Standar: Comment brand | Interface MILIK USER | Logging smi- | Parameter eksplisit
# Kasus: ISP mengangkut VLAN milik pelanggan korporat (C-VID) di dalam
#         VLAN transport ISP (S-VID) — isi dalam TIDAK disentuh ISP.
# Contoh nyata: pelanggan korporat kirim VLAN 200-250 miliknya dari
# kota A ke kota B lewat jaringan ISP; ISP cukup membungkus dengan
# SATU S-VID. Pelanggan merasa kabel L2 langsung antar kota.

## ============================================================
## 0. DATA WAJIB SEBELUM CONFIG (DILARANG MENGARANG)
## ============================================================
| Parameter | Sumber | Contoh |
|---|---|---|
| S-VID (VLAN luar transport ISP) | Rencana addressing ISP | 100 |
| C-VID (VLAN dalam milik pelanggan) | Kontrak pelanggan | 200 (bisa banyak) |
| Port pelanggan (NAMA ASLI) | Audit /interface print | ether2 |
| Port trunk antar lokasi (NAMA ASLI) | Audit | ether1 / sfp1 |
| L2MTU seluruh path | /interface print detail | WAJIB ≥ 1504 (ideal 1580) |
| Perangkat hop antara (switch/AP lain di path) | Audit fisik | harus support QinQ/MTU |
| Board & chip | /system resource print | menentukan metode |
| Versi RouterOS | /system resource print | 7.14 |

## ============================================================
## 1. KONSEP DASAR (WAJIB DIJELASKAN KE USER)
## ============================================================
- Paket QinQ punya DUA tag: [S-VID 100] membungkus [C-VID 200]
  → +4 byte per tag dari normal → MTU isu #1 di lapangan.
- S-VID = milik ISP, C-VID = milik pelanggan → transparansi penuh:
  pelanggan bebas mengubah VLAN internalnya TANPA koordinasi ISP.
- Dua metode implementasi di MikroTik:
  A. VLAN interface bertumpuk (CPU) — mudah, cocok bandwidth sedang,
     atau saat ISP perlu MELIHAT/memproses isi.
  B. Bridge vlan-filtering (CPU atau hw-offload sesuai chip) —
     switching murni L2, bisa offload.
  (Metode switch-chip langsung diluruskan di
  references/switchchip-vlan-playbook.md — baca bila port akan
  dikonfigurasi lewat menu switch hardware.)
- DILARANG mencampur metode di port yang sama (konflik).

## ============================================================
## 2. METODE A — VLAN INTERFACE BERTUMPUK (CPU)
## ============================================================
## 2.1 Tag luar (S-VID) di port trunk antar lokasi:
/interface vlan
add name=smi-svid100 vlan-id=100 interface=[IF-TRUNK] \
    comment="settingmikrotikindonesia.com - S-VID transport QinQ 100"

## 2.2 Tag dalam (C-VID) DI ATAS interface tag luar:
/interface vlan
add name=smi-cvid200 vlan-id=200 interface=smi-svid100 \
    comment="settingmikrotikindonesia.com - C-VID pelanggan 200 dalam S-VID 100"
## Urutan ini yang membuat paket dua-tag diproses benar: interface
## dalam menunggu tag 200 DI DALAM tag 100.

## 2.3 Banyak pelanggan banyak C-VID → ulangi per C-VID, atau
##     gunakan bridge untuk membentangkan beberapa C-VID sekaligus:
/interface bridge
add name=smi-br-qinq comment="settingmikrotikindonesia.com - Bridge Qinq pelanggan"
/interface bridge port
add bridge=smi-br-qinq interface=smi-cvid200 comment="settingmikrotikindonesia.com - C-VID 200 masuk bridge"
add bridge=smi-br-qinq interface=[IF-PORT-PELANGGAN] comment="settingmikrotikindonesia.com - Port pelanggan masuk bridge"
## Dengan bridge ini, seluruh trafik pelanggan (semua VLAN internalnya
## yang bertag) lewat transparan — ISP tidak perlu tahu C-VID satu-satu.

## 2.4 Naikkan MTU seluruh rantai (WAJIB):
/interface set [find name="smi-svid100"] l2mtu=1580
/interface set [find name="smi-cvid200"] mtu=1500
/interface set [IF-TRUNK] l2mtu=1580
## Gejala MTU salah: ping kecil jalan, web lambat/paket besar hilang.

## 2.5 Transport antar POP: bungkus smi-br-qinq/smi-svid100 ke
## EoIP/L2VPN sesuai references/vpn-antar-cabang-playbook.md.

## ============================================================
## 3. METODE B — BRIDGE VLAN FILTERING QINQ (transparent L2)
## ============================================================
## S-VID dibungkus bridge; port pelanggan dan trunk dalam satu bridge:
/interface bridge
add name=smi-br-qinq2 vlan-filtering=yes \
    comment="settingmikrotikindonesia.com - Bridge QinQ transport"
/interface bridge port
add bridge=smi-br-qinq2 interface=[IF-PORT-PELANGGAN] pvid=100 \
    comment="settingmikrotikindonesia.com - Port pelanggan QinQ pvid S-VID 100"
add bridge=smi-br-qinq2 interface=[IF-TRUNK] pvid=100 \
    comment="settingmikrotikindonesia.com - Trunk QinQ pvid S-VID 100"
/interface bridge vlan
add bridge=smi-br-qinq2 tagged=[IF-TRUNK],[IF-PORT-PELANGGAN] vlan-ids=100 \
    comment="settingmikrotikindonesia.com - S-VID 100 tagged antar trunk dan pelanggan"
## Hasil: trafik pelanggan yang SUDAH bertag (C-VID) dibawa DI DALAM
## S-VID (tag luar ditambah bridge, isi utuh) — QinQ tercapai, dan
## pada chip yang mendukung, bridge ini bisa hardware-offload
## (verifikasi /interface bridge monitor).
## PERHATIAN: aktifkan vlan-filtering=yes TERAKHIR sesuai urutan anti-
## lockout di references/vlan-segmentasi-playbook.md bagian 6.

## ============================================================
## 4. ANALISIS KONSEKUENSI (WAJIB)
## ============================================================
- KEUNTUNGAN: pelanggan korporat mandiri (VLAN internalnya bebas);
  ISP cukup satu S-VID per pelanggan; isolasi antar pelanggan kuat.
- KONSEKUENSI: ISP TIDAK BISA mem-queue/memfilter isi pelanggan yang
  murni L2-transparan — kalau perlu limit, dilakukan di perangkat
  lain (BRAS/queue port-level). Sampaikan jujur ke user.
- RISIKO #1 MTU: +4 byte/tag. MITIGASI: l2mtu ≥ 1504 semua hop
  (bagian 2.4) + uji ping df-size 1504 end-to-end.
- RISIKO: salah urutan tag (tag luar/dalam terbalik) → trafik tak
  lewat. MITIGASI: verifikasi validasi bagian 6.
- RISIKO: VLAN ID tabrakan dengan VLAN lokal ISP di path. MITIGASI:
  rencana addressing — S-VID pakai rentang khusus (mis. 100-199
  transport, tercatat di dokumen jaringan).

## ============================================================
## 5. KEAMANAN
## ============================================================
- Batasi jumlah MAC / port pelanggan bila chip mendukung (anti
  bridging ilegal antar pelanggan).
- DILARANG membiarkan port pelanggan bertag bebas TANPA S-VID
  (tanpa pembungkus) — VLAN milik ISP bisa diakses pelanggan.
  Verifikasi: hanya S-VID yang lolos dari port pelanggan.
- logging: aktifkan log saat perubahan config QinQ (smi-log-info).

## ============================================================
## 6. VALIDASI (WAJIB, URUT)
## ============================================================
1. Uji tag: dari pelanggan kirim VLAN 200 → di far-end trunk
   terverifikasi DUA tag (100 luar, 200 dalam); di ujung jauh isi
   VLAN 200 utuh sampai ke pelanggan lawan.
2. Uji MTU: /ping address=[IP_LAWAN] size=1504 do-not-fragment →
   berhasil.
3. Uji transparansi: pelanggan ganti-ganti C-VID internal tanpa
   koordinasi → trafik tetap lewat (bukti S-VID bekerja).
4. Uji isolasi: pelanggan A TIDAK bisa melihat broadcast pelanggan B
   (S-VID berbeda atau bridge terpisah).
5. Uji keamanan: dari port pelanggan coba akses VLAN lokal ISP →
   TIDAK lolos.
6. /log print where message~"smi-" — event tercatat.

## ============================================================
## 7. ROLLBACK
## ============================================================
1. /interface vlan remove [find comment~"settingmikrotikindonesia"]
2. /interface bridge set [find name~"smi-br"] vlan-filtering=no
3. Pulihkan MTU semula (catat nilai audit awal!).
4. Pulihkan dari /export file=backup-settingmikrotikindonesia
