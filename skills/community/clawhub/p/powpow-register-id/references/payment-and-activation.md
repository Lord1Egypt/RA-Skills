# Aktivasi langganan dan pembayaran — powpow-register

## Kesimpulan (jawaban dulu)
> **Masa uji coba gratis (mulai 2026-10-18; perilaku aktual platform yang berlaku)**: selama periode ini akun yang sudah terdaftar bisa langsung memakai semua fitur, dan **berlangganan adalah peningkatan opsional, bukan keharusan** — ikuti alur di file ini hanya bila pengguna sendiri ingin keanggotaan. Ketika masa uji coba berakhir, akun tanpa langganan yang mengunjungi halaman konten akan dialihkan ke halaman langganan; cukup selesaikan langganannya sesuai file ini.


**Kanal Alipay dan PayPal sekarang bisa dikerjakan agent — termasuk pembuatan pesanan dan pelacakan dana masuk.**
Alipay beli putus sekali tanpa perpanjangan otomatis, untuk pengguna daratan Tiongkok dan pengguna yang punya Alipay;
PayPal perpanjangan otomatis bulanan dan bisa dibatalkan kapan saja, untuk pengguna luar negeri dan tanpa Alipay.
Pindai QR WeChat (konfirmasi manual) dan Huawei IAP tetap tersedia, tapi tidak dikerjakan skill.

Batas tanggung jawab pada tahap pembayaran: agent boleh **membuat pesanan, membuka kasir, memeriksa dana
masuk**; **tidak pernah** menyentuh akun Alipay/PayPal/bukti pembayaran pengguna, tidak pernah menjanjikan «membayarkan».
Aksi membayar selalu diselesaikan oleh pengguna sendiri di kasir resmi.

## Kanal Alipay (vibepay, yang direkomendasikan)

Sistem beli putus sekali: bayar sekali membuka masa berlaku yang bersangkutan, **tanpa perpanjangan otomatis**.
Paket ditulis tetap di `src/lib/alipay-vibepay.ts` (`ALIPAY_PACKAGES`):

| key | planId | Nama | Harga | Masa berlaku |
|---|---|---|---|---|
| `monthly` | alipay-monthly | Keanggotaan bulanan | ¥6.99 | 30 hari |
| `quarterly` | alipay-quarterly | Keanggotaan triwulan | ¥19.99 | 90 hari |
| `yearly` | alipay-yearly | Keanggotaan tahunan | ¥69.99 | 365 hari |

### Kontrak antarmuka (sudah dibungkus skrip skill, agent tidak merangkai request secara langsung)

| Antarmuka | Metode | Keterangan |
|---|---|---|
| `/api/payment/alipay/create-order` | POST | Butuh `Authorization: Bearer <JWT>` (pengguna pending pun cukup). body `{package}` → mengembalikan `{paymentHtml, outTradeNo, amount, planName}`; `paymentHtml` adalah halaman formulir yang mengirim otomatis ke gateway Alipay |
| `/api/payment/alipay/query` | GET `?outTradeNo=` | Sama-sama autentikasi Bearer. Mengembalikan `paid` / `pending` / `closed` / `unknown` |
| `/api/payment/alipay/notify` | POST (callback server Alipay) | Verifikasi tanda tangan lima unsur (tanda tangan, app_id, jumlah konsisten, TRADE_SUCCESS/TRADE_FINISHED, keunikan merchant) → pembaruan pesanan **idempoten** + buat langganan + aktifkan akun. Skill tidak pernah menyentuh antarmuka ini |
| `/payment/alipay/return` | Halaman lompat-balik browser | Jalur publik, setelah membayar menampilkan konfirmasi «pembayaran berhasil», melakukan polling di halaman terhadap status backend yang sebenarnya |

- Pesanan belum dibayar **otomatis tertutup 2 jam**; bila pengguna menyerah di tengah jalan → langsung
  `create-order` ulang, pesanan lama tak perlu diperhatikan.
- Skrip menulis `paymentHtml` ke file HTML sementara, agent cukup membukanya dengan perintah sistem untuk masuk
  ke kasir Alipay (pindai kode atau login di dalam Alipay untuk membayar).

### Rantai aktivasi (otomatis, tanpa perlu manual)

Verifikasi tanda tangan notify lolos → `paymentOrders` ditandai sudah dibayar → `user_subscriptions`
dibuat/diperpanjang (`planId`, `currentPeriodEnd` dihitung per durationDays, perpanjangan ditambahkan pada
tanggal kedaluwarsa semula) → `users.accountStatus: active` + `subscriptionStatus: ACTIVE` → halaman
lompat-balik mem-polling sampai paid dan menampilkan sukses.

### Setelah membayar wajib mengganti status login baru (penting)

JWT membawa klaim langganan (akun pending adalah `NONE`). **Dana masuk dari pembayaran hanya memperbarui
database, tidak mengubah JWT yang sudah terbit** — klaim token lama tetap NONE, memakainya langsung untuk
menghasilkan tautan login akan tampak seperti «bukan anggota».
Karena itu setelah `paid` / PayPal `ACTIVE` terkonfirmasi skill lebih dulu menjalankan `refresh-login` (login ulang menukar JWT
baru, klaim berubah ACTIVE), baru menghasilkan tautan 2. Ini perilaku yang memang didesain, bukan perbaikan
celah.

## Kanal Langganan PayPal (dikerjakan skill; web, non-HarmonyOS)

Hanya ada satu paket, Premium Monthly (sekitar $1/bulan, sesuai yang dikembalikan `/api/subscription/plans`); **perpanjangan otomatis bulanan**
dan pengguna bisa membatalkannya kapan saja di akun PayPal-nya.

### Kontrak API (sudah dibungkus skrip skill; agent tidak pernah merakit request sendiri)

| Endpoint | Metode | Catatan |
|---|---|---|
| `/api/subscription/plans` | GET | Butuh Bearer; mengembalikan daftar paket yang tersedia (saat ini hanya 1) |
| `/api/subscription/create` | POST | body `{planId}` → mengembalikan `{subscriptionId, approveUrl, status}`; `status` biasanya `APPROVAL_PENDING` |
| `/api/subscription/create` | GET | Butuh Bearer; mengembalikan `{activeSubscription, allSubscriptions}`; agent mem-poll `activeSubscription.subscription.status === 'ACTIVE'` |
| `/api/subscription/verify` | POST | Dipanggil otomatis oleh halaman sukses (membawa cookie); mengaktifkan lewat API PayPal langsung saat webhook belum datang |
| `/subscription/success` | Halaman balik browser | Halaman mendarat setelah otorisasi PayPal; mem-poll verify otomatis, lalu kembali ke beranda / halaman asal |
| `/subscription/cancel` | Halaman browser | Halaman mendarat saat pengguna membatalkan atau gagal; bisa mulai ulang |

### Alur agent

```
create-order --provider paypal   # → mengembalikan approveUrl, ditulis ke file HTML lokal
buka file HTML                   # → browser melompat ke halaman otorisasi PayPal
query (tiap 10–15 dtk)           # → poll sampai ACTIVE
refresh-login                    # → tukar JWT baru (klaim langganan ACTIVE)
login-link --target home         # → hasilkan tautan login resmi
```

- Langganan PENDING yang tidak selesai dalam 1 jam dibersihkan otomatis oleh backend; mulai ulang saja.
- Jika pengguna menjalankan `create-order` lagi, backend memakai ulang langganan `APPROVAL_PENDING` yang masih berlaku, sehingga menghindari 409.
- Sama seperti Alipay: dana masuk hanya memperbarui DB — JWT lama tidak diperbarui otomatis, jadi **wajib** menjalankan `refresh-login` sebelum mengirim tautan beranda.

## Empat kanal halaman langganan

Halaman langganan `src/app/(public)/subscription/page.tsx` ditampilkan sesuai lingkungan berjalan:

| Kanal | Lingkungan | Mekanisme | Cara aktivasi |
|---|---|---|---|
| **Alipay (utama)** | Web | `AlipayPaymentSection` lewat antarmuka vibepay (tabel di atas) | notify diaktifkan otomatis sisi server, hitungan detik |
| Langganan PayPal | Web (non-HarmonyOS) | `/api/subscription/create` → lompat ke otorisasi PayPal; perpanjangan otomatis bulanan bisa dibatalkan kapan saja (`/api/subscription/manage`) | PayPal Webhook (`BILLING.SUBSCRIPTION.*`) otomatis dijadikan active |
| Langganan pindai WeChat | Web (non-HarmonyOS) | Bagian bawah halaman «Langganan pindai WeChat»: pindai kode untuk transfer | **Konfirmasi manual**, dana masuk bisa tertunda; setelah membayar jangan buru-buru menyimpulkan gagal |
| Pembelian dalam aplikasi Huawei | Di dalam App HarmonyOS | Native `NativeBridge.purchaseSubscription()` | `/api/subscription/activate-huawei` memverifikasi pesanan Huawei lalu mengaktifkan |

Rencana dan harga PayPal dibaca dinamis dari `/api/subscription/plans`; teks tetap halaman: Auto-renews.
Cancel anytime.

## Status dan pengalihan

- Alipay selesai dibayar → halaman lompat-balik menampilkan sukses; PayPal sukses → `/subscription/success` →
  akun active → otomatis melompat kembali ke halaman semula yang ditunjuk parameter `next` (bila tidak ada,
  beranda).
- Pengguna yang sudah berlangganan mengunjungi lagi halaman langganan → menampilkan "You're All Set!", 3 detik
  kemudian otomatis kembali ke beranda.
- Pembayaran gagal/dibatalkan (PayPal) → `/subscription/cancel`, bisa dimulai ulang.

## Penelusuran

| Gejala | Penanganan |
|---|---|
| Alipay sudah dibayar tapi `query` masih pending | Keterlambatan notify sangat jarang; tunggu 30 detik lalu periksa sekali lagi. Bila tetap tidak bisa suruh pengguna kembali ke browser melihat status halaman lompat-balik, bila masih tidak bisa hubungi dukungan platform (dongtao@outlook.com), laporkan `outTradeNo` |
| Alipay sudah dibayar, masuk lewat tautan 2 tetap ditahan | `refresh-login` terlewat (klaim JWT lama belum diperbarui) — lebih dulu `refresh-login` baru `login-link` |
| `query` PayPal terus PENDING | Pengguna belum menyelesaikan otorisasi di PayPal; pastikan tautan otorisasi sudah terbuka di browser. Bila setelah otorisasi masih PENDING, webhook mungkin tertunda — suruh pengguna menunggu beberapa detik lagi di halaman sukses atau menyegarkannya |
| `query` PayPal mengembalikan 409 | Sudah ada langganan PENDING yang belum selesai; tunggu 1 jam sampai kedaluwarsa, atau selesaikan otorisasi tautan lama di browser |
| PayPal sudah dibayar tapi tautan 2 tetap ditahan | Sama seperti Alipay: jalankan `refresh-login` lebih dulu, baru `login-link` |
| Setelah bayar tetap 403 (PayPal) | Webhook kadang tertunda, login ulang untuk menyegarkan status |
| WeChat dibayar tapi belum aktif | Konfirmasi manual itu asinkron, bila dalam beberapa jam belum aktif barulah hubungi dukungan platform |
| Halaman langganan menampilkan "No subscription plans available" | `/api/subscription/plans` tidak punya rencana PayPal yang tersedia, masalah konfigurasi sisi platform; pengguna domestik cukup beralih ke Alipay |

## Catatan historis

Di dalam kode ada satu set **lama** pembayaran web Alipay (`src/lib/alipay.ts`, `/api/payment/create-order`,
¥9.90/¥99 beli putus sekali, saat sandbox tanpa kunci didegradasi jadi pembayaran simulasi), yang tidak pernah
dihubungkan ke UI halaman langganan, tak berhubungan dengan vibepay. Skill tidak pernah menyentuhnya;
`alipay-vibepay.ts` adalah kanal yang berlaku sekarang.
