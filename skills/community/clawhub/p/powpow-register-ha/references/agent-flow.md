# Tsarin agent-yana-taimakawa da kwangilar script — powpow-register

Cikakkun bayanai na aiwatar da matakai a SKILL.md. Duk umarni suke `node scripts/powpow-register.mjs <umarnin-ciki> [mahawari]`, script ɗin **ba shi da dogaro**, yana buƙatar **Node >= 18**, duk buƙatun suna tafiya ga `https://global.powpow.online` kawai.

## Zanen tsaro (me yasa aka zane haka)

| Zane | Dalili |
|---|---|
| Kalmar sirri tana wucewa ta canjin muhalli `POWPOW_REGISTER_PASSWORD` kawai | Mahawarin umarnin aiwatarwa na iya ganuwa ta wasu aiwatarwa na wannan na'ura (fafutukar argv), canjin muhalli a cikin script ɗin ana karantewa ana amfani da shi nan take |
| Kalmar sirri **kada ta rubuta a cikin fayil ɗin hali**, kada ta bayyana a cikin rajistan ayyukan | Fayil ɗin hali na iya zama a kan diski; yanayin ƙirƙira yana nunta sau ɗaya domin mai amfani ya adana |
| Fayil ɗin hali yana cikin babban fayil ɗin wucin gadi na tsarin (`os.tmpdir()/powpow-register-state.json`, 0600) | Yana ɗauke da filaye biyar kawai: email / username / nickname / token / outTradeNo, `cleanup` yana sharewa da danna ɗaya |
| JWT ɗin da agent ta samu ana musanya shi zuwa cookie ɗin burauza ta hanyar gada ta hukuma `me?token=` | Gada ce ta hukuma da dandalin ya zana wa Harmony WebView; tabbatarwa tana duba saitti + lokacin inganci kawai, ba ta ɗaura da sawun na'ura ba, burauzar mai amfani za ta iya amfani da ita |
| Biya yana yin create-order / query / buɗe cashier kawai | Aikin biya da takaddun biya koyaushe suna tsakanin mai amfani da cashier na Alipay na hukuma, agent ba ta shiga ba |

## Jagoran umarni

| Umarni | Mahawari masu mahimmanci | Aiki / lokaci |
|---|---|---|
| `status` | —— | Duba ci gaban tsari (karanta fayil ɗin hali); bayan tattaunawa ta katse ka fara da wannan |
| `gen-password` | —— | Ƙirƙiri kalmar sirri mai ƙarfi ta haruffa 24 (girma-kanana + lambobi), ana nunta a stdout **sau ɗaya kawai** |
| `prepare-suggest` | `--username --nickname --email` | Ka rubuta bayanan da aka tabbatar a cikin fayil ɗin hali (daga baya register ba buƙatar maimaita wucewa) |
| `send-code` | `--email` | Ka haddasa dandalin ya aika lambar lambobi 6 (mai inganci a cikin minti 10, lokacin jira daƙiƙa 60) |
| `register` | `--code` (wajibi); `--username --nickname --avatar --phone` (na zaɓi, idan fayil ɗin hali yana da su ba buƙatar wucewa) | Ka gina asusun pending; kalmar sirri ta `POWPOW_REGISTER_PASSWORD`; bayan nasara JWT ana adanawa cikin fayil ɗin hali ta kai |
| `login-link` | `--target pending` ko `--target home` | Yana kirkirar hanyar shiga da danna daya (tsarin hanyoyi biyu, duba a kasa) |
| `create-order` | `--package monthly\|quarterly\|yearly` (tsoho na Alipay)<br>`--provider alipay\|paypal` | Ƙirƙiri oda biya; Alipay yana dawo da hanyar fayil ɗin shafin biya + outTradeNo; PayPal yana dawo da hanyar fayil ɗin shafin izini + subscriptionId (ana adanawa cikin fayil ɗin hali ta kai) |
| `query` | —— | Duba halin oda/membanci. Alipay: `paid / pending / closed / unknown`; PayPal: `ACTIVE / PENDING`; sake duba kowace daƙiƙa 10–15 |
| `refresh-login` | Kalmar sirri ta canjin muhalli | Ka sake shiga ka musanya **JWT sabuwa** (da'awar membanci na canzawa daga NONE zuwa ACTIVE), dole ne a gudanar da ita bayan kuɗin ya shiga |
| `whoami` | —— | Ka yi amfani da token ɗin fayil ɗin hali ka duba halin asusu da membanci (tabbatar da kunna ta yi aiki) |
| `cleanup` | —— | Ka share fayil ɗin hali (dole ne a gudanar da ita a ƙarshe) |

**Wucewa ta canjin muhalli** (kalmar sirri kada ta taɓa umarni):

```bash
# bash / zsh / WSL
POWPOW_REGISTER_PASSWORD='<kalmar sirri>' node scripts/powpow-register.mjs register --code 123456
# PowerShell
$env:POWPOW_REGISTER_PASSWORD = '<kalmar sirri>'; node scripts/powpow-register.mjs register --code 123456
# cmd
set POWPOW_REGISTER_PASSWORD=<kalmar sirri> && node scripts/powpow-register.mjs register --code 123456
```

## Tsarin hanyoyi biyu (tsarin asali)

Yanayin shiga na yanar gizo kuki ne na HttpOnly, wanda magidiman ba zai iya dasa shi kai tsaye a burauza; gada shi ne iyakar
`/api/auth/me?token=<JWT>&redirect=<hanya a cikin gidan yanar gizo>`: tabbatar da sa hannu → kirkira kai tsaye
zama → `Set-Cookie: powpow_token` (HttpOnly / SameSite=Lax / kwanaki 7) → tabbatar da
maye gurbin (dole ya fara da salo daya, `//` da salo masu baya an hana, dole ya zama same-origin bayan warware) → 307 maye gurbin na wancan lokaci zuwa shafin manufa.

Akwai manufofi biyu na hanyoyi, **fara kirkirar home, sannan ka yanke shawarar wucewa pending bisa inda mai amfani ya sauka**:

- **hanyar home (ana aika ta by default, `--target home` → sauka a `/`)**: ana kirkirar ta kuma aika wa mai amfani nan take bayan rajista ta samu nasara.
  A lokacin gwaji kyauta mai amfani yana zuwa shafin gida kai tsaye, cikakken amfani; **in ya danna hanyar amma ya sauka a shafin biya — lokacin gwaji kyauta ya kare** — sauya zuwa jawardar biya (duba a kasa); babu bukatar canza rubutu ko sake yin rajista.
- **hanyar pending (ana amfani da ita a jawardar biya, `--target pending` → sauka a `/subscription`)**:
  burauza mai amfani yana shiga yanayin "rabin shiga": shafin biya da shafin dawowa bayan biya suna bayyana kuma suna aiki. Bayan saukar kudi,
  gudanar da `refresh-login` don musanya sabon JWT tare da kimar ACTIVE, sannan aika hanyar home sake daya don cikakken matsayin mamba.

## Cikakken jeri

### Hanya mai sauri (a lokacin gwaji kyauta — yawancin lokuta)

```
1.  status                          # tabbatar da yanayin kansa
2.  (mataki 2 tattaunawa don tabbatar da bayani, kalmar sirri ko kaza; yanayin kirkira: gen-password → ce wa mai amfani ya ajiye nan take)
3.  prepare-suggest --username U --nickname N --email E
4.  send-code --email E             # → mai amfani yana duba lambar a akwatin sakonni (lokacin barin tattaunawa)
5.  POWPOW_REGISTER_PASSWORD=*** register --code 123456 [--avatar pic.jpg]
6.  login-link --target home        # → aika hanyar ga mai amfani; danna daya kuma a shafin gida
7.  (mai amfani ya tabbatar da shigarsa) → kammala nan take: cleanup + katin asusu + nuna matakan farko
```

### Hanyar biya (sa'adda mai amfani ya so mamba, ko lokacin gwaji kyauta ya kare)

```
1–5. Kamar hanya mai sauri (yanayi yana da token bayan rajista ta samu nasara)
6.  login-link --target pending     # → hanyar rabin shiga, tana rike shafin dawowa bayan biya yana aiki
7.  (mai amfani ya zabi hanyar biya)
    # Alipay: create-order --package monthly|quarterly|yearly
    # PayPal: create-order --provider paypal
8.  start <fayil din shafin biya>       # Windows; macOS yana amfani da open, Linux yana amfani da xdg-open
    # → mai amfani yana kammala biya/izini a karfat kudin Alipay/PayPal (yana barin tattaunawa)
9.  query (kowane 10–15s) har paid / ACTIVE
10. refresh-login                   # musanya sabon JWT tare da kimar ACTIVE
11. login-link --target home        # → aika hanyar cikakken mamba ga mai amfani
12. whoami                          # tabbatar da subscriptionStatus: ACTIVE (na zabi)
13. cleanup                         # share fayil din yanayi
```
## Taswirar umarni → API na dandalin

| Umarnin script | Tashar dandalin |
|---|---|
| `send-code` | `POST /api/auth/register/send-code` |
| `register` | `POST /api/auth/register` (multipart, ana ɗora avatar kai tsaye) |
| `login-link` | `GET /api/auth/me?token=…&redirect=…` (mahaɗi ɗaya ne, yana aiki lokacin da burauza ta danna) |
| `create-order` | `POST /api/payment/alipay/create-order` (Bearer, Alipay)<br>`GET /api/subscription/plans` + `POST /api/subscription/create` (Bearer, PayPal) |
| `query` | `GET /api/payment/alipay/query?outTradeNo=…` (Bearer, Alipay)<br>`GET /api/subscription/create` (Bearer, PayPal) |
| `refresh-login` | `POST /api/auth/login` (`{step:1, username, password}`) |
| `whoami` | `GET /api/auth/me?token=…` |

Inda dokuka suka samo: dokokin filaye da iyakancewa na rijista duba `registration-flow.md`; shiri da hanyar kunnawa duba
`payment-and-activation.md` (duka sun ambaci fayilolin code na dandalin).

## Kula da kuskure a matakin script

| Alama | Yadda ake kula |
|---|---|
| `Node 版本过低` (Node tana da ƙananan siga) | Ka koma yanayin jagora kawai, kada ka yi ta gwadawa da ƙarfi |
| Kuskuren hanyar sadarwa / lokaci ya wuce | Ka sake gwadawa sau ɗaya; har yanzu ya gaza, ka tambayi mai amfani ya duba hanyar sadarwa sannan ya ci gaba (fayil ɗin hali yana nan, ka gudanar da `status` daga farko domin dawowa) |
| register ta kawo kuskuren kasuwanci (用户名已存在 da sauransu) | Ka kula bisa teburin Mataki na 5 na SKILL.md, **lambar tabbatarwa ba buƙatar sake aikawa** (tana da inganci a cikin minti 10) |
| register ta kawo `邮箱验证码错误或已过期` (lambar tabbatarwa ta imel ba ta daidai ko ta ƙare) | Ya wuce lokaci → a sake `send-code` |
| Bayan `create-order` mai amfani ya rufe shafin biya | Ka sake `create-order` kai tsaye (tsohon oda yana rufewa da kai bayan sa'o'i 2; membancin PayPal PENDING yana ƙarewa bayan sa'a 1) |
| `create-order --provider paypal` ya dawo da 409 | Akwai membancin PayPal da ba a kammala ba; ka jira sa'a 1 ya ƙare, ko ka kammala tsohon izini a burauza |
| `query` na ci gaba da pending / PENDING | Mai amfani mai yiwuwa ba ya biya; ka tambaya. Hakika ya biya → ka bi teburin bincike na payment-and-activation.md |
| Mai amfani ya danna hanyar gida amma ya sauka a shafin biya | Lokacin gwaji kyauta ya kare → sauya zuwa jawardar biya: `login-link --target pending` → zabi hanyar biya → `create-order` |
| `refresh-login` 403 `pending_payment` | Lokacin gwaji kyauta ya kare kuma biya bata sauka ba; koma zuwa mataki 9 don ci gaba da nema, ko tabbatar da cewa mai amfani ya kammala biya |
| Fayil ɗin hali ya ɓace (an share shi ba zato ba tsammani / an canza na'ura) | `whoami`/`refresh-login` ba za a iya amfani da su ba; ka tambayi mai amfani a cikin burauzar da ta taɓa buɗe mahaɗi na 1 ya sabunta shafin membanci ya tabbatar da hali, ko ya sake shiga (yanayin yanar gizo) |

## Yanayin dawowa (jagora kawai)

A kowane ɗayan waɗannan hali, ka koma nan take ga yanayin jagora kawai na salon v1, kada ka ƙara damuwa da script ɗin:

- Ba a sami Node >= 18 ko script ɗin ta gaza sau biyu a jere iri ɗaya;
- Mai amfani ya faɗi a bayyane 'na da kansa zai yi aiki a yanar gizo';
- Manufofin kamfani/na'ura sun hana script ɗin haɗawa da intanet.

Bayan koma: ba shafin rajista https://global.powpow.online/register (a lokacin gwaji kyauta, rajistar yanar gizo ita ce nan take; sa'adda ana bukatar rajista, ba shafin biya kuma https://global.powpow.online/subscription ), warware matsala tare bisa ka'idodin `registration-flow.md`, riƙe kalar magana daya, kuma kammala kowane juyi da sashin "mataki na gaba".
https://global.powpow.online/subscription , ka bi dokokin `registration-flow.md` ka taimaka gyara kuskure, salo
ba ya canzawa, kowane zagaye har yanzu yana rufewa da sashin 'mataki na gaba'.
