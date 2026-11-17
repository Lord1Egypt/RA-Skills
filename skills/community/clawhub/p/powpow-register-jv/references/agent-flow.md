# Alur agen-ditindakake lan kontrak skrip — powpow-register

Detail eksekusi saben langkah ing SKILL.md. Kabeh printah yaiku `node scripts/powpow-register.mjs <sub-printah> [paramèter]`,
skrip **tanpa dependensi**, butuh **Node >= 18**, kabeh panjalukan mung menyang `https://global.powpow.online`.

## Desain keamanan (ngapa didesain kaya mangkene)

| Desain | Alesan |
|---|---|
| Tembung sandhi mung dilebokake liwat variabel lingkungan `POWPOW_REGISTER_PASSWORD` | paramèter printah proses katon dening proses liya ing mesin sing padha (lumahing bocore argv), variabel lingkungan dibaca ing skrip banjur langsung dienggo |
| Tembung sandhi **aja tau ditulis ing berkas status**, aja tau katon ing log | berkas status bisa tetep ana ing disk; mode nggawe mung nampilake sepisan supaya panganggo nyimpen |
| Berkas status disimpen ing direktori sementara sistem (`os.tmpdir()/powpow-register-state.json`, 0600) | mung ngemot limang kolom: email / username / nickname / token / outTradeNo, `cleanup` mbusak sepisan klik |
| JWT sing ditampa agen diowahi dadi cookie browser liwat endpoint resmi `me?token=` | jembatan resmi platform sing didesain kanggo Harmony WebView; verifikasi mung mriksa tandha + masa berlaku, ora ndheleng fingerprint piranti, bisa dienggo browser panganggo |
| Bayaran mung nindakake create-order / query / mbukak kasir | tumindak mbayar lan bukti bayaran tansah ana antarane panganggo lan kasir resmi Alipay, agen ora nyekel |

## Referensi printah

| Printah | Paramèter kunci | Fungsi / kapan |
|---|---|---|
| `status` | —— | Ndeleng kemajuan alur (maca berkas status); sawise obrolan mandheg, jalanke iki dhisik |
| `gen-password` | —— | Nggawe tembung sandhi kuwat 24 karakter (campuran huruf gedhe-cilik + angka), ditampilake ing stdout **mung sepisan iki** |
| `prepare-suggest` | `--username --nickname --email` | Nyathet info sing wis dikonfirmasi menyang berkas status (sawise iku register ora perlu dikirim maneh) |
| `send-code` | `--email` | Micu platform ngirim kode verifikasi 6 digit (sah 10 menit, cooldown 60 detik) |
| `register` | `--code` (wajib); `--username --nickname --avatar --phone` (opsional, yen berkas status wis ana, ora perlu dikirim) | Nggawe akun pending; tembung sandhi liwat variabel lingkungan `POWPOW_REGISTER_PASSWORD`; sawise sukses JWT otomatis disimpen ing berkas status |
| `login-link` | `--target pending` utawa `--target home` | Nggawe link mlebu siji klik (desain rong link, delok ngisor) |
| `create-order` | `--package monthly\|quarterly\|yearly` (gawan Alipay)<br>`--provider alipay\|paypal` | Nggawe pesanan bayaran; Alipay mbalekake path berkas kaca bayaran + outTradeNo; PayPal mbalekake path berkas kaca ijin + subscriptionId (otomatis dicathet ing berkas status) |
| `query` | —— | Ndeleng status pesanan/langganan. Alipay: `paid / pending / closed / unknown`; PayPal: `ACTIVE / PENDING`; polling 10–15 detik |
| `refresh-login` | tembung sandhi liwat variabel lingkungan | Mlebu maneh kanggo njupuk **JWT anyar** (klaim langganan owah saka NONE dadi ACTIVE), wajib jalanke sawise bayaran tekan |
| `whoami` | —— | Nganggo token ing berkas status ndeleng status akun lan langganan (verifikasi aktivasi wis efektif) |
| `cleanup` | —— | Mbusak berkas status (wajib jalanke ing penutup) |

**Ngirimake liwat variabel lingkungan** (tembung sandhi ora tau mlebu printah):

```bash
# bash / zsh / WSL
POWPOW_REGISTER_PASSWORD='<tembung sandhi>' node scripts/powpow-register.mjs register --code 123456
# PowerShell
$env:POWPOW_REGISTER_PASSWORD = '<tembung sandhi>'; node scripts/powpow-register.mjs register --code 123456
# cmd
set POWPOW_REGISTER_PASSWORD=<tembung sandhi> && node scripts/powpow-register.mjs register --code 123456
```

## Mekanisme rong link (desain inti)

Kahanan mlebu platform iku cookie HttpOnly, sing ora bisa ditancemake agen langsung menyang browser; jembatan iku titik pungkasan resmi
`/api/auth/me?token=<JWT>&redirect=<path ing sajroning situs>`: verifikasi tanda tangan → gawe otomatis
sesi → `Set-Cookie: powpow_token` (HttpOnly / SameSite=Lax / 7 dina) → validasi
redirect (kudu diwiwani karo slash tunggal, `//` lan slash mburi dilarang, kudu same-origin sawise diurai) → 307 redirect sementara menyang kaca target.

Ana rong target link, **dhisik gawe home, banjur mutusake liwat pending utawa ora adhedhasar ngendi pangguna mandheg**:

- **link home (dikirim kanthi default, `--target home` → mandheg ing `/`)**: digawe lan dikirim menyang pangguna sawise registrasi kasil.
  Ing wektu coba gratis pangguna langsung menyang kaca ngarep, kabeh bisa dipa; **yen dheweke klik nanging mandheg ing kaca langganan — wektu coba gratis wis rampung** — pindhah menyang alur pambayaran (delok ngisor); ora perlu ngowahi skrip lan registrasi maneh.
- **link pending (dipakai ing alur pambayaran, `--target pending` → mandheg ing `/subscription`)**:
  browser pangguna mlebu kahanan "mlebu separo": kaca langganan lan kaca bali sawise pambayaran katon lan bisa dioperasikake. Sawise pambayaran mlebu,
  lakokake `refresh-login` kanggo gentiak JWT anyar karo klaim ACTIVE, banjur kirim link home maneh kanggo status keanggotaan lengkap.

## Urutan lengkap

### Alur cepet (ing wektu coba gratis — mayoritas kahanan)

```
1.  status                          # pemeriksaan kahanan lingkungan
2.  (langkah 2 rembugan konfirmasi informasi, sandi bebas; mode generate: gen-password → kon pangguna simen langsung)
3.  prepare-suggest --username U --nickname N --email E
4.  send-code --email E             # → pangguna ndelok kode ing inbox (sasi-sasi ninggal rembugan)
5.  POWPOW_REGISTER_PASSWORD=*** register --code 123456 [--avatar pic.jpg]
6.  login-link --target home        # → kirim link menyang pangguna; siji klik langsung ing kaca ngarep
7.  (pangguna konfirmasi wis mlebu) → langsung rampung: cleanup + kartu akun + tuduhake langkah awal
```

### Alur pambayaran (nalika pangguna pengin keanggotaan, utawa wektu coba gratis wis rampung)

```
1–5. Padha karo alur cepet (kahanan wis nduweni token sawise registrasi kasil)
6.  login-link --target pending     # → link mlebu separo, njaga kaca bali pambayaran bisa mlaku
7.  (pangguna milih cara pambayaran)
    # Alipay: create-order --package monthly|quarterly|yearly
    # PayPal: create-order --provider paypal
8.  start <file kaca pambayaran>       # Windows; macOS nggunakake open, Linux nggunakake xdg-open
    # → pangguna ngrampungake pambayaran/otorisasi ing kasir Alipay/PayPal (ninggal rembugan)
9.  query (saben 10–15s) nganti paid / ACTIVE
10. refresh-login                   # gentiak JWT anyar karo klaim ACTIVE
11. login-link --target home        # → kirim link keanggotaan lengkap menyang pangguna
12. whoami                          # konfirmasi subscriptionStatus: ACTIVE (opsional)
13. cleanup                         # resikake file kahanan
```
## Pemetaan printah → API platform

| Printah skrip | API platform |
|---|---|
| `send-code` | `POST /api/auth/register/send-code` |
| `register` | `POST /api/auth/register` (multipart, unggah avatar langsung) |
| `login-link` | `GET /api/auth/me?token=…&redirect=…` (tautane dhewe, aktif nalika browser diklik) |
| `create-order` | `POST /api/payment/alipay/create-order` (Bearer, Alipay)<br>`GET /api/subscription/plans` + `POST /api/subscription/create` (Bearer, PayPal) |
| `query` | `GET /api/payment/alipay/query?outTradeNo=…` (Bearer, Alipay)<br>`GET /api/subscription/create` (Bearer, PayPal) |
| `refresh-login` | `POST /api/auth/login` (`{step:1, username, password}`) |
| `whoami` | `GET /api/auth/me?token=…` |

Sumber aturan: aturan kolom lan watesan laju registrasi ndeleng `registration-flow.md`; paket lan rantai aktivasi ndeleng
`payment-and-activation.md` (loro-lorone ndhawuhake berkas kode sumber platform).

## Penanganan kesalahan tingkat skrip

| Fenomena | Penanganan |
|---|---|
| `Node 版本过低` (versi Node kedhapur) | Bali menyang mode pandhuan murni, aja ngoyo nyoba |
| Kesalahan jaringan / timeout | Coba maneh sepisan; isih gagal nyurup panganggo mriksa jaringan banjur nerusake (berkas status isih ana, jalanke `status` saka wiwitan kanggo pulih) |
| register mbalikake kesalahan bisnis (用户名已存在 lan liya-liyane) | Nangani miturut tabel Langkah 5 SKILL.md, **kode verifikasi ora perlu dikirim maneh** (isih sah ing 10 menit) |
| register mbalikake 「邮箱验证码错误或已过期」 (kode verifikasi email salah utawa kedaluwarsa) | Ketemu wektu → kirim maneh `send-code` |
| Sawise `create-order` panganggo nutup kaca bayaran | Langsung jalanke maneh `create-order` (pesanan lawas otomatis ditutup sawise 2 jam; langganan PayPal PENDING kadaluwarsa sawise 1 jam) |
| `create-order --provider paypal` mbalekake 409 | Ana langganan PayPal sing durung rampung; enteni 1 jam nganti kadaluwarsa, utawa rampungake ijin lawas ing browser |
| `query` tansah pending / PENDING | Panganggo mbokmenawa durung mbayar; takona sepisan. Yen pancen wis mbayar → tindakake tabel diagnostik payment-and-activation.md |
| Pangguna klik link home nanging mandheg ing kaca langganan | Wektu coba gratis wis rampung → pindhah menyang alur pambayaran: `login-link --target pending` → pilih cara pambayaran → `create-order` |
| `refresh-login` 403 `pending_payment` | Wektu coba gratis wis rampung lan pambayaran durung mlebu; bali menyang langkah 9 terus ngenteni, utawa konfirmasi apa pangguna wis ngrampungake pambayaran |
| Berkas status ilang (kecele dibusak / ganti mesin) | `whoami`/`refresh-login` ora bisa dienggo; nyurup panganggo ing browser sing tau mbukak tautan 1 langsung nganyari kaca langganan kanggo konfirmasi status, utawa mlebu maneh (mode web) |

## Mode fallback (pandhuan murni)

Kahanan ing ngisor iki, langsung bali menyang mode pandhuan murni gaya v1, aja rep-rep skrip maneh:

- Ora ana Node >= 18 utawa skrip gagal ping pindho berturut-turut kanthi jinis sing padha;
- Panganggo jelas ngomong "aku dhewe sing ngoperasikake ing web";
- Kebijakan perusahaan/perangkat mbatesi skrip nyambung internet.

Sawise bali: menehi kaca registrasi https://global.powpow.online/register (ing wektu coba gratis, registrasi web uga padha cepet; nalika langganan dibutuhake, menehi kaca langganan uga https://global.powpow.online/subscription ), tangani bebarengan miturut aturan ing `registration-flow.md`, njaga swara padha, lan tansah rampungake saben giliran karo blok "langkah sabanjure".
https://global.powpow.online/subscription , ngetutake aturan `registration-flow.md` mèlu ngatasi masalah, swara
ora owah, saben giliran isih ditutup karo bagean "langkah sabanjure".
