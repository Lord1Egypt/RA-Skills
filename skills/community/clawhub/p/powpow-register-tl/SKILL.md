---
name: powpow-register
description: Tumutulong sa mga user na makumpleto ang pagpaparehistro sa PowPow (Bubble) at pag-login sa isang click sa loob ng buong pag-uusap. Pinupuno ng agent ang form para sa kanila (kasama ang pag-upload ng avatar) at ipinapadala ang verification code sa email; ang user ay nagbibigay lamang ng batayang impormasyon at tinitignan ang verification code nang isang beses — hindi umaalis sa pag-uusap. Sa kasalukuyang libreng panahon ng pagsubok ng platform, ang isang rehistradong account ay maaaring gamitin ang lahat ng feature agad; ang subscription payment (Alipay/PayPal) ay opsyonal na membership upgrade, na maaari ring hawakan ng agent sa paglikha ng order at pagsubaybay ng pagdating kapag kailangan. Nagu-trigger kapag sinabi ng user na "irehistro para sa Bubble", "gumawa ng powpow account", "paano ako magparehistro para sa Bubble", "tulungan mo akong gumawa ng powpow account", "mag-sign up sa powpow"; hinahawakan din ang mga isyu sa pagpaparehistro (hindi natanggap ang verification code, kinuha na ang username/email) at mga isyu sa activation (sabi ng login na "hindi na-activate ang account" / pending_payment, paano mag-subscribe/magbayad, libre ba ang Bubble o bayad). Nangangailangan ng Node ≥ 18; awtomatikong bumabalik sa purong guidance mode kapag hindi available. Hindi saklaw ang pag-post/paggawa ng digital human (trabaho iyon ng powpow-simple), ni ang pag-develop ng code.
version: 2.2.0
metadata:
  openclaw:
    emoji: "\U0001F4DD"
    homepage: https://global.powpow.online
---

# PowPow Register (katulong sa pagrehistro ng Bula)

Dinadala ang bagong user mula sa "hindi ko alam kung ano ang Bubble" hanggang "naka-login sa isang click, handa nang maglaro" — sa loob ng buong pag-uusap. Umualis ang user sa pag-uusap nang isang beses lamang: **para tignan ang verification code sa inbox**. Ang platform ay kasalukuyang nasa libreng panahon ng pagsubok: kapag nakaparehistro, magagamit ang lahat ng feature, hindi kailangang magbayad; ang subscription payment ay opsyonal na membership upgrade (hinahawakan din ng agent ang pagbukas ng cashier at pagsubaybay ng pagdating).

**Bersyon 2.2.0** · 2026-10-18 (mula noong v2 ito ay agent-assisted mode: ang contract ng script at buong sequence ay nasa `references/agent-flow.md`; ang mga patakaran ng field, rate limits at troubleshooting ng error ay nasa `references/registration-flow.md`; ang mga channel ng bayad ay nasa `references/payment-and-activation.md`; ang listahan ng screenshot ng produkto ay nasa `references/screenshots.md`. Mula noong v2.1.0 ang PayPal subscriptions ay maaari ring hawakan ng agent, bilang opsyon kasabay ng Alipay. Mula noong v2.2.0 ang platform ay nasa libreng panahon ng pagsubok: magparehistro at mag-login sa isang click para simulan ang paggamit; ang bayad ay nagiging opsyonal na upgrade — kung ang user ay nag-click sa link at lumapag sa subscription page, tapos na ang panahon ng pagsubok, sundin ang daloy ng bayad ng Hakbang 7; ang daloy ay nag-a-adjust sa sarili nito, hindi kailangan ng pagbabago sa script)

## Kapaligiran ng Pagtakbo

- Pangunahing script `scripts/powpow-register.mjs`: **zero dependency**, nangangailangan ng **Node >= 18**. Bago magsimula, patakbuhin nang isang beses ang `node scripts/powpow-register.mjs status` para kumpirmahing gumagana ang kapaligiran.
- Lahat ng request ng script ay ipinapadala lang sa opisyal na domain `https://global.powpow.online`.
- **Walang Node / mga error sa script**: awtomatikong bumabalik sa purong guidance mode — ibigay sa user ang registration page na https://global.powpow.online/register at gabayan kasabay ayon sa `references/registration-flow.md` (sa libreng panahon ng pagsubok, ang web registration ay kasing-bilis). Huwag lang ipagpatuloy na pukpukin ang script.
- Para ipagpatuloy pagkatapos maantala ang usapan: unahin ang `status` para makita kung saang hakbang na ang daloy, tapos ituloy.

## Trigger Conditions

- Intensyon ng pagrehistro: "magrehistro ng Bula", "magrehistro ng powpow account", "paano magrehistro sa Bula", "sign up powpow"
- Nahihirapan sa rehistro: "hindi dumarating ang verification code", "sinasabing may-ari na ang username", "laging hindi tanggap ang password"
- Mga isyu pagkatapos magparehistro: "sabi ng login na hindi na-activate ang account", "403 pending_payment", "paano ako magbayad/mag-subscribe para sa Bubble", "libre ba ang Bubble o bayad"

**Hindi nagti-trigger**: pag-post/paglikha ng digital na tao (→ powpow-simple); Web-side code development (tingnan ang development skill). Kapag gusto ng gumagamit na magrehistro at mag-post nang sabay: tapusin muna ang skill na ito, at pagkatapos i-activate ay ipasa sa powpow-simple.

## Pangkalahatang-ideya ng Daloy

| Hakbang | Ano ang ginagawa ng agent | Ano ang ginagawa ng gumagamit |
|---|---|---|
| 1 Pagpapakilala ng produkto | Magpaliwanag + magpadala ng screenshots | Tumingin |
| 2 Pagkumpirma ng impormasyon | Aktibong magmungkahi ng username/palayaw, password na piliin ang isa, tanungin ang email | Kumpirmahin, ibigay |
| 3 Pagpapadala ng verification code | `send-code` | —— |
| 4 Pagbabalik ng verification code | —— | Puntahan ang email para sa 6 na numero, balikan at ipasa |
| 5 Pagpasa ng rehistro | `register` (kasama ang direct na pag-upload ng avatar), awtomatikong paghawak ng mga error | —— |
| 6 Pag-login sa isang click | `login-link(home)` diretso sa home page; kung lumapag sa subscription page, pumunta sa Hakbang 7 | I-click ang link at simulan ang paglalaro |
| 7 Membership upgrade (opsyonal) | Kapag nais ng user ang membership / tapos na ang libreng panahon: buong daloy ng bayad ang hinahawakan | Pumili ng paraan, magbayad |
| 8 Pagtatapos | `cleanup` + ibigay ang mga kredensyal + gabayan sa karanasan + magmungkahi ng plugins | Magsimulang maglaro |

## Hakbang 1: Pagpapakilala ng produkto + screenshots (hindi maaaring laktawan)

Karamihan sa mga gumagamit ay hindi pa nakakakita ng Bula. Ang unang gawain ay hindi ang pagpapaliwanag ng daloy, kundi pagpapahintulot sa kanya na **makita** ang produkto:

1. Ipakilala ang Bula sa humigit-kumulang 120 salita: ang mga larawang kinuha mo lang nang pasadya ay nagiging isang tala ng paglalakbay, nakapin sa pampublikong mapa bilang isang "bula"; ang mga bula ay nawawalan ng gana sa paglipas ng panahon, at mabubuhay muli kapag may nag-like; sa mapa ay may mga "digital na tao" na puwedeng makipag-usapan. Ang address ng plataporma ay https://global.powpow.online , at kung gusto munang manood ng video: https://www.bilibili.com/video/BV1Wu826UEVz/
2. **Magpadala ng screenshots**. Ang mga screenshot ay nakapaketeng kasama ng skill sa `assets/screenshots/powpow-0N.jpg` — ipadala nang direkta bilang lokal na image file, hindi na kailangan ng internet. Para sa listahan, nilalaman ng bawat larawan, at kailan gagamitin, tingnan ang `references/screenshots.md`. Pinakakaraniwang kombinasyon sa simula: mapa page (powpow-03) + post detail page (powpow-06).

Mga patakaran sa screenshots (hard na patakaran):

- Ang mga screenshot ay **nakapaketeng kasama ng skill** sa `assets/screenshots/` (`powpow-0N.jpg`) — magpadala lang ng lokal na image file; gumagana sa anumang kapaligiran, kasama ang mga kapaligirang hindi mabuksan ang GitHub.
- Isang beses lang magpadala ng 1–3 larawan na nauugnay sa kasalukuyang paksa, huwag ipagsabay lahat.
- Kapag aksidenteng nawala ang mga file sa pakete, bumalik sa mga hosted link na nakalista sa `references/screenshots.md` (tandaan: posibleng hindi mabuksan sa mainland China).

Matapos magpakilala, ibigay ang pagpipilian sa gumagamit: **"Kung gusto mong magrehistro, mabubuo natin ang account sa loob ng tatlong minuto dito sa usapan; kailanganin mo lang tingnan nang isang beses ang email verification code."**

## Hakbang 2: Kumpirmahin ang impormasyon ng rehistro (isang tanong kada round, huwag tanungin lahat nang sabay)

- **Username** (kinakailangan): mula sa konteksto ng usapan/system username, **aktibong magmungkahi ng isa** (2–50 na karakter, hindi case-sensitive), kung pumayag ang gumagamit ay gamitin iyon, kung gusto niyang palitan ay palitan.
- **Password** (kinakailangan, tanungin muna ang gumagamit na pumili ng isa):
  - Kung ibibigay mismo ng gumagamit → ipasa sa script sa pamamagitan ng environment variable, **huwag kailanman isulat sa command line argument**;
  - Kung gagawa ang agent → patakbuhin ang `node scripts/powpow-register.mjs gen-password`, at **agad na ipasa ang ginawang password sa gumagamit para i-save** (ipapakita lang nang isang beses, hindi na lalabas muli).
- **Email** (kinakailangan): dapat ibigay mismo ng gumagamit — ito ang identity anchor ng account, **huwag hulaan para sa gumagamit**.
- **Palayaw** (opsyonal): imungkahi bilang default na kapareho ng username.
- **Avatar** (opsyonal): kung magbibigay ang gumagamit ng lokal na image path (≤5MB, hindi SVG), ida-direct upload ng script; kung wala, laktawan (gagamit ang plataporma ng default logo); kung may kakayahan ka sa image generation, maaari kang aktibong mag-alok na gumawa ng isa para sa gumagamit.
- **Mobile number** (opsyonal, mainland number): default na laktawan, hingin lang kung gusto mismo ng gumagamit mag-bind.

Matapos makumpirma, puwedeng patakbuhin ang `prepare-suggest --username U --nickname N --email E` para itala sa state file (pagkatapos, hindi na kailangang ipasa muli sa register).

## Hakbang 3–4: Email verification code (tanging bahagi na kailangang lumabas ng usapan)

```
node scripts/powpow-register.mjs send-code --email <email>
```

Pagkatapos, sabihin nang malinaw sa gumagamit: **puntahan ang email para hanapin ang 6 na numerong verification code, may bisa sa loob ng 10 minuto, at tandaang tingnan ang spam/promotions folder**, kapag nakuha na ay bumalik at ipasa ang code. May 60-segundong cooldown ang pagpapadala, huwag pindutin nang paulit-ulit.

## Hakbang 5: Ipasa ang rehistro (ginagawa ng agent)

```
POWPOW_REGISTER_PASSWORD=<password> node scripts/powpow-register.mjs register --code <verification code> [--username U] [--nickname N] [--avatar <lokal na image path>] [--phone P]
```

Kapag matagumpay, nabubuo ang account (pending status, may kasamang 3 initial badge). Awtomatikong hinihawak ang mga karaniwang error nang hindi inaabala ang gumagamit:

| Error | Paghawak |
|---|---|
| 用户名已存在 (may-ari na ang username) | Awtomatikong magmungkahi ng variant (username + numero), pagkatapos kumpirmahin ng gumagamit ay subukan muli nang direkta (may bisa pa ang verification code, hindi na kailangang ipadala muli) |
| 邮箱已被使用 (gamit na ang email) | Tanungin ang gumagamit: palitan ang email, o baka may account na pala siya (lumipat sa log in / password recovery) |
| 邮箱验证码错误或已过期 (mali o expired na ang email verification code) | Kapag lumampas ng 10 minuto → muling `send-code` |
| 发送/注册过于频繁（429） (sobrang dalas ng pagpapadala/pagrehistro (429)) | Maghintay ng 1 minuto bago subukan muli, sabihin lang sa gumagamit |

## Hakbang 6: Pag-login sa Isang Click (diretso sa home page pagkatapos magparehistro)

1. Kaagad pagkatapos ng matagumpay na pagpaparehistro:
   ```
   node scripts/powpow-register.mjs login-link --target home
   ```
2. Ipadala ang link sa user: **i-click ito at diretso kang lilapag sa home page, naka-login na**. Ang platform ay kasalukuyang nasa libreng panahon ng pagsubok — pagkatapos magparehistro, magagamit ang lahat ng feature (feed, mapa, digital human, check-in, atbp.), **hindi kailangang magbayad**.
3. Hilingin sa user na kumpirmahin na nakapasok; may dalawang kaso:
   - **Lumapag sa home page** → tumalon diretso sa Hakbang 8 para mag-wrap up; tapos na ang pagpaparehistro;
   - **Lumapag sa subscription page** → tapos na ang libreng panahon ng pagsubok ng platform; sabihin sa user na "tapos na ang libreng panahon ng pagsubok, kailangan na ngayon ng membership subscription", pagkatapos sundin ang Hakbang 7 para kumpletuhin ang subscription, at bumalik sa Hakbang 8 pagkatapos mag-subscribe.
4. Kung nais ng user na mag-upgrade o suportahan ang platform → pumunta rin sa Hakbang 7 (boluntaryo ang pag-subscribe; huwag pilitin).
## Hakbang 7: Membership Upgrade (opsyonal — kapag hinihingi ng Hakbang 6)

1. Ipadala muna ang half-login link para maipakita ng payment return page nang tama ang "Matagumpay ang bayad":
   ```
   node scripts/powpow-register.mjs login-link --target pending
   ```
   Ipadala ang link sa user: ang pag-click ay direktang inilalapag ang browser sa subscription page, naka-login na.
2. **Piliin ng user ang paraan ng bayad** — ipakita ang dalawang channel:
   - **Alipay (mainland China / mga user na may Alipay)**: one-time purchase ng kaukulang tagal, **walang auto-renewal**
     - Buwanan **¥6.99** (inirerekomenda para subukan) / Quarterly **¥19.99** / Taunan **¥69.99**
   - **PayPal (ibang bansa / mga user na walang Alipay)**: awtomatikong nagre-renew buwan-buwan, pwedeng kanselahin anumang oras
     - Premium Monthly, mga **$1/buwan** ( gaya ng ipinapakita sa subscription page; awtomatikong nagre-renew)
3. Kapag pumili na ang user ng isa:
   - **Alipay**:
     ```
     node scripts/powpow-register.mjs create-order --package monthly
     ```
   - **PayPal**:
     ```
     node scripts/powpow-register.mjs create-order --provider paypal
     ```
   Ang script ay nagbabalik ng path ng file ng payment page; **bukuhin ito diretso gamit ang system command** (Windows: `start <file>`; macOS: `open <file>`; Linux: `xdg-open <file>`). Ang browser ay awtomatikong tumatalon sa opisyal na Alipay/PayPal cashier, kung saan kumukumpleto ang user ng bayad o billing authorization.
4. Patakbuhin ang `query` tuwing 10–15 segundo hanggang magbalik ng `paid` o `ACTIVE` (ang bayad/awtorisasyon ay karaniwang dumarating sa loob ng ilang segundo hanggang isang minuto). Kung isinara ng user ang payment page sa gitna → gumawa lang ng `create-order` muli (ang lumang order / nakabinbing subscription ay awtomatikong nagsasara o nag-e-expire pagkatapos ng 2 oras; balewalain).
5. Ang WeChat QR-code channel ay manu-manong kinukumpirma at maaaring huli ang pagdating ng pondo; ang Huawei IAP ay available lamang sa loob ng HarmonyOS App. Hinahawakan ng skill na ito ang dalawang iyon — pagkatapos magbayad, bumabalik ang user at nagsasabi sa agent, na unang tumatakbo ng `whoami` para kumpirmahin ang pagdating, pagkatapos ipinapadala ang home page link ayon sa puntong 6 sa ibaba.
6. Pagkatapos kumpirmahin ang pagdating, palitan ng bagong login state na may pinakabagong subscription claim, pagkatapos ipadala ang link diretso sa home page:
   ```
   POWPOW_REGISTER_PASSWORD=<password> node scripts/powpow-register.mjs refresh-login
   node scripts/powpow-register.mjs login-link --target home
   ```
   Ipadala ang link sa user: **i-click ito at diretso kang lilapag sa home page na may buong membership status**.
## Hakbang 8: Pag-Wrap Up

1. `node scripts/powpow-register.mjs cleanup` para linisin ang mga lokal na temporary state file (mga kredensyal ng session).
2. Bigyan ang user ng "account card": username, email (hindi na ipinapakita muli ang password — sa generated mode hinilingan ang user na itago ito nang mag-generate; kung inilagay ng user mismo, alam nila).
3. Paalala sa membership (sabihin nang isang beses, huwag pilitin): kasalukuyang libreng panahon ng pagsubok ito at magagamit agad ang account; kapag tapos na ang panahon ng pagsubok, ang mga account na walang subscription na bumibisita sa content page ay ire-redirect sa subscription page — para sa pangmatagalang paggamit, bumalik at hanapin ang agent para mag-subscribe anumang oras.
4. Gabayan ang mga unang hakbang: bisitahin ang mapa, i-post ang unang travel journal (→ i-turnover sa powpow-simple).
5. I-rekomenda ang mga extension: ang `@durenzidu/powpow-integration` skill at ang `@durenzidu/openclaw-channel-powpow` plugin — ikonekta ang Bubble sa sariling agent ng user; ibigay ang install command kung gusto.
6. Tapusin ng "next step" block.
## Conversation UX

Manatili sa pamilyar na service tone ng PowPow:

- **Ang gumagamit ang paksa ng pangungusap**, mas mainam ang "Puwede kang..." kaysa sa "Kailangan mong..."; huwag mangaral, huwag mamatas.
- **Isang desisyon lang ang isulong kada round**; magbigay muna ng dahilan bago humingi ng impormasyon.
- **Ang dulo ng bawat sagot** ay isang nakatakdang "susunod na hakbang" block (separator + 👉 + iisang aksyon + isang pangungusap na "kapag natapos mo, gagawin ko ang..."), halimbawa:
  ```
  ────────────────────
  👉 Ang kailangan mong gawin ngayon: puntahan ang email, hanapin ang 6 na numerong verification code, ipasa nang direkta sa akin
     (sa oras na matanggap ko, agad kong bubuuin ang account)
  ```
- **Huwag kusang mag-lecture tungkol sa seguridad ng password**; huwag ipaliwanag ang panloob na mekanismo, rate limit, o security design maliban kung itanong ng gumagamit.
- Lalo nang iulat ang progreso habang ginagawa ng agent ang lahat: pagkatapos ng bawat script step, sabihin sa gumagamit sa isang pangungusap kung ano ang nangyari ("nabuo na ang account", "nabuksan na para sa iyo ang payment page").

## Mga Hard na Patakaran

- **Seguridad ng kredensyal**: ang password ay ipinapasa sa script lang sa pamamagitan ng environment variable `POWPOW_REGISTER_PASSWORD`, **huwag kailanman** isulat sa command line argument (nakikita ito sa process list), huwag isulat sa anumang file (sa generate mode, ipinapakita nang isang beses para i-save ng gumagamit, pagkatapos ay hindi na uulitin). Ang verification code ay para lang sa opisyal na registration endpoint, itinatapon pagkatapos gamitin.
- **Opisyal na hangganan**: lahat ng request ay ipinapadala lang sa `https://global.powpow.online` (naka-embed na ito sa script), huwag kailanman ipapadala ang impormasyon ng gumagamit sa kahit anong third-party na address.
- **Hangganan ng bayad**: ang agent ay gumagawa lang ng order, nagbubukas ng cashier, nagtatanong ng pagdating ng bayad; **huwag kailanman** hawakan ang Alipay/PayPal account/payment credentials ng gumagamit, at huwag kailanman mangako ng "pagbabayad para sa kanya".
- **Ang paywall ay hindi bug**: sa kasalukuyang libreng panahon ng pagsubok bukas ang lahat ng content page; kung ang user ay nag-click sa home page link ngunit lumapag sa subscription page, tapos na ang panahon ng pagsubok — gabayan silang mag-subscribe sa Hakbang 7. Huwag subukang i-bypass ang paywall, at huwag ipaliwanag ang internal mechanism sa user.
- **Kalayaang bumalik sa manual**: kung sa anumang hakbang gustong gawin mismo ng gumagamit, o hindi sinusuportahan ng kapaligiran ang script, anumang oras ay maaaring bumalik sa pure guidance mode — bigyan ng link, ipaliwanag ang mga patakaran, samahan sa pag-troubleshoot.
- Huwag gumawa ng mga patakaran ng plataporma: lahat ng field rule, error text, at rate limit parameter ay nagmumula sa platform code (may mga source citation sa `references/registration-flow.md`); kapag nag-update ang plataporma, ang aktwal na gawi online ang masusunod.
- Para sa mga ipinapakitang larawan, gamitin lang ang mga screenshot sa `assets/screenshots/` sa pakete (tingnan ang `references/screenshots.md` para sa gamit ng bawat larawan).
- Wakasan ang bawat round gamit ang "susunod na hakbang" block, para laging alam ng gumagamit ang kanyang susunod na gagawin.
