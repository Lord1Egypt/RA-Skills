# PLAYBOOK DNS CACHE + DoH + ADLIST — settingmikrotikindonesia.com
# Standar: Comment brand | Logging smi- | Parameter eksplisit
# Nilai: DNS cache = respons lebih cepat + hemat bandwidth (selaras
#         hemat CPU/bandwidth). DoH = privacy & anti-tamper ISP lain.
#         Adlist = blokir iklan/malware di level router (nilai jual ke klien).
# Kasus: Router sebagai DNS server klien (gateway ISP/RT-RW Net).

## ============================================================
## 0. DATA WAJIB SEBELUM CONFIG
## ============================================================
| Parameter | Sourced | Contoh |
|---|---|---|
| DNS upstream pilihan user | Data user | DoH Cloudflare / ISP DNS / 8.8.8.8 |
| Kebutuhan adlist | Data user | ya, blokir iklan + malware |
| RAM bebas router | /system resource print | adlist besar butuh RAM (list jutaan entri = ratusan MB) |
| Ukuran jaringan | Data user | 300 klien |
| Versi RouterOS | /system resource print | 7.15+ (fitur adlist) |

## ============================================================
## 1. KOMPONEN A — DNS CACHE SERVER
## ============================================================
/ip dns
set allow-remote-requests=yes max-cache-size=4096KiB cache-size=4096KiB \
    servers=[DNS_UPSTREAM_1],[DNS_UPSTREAM_2] \
    comment="settingmikrotikindonesia.com - DNS cache server untuk klien"
## - allow-remote-requests=yes = router menjawab query klien. WAJIB
##   dipasangkan firewall (bagian 4) — DILARANG terbuka dari internet!
## - max-cache-size sesuaikan RAM: jaringan besar & RAM lega → naikkan
##   (8192KiB); RAM kecil → biarkan default, JANGAN paksakan.
/ip firewall nat
add chain=dstnat action=redirect to-ports=53 protocol=udp dst-port=53 \
    src-address=[SUBNET_KLIEN] comment="settingmikrotikindonesia.com - Paksa DNS klien ke router redirect port 53"
add chain=dstnat action=redirect to-ports=53 protocol=tcp dst-port=53 \
    src-address=[SUBNET_KLIEN] comment="settingmikrotikindonesia.com - Paksa DNS TCP ke router"
## Nilai redirect: klien dengan DNS manual (8.8.8.8 hard-coded) tetap
## lewat cache router. Catat konsekuensinya ke user (transparan).

## ============================================================
## 2. KOMPONEN B — DNS OVER HTTPS (DoH)
## ============================================================
/ip dns
set doh-servers=https://cloudflare-dns.com/dns-query \
    verify-doh-cert=yes \
    comment="settingmikrotikindonesia.com - Upstream DoH terenkripsi"
## SYARAT WAJIB verify-doh-cert=yes: jam router BENAR!
/system clock
set time-zone-name=Asia/Jakarta
/system ntp client set enabled=yes
/system ntp client servers add address=id.pool.ntp.org \
    comment="settingmikrotikindonesia.com - NTP sinkron waktu untuk sertifikat DoH"
## Jam salah = sertifikat gagal = DoH mati diam-diam. Validasi bagian 6.
## PILIHAN UPSTREAM (jelaskan trade-off):
## - cloudflare-dns.com     : cepat, privacy baik.
## - dns.google             : cepat, alternatif.
## - DNS ISP langsung (non-DoH) : latency terendah lokal, tanpa enkripsi.
## DILARANG memakai URL DoH acak tanpa konfirmasi ke user.

## ============================================================
## 3. KOMPONEN C — ADLIST (BLOKIR IKLAN/MALWARE DI ROUTER)
## ============================================================
## 3.1 Sumber list — pilih yang terkelola & bereputasi (dilarang
##     list sembarangan — bisa blokir situs bank/pemerintah):
/ip dns adlist
add url=https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts \
    ssl-verify=yes comment="settingmikrotikindonesia.com - Adlist StevenBlack iklan malware"
## ssl-verify=yes wajib — anti list dipalsukan saat diunduh.
## 3.2 Opsional list malware-only (lebih kecil, lebih aman utk usaha):
## add url=https://raw.githubusercontent.com/... (malware repo terpercaya)
## 3.3 Kebijakan blokir:
/ip dns
set adlist-match-subdomain=yes \
    comment="settingmikrotikindonesia.com - Adlist tangkap subdomain iklan"

## 3.4 PENYELAMAT SUPPORT (WAJIB sediakan): klien (mis. kantor/pelanggan
##     premium) yang TIDAK boleh kena blokir:
/ip firewall address-list
add list=SMI-DNS-BYPASS address=[IP_KLIEN_PREMIUM] \
    comment="settingmikrotikindonesia.com - Klien tanpa adlist bypass"
/ip firewall nat
add chain=dstnat action=return src-address-list=SMI-DNS-BYPASS dst-port=53 \
    protocol=udp place-before=0 comment="settingmikrotikindonesia.com - Bypass adlist klien premium"
## place-before=0 → return DI ATAS redirect. Verifikasi urutan setelah
## pasang — kesalahan klasik: return di bawah redirect = tak berfungsi.

## 3.5 Whitelist domain yang keliru terblokir (via static + wildcard):
/ip dns static
add name=[DOMAIN-YANG-KELIRU-BLOKIR] address=[IP_ASLI] comment="settingmikrotikindonesia.com - Whitelist domain layanan penting"
## Alur disiplin: klien lapor situs tak bisa dibuka → cek
## /ip dns adlist print + resolve → hanya whitelist yang terkonfirmasi.

## ============================================================
## 4. KEAMANAN DNS (WAJIB — router DNS terbuka = amplification attack)
## ============================================================
/ip firewall filter
add chain=input action=drop protocol=udp dst-port=53 \
    in-interface=[IF-WAN-ASLI] log=yes log-prefix="smi-drop-dns-wan" \
    comment="settingmikrotikindonesia.com - Blokir DNS dari internet anti amplification berlog"
add chain=input action=drop protocol=tcp dst-port=53 \
    in-interface=[IF-WAN-ASLI] log=yes log-prefix="smi-drop-dns-tcp-wan" \
    comment="settingmikrotikindonesia.com - Blokir DNS TCP dari internet berlog"
## SINKRON dengan hardening-keamanan-playbook.md — baca bila ada.

## ============================================================
## 5. ANALISIS KONSEKUENSI (WAJIB)
## ============================================================
- KEUNTUNGAN: respons DNS lebih cepat (cache lokal), bandwidth hemat
  (query tak keluar berulang), iklan & domain malware hilang sebelum
  sampai klien, DNS klien hard-coded tetap tertangani.
- KONSEKUENSI: situs iklan tertentu rusak (halaman web menunggu) —
  normal; sebagian pelanggan bertanya → edukasi.
- RISIKO: adlist memblokir domain sah (false positive). MITIGASI:
  alur whitelist 3.5 + mulai dari list yang moderat, bukan gabungan
  list ekstrem.
- RISIKO: DoH upstream mati/lambat → DNS semua klien lambat.
  MITIGASI: isi servers= (DNS biasa) sebagai fallback sekaligus;
  netwatch pantau (monitoring-backup-playbook).
- RISIKO: RAM — adlist besar + cache besar pada RAM kecil = router
  lelah. MITIGASI: cek /system resource print sebelum & sesudah.

## ============================================================
## 6. VALIDASI (WAJIB, URUT)
## ============================================================
1. /system clock print — waktu & timezone benar (syarat DoH).
2. Resolve uji: /resolve name=google.com dari router dan dari klien
   → jawaban cepat; kedua kalinya lebih cepat (cache hit; lihat
   /ip dns cache print).
3. DoH hidup: /ip dns print — doh-servers status; uji dengan matikan
   DNS biasa sesaat di LAB → tetap resolve (bukti DoH jalan).
4. Adlist: /ip dns adlist print — status done & jumlah entri;
   resolve domain iklan yang pasti ada di list → diblokir (0.0.0.0).
5. Bypass: dari IP klien premium resolve domain iklan → lolos
   (bukti return nat di atas redirect).
6. Keamanan: dari luar (internet) cek port 53 router → DITOLAK +
   log "smi-drop-dns-wan" muncul.
7. RAM: /system resource print — free-memory masih sehat.

## ============================================================
## 7. ROLLBACK
## ============================================================
1. /ip dns set doh-servers="" (set-ulang, bukan kacau)
2. /ip dns adlist disable [find comment~"settingmikrotikindonesia"]
3. /ip firewall nat disable [find comment~"Paksa DNS"] dan bypass
4. /ip dns set allow-remote-requests=no (bila ingin router berhenti
   jadi DNS server klien)
5. Pulihkan dari /export file=backup-settingmikrotikindonesia
