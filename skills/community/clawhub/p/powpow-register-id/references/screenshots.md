# Tangkapan layar antarmuka produk — powpow-register

Dipakai sesuai kebutuhan saat runtime. Ketika pengguna belum punya gambaran tentang Gelembung, atau perlu
«melihat» seperti apa jadinya produk, kirim langsung tangkapan layar yang sesuai.

## Lokasi gambar

- Enam tangkapan layar **sudah dibundel bersama skill**, berada di `assets/screenshots/powpow-0N.jpg`
  (`N` adalah 1–6). Kirim langsung sebagai file gambar lokal — tanpa internet, bisa dipakai di lingkungan mana
  pun (termasuk yang tidak bisa membuka GitHub).
- Fallback hanya jika file dalam bundel hilang tak sengaja: salinan tersimpan
  `https://raw.githubusercontent.com/durenzidu/durenzidu/main/screenshots/powpow-0N.jpg` atau mirror
  `https://cdn.jsdelivr.net/gh/durenzidu/durenzidu@main/screenshots/powpow-0N.jpg`
  (catatan: keduanya di daratan Tiongkok bisa saja tidak terbuka — utamakan file dalam bundel).
- Setiap kali kirim hanya 1–3 gambar yang relevan dengan topik saat ini.

## Daftar

### powpow-01.jpg — halaman detail manusia digital

![halaman detail manusia digital](../assets/screenshots/powpow-01.jpg)

Kartu orang sungguhan/tokoh sejarah yang dijadikan manusia digital: status daring, lokasi keberadaan, profil
tokoh, «mulai percakapan», dsb.
**Dipakai saat**: memperkenalkan «setelah daftar bisa ngobrol dengan manusia digital di peta».

### powpow-02.jpg — halaman editor postingan

![halaman editor postingan](../assets/screenshots/powpow-02.jpg)

Antarmuka penyuntingan untuk menulis postingan/catatan perjalanan, dengan sekelompok tombol mengambang di kanan
bawah.
**Dipakai saat**: pengguna bertanya «setelah daftar bisa apa», «nulis di mana».

### powpow-03.jpg — halaman peta (Gelembung + manusia digital)

![halaman peta](../assets/screenshots/powpow-03.jpg)

Seluruh peta publik: postingan bertempat terkumpul sebagai «Gelembung» di atas peta, manusia digital disematkan
dengan foto profilnya di lokasi nyata.
**Dipakai saat**: **gambar pilihan utama saat membuka perkenalan produk** — «catatan perjalananmu akan menjadi
sebuah gelembung di atas peta».

### powpow-04.jpg — halaman profil pribadi (aset digital)

![halaman profil pribadi](../assets/screenshots/powpow-04.jpg)

Halaman milik pengguna sendiri: teman/mengikuti/pengikut, serta «aset digital» — saldo lencana, Gelembung saya,
manusia digital saya.
**Dipakai saat**: menunjukkan di mana lencana berada saat bilang «daftar dapat gratis 3 lencana»; pengguna
bertanya «aset apa saja yang aku punya».

### powpow-05.jpg — halaman kemajuan cerita

![halaman kemajuan cerita](../assets/screenshots/powpow-05.jpg)

Permainan cerita di dalam platform (contoh «Yongle·1421»): kemajuan bab, mendapat lencana, bermain peran.
**Dipakai saat**: pengguna bertanya «selain postingan bisa main apa», «cara dapat lencana gimana».

### powpow-06.jpg — halaman detail postingan (contoh jadi)

![halaman detail postingan](../assets/screenshots/powpow-06.jpg)

Sebuah catatan perjalanan yang sudah tayang: penulis, tag lokasi, isi, foto, di bagian bawah bisa
suka/komentar/bagikan/simpan.
**Dipakai saat**: **gambar kedua saat pembukaan** — «orang lain membuka gelembungmu di peta, yang dilihat
seperti inilah».

## Kilas cepat per skenario

| Ucapan pengguna / tahap saat ini | Kirim gambar mana |
|---|---|
| Pembukaan, memperkenalkan «apa itu Gelembung» | powpow-03 + powpow-06 |
| «Setelah daftar bisa apa?» | powpow-02 + powpow-01 |
| «Lencana apa / aku punya apa?» | powpow-04 |
| «Selain postingan bisa main apa?» | powpow-05 |
| Menelusuri galat daftar/langganan | Umumnya tak perlu gambar; kirim hanya bila memang perlu menunjukkan letak halaman |

## Catatan pemeliharaan

- Gambar di `assets/screenshots/` adalah salinan utama yang didistribusikan bersama bundel. Saat tangkapan layar
  perlu diperbarui, ganti file bernama sama di bawah `assets/screenshots/` (pertahankan penamaan `powpow-0N.jpg`)
  dan terbitkan versi baru.
- Salinan tersimpan di repositori publik `durenzidu/durenzidu` (direktori `screenshots/`) dipertahankan sebagai
  mirror cadangan, diperbarui selaras dengan file dalam bundel.
- Galeri saat ini **belum memiliki** tangkapan layar halaman pendaftaran dan halaman langganan. Bila kelak
  ditambahkan (mis. `powpow-07.jpg` halaman pendaftaran, `powpow-08.jpg` halaman langganan), letakkan filenya di
  `assets/screenshots/` dan tambahkan satu bagian dengan format yang sama; teks perkenalan di SKILL.md bisa
  sekalian mengacuinya.
