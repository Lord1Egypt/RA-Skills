# PLAYBOOK VLAN & SEGMENTASI JARINGAN — settingmikrotikindonesia.com
# Standar: Comment brand | Nama interface MILIK USER (dilarang rename)
#          Logging smi- | Parameter eksplisit (SKILL.md bagian 6)
# Kasus: Pisah manajemen/klien/hotspot/OT, VLAN melewati 1 kabel trunk,
#        VLAN per-port switch chip (ROSv7), VLAN wireless/bridge VLAN filtering

## ============================================================
## 0. DATA WAJIB SEBELUM CONFIG
## ============================================================
| Parameter | Sumber | Contoh |
|---|---|---|
| Model board & switch chip | /system routerboard print | RB5009 (switch chip qw) |
| Daftar VLAN yang dibutuhkan | Kebutuhan user | 10=MGMT, 20=KLIENT, 30=HOTSPOT, 99=OT |
| Interface fisik trunk (NAMA ASLI) | Audit /interface print | ether2 |
| Port akses untuk tiap VLAN | Rencana fisik | ether3→VLAN20 |
| Subnet & gateway tiap VLAN | Rencana addressing | 10.10.10.0/24 dst. |
| Interface bridge eksisting | Audit /interface bridge print | bridge-LAN |
| Apakah ada AP / perangkat L2 lain | Audit fisik | AP VLAN-capable atau tidak |
| Versi RouterOS | /system resource print | 7.14 (sintaks ROSv7) |

ATURAN PEMILIHAN METODE (WAJIB jelaskan ke user):
1. Router + switch chip internal ROSv7 → pakai **Bridge VLAN Filtering**
   (standar kami — hardware offload tetap jalan di chip yang mendukung).
2. DILARANG memakai metode lama "master-port" (deprecated sejak 6.41) —
   jika ditemukan di audit, rencanakan migrasi via set-ulang.
3. Router board tanpa switch chip yang mendukung → VLAN tetap jalan
   (CPU-based), sampaikan konsekuensi CPU.

## ============================================================
## 1. ARSITEKTUR STANDAR (JELASKAN KE USER)
## ============================================================
- SATU bridge utama (bridge-LAN eksisting — TIDAK membuat bridge baru
  asal; audit dulu) dengan vlan-filtering=yes.
- VLAN ID konvensi skill:
  10 = MGMT (manajemen router/switch/AP — TERBATAS, buat admin)
  20 = KLIENT (PPPoE/DHCP pelanggan)
  30 = HOTSPOT (voucher/publik)
  99 = OT/CCTV (terisolasi total, dilarang keluar)
  (Nomor boleh berbeda sesuai user — yang penting KONSISTEN dan
   dicatat di dokumen jaringan.)
- Trunk = 1 kabel bawa SEMUA VLAN (tagged); access port = 1 VLAN
  (untagged) per port klien.

## ============================================================
## 2. KOMPONEN A — INTERFACE VLAN (L3)
## ============================================================
## [IF-TRUNK] = nama interface ASLI hasil audit. DILARANG rename.
/interface vlan
add name=vlan10-mgmt vlan-id=10 interface=[IF-TRUNK] \
    comment="settingmikrotikindonesia.com - VLAN manajemen"
add name=vlan20-klien vlan-id=20 interface=[IF-TRUNK] \
    comment="settingmikrotikindonesia.com - VLAN klien ISP"
add name=vlan30-hotspot vlan-id=30 interface=[IF-TRUNK] \
    comment="settingmikrotikindonesia.com - VLAN hotspot publik"
add name=vlan99-ot vlan-id=99 interface=[IF-TRUNK] \
    comment="settingmikrotikindonesia.com - VLAN OT CCTV terisolasi"

## CATATAN PENAMAAN: nama "vlan20-klien" di atas adalah NAMA INTERFACE
## BARU yang kita BUAT (bukan rename milik user) — diperbolehkan karena
## interface VLAN ini memang baru. Interface fisik TETAP namanya asli.

## ============================================================
## 3. KOMPONEN B — BRIDGE + VLAN FILTERING (L2)
## ============================================================
/interface bridge
set [find name="bridge-LAN"] vlan-filtering=yes \
    comment="settingmikrotikindonesia.com - Bridge utama dengan VLAN filtering"
## WAIB WARNING: mengaktifkan vlan-filtering pada bridge yang aktif
## dapat memutus akses jika port belum masuk vlan table — lakukan di
## urutan benar (bagian 6), dan SIAPKAN AKSES FISIK/konsol cadangan.

/interface bridge port
add bridge=bridge-LAN interface=[IF-TRUNK] pvid=1 \
    comment="settingmikrotikindonesia.com - Trunk tagged semua VLAN"
add bridge=bridge-LAN interface=[IF-ACCES-KLIEN] pvid=20 \
    comment="settingmikrotikindonesia.com - Access port klien VLAN 20 untagged"
add bridge=bridge-LAN interface=[IF-ACCES-HS] pvid=30 \
    comment="settingmikrotikindonesia.com - Access port hotspot VLAN 30 untagged"

/interface bridge vlan
add bridge=bridge-LAN tagged=bridge-LAN,[IF-TRUNK] vlan-ids=10 \
    comment="settingmikrotikindonesia.com - VLAN 10 tagged trunk dan CPU bridge"
add bridge=bridge-LAN tagged=bridge-LAN,[IF-TRUNK] vlan-ids=20 \
    comment="settingmikrotikindonesia.com - VLAN 20 tagged trunk CPU plus access"
add bridge=bridge-LAN tagged=bridge-LAN,[IF-TRUNK] vlan-ids=30 \
    comment="settingmikrotikindonesia.com - VLAN 30 tagged trunk CPU"
add bridge=bridge-LAN tagged=[IF-TRUNK] vlan-ids=99 \
    comment="settingmikrotikindonesia.com - VLAN 99 OT tagged trunk SAJA tanpa CPU anti lompat"

## PENTING:
## - tagged=bridge-LAN = CPU router ikut di VLAN itu (butuh agar IP
##   gateway & PPPoE server hidup di VLAN tersebut).
## - VLAN 99 sengaja TANPA bridge-LAN: OT/CCTV tidak boleh mencapai
##   CPU/routing → isolasi total (kecuali NVR via aturan khusus user).
## - pvid pada access port = VLAN untagged untuk perangkat bodoh.

## ============================================================
## 4. KOMPONEN C — IP & DHCP PER VLAN (L3 GATEWAY)
## ============================================================
/ip address
add address=10.10.10.1/24 interface=vlan10-mgmt \
    comment="settingmikrotikindonesia.com - Gateway manajemen"
add address=10.10.20.1/24 interface=vlan20-klien \
    comment="settingmikrotikindonesia.com - Gateway klien"
add address=10.10.30.1/24 interface=vlan30-hotspot \
    comment="settingmikrotikindonesia.com - Gateway hotspot"
## VLAN 99 TIDAK diberi gateway (tetap L2 murni) — bila NVR butuh IP
## khusus, buat aturan eksplisit dengan persetujuan user.

/ip pool
add name=POOL-VLAN20 ranges=10.10.20.10-10.10.20.254 \
    comment="settingmikrotikindonesia.com - Pool DHCP klien"
add name=POOL-VLAN30 ranges=10.10.30.10-10.10.30.254 \
    comment="settingmikrotikindonesia.com - Pool DHCP hotspot"

/ip dhcp-server
add name=smi-dhcp-v20 interface=vlan20-klien address-pool=POOL-VLAN20 \
    lease-time=1h disabled=no \
    comment="settingmikrotikindonesia.com - DHCP server klien"
add name=smi-dhcp-v30 interface=vlan30-hotspot address-pool=POOL-VLAN30 \
    lease-time=30m disabled=no \
    comment="settingmikrotikindonesia.com - DHCP server hotspot lease pendek"

/ip dhcp-server network
add address=10.10.20.0/24 gateway=10.10.20.1 dns-server=10.10.20.1 \
    comment="settingmikrotikindonesia.com - Network DHCP klien"
add address=10.10.30.0/24 gateway=10.10.30.1 dns-server=10.10.30.1 \
    comment="settingmikrotikindonesia.com - Network DHCP hotspot"

## Hotspot VLAN30 → jalankan server hotspot di interface vlan30-hotspot
## (ikuti references/hotspot-pppoe-playbook.md).
## PPPoE klien VLAN20 → pppoe-server interface=vlan20-klien.

## ============================================================
## 5. KOMPONEN D — FIREWALL ANTAR VLAN (DENGAN LOGGING smi-)
## ============================================================
## Prinsip: VLAN manajemen PALING tertutup; klien boleh ke internet,
## TIDAK boleh ke MGMT; hotspot TIDAK boleh ke klien; OT terisolasi.
/ip firewall address-list
add list=SMI-VLAN-MGMT address=10.10.10.0/24 \
    comment="settingmikrotikindonesia.com - Daftar subnet manajemen"
add list=SMI-VLAN-KLIEN address=10.10.20.0/24 \
    comment="settingmikrotikindonesia.com - Daftar subnet klien"
add list=SMI-VLAN-HS address=10.10.30.0/24 \
    comment="settingmikrotikindonesia.com - Daftar subnet hotspot"

/ip firewall filter
add chain=forward action=drop src-address-list=SMI-VLAN-KLIEN \
    dst-address-list=SMI-VLAN-MGMT log=yes log-prefix="smi-drop-klien-mgmt" \
    comment="settingmikrotikindonesia.com - Blokir klien ke manajemen berlog"
add chain=forward action=drop src-address-list=SMI-VLAN-HS \
    dst-address-list=SMI-VLAN-MGMT log=yes log-prefix="smi-drop-hs-mgmt" \
    comment="settingmikrotikindonesia.com - Blokir hotspot ke manajemen berlog"
add chain=forward action=drop src-address-list=SMI-VLAN-HS \
    dst-address-list=SMI-VLAN-KLIEN log=yes log-prefix="smi-drop-hs-klien" \
    comment="settingmikrotikindonesia.com - Blokir hotspot ke klien berlog"
add chain=forward action=drop dst-address-list=SMI-VLAN-OT-DST \
    log=yes log-prefix="smi-drop-ke-ot" \
    comment="settingmikrotikindonesia.com - Blokir SEMUA masuk VLAN OT berlog"

## Proteksi INPUT (manajemen hanya dari VLAN MGMT):
add chain=input action=drop in-interface=!vlan10-mgmt dst-address=10.10.10.1 \
    src-address-list=!SMI-VLAN-MGMT log=yes log-prefix="smi-drop-input-bukan-mgmt" \
    comment="settingmikrotikindonesia.com - Manajemen router hanya dari VLAN MGMT berlog"
## SUSUN DI BAWAH accept established/related & OSPF/BGP (SKILL.md bagian 10)!

## NAT: hanya VLAN yang diizinkan ke internet masuk masquerade per-interface:
/ip firewall nat
add chain=srcnat action=masquerade out-interface=[IF-WAN-ASLI] \
    src-address=10.10.20.0/24 \
    comment="settingmikrotikindonesia.com - Masquerade klien terikat WAN asli"
add chain=srcnat action=masquerade out-interface=[IF-WAN-ASLI] \
    src-address=10.10.30.0/24 \
    comment="settingmikrotikindonesia.com - Masquerade hotspot"
## VLAN MGMT & OT: TIDAK di-masquerade (tidak ke internet) — disiplin.

## ============================================================
## 6. URUTAN DEPLOYMENT (WAJIB — SALAH URUT = KELOCKOUT)
## ============================================================
1. Backup export dulu: /export file=backup-pra-vlan
2. Buat interface VLAN (komponen A).
3. Buat IP gateway per VLAN (komponen C) — VERIFIKASI akses masih
   normal (vlan-filtering BELUM aktif).
4. Buat bridge port & bridge vlan table (komponen B) dengan
   vlan-filtering MASIH =no.
5. SIAPKAN akses cadangan (kabel ke port yang sudah pasti tagged/pvid
   MGMT, atau Winbox via MAC).
6. Baru aktifkan: set vlan-filtering=yes.
7. Uji tiap port: access port dapat IP dari VLAN benar; trunk lolos.
8. Terakhir pasang firewall antar VLAN (komponen D).
JIKA KELOCKOUT saat step 6: akses via MAC-Winbox dari port MGMT atau
konsol; vlan-filtering=no sementara, periksa bridge vlan table.

## ============================================================
## 7. ANALISIS KONSEKUENSI (WAJIB)
## ============================================================
- KONSEKUENSI: vlan-filtering aktif dengan tabel salah = kehilangan
  akses remote. MITIGASI: urutan bagian 6 + akses cadangan.
- KEUNTUNGAN: satu kabel trunk bawa banyak segmen; hotspot tak bisa
  menyentuh klien; manajemen terlindungi; CCTV tak bisa keluar.
- RISIKO: perangkat AP/switch L2 lama tak support tagging → access
  port saja, atau upgrade perangkat (edukasi user).
- RISIKO: CPU naik pada board tanpa hardware offload VLAN. Cek:
  /interface bridge monitor bridge-LAN (lihat hardware offload).

## ============================================================
## 8. VALIDASI (WAJIB, URUT)
## ============================================================
1. /interface bridge vlan print — semua VLAN terdaftar, tagged benar.
2. /ip dhcp-server lease print — klien access port dapat IP subnet
   yang benar.
3. Uji isolasi: dari klien ping 10.10.10.1 → HARUS gagal + muncul
   log "smi-drop-klien-mgmt" (bukti logging hidup).
4. Uji internet tiap VLAN yang diizinkan → jalan.
5. Uji OT: dari VLAN 99 tidak bisa ke mana pun; CCTV tetap tayang ke
   NVR (bila NVR di VLAN 99 juga).
6. /interface bridge monitor bridge-LAN — hardware offload yes (bila
   chip mendukung).
7. Winbox akses admin HANYA via VLAN 10 (dari VLAN lain ditolak +
   berlog).

## ============================================================
## 9. ROLLBACK
## ============================================================
1. /interface bridge set [find name="bridge-LAN"] vlan-filtering=no
   — segala trafik kembali like-for-like tanpa VLAN.
2. Disable firewall antar VLAN: /ip firewall filter disable [find
   log-prefix~"smi-drop"]
3. Pulihkan penuh dari /export file=backup-pra-vlan
