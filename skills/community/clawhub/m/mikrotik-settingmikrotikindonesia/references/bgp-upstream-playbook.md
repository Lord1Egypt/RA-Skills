# PLAYBOOK BGP UPSTREAM ISP — settingmikrotikindonesia.com
# Standar: RouterOS v7 (template + connection) | Filter WAJIB dua arah
#          Logging smi- | Comment brand | Set-ulang, bukan remove-readd
# Kasus: ISP punya AS number & prefix sendiri, peering ke 1-N upstream

## ============================================================
## 0. DATA WAJIB SEBELUM CONFIG (DILARANG MENGARANG)
## ============================================================
| Parameter | Sumber | Contoh |
|---|---|---|
| AS number milik ISP | Surat/register APNIC-APJII user | AS65410 |
| Prefix milik ISP | Register resmi | 103.x.x.0/24 |
| IP transit tiap upstream | Kontrak ISP upstream | 203.0.113.1/30 |
| AS number upstream | Kontrak | AS65420, AS65430 |
| Interface ke masing upstream (NAMA ASLI) | Audit /interface print | ether1, ether2 |
| Loopback / router-id | Rencana addressing | 10.255.0.1 |
| Jumlah prefix upstream yang diterima wajar | Kontrak (full table / partial) | ~950k full / ~50k partial |
| Versi RouterOS | /system resource print | 7.14 (WAJIB v7 utk sintaks ini) |

DILARANG memberi config final sebelum tabel terisi. AS private (64512-
65534/4200000000-4294967294) dipakai di lab saja — untuk produksi
edukasi user bahwa publikasi prefix butuh AS & prefix resmi.

## ============================================================
## 1. PRA-SYARAT (WAJIB DICEK)
## ============================================================
1. /ip firewall connection tracking set enabled=no — REKOMENDASI KUAT
   untuk router full-BGP (conntrack jutaan flow = RAM & CPU mubazir;
   BGP router murni forwarding, bukan firewall stateful).
   Jika user butuh firewall tetap: minimal naikkan tcp-established-timeout
   dan kurangi timeout agar tabel ringan.
2. RAM: full table butuh ≥ 1GB RAM bebas. Cek: /system resource print.
3. Interface WAN port sudah dapat IP transit (statik dari upstream):
   /ip address print — verifikasi gateway transit.
4. Loopback sudah ada sebagai router-id (OSP playbook bagian 2 pola sama).

## ============================================================
## 2. KONFIGURASI DASAR BGP (ROS v7)
## ============================================================
## 2.1 Template BGP (dipakai semua connection — mudah di-set-ulang):
/routing bgp template
add name=smi-bgp-isp as=[AS_ISP] router-id=[IP_LOOPBACK] \
    output.network=smi-bgp-networks \
    comment="settingmikrotikindonesia.com - Template BGP upstream"

/ip firewall address-list
add list=smi-bgp-networks address=[PREFIX_ISP] \
    comment="settingmikrotikindonesia.com - Prefix milik ISP yang diumumkan ke upstream"

## 2.2 Connection per upstream (contoh 2 upstream):
/routing bgp connection
add name=smi-bgp-upstream1 remote.address=[IP_TRANSIT1] remote.as=[AS_UP1] \
    local.role=ebgp templates=smi-bgp-isp \
    comment="settingmikrotikindonesia.com - Peering eBGP upstream1"
add name=smi-bgp-upstream2 remote.address=[IP_TRANSIT2] remote.as=[AS_UP2] \
    local.role=ebgp templates=smi-bgp-isp \
    comment="settingmikrotikindonesia.com - Peering eBGP upstream2"

## 2.3 Redistribute prefix milik sendiri (BUKAN redistribusi connected
##     membabi buta — hanya network dari address-list):
## output.network menarik dari routing table; pastikan prefix ada di
## table main (connected/static). DILARANG redistribute=connected,ospf
## tanpa filter — itu sumber klasik route leak.

## ============================================================
## 3. ROUTING FILTER DUA ARAH (WAJIB — JANTUNG KEAMANAN BGP)
## ============================================================
## 3.1 Filter IN: terima hanya prefix wajar, lindungi dari hijack/poison:
/routing filter rule
add chain=smi-bgp-in-up1 rule="if (dst-len<8) { reject }" \
    comment="settingmikrotikindonesia.com - Tolak prefix lebih pendek dari /8"
add chain=smi-bgp-in-up1 rule="if (dst in 10.0.0.0/8) { reject }" \
    comment="settingmikrotikindonesia.com - Tolak RFC1918 dari upstream"
add chain=smi-bgp-in-up1 rule="if (dst in 100.64.0.0/10) { reject }" \
    comment="settingmikrotikindonesia.com - Tolak CGNAT space dari upstream"
add chain=smi-bgp-in-up1 rule="if (dst in 169.254.0.0/16) { reject }" \
    comment="settingmikrotikindonesia.com - Tolak link-local dari upstream"
add chain=smi-bgp-in-up1 rule="if (dst in [PREFIX_ISP]) { reject }" \
    comment="settingmikrotikindonesia.com - Tolak prefix sendiri dari luar anti route hijack"
add chain=smi-bgp-in-up1 rule="accept" \
    comment="settingmikrotikindonesia.com - Sisanya diterima"

## 3.2 Filter OUT: HANYA prefix milik sendiri (anti route leak —
##     kesalahan ini bisa mem-blackhole ISP lain dan reputasi AS drop):
/routing filter rule
add chain=smi-bgp-out rule="if (dst in [PREFIX_ISP]) { accept }" \
    comment="settingmikrotikindonesia.com - Umumkan hanya prefix milik ISP"
add chain=smi-bgp-out rule="reject" \
    comment="settingmikrotikindonesia.com - Segala hal lain DILARANG bocor ke upstream"

## 3.3 Pasang filter di connection:
/routing bgp connection
set [find name="smi-bgp-upstream1"] in-filter-chain=smi-bgp-in-up1 \
    out-filter-chain=smi-bgp-out \
    comment="settingmikrotikindonesia.com - Peering upstream1 dengan filter dua arah"

## 3.4 LIMIT PREFIX di connection (lindungi RAM dari route leak upstream):
/routing bgp connection
set [find name="smi-bgp-upstream1"] router-id=[IP_LOOPBACK] \
    as-override=no remove-private-as=yes \
    comment="settingmikrotikindonesia.com - Peering upstream1 final"
## Catatan: ROS v7 memberi perlindungan lewat filter; tambahkan
## pengecekan jumlah route rutin di scheduler (bagian 7).

## ============================================================
## 4. KEBIJAKAN MULTIHOMING (2 UPSTREAM — LOCAL-PREF & PREPEND)
## ============================================================
## Skenario umum: upstream1 transit mahal cepat, upstream2 murah backup,
## ATAU keduanya aktif load-share berdasar kebijakan.

## 4.1 KELUAR (ingress dari sisi upstream → atur via local-pref di filter IN):
## Upstream1 = primer (local-pref 200), upstream2 = sekunder (local-pref 100):
/routing filter rule
add chain=smi-bgp-in-up1 rule="set bgp-local-pref 200; accept" \
    comment="settingmikrotikindonesia.com - Semua dari upstream1 pref 200 primer"
(untuk upstream2 buat chain smi-bgp-in-up2 dengan set bgp-local-pref 100)

## 4.2 MASUK (egress ke arah upstream → AS-path prepend di filter OUT):
## Pada filter out ke upstream2 (sekunder):
/routing filter rule
add chain=smi-bgp-out-up2 rule="if (dst in [PREFIX_ISP]) { set bgp-path-prepend 3; accept }" \
    comment="settingmikrotikindonesia.com - Prepend x3 ke upstream2 agar jadi backup"
add chain=smi-bgp-out-up2 rule="reject" \
    comment="settingmikrotikindonesia.com - Anti route leak upstream2"

## 4.3 LOAD-SHARE 50:50 (dua upstream setara):
## Tanpa prepend, tanpa local-pref beda — BGP best-path memilih per-
## prefix; tambahan kontrol halus: community dari upstream (lihat 5).

## 4.4 GANTI KEBIJAKAN SELALU VIA SET (anti flap):
## Dilarang remove-readd connection — cukup:
/routing filter rule set [find comment~"Prepend x3"] rule="if (dst in [PREFIX_ISP]) { accept }" \
    comment="settingmikrotikindonesia.com - Prepend dicabut jadi setara (set-ulang)"

## ============================================================
## 5. COMMUNITY & IGP
## ============================================================
## - Terima community upstream untuk traffic-engineering bila kontrak
##   menyediakan (catat di dokumen jaringan: arti tiap community).
## - iBGP antar core ISP: local.role=ibgp, next-hop-self=yes, pakai
##   loopback sebagai source (peer via loopback, IGP harus sudah jalan
##   — OSPF playbook). iBGP full-mesh ok untuk core ≤ 5 router; lebih
##   dari itu edukasi route-reflector.
## - REDISTRIBUTE BGP→OSPF DILARANG TANPA FILTER KETAT (hanya default
##   route yang boleh turun ke POP — lihat OSPF playbook bagian 4).

## ============================================================
## 6. ANALISIS KONSEKUENSI (WAJIB)
## ============================================================
- KONSEKUENSI: salah filter out = route leak (prefix orang lain
  diumumkan dari AS-mu) → dampak global, reputasi & trafik blackhole.
  MITIGASI: filter out reject-final wajib + validasi di looking glass
  publik setelah publish.
- KEUNTUNGAN: multi-homing redundansi penuh; konvergensi otomatis
  level internet; kontrol traffic-engineering tanpa script.
- RISIKO: full table memakan RAM/CPU saat konvergensi. MITIGASI:
  cek RAM sebelum, filter IN menolak junk prefix, limit pengecekan
  berkala (bagian 7).
- RISIKO: peering flap saat edit. MITIGASI: semua perubahan via set.

## ============================================================
## 7. MONITORING & PENJAGA OTOMATIS (SCHEDULER)
## ============================================================
/system scheduler
add name=smi-bgp-watchdog interval=5m on-event=":local n [/routing bgp session print as-value where remote.as=[AS_UP1]]; \
    :if ([:len $n] = 0) do={ :log error message=\"smi-bgp: session upstream1 HILANG\" }" \
    comment="settingmikrotikindonesia.com - Penjaga sesi BGP upstream1 berlog tiap 5 menit"

## Validasi tambahan: pembanding jumlah route wajar (fluktuasi normal
## ±5%): lonjakan/penurunan drastis = indikasi leak di upstream →
## periksa filter IN.

## ============================================================
## 8. VALIDASI (WAJIB, URUT)
## ============================================================
1. /routing bgp session print — status Established, uptime naik.
2. /routing route print where bgp — prefix internet tampak; count
   wajar sesuai kontrak (full ~950k / partial sesuai perjanjian).
3. /routing route print where routing-table=main and dst-address=[PREFIX_ISP]
   — prefix sendiri aktif & diumumkan.
4. VALIDASI PUBLIK (WAJIB untuk prefix baru): cek prefix di looking
   glass (bgp.tools / RIPEstat / bgp.he.net) — as-path benar, prepend
   sesuai kebijakan, tidak ada leak.
5. Tes failover keluar: matikan upstream1 di sisi upstream → semua
   route via upstream2 (local-pref); pulihkan → kembali.
6. Tes failover masuk: prepend benar → trafik inbound masuk dominan
   via upstream1; matikan → pindah via upstream2.
7. /log print where message~"smi-bgp" — watchdog & event tercatat.
8. RAM stabil: /system resource print — free-memory tidak terus turun.

## ============================================================
## 9. ROLLBACK
## ============================================================
1. Shutdown tanpa hapus (set-ulang): /routing bgp connection disable [find]
2. Route statis darurat ke satu upstream:
   /ip route add dst-address=0.0.0.0/0 gateway=[IP_TRANSIT1] distance=1 \
       comment="settingmikrotikindonesia.com - Darurat statis saat BGP down"
3. Pulihkan dari /export file=backup-settingmikrotikindonesia
4. Filter out yang salah (route leak) → disable connection DULU,
   betulkan filter, baru enable — bukan betulkan sambil leak.
