# Ṣiṣan agent-oluranlọwọ ati adehun iwe — powpow-register

Awọn alaye ṣiṣe ti awọn ipe SKILL.md. Gbogbo awọn aṣẹ jẹ `node scripts/powpow-register.mjs <subcommand> [awọn ariyanjiyan]`, iwe naa **laisi awọn igbẹkẹle**, nilo **Node >= 18**, gbogbo awọn ibeere n lọ si `https://global.powpow.online` nikan.

## Apẹrẹ aabo (ki a fi le ṣe bẹ)

| Apẹrẹ | Idi |
|---|---|
| Ọrọ igbaniwọle n lọ nipasẹ oniyipada ayika `POWPOW_REGISTER_PASSWORD` nikan | Awọn ariyanjiyan aṣẹ aṣẹ han si awọn ilana miiran lori ẹrọ kanna (ipa ṣiṣafihan argv), oniyipada ayika a ka ninu iwe ki o lo lẹṣẹkan |
| Ọrọ igbaniwọle **ko kọ sinu faili ipo rara**, ko han ninu akọọlẹ | Faili ipo le duro lori disk; ipo ipilẹṣẹ ninu ibaraẹnisọrọ fihan lẹẹkan nikan ki olumulo to tọju |
| Faili ipo wa ninu folda igba-die eto (`os.tmpdir()/powpow-register-state.json`, 0600) | O ni awọn aaye marun nikan `email / username / nickname / token / outTradeNo`, `cleanup` nu laifọwọyi |
| JWT ti agent gba n lọ nipasẹ aaye osise `me?token=` ṣe cookie aṣawakiri | Afara osise ti a ṣe apẹrẹ fun Harmony WebView; ayẹwo ibuwọn ṣayẹwo ibuwọn + akoko nikan, ko so mọ ika ẹrọ, aṣawakiri olumulo le lo |
| Isanwo n ṣe create-order / query / ṣiṣi alagbata nikan | Iṣe isanwo ati ẹri isanwo nigbagbogbo wa laarin olumulo ati alagbata Alipay osise, agent ko ṣe afọwọṣe |

## Itọkasi aṣẹ

| Aṣẹ | Awọn ariyanjiyan bọtini | Iṣe / akoko |
|---|---|---|
| `status` | —— | Wo ilọsiwaju ilana (ka faili ipo); lẹhin ti ibaraẹnisọrọ ti ge kọkọ ṣiṣẹ eyi |
| `gen-password` | —— | Ṣe ipilẹṣẹ ọrọ igbaniwọle to lagbara oni-nọmba 24 (pẹlu nla-kekere + nọmba), stdout fihan **lẹẹkan nikan** |
| `prepare-suggest` | `--username --nickname --email` | Kọ alaye ti a ti damiloju sinu faili ipo (lẹhinna register ko nilu tun ranṣẹ) |
| `send-code` | `--email` | Nṣe okunfa pẹpẹ lati fi nọmba oni-nọmba 6 ranṣẹ (wulo fun iṣẹju 10, ihamọ iṣẹju 60) |
| `register` | `--code` (dandan); `--username --nickname --avatar --phone` (iyanjiyan, ti faili ipo ba ni ko nilo tun ranṣẹ) | Ṣẹda akọọlẹ pending; ọrọ igbaniwọle nipasẹ oniyipada ayika `POWPOW_REGISTER_PASSWORD`; lẹhin aṣeyọri JWT fi sinu faili ipo laifọwọyi |
| `login-link` | `--target pending` tabi `--target home` | Ṣe ẹda ọna iwọle ẹyọkan (apẹẹrẹ ọna meji, wo ni isalẹ) |
| `create-order` | `--package monthly\|quarterly\|yearly` (Alipay aiyipada)<br>`--provider alipay\|paypal` | Ṣẹda aṣẹ isanwo; Alipay da ọna faili oju-iwe isanwo + outTradeNo pada; PayPal da ọna faili oju-iwe ifọwọsi + subscriptionId pada (fi sinu faili ipo laifọwọyi) |
| `query` | —— | Ṣe ibeere ipo aṣẹ/ṣiṣe alaisanfarasin. Alipay: `paid / pending / closed / unknown`; PayPal: `ACTIVE / PENDING`; ṣe ibeere ni iṣẹmu 10–15 |
| `refresh-login` | Ọrọ igbaniwọle nipasẹ oniyipada ayika | Tun wọle lati ṣe paṣipaarọ JWT tuntun (ikede ṣiṣe alaisanfarasin lati NONE di ACTIVE), ṣiṣe lẹhin isanwo de |
| `whoami` | —— | Lo token ninu faili ipo lati ṣe ibeere akọọlẹ ati ipo ṣiṣe alaisanfarasin (jẹrisi boya imuyipada ti ṣiṣẹ) |
| `cleanup` | —— | Nu faili ipo kuro (ṣiṣe ni ipari) |

**Gbigbe oniyipada ayika** (ọrọ igbaniwọle ko gun aṣẹ rara):

```bash
# bash / zsh / WSL
POWPOW_REGISTER_PASSWORD='<ọrọigbaniwọle>' node scripts/powpow-register.mjs register --code 123456
# PowerShell
$env:POWPOW_REGISTER_PASSWORD = '<ọrọigbaniwọle>'; node scripts/powpow-register.mjs register --code 123456
# cmd
set POWPOW_REGISTER_PASSWORD=<ọrọigbaniwọle> && node scripts/powpow-register.mjs register --code 123456
```

## Ilana Ọna Meji (apẹẹrẹ ipilẹ)

Ipo iwọle sajoo jẹ kuki HttpOnly, ti ajanṣan ko le gbin fun aṣawakiri taara; ọfa ni ofeefee
`/api/auth/me?token=<JWT>&redirect=<ọna inu sajtii>`: jẹrisi ibuwọlu → ṣẹda ajo
adaṣe → `Set-Cookie: powpow_token` (HttpOnly / SameSite=Lax / ọjọ 7) → jẹrisi
itọkasi (gbọdọ bẹrẹ pẹlu kiakia kan, `//` ati kiakia ẹhin ko gba, gbọdọ jẹ orisun kan lẹhin atupale) → 307 itọkasi akoko si ojú-iwe ti a fẹ.

Awọn ọna meji wa, **ṣẹda ile kọọkan, lẹhinna pinnu boya yoo fa nipasẹ pending gẹgẹbi ibiti olumulo gbalẹ**:

- **ọna ile (fi ranṣẹ gẹgẹbi aiyipada, `--target home` → gbalẹ lori `/`)**: ṣẹda ki o fi ranṣẹ si olumulo lẹyin iforukọsilẹ to ṣaṣeyọri.
  Ni akoko idanwo ọfẹ olumulo lọ taara si ojú-iwe ile, gbogbo rẹ wa; **ti olumulo ba tẹ ṣugbọn gbalẹ lori ojú-iwe sập, akoko idanwo ọfẹ ti pari** — pada si ọna owo (wo ni isalẹ); ko nilo iyipada iwe ko si iforukọsilẹ titun.
- **ọna pending (lo ni ọna owo, `--target pending` → gbalẹ lori `/subscription`)**:
  aṣawakiri olumulo wọle ipo "idaji-iwọle": ojú-iwe sập ati ojú-iwe ipadabọ owo han ati ṣiṣẹ. Lẹhin owo de,
  ṣiṣẹ `refresh-login` lati paṣiparọ fun JWT titun pẹlu asẹ ACTIVE, lẹhinna fi ọna ile ranṣẹ lẹẹkansi fun ipo ọmọ-ẹyọn kikun.

## Gbogbo Ilana

### Ọna Kia (ni akoko idanwo ọfẹ — ọpọlọpọ awọn ipo)

```
1.  status                          # ayẹwo ara ẹrọ
2.  (iwiregba Igba 2 lati jẹrisi alaye, ọrọ igbaniwọle eyikeyi; ipo ipilẹṣẹ: gen-password → jẹ ki olumulo fipamọ lẹsẹkẹsẹ)
3.  prepare-suggest --username U --nickname N --email E
4.  send-code --email E             # → olumulo wo koodu ni apoti-ìwé rẹ (igba kan ṣoṣo ti o jade kuro ninu iwiregba)
5.  POWPOW_REGISTER_PASSWORD=*** register --code 123456 [--avatar pic.jpg]
6.  login-link --target home        # → fi ọna ranṣẹ si olumulo; ẹyọkan ki o wà lori ojú-iwe ile
7.  (olumulo jẹrisi pe o wọle) → pari taara: cleanup + kaadi akanti + ṣe itọsọna igba akọkọ
```

### Ọna Owo (nigbati olumulo fẹ ọmọ-ẹyọn, tabi akoko idanwo ọfẹ ti pari)

```
1–5. Gẹgẹbi ọna kia (ipo ni tokeni tẹlẹ lẹhin register ṣaṣeyọri)
6.  login-link --target pending     # → ọna idaji-iwọle, jẹ ki ojú-iwe ipadabọ owo ṣiṣẹ
7.  (olumulo yan ọna owo)
    # Alipay: create-order --package monthly|quarterly|yearly
    # PayPal: create-order --provider paypal
8.  start <faili ojú-iwe owo>       # Windows; macOS lo open, Linux lo xdg-open
    # → olumulo pari owo/aṣẹ ni ile-owo Alipay/PayPal (o jade kuro ninu iwiregba)
9.  query (gbogbọn 10–15s) titi paid / ACTIVE
10. refresh-login                   # paṣiparọ fun JWT titun pẹlu asẹ ACTIVE
11. login-link --target home        # → fi ọna ọmọ-ẹyọn kikun ranṣẹ si olumulo
12. whoami                          # jẹrisi subscriptionStatus: ACTIVE (aṣayan)
13. cleanup                         # nu faili ipo
```
## Maapu aṣẹ → API pẹpẹ

| Aṣẹ iwe | Aaye pẹpẹ |
|---|---|
| `send-code` | `POST /api/auth/register/send-code` |
| `register` | `POST /api/auth/register` (multipart, ikojade aworan taara) |
| `login-link` | `GET /api/auth/me?token=…&redirect=…` (ọna asopọ funrarẹ, ni imuṣẹ nigbati a ba tẹ) |
| `create-order` | `POST /api/payment/alipay/create-order` (Bearer, Alipay)<br>`GET /api/subscription/plans` + `POST /api/subscription/create` (Bearer, PayPal) |
| `query` | `GET /api/payment/alipay/query?outTradeNo=…` (Bearer, Alipay)<br>`GET /api/subscription/create` (Bearer, PayPal) |
| `refresh-login` | `POST /api/auth/login` (`{step:1, username, password}`) |
| `whoami` | `GET /api/auth/me?token=…` |

Orisun ofin: awọn aaye iforukosile ati ihamọ wo `registration-flow.md`; awọn ẹgbẹ ati ṣiṣan imuyipada wo
`payment-and-activation.md` (awọn mejeeji ni orisun koodu pẹpẹ).

## Ṣiṣayẹwo aṣiṣe ipe iwe

| Iṣẹlẹ | Ṣetọju |
|---|---|
| `Node ẹ̀dà rẹ̀ kẹ́gàn` (Node version too low) | Pada si ipo itọsọna lasan, maṣe gbiyanju ni agbara |
| Aṣiṣe nẹtiwọọki / akoko tu | Tun gbiyanju lẹẹkan; ti ko ba ṣaṣeyọri jẹ ki olumulo ṣayẹwo nẹtiwọọki ki o tẹsiwaju (faili ipo tun wa, tun ṣiṣẹ `status` lati bọsipọ) |
| register n ṣafihan aṣiṣe iṣowo (oruko olumulo ti wa tẹlẹ, ati bẹbẹ) | Ṣetọju gẹgẹbi tabili Ipe 5 SKILL.md, **maṣe tun ranṣẹ koodu ijẹrisi** (wulo laarin iṣẹju 10) |
| register n ṣafihan "邮箱验证码错误或已过期" | Ti o ba kọja akoko → tun `send-code` |
| Lẹhin `create-order` olumulo ti pa oju-iwe isanwo | Tun ṣiṣẹ `create-order` taara (aṣẹ atijọ laipẹ pa laifọwọyi ni wakati 2; ṣiṣe alaisanfarasin PayPal PENDING yoo di ofo lẹhin wakati 1) |
| `create-order --provider paypal` da 409 pada | Ṣiṣe alaisanfarasin PENDING PayPal ti ko pari wa; duro wakati 1 ki o to di ofo, tabi pari ifọwọsi atijọ ninu aṣawakiri |
| `query` wa pending / PENDING nigbagbogbo | Olumulo le ma sanwo; beere ọrọ kan. Ti o ba sanwo gangan → tẹle tabili ṣiṣayẹwo `payment-and-activation.md` |
| Olumulo tẹ ọna ile ṣugbọn gbalẹ lori ojú-iwe sập | Akoko idanwo ọfẹ ti pari → pada si ọna owo: `login-link --target pending` → yan ọna owo → `create-order` |
| `refresh-login` 403 `pending_payment` | Akoko idanwo ọfẹ ti pari ati owo ko de; pada si igba 9 lati tẹsiwaju ibi-iṣẹ, tabi jẹrisi boya olumulo pari owo |
| Faili ipo sọnù (aṣiṣe nu / pa ẹrọ) | `whoami`/`refresh-login` ko le lo; jẹ ki olumulo ṣe awọn atunto ninu aṣawakiri nibiti o ti ṣii ọna asopọ 1 lati ṣayẹwo ipo, tabi tun wọle (ipo oju-iwe) |

## Ipo ipadabọ (itọsọna lasan)

Eyikeyi ninu awọn ipo wọnyi pada lẹṣẹkan si ipo itọsọna lasan v1, maṣe tun yan iwe:

- Ko si Node >= 18 tabi iwe naa kuna iru aṣiṣe meji ni itẹlera;
- Olumulo sọ ni gbangba "ema ṣe lori oju-iwe funrarẹ";
- Ilana ile/ẹrọ fi iwe de idiwọ nẹtiwọọki.

Lẹhin pada: fi ojú-iwe iforukọsilẹ https://global.powpow.online/register (ni akoko idanwo ọfẹ, iforukọsilẹ wẹẹbu jẹ iyara kan; nigbati sập nilo, fi ojú-iwe sập ranṣẹ pẹlu https://global.powpow.online/subscription ), ṣe itọju pẹlu gẹgẹbi awọn ofin ni `registration-flow.md`, tọju iro kan, ati pari gbogbo iyi pẹlu bulọọki "igba ti o tẹle".
https://global.powpow.online/subscription , tẹle awọn ofin `registration-flow.md` lati ṣe ibaṣepọ ṣiṣayẹwo aṣiṣe,
ohun orin ko yipada, iyipo kọọkan tun pari pẹlu apa "igbesẹ ti nbọ".
