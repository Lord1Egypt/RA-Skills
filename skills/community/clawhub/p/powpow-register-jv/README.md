# powpow-register

Pambantu registrasi PowPow Gelembung (versi OpenClaw): ngeterake panganggo anyar saka "ora ngerti Gelembung iku apa" nganti "akun wis aktif, mlebu sapisan klik, miwiti dolanan" — pratelan produk (kalebu tangkapan layar antarmuka), registrasi ditangani agen (kalebu unggah avatar), pesanan langganan Alipay/PayPal lan ngawasi tekan dhuwit, mlebu sapisan klik tautan dobel, diagnostik kesalahan.

**Wiwit v2.0.0 iki mode bantuan agen, lan wiwit v2.2.0 nyetel dhewe karo wektu coba gratis platform**: skrip inti `scripts/powpow-register.mjs` tanpa dependensi
(Node ≥ 18); pangguna mung ninggal rembugan sepisan: kanggo ndelok kode verifikasi ing inbox. Ing wektu coba gratis saiki, akun sing wis didhaftar bisa langsung nggunakake kabeh fitur — pambayaran langganan iku peningkatan opsional; yen wektu coba rampung lan pangguna mandheg ing kaca langganan, alur pindhah menyang alur pambayaran kanthi otomatis. Tanpa Node, utawa nalika pangguna luwih seneng dewe, otomatis bali menyang mode pandhuan murni.

## Instalasi

```
openclaw skills install @durenzidu/powpow-register
```

## Fitur

1. **Pratelan produk**: pratelan udakara 120 tembung + tangkapan layar antarmuka sing dibundel ing paket (`assets/screenshots/` isi 6 gambar: kaca peta, kaca detail kiriman, lsp., pilih kirim 1–3 gambar miturut skenario; tanpa layanan gambar njaba, bisa offline).
2. **Registrasi ditangani agen**: agen aktif nyaranake jeneng panganggo/julukan, tembung sandhi milih siji (panganggo menehi utawa agen nggawe), ngirim lan ngirimake kode verifikasi, unggah avatar langsung (≤5MB dudu SVG), kesalahan umum ditangani otomatis (wis dienggo/kedaluwarsa/watesan laju).
3. **Mlebu siji klik (rong link)**: sawise registrasi kasil, link mlebu langsung nggawa pangguna menyang kaca ngarep (ing wektu coba gratis, siji klik langsung bisa dipa);
   yen mandheg ing kaca langganan (wektu coba rampung) utawa pangguna pengin nambah, tindakake alur langganan — sawise pambayaran mlebu, kahanan mleku anyar digentiak lan link keanggotaan lengkap nggawa menyang kaca ngarep
   (liwat jembatan resmi `me?token=` platform, sing nancepake cookie HttpOnly kanthi otomatis).
4. **Langganan bayaran**: Alipay (wulan ¥6.99 / kuartal ¥19.99 / taunan ¥69.99, tuku langsung ora langganan otomatis) lan PayPal (Premium Monthly, kira-kira $1/sasi, langganan otomatis, bisa dibatalake kapan wae) loro-lorone ditangani agen nganggo nggawe pesanan + polling tekan dhuwit; pindai kode WeChat / Huawei IAP mung tuduhake dalan.
5. **Diagnostik kesalahan**: kode verifikasi ora tekan, jeneng panganggo/email wis dienggo, 403 durung aktif, akun dikunci lsp. masalah umum, kabeh asale saka kode sumber platform lan diwenehi sumber.

## Struktur berkas

```
powpow-register/
├── SKILL.md                            # Pandhuan utama (syarat trigger, alur 8 langkah, standar swara, aturan keras)
├── README.md
├── .clawhubignore
├── assets/
│   └── screenshots/                    # Tangkapan layar produk dibundel bareng paket (powpow-01~06.jpg)
├── scripts/
│   └── powpow-register.mjs             # Skrip inti (tanpa dependensi Node>=18, 11 sub-printah)
└── references/
    ├── agent-flow.md                   # Kontrak skrip, urutan lengkap, mekanisme tautan dobel, desain keamanan
    ├── registration-flow.md            # Aturan kolom, watesan laju, tabel diagnostik kesalahan (kalebu sumber kode)
    ├── payment-and-activation.md       # Kontrak vibepay Alipay, rantai aktivasi, diagnostik saluran
    └── screenshots.md                  # Pratelan tangkapan layar paket + rujukan cepet skenario
```

## Keamanan

- **Tembung sandhi** mung dilebokake menyang proses skrip liwat variabel lingkungan, aja tau ditulis paramèter printah, ora disimpen ing disk, ora mlebu berkas status; tembung sandhi sing digawe agen mung ditampilake sepisan kanggo panganggo simpen.
- **Kode verifikasi** mung dienggo API registrasi resmi, sawise dienggo langsung dibuang; berkas status (email/jeneng panganggo/token/nomor pesanan) disimpen ing direktori sementara sistem, pungkasan alur `cleanup` mbusak sepisan klik.
- **Bayaran**: agen mung nggawe pesanan, mbukak kasir, ngawasi tekan dhuwit; aja tau nyentuh akun Alipay/PayPal utawa bukti bayaran panganggo, aja tau mbayarke. Bayaran tansah dumadi antarane panganggo lan kasir resmi.
- Kabeh panjalukan mung menyang domain resmi `https://global.powpow.online`; ora ngemot kunci apa wae.

## Lisensi

MIT-0 (lisensi standar ClawHub).

## Tautan

- Situs resmi: https://global.powpow.online
- Registrasi: https://global.powpow.online/register
- Kenal Gelembung (video): https://www.bilibili.com/video/BV1Wu826UEVz/
