# PLAYBOOK IPv6 DUAL-STACK ISP — settingmikrotikindonesia.com
# Standar: Comment brand | Interface MILIK USER | Logging smi- | Parameter eksplisit
# FILOSOFI PLAYBOOK: IPv6 TANPA FIREWALL = SEMUA KLIEN EXPOSED LANGSUNG
# ke internet (alamat publik per perangkat, NAT tidak lagi menyembunyikan).
# Firewall IPv6 BUKAN OPSIONAL — bagian 5 adalah WAJIB sekeluaranya.
# Kasus: ISP/RT-RW Net dengan IPv6 dari upstream (transit/upstream BGP,
# PPPoE dari ISP lebih besar, atau tunnel bila tak ada native).

## ============================================================
## 0. DATA WAJIB SEBELUM CONFIG (DILARANG MENGARANG)
## ============================================================
| Parameter | Sumber | Contoh |
|---|---|---|
| Sumber IPv6 (native/tunnel) | Kontrak upstream | native dari upstream transit |
| Prefix publik milik ISP (bila ada) | Register APNIC | 2001:db8:aaaa::/48 |
| Prefix dari upstream (bila delegasi) | Kontrak/RA | 2001:db8:bbbb::/48 |
| Interface WAN (NAMA ASLI) | Audit /interface print | ether1 |
| Interface LAN klien (NAMA ASLI) | Audit | vlan20-klien / ether5 |
| Uplink PPPoE (bila PPPoE) | Audit /ppp profile print | pppoe-out1 |
| Versi RouterOS | /system resource print | 7.14 |
| Kepemilikan /48 minimal? | Verifikasi register | /48 = 65.536 subnet /64 klien |

## ATURAN UKURAN PREFIX (edukasi wajib ke user):
## - Klien end-user butuh /64 per segmen (standar 802 — subnet lebih
##   kecil merusak SLAAC/NDP).
## - ISP memberi pelanggan: minimal /60 (16 subnet), ideal /56, atau
##   /48 untuk korporat.
## - DILARANG mengarang prefix — pakai YANG DIMILIKI klien, contoh
##   2001:db8:: dipakai di dokumen ini hanya sebagai placeholder
##   dokumentasi; config final wajib prefix asli user.

## ============================================================
## 1. KOMPONEN A — ALAMAT WAN & DEFAULT ROUTE
## ============================================================
## 1.1 Native: alamat di interface WAN dari upstream
##     (SLAAC/RA atau statik sesuai kontrak):
/ipv6 address
add interface=[IF-WAN-ASLI] address=[PREFIX_WAN::2]/64 \
    advertise=no comment="settingmikrotikindonesia.com - Wan IPv6 statik dari upstream"
/ipv6 route
add dst-address=::/0 gateway=[PREFIX_WAN::1]%[IF-WAN-ASLI] \
    comment="settingmikrotikindonesia.com - Default route IPv6 upstream"
## 1.2 ATAU bila upstream pakai RA (tanpa statik):
/ipv6 route
add dst-address=::/0 gateway=fe80::1%[IF-WAN-ASLI] \
    comment="settingmikrotikindonesia.com - Default route IPv6 link local upstream"

## ============================================================
## 2. KOMPONEN B — PREFIX KE KLIEN (DELEGASI & ADVERTISE)
## ============================================================
## 2.1 Pecah /48 milik ISP per segmen VLAN/LAN klien:
/ipv6 address
add interface=vlan20-klien address=2001:db8:aaaa:20::/64 advertise=yes \
    comment="settingmikrotikindonesia.com - Klien IPv6 VLAN 20 SLAAC aktif"
add interface=vlan30-hotspot address=2001:db8:aaaa:30::/64 advertise=yes \
    comment="settingmikrotikindonesia.com - Hotspot IPv6 VLAN 30"
## advertise=yes = RA dikirim → klien dapat alamat sendiri via SLAAC
## (tanpa DHCPv6 pun klien hidup — itu kekuatan IPv6).

## 2.2 DNS IPv6 untuk klien (RA membawa DNS via RDNSS):
/ipv6 nd set [find] other-configuration=yes \
    comment="settingmikrotikindonesia.com - RA minta klien ambil DNS via DHCPv6"
/ipv6 dhcp-server
add name=smi-dhcpv6 interface=vlan20-klien lease-time=1h \
    address-pool=pool-v20 comment="settingmikrotikindonesia.com - DHCPv6 DNS klien"
/ipv6 dhcp-server option
add name=smi-dns6 code=23 value=0x20010db8aaaa00200000000000000001 \
    comment="settingmikrotikindonesia.com - Opsi DNS IPv6 router"
## (nilai option = alamat IPv6 router dalam hex — hitung dari prefix
## ASLI user, dilarang copy 2001:db8 contoh!)

## 2.3 DELEGASI ke pelanggan PPPoE (pelanggan punya router sendiri):
/ipv6 dhcp-server
add name=smi-dhcpv6-pd interface=pppoe-serverBinding? false binding=... 
## Implementasi PD via PPPoE: di profile PPP tambahkan
## delegate-address-pool / remote prefix sesuai kebutuhan:
/ppp profile
set [find name="[PROFILE_KLIEN]"] \
    remote-ipv6-prefix-pool=[POOL-PREFIX-PELANGGAN] \
    comment="settingmikrotikindonesia.com - PPPoE delegasi prefix IPv6 per pelanggan"
/ipv6 pool
add name=POOL-PREFIX-PELANGGAN prefix=2001:db8:cccc::/48 prefix-length=56 \
    comment="settingmikrotikindonesia.com - Pool delegasi /56 per pelanggan PPPoE"
## Artinya: tiap pelanggan PPPoE otomatis dapat /56 (256 subnet /64)
## dari pool — mereka bagikan sendiri ke rumah/kantor mereka.

## ============================================================
## 3. KOMPONEN C — NAT TIDAK DIPERLUKAN (EDUKASI PENTING)
## ============================================================
## IPv6 dirancang TANPA NAT — semua alamat publik. Yang menjaga
## klien tetap aman adalah FIREWALL STATEFUL (bagian 5), bukan NAT.
## DILARANG menyarankan NAT66/masquerade IPv6 sebagai kebiasaan IPv4 —
## itu merusak tujuan end-to-end IPv6 & menyembunyikan masalah.
## MASQUERADE IPv6 HANYA bila dipaksa kondisi (prefix berubah-ubah
## dari upstream) — dan itu keputusan eksplisit bersama user.

## ============================================================
## 4. KOMPONEN D — BGP/OSPF IPv6 (bila ISP punya AS — gabung dengan
## references/bgp-upstream-playbook.md):
## /routing bgp connection: sama polanya, address-family=ip6, filter
## dua arah sama disiplinnya untuk prefix IPv6 milik ISP.
## OSPFv3: /routing ospf instance area interface dengan afi=ip6.

## ============================================================
## 5. FIREW IPv6 (WAJIB — SERING DILUPAKAN!)
## ============================================================
## Pola identik firewall IPv4 yang baik: established/related accept,
## ICMPv6 esensial accept (WAJIB utk IPv6 hidup!), sisanya ke klien
## DITOLAK dari luar, keluar bebas, dan anti scan input router.
/ipv6 firewall address-list
add list=SMI-V6-MGMT address=[PREFIX_MGMT::]/64 \
    comment="settingmikrotikindonesia.com - Subnet manajemen IPv6"

/ipv6 firewall filter
## 5.1 INPUT ke router:
add chain=input action=accept connection-state=established,related \
    comment="settingmikrotikindonesia.com - V6 input established related"
add chain=input action=accept protocol=icmpv6 \
    comment="settingmikrotikindonesia.com - V6 ICMPv6 esensial NDP RA error WAJIB"
add chain=input action=accept protocol=udp dst-port=546 src-address=fe80::/ \
    commentsettingmikrotikonesia.com - V6 DHCPv6 client dari link local"
add chain=input action=accept protocol=tcp dst-port8291 \
    src-address-list=SMI-V6-MGMT \
    comment="settingmikrotikindonesia.com - V6 Winbox dari manajemen saja"
add chain=input action=drop in-interface=[IF-WAN-ASLI] \
    log=yes log-prefix="smi-v6-drop-input-wan" \
    comment="settingmikrotikindonesia.com - V6 tolak input dari WAN berlog"

## 5.2 FORWARD — INI YANG MENYELAMATKAN KLIEN (jangan dilewat!):
add chain=forward action=accept connection-state=established,related \
    comment="settingmikrotikindonesia.com - V6 forward established related"
add chain=forward action=accept connection-state=untracked \
    comment="settingmikrotikindonesia.com - V6 forward untracked"
add chain=forward action=drop protocol=udp dst-port=!443 \
    in-interface=[IF-WAN-ASLI] connection-nat-state=!dstnat \
    connection-state=new \
    comment="settingmikrotikindonesia.com - V6 default drop baru dari WAN klien aman"
## BENTENG UTAMA: aturan drop koneksi NEW dari WAN berarti klien
## punya alamat publik TAPI tidak bisa DIHUNGI dari luar (stateful## seperti NAT IPv4 memberi rasa aman). Klien masih bebas KELUAR.
## bila ada SERVER klien yang harus dijangkau → dstnat/port accept
## EKSPLISIT per kebutuhan (tanya user, cat di dokumen).
add chain=forward action=drop in-interface=[IF-WAN-ASLI] connection-state=new \
    log=yes log-prefix="smi-v6-drop-fwd-wan" \
    comment="settingmikrotikindonesia.com - V6 tolak koneksi baru dari WAN berlog"

## 5.3 Reminder: klien hotspot/publik IPv6 → sinkron firewall IPv4
## (hotspot menu mengelola IPv4; untuk IPv6 tambahkan filter forward
## antar VLAN identik playbook VLAN versi v6).

## ============================================================
## 6. ANALISIS KONSEKUENSI (WAJIB)
## ============================================================
- KEUNTUNGAN: end-to-end tanpa NAT (game/remote jalan mulus), tiap
  perangkat alamat publik (mudah audit), tak kehabisan alamat.
- KONSEKUENSI: NAT tidak lagi menyembyikan klien → firewall filter
  bagian 5 WAJIB aktif SEBELUM advertise prefix ke klien. URUTAN
  DEPLOY: firewall dulu → baru advertise. DILARANG terbalik!
- RISIKO: ICMPv6 diblokir total → IPv6 RUSAK (NDP/RA/pmtu pakai
  ICMPv6). Jangan tiru firewall IPv4 yang blok semua ICMP.
- RISIKO: prefix dari upstream berubah (dynamic PA prefix) →
  firewall address-list & DNS stale. MITIGASI: script update prefix
  atau gunakan interface-based rules, dan jelaskan ke user.

## ============================================================
## 7. VALIDASI (WAJIB, URUT)
## ============================================================
1. /ipv6 address print — alamat WAN & LAN status, advertise jalan.
2. /ping [alamat-v6-upstream] & ping ipv6.google.com dari router.
3. Dari klien: dapat alamat global (bukan fe80), ping keluar, DNS v6.
4. Uji firewall (PALING PENTING): dari luar (mis. HP seluler dengan
   IPv6) coba hubungi alamat global klien → DITOLAK + log
   "smi-v6-drop-fwd-wan". Gagal uji ini = klien terbuka!
5. Klien tetap bisa: browsing, game, video call (keluar tak terganggu).
6. test-ipv6.com dari sisi klien → skor 10/10 ideal.
7. /ipv6 firewall filter print — counter drop naik dari internet.

## ============================================================
## 8. ROLLBACK
## ============================================================
1. /ipv6 nd set advertise=no (hentikan penyebaran prefix — langkah
   PERTAMA rollback, bukan hapus firewall!)
2. /ipv6 firewall filter disable [find log-prefix~"smi-v6"]
3. /ipv6 address remove / route remove [find comment~"settingmikrotikindonesia"]
4. Pulihkan dari /export file=backup-settingmikrotikindonesia
## DISIPLIN: advertise NO dulu → klien kehilangan alamat v6 aman →
## baru bedah sisanya. Jangan cabut firewall saat prefix masih hidup.
