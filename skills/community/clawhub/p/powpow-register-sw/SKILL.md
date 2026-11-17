---
name: powpow-register
description: Husaidia watumiaji kukamilisha usajili wa PowPow (Bubble) na kuingia kwa bonyezo moja ndani ya mazungumzo yote. Wakala hujaza fomu kwa niaba yao (ikiwa ni pamoja na kupakia picha ya wasifu) na hutuma msimbo wa uthibitishaji wa barua pepe; mtumiaji hutoa tu taarifa za msingi na kukagua msimbo wa uthibitishaji mara moja — haachi mazungumzo kabisa. Katika kipindi cha sasa cha majaribio bila malipo cha jukwaa, akaunti iliyosajiliwa inaweza kutumia kila kipengele mara moja; malipo ya sasiri (Alipay/PayPal) ni uboreshaji wa hiari wa uanachama, ambao wakala anaweza pia kuyashughulikia kwa kuunda oda na kufuatilia mapato inapohitajika. Huchochea wakati mtumiaji anasema "jiandikishe kwa Bubble", "fungua akaunti ya powpow", "nawezaje kujiandikisha kwa Bubble", "nisaidie kufungua akaunti ya powpow", "jiandikishe powpow"; pia hushughulikia matatizo ya usajili (msimbo wa uthibitishaji haujapokelewa, jina la mtumiaji/barua pepe tayari yamechukuliwa) na matatizo ya uamshaji (kuingia kunasema "akaunti haijawashwa" / pending_payment, nawezaje kusajili/kulipa, Bubble ni bila malipo au inagharimu). Inahitaji Node ≥ 18; hurejea kiotomatiki kwenye hali ya mwongozo safi inapopatikana. Haifanyi kazi za kuchapisha/kuunda binadamu wa digitali (ni kazi ya powpow-simple), wala maendeleo ya msimbo.
version: 2.2.0
metadata:
  openclaw:
    emoji: "\U0001F4DD"
    homepage: https://global.powpow.online
---

# PowPow Register (msaidizi wa usajili wa Povu)

Inachukua mtumiaji mpya kutoka "sijui Bubble ni nini" hadi "nimeingia kwa bonyezo moja, niko tayari kucheza" — yote ndani ya mazungumzo. Mtumiaji anaacha mazungumzo mara moja tu: **kukagua msimbo wa uthibitishaji kwenye kikasha chake**. Jukwaa kwa sasa liko katika kipindi cha majaribio bila malipo: mara baada ya kujiandikisha, kila kipengele kinapatikana, hakuna malipo yanayohitajika; malipo ya sasiri ni uboreshaji wa hiari wa uanachama (wakala pia hushughulikia kufungua kasha na kufuatilia mapato).

**Toleo 2.2.0** · 2026-10-18 (tangu v2 hii ni hali ya wakala-msaidizi: mkataba wa hati na mpangilio kamili kwenye `references/agent-flow.md`; kanuni za uwanja, vikomo za kiwango na utatuzi wa makosa kwenye `references/registration-flow.md`; njia za malipo kwenye `references/payment-and-activation.md`; orodha ya picha za bidhaa kwenye `references/screenshots.md`. Tangu v2.1.0 sasiri za PayPal pia zinaweza kushughulikiwa na wakala, kama chaguo pamoja na Alipay. Tangu v2.2.0 jukwaa limeingia katika kipindi cha majaribio bila malipo: jiandikishe na kuingia kwa bonyezo moja ili kuanza kutumia; malipo yamekuwa uboreshaji wa hiari — ikiwa mtumiaji anabonyeza kiungo na kutua kwenye ukurasa wa sasiri, kipindi cha majaribio kimekamilika, fuata mtiririko wa malipo wa Hatua 7; mtiririko unajirekebisha yenyewe, hakuna mabadiliko ya hati yanayohitajika)

## Mazingira ya kukimbia

- Hati kuu `scripts/powpow-register.mjs`: **haina tegemezi**, inahitaji **Node >= 18**. Kabla ya kuanza endesha mara moja `node scripts/powpow-register.mjs status` kuwa na uhakika mazingira yanafaa.
- Maombi yote ya hati yanaenda tu kwenye kikoa rasmi `https://global.powpow.online`.
- **Hakuna Node / makosa ya hati**: hurejea kiotomatiki kwenye hali ya mwongozo safi — mpe mtumiaji ukurasa wa usajili https://global.powpow.online/register na umwongoze kando kulingana na `references/registration-flow.md` (katika kipindi cha majaribio bila malipo, usajili wa wavuti ni wa haraka sawa). Usizidi kubisha hati.
- Baada ya mazungumzo kukatika na kurudisha: kwanza `status` kuona mchakato umefika hatua gani, kisha endelea.

## Trigger Conditions

- Nia ya usajili: "sajili Povu", "sajili akaunti ya powpow", "jinsi ya kusajili powpow", "sign up powpow"
- Usajili umekwama: "hauskii nambari ya uthibitisho", "jina la mtumiaji limesemwa kuwa limeshakuwepo", "nenosiri haifai kila wakati"
- Matatizo baada ya usajili: "kuingia kunasema akaunti haijawashwa", "403 pending_payment", "nawezaje kulipa/kusajili kwa Bubble", "Bubble ni bila malipo au inagharimu"

**Haifanyi trigger**: kutuma chapisho/kuunda mtu wa kidijitali (→ powpow-simple); maendeleo ya msimbo wa wavuti (tazama skill ya maendeleo). Mtumiaji anapotaka kusajili na pia kutuma chapisho: kwanza maliza skill hii, baada ya uwezeshaji peleka kwa powpow-simple.

## Muhtasari wa mtiririko

| Hatua | Agent anafanya nini | Mtumiaji anafanya nini |
|---|---|---|
| 1 Utangulizi wa bidhaa | Eleza + tuma picha | Tazama |
| 2 Uthibitisho wa maelezo | Pendekeza jina la mtumiaji/jina la kirafiki, nenosiri uchague moja, uliza barua pepe | Thibitisha, toa |
| 3 Tuma nambari ya uthibitisho | `send-code` | —— |
| 4 Soma nambari ya uthibitisho | —— | Nenda barua pepe tazama nambari ya tarakimu 6, rudi uitume |
| 5 Wasilisha usajili | `register` (pamoja na picha ya wasifu moja kwa moja), shughulikia makosa kiotomatiki | —— |
| 6 Kuingia kwa bonyezo moja | `login-link(home)` moja kwa moja kwenye ukurasa wa nyumbani; ikiwa kinatua kwenye ukurasa wa sasiri, nenda Hatua 7 | Bonyeza kiungo na uanze kucheza |
| 7 Uboreshaji wa sasiri (wa hiari) | Tu wakati mtumiaji anataka uanachama / kipindi cha bila malipo kimekamilika: mtiririko kamili wa malipo unashughulikiwa | Chagua njia, lipa |
| 8 Kumalizia | `cleanup` + toa utambulisho + ongoza uzoefu + pendekeza programu-jalizi | Anza kucheza |

## Hatua ya 1: Utangulizi wa bidhaa + picha (haipitiwi)

Watumiaji wengi hawajawahi kuona Povu. Jambo la kwanza si kueleza mtiririko, bali kumfanya **aone** bidhaa:

1. Eleza Povu kwa maneno ya takriban 120: picha ulizoipiga kirahisi zinageuka kuwa safari ya kusafiri, zimepachikwa kwenye ramani ya wazi kuwa "povu" moja; povu huzidi kupoa kwa wakati, watu wengine wakipenda huufufua; kwenye ramani pia kuna "watu wa kidijitali" unaweza kuongea nao. Anwani ya jukwaa https://global.powpow.online, ukiwa unataka kutazama video kwanza: https://www.bilibili.com/video/BV1Wu826UEVz/
2. **Tuma picha**. Picha zimefungwa pamoja na skill katika `assets/screenshots/powpow-0N.jpg` — tuma moja kwa moja kama faili ya picha ya ndani, huhitaji mtandao. Orodha, yaliyomo ya kila picha na wakati wa kuzitumia angalia `references/screenshots.md`. Mchanganyiko unaotumika zaidi kwa mwanzo: ukurasa wa ramani (powpow-03) + ukurasa wa maelezo ya chapisho (powpow-06).

Sheria za picha (kanuni ngumu):

- Picha **zimefungwa pamoja na skill** katika `assets/screenshots/` (`powpow-0N.jpg`) — tuma tu faili ya picha ya ndani; inafaa katika mazingira yoyote, hata mazingira ambayo GitHub haifunguliwi.
- Tuma mara moja tu picha 1–3 zinazohusiana na mada ya sasa, usizipake zote mara moja.
- Ikiwa faili za ndani zinakosekana kwa bahati mbaya, rudi kwenye viungo vya hifadhi vilivyoorodheshwa katika `references/screenshots.md` (tahadhari: nchini China vinaweza kutofunguliwa).

Baada ya kueleza, mruhusu mtumiaji achague: **"Ukitaka kusajili, tutajenga akaunti mazungumzoni kwa dakika tatu, unahitaji tu kutazama nambari ya uthibitisho ya barua pepe mara moja."**

## Hatua ya 2: Thibitisha maelezo ya usajili (uliza swali moja kwa wakati, usziulize zote mara moja)

- **Jina la mtumiaji** (inahitajika): kutoka muktadha wa mazungumzo/jina la mtumiaji wa mfumo **pendekeza moja** (herufi 2~50, bila kujali herufi kubwa ndogo), mtumiaji akipiga kuni atumie, akitaka kubadilisha abadilishe.
- **Nenosiri** (inahitajika, uliza mtumiaji uchague moja):
  - Mtumiaji mwenyewe atoe → baadaye litumie kupitia kigezo cha mazingira kwa hati, **kamwe usiiandike kwenye vigezo vya amri**;
  - Agent itengeneze → endesha `node scripts/powpow-register.mjs gen-password`, utume nenosiri lililotengenezwa **mara moja kwa mtumiaji aliweke** (inaonyeshwa mara moja tu, baadaye haitatokea tena).
- **Barua pepe** (inahitajika): lazima mtumiaji atoe — hii ndiyo nanga ya utambulisho wa akaunti, **usimwaghani mtumiaji**.
- **Jina la kirafiki** (hiari): pendekeza chaguo-msingi sawa na jina la mtumiaji.
- **Picha ya wasifu** (hiari): mtumiaji akitoa njia ya faili ya picha ya ndani (<=5MB, sio SVG) hati itaipakia moja kwa moja; usipotoa aache (jukwaa litumie nembo ya chaguo-msingi); ukiwa na uwezo wa kutengeneza picha, unaweza kupendekeza kumsaidia mtumiaji kutengeneza moja.
- **Nambari ya simu** (hiari, nambari ya bara): chaguo-msingi ache, mtumiaji akipenda kufunga atoe.

Baada ya kuthibitisha unaweza kuendesha `prepare-suggest --username U --nickname N --email E` kuandika kwenye faili ya hali (baadaye register haitaki kurudia kutuma).

## Hatua ya 3–4: Nambari ya uthibitisho ya barua pepe (sehemu pekee inayohitaji kuondoka mazungumzoni)

```
node scripts/powpow-register.mjs send-code --email <barua pepe>
```

Kisha mwambie wazi mtumiaji: **nenda barua pepe tafuta nambari ya tarakimu 6, inayofaa kwa dakika 10, kumbuka kuangalia folda ya barua taka/utangazaji**, ukipata rudi uitume. Kutuma kuna muda wa kupoeza sekunde 60, usibofye mara kwa mara.

## Hatua ya 5: Wasilisha usajili (agent husaidia)

```
POWPOW_REGISTER_PASSWORD=<nenosiri> node scripts/powpow-register.mjs register --code <nambari ya uthibitisho> [--username U] [--nickname N] [--avatar <njia ya faili ya picha ya ndani>] [--phone P]
```

Mafanikio yaunda akaunti (hali ya pending, pamoja na beji 3 za mwanzo). Makosa ya kawaida yashughulikiwa kiotomatiki, hayakatishi mtumiaji:

| Kosa | Shughulikia |
|---|---|
| 用户名已存在 (jina la mtumiaji limeshakuwepo) | Pendekeza toleo (jina la mtumiaji + nambari) kiotomatiki, mtumiaji athibitisha halafu jaribu tena moja kwa moja (nambari ya uthibitisho bado inafaa, hahitaji kutuma tena) |
| 邮箱已被使用 (barua pepe imeshatumiwa) | Uliza mtumiaji: badilisha barua pepe nyingine, au labda tayari ana akaunti (badili kwenda kuingia/urejeshaji nenosiri) |
| 邮箱验证码错误或已过期 (nambari ya uthibitisho ya barua pepe ni mbaya au imeisha muda) | Ikipita dakika 10 → tuma tena `send-code` |
| 发送/注册过于频繁（429） (kutuma/usajili mara nyingi mno (429)) | Subiri dakika 1 kisha jaribu tena, mwambie mtumiaji tu |

## Hatua 6: Kuingia kwa Bonyezo Moja (moja kwa moja kwenye ukurasa wa nyumbani baada ya usajili)

1. Mara baada ya usajili kufanikiwa:
   ```
   node scripts/powpow-register.mjs login-link --target home
   ```
2. Tuma kiungo kwa mtumiaji: **bonyeza na wewe unatua moja kwa moja kwenye ukurasa wa nyumbani, tayari umeingia**. Jukwaa kwa sasa liko katika kipindi cha majaribio bila malipo — baada ya kujiandikisha, kila kipengele kinapatikana (mlipuko, ramani, binadamu wa digitali, viingilio, n.k.), **hakuna malipo yanayohitajika**.
3. Mwombe mtumiaji athibitishe kuwa ameingia; kuna hali mbili:
   - **Ametua kwenye ukurasa wa nyumbani** → rukia moja kwa moja Hatua 8 kufunga kazi; usajili umekamilika;
   - **Ametua kwenye ukurasa wa sasiri** → kipindi cha majaribio bila malipo cha jukwaa kimekamilika; mwambie mtumiaji "kipindi cha majaribio bila malipo kimeisha, sasiri ya uanachama inahitajika sasa", kisha fuata Hatua 7 kukamilisha sasiri, na urudi Hatua 8 baada ya kusajili.
4. Kama mtumiaji mwenyewe anataka kuboresha au kusaidia jukwaa → pia nenda Hatua 7 (kusajiri ni kwa hiari; usisukume).
## Hatua 7: Uboreshaji wa Sasiri (wa hiari — tu wakati Hatua 6 inaita)

1. Kwanza tuma kiungo cha nusu-kuingia ili ukurasa wa kurudi kwa malipo uweze kuonyesha "Malipo yamefanikiwa" kwa usahihi:
   ```
   node scripts/powpow-register.mjs login-link --target pending
   ```
   Tuma kiungo kwa mtumiaji: kubonyeza kunamwacha kivinjari moja kwa moja kwenye ukurasa wa sasiri, tayari ameingia.
2. **Mwombe mtumiaji achague njia ya malipo** — onyesha njia zote mbili:
   - **Alipay (China bara / watumiaji wenye Alipay)**: ununuzi wa mara moja wa muda unaolingana, **hakuna kujirudia kiotomatiki**
     - Kila mwezi **¥6.99** (inapendekezwa kwa majaribio) / Kila robo **¥19.99** / Kila mwaka **¥69.99**
   - **PayPal (nje ya nchi / watumiaji wasio na Alipay)**: hujirudia kiotomatiki kila mwezi, ghairi wakati wowote
     - Premium Kila mwezi, karibu **$1/mwezi** (kama inavyoonyeshwa kwenye ukurasa wa sasiri; hujirudia kiotomatiki)
3. Mara mtumiaji anapochagua moja:
   - **Alipay**:
     ```
     node scripts/powpow-register.mjs create-order --package monthly
     ```
   - **PayPal**:
     ```
     node scripts/powpow-register.mjs create-order --provider paypal
     ```
   Hiti inarudisha njia ya faili ya ukurasa wa malipo; **ifungue moja kwa moja kwa amri ya mfumo** (Windows: `start <file>`; macOS: `open <file>`; Linux: `xdg-open <file>`). Kivinjari hurukia kiotomatiki kwenye kasha rasmi ya Alipay/PayPal, ambapo mtumiaji hukamilisha malipo au idhini ya bili.
4. Endesha `query` kila sekunde 10–15 hadi irudishe `paid` au `ACTIVE` (malipo/idhini kwa kawaida hufika ndani ya sekunde chache hadi dakika moja). Kama mtumiaji anafunga ukurasa wa malipo katikati → fanya `create-order` tena (oda za zamani / sasiri zinazosubiri hufungwa au kwisha kiotomatiki baada ya masaa 2; ziondoe).
5. Njia ya msimbo wa QR ya WeChat huthibitishwa kwa mikono na fedha zinaweza kufika marehemu; Huawei IAP inapatikana tu ndani ya Programu ya HarmonyOS. Hiti hii haiwezi kushughulikia hizi mbili — baada ya kulipa, mtumiaji anarudi na kumwambia wakala, ambaye kwanza anaendesha `whoami` kuthibitisha mapato, kisha anatuma kiungo cha ukurasa wa nyumbani kwa punto 6 hapa chini.
6. Baada ya mapato kuthibitishwa, badilishana hali ya kuingia yenye dai la sasa la sasiri, kisha tuma kiungo moja kwa moja kwenye ukurasa wa nyumbani:
   ```
   POWPOW_REGISTER_PASSWORD=<password> node scripts/powpow-register.mjs refresh-login
   node scripts/powpow-register.mjs login-link --target home
   ```
   Tuma kiungo kwa mtumiaji: **bonyeza na wewe unatua moja kwa moja kwenye ukurasa wa nyumbani wenye hali kamili ya uanachama**.
## Hatua 8: Kufunga Kazi

1. `node scripts/powpow-register.mjs cleanup` kusafisha faili za hali za muda za ndani (vitambulisho vya kipindi).
2. Mpe mtumiaji "kadi ya akaunti": jina la mtumiaji, barua pepe (nywila haionyeshwi tena — katika hali ya kuzalisha mtumiaji aliombwa kuhifadhi wakati ilizalishwa; kama mtumiaji aliweka mwenyewe, anaijua).
3. Ukumbusho wa uanachama (sema mara moja, usisukume): hii kwa sasa ni kipindi cha majaribio bila malipo na akaunti inapatikana mara moja; kipindi cha majaribio kinapokamilika, akaunti zisizo na sasiri zinazotembelea kurasa za maudhui zitaelekezwa kwenye ukurasa wa sasiri — kwa matumizi ya muda mrefu, rudi na umtafute wakala kusajiri wakati wowote.
4. Ongoza hatua za kwanza: vinjari ramani, chapisha jarida la kwanza la safari (→ peleka kwa powpow-simple).
5. Pendekeza viendelezi: hati ya `@durenzidu/powpow-integration` na programu-jalizi ya `@durenzidu/openclaw-channel-powpow` — unganisha Bubble kwenye wakala mwenyewe wa mtumiaji; mpe amri ya usakinishaji akitaka.
6. Maliza na bloku ya "hatua inayofuata".
## Conversation UX

Endeleza sauti ya huduma ya PowPow:

- **Mtumiaji ndiye mada ya sentensi**, "unaweza..." ni bora kuliko "ninahitaji wewe..."; usifundishe, usijinyanyue.
- **Songa mbele kwa uamuzi mmoja kwa raundi**; kabla ya kuomba maelezo toa sababu.
- **Mwisho wa kila jibu** ni sehemu ya kudumu ya "hatua inayofuata" (mlalo wa kutenganisha + 👉 + kitendo kimoja + sentensi moja ya "nitakapofanya..."), kwa mfano:
  ```
  ────────────────────
  👉 Unachohitaji sasa: nenda barua pepe tafuta nambari ya tarakimu 6, uitume moja kwa moja
     (nitakapopokea nitajenga akaunti mara moja)
  ```
- **Usifanye mafunzo ya usalama kwa nenosiri kwa nafsi yako**; usieleze utaratibu wa ndani, vizuizi, au muundo wa usalama, isipokuwa mtumiaji aulize.
- Wakati agent inaposaidia, toa taarifa za maendeleo zaidi: baada ya kila hatua ya hati mwambie kwa sentensi moja kilichoendelea (akaunti imejengwa, ukurasa wa malipo umefunguliwa kwa ajili yako).

## Kanuni ngumu

- **Usalama wa kitambulisho**: nenosiri hutumiwa tu kupitia kigezo cha mazingira `POWPOW_REGISTER_PASSWORD` kwa hati, **kamwe** usiiandike kwenye vigezo vya amri (orodha ya mchakato inaonekana), usiiandike kwenye faili yoyote (mtindo wa kutengeneza unaonyesha mara moja ili mtumiaji ahifadhi, baadaye haitajwi tena). Nambari ya uthibitisho hutumiwa tu kwa kiolesura rasmi cha usajili, inapotumika inaachwa.
- **Mpaka rasmi**: maombi yote yanaenda tu kwenye `https://global.powpow.online` (hati imejumuisha tayari), kamwe usitume maelezo ya mtumiaji kwa anwani yoyote ya mtu wa tatu.
- **Mpaka wa malipo**: agent huunda agizo, hufungua cashier, hufuatilia malipo; **kamwe** haigusi akaunti ya Alipay/PayPal ya mtumiaji / kitambulisho cha malipo, wala haiahidi "kulipa badala yake".
- **Ukuta wa malipo si hitilafu**: katika kipindi cha sasa cha majaribio bila malipo kurasa zote za maudhui zimefunguliwa; kama mtumiaji anabonyeza kiungo cha ukurasa wa nyumbani lakini anatua kwenye ukurasa wa sasiri, kipindi cha majaribio kimekamilika — mwongoze kusajili kupitia Hatua 7. Usijaribu kupita ukuta wa malipo, na usieleze mifumo ya ndani kwa mtumiaji.
- **Uhuru wa kurudi nyuma**: hatua yoyote mtumiaji anapotaka kufanya mwenyewe, au mazingira hayasaidii hati, anaweza kurudi wakati wowote kwenye mtindo wa mwongozo mtupu — toa viungo, eleza sheria, saidia kutatua makosa.
- Usitengeneze sheria za jukwaa: sheria za sehemu, maandishi ya makosa, vigezo vya vizuizi vyote vinatoka kwenye msimbo wa jukwaa (`references/registration-flow.md` ina chanzo cha msimbo), sasisho la jukwaa hufuata tabia halisi ya mtandaoni.
- Picha uonyesho tumia tu zile za `assets/screenshots/` zilizofungwa pamoja na skill (matumizi ya kila picha angalia `references/screenshots.md`).
- Kila raundi malizia kwa sehemu ya "hatua inayofuata", ili mtumiaji ajuu kila wakati anachopaswa kufanya.
