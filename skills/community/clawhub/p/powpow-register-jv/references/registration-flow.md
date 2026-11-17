# Detail alur registrasi — powpow-register

Kanggo diwaca nalika ngatasi masalah. Kabeh aturan asale saka kode sumber platform (validasi konsistensi Next.js ngarep-mburi), wis diwenehi sumber. Nalika platform nganyari, nganggo tumindak nyata online minangka patokan.

## Pintu mlebu

- Kaca registrasi: https://global.powpow.online/register
- Kaca mlebu: https://global.powpow.online/login
- Kaca langganan: https://global.powpow.online/subscription
- Yen mlebu saka tautan mbagi sing nggawa `?next=...`, sawise registrasi + bayaran rampung bakal otomatis bali menyang kaca asal.

## Kolom formulir lan aturan

| Kolom | Wajib | Aturan | Sumber kode |
|---|---|---|---|
| Avatar | Opsional | Gambar ≤5MB, ora ndhukung SVG; server otomatis ngompres (yen >100KB diompres dadi 400×400 / kualitas 90) | `src/app/api/auth/register/route.ts` |
| Jeneng panganggo | Wajib | 2~50 karakter, sawise trim disimpen kanthi **huruf cilik** (Tom lan tom dianggep jeneng panganggo sing padha, pihak registrasi lan pihak mlebu loro-lorone ora sensitif huruf gedhe-cilik) | padha (zod schema) |
| Tembung sandhi | Wajib | 8~100 karakter, kudu ngemot huruf gedhe, huruf cilik, lan angka bebarengan | padha |
| Konfirmasi tembung sandhi | Wajib | Padha karo tembung sandhi (validasi mung ing sisih ngarep) | `src/app/(public)/register/page.tsx` |
| Julukan | Opsional | ≤100 karakter; yen kosong standar njupuk jeneng panganggo | register route |
| Email | **Wajib** | Format email sah, ≤255 karakter; siji email mung bisa ndhaftar siji akun | register route |
| Kode verifikasi email | **Wajib** | 6 digit; **sah 10 menit**; sawise verifikasi sukses langsung batal; ngirim maneh bakal nandhani kode lawas minangka wis digunakake | `src/lib/email-verification.ts` |
| Nomer telpon | Opsional | Nomer telpon daratan diawali `1[3-9]` total 11 digit; siji nomer telpon mung bisa diikat menyang siji akun | register route |

Kaca uga nyediakake telung tombol mlebu pihak katelu: **Google, Watcha, Huawei** (`GoogleSignInButton` /
`WatchaLoginButton` / `HuaweiLoginButton`). Akun pihak katelu ora duwe tembung sandhi lokal, mengko yen mlebu nganggo tembung sandhi bakal
njaluk 「该账号未设置密码，请使用其他方式登录」 (akun iki durung nyetel tembung sandhi, mangga nganggo cara mlebu liya).

## Paramèter watesan laju lan anti-brute-force

| Tumindak | Watesan | Sumber |
|---|---|---|
| Ngirimake registrasi | **3 ping/menit/IP**, ngluwihi wates 429 | `src/lib/rate-limit.ts` `REGISTER_RATE_LIMIT` |
| Ngirim kode verifikasi | IP padha 1 ping/menit **lan** email padha 1 ping/menit, ngluwihi wates 429; tombol ngarep countdown 60 detik | `src/app/api/auth/register/send-code/route.ts` |
| Validasi kode verifikasi | Saben email maksimal nyoba **5 ping** ing 10 menit, tekan wates sanajan kodenya bener ditolak, kudu ngirim kode maneh | `src/lib/email-verification.ts` |
| Ngirim kode 忘记密码 (luput tembung sandhi) | 1 ping/menit/IP | `src/app/api/auth/forgot-password/route.ts` |
| Mlebu | 5 ping/menit/IP; akun padha gagal berturut-turut **5 ping dikunci 30 menit** (423), sajrone wektu iku sisa nyoba terus nyuda lan ditampilake | `src/app/api/auth/login/route.ts`, `rate-limit.ts` |

**Tumindak protèksi privasi**: nalika ngirim kode verifikasi / 忘记密码 (luput tembung sandhi), yen email wis kadhaptar utawa ora ana, API bali teks sukses padha, ora mbeberi yen email wis kadhaptar apa ora.

## Kesetaraan mode agen-ditindakake lan registrasi web

Skrip skill nelpon **set API umum sing padha** (`/api/auth/register`, `send-code`, `login`,
`/api/auth/me`), karo formulir kaca registrasi ngliwati jalur validasi, watesan laju, lan kesalahan sing padha persis — kabeh
aturan ing berkas iki berlaku rata kanggo loro mode. Urutan skrip lan kontrak printah ndeleng `references/agent-flow.md`.

## Alur kahanan sawise registrasi kasil

> **Wektu coba gratis (wiwit 2026-10-18; tumindak platform nyata sing absah)**: akun anyar sing didhaftar bisa **langsung nggunakake kabeh fitur**
> (feed, peta, manungsa digital, check-in, lsp) tanpa pambayaran; akun tanpa langganan ora dikurung maneh saka kaca isi. "Pencekalan pending"
> sing dijelasake ing bagean iki yaiku kahanan lumrah sawise wektu coba rampung — nalika wektu kuwi teka, tumindak online nyata sing absah.

1. Pangguna disimpen karo `accountStatus: 'pending'` lan **3 lencana awal** (rute register).
2. Server uga nancepake rong cookie HttpOnly: JWT (bisa mlebu kaca langsung) lan pendingUserToken (kredensial identitas kanggo alur langganan).
3. Ing kahanan lumrah (wektu coba rampung / ora ana wektu gratis), kaca registrasi ndeteksi `pending_payment` → dialihakake menyang `/subscription`
   (njaga parameter bali `next`); ing mode bantuan agen, `me?token=…&redirect=/subscription` entuk efek sing padha.
   **Ing wektu coba gratis langkah iki ora dipicu** — sawise dhaptar, langsung menyang kaca ngarep lan miwiti dipa.
4. Pambayaran rampung → `accountStatus` dadi `active` (**Alipay ngaktifake kanthi otomatis sisi server liwat notify**;
   PayPal ngaktifake liwat Webhook; kode QR WeChat dikonfirmasi manual; Huawei IAP liwat `activate-huawei`).
   Delok `payment-and-activation.md` kanggo rincian.

Ing kahanan lumrah, pangguna ora aktif (pending) nimbali API inti (feed, peta, obrolan manungsa digital, check-in, lsp) entuk 403;
link posting sing dibagi dadi pengecualian (tetap bisa diakses publik). Ing wektu coba gratis pencekalan iki disendheksa lan kabeh kabukak.
## Tabel diagnostik kesalahan umum

| Fenomena | Sebab | Kepriye |
|---|---|---|
| 「用户名已存在」 (jeneng panganggo wis ana) | Jeneng panganggo wis dienggo (ora ndeleng huruf gedhe-cilik) | Ganti jeneng panganggo liya |
| 「邮箱已被使用」 (email wis dienggo) | Email wis kadhaptar | Ganti email; utawa alih menyang mlebu + 忘记密码 (luput tembung sandhi) kanggo njupuk akun lawas |
| 「邮箱验证码错误或已过期」 (kode verifikasi email salah utawa kedaluwarsa) | Kode salah ketik / ngluwihi 10 menit / nyoba ngluwihi 5 ping ditolak | Klik 「重新发送」 (kirim maneh), nganggo kode verifikasi saka email **paling anyar** |
| Kode verifikasi ora tekan | Watesan laju 60 detik; utawa mlebu folder spam/iklan | Enteni countdown rampung banjur kirim; golèk ing folder spam email |
| 「手机号已被使用」 (nomer telpon wis dienggo) | Nomer telpon wis diikat akun liya | Busak nomer telpon (opsional) utawa ganti nomer |
| 「注册请求过于频繁」/ 429 (panjalukan registrasi kekerehan) | Registrasi 3 ping/menit/IP kena plafon | Enteni sawetara menit banjur coba maneh |
| 409「用户名或邮箱已被注册」 (jeneng panganggo utawa email wis kadhaptar) | Ing wektu ngirim bentrok jeneng karo wong liya (jaring pengaman konkurensi) | Ganti jeneng panganggo utawa email banjur coba maneh |
| 「图片大小不能超过5MB」/「不支持 SVG」 (ukuran gambar ora bisa ngluwihi 5MB / ora ndhukung SVG) | Avatar ora mumpuni | Ganti gambar utawa lalewatan avatar |
| Pangguna klik link mlebu nanging mandheg ing kaca langganan (dudu kaca ngarep) | Wektu coba gratis wis rampung lan paywall platform bali | Tindakake alur pambayaran langganan langkah 7 ing SKILL.md; sawise langganan, lakokake `refresh-login` banjur kirim link kaca ngarep |
| Kasil registrasi nanging mlebu mbalekake 403 "请完成订阅以激活账户" | Akun isih pending, lan platform ora ing wektu coba gratis (kahanan sing dikarepake sadurunge pambayaran) | Ora bakal kelakon ing wektu coba gratis; yen kelakon, wektu coba wis rampung — rampungake langganan dhisik; yen isih 403 sawise mbayar, JWT lawas sing dipakai — ing mode skrip dhisik lakokake `refresh-login` kanggo gentiak kahanan mlebu anyar |
| Mlebu 423「账户已锁定」 (akun dikunci) | Tembung sandhi salah berturut-turut 5 ping | Enteni 30 menit |
| Mlebu 401「还剩 N 次尝试机会」 (isih ana N kesempatan nyoba) | Tembung sandhi salah, cedhak dikunci | Mikir pantes banjur coba, utawa langsung tindak 忘记密码 (luput tembung sandhi) |
| 「该账号未设置密码，请使用其他方式登录」 (akun iki durung nyetel tembung sandhi, mangga nganggo cara mlebu liya) | Akun pihak katelu (Google/Watcha/Huawei) | Nganggo tombol pihak katelu asal kanggo mlebu |
| 「该账号已注销」 (akun iki wis dibatalake) | Akun wis deactivate | Perlu registrasi maneh |

## Sari patik mlebu (sapanunggalane kanggo diagnostik)

Mlebu ndhukung input telung-dadi-siji **jeneng panganggo / email / nomer telpon** (siji wae saka telu bisa dianggep jeneng akun).
忘记密码 (luput tembung sandhi): kaca mlebu → 忘记密码 (luput tembung sandhi) → lebokake email registrasi nampa kode verifikasi 6 digit → ngreset.
