# Agent-assisted na daloy at script contract — powpow-register

Mga detalye ng pagpapatupad ng bawat hakbang sa SKILL.md. Lahat ng command ay `node scripts/powpow-register.mjs <subcommand> [mga argumento]`; ang script ay **zero dependency**, nangangailangan ng **Node >= 18**, at lahat ng request ay ipinapadala lang sa `https://global.powpow.online`.

## Disenyo ng seguridad (bakit ganito ang disenyo)

| Disenyo | Dahilan |
|---|---|
| Ang password ay ipinapasa lang sa pamamagitan ng environment variable `POWPOW_REGISTER_PASSWORD` | Ang command line arguments ng process ay nakikita ng iba pang process sa parehong makina (argv leak surface); ang environment variable ay binabasa at ginagamit agad sa loob ng script |
| Ang password ay **huwag kailanman isulat sa state file**, huwag lalabas sa mga log | Maaaring manatili sa disk ang state file; sa generate mode sa usapan, isang beses lang ito ipinapakita para i-save ng gumagamit |
| Ang state file ay nakaimbak sa system temp directory (`os.tmpdir()/powpow-register-state.json`, 0600) | Naglalaman lang ito ng limang field: email / username / nickname / token / outTradeNo, binubura nang isang `cleanup` lang |
| Ang JWT na nakuha ng agent ay pinalilitan sa browser cookie sa pamamagitan ng opisyal na `me?token=` endpoint | Opisyal na bridge na dinisenyo para sa HarmonyOS WebView; ang beripikasyon ay nag-beripika lang ng signature + validity period, hindi nakatali sa device fingerprint, kaya magagamit sa browser ng gumagamit |
| Ang bayad ay gumagawa lang ng create-order / query / pagbukas ng cashier | Ang pagbabayad at payment credentials ay palaging nasa pagitan ng gumagamit at ng opisyal na Alipay cashier, hindi dumadaan sa agent |

## Sanggunian ng mga Command

| Command | Mga pangunahing argumento | Gamit / kailan |
|---|---|---|
| `status` | —— | Tingnan ang progreso ng daloy (binabasa ang state file); patakbuhin ito muna pagkatapos maantala ang usapan |
| `gen-password` | —— | Gumawa ng 24-character na malakas na password (may maliliit/malalaking titik + mga numero), ipapakita sa stdout **nang isang beses lang** |
| `prepare-suggest` | `--username --nickname --email` | Itala ang kumpirmadong impormasyon sa state file (pagkatapos, hindi na kailangang ipasa muli sa register) |
| `send-code` | `--email` | Pagsabihan ang plataporma na magpadala ng 6 na numerong verification code (bisa 10 minuto, 60s cooldown) |
| `register` | `--code` (kinakailangan); `--username --nickname --avatar --phone` (opsyonal, hindi na kailangang ipasa kung nasa state file na) | Gumawa ng pending account; ang password ay sa `POWPOW_REGISTER_PASSWORD` environment variable; sa tagumpay, awtomatikong mase-save ang JWT sa state file |
| `login-link` | `--target pending` o `--target home` | Gumagawa ng one-click login link (dual-link na disenyo, tingnan sa ibaba) |
| `create-order` | `--package monthly\|quarterly\|yearly` (default ng Alipay)<br>`--provider alipay\|paypal` | Gumawa ng payment order; ibinabalik ng Alipay ang payment page file path + outTradeNo; ibinabalik ng PayPal ang authorization page file path + subscriptionId (awtomatikong nakatala sa state file) |
| `query` | —— | Tingnan ang status ng order/subscription. Alipay: `paid / pending / closed / unknown`; PayPal: `ACTIVE / PENDING`; poll kada 10–15s |
| `refresh-login` | ang password ay sa environment variable | Mag-log in muli para sa **bagong JWT** (ang subscription claim ay nagiging ACTIVE mula NONE), kailangang patakbuhin pagkatapos dumating ang bayad |
| `whoami` | —— | Gamitin ang token sa state file para tingnan ang status ng account at subscription (beripikahin na gumana ang activation) |
| `cleanup` | —— | Burahin ang state file (kailangang patakbuhin sa dulo) |

**Pagpasa sa pamamagitan ng environment variable** (ang password ay hindi kailanman dumadaan sa command line):

```bash
# bash / zsh / WSL
POWPOW_REGISTER_PASSWORD='<password>' node scripts/powpow-register.mjs register --code 123456
# PowerShell
$env:POWPOW_REGISTER_PASSWORD = '<password>'; node scripts/powpow-register.mjs register --code 123456
# cmd
set POWPOW_REGISTER_PASSWORD=<password> && node scripts/powpow-register.mjs register --code 123456
```

## Dual-Link na Mekanismo (core na disenyo)

Ang login state ng platform ay HttpOnly cookie, na hindi kayang itanim ng agent para sa browser nang diretso; ang tulay ay ang opisyal na
`/api/auth/me?token=<JWT>&redirect=<in-site na path>` endpoint: i-verify ang lagda → awtomatikong lumikha ng
session → `Set-Cookie: powpow_token` (HttpOnly / SameSite=Lax / 7 araw) → i-validate ang
redirect (dapat magsimula sa single slash, ipinagbabawal ang `//` at backslash, dapat same-origin pagkatapos i-parse) → 307 temporary redirect sa target page.

May dalawang target ng link, **gumawa ng home muna, pagkatapos magdesisyon kung dadaan sa pending batay sa kung saan lilapag ang user**:

- **home link (ipinapadala bilang default, `--target home` → lilapag sa `/`)**: ginagawa at ipinapadala sa user kaagad pagkatapos ng matagumpay na pagpaparehistro.
  Sa libreng panahon ng pagsubok ang user ay direktso sa home page, buong magagamit; **kung ang user ay nag-click ngunit lumapag sa subscription page, tapos na ang libreng panahon ng pagsubok** — lumipat sa daloy ng bayad (tingnan sa ibaba); hindi kailangan ng pagbabago sa script at hindi kailangang magparehistro muli.
- **pending link (ginagamit sa daloy ng bayad, `--target pending` → lilapag sa `/subscription`)**:
  ang browser ng user ay pumapasok sa "half-logged-in" na estado: nakikita at napapagana ang subscription page at payment return page. Pagkatapos dumating ang bayad,
  patakbuhin ang `refresh-login` para palitan ng bagong JWT na may ACTIVE claim, pagkatapos ipadala muli ang home link para sa buong membership state.

## Buong Sequence

### Mabilis na Landas (sa libreng panahon ng pagsubok — ang napakaraming kaso)

```
1.  status                          # environment self-check
2.  (Hakbang 2 na pag-uusap para kumpirmahin ang impormasyon, password alinman; generated mode: gen-password → paiponin agad sa user na itago ito)
3.  prepare-suggest --username U --nickname N --email E
4.  send-code --email E             # → tinitignan ng user ang code sa inbox (ang tanging oras na umaalis sa pag-uusap)
5.  POWPOW_REGISTER_PASSWORD=*** register --code 123456 [--avatar pic.jpg]
6.  login-link --target home        # → ipadala ang link sa user; isang click at nasa home page na sila
7.  (kinukumpirma ng user na nakapasok) → mag-wrap up diretso: cleanup + account card + gabayan ang unang hakbang
```

### Landas ng Bayad (kapag nais ng user ang membership, o tapos na ang libreng panahon ng pagsubok)

```
1–5. Katulad ng mabilis na landas (nasa state na ang token pagkatapos matagumpay na register)
6.  login-link --target pending     # → half-login link, pinapanatiling gumagana ang payment return page
7.  (pumili ang user ng paraan ng bayad)
    # Alipay: create-order --package monthly|quarterly|yearly
    # PayPal: create-order --provider paypal
8.  start <file ng payment page>       # Windows; gumagamit ng open ang macOS, xdg-open ang Linux
    # → kinukumpleto ng user ang bayad/awtorisasyon sa Alipay/PayPal cashier (umaalis sa pag-uusap)
9.  query (tuwing 10–15s) hanggang paid / ACTIVE
10. refresh-login                   # palitan ng bagong JWT na may ACTIVE claim
11. login-link --target home        # → ipadala ang buong membership link sa user
12. whoami                          # kumpirmahin ang subscriptionStatus: ACTIVE (opsyonal)
13. cleanup                         # linisin ang state file
```
## Command → platform API mapping

| Command ng script | Platform endpoint |
|---|---|
| `send-code` | `POST /api/auth/register/send-code` |
| `register` | `POST /api/auth/register` (multipart, direct na pag-upload ng avatar) |
| `login-link` | `GET /api/auth/me?token=…&redirect=…` (ang link mismo, gumagana kapag na-click sa browser) |
| `create-order` | `POST /api/payment/alipay/create-order` (Bearer, Alipay)<br>`GET /api/subscription/plans` + `POST /api/subscription/create` (Bearer, PayPal) |
| `query` | `GET /api/payment/alipay/query?outTradeNo=…` (Bearer, Alipay)<br>`GET /api/subscription/create` (Bearer, PayPal) |
| `refresh-login` | `POST /api/auth/login` (`{step:1, username, password}`) |
| `whoami` | `GET /api/auth/me?token=…` |

Pinagmulan ng mga patakaran: para sa mga field rule at rate limit sa rehistro, tingnan ang `registration-flow.md`; para sa mga package at activation chain, tingnan ang
`payment-and-activation.md` (pareho may nakalistang platform source file).

## Script-level error handling

| Sintomas | Paghawak |
|---|---|
| `Node 版本过低` (masyadong lumang bersyon ng Node) | Bumalik sa pure guidance mode, huwag pilitin |
| Error sa network / timeout | Subukan muli nang isang beses; kung tatagal pa, sabihan ang gumagamit na i-check ang network at magpatuloy (nasaan pa rin ang state file, patakbuhin ang `status` mula simula para ipagpatuloy) |
| Nagbalik ng business error ang register (用户名已存在 at iba pa) | I-handle ayon sa table sa Hakbang 5 ng SKILL.md, **hindi na kailangang ipadala muli ang verification code** (may bisa pa ito sa loob ng 10 minuto) |
| Nagbalik ang register ng `邮箱验证码错误或已过期` (mali o expired na ang email verification code) | Kung nag-expire → muling `send-code` |
| Pagkatapos ng `create-order`, isinara ng gumagamit ang payment page | Muling patakbuhin lang ang `create-order` (awtomatikong magsasara ang lumang order pagkatapos ng 2 oras; ang PayPal PENDING subscription ay mag-e-expire pagkatapos ng 1 oras) |
| `create-order --provider paypal` nagbabalik ng 409 | May hindi pa natatapos na PayPal subscription; maghintay ng 1 oras para mag-expire, o tapusin ang lumang authorization sa browser |
| `query` ay laging pending / PENDING | Maaaring hindi pa nagbayad ang gumagamit; magtanong. Kung talagang nagbayad → sundan ang troubleshooting table ng payment-and-activation.md |
| Nag-click ang user sa home link ngunit lumapag sa subscription page | Tapos na ang libreng panahon ng pagsubok → lumipat sa daloy ng bayad: `login-link --target pending` → pumili ng paraan ng bayad → `create-order` |
| `refresh-login` 403 `pending_payment` | Tapos na ang libreng panahon ng pagsubok at hindi pa dumarating ang bayad; bumalik sa hakbang 9 para magpatuloy ng pag-poll, o kumpirmahin kung natapos ng user ang bayad |
| Nawala ang state file (nabura nang aksidente / lumipat ng makina) | Hindi na magagamit ang `whoami`/`refresh-login`; sabihan ang gumagamit na i-refresh ang subscription page mismo sa browser kung saan nabuksan ang Link 1 para kumpirmahin ang status, o mag-log in muli (web mode) |

## Fallback mode (pure guidance)

Sa alinmang sumusunod na sitwasyon, agad na bumalik sa v1-style na pure guidance at hindi na mag-eksperimento sa script:

- Walang Node >= 18, o ang script ay nabigo nang dalawang beses magkasunod sa parehong uri;
- Malinaw na sinabi ng gumagamit na "ako mismo ang gagawa sa web page";
- Pinaghihigpitan ng patakaran ng kumpanya/device ang pagkakakonekta ng script sa internet.

Pagkatapos bumalik: ibigay ang registration page na https://global.powpow.online/register (sa libreng panahon ng pagsubok, ang web registration ay kasing-bilis; kapag kailangan ng subscription, ibigay din ang subscription page na https://global.powpow.online/subscription ), mag-troubleshoot kasabay ayon sa mga patakaran sa `registration-flow.md`, panatilihing pareho ang tono, at tapusin pa rin ang bawat turn ng "next step" block.
https://global.powpow.online/subscription , gabayan ang pag-troubleshoot ayon sa mga patakaran sa `registration-flow.md`, hindi nagbabago ang tono, at ang bawat round pa rin ay nagtatapos sa "susunod na hakbang" block.
