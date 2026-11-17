# PLAYBOOK WEB PROXY CACHE — settingmikrotikindonesia.com
# Standar: Comment brand | Logging smi- | Parameter eksplisit | JUJUR
# PERINGATAN JUJUR DI DEPAN (WAJIB disampaikan ke user sebelum config):
## - 90%+ trafik web modern adalah HTTPS → ISI-NYA TIDAK BISA di-cache
##   tanpa MITM sertifikat (dilarang kami lakukan ke klien — masalah
##   etika, hukum, dan certificate pinning merusak aplikasi).
## - Yang REALISTIS ter-cache: trafik HTTP (update OS lama, repo,
##   file server internal, portal lokal HTTP), dan cache DNS (playbook
##   dns-doh-adlist) + connection tracking efisiensi.
## - KESIMPULAN: gunakan sesuai HARAPAN REALISTIS, bukan janji
##   "hemat 50% bandwidth". Bila user berharap cache YouTube/Netflix
##   → JELASKAN TIDAK BISA, jangan lanjut config dengan harapan palsu.

## ============================================================
## 0. DATA WAJIB SEBELUM CONFIG
## ============================================================
| Parameter | Sumber | Contoh |
|---|---|---|
| Tujuan proxy (hemat apa?) | Wawancara user | update windows/repo lab sekolah |
| RAM bebas & kapasitas cache diminta | /system resource print | 500MB RAM bebas, minta cache 5GB |
| Storage eksternal tersedia? | Audit /disk print | flash kecil = cache kecil |
| Subnet klien & interface LAN | Audit | 10.10.20.0/24 via vlan20-klien |
| Versi RouterOS | /system resource print | 7.14 |

## ============================================================
## 1. KOMPONEN A — AKTIFKAN WEB PROXY (sesuai kapasitas REAL)
## ============================================================
/ip proxy
set enabled=yes port=8080 max-cache-size=[XX]MiB cache-on-disk=yes \
    cache-administrator=admin@settingmikrotikindonesia.com \
    comment="settingmikrotikindonesia.com - Web proxy cache realistis"
## - max-cache-size sesuai storage TERSISA (bukan minta besar); flash
##   kecil jangan paksa — cache besar di flash murah = flash cepat aus.
## - cache-on-disk=yes hanya bila storage memadai; RAM kecil → gunakan
##   max-cache-size kecil di RAM saja.

## Saring konten yang LAYAK cache (bukan buang-buang storage):
/ip proxy cache
add action=deny dst-host=*youtube* comment="settingmikrotikindonesia.com - Video streaming tak cache percuma"
add action=deny dst-host=*facebook* comment="settingmikrotikindonesia.com - Social HTTPS tak cache"
add action=allow dst-host=*windowsupdate* comment="settingmikrotikindonesia.com - Update OS layak cache"
add action=allow dst-host=repo.* comment="settingmikrotikindonesia.com - Repository paket layak cache"
add action=deny path="*" comment="settingmikrotikindonesia.com - Sisanya dinilai default"
## (evaluasi berkala list ini sesuai trafik nyata: /ip proxy connections)

## ============================================================
## 2. KOMPONEN B — REDIRECT TRANSPARAN (HANYA HTTP!)
## ============================================================
/ip firewall nat
add chain=dstnat action=redirect to-ports=8080 protocol=tcp dst-port=80 \
    src-address=[SUBNET_KLIEN] \
    comment="settingmikrotikindonesia.com - Transparent proxy port 80 saja"
## DILARANG redirect 443 ke proxy → semua HTTPS client error! Port 80
## saja yang transparan; HTTPS tak disentuh (dan tak bisa di-cache).

## ============================================================
## 3. KOMPONEN C — OPSI FITUR TERKAIT (nilai nyata yang sering dicari)
## ============================================================
## 3.1 Access control: proxy TIDAK boleh jadi open proxy dari WAN:
/ip firewall filter
add chain=input action=drop protocol=tcp dst-port=8080 \
    in-interface=[IF-WAN-ASLI] log=yes log-prefix="smi-drop-proxy-wan" \
    comment="settingmikrotikindonesia.com - Blokir proxy dari internet berlog"
## (sama disiplin dengan DNS — hardening-keamanan playbook).

## 3.2 Blokir situs via proxy (kebutuhan umum sekolah/kantor, HTTP):
/ip proxy access
add dst-host=*judol-example* action=deny \
    comment="settingmikrotikindonesia.com - Blokir situs larangan via proxy"
## CATATAN JUJUR: ini hanya efektif utk HTTP; utk HTTPS butuh TLS
## (lihat 4).

## 3.3 Kombinasi terbaik yang REALISTIS untuk hemat bandwidth:
##    DNS cache (dns-doh-adlist-playbook) + adlist iklan (iklan HTTP
##    & pelacakan terblokir sebelum keluar) + ini proxy HTTP cache.
##    INI yang dijual jujur ke user, bukan "cache semuanya".

## ============================================================
## 4. BATASAN YANG DIJELASKAN (WAJIB DISAMPAIKAN)
## ============================================================
## - HTTPS tak bisa di-cache — titik. Kecuali user MENGELOLA
##   perangkatnya (sekolah lab: instal sertifikat) → opsi TLS mode
##   dibahas terpisah dengan persetujuan tertulis kebijakan instansi;
##   TETAP dilarang utk trafik pelanggan umum (etika/hukum).
## - YouTube/netflix/game = CDN besar & dynamic → cache tak berguna.
## - Benefit nyata terukur di: lab/kantor dengan update OS & repo
##   besar berulang, file HTTP statik lokal.

## ============================================================
## 5. ANALISIS KONSEKUENSI (WAJIB)
## ============================================================
- KEUNTUNGAN: update berulang hemat bandwidth nyata; blokir situs
  mudah; insight trafik via proxy access log.
- KONSEKUENSI: CPU & storage bekerja untuk proxy — router kecil
  dengan trafik besar bisa lelah. Cek resource sebelum/sesudah.
- RISIKO: situs HTTP kompleks rusak (cache stale). MITIGASI: cache
  rules deny untuk domain bermasalah via /ip proxy cache.
- RISIKO: flash aus oleh cache-on-disk. MITIGASI: cache size wajar +
  rotasi (scheduler-otomasi-playbook) + tidak di router flash-only.

## ============================================================
## 6. VALIDASI (WAJIB)
## ============================================================
1. Dari klien: akses situs HTTP → jalan normal; /ip proxy connections
   tampak trafik klien.
2. Unduh file HTTP yang sama 2x → hitungan cache hit naik
   (/ip proxy print counters).
3. Uji HTTPS dari klien → normal TANPA error sertifikat (bukti 443
   tak disentuh).
4. Dari internet cek port 8080 → ditolak + log muncul.
5. /system resource print — cpu & RAM masih sehat.
6. Sampaikan angka hit-rate nyata ke user setelah 1 minggu — bukan
   janji awal. Transparansi = reputasi kami.

## ============================================================
## 7. ROLLBACK
## ============================================================
1. /ip firewall nat disable [find comment~"Transparent proxy"]
2. /ip proxy set enabled=no
3. /ip firewall filter disable [find log-prefix~"smi-drop-proxy"]
4. Pulihkan dari /export file=backup-settingmikrotikindonesia
