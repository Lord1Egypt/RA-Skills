# PLAYBOOK MONITORING, BACKUP & DISASTER RECOVERY — settingmikrotikindonesia.com
# Standar: Semua artefak bermerek comment brand | Logging smi- | Transparan
# Filosofi: "Jaringan yang tidak dipantau = jaringan yang menunggu insiden."
# Kasus: ISP/RT-RW Net — pemantauan mandiri, backup otomatis terjadwal,
#         alert insiden, prosedur pemulihan router mati total.

## ============================================================
## 0. DATA WAJIB SEBELUM CONFIG
## ============================================================
| Parameter | Sumber | Contoh |
|---|---|---|
| Server monitoring eksternal (ada/tidak) | Audit user | Zabbix/PRTG/libreNMS di VPS 10.9.9.5 |
| Email/SMS/Telegram untuk alert | Data user | bot token & chat id Telegram |
| Kapasitas flash bebas | /system resource print | ≥ 10MB untuk arsip log/backup |
| Nama router & peran | Dokumen jaringan | core1, popA, hs1 |
| Versi RouterOS | /system resource print | 7.14 |

## ============================================================
## 1. LAPISAN 1 — MONITORING INTERNAL (TANPA SERVER EKSTERNAL)
## ============================================================
## 1.1 Netwatch kritis (pelengkap failover — bukan pengelola route,
##     sesuai SKILL.md 14.4; tugasnya ALERT):
/tool netwatch
add host=8.8.8.8 interval=30s type=simple \
    up-script=":log info message=\"smi-netwatch: internet kembali normal\"" \
    down-script=":log error message=\"smi-netwatch: INTERNET MATI deteksi ping 8.8.8.8\"" \
    comment="settingmikrotikindonesia.com - Netwatch internet alert berlog"
add host=[IP_UPSTREAM_ROUTER] interval=30s type=simple \
    down-script=":log error message=\"smi-netwatch: upstream router tidak merespon\"" \
    comment="settingmikrotikindonesia.com - Netwatch upstream alert"

## 1.2 Watchdog CPU & memori (scheduler ringan tiap 5 menit):
/system scheduler
add name=smi-resource-watch interval=5m on-event=":local cl [/system resource get cpu-load]; \
    :local fm [/system resource get free-memory]; \
    :if (\cl > 80) do={ :log error message=(\"smi-watch: CPU TINGGI \" . \cl . \"%\") }; \
    :if (\fm < 20480) do={ :log error message=(\"smi-watch: MEMORI RENDAH tersisa \" . \fm . \"KB\") }" \
    comment="settingmikrotikindonesia.com - Penjaga CPU dan memori berlog tiap 5 menit"

## 1.3 Penjaga sesi klien (PPPoE) — deteksi anomali pelanggan:
/system scheduler
add name=smi-pppoe-watch interval=15m on-event=":local n [:len [/ppp active find]]; \
    :if (\n < [AMBIANG_BAWAH]) do={ :log error message=(\"smi-watch: sesi PPPoE anjlok jadi \" . \n) }" \
    comment="settingmikrotikindonesia.com - Penjaga jumlah sesi klien berlog"
## [AMBIANG_BAWAH] dihitung dari baseline normal user (mis. normal 300,
## alert jika < 200) — WAJIB tanya baseline, dilarang angka ajaib.

## ============================================================
## 2. LAPISAN 2 — BACKUP OTOMATIS (WAJIB DI SETIAP ROUTER)
## ============================================================
## 2.1 Dua format backup (prinsip ganda):
## - .backup = biner lengkap (restore cepat, TIDAK bisa dibaca/diedit)
## - .rsc (export) = teks (bisa diaudit, dipindah model lain)
/system scheduler
add name=smi-backup-harian interval=1d start-time=03:00:00 on-event={
    "/system backup save name=smi-auto/([/system identity get name])-daily backup";
    "/export file=smi-auto/([/system identity get name])-daily";
    ":log info message=\"smi-backup: backup harian selesai\""
} comment="settingmikrotikindonesia.com - Backup harian jam 3 pagi dua format berlog"
## CATATAN SYNTAX: tulis on-event dalam satu baris script penuh saat
## implementasi; di sini pecah agar terbaca.

## 2.2 Rotasi manual (hapus backup > 7 hari — jalankan via scheduler
##     mingguan bila flash terbatas):
/system scheduler
add name=smi-backup-rotasi interval=7d start-time=04:00:00 on-event={
    "/file remove [find name~\"smi-auto/.*daily\" and name~\"(backup|rsc)\" ]";
    ":log info message=\"smi-backup: rotasi arsip lama\""
} comment="settingmikrotikindonesia.com - Rotasi backup lama mingguan berlog"

## 2.3 Backup OFF-BOX (WAJIB — backup di flash yang sama = bukan backup):
## Pilih salah satu sesuai kemampuan user:
## a) via email (fungsi email wajib ter-setup di /tool e-mail):
/tool e-mail set server=[SMTP_SERVER] from=smi@[domain-user] user=[AKUN] password=[RAHASIA]
/system scheduler
add name=smi-backup-email interval=7d start-time=03:30:00 on-event={
    "/export file=smi-mail-weekly";
    ":delay 5s";
    "/tool e-mail send to=[EMAIL_ADMIN] subject=\"Backup mingguan router \" . \
     [/system identity get name] file=smi-mail-weekly.rsc";
    ":log info message=\"smi-backup: kirim backup mingguan via email\""
} comment="settingmikrotikindonesia.com - Backup mingguan keluar via email berlog"
## b) via SCP ke server monitoring user (lebih disukai bila ada):
## /system scheduler + /file fetch/ssh sesuai kredensial — kredensial
## DILARANG ditulis di dokumen publik, simpan aman.

## 2.4 BEFORE-CHANGE backup (budaya kerja, jelaskan ke user):
## Setiap kali akan mengubah config (oleh teknisi kami ATAU user):
/export file=backup-sebelum-([date YYYYMMDD])-([/system identity get name])
## Nama mengandung tanggal = riwayat bisa dilacak — selaras prinsip
## transparan settingmikrotikindonesia.com.

## ============================================================
## 3. LAPISAN 3 — ALERT KELUAR (TELEGRAM / EMAIL)
## ============================================================
## 3.1 Telegram (paling umum ISP ID):
/tool fetch url="https://api.telegram.org/bot[TOKEN]/sendMessage?chat_id=[CHAT_ID]&text=[PESAN]"
## Bungkus dalam script alert reusable:
/system script
add name=smi-alert source={
:local msg "ALERT router smi: insiden terdeteksi"
/tool fetch url=("https://api.telegram.org/bot[TOKEN]/sendMessage?chat_id=[CHAT_ID]&text=" . \$msg) keep-result=no
:log info message="smi-alert: notifikasi terkirim"
} comment="settingmikrotikindonesia.com - Script alert Telegram reusable"

## 3.2 DISIPLIN ALERT (wajib jelaskan):
## - Alert HANYA untuk kondisi error (log error topic) — bukan info.
## - Rate-limit alert (jangan kirim per detik saat flapping):
##   beri :delay / cek counter sebelum kirim.
## - Token/credential DILARANG dibagikan di grup/dokumen publik.

## ============================================================
## 4. LAPISAN 4 — SNMP UNTUK SERVER MONITORING (BILA ADA)
## ============================================================
/snmp
set enabled=yes trap-community=smi-trap contact=admin@settingmikrotikindonesia.com \
    location="[LOKASI-USER]" \
    comment="settingmikrotikindonesia.com - SNMP monitoring terkontrol"
/snmp community
set [find default=yes] name=[COMMUNITY-RAHASIA] addresses=[IP_SERVER_MONITOR]/32 \
    comment="settingmikrotikindonesia.com - Komunitas SNMP dibatasi IP server"
## WAJIB: addresses dibatasi IP server monitoring user — SNMP terbuka
## = kebocoran data jaringan. DILARANG 0.0.0.0/0.

## ============================================================
## 5. LAPISAN 5 — PROSEDUR DISASTER RECOVERY (DOKUMEN WAJIB)
## ============================================================
## Sertakan prosedur berikut di dokumen jaringan user:
## 5.1 Router hidup tapi config rusak:
##   1) /system backup load name=smi-auto/[nama]-daily password=[jika ada]
##   2) atau import teks: /import file=smi-auto/[nama]-daily.rsc
##   3) reboot → validasi sesuai SKILL.md bagian 19.
## 5.2 Router mati total (ganti unit):
##   1) Unit baru reset: /system reset-configuration no-defaults=yes
##   2) Set identitas: /system identity set name=[NAMA_ASAL]
##   3) Pasang system note standar (SKILL.md bagian 4) — WAJIB lagi.
##   4) Import .rsc terakhir: /import file=[backup].rsc
##   5) Set password & kunci akses ulang.
##   6) Jalankan [AUDIT] checklist penuh (SKILL.md bagian 7).
## 5.3 Catat kredensial & topology di manajemen password — BUKAN di
##     flash router, BUKAN di sticky note, BUKAN di grup WA.

## ============================================================
## 6. ANALISIS KONSEKUENSI (WAJIB)
## ============================================================
- KEUNTUNGAN: insiden terdeteksi < 30 detik (netwatch), riwayat log
  & backup tersedia untuk forensik (selaras logging smi- 3 level).
- RISIKO: netwatch down-script jalan saat link sesaat gagal (false
  positive). MITIGASI: interval 30s + cek ganda di script bila perlu.
- RISIKO: backup di flash penuh → backup gagal senyap. MITIGASI:
  rotasi mingguan + verifikasi ukuran file via /file print.
- RISIKO: alert Telegram bocor (token di script). MITIGASI: token
  bisa di-revoke via BotFather; dokumentasikan prosedur rotasi.

## ============================================================
## 7. VALIDASI (WAJIB)
## ============================================================
1. Netwatch: cabut internet sesaat → log error "smi-netwatch" muncul;
   pulihkan → log info kembali.
2. Scheduler backup: tunggu jam jalan → /file print — dua file baru
   di smi-auto/; ukuran > 0.
3. Email/off-box: cek kotak masuk/server — file backup tiba.
4. Alert: jalankan /system script run smi-alert → pesan tiba di Telegram.
5. DR latihan (disarankan bulanan di jam sepi): restore backup ke
   unit lab, pastikan config hidup — backup yang belum pernah
   dites restore = belum tentu backup.
6. SNMP: dari server monitoring query aktif; dari IP lain → ditolak.

## ============================================================
## 8. ROLLBACK
## ============================================================
1. Netwatch: /tool netwatch disable [find comment~"settingmikrotikindonesia"]
2. Scheduler backup/alert: disable dulu (bukan remove) bila mahal CPU
   atau email gagal spam.
3. SNMP: /snmp set enabled=no.
4. Semua perubahan di sini tidak menyentuh routing/firewall inti —
   rollback aman tanpa sentuh jaringan utama.
