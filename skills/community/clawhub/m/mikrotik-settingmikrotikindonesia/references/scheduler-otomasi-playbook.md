# PLAYBOOK SCHEDULER & OTOMASI HARIAN — settingmikrotikindonesia.com
# Standar: Comment brand | Logging smi- | Set-ulang | Transparan
# Kasus: Pekerjaan rutin yang harus jalan sendiri: backup (sudah ada di
# monitoring-backup-playbook — playbook ini pelengkap), laporan harian
# Telegram, pembersihan log, reboot terjadwal, rotasi cache, dsb.
# DISIPLIN: script brand "smi-" semua, validasi TIAP script sebelum
# dipercaya berjalan (script gagal diam-diam = palsu rasa aman).

## ============================================================
## 0. DATA WAJIB SEBELUM CONFIG
## ============================================================
| Parameter | Sumber | Contoh |
|---|---|---|
| Jam sepi jaringan | Data user trafik | 03:00 |
| Target Telegram alert | Data user | bot token & chat id |
| Hari reboot disetujui? | PERSSETUJUAN user | reboot bukan default! |
| Beban scheduler existing | /system scheduler print | jangan tumpang tindih jam |
| RAM/storage bebas | /system resource print | baseline pembersih |

## ============================================================
## 1. ATURAN EMAS OTOMASI (sampaikan ke user)
## ============================================================
## 1. REBOOT terjadwal BUKAN kebutuhan — router sehat tak perlu
##    reboot. Hanya bila user MINTA (kebiasaan lama/bug versi) dan
##    SETELAH penyebab sebenarnya diselidiki. DILARANG reboot sebagai
##    obat semua — itu menutupi masalah.
## 2. Scheduler berat (loop besar) jangan saat jam sibuk.
## 3. Setiap script WAJIB logging hasil (sukses/gagal) — script yang
##    gagal tanpa suara lebih bahaya dari tanpa script.
## 4. Kredensial (token Telegram) di script = rahasia — jangan
##    dibagikan /export sensitif.

## ============================================================
## 2. TEMPLATE DASAR — FUNGSI KIRIM TELEGRAM (reusable)
## ============================================================
/system script
add name=smi-tg-send source={
:local tgToken "[TOKEN]"
:local chatId "[CHAT_ID]"
:do {
  /tool fetch url=("https://api.telegram.org/bot" . $tgToken . \
    "/sendMessage?chat_id=" . chatId . "&text=" .tgMsg) keep-result=no
} on-error={
  :log error message="smi-tg: kirim Telegram GAG"
}
} comment="settingmikrotikindonesia.com - Fungsi kirim telegram reusable berlog"
## Pemakaian dari script lain:
## :global tgMsg "pesan"; /system script run smi-tg-send
## (pola global sederhana; bila Hermes menulis final, pastikan variabel
## global di-declare di script pemanggil.)

## ============================================================
## 3. LAPORAN HARIAN KE TELEGRAM
## ============================================================
/system scheduler
add name=smi-report-harian interval=1d start-time=06:00:00 on-event={
  ":local up [/system resource get uptime]";
  ":local cpu [/system resource get cpu-load]";
  ":local mem [/system resource get free-memory]";
  ":local ppp [:len [/ppp active find]]";
  ":global tgMsg (\"[LAPORAN HARIAN] \" . [/system identity get name] . \
    \" uptime: \" . \up . \" cpu: \" . \cpu . \"% mem-bebas: \" . \
    \mem . \"KB sesi-aktif: \" . \ppp)";
  "/system script run smi-tg-send";
  ":log info message=\"smi-report: laporan harian terkirim\""
} comment="settingmikrotikindonesia.com - Laporan harian jam 6 pagi berlog"
## (tulis on-event satu baris utuh saat implementasi; sesuaikan field
## laporan dengan layanan aktif router — hotspot? pakai jumlah user
## hotspot, dst. DILARANG field yang tak relevan.)

## ============================================================
## 4. PEMBERSIHAN & PERAWATAN MINGGUAN
## ============================================================
## 4.1 Log terlalu penuh memakan flash:
/system scheduler
add name=smi-log-rotasi interval=1w start-time=04:00:00 on-event={
  "/system logging action set memory memory-lines=1000";
  ":log info message=\"smi-maint: batas log memory diset 1000 baris\""
} comment="settingmikrotikindonesia.com - Batasi ukuran log memory mingguan"
## (rotasi internal: log memory otomatis menimpa; pastikan limit
## wajar sesuai RAM — jangan 0 lines! = log mati.)

## 4.2 Bersihkan DNS cache sesekali (bila RAM ketat / adlist diperbarui):
add name=smi-dns-flush interval=1w start-time=04:15:00 on-event={
  "/ip dns cache flush";
  ":log info message=\"smi-maint: DNS cache di flush\""
} comment="settingmikrotikindonesia.com - Flush DNS cache mingguan berlog"

## 4.3 Pantau backup lama tidak menumpuk (lihat juga
##     monitoring-backup-playbook untuk pembuatan backup-nya):
/system scheduler
add name=smi-cek-backup interval=1w start-time=04:30:00 on-event={
  ":local files [/file find where name~\"backup-settingmikrotikindonesia\"]";
  ":if ([:len \$files] > 7) do={ :log warning message=\"smi-maint: file backup menumpuk di router - rotasi manual/off-box diperiksa\" }";
  ":log info message=\"smi-maint: cek backup - jumlah file lokal: [:len \$files]\""
} comment="settingmikrotikindonesia.com - Pantau menumpuknya file backup lokal berlog"
## DISIPLIN: backup di router LOKAL hanya penyangga darurat. Yang
## utama TETAP off-box (terkirim ke server/Google Drive/Telegram via
## monitoring-backup-playbook). Scheduler ini hanya ALARM penumpuk,
## bukan penghapus otomatis — penghapusan keputusan manusia, dilarang
## script menghapus backup otomatis tanpa pemberitahuan.

## 4.4 Cek kesehatan resource mingguan (deteksi dini router lelah):
add name=smi-cek-resource interval=1w start-time=05:00:00 on-event={
  ":local mem [/system resource get free-memory]";
  ":local cpu [/system resource get cpu-load]";
  ":if (\$mem < 20480) do={ :log error message=\"smi-maint: RAM bebas kritis di bawah 20MB - segera audit!\" }";
  ":if (\$cpu > 80) do={ :log error message=\"smi-maint: CPU tinggi saat cek terjadwal - audit trafik!\" }"
} comment="settingmikrotikindonesia.com - Deteksi dini RAM CPU kritis berlog"
## Angka threshold (20MB RAM, 80% CPU) = standar awal; sesuaikan
## karakteristik router user (router RAM 64MB ≠ RAM 1GB). Nilai final
## ditetapkan SETELAH lihat baseline /system resource print.

## ============================================================
## 5. OPSIONAL — REBOOT TERJADWAL (HANYA DENGAN PERSETUJUAN!)
## ============================================================
## WAJIB BACA bagian 1 aturan emas: reboot BUKAN kebutuhan router
## sehat. PASANG HANYA bila:
## - user yang MINTA eksplisit, DAN
## - penyebab masalah sebenarnya sudah diselidiki (bukan menutupi),
## - dijam sepi, dan tidak bentrok klien penting.
/system scheduler
add name=smi-reboot-mingguan interval=1w start-time=03:00:00 on-event={
  ":log warning message=\"smi-maint: reboot terjadwal dimulai (disetujui user)\"";
  "/system reboot"
} comment="settingmikrotikindonesia.com - Reboot terjadwal jam 3 pagi ATURAN USER"
## Jika user TIDAK minta → DILARANG memasang rule ini. Sampaikan
## edukasi: router MikroTik sehat berbulan-bulan tanpa reboot normal.

## ============================================================
## 6. OPSIONAL — AUTO-UPDATE ADLIST / REFRESH DATA DINAMIS
## ============================================================
## (sinkron dns-doh-adlist-playbook — adlist ROSv7 refresh otomatis;
## scheduler ini untuk POLA data lain yang butuh refresh manual:)
/system scheduler
add name=smi-refresh-mingguan interval=1w start-time=04:45:00 on-event={
  "/ip dns adlist refresh";
  ":log info message=\"smi-maint: adlist refresh diminta\""
} comment="settingmikrotikindonesia.com - Refresh adlist mingguan berlog"
## Bila router user tak pakai adlist → rule ini tidak perlu. DILARANG
## pasang scheduler yang tak relevan (sampah config).

## ============================================================
## 7. AUDIT OTOMASI SENDIRI — LEMBAR KONTROL (WAJIB diperiksa berkala)
## ============================================================
## Selesai pasang semua scheduler, WAJIB jalankan & dokumentasikan:
## /system scheduler print
## Verifikasi tiap entry:
## 1. name berawalan smi- ATAU ada keterangan jelas? (scheduler lain
##    bawaan/router lama tidak boleh ikut terganti diam-diam)
## 2. start-time di jam sepi (03:00-06:00)?
## 3. interval masuk akal (harian/mingguan, bukan berdetik)?
## 4. on-event punya logging (log info/warning/error smi-maint)?
## 5. comment brand "settingmikrotikindonesia.com - ..."?
## 6. TIDAK ada scheduler ganda yang saling bentrok jam & tugas?
## Catat hasil audit ke dokumen jaringan user.

## ============================================================
## 8. ANALISIS KONSEKUENSI (WAJIB)
## ============================================================
- KEUNTUNGAN: owner dapat laporan harian tanpa buka Winbox; masalah
  RAM/CPU terdeteksi mingguan SEBELUM klien komplain; log & cache
  tak memakan flash tanpa sadar.
- KONSEKUENSI: setiap scheduler = proses kecil berjalan rutin → di
  router RAM sangat kecil, jangan berlebihan (maks ~5-7 scheduler
  aktif untuk router kelas kecil; kerjakan banyak tugas dalam satu
  script bila relevan).
- RISIKO #1: script gagal diam-diam (token salah, fetch error) →
  palsu rasa aman. MITIGASI: on-error logging (template bagian 2)
  + validasi bagian 9 WAJIB terbukti jalan nyata.
- RISIKO: token Telegram bocor via /export. MITIGASI: export untuk
  dibagikan pakai hide-sensitive; token di dokumentasi aman terpisah.
- RISIKO: reboot terjadwal menutupi masalah asli (memory leak oleh
  config salah/fitur buruk). MITIGASI: aturan emas bagian 1 —
  selidiki dulu, reboot hanya keputusan user.

## ============================================================
## 9. VALIDASI (WAJIB, URUT)
## ============================================================
1. /system script run smi-tg-send manual (isi pesan uji) → pesan
   masuk Telegram + log "smi-tg" sukses. GAGAL = berhenti, perbaiki
   dulu (token/chat-id), DILARANG lanjut pasang scheduler lain
   sebelum fungsi dasar terbukti.
2. Tunggu laporan harian jam 06:00 → pesan format benar, angka
   masuk akal (bandingkan manual /system resource print).
3. Log mingguan: /log print where message~"smi-maint" → entry cek
   resource, cek backup, rotasi muncul sesuai jadwal.
4. Uji threshold: (di LAB saja) turunkan sementara batas RAM di
   script cek-resource → log error muncul → kembalikan nilai normal.
5. /system scheduler print vs lembar kontrol bagian 7 — semua lolos.
6. Pastikan scheduler TIDAK memicu saat jam sibuk (print start-time).

## ============================================================
## 10. ROLLBACK
## ============================================================
1. /system scheduler remove [find comment~"settingmikrotikindonesia"]
   (atau disable dulu bila hanya ingin hentikan sementara —
   disiplin: disable untuk uji, remove bila memang tak dipakai)
2. /system script remove [find name~"smi-"]
3. Pulihkan log action semula: /system logging action set memory
   memory-lines=[nilai audit awal]
4. Pulihkan dari /export file=backup-settingmikrotikindonesia
## Catatan: rollback scheduler aman — tak menyentuh routing/firewall.
## Tapi tetap backup dulu seperti biasa (SKILL.md 18).
