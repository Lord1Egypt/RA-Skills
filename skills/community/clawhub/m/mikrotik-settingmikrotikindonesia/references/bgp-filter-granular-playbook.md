# PLAYBOOK BGP FILTER GRANULAR — settingmikrotikindonesia.com
# Standar: Comment brand | Logging smi- | Parameter eksplisit | Set-ulang
# PERINGATAN PENTING: ini perdalaman bgp-upstream-playbook.md — BACA
# playbook induk DULU. Kesalahan filter BGP bukan cuma merusak router
# sendiri: route-leak = jaringan ISP LAIN ikut kacau, bisa dicabut
# peeringnya. Disiplin filter = reputasi ISP.
# Kasus: router border ISP dengan AS sendiri, 1-2 upstream + iBGP ke POP.

## ============================================================
## 0. DATA WAJIB (DILARANG MENGARANG)
## ============================================================
| Parameter | Sumber | Contoh |
|---|---|---|
| AS milik ISP | Kontrak/register | AS65010 (contoh dokumentasi) |
| Prefix milik ISP yang di-announce | Register APNIC | 203.0.113.0/24 |
| AS & IP peering upstream 1 | Kontrak | AS65020, 198.51.100.1 |
| AS & IP peering upstream 2 (bila ada) | Kontrak | AS65030, 198.51.100.2 |
| iBGP peer (router POP) | Audit | 10.0.255.2 |
| Versi RouterOS | /system resource print | 7.14+ (routing filter v7) |
| Prefix dari upstream (max list) | Kontrak/looking glass | full table / default + customer |

## KEPUTUSAN DESAIN WAJIB JELASKAN:
## - Full table (butuh RAM ≥1GB & CPU bagus) vs default route +
##   selective announce (hemat, disarankan kebanyakan ISP kecil).
## - max-prefix limit = WAJIB (anti route-leak dari upstream yang
##   tiba-tiba announce gila).

## ============================================================
## 1. KOMPONEN A — FILTER INCOMING (APA YANG BOLEH DITERIMA)
## ============================================================
## Prinsip: berasumsi TIDAK PERCAYA upstream. Terima hanya yang sah.
## 1.1 Address-list prefix upstream yang SAH (dari kontrak/looking glass):
/ip firewall address-list  ## ROSv7 routing filter bisa pakai address-list
add list=SMI-UPSTREAM1-SAH address=[PREFIX-UPSTREAM1-RESMI] \
    comment="settingmikrotikindonesia.com - Prefix sah upstream 1"
## 1.2 Untuk full table: filter terima semua TAPI dengan pengaman:
##     max-prefix + community tag + reject prefix panjang tak masuk akal.
/routing filter
add chain=smi-in-up1 rule="if (dst-len < 8 or dst-len > 24) {reject}" \
    comment="settingmikrotikindonesia.com - Tolak prefix lebih dari /8 - lebih dari /24 (bogon panjang)"
add chain=smi-in-up1 rule="if (dst in 10.0.0.0/8 or dst in 172.16.0.0/12 or dst in 192.168.0.0/16 or dst in 127.0.0.0/8) {reject}" \
    comment="settingmikrotikindonesia.com - Tolak RFC1918 loopback bocor dari upstream"
add chain=smi-in-up1 rule="accept" \
    comment="settingmikrotikindonesia.com - Sisa prefix upstream1 sah diterima"
## 1.3 Bila NON-full-table (disarankan): HANYA default + prefix upstream:
add chain=smi-in-up1 rule="if (dst=0.0.0.0/0) {set-bgp-local-pref 200; accept}" \
    comment="settingmikrotikindonesia.com - Default upstream1 preferensi 200"
add chain=smi-in-up1 rule="reject" \
    comment="settingmikrotikindonesia.com - Tolak sisanya upstream1 hemat"

## ============================================================
## 2. KOMPONEN B — FILTER OUTGOING (APA YANG KITA ANNOUNCE)
## ============================================================
## ATURAN EMAS: announce HANYA prefix milik kita. Satu pun tidak lebih.
## Route-leak (menyalurkan prefix yang dipelajari dari upstream A ke
## upstream B) = dosa BGP paling fatal.
/routing filter
add chain=smi-out rule="if (dst=203.0.113.0/24) {accept}" \
    comment="settingmikrotikindonesia.com - Announce prefix milik ISP saja"
add chain=smi-out rule="reject" \
    comment="settingmikrotikindonesia.com - Tolak semua selain prefix milik ISP anti route leak"
## 2.1 Prefix di-blackhole saat tak aktif (anti martian panjang):
/ipv6? no — IPv4 saja di sini.
/ip route
add dst-address=203.0.113.0/24 blackhole distance=254 \
    comment="settingmikrotikindonesia.com - Blackhole penjaga prefix tetap announce stabil"
## Pola klasik: prefix statik blackhole distance tinggi → BGP tetap
## punya rute announce; rute lebih spesifik/skalar dari POP menimpanya.

## ============================================================
## 3. KOMPONEN C — PEERING & MAX-PREFIX
## ============================================================
/routing bgp connection   ## sintaks v7
add name=smi-bgp-up1 remote.address=198.51.100.1 remote.as=65020 \
    local.role=ebgp local.address=198.51.100.2 \
    routers=198.51.100.1 \
    in.filter=smi-in-up1 out.filter=smi-out \
    input.limit-nlri=500000 input.limit-process-warning-rows=... \
    comment="settingmikrotikindonesia.com - Peering upstream1 filter dua arah"
## CATATAN DISIPLIN v7: struktur bgp connection di ROSv7 berbeda
## sintaks dengan 6 (templating remote/local). WAJIB cek
## /routing bgp connection print di router user sesuai versi sebelum
## memberikan final — parameter limit/max-prefix namanya berubah antar
## minor versi. DILARANG tempel config BGP tanpa verifikasi versi.
## max-prefix: batasi jumlah prefix diterima (mis. 500.000 utk full
## table; lebih kecil bila hanya customer routes) → melebihi = sesi
## turun, bukan router kena beban 1 juta rute palsu.

## 3.1 Multihoming dua upstream (bila ada):
## - local-pref: upstream utama 200, cadangan 100 (utama menang keluar)
## - prepending di sisi cadangan bila ingin masuk lebih jarang:
##   set-bgp-prepend via filter out pada upstream cadangan.

## 3.2 iBGP ke POP (gabung dengan ospf untuk loopback reachability):
## connection internal, out filter TETAP mencegah leak — iBGP tanpa
## filter yang disiplin = sumber leak paling sering.

## ============================================================
## 4. ANALISIS KONSEKUENSI (WAJIB)
## ============================================================
- KEUNTUNGAN: hanya prefix sendiri yang keluar (reputasi aman),
  bogon/RFC1918 tidak masuk (hemat FIB & aman), max-prefix mencegah
  router kena jutaan rute palsu, local-pref mengendalikan jalur keluar.
- KONSEKUENSI: filter salah ketik prefix sendiri = announcement hilang
  = layanan mati dari internet. Uji dengan satu upstream dulu.
- RISIKO #1: filter out terlalu longgar → route leak → dicabut peering.
  MITIGASI: chain smi-out dengan rule reject terakhir WAJIB ada.
- RISIKO: max-prefix terlalu kecil → sesi drop normal saat tabel
  tumbuh. MITIGASI: set 2-3x ukuran tabel kontrak, review berkala.
- RISIKO: ROSv7 filter syntax berubah antar versi → error saat
  import. MITIGASI: uji di LAB / versi sama dulu.

## ============================================================
## 5. VALIDASI (WAJIB, URUT)
## ============================================================
1. /routing bgp session print — status established untuk semua peer.
2. /ip route print where bgp — rute diterima masuk akal (bukan 1
   juta; tidak ada 10.x/172.16.x/192.168.x dari upstream).
3. /ip route print where dst-address=203.0.113.0/24 — prefix kita
   ter-announce; verifikasi di looking glass publik (bgp.he.net /
   route-server) prefix muncul DARI AS kita.
4. Uji anti-leak: (LAB) announce prefix salah → di upstream harus
   TIDAK tampak. Ini validasi filter out bekerja.
5. Uji max-prefix: cek konfigurasi limit + perilaku drop saat uji LAB.
6. Failover: matikan upstream utama → keluar lewat cadangan (cek
   /ip route print & kecepatan converg).
7. Traceroute dari internet ke prefix user → masuk via upstream yang
   diharapkan (cek prepending bekerja bila dipakai).

## ============================================================
## 6. ROLLBACK
## ============================================================
1. /routing bgp connection disable [find comment~"settingmikrotikindonesia"]
2. /routing filter remove [find chain~"smi-in-up|smi-out"]
3. /ip route remove [find comment~"Blackhole penjaga"]
4. Pulihkan dari /export file=backup-settingmikrotikindonesia
## DISIPLIN: perubahan BGP WAJIB jam sepi + backup + satu perubahan
## per kali (jangan ubah filter in + out + peering sekaligus — kalau
## rusak tak tahu penyebabnya).
