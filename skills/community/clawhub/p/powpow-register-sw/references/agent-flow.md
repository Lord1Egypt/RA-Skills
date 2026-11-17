# Mkato wa agent-kusaidia na mkataba wa hati — powpow-register

Maelezo ya utekelezaji wa hatua za SKILL.md. Amri zote ni `node scripts/powpow-register.mjs <amri-ndogo> [vigezo]`, hati **haina tegemezi**, inahitaji **Node >= 18**, maombi yote yanaenda tu `https://global.powpow.online`.

## Muundo wa usalama (kwa nini imeundwa hivi)

| Muundo | Sababu |
|---|---|
| Nenosiri hutumiwa tu kupitia kigezo cha mazingira `POWPOW_REGISTER_PASSWORD` | vigezo vya amri ya mchakato vinaonekana kwa michakato mingine ya mashine hii (usemi wa uvujaji wa argv), kigezo cha mazingira ndani ya hati kinasomwa kikitumika mara moja |
| Nenosiri **kamwe haiiandikwi kwenye faili ya hali**, kamwe haionekani kwenye logi | faili ya hali inaweza kubaki kwenye diski; mtindo wa kutengeneza unaoonyesha mara moja ni ili mtumiaji ahifadhi |
| Faili ya hali imehifadhiwa katika saraka ya muda ya mfumo (`os.tmpdir()/powpow-register-state.json`, 0600) | inayo sehemu tano tu: email / username / nickname / token / outTradeNo, `cleanup` hufuta kiotomatiki |
| JWT anayopata agent hubadilishwa kuwa cookie ya kivinjari kupitia kiolesura rasmi `me?token=` | daraja rasmi jukwaa lililounda kwa Harmony WebView; uthibitisho wa saini huchunguza tu saini + muda wa ufanisi, haifungi kwenye alama ya kifaa, kivinjari cha mtumiaji kinaweza kutumia |
| Malipo yanafanya tu create-order / query / kufungua cashier | kitendo cha kulipa na kitambulisho cha malipo kila wakati kiko kati ya mtumiaji na cashier rasmi ya Alipay, agent haipiti |

## Marejeleo ya amri

| Amri | Vigezo vya msingi | Kazi / wakati |
|---|---|---|
| `status` | —— | Tazama maendeleo ya mtiririko (soma faili ya hali); baada ya mazungumzo kukatika endesha hii kwanza |
| `gen-password` | —— | Tengeneza nenosiri dhabiti ya herufi 24 (mchanganyiko wa herufi kubwa ndogo + tarakimu), inaonyeshwa **mara moja tu** kwenye stdout |
| `prepare-suggest` | `--username --nickname --email` | Andika maelezo yaliyothibitishwa kwenye faili ya hali (baadaye register haitaki kurudia kutuma) |
| `send-code` | `--email` | Chasema jukwaa litume nambari ya tarakimu 6 (inayofaa kwa dakika 10, muda wa kupoeza sekunde 60) |
| `register` | `--code` (inahitajika); `--username --nickname --avatar --phone` (hiari, kama faili ya hali inavo hahitaji kutuma) | Unda akaunti ya pending; nenosiri kupitia `POWPOW_REGISTER_PASSWORD`; baada ya mafanikio JWT huhifadhiwa kiotomatiki kwenye faili ya hali |
| `login-link` | `--target pending` au `--target home` | Huzalisha kiungo cha kuingia kwa bonyezo moja (muundo wa viungo viwili, ona hapa chini) |
| `create-order` | `--package monthly\|quarterly\|yearly` (chaguomsingi Alipay)<br>`--provider alipay\|paypal` | Unda agizo la malipo; Alipay inarudisha njia ya faili ya ukurasa wa malipo + outTradeNo; PayPal inarudisha njia ya faili ya ukurasa wa uidhinishaji + subscriptionId (huhifadhiwa kiotomatiki kwenye faili ya hali) |
| `query` | —— | Angalia hali ya agizo/usajili. Alipay: `paid / pending / closed / unknown`; PayPal: `ACTIVE / PENDING`; hoji kila sekunde 10–15 |
| `refresh-login` | Nenosiri kupitia kigezo cha mazingira | Ingia tena kubadilisha **JWT mpya** (tamko la usajili hubadilika kutoka NONE kuwa ACTIVE), lazima iendeshwe baada ya malipo kufika |
| `whoami` | —— | Tumia token ya faili ya hali kuangalia hali ya akaunti na usajili (thibitisha uwezeshaji umefanya kazi) |
| `cleanup` | —— | Futa faili ya hali (lazima iendeshwe mwishoni) |

**Upitishaji wa kigezo cha mazingira** (nenosiri kamwe haingii kwenye amri):

```bash
# bash / zsh / WSL
POWPOW_REGISTER_PASSWORD='<nenosiri>' node scripts/powpow-register.mjs register --code 123456
# PowerShell
$env:POWPOW_REGISTER_PASSWORD = '<nenosiri>'; node scripts/powpow-register.mjs register --code 123456
# cmd
set POWPOW_REGISTER_PASSWORD=<nenosiri> && node scripts/powpow-register.mjs register --code 123456
```

## Mfumo wa Viungo Viwili (muundo wa msingi)

Hali ya kuingia ya jukwaa ni kuki ya HttpOnly, ambayo wakala hawezi kuzalisha kwa kivinjari moja kwa moja; daraja ni rasmi
`/api/auth/me?token=<JWT>&redirect=<njia ya ndani ya tovuti>`: thibitisha saini → unda kipindi
kiotomatiki → `Set-Cookie: powpow_token` (HttpOnly / SameSite=Lax / siku 7) → thibitisha
kuelekeza (lazima ianze na mkwaju mmoja, `//` na mikwaju ya nyuma imekatazwa, lazima iwe chanzo sawa baada ya kuchanganua) → 307 kuelekeza kwa muda hadi ukurasa lengwa.

Kuna malengo mawili ya viungo, **zalisha nyumbani kwanza, kisha amua kama utapitia pending kulingana na mahali mtumiaji anapotua**:

- **kiungo cha nyumbani (kinatumwa kwa chaguo-msingi, `--target home` → kinatua kwenye `/`)**: kinazalishwa na kutumwa kwa mtumiaji mara baada ya usajili kufanikiwa.
  Katika kipindi cha majaribio bila malipo mtumiaji huenda moja kwa moja kwenye ukurasa wa nyumbani, kinapatikana kikamilifu; **kama mtumiaji anabonyeza lakini anatua kwenye ukurasa wa sasiri, kipindi cha majaribio bila malipo kimekamilika** — badilisha kwenye njia ya malipo (ona hapa chini); hakuna mabadiliko ya hati na hakuna usajili upya unaohitajika.
- **kiungo cha pending (kinatumika katika njia ya malipo, `--target pending` → kinatua kwenye `/subscription`)**:
  kivinjari cha mtumiaji huingia katika hali ya "nusu-kuingia": ukurasa wa sasiri na ukurasa wa kurudi kwa malipo ni vinara na vinafanya kazi. Baada ya malipo kufika,
  endesha `refresh-login` kubadilishana JWT mpya yenye dai la ACTIVE, kisha tuma kiungo cha nyumbani tena kwa hali kamili ya uanachama.

## Mpangilio Kamili

### Njia ya Haraka (katika kipindi cha majaribio bila malipo — wingi mkubwa wa matukio)

```
1.  status                          # ukaguzi wa mazingira
2.  (mazungumzo ya Hatua 2 kuthibitisha taarifa, nywila mojawapo; hali ya kuzalisha: gen-password → mwombe mtumiaji ahifadhi mara moja)
3.  prepare-suggest --username U --nickname N --email E
4.  send-code --email E             # → mtumiaji hukagua msimbo kwenye kikasha chake (wakati pekee wa kuacha mazungumzo)
5.  POWPOW_REGISTER_PASSWORD=*** register --code 123456 [--avatar pic.jpg]
6.  login-link --target home        # → tuma kiungo kwa mtumiaji; bonyezo moja na yuko kwenye ukurasa wa nyumbani
7.  (mtumiaji athibitishe ameingia) → funga moja kwa moja: cleanup + kadi ya akaunti + ongoza hatua za kwanza
```

### Njia ya Malipo (wakati mtumiaji anataka uanachama, au kipindi cha majaribio bila malipo kimekamilika)

```
1–5. Sawa na njia ya haraka (hali tayari ina tokeni baada ya register kufanikiwa)
6.  login-link --target pending     # → kiungo cha nusu-kuingia, huweka ukurasa wa kurudi kwa malipo ukifanya kazi
7.  (mtumiaji achague njia ya malipo)
    # Alipay: create-order --package monthly|quarterly|yearly
    # PayPal: create-order --provider paypal
8.  start <faili ya ukurasa wa malipo>       # Windows; macOS hutumia open, Linux hutumia xdg-open
    # → mtumiaji hukamilisha malipo/idhini kwenye kasha cha Alipay/PayPal (anaacha mazungumzo)
9.  query (kila 10–15s) hadi paid / ACTIVE
10. refresh-login                   # badilishana JWT mpya yenye dai la ACTIVE
11. login-link --target home        # → tuma kiungo cha uanachama kamili kwa mtumiaji
12. whoami                          # thibitisha subscriptionStatus: ACTIVE (hiari)
13. cleanup                         # safisha faili ya hali
```
## Ramani ya amri → API ya jukwaa

| Amri ya hati | Kiolesura cha jukwaa |
|---|---|
| `send-code` | `POST /api/auth/register/send-code` |
| `register` | `POST /api/auth/register` (multipart, picha ya wasifu hupakia moja kwa moja) |
| `login-link` | `GET /api/auth/me?token=…&redirect=…` (kiungo yenyewe, kinatoa madhumuni wakati mtumiaji abofya) |
| `create-order` | `POST /api/payment/alipay/create-order` (Bearer, Alipay)<br>`GET /api/subscription/plans` + `POST /api/subscription/create` (Bearer, PayPal) |
| `query` | `GET /api/payment/alipay/query?outTradeNo=…` (Bearer, Alipay)<br>`GET /api/subscription/create` (Bearer, PayPal) |
| `refresh-login` | `POST /api/auth/login` (`{step:1, username, password}`) |
| `whoami` | `GET /api/auth/me?token=…` |

Chanzo cha sheria: sheria za sehemu na vizuizi za usajili angalia `registration-flow.md`; mpango na mlolongo wa uwezeshaji angalia
`payment-and-activation.md` (yote yana chanzo la faili ya msimbo wa jukwaa kilichotajwa).

## Utatuzi wa makosa ya kiwango cha hati

| Tukio | Shughulikia |
|---|---|
| `Node 版本过低` (Node imekuwa toleo la chini) | Rudi kwenye mtindo wa mwongozo mtupu, usijaribu kwa nguvu |
| Kosa la mtandao / muda uliopita | Jaribu tena mara moja; bado ikishindwa mwambie mtumiaji achunguze mtandao kisha aendelee (faili ya hali bado ipo, endesha `status` mwanzo ili urudie) |
| register inaporoja kosa la biashara (jina la mtumiaji limeshakuwepo, n.k.) | Shughulikia kulingana na jedwali la Hatua ya 5 la SKILL.md, **nenosiri haihitaji kutumiwa tena** (bado inafaa ndani ya dakika 10) |
| register inaporoja `邮箱验证码错误或已过期` (nambari ya uthibitisho ya barua pepe ni mbaya au imeisha muda) | Ikipita muda → tuma tena `send-code` |
| Baada ya `create-order` mtumiaji amefunga ukurasa wa malipo | Endesha tu tena `create-order` (agizo la zamani hufungwa kiotomatiki baada ya saa 2; usajili wa PENDING wa PayPal hufungwa baada ya saa 1) |
| `create-order --provider paypal` inarudisha 409 | Tayari kuna usajili wa PayPal usio malizika; subiri saa 1 upite, au maliza uidhinishaji wa zamani kwenye kivinjari |
| `query` inabaki pending / PENDING | Labda mtumiaji hajali; uliza. Amekweli kulipa → fuata jedwali la utatuzi wa payment-and-activation.md |
| Mtumiaji anabonyeza kiungo cha nyumbani lakini anatua kwenye ukurasa wa sasiri | Kipindi cha majaribio bila malipo kimekamilika → badilisha kwenye njia ya malipo: `login-link --target pending` → chagua njia ya malipo → `create-order` |
| `refresh-login` 403 `pending_payment` | Kipindi cha majaribio bila malipo kimekamilika na malipo hayajafika; rudi hatua 9 kuendelea kuchunguza, au thibitisha kama mtumiaji alikamilisha malipo |
| Faili ya hali imepotea (ilifutwa kwa bahati mbaya / kuhamia mashine nyingine) | `whoami`/`refresh-login` haviwezi kutumika; mruhusu mtumiaji kwenye kivinjari alichofungua kiungo 1 aburudge ukurasa wa usajili wa malipo ili athibitishe hali, au ingia tena (mtindo wa wavuti) |

## Mtindo wa kurudi nyuma (mwongozo mtupu)

Hali yoyote ifuatayo, rudi mara moja kwenye mtindo wa mwongozo mtupu wa v1, usisumbue tena hati:

- Hakuna Node >= 18 au hati inashindwa mara mbili mfululizo kwa aina ile ile;
- Mtumiaji anasema wazi "mimi mwenyewe nitafanya kwenye wavuti";
- Sera ya kampuni/kifaa inazuia hati kuunganisha mtandao.

Baada ya kurejea: mpe ukurasa wa usajili https://global.powpow.online/register (katika kipindi cha majaribio bila malipo, usajili wa wavuti ni wa haraka sawa; wakati sasiri inahitajika, pia mpe ukurasa wa sasiri https://global.powpow.online/subscription ), tatua kando kulingana na kanuni za `registration-flow.md`, weka sauti sawa, na bado maliza kila zamu na bloku ya "hatua inayofuata".
https://global.powpow.online/subscription, fuata sheria za `registration-flow.md` kumsaidia kutatua, sauti
hubadilika, kila raundi bado malizia kwa sehemu ya "hatua inayofuata".
