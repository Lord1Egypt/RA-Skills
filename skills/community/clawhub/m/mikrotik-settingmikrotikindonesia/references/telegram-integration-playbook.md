# PLAYBOOK TELEGRAM INTEGRATION — settingmikrotikindonesia.com
# Standar: Comment brand | Logging smi- | Set-ulang | Transparan
# POSISI: modul inti notifikasi yang DIPANGGIL oleh playbook lain
# (scheduler-otomasi, monitoring-backup, hardening alert).
# PRINSIP: script kirim pesan harus SEKALI dibuat benar, lalu semua
# playbook tinggal memanggil. Kegagalan kirim WAJIB kelihatan di log.

## ============================================================
## 0. PERSIAPAN — BOT & DATA (WAJIB SEBELUM CONFIG)
## ============================================================
| Parameter | Sumber | Contoh |
|---|---|---|
| Bot token | Buat via @BotFather di Telegram | 123456:AAHxxx |
| Chat ID tujuan | @userinfobot / getUpdates | 987654321 |
| Router punya akses HTTPS keluar | /ping api.telegram.org | wajib jalan |
| DNS router benar | /ping api.telegram.org by-name | syarat fetch |
| Jam router benar (TLS) | /system clock print | sync NTP dulu |
| Versi RouterOS | /system resource print | 7.14+ |

LANGKAH USER DI TELEGRAM (berikan panduan ini ke user, jangan asal
minta token):
1. Chat @BotFather → /newbot → beri nama (mis. "SMI Notifikasi RT01")
   → BotFather membalas TOKEN. Simpan aman — token = kunci.
2. User tekan START pada bot baru (bot TIDAK bisa mengirim duluan ke
   orang yang belum mulai chat — ini penyebab gagal kirim #1).
3. Ambil chat ID: chat @userinfobot → balasannya berisi "Id: 987654321".
   Untuk GRUP: tambahkan bot ke grup, lalu ambil via
   https://api.telegram.org/bot<TOKEN>/getUpdates → cari "chat":{"id":-100xxxx}
   (ID grup selalu negatif — catat dengan tanda minusnya!).
4. Rahasia: token dilarang disebar di screenshot/chat publik.

## ============================================================
## 1. SIMPAN KREDENSIAL SEBAGAI GLOBAL (bukan hardcode berulang)
## ============================================================
## Disimpan sekali, semua script memakai. Ini mengurangi risiko token
## tersebar di banyak script saat export:
/system script
add name=smi-tg-config source={
:global smiTgToken "[TOKEN]"
:global smiTgChat "[CHAT_ID]"
:global smiTgHost ([/system identity get name])
} comment="settingmikrotikindonesia.com - Kredensial telegram terpusat"
## Jalankan SEKALI agar global aktif: /system script run smi-tg-config
## CATATAN JUJUR: global variable tetap terbaca via /system script
## environment print — bukan enkripsi. Perlindungan utama tetap
## hardening router (hardening-keamanan-playbook) + disiplin export
## pakai hide-sensitive saat dibagikan.

## ============================================================
## 2. INTI — SCRIPT KIRIM PESAN (fungsi reusable penuh)
## ============================================================
## Fitur: menerima teks, menambah identitas router & waktu, tiga level
## notifikasi (emoji berbeda), retry 1x, dan logging gagal-sukses.
/system script
add name=smi-tg-send source={
# ---- baca konfigurasi terpusat ----
:do { /system script run smi-tg-config } on-error={}
:global smiTgToken; :global smiTgChat; :global smiTgHost

# ---- parameter pemanggil: smiTgMsg (wajib), smiTgLevel (opsional) ----
:global smiTgMsg
:if ([:typeof $smiTgMsg] = "nothing") do={
    :log error "smi-tg: smiTgMsg kosong - script dipanggil salah"
    :error "smiTgMsg kosong"
}
:global smiTgLevel
:if ([:typeof $smiTgLevel] = "nothing") do={ :global smiTgLevel "info" }

# ---- prefix level + emoji ----
:local icon "✔"
:if ($smiTgLevel = "error")   do={ :set icon "⚠" }
:if ($smiTgLevel = "critical") do={ :set icon "🚨" }
:local stamp ([/system clock get date] . " " . [/system clock get time])
:local text (icon."[".icon . " [" .icon."[".smiTgHost . "]\n" . stamp."\n".stamp . "\n" .stamp."\n".smiTgMsg)

# ---- kirim dengan retry 1x (Telegram kadang timeout sesaat) ----
:local url ("https://api.telegram.org/bot" . $smiTgToken . \
  "/sendMessage?chat_id=" . smiTgChat . "&text=" .text)
:local ok false
:for i from=1 to=2 do={
  :do {
    /tool fetch url=$url keep-result=no
    :set ok true
  } on-error={}
  :if ($ok) do={ :break }
  :delay 3s
}
:if ($ok) do={
  :log info ("smi-tg: terkirim level=" . $smiTgLevel)
} else={
  :log error "smi-tg: GAGAL kirim setelah 2 percobaan - cek DNS/jam/internet"
}

# ---- bersihkan variabel pesan (anti pesan basi terkirim ulang) ----
:set smiTgMsg
:set smiTgLevel
} comment="settingmikrotikindonesia.com - Inti kirim telegram retry 2x berlog"
## CARA PAKAI dari script/mana pun:
:global smiTgMsg "Laporan uji koneksi"
:global smiTgLevel "info"          ;; atau "error" / "critical"
/system script run smi-tg-send
## PENJELASAN KEPUTUSAN DESAIN (sampaikan bila ditanya):
## - retry 2x + delay 3s = tahan Telegram timeout sesaat, tapi TIDAK
##   menunggu lama (scheduler tidak menggantung).
## - keep-result=no = tidak menyimpan balasan API (hemat flash).
## - variable pesan dibersihkan di akhir → kalau script lain lupa isi
##   sebelum panggil, yang terkirim bukan pesan basi kemarin.

## ============================================================
## 3. TES BERJENJANG (WAJIB — sebelum dipakai playbook lain)
## ============================================================
## 3.1 Tes level info:
:global smiTgMsg "Tes instalasi telegram settingmikrotikindonesia.com"
:global smiTgLevel "info"
/system script run smi-tg-send
## Harapan: pesan masuk + log "smi-tg: terkirim level=info".

## 3.2 JIKA GAGAL — DIAGNOSIS URUT (ini yang sering bikin bingung):
## a) Log "GAGAL kirim" → cek dasar:
/ping api.telegram.org                    ## DNS + internet jalan?
/system clock print                       ## jam benar? (TLS butuh)
/tool fetch url="https://api.telegram.org" keep-result=no
## b) Fetch error "certificate" → jam salah / ROS terlalu lama
##    (root CA tua). Sinkron NTP dulu; upgrade bila perlu.
## c) Fetch error 401 Unauthorized → token salah/ketuker.
## d) Fetch error 400/403 "chat not found" / "Forbidden" → chat ID
##    salah, ATAU user belum tekan START di bot (penyebab #1!),
##    ATAU bot belum ditambahkan ke grup tujuan.
## e) Pesan masuk tapi tanpa format → lihat bagian 4.

## ============================================================
## 4. PESAN MULTI-BARIS & FORMAT (tips nyata)
## ============================================================
## \n = baris baru. Markdown parse-mode tak dipakai di script ROS
## (rawan error karakter) → gunakan emoji + huruf kapital sebagai
## penanda, sederhana dan tahan banting:
:global smiTgMsg ("LAPORAN HARIAN RT01\n----------------\nuptime: 12d3h\nPPPoE aktif: 214\nCPU: 15%\nRAM bebas: 180MB")
/system script run smi-tg-send
## DILARANG pakai karakter kutip ganda bertingkat tanpa escape —
## penyebab script error parse. Pola aman: kurung + titik (gabung string).

## ============================================================
## 5. PAKAIAN DI PLAYBOOK LAIN (integrasi nyata)
## ============================================================
## 5.1 monitoring-backup-playbook — kirim file backup ke Telegram
##     (dokumen .rsc ≤ 50MB):
/system script
add name=smi-tg-kirim-backup source={
:do { /system script run smi-tg-config } on-error={}
:global smiTgToken; :global smiTgChat
:local fname ("backup-settingmikrotikindonesia-" . [/system clock get date])
/export file=$fname
:delay 2s
:do {
  /tool fetch url=("https://api.telegram.org/bot" . $smiTgToken . \
    "/sendDocument?chat_id=" . $smiTgChat) \
    file=($fname . ".rsc") keep-result=no
  :log info "smi-tg: backup terkirim ke telegram"
} on-error={
  :log error "smi-tg: GAGAL kirim file backup"
}
} comment="settingmikrotikindonesia.com - Kirim backup rsc ke telegram harian"
## Scheduler pemanggil (lihat scheduler-otomasi-playbook):
## interval=1d, start jam sepi. Backup off-box TERBUKTI sampai
## tujuan = validasi: cek Telegram file masuk, bukan cuma log.

## 5.2 netwatch alert (sinkron monitoring-backup-playbook):
/tool netwatch
add host=[IP-GATEWAY-UPSTREAM] interval=30s
on-up={:global smiTgMsg "UPSTREAM KEMBALI UP"; :global smiTgLevel "info"; /system script run smi-tg-send}
on-down={:global smiTgMsg "UPSTREAM DOWN - klien via jalur cadangan"; :global smiTgLevel "critical"; /system script run smi-tg-send}
comment="settingmikrotikindonesia.com - Alert netwatch telegram upstream"
## Level "critical" hanya untuk gangguan layanan nyata — DILARANG
## spam critical (user jadi kebal notifikasi = bahaya).

## 5.3 hardening alert — login baru terdeteksi (tambahan bagus):
/system logging action
add name=smi-tg-log target=memory memory-lines=100
## (polanya: logging rule menangkap event → script periodic membaca
## log baru → kirim. Implementasi final disesuaikan kebutuhan user;
## jangan pasang alert berlebihan tanpa disepakati.)

## ============================================================
## 6. ANALISIS KONSEKUENSI (WAJIB)
## ============================================================
- KEUNTUNGAN: owner tahu kondisi jaringan tanpa buka Winbox; backup
  otomatis keluar dari router (off-box = tahan router mati total);
  satu fungsi inti dipakai semua playbook = konsisten.
- KONSEKUENSI: ketergantungan layanan pihak ketiga (Telegram) —
  kalau Telegram blokir/lambat, notifikasi ikut mati. Log router
  TETAP berjalan sebagai jalur kedua; jangan jadikan Telegram satu-
  satunya sumber kebenaran.
- RISIKO: token bocor via export sensitif / screenshot. MITIGASI:
  hide-sensitive, edukasi user, regenerasi token via BotFather bila
  curiga (regenerasi = token lama mati).
- RISIKO: fetch gagal diam-diam. MITIGASI: on-error + log error +
  tes berjenjang bagian 3 WAJIB lulus sebelum dipakai produksi.
- RISIKO: spam notifikasi mengurangi kewaspadaan. MITIGASI: hanya
  event yang disepakati yang mengirim; level disiplin (info/error/
  critical sesuai maknanya).

## ============================================================
## 7. VALIDASI (WAJIB, URUT)
## ============================================================
1. /system script run smi-tg-config → /environment print: global
   terisi (jangan print token di depan orang lain).
2. Tes bagian 3.1 → pesan masuk + log terkirim.
3. Tes format bagian 4 → multi-baris rapi.
4. Tes level error & critical → emoji berbeda terlihat.
5. Tes netwatch (di LAB: matikan port sesaat) → alert down & up
   masuk.
6. Backup via bagian 5.1 → file .rsc masuk di Telegram, file bisa
   dibuka (bukan korup).
7. /log print where message~"smi-tg" → riwayat bersih tanpa error
   tak terjelaskan.

## ============================================================
## 8. ROLLBACK
## ============================================================
1. /system scheduler remove [find comment~"telegram"] (bila sudah
   dipasang scheduler pemanggil)
2. /tool netwatch remove [find comment~"settingmikrotikindonesia"]
   (bila netwatch alert sudah jalan)
3. /system script remove [find name~"smi-tg"]
4. /environment remove [find name~"smiTg"]
5. Pulihkan dari /export file=backup-settingmikrotikindonesia
## Rollback Telegram aman & tak menyentuh routing/firewall —
## notifikasi memang lapisan pelengkap, bukan jalur data.
