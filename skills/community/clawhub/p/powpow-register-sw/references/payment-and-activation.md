# Uwezeshaji wa usajili na malipo — powpow-register

## Hitimisho (jibu kwanza)
> **Kipindi cha majaribio bila malipo (kuanzia 2026-10-18; tabia halisi ya jukwaa ndiyo inayotawala)**: katika kipindi hiki akaunti iliyosajiliwa inaweza kutumia kila kipengele moja kwa moja, na **kusajiri ni uboreshaji wa hiari sio sharti** — fuata mtiririko wa faili hili tu wakati mtumiaji mwenyewe anataka uanachama. Kipindi cha majaribio kinapokamilika, akaunti zisizo na sasiri zinazotembelea kurasa za maudhui zitaelekezwa kwenye ukurasa wa sasiri; kamilisha tu sasiri kulingana na faili hili.


**Sasa njia zote mbili za Alipay na PayPal zinaweza kushughulikiwa na agent — kuunda agizo na kufuatilia ufikiaji wa malipo.**
Alipay ni ununuzi wa mara moja bila ushamiri otomatiki, kwa watumiaji wa China bara na watumiaji wenye Alipay; PayPal inashamiri otomatiki kila mwezi na inaweza kubatilishwa wakati wowote, kwa watumiaji wa nje na watumiaji wasio na Alipay. Usome msimbo wa WeChat (uthibitisho wa mtu) na Huawei IAP bado zipo, lakini hazimsimamiwi na skill.

Mpaka wa wajibu wa sehemu ya malipo: agent inaweza **unda agizo, fungua cashier, fuatilia malipo**; **kamwe** haigusi akaunti ya Alipay/PayPal ya mtumiaji / kitambulisho cha malipo, kamwe haiachi "kulipa badala yake". Kitendo cha kulipa kila wakati kinafanywa na mtumiaji mwenyewe kwenye cashier rasmi.

## Njia ya Alipay (vibepay, kuu)

Mfumo wa ununuzi wa mara moja: ulipa mara moja kuwezesha muda unaolingana, **haushamiri otomatiki**. Mpango umefungwa katika `src/lib/alipay-vibepay.ts` (`ALIPAY_PACKAGES`):

| key | planId | Jina | Bei | Muda |
|---|---|---|---|---|
| `monthly` | alipay-monthly | Mwanachama wa mwezi | ¥6.99 | siku 30 |
| `quarterly` | alipay-quarterly | Mwanachama wa robo mwaka | ¥19.99 | siku 90 |
| `yearly` | alipay-yearly | Mwanachama wa mwaka | ¥69.99 | siku 365 |

### Mkataba wa kiolesura (skill imefunga tayari, agent haichanganyi ombi moja kwa moja)

| Kiolesura | Njia | Maelezo |
|---|---|---|
| `/api/payment/alipay/create-order` | POST | Inahitaji `Authorization: Bearer <JWT>` (mtumiaji wa pending anaridhika). body `{package}` → inarudisha `{paymentHtml, outTradeNo, amount, planName}`; `paymentHtml` ni ukurasa wa fomu inayotuma kiotomatiki kwenye lango la Alipay |
| `/api/payment/alipay/query` | GET `?outTradeNo=` | Kadhalika uthibitisho wa Bearer. Inarudisha `paid` / `pending` / `closed` / `unknown` |
| `/api/payment/alipay/notify` | POST (Alipay server callback) | Uthibitisho wa saini ya vipengele vitano (saini, app_id, idadi ya pesa inalingana, TRADE_SUCCESS/TRADE_FINISHED, ya kipekee ya mfanyabiashara) → **idempotent** inasasisha agizo + kujenga usajili + kuwezesha akaunti. Skill haiigusi kamwe kiolesura hiki |
| `/payment/alipay/return` | Ukurasa wa kurudi wa kivinjari | Njia wazi, baada ya malipo inaonyesha uthibitisho wa "支付成功" (malipo yamefanikiwa), ukurasa unahoji hali halisi ya upande wa nyuma |

- Agizo lisilolipwa **hufungwa kiotomatiki baada ya saa 2**; mtumiaji aache katikati → endesha tu tena `create-order`, agizo la zamani hahitaji kujali.
- Hati inaandika `paymentHtml` kwenye faili ya muda ya HTML, agent hutumia amri ya mfumo kufungua ili ingie kwenye cashier ya Alipay (soma msimbo au ingia kwenye Alipay kulipa).

### Mlolongo wa uwezeshaji (otomatiki, hauhitaji mtu)

notify uthibitisho wa saini upitapo → `paymentOrders` umewekwa kuwa imeilipwa → `user_subscriptions` kujengwa/inakwama (`planId`, `currentPeriodEnd` inakokotolewa kulingana na durationDays, kujiunga tena kunakwama kwenye tarehe ya mwisho ya awali) →
`users.accountStatus: active` + `subscriptionStatus: ACTIVE` → ukurasa wa kurudi unahoji hadi paid unaonyesha mafanikio.

### Baada ya kulipa lazima ubadilishe hali ya ingia mpya (muhimu)

JWT inabeba tamko la usajili (akaunti ya pending ni `NONE`). **Malipo yalipofika hubadilisha tu database, haibadilishi JWT iliyotolewa tayari** — tamko la token ya zamani bado ni NONE, ukitumia moja kwa moja kutengeneza kiungo cha ingia utaonekana "hana usajili".
Kwa hiyo skill baada ya kuthibitisha `paid` / PayPal `ACTIVE` kwanza inaendesha `refresh-login` (ingia tena kubadilisha JWT mpya, tamko hubadilika kuwa ACTIVE), kisha itengeneze kiungo 2. Hii ni tabia ya muundo, sio marekebisho ya ufa.

## Njia ya Usajili wa PayPal (inashughulikiwa na agent; wavuti, sio HarmonyOS)

Kuna mpango mmoja tu, Premium Monthly (takriban $1/mwezi, kama inavyorudishwa na `GET /api/subscription/plans`); **inashamiri otomatiki kila mwezi**
na mtumiaji anaweza kubatilisha wakati wowote katika akaunti yake ya PayPal.

### Mkataba wa API (umeshikwa tayari na hati ya skill; agent haijengi maombi moja kwa moja)

| Endpoint | Method | Maelezo |
|---|---|---|
| `/api/subscription/plans` | GET | Bearer auth; inarudisha orodha ya mipango inayopatikana (kwa sasa 1 tu) |
| `/api/subscription/create` | POST | Mwili `{planId}` → inarudisha `{subscriptionId, approveUrl, status}`; `status` kwa kawaida ni `APPROVAL_PENDING` |
| `/api/subscription/create` | GET | Bearer auth; inarudisha `{activeSubscription, allSubscriptions}`; agent hupima `activeSubscription.subscription.status === 'ACTIVE'` |
| `/api/subscription/verify` | POST | Ukurasa wa mafanikio unaita kiotomatiki (kwa cookie); inawezesha moja kwa moja kupitia API ya PayPal wakati webhook haijafika |
| `/subscription/success` | Ukurasa wa kurudi wa kivinjari | Ukurasa wa kutua baada ya uidhinishaji wa PayPal; hupima verify kiotomatiki, kisha inarudi kwenye ukurasa wa nyumbani / ukurasa wa awali |
| `/subscription/cancel` | Ukurasa wa kivinjari | Ukurasa wa kutua mtumiaji anapobatilisha au itashindwa; jaribio jipya linaweza kuanza |

### Mtiririko wa Agent

```
create-order --provider paypal   # → inarudisha approveUrl, huandikwa kwenye faili ya HTML ya ndani
open faili ya HTML               # → kivinjari kinaelekea ukurasa wa uidhinishaji wa PayPal
query (kila sekunde 10–15)        # → pima hadi ACTIVE
refresh-login                    # → badilisha JWT mpya (madai ya usajili ACTIVE)
login-link --target home         # → tengeneza kiungo rasmi cha kuingia
```

- Usajili wa PENDING ambao haujamalizika ndani ya saa 1, hufutwa kiotomatiki na backend; anza tu tena.
- Ikiwa mtumiaji anaendesha `create-order` tena, backend hutumia tena usajili uliopo wa `APPROVAL_PENDING`, huzuia 409.
- Sawa na Alipay: ufikiaji huwashesha tu DB — JWT ya zamani haibadilishwi kiotomatiki, kwa hiyo **lazima** uendeshe `refresh-login` kabla ya kutuma kiungo cha ukurasa wa nyumbani.

## Njia nne za ukurasa wa usajili wa malipo

Ukurasa wa usajili wa malipo `src/app/(public)/subscription/page.tsx` unaonyesha kulingana na mazingira ya kukimbia:

| Njia | Mazingira | Utaratibu | Njia ya uwezeshaji |
|---|---|---|---|
| **Alipay (kuu)** | Upande wa wavuti | `AlipayPaymentSection` hupitia kiolesura cha vibepay (jedwali la juu) | notify inawezesha upande wa seva kiotomatiki, sekunde chache |
| Usajili wa PayPal | Upande wa wavuti (siyo Harmony) | `/api/subscription/create` → inaelekea idhini ya PayPal; ununuzi wa kila mwezi unaoshirikiana unaweza kufutwa wakati wowote (`/api/subscription/manage`) | PayPal Webhook (`BILLING.SUBSCRIPTION.*`) inaweka active kiotomatiki |
| Usajili wa usome msimbo wa WeChat | Upande wa wavuti (siyo Harmony) | "微信扫码订阅" (usajili wa usome msimbo wa WeChat) chini ya ukurasa: soma msimbo uhamishe pesa | **uthibitisho wa mtu**, malipo yanaweza kuchelewa; usipofanikiwa usihukumu upesi |
| Ununuzi wa ndani wa Huawei | Ndani ya programu ya Harmony | Asili `NativeBridge.purchaseSubscription()` | `/api/subscription/activate-huawei` inathibitisha agizo la Huawei kisha inawezesha |

Mpango na bei ya PayPal zinatolewa kutoka `/api/subscription/plans` kwa dynamic; ujumbe wa kudumu wa ukurasa: Auto-renews. Cancel anytime.

## Hali na uelekezaji

- Baada ya Alipay kulipa → ukurasa wa kurudi unaonyesha mafanikio; PayPal inapofanikiwa → `/subscription/success` → akaunti active →
  inaelekezwa moja kwa moja kwenye ukurasa wa asili uliotajwa na `next` (usipokuwa ukurasa wa nyumbani).
- Mtumiaji aliyejiunga tayari akifika ukurasa wa usajili wa malipo → inaonyesha "You're All Set!", baada ya sekunde 3 inarudi ukurasa wa nyumbani kiotomatiki.
- Malipo yameshindwa/kufutwa (PayPal) → `/subscription/cancel`, inaweza kuanzisha tena.

## Utatuzi

| Tukio | Shughulikia |
|---|---|
| Alipay imeilipa `query` bado ni pending | notify inachelewa sana mara chache; subiri sekunde 30 kisha hoji tena. Bado isipofanya mruhusu mtumiaji arudi kivinjari aone hali ya ukurasa wa kurudi, bado isipofanya wasiliana na usaidizi wa jukwaa (dongtao@outlook.com), toa `outTradeNo` |
| Alipay imeilipa, kiungo 2 kinaingia bado kinazuiliwa | Imepungukiwa `refresh-login` (tamko la JWT ya zamani halijasasishwa) — kwanza `refresh-login` kisha `login-link` |
| PayPal `query` inabaki PENDING | Mtumiaji labda hajakamilisha uidhinishaji kwenye PayPal; hakikisha kiungo cha uidhinishaji kimefunguliwa kwenye kivinjari. Ikiwa bado ni PENDING baada ya uidhinishaji, webhook inaweza kuchelewa — mwongo mtumiaji asubiri sekunde chache kwenye ukurasa wa mafanikio au arekebishe |
| PayPal `query` inarudisha 409 | Tayari kuna usajili wa PayPal usio malizika; subiri saa 1 upite, au kamilisha uidhinishaji wa zamani kwenye kivinjari |
| PayPal imeilipa lakini Link 2 bado inazuiliwa | Sawa na Alipay: kwanza `refresh-login`, kisha `login-link` |
| Bado 403 baada ya kulipa (PayPal) | Webhook wakati mwingine inachelewa, ingia tena usishe hali |
| WeChat imeilipa bila ya kuwezesha | Uthibitisho wa mtu ni asynchronous, ndani ya masaa machache bado isipoweza kuwezesha wasiliana na usaidizi wa jukwaa |
| Ukurasa wa usajili wa malipo unaonyesha "No subscription plans available" | `/api/subscription/plans` haina mpango wowote wa PayPal unao patikana, ni tatizo la usanidi wa upande wa jukwaa; watumiaji wa China badilisha kwenda Alipay tu |

## Maelezo ya kihistoria

Katika msimbo kuna seti nyingine ya **zamani** ya malipo ya wavuti ya Alipay (`src/lib/alipay.ts`, `/api/payment/create-order`,
¥9.90/¥99 ununuzi wa mara moja, wakati wa sandbox bila ufunguo imewekwa inashuka kuwa malipo ya kuiga), haijawahi kuunganishwa kwenye sehemu ya UI ya ukurasa wa usajili wa malipo, hairuhusiwi na vibepay. Skill haiigusi kamwe; `alipay-vibepay.ts` ndiyo njia ya sasa inayotumika.
