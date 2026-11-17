---
name: powpow-register
description: Mbantu pangguna ngrampungake registrasi PowPow (Bubble) lan mlebu siji klik ing sajroning rembugan. Agen ngisi formulir minangka pangguna (kalebu unggah avatar) lan ngirim kode verifikasi email; pangguna mung menehi informasi dhasar lan ndelok kode verifikasi sepisan — tanpa ninggal rembugan. Platform saiki lagi ing wektu coba gratis: akun sing wis didhaftar bisa langsung nggunakake kabeh fitur; pambayaran langganan (Alipay/PayPal) iku peningkatan keanggotaan opsional, sing uga bisa ditangani agen kanthi nggawe pesenan lan nglacak dana mlebu yen perlu. Dipicu nalika pangguna ngomong "dhaptar Bubble", "gawe akun powpow", "piye cara dhaptar Bubble", "mbantu aku gawe akun powpow", "sign up powpow"; uga nangani masalah registrasi (kode verifikasi ora teka, jeneng pangguna/email wis dijupuk) lan masalah aktivasi (nalika mlebu kandha "akun durung diaktifake" / pending_payment, piye cara langganan/mbayar, Bubble gratis utawa mbayar). Mbutuhake Node ≥ 18; yen ora kasedhiya, otomatis bali menyang mode pandhuan murni. Ora kalebu posting/gawe manungsa digital (iku tugas powpow-simple), uga ora kalebu pengembangan kode.
version: 2.2.0
metadata:
  openclaw:
    emoji: "\U0001F4DD"
    homepage: https://global.powpow.online
---

# PowPow Register (pambantu registrasi Gelembung)

Nggawa pangguna anyar saka "aku ora ngerti Bubble kuwi apa" dadi "mlebu siji klik, siap dipa" — kabeh ing sajroning rembugan. Pangguna mung ninggal rembugan sepisan: **kanggo ndelok kode verifikasi ing inbox**. Platform saiki lagi ing wektu coba gratis: sawise dhaptar, kabeh fitur kasedhiya, ora perlu mbayar; pambayaran langganan iku peningkatan keanggotaan opsional (agen uga mbukak kasir lan nglacak dana mlebu).

**Versi 2.2.0** · 2026-10-18 (wiwit v2 iki mode bantuan agen: kontrak skrip lan urutan lengkap ana ing `references/agent-flow.md`; aturan kolom, wates laju, lan diagnosa kesalahan ana ing `references/registration-flow.md`; saluran pambayaran ana ing `references/payment-and-activation.md`; dhaptar cuplikan produk ana ing `references/screenshots.md`. Wiwit v2.1.0 langganan PayPal uga bisa ditangani agen, minangka pilihan bareng karo Alipay. Wiwit v2.2.0 platform mlebu wektu coba gratis: dhaptar banjur mlebu siji klik langsung bisa dipa; pambayaran dadi peningkatan opsional — yen pangguna mbukak link banjur mandheg ing kaca langganan, wektu coba wis rampung, tindakake alur pambayaran saka langkah 7; alurnya nyetel dhewe, ora perlu ngowahi skrip)

## Lingkungan Eksekusi

- Skrip inti `scripts/powpow-register.mjs`: **tanpa dependensi**, butuh **Node >= 18**. Sadurunge miwiti, jalanke sepisan `node scripts/powpow-register.mjs status` kanggo masthekake lingkungan siap.
- Kabeh panjalukan skrip mung menyang domain resmi `https://global.powpow.online`.
- **Ora ana Node / kesalahan skrip**: otomatis bali menyang mode pandhuan murni — menehi pangguna kaca registrasi https://global.powpow.online/register lan nuntun bebarengan miturut `references/registration-flow.md` (ing wektu coba gratis, registrasi web uga padha cepet). Aja terus nggodhog skrip.
- Sawise obrolan mandheg banjur nerusake: kapisan `status` kanggo ndeleng alur wis teka ing ngendi, banjur nglajengake.

## Trigger Conditions

- Niat registrasi: "ndhaftar Gelembung", "ndhaftar akun powpow", "piye carane ndhaftar powpow", "sign up powpow"
- Registrasi macet: "kode verifikasi ora tekan", "jeneng panganggo diarani wis ana", "tembung sandhi tansah ora lulus"
- Masalah sawise registrasi: "nalika mlebu kandha akun durung diaktifake", "403 pending_payment", "piye cara mbayar/langganan ing Bubble", "Bubble gratis utawa mbayar"

**Ora aktif kanggo**: ngirim kiriman/gawe manungsa digital (→ powpow-simple); pangembangan kode web (ndeleng skill pangembangan). Yen panganggo arep registrasi lan arep ngirim kiriman: rampungake skill iki dhisik, sawise aktif serahake menyang powpow-simple.

## Ringkesan Alur

| Langkah | Agen nindakake apa | Panganggo nindakake apa |
|---|---|---|
| 1 Pratelan produk | Jlentrehake + kirim tangkapan layar | Ndeleng |
| 2 Konfirmasi info | Aktif nyaranake jeneng panganggo/julukan, tembung sandhi milih siji, takon email | Konfirmasi, menehi |
| 3 Kirim kode verifikasi | `send-code` | —— |
| 4 Waca kode verifikasi | —— | Menyang email ndeleng kode 6 digit, bali kirimake |
| 5 Ngirimake registrasi | `register` (kalebu unggah avatar langsung), nangani kesalahan otomatis | —— |
| 6 Mlebu siji klik | `login-link(home)` langsung menyang kaca ngarep; yen mandheg ing kaca langganan, mangkat menyang langkah 7 | Klik link lan miwiti dipa |
| 7 Peningkatan langganan (opsional) | Mung nalika pangguna pengin keanggotaan / wektu gratis wis rampung: tangani alur pambayaran lengkap | Pilih cara, mbayar |
| 8 Panutup | `cleanup` + menehi bukti + nuntun pengalaman + nyarani plugin | Miwiti dolanan |

## Langkah 1: Pratelan produk + tangkapan layar (ora bisa diliwati)

Akeh panganggo durung tau ngrungokake Gelembung. Sing kapisan dudu nerangake alur, nanging nggawe dheweke **ndeleng** produk:

1. Pratelanake Gelembung kanthi udakara 120 tembung: poto sing dijupuk kanthi apa anane dadi cathetan lelampahan, dipacak ing peta umum dadi siji "gelembung"; gelembung bakal mudhun popularitas suwe-suwe, yen wong liya menehi seneng bisa urip maneh; ing peta uga ana "manungsa digital" sing bisa diajak ngobrol. Alamat platform https://global.powpow.online , yen arep ndeleng video dhisik: https://www.bilibili.com/video/BV1Wu826UEVz/
2. **Kirim tangkapan layar**. Tangkapan layar wis dikemas bebarengan skill ing `assets/screenshots/powpow-0N.jpg` — kirim langsung minangka berkas gambar lokal, tanpa butuh internet. Pratelan, isi saben gambar lan wektu nggunakake ndeleng `references/screenshots.md`. Kombinasi sing paling asring digunakake ing mbukak: kaca peta (powpow-03) + kaca detail kiriman (powpow-06).

Aturan tangkapan layar (aturan keras):

- Tangkapan layar **wis dikemas bebarengan skill** ing `assets/screenshots/` (`powpow-0N.jpg`) — kirim berkas gambar lokal langsung; bisa digunakake ing lingkungan apa wae, kalebu lingkungan sing GitHub ora bisa dibukak.
- Saben giliran mung kirim 1–3 gambar sing ana gandheng cengenge karo topik saiki, aja kabeh dikirim sepisan.
- Yen berkas ing paket kepara ilang, bali menyang tautan hosting sing kadhaptar ing `references/screenshots.md` (eling: ing daratan Cina bisa uga ora bisa dibukak).

Sawise pratelan, menehake pilihan marang panganggo: **"Yen arep ndhaftar, ing telung menit kita bisa nggawe akun ing obrolan, sampeyan mung perlu ndeleng kode verifikasi email sepisan."**

## Langkah 2: Konfirmasi info registrasi (siji pitakon saben giliran, aja kabeh ditakokake sepisan)

- **Jeneng panganggo** (wajib): saka konteks obrolan/jeneng panganggo sistem **aktif netepake sapisan saran** (2~50 karakter, ora mbédakake huruf gedhe-cilik), yen panganggo nyetujoni dienggo, yen arep ganti ya ganti.
- **Tembung sandhi** (wajib, dhisik takon panganggo milih siji):
  - Panganggo sing menehi → sawise iku dilebokake menyang skrip liwat variabel lingkungan, **aja tau ditulis ing paramèter printah**;
  - Agen sing nggawe → jalanke `node scripts/powpow-register.mjs gen-password`, tembung sandhi sing digawe **gelis kirimake marang panganggo supaya disimpen** (mung katon sepisan iku, sawise iku ora muncul maneh).
- **Email** (wajib): kudu panganggo sing menehi — iki jangkar identitas akun, **aja ngira-ngira nggantekake panganggo**.
- **Julukan** (opsional): saran standar padha karo jeneng panganggo.
- **Avatar** (opsional): yen panganggo menehi path berkas gambar lokal (≤5MB, dudu SVG), skrip bakal ngunggah langsung; yen ora ana, skip (platform nganggo logo standar); yen sampeyan duwe kemampuan nggawe gambar, bisa aktif ngajak nggawekake siji kanggo panganggo.
- **Nomer telpon** (opsional, nomer daratan Cina): standar di-skip, yen panganggo dhewe arep ndhelok banjur takon.

Sawise konfirmasi rampung, bisa jalanke `prepare-suggest --username U --nickname N --email E` kanggo nyathet menyang berkas status (sawise iku register ora perlu dikirim maneh).

## Langkah 3–4: Kode verifikasi email (siji-sijine bagean sing kudu metu saka obrolan)

```
node scripts/powpow-register.mjs send-code --email <email>
```

Banjur jelas marang panganggo: **menyang email golèk kode verifikasi 6 digit, sah 10 menit, elinga mriksa folder spam/email iklan**, yen wis nemu bali kirimake kodené marang aku. Ngirim nduwèni cooldown 60 detik, aja terus-terusan ngeklik.

## Langkah 5: Ngirimake registrasi (agen sing nindakake)

```
POWPOW_REGISTER_PASSWORD=<tembung sandhi> node scripts/powpow-register.mjs register --code <kode verifikasi> [--username U] [--nickname N] [--avatar <path berkas gambar lokal>] [--phone P]
```

Sukses tegese akun wis digawe (status pending, karo 3 lencana awal). Kesalahan umum ditangani otomatis, ora nggangu panganggo:

| Kesalahan | Penanganan |
|---|---|
| 用户名已存在 (jeneng panganggo wis ana) | Otomatis nyaranake varian (jeneng panganggo + angka), sawise panganggo konfirmasi langsung coba maneh (kode verifikasi isih sah, ora perlu dikirim maneh) |
| 邮箱已被使用 (email wis dienggo) | Takon panganggo: ganti email liya, utawa mbokmenawa pancen wis duwe akun (alih menyang mlebu/luput tembung sandhi) |
| 邮箱验证码错误或已过期 (kode verifikasi email salah utawa kedaluwarsa) | Ngluwihi 10 menit → kirim maneh `send-code` |
| 发送/注册过于频繁（429） (ngirim/registrasi kekerehan (429)) | Enteni 1 menit banjur coba maneh, cukup ngomong marang panganggo |

## Langkah 6: Mlebu siji klik (sawise registrasi langsung menyang kaca ngarep)

1. Sawise registrasi kasil:
   ```
   node scripts/powpow-register.mjs login-link --target home
   ```
2. Kirim link menyang pangguna: **klik lan kowe langsung menyang kaca ngarep, wis mlebu**. Platform saiki lagi ing wektu coba gratis — sawise dhaptar, kabeh fitur bisa dipa (feed, peta, manungsa digital, check-in, lsp), **ora perlu mbayar**.
3. Takon pangguna konfirmasi wis mlebu; ana rong kahanan:
   - **Manggat menyang kaca ngarep** → langsung mangkat menyang langkah 8 kanggo ngrampungake; registrasi rampung;
   - **Mandheg ing kaca langganan** → wektu coba gratis platform wis rampung; kandha pangguna "wektu coba gratis wis rampung, saiki butuh langganan keanggotaan", banjur tindakake langkah 7 kanggo ngrampungake langganan, lan sawise langganan bali menyang langkah 8.
4. Yen pangguna dewe pengin nambah utawa ndhukung platform → uga tindakake langkah 7 (langganan sukarela; aja meksa).
## Langkah 7: Peningkatan langganan (opsional — mung nalika langkah 6 njaluk)

1. Dhisik kirim link mlebu separo supaya kaca bali sawise pambayaran bisa nuduhake "Pembayaran kasil" kanthi bener:
   ```
   node scripts/powpow-register.mjs login-link --target pending
   ```
   Kirim link menyang pangguna: klik lan browser langsung menyang kaca langganan, wis mlebu.
2. **Takon pangguna milih cara pambayaran** — tuduhake rong saluran:
   - **Alipay (daratan Cina / pangguna nganggo Alipay)**: tuku sepisan kanggo wektu sing cocog, **ora auto-renewal**
     - Saben wulan **¥6.99** (disaranake kanggo nyoba) / Telung wulan **¥19.99** / Saben taun **¥69.99**
   - **PayPal (maneka negara / tanpa Alipay)**: auto-renewal saben wulan, bisa dibatalake kapan wae
     - Premium Monthly, kira-kira **$1/wulan** (kaya sing katuduhake ing kaca langganan; karo auto-renewal)
3. Sawise pangguna milih siji:
   - **Alipay**:
     ```
     node scripts/powpow-register.mjs create-order --package monthly
     ```
   - **PayPal**:
     ```
     node scripts/powpow-register.mjs create-order --provider paypal
     ```
   Skrip bakal mbalekake path file kaca pambayaran; **bukak langsung nganggo printah sistem** (Windows: `start <file>`; macOS: `open <file>`; Linux: `xdg-open <file>`). Browser bakal otomatis pindhah menyang kasir resmi Alipay/PayPal, panggonan pangguna ngrampungake pambayaran utawa otorisasi tagihan.
4. Lakokake `query` saben 10–15 detik nganti mbalekake `paid` utawa `ACTIVE` (pembayaran/otorisasi biasane mlebu ing sawetara detik nganti sakmenit). Yen pangguna nutup kaca pambayaran ing tengah → mung `create-order` maneh (pesenan lawas / langganan mandheg bakal nutup utawa kadaluwarsa sawise 2 jam; aja digatekake).
5. Saluran kode QR WeChat dikonfirmasi kanthi manual lan dana bisa mlecu; Huawei IAP mung kasedhiya ing sajroning aplikasi HarmonyOS. Skrip ora nangani loro kuwi — sawise mbayar, pangguna bali lan kandha agen, sing dhisik lakokake `whoami` kanggo konfirmasi dana mlebu, banjur kirim link kaca ngarep miturut poin 6 ing ngisor iki.
6. Sawise dana mlebu dikonfirmasi, gentiak kahanan mlebu karo klaim langganan paling anyar, banjur kirim link langsung menyang kaca ngarep:
   ```
   POWPOW_REGISTER_PASSWORD=<sandi> node scripts/powpow-register.mjs refresh-login
   node scripts/powpow-register.mjs login-link --target home
   ```
   Kirim link menyang pangguna: **klik lan kowe langsung menyang kaca ngarep karo status keanggotaan lengkap**.
## Langkah 8: Ngrampungake

1. `node scripts/powpow-register.mjs cleanup` kanggo ngresiki file kahanan sementara lokal (kredensial sesi).
2. Menehi pangguna "kartu akun": jeneng pangguna, email (sandi ora dituduhake maneh — ing mode generate pangguna dikon ndelok nalika digawe; yen pangguna nyetel dewe, dheweke ngerti).
3. Pangeling-eling keanggotaan (kandha sepisan, aja meksa): saiki lagi wektu coba gratis lan akun bisa langsung dipa; nalika wektu coba rampung, akun tanpa langganan nalika mlebu kaca isi bakal dialihakake menyang kaca langganan — kanggo dipa suwe, bali lan langganan kapan wae.
4. Tuduhake langkah awal: delok peta, posting jurnal perjalanan pisanan (→ serahake menyang powpow-simple).
5. Rekomendasi ekstensi: skill `@durenzidu/powpow-integration` lan plugin `@durenzidu/openclaw-channel-powpow` — sambungake menyang agen dhewe pangguna; menehi printah instalasi yen dikarepake.
6. Rampungake karo blok "langkah sabanjure".
## Conversation UX

Nganut swara layanan khas PowPow:

- **Panganggo yaiku subyek ukara**, "sampeyan bisa..." luwih apik tinimbang "aku butuh sampeyan..."; ora ceramah, ora sirep.
- **Saben giliran mung nggayuh siji kaputusan**; sadurunge njaluk info, dhisik wenehake alesan.
- **Pungkasan saben balesan** yaiku bagean tetep "langkah sabanjure" (garis pamisah + 👉 + siji tumindak + siji ukara "sawise rampung aku bakal..."), umpamane:
  ```
  ────────────────────
  👉 Sing sampeyan kudu nindakake saiki: menyang email golèk kode verifikasi 6 digit, langsung kirimake marang aku
     (sawise ditampa, langsung tak gawekake akune)
  ```
- **Ora aktif menehi ceramah keamanan tembung sandhi**; ora nerangake mekanisme internal, watesan laju, utawa desain keamanan, kejuali panganggo takon.
- Nalika agen sing nindakake, luwih kudu laporan kemajuan: sawise saben langkah skrip ngomong siji ukara marang panganggo apa sing wis kedaden ("akun wis digawe", "kaca bayaran wis tak mbukakke kanggo sampeyan").

## Aturan Keras

- **Keamanan kredensial**: tembung sandhi mung diwenehake marang skrip liwat variabel lingkungan `POWPOW_REGISTER_PASSWORD`, **aja tau** ditulis ing paramèter printah (katon ing daftar proses), ora ditulis menyang berkas apa wae (mode nggawe nampilake sepisan supaya panganggo nyimpen, sawise iku ora diucapake maneh). Kode verifikasi mung dienggo API registrasi resmi, sawise dienggo langsung dibuang.
- **Bates resmi**: kabeh panjalukan mung menyang `https://global.powpow.online` (wis dibangun ing skrip), aja tau ngirim info panganggo menyang alamat pihak katelu apa wae.
- **Bates bayaran**: agen mung nggawe pesanan, mbukak kasir, takokake tekan dhuwit; **aja tau** nyentuh akun Alipay/PayPal/bukti bayaran panganggo, uga aja tau janji "mbayarke".
- **Paywall dudu bug**: ing wektu coba gratis saiki kabeh kaca isi kabukak; yen pangguna klik link kaca ngarep nanging mandheg ing kaca langganan — wektu coba wis rampung, tuduhake langganan liwat langkah 7. Aja nyoba ngapusi paywall, lan aja nerangake mekanisme internal menyang pangguna.
- **Bebas bali maneh**: panganggo ing langkah apa wae arep dhewe nindakake, utawa lingkungan ora ndhukung skrip, kapan wae bisa bali menyang mode pandhuan murni — wenehake tautan, nerangake aturan, mèlu ngatasi masalah.
- Aja nggawe-gawe aturan platform: aturan kolom, teks kesalahan, paramèter watesan laju kabeh asale saka kode platform (`references/registration-flow.md` ndhawuhake sumber kode), nganyari platform nganggo tumindak nyata minangka patokan.
- Nampilake gambar mung nganggo tangkapan layar saka `assets/screenshots/` ing paket (gunane saben gambar ndeleng `references/screenshots.md`).
- Saben giliran ditutup karo bagean "langkah sabanjure", supaya panganggo tansah ngerti saiki kudu nindakake apa.
