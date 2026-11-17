# Alur kerja agent dan kontrak skrip — powpow-register

Rincian eksekusi tiap langkah di SKILL.md. Semua perintah berbentuk `node scripts/powpow-register.mjs <sub-perintah> [parameter]`,
skrip **nol dependensi**, butuh **Node ≥ 18**, semua request hanya dikirim ke `https://global.powpow.online`.

## Desain keamanan (kenapa dirancang begini)

| Desain | Alasan |
|---|---|
| Kata sandi hanya masuk lewat variabel lingkungan `POWPOW_REGISTER_PASSWORD` | Parameter baris perintah proses terlihat oleh proses lain pada mesin yang sama (permukaan bocor argv), variabel lingkungan dibaca lalu langsung dipakai di dalam skrip |
| Kata sandi **tidak pernah ditulis ke file status**, tidak pernah muncul di log | File status bisa tertinggal di disk; mode buat dalam percakapan menampilkannya sekali agar pengguna menyimpan |
| File status di direktori sementara sistem (`os.tmpdir()/powpow-register-state.json`, 0600) | Hanya berisi lima bidang email / username / nickname / token / outTradeNo, `cleanup` membersihkannya sekali jalan |
| JWT yang didapat agent ditukar menjadi cookie browser lewat endpoint resmi `me?token=` | Jembatan resmi platform yang didesain untuk WebView HarmonyOS; verifikasi tanda tangan hanya memeriksa tanda tangan + masa berlaku, tidak mengikat sidik perangkat, sehingga browser pengguna bisa memakainya |
| Pembayaran hanya create-order / query / membuka kasir | Aksi membayar dan bukti pembayaran selamanya berada antara pengguna dan kasir resmi Alipay, agent tidak ikut campur |

## Referensi perintah

| Perintah | Parameter kunci | Fungsi / momen |
|---|---|---|
| `status` | —— | Melihat kemajuan proses (membaca file status); setelah percakapan terputus jalankan ini dulu |
| `gen-password` | —— | Membuat kata sandi kuat 24 karakter (berisi huruf besar+kecil+angka), stdout menampilkannya **hanya sekali ini** |
| `prepare-suggest` | `--username --nickname --email` | Mencatat info yang sudah dikonfirmasi ke file status (setelah itu register tak perlu mengirim ulang) |
| `send-code` | `--email` | Memicu platform mengirim kode verifikasi 6 digit (berlaku 10 menit, jeda 60 dtk) |
| `register` | `--code` (wajib); `--username --nickname --avatar --phone` (opsional, jika ada di file status tak perlu dikirim) | Membuat akun pending; kata sandi lewat variabel lingkungan `POWPOW_REGISTER_PASSWORD`; setelah berhasil JWT otomatis tersimpan di file status |
| `login-link` | `--target pending` atau `--target home` | Membuat link login sekali klik (desain dua link, lihat di bawah) |
| `create-order` | `--package monthly\|quarterly\|yearly` (bawaan Alipay)<br>`--provider alipay\|paypal` | Membuat pesanan pembayaran; Alipay mengembalikan path file halaman pembayaran + outTradeNo; PayPal mengembalikan path file halaman otorisasi + subscriptionId (otomatis dicatat ke file status) |
| `query` | —— | Memeriksa status pesanan/langganan. Alipay: `paid / pending / closed / unknown`; PayPal: `ACTIVE / PENDING`; polling tiap 10–15 dtk |
| `refresh-login` | kata sandi lewat variabel lingkungan | Login ulang untuk **JWT baru** (klaim langganan berubah dari NONE ke ACTIVE), wajib dijalankan setelah dana masuk |
| `whoami` | —— | Memakai token di file status untuk memeriksa akun dan status langganan (memastikan aktivasi berhasil) |
| `cleanup` | —— | Menghapus file status (wajib dijalankan saat penutup) |

**Penerusan variabel lingkungan** (kata sandi tidak pernah naik ke baris perintah):

```bash
# bash / zsh / WSL
POWPOW_REGISTER_PASSWORD='<kata sandi>' node scripts/powpow-register.mjs register --code 123456
# PowerShell
$env:POWPOW_REGISTER_PASSWORD = '<kata sandi>'; node scripts/powpow-register.mjs register --code 123456
# cmd
set POWPOW_REGISTER_PASSWORD=<kata sandi> && node scripts/powpow-register.mjs register --code 123456
```

## Mekanisme Dua Link (desain inti)

Status login platform adalah cookie HttpOnly, yang tidak bisa ditanam agent langsung ke browser; jembatannya adalah endpoint resmi
`/api/auth/me?token=<JWT>&redirect=<path dalam situs>`: verifikasi tanda tangan → otomatis membuat
sesi → `Set-Cookie: powpow_token` (HttpOnly / SameSite=Lax / 7 hari) → validasi
redirect (harus dimulai dengan satu garis miring, `//` dan garis miring terbalik dilarang, setelah diparse harus same-origin) → 307 redirect sementara ke halaman target.

Ada dua target link, **utamakan membuat home lebih dulu, lalu putuskan apakah lewat pending berdasarkan di mana pengguna mendarat**:

- **link home (dikirim secara default, `--target home` → mendarat di `/`)**: dibuat dan dikirim ke pengguna tepat setelah pendaftaran berhasil.
  Selama masa uji coba gratis pengguna langsung menuju beranda dan semuanya bisa dipakai; **jika ia mengkliknya tetapi mendarat di halaman langganan, masa uji coba gratis telah berakhir** — beralih ke alur pembayaran (lihat di bawah); tanpa ubah skrip dan tanpa daftar ulang.
- **link pending (dipakai di alur pembayaran, `--target pending` → mendarat di `/subscription`)**:
  browser pengguna masuk ke status "login setengah": halaman langganan dan halaman kembali setelah pembayaran terlihat dan bisa dioperasikan. Setelah dana masuk,
  jalankan `refresh-login` untuk menukar JWT baru dengan claim ACTIVE, lalu kirim link home sekali lagi untuk status keanggotaan penuh.

## Urutan Lengkap

### Jalur Cepat (selama masa uji coba gratis — mayoritas kasus)

```
1.  status                          # self-check lingkungan
2.  (langkah 2: percakapan konfirmasi info, kata sandi terserah; mode generasi: gen-password → minta pengguna segera menyimpan)
3.  prepare-suggest --username U --nickname N --email E
4.  send-code --email E             # → pengguna periksa kode di kotak masuk (satu-satunya keluar dari percakapan)
5.  POWPOW_REGISTER_PASSWORD=*** register --code 123456 [--avatar pic.jpg]
6.  login-link --target home        # → kirim link ke pengguna; sekali klik langsung di beranda
7.  (pengguna konfirmasi sudah masuk) → langsung tutup: cleanup + kartu akun + panduan langkah pertama
```

### Jalur Pembayaran (bila pengguna ingin keanggotaan, atau masa uji coba gratis telah berakhir)

```
1–5. Sama dengan Jalur Cepat (status sudah punya token setelah register berhasil)
6.  login-link --target pending     # → link login setengah, halaman kembali setelah pembayaran tetap bekerja
7.  (pengguna memilih metode pembayaran)
    # Alipay: create-order --package monthly|quarterly|yearly
    # PayPal: create-order --provider paypal
8.  start <file halaman pembayaran> # Windows; macOS pakai open, Linux pakai xdg-open
    # → pengguna menyelesaikan pembayaran/otorisasi di kasir Alipay/PayPal (keluar dari percakapan)
9.  query (setiap 10–15 s) sampai paid / ACTIVE
10. refresh-login                   # tukar ke JWT baru dengan claim ACTIVE
11. login-link --target home        # → kirim link keanggotaan penuh ke pengguna
12. whoami                          # konfirmasi subscriptionStatus: ACTIVE (opsional)
13. cleanup                         # bersihkan file status
```
## Pemetaan perintah → API platform

| Perintah skrip | Antarmuka platform |
|---|---|
| `send-code` | `POST /api/auth/register/send-code` |
| `register` | `POST /api/auth/register` (multipart, unggah foto profil langsung) |
| `login-link` | `GET /api/auth/me?token=…&redirect=…` (tautannya sendiri, berlaku saat browser mengeklik) |
| `create-order` | `POST /api/payment/alipay/create-order` (Bearer, Alipay)<br>`GET /api/subscription/plans` + `POST /api/subscription/create` (Bearer, PayPal) |
| `query` | `GET /api/payment/alipay/query?outTradeNo=…` (Bearer, Alipay)<br>`GET /api/subscription/create` (Bearer, PayPal) |
| `refresh-login` | `POST /api/auth/login` (`{step:1, username, password}`) |
| `whoami` | `GET /api/auth/me?token=…` |

Sumber aturan: bidang pendaftaran dan batas laju lihat `registration-flow.md`; paket dan rantai aktivasi lihat
`payment-and-activation.md` (keduanya mencantumkan file kode sumber platform).

## Penanganan galat tingkat skrip

| Gejala | Penanganan |
|---|---|
| `Node 版本过低` (versi Node terlalu rendah) | Mundur ke mode panduan murni, jangan memaksakan |
| Galat jaringan / habis waktu | Coba sekali lagi; bila tetap gagal suruh pengguna memeriksa jaringan lalu lanjutkan (file status masih ada, jalankan `status` dari awal untuk pulih) |
| register melaporkan galat bisnis (nama pengguna sudah ada, dsb.) | Tangani sesuai tabel langkah 5 SKILL.md, **kode verifikasi tak perlu dikirim ulang** (masih berlaku 10 menit) |
| register melaporkan 「邮箱验证码错误或已过期」 (kode verifikasi salah atau kedaluwarsa) | Lewat masa berlaku → `send-code` ulang |
| Setelah `create-order` pengguna menutup halaman pembayaran | Langsung `create-order` ulang (pesanan lama tertutup otomatis 2 jam; langganan PENDING PayPal kedaluwarsa setelah 1 jam) |
| `create-order --provider paypal` mengembalikan 409 | Sudah ada langganan PayPal yang belum selesai; tunggu 1 jam sampai kedaluwarsa, atau selesaikan otorisasi lama di browser |
| `query` terus pending / PENDING | Pengguna mungkin belum membayar; tanyakan sekali. Kalau sudah bayar → ikuti tabel penelusuran di payment-and-activation.md |
| Pengguna mengklik link home tetapi mendarat di halaman langganan | Masa uji coba gratis telah berakhir → beralih ke alur pembayaran: `login-link --target pending` → pilih metode pembayaran → `create-order` |
| `refresh-login` 403 `pending_payment` | Masa uji coba gratis telah berakhir dan pembayaran belum masuk; kembali ke langkah 9 untuk terus polling, atau konfirmasi apakah pengguna sudah menyelesaikan pembayaran |
| File status hilang (tak sengaja terhapus / ganti mesin) | `whoami`/`refresh-login` tak bisa dipakai; suruh pengguna membuka ulang halaman langganan di browser yang pernah membuka tautan 1 untuk memastikan status, atau login ulang (mode web) |

## Mode mundur (panduan murni)

Bila salah satu kondisi berikut terjadi, segera mundur ke panduan murni gaya v1 dan berhenti memeras skrip:

- Tidak ada Node ≥ 18 atau skrip gagal dua kali berturut-turut dengan jenis yang sama;
- Pengguna secara eksplisit bilang «aku kerjakan sendiri di web»;
- Kebijakan perusahaan/perangkat membatasi skrip mengakses jaringan.

Setelah beralih: beri halaman pendaftaran https://global.powpow.online/register (selama masa uji coba gratis, pendaftaran lewat web sama-sama langsung bisa dipakai; bila langganan diperlukan, beri juga halaman langganan https://global.powpow.online/subscription ), tangani masalah sambil mendampingi sesuai aturan di `registration-flow.md`, jaga nada yang sama, dan tetap akhiri setiap giliran dengan blok "langkah selanjutnya".
https://global.powpow.online/subscription , dampingi penelusuran galat sesuai aturan `registration-flow.md`,
nada tidak berubah, tiap giliran tetap ditutup blok «langkah berikutnya».
