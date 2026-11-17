---
name: powpow-register
description: Membantu pengguna menyelesaikan pendaftaran PowPow (Bubble) dan login sekali klik sepenuhnya di dalam percakapan. Agent mengisi formulir atas nama pengguna (termasuk unggah avatar) dan mengirim kode verifikasi email; pengguna hanya perlu memberikan informasi dasar dan memeriksa kode verifikasi sekali — tanpa pernah meninggalkan percakapan. Platform saat ini sedang dalam masa uji coba gratis: akun yang sudah terdaftar langsung bisa memakai semua fitur; pembayaran langganan (Alipay/PayPal) adalah peningkatan keanggotaan opsional, yang juga bisa ditangani agent dengan pembuatan pesanan dan pelacakan dana masuk bila diperlukan. Terpicu ketika pengguna mengatakan "daftar Bubble", "buat akun powpow", "cara daftar Bubble", "bantu saya buat akun powpow", "sign up powpow"; juga menangani masalah pendaftaran (kode verifikasi tidak masuk, nama pengguna/email sudah dipakai) dan masalah aktivasi (saat login bilang "akun belum diaktivasi" / pending_payment, cara langganan/bayar, Bubble gratis atau berbayar). Membutuhkan Node ≥ 18; bila tidak tersedia, otomatis beralih ke mode panduan murni. Tidak mencakup posting/membuat manusia digital (itu tugas powpow-simple), maupun pengembangan kode.
version: 2.2.0
metadata:
  openclaw:
    emoji: "\U0001F4DD"
    homepage: https://global.powpow.online
---

# PowPow Register (asisten pendaftaran Gelembung)

Membawa pengguna baru dari "tidak tahu Bubble itu apa" menjadi "login sekali klik, siap dimainkan" — seluruhnya di dalam percakapan. Pengguna hanya meninggalkan percakapan satu kali: **untuk memeriksa kode verifikasi di kotak masuk**. Platform saat ini sedang dalam masa uji coba gratis: setelah mendaftar, semua fitur bisa dipakai, tidak perlu bayar; pembayaran langganan adalah peningkatan keanggotaan opsional (agent juga membuka kasir dan melacak dana masuk).

**Versi 2.2.0** · 2026-10-18 (sejak v2 ini mode perantara agent: kontrak skrip dan urutan lengkap ada di `references/agent-flow.md`; aturan field, batas laju, dan diagnosa error di `references/registration-flow.md`; kanal pembayaran di `references/payment-and-activation.md`; daftar tangkapan layar produk di `references/screenshots.md`. Sejak v2.1.0 langganan PayPal juga bisa ditangani agent, sebagai pilihan bersama Alipay. Sejak v2.2.0 platform memasuki masa uji coba gratis: daftar lalu login sekali klik langsung bisa dipakai; pembayaran berubah menjadi peningkatan opsional — jika pengguna membuka link dan mendarat di halaman langganan, berarti masa uji coba telah berakhir, ikuti alur pembayaran dari langkah 7; alurnya menyesuaikan sendiri, tidak perlu ubah skrip)

## Lingkungan eksekusi

- Skrip utama `scripts/powpow-register.mjs`: **nol dependensi**, butuh **Node ≥ 18**. Sebelum mulai, jalankan sekali `node scripts/powpow-register.mjs status` untuk memastikan lingkungan berfungsi.
- Semua request skrip hanya dikirim ke domain resmi `https://global.powpow.online`.
- **Node tidak ada / skrip error**: otomatis beralih ke mode panduan murni — beri pengguna halaman pendaftaran https://global.powpow.online/register dan dampingi sesuai `references/registration-flow.md` (selama masa uji coba gratis, pendaftaran lewat web sama-sama langsung bisa dipakai). Jangan memaksa skrip berulang kali.
- Pemulihan setelah percakapan terputus: jalankan `status` dulu untuk melihat proses berhenti di langkah mana, lalu lanjutkan dari sana.

## Trigger Conditions

- Niat mendaftar: «daftar Gelembung», «buat akun powpow», «cara daftar Gelembung», «sign up powpow»
- Pendaftaran macet: «kode verifikasi tidak datang», «katanya nama pengguna sudah ada», «kata sandi terus tidak lolos»
- Masalah setelah daftar: "login bilang akun belum diaktivasi", "403 pending_payment", "cara bayar/langganan Bubble", "Bubble gratis atau berbayar"

**Tidak aktif untuk**: memposting/membuat manusia digital (→ powpow-simple); pengembangan kode sisi Web (lihat skill pengembangan). Pengguna yang ingin mendaftar sekaligus memposting: selesaikan skill ini dulu, setelah aktif baru serahkan ke powpow-simple.

## Gambaran proses

| Langkah | Apa yang agent lakukan | Apa yang pengguna lakukan |
|---|---|---|
| 1 Perkenalan produk | Memperkenalkan + mengirim tangkapan layar | Melihat sebentar |
| 2 Konfirmasi info | Merekomendasikan nama pengguna/nama panggilan, kata sandi pilih 1 dari 2, menanyakan email | Mengonfirmasi, memberi data |
| 3 Kirim kode | `send-code` | —— |
| 4 Baca kode | —— | Masuk email, membaca kode 6 digit, mengirimkannya |
| 5 Kirim pendaftaran | `register` (termasuk unggah foto profil), menangani galat otomatis | —— |
| 6 Login sekali klik | `login-link(home)` langsung ke beranda; jika mendarat di halaman langganan, lanjut ke langkah 7 | Klik link dan mulai main |
| 7 Peningkatan langganan (opsional) | Hanya bila pengguna mau keanggotaan / masa gratis telah berakhir: tangani seluruh alur pembayaran | Pilih metode, bayar |
| 8 Penutup | `cleanup` + menyerahkan info akun + panduan pengalaman + saran plugin | Mulai bermain |

## Langkah 1: perkenalan produk + tangkapan layar (tidak boleh dilewati)

Sebagian besar pengguna belum pernah melihat Gelembung. Hal pertama bukan menceritakan proses, melainkan membuat mereka **melihat** produknya:

1. Perkenalkan Gelembung dalam ~120 karakter: mengubah foto-foto spontan menjadi catatan perjalanan, menyematkannya di peta publik sebagai sebuah «gelembung»; gelembung mendingin seiring waktu, «suka» dari orang lain bisa menghidupkannya kembali; di peta juga ada «manusia digital» yang bisa diajak ngobrol. Alamat platform: https://global.powpow.online ; ingin lihat video dulu: https://www.bilibili.com/video/BV1Wu826UEVz/
2. **Kirim tangkapan layar**. Tangkapan layar sudah dibundel bersama skill di `assets/screenshots/powpow-0N.jpg` — kirim langsung sebagai file gambar lokal, tanpa perlu internet. Daftar, isi tiap gambar, dan momen penggunaannya ada di `references/screenshots.md`. Pasangan yang paling sering dipakai di pembukaan: halaman peta (powpow-03) + halaman detail postingan (powpow-06).

Aturan tangkapan layar (aturan keras):

- Tangkapan layar **sudah dibundel bersama skill** di `assets/screenshots/` (`powpow-0N.jpg`) — kirim langsung sebagai file gambar lokal; bisa dipakai di semua lingkungan, termasuk yang tidak bisa membuka GitHub.
- Setiap kali kirim hanya 1–3 gambar yang relevan dengan topik saat ini, jangan menumpuk semuanya sekaligus.
- Jika file di dalam bundel hilang tak sengaja, fallback ke tautan hosting yang tercantum di `references/screenshots.md` (catatan: di daratan Tiongkok bisa saja tidak terbuka).

Selesai memperkenalkan, kembalikan pilihan ke pengguna: **«Kalau kamu mau daftar, tiga menit lagi akunmu selesai saya buat di obrolan ini; kamu cukup membaca kode verifikasi di email satu kali.»**

## Langkah 2: konfirmasi info pendaftaran (satu pertanyaan per giliran, jangan menanyakan semuanya sekaligus)

- **Nama pengguna** (wajib): **proaktif menyarankan satu** dari konteks percakapan/nama pengguna sistem (2~50 karakter, tidak peka huruf besar/kecil); pengguna mengangguk ya dipakai, mau ganti ya diganti.
- **Kata sandi** (wajib; lebih dulu suruh memilih 1 dari 2):
  - Pengguna memberikan sendiri → lalu sampaikan ke skrip lewat variabel lingkungan, **jangan sekali-kali memasukkannya ke parameter baris perintah**;
  - agent yang membuat → jalankan `node scripts/powpow-register.mjs gen-password` dan **segera kirim kata sandi yang baru dibuat ke pengguna untuk disimpan** (hanya ditampilkan sekali, setelah itu tidak muncul lagi).
- **Email** (wajib): harus diberikan pengguna sendiri — ini jangkar identitas akun, **jangan menebak-nebak**.
- **Nama panggilan** (opsional): sarankan bawaan sama dengan nama pengguna.
- **Foto profil** (opsional): jika pengguna memberi path gambar lokal (≤5MB, bukan SVG) skrip mengunggahnya langsung; kalau tidak ada ya dilewati (platform memakai logo bawaan); jika kamu punya kemampuan menghasilkan gambar, boleh menawarkan membuatkan satu.
- **Nomor telepon** (opsional, nomor daratan Tiongkok): bawaan dilewati; tanyakan hanya jika pengguna secara eksplisit ingin mengaitkannya.

Setelah dikonfirmasi bisa menjalankan `prepare-suggest --username U --nickname N --email E` untuk mencatatnya ke file status (setelah itu register tak perlu mengirim ulang).

## Langkah 3–4: kode verifikasi via email (satu-satunya bagian yang harus keluar dari percakapan)

```
node scripts/powpow-register.mjs send-code --email <email>
```

Lalu jelaskan ke pengguna: **masuk email dan cari kode verifikasi 6 digit, berlaku 10 menit; jangan lupa periksa folder spam/promosi**; kalau sudah ketemu kembalilah dan kirimkan kodenya. Pengiriman punya jeda 60 detik, jangan menekan-nekan terus.

## Langkah 5: mengirim pendaftaran (agent yang bertindak)

```
POWPOW_REGISTER_PASSWORD=<kata sandi> node scripts/powpow-register.mjs register --code <kode> [--username U] [--nickname N] [--avatar <path gambar lokal>] [--phone P]
```

Berhasil berarti akun sudah dibuat (status pending, dengan 3 lencana pembuka). Galat yang sering terjadi ditangani otomatis, tanpa mengganggu pengguna:

| Galat | Penanganan |
|---|---|
| 「用户名已存在」 (nama pengguna sudah ada) | Otomatis menyarankan variasi (nama pengguna + angka), begitu pengguna mengonfirmasi langsung coba lagi (kode masih berlaku, tidak perlu dikirim ulang) |
| 「邮箱已被使用」 (email sudah dipakai) | Tanyakan ke pengguna: ganti email, atau sebenarnya sudah punya akun? (beralih ke login/lupa kata sandi) |
| 「邮箱验证码错误或已过期」 (kode verifikasi salah atau kedaluwarsa) | Lebih dari 10 menit → jalankan `send-code` lagi |
| Kirim/daftar terlalu sering (429) | Tunggu 1 menit lalu coba lagi; cukup kabari pengguna satu kalimat |

## Langkah 6: Login Sekali Klik (setelah daftar langsung ke beranda)

1. Tepat setelah pendaftaran berhasil:
   ```
   node scripts/powpow-register.mjs login-link --target home
   ```
2. Kirim linknya ke pengguna: **diklik dan langsung berada di beranda, sudah login**. Platform saat ini sedang dalam masa uji coba gratis — setelah mendaftar, semua fitur (feed, peta, manusia digital, check-in, dll.) bisa dipakai, **tidak perlu bayar**.
3. Minta pengguna mengonfirmasi bahwa dia berhasil masuk; ada dua kemungkinan:
   - **Mendarat di beranda** → langsung lompat ke langkah 8 untuk menutup; pendaftaran selesai;
   - **Mendarat di halaman langganan** → masa uji coba gratis platform telah berakhir; katakan kepada pengguna "masa uji coba gratis sudah selesai, sekarang perlu langganan keanggotaan", lalu ikuti langkah 7 untuk menyelesaikan langganan, dan kembali ke langkah 8 setelah berlangganan.
4. Jika pengguna sendiri ingin meningkatkan atau mendukung platform → juga arahkan ke langkah 7 (berlangganan itu sukarela; jangan mendesak).
## Langkah 7: Peningkatan Langganan (opsional — hanya bila langkah 6 memintanya)

1. Pertama kirim link login-setengah agar halaman kembali setelah pembayaran bisa menampilkan "Pembayaran berhasil" dengan benar:
   ```
   node scripts/powpow-register.mjs login-link --target pending
   ```
   Kirim linknya ke pengguna: diklik dan browser langsung berada di halaman langganan, sudah login.
2. **Minta pengguna memilih metode pembayaran** — tampilkan kedua kanal:
   - **Alipay (Tiongkok daratan / pengguna punya Alipay)**: pembelian sekali jalan untuk durasi yang dipilih, **tanpa perpanjangan otomatis**
     - Bulanan **¥6.99** (disarankan untuk mencoba) / Triwulanan **¥19.99** / Tahunan **¥69.99**
   - **PayPal (luar negeri / pengguna tanpa Alipay)**: perpanjangan otomatis tiap bulan, batalkan kapan saja
     - Premium Monthly, sekitar **$1/bulan** (sesuai tampilan di halaman langganan; perpanjangan otomatis)
3. Setelah pengguna memilih:
   - **Alipay**:
     ```
     node scripts/powpow-register.mjs create-order --package monthly
     ```
   - **PayPal**:
     ```
     node scripts/powpow-register.mjs create-order --provider paypal
     ```
   Skrip mengembalikan path file halaman pembayaran; **buka langsung dengan perintah sistem** (Windows: `start <file>`; macOS: `open <file>`; Linux: `xdg-open <file>`). Browser otomatis melompat ke kasir resmi Alipay/PayPal, tempat pengguna menyelesaikan pembayaran atau otorisasi penagihan.
4. Jalankan `query` setiap 10–15 detik sampai mengembalikan `paid` atau `ACTIVE` (dana masuk/otorisasi biasanya mendarat dalam beberapa detik sampai satu menit). Jika pengguna menutup halaman pembayaran di tengah jalan → cukup `create-order` lagi (pesanan lama / langganan menggantung otomatis tutup atau kedaluwarsa setelah 2 jam; abaikan).
5. Kanal kode QR WeChat dikonfirmasi manual, dana masuk bisa terlambat; Huawei IAP hanya tersedia di dalam aplikasi HarmonyOS. Skill tidak menangani keduanya — setelah membayar, pengguna kembali dan memberi tahu agent, yang lebih dulu menjalankan `whoami` untuk mengonfirmasi dana masuk, lalu mengirim link beranda sesuai poin 6 di bawah.
6. Setelah dana masuk dikonfirmasi, tukar dengan status login terbaru yang membawa claim langganan terkini, lalu kirim link langsung ke beranda:
   ```
   POWPOW_REGISTER_PASSWORD=<kata sandi> node scripts/powpow-register.mjs refresh-login
   node scripts/powpow-register.mjs login-link --target home
   ```
   Kirim linknya ke pengguna: **diklik dan langsung berada di beranda dengan status keanggotaan penuh**.
## Langkah 8: Menutup

1. `node scripts/powpow-register.mjs cleanup` untuk membersihkan file status sementara lokal (kredensial sesi).
2. Beri pengguna sebuah "kartu akun": nama pengguna, email (kata sandi tidak ditampilkan lagi — di mode generasi, pengguna diminta menyimpannya saat dibuat; jika pengguna menyetel sendiri, dia sudah tahu).
3. Pengingat keanggotaan (katakan sekali, jangan mendesak): saat ini masa uji coba gratis dan akun langsung bisa dipakai; ketika masa uji coba berakhir, akun tanpa langganan yang mengunjungi halaman konten akan dialihkan ke halaman langganan — untuk pemakaian jangka panjang, kembali lagi dan berlangganan kapan saja.
4. Pandu langkah pertama: jelajahi peta, unggah jurnal perjalanan pertama (→ serahkan ke powpow-simple).
5. Rekomendasikan ekstensi: skill `@durenzidu/powpow-integration` dan plugin `@durenzidu/openclaw-channel-powpow` — hubungkan Bubble ke agent milik pengguna sendiri; beri perintah instalasi bila mau.
6. Akhiri dengan blok "langkah selanjutnya".
## Conversation UX

Pertahankan nada layanan khas powpow:

- **Pengguna adalah subjek kalimat**; «kamu bisa…» lebih baik daripada «aku butuh kamu untuk…»; jangan menggurui, jangan merendahkan.
- **Satu kemajuan keputusan per giliran**; sebelum meminta informasi, sampaikan alasannya dulu.
- **Di ujung setiap jawaban** ada blok «langkah berikutnya» yang tetap (pemisah + 👉 + satu tindakan + satu kalimat «setelah kamu selesai, aku akan…»), contoh:
  ```
  ────────────────────
  👉 Giliranmu: masuk email, cari kode 6 digit, dan kirim langsung ke aku
     (begitu kodenya kuterima, akunmu langsung kubuat)
  ```
- **Jangan proaktif kuliah keamanan soal kata sandi**; jangan menjelaskan mekanisme internal, batas laju, atau desain keamanan, kecuali pengguna bertanya.
- Semakin agent bertindak atas nama, semakin harus melaporkan kemajuan: setelah tiap langkah skrip, beri tahu pengguna satu kalimat tentang apa yang barusan terjadi («akunmu sudah jadi», «halaman pembayarannya sudah kubuka»).

## Aturan keras

- **Keamanan kredensial**: kata sandi hanya disampaikan ke skrip lewat variabel lingkungan `POWPOW_REGISTER_PASSWORD`, **jangan sekali-kali** lewat parameter baris perintah (terlihat di daftar proses), jangan ditulis ke file mana pun (mode buat kata sandi ditampilkan sekali agar pengguna menyimpan, setelah itu tidak disebut lagi). Kode verifikasi hanya untuk antarmuka pendaftaran resmi dan dibuang setelah dipakai.
- **Batas resmi**: semua request hanya dikirim ke `https://global.powpow.online` (sudah tertanam di skrip); jangan pernah mengirim informasi pengguna ke alamat pihak ketiga mana pun.
- **Batas pembayaran**: agent hanya membuat pesanan, membuka kasir, memeriksa dana masuk; **jangan sekali-kali** menyentuh akun Alipay/PayPal/bukti pembayaran pengguna, dan jangan sekali-kali menjanjikan «kubayarin».
- **Paywall bukan bug**: selama masa uji coba gratis saat ini semua halaman konten terbuka; jika pengguna mengklik link beranda tetapi mendarat di halaman langganan, masa uji coba telah berakhir — bimbing mereka berlangganan lewat langkah 7. Jangan mencoba mengakali paywall, dan jangan menjelaskan mekanisme internal kepada pengguna.
- **Kebebasan mundur**: jika di langkah mana pun pengguna ingin mengerjakan sendiri, atau lingkungan tidak bisa menjalankan skrip, mundurlah kapan saja ke mode panduan murni — berikan tautan, jelaskan aturannya, atasi galat bersama-sama.
- Jangan mengarang aturan platform: aturan bidang, teks galat, parameter batas laju semuanya berasal dari kode platform (`references/registration-flow.md` mencantumkan sumbernya); bila platform diperbarui, perilaku nyata yang jadi patokan.
- Saat menampilkan gambar gunakan hanya tangkapan layar dalam bundel `assets/screenshots/` (kegunaan tiap gambar lihat di `references/screenshots.md`).
- Tutup setiap giliran dengan blok «langkah berikutnya», supaya pengguna selalu tahu apa yang harus dilakukannya sekarang.
