# Kunna membanci da biya — powpow-register

## Ƙarshe (amsa da farko)
> **Lokacin gwaji kyauta (tun daga 2026-10-18; halayen yanar gizo na gaske ya fi)**: a wannan lokaci asusu da aka yi rajista zai iya amfani da dukkan fannoni kai tsaye, kuma **yi rajista kari ne na zabi ba wajibi ba** — bi jawardar wannan fayil kawai sa'adda mai amfani da kansa ya so mamba. Sa'adda lokacin gwaji ya kare, asusun da ba su yi rajista ba za a mayar da su zuwa shafin biya sa'adda suka shiga shafukan abun ciki; kammala rajista bisa wannan fayil.


**Hanyoyin Alipay da PayPal duka yanzu agent za ta iya kula da su — ƙirƙirar oda da bin diddigin shigar kuɗi sun haɗa.**
Alipay biya sau ɗaya ne ba ya sabunta kansa, ga masu amfani na China da waɗanda ke da Alipay; PayPal na sabunta kansa kowace wata kuma ana iya soke shi kowane lokaci,
ga mai amfani na ƙasashen waje da waɗanda ba su da Alipay. Siffanta lambar QR ta WeChat (tabbatarwa ta hannu) da Huawei IAP har yanzu suna nan, amma skill ba ta aikatawa ba.

Iyakar aiki na ɓangaren biya: agent za ta iya **ƙirƙirar oda, buɗe cashier, duba shigar kuɗi**; **kada ta taba** asusun Alipay/PayPal na mai amfani/takaddun biya, kada ta taɓa alkawari 'biya a madadinsa'. Aikin biya koyaushe mai amfani da kansa yana yi a cashier na hukuma.

## Hanyar Alipay (vibepay, babbar)

Tsarin biya sau ɗaya: ka biya sau ɗaya ka kunna lokacin da ya dace, **ba ya sabunta kansa da kai**. Shirye-shirye an ƙuntata su a
`src/lib/alipay-vibepay.ts` (`ALIPAY_PACKAGES`):

| key | planId | Suna | Farashi | Lokaci |
|---|---|---|---|---|
| `monthly` | alipay-monthly | Membanci na wata | ¥6.99 | kwanaki 30 |
| `quarterly` | alipay-quarterly | Membanci na kwata | ¥19.99 | kwanaki 90 |
| `yearly` | alipay-yearly | Membanci na shekara | ¥69.99 | kwanaki 365 |

### Kwangilar tashoshi (script ɗin skill ya riga ya ƙunsa, agent ba ta gina buƙata kai tsaye ba)

| Tasha | Hanya | Bayani |
|---|---|---|
| `/api/payment/alipay/create-order` | POST | Tana buƙatar `Authorization: Bearer <JWT>` (mai amfani na pending ya isa). jiki `{package}` → tana dawo da `{paymentHtml, outTradeNo, amount, planName}`; `paymentHtml` shafi ne na fom mai tura kai tsaye ga ƙofar Alipay |
| `/api/payment/alipay/query` | GET `?outTradeNo=` | Hakika tabbatarwa ta Bearer. Tana dawo da `paid` / `pending` / `closed` / `unknown` |
| `/api/payment/alipay/notify` | POST (kiran uwar garwa ta Alipay) | Tabbatar da saitti na abubuwa biyar (saitti, app_id, adadin kuɗin yayi daidai, TRADE_SUCCESS/TRADE_FINISHED, keɓaɓɓun ma'aikaci) → **idempotent** sabunta oda + gina membanci + kunna asusu. Skill kada ta taba wannan tasha |
| `/payment/alipay/return` | Shafin dawowa na burauza | Hanya ce ta jama'a, bayan biya tana nuna tabbacin "支付成功" (biyan ya yi nasara), shafin yana sake duba halin gaske na ɓangaren baya |

- Oda da ba a biya ba **tana rufewa da kai bayan sa'o'i 2**; mai amfani ya bar a tsakanin → ka sake `create-order` kai tsaye, tsohon oda ba buƙatar damuwa.
- Script ɗin yana rubuta `paymentHtml` a cikin fayil ɗin HTML na wucin gadi, agent ta yi amfani da umarnin tsarin ta buɗe shi ta shiga cashier na Alipay
  (siffanta lambar QR ko shiga cikin Alipay ya biya).

### Hanyar kunnawa (ta kai, ba buƙatar hannu)

notify tabbatar da saitti ta wuce → `paymentOrders` alamta an biya → `user_subscriptions` gina/cigaba
(`planId`, `currentPeriodEnd` ana ƙidaya bisa durationDays, sabunta membanci na cigabawa a kan ranar ƙarewa ta asali) →
`users.accountStatus: active` + `subscriptionStatus: ACTIVE` → shafin dawowa yana sake duba har paid yana nuna nasara.

### Bayan biya dole ne a musanya halin shiga sabuwa (mai mahimmanci)

JWT na ɗauke da da'awar membanci (asusun pending `NONE`). **Shigar kuɗin kawai na sabunta ma'ajiyar bayanai, ba ta canza JWT da aka riga aka bayar ba** — da'awar token ɗin da ya gabata har yanzu NONE, idan ka yi amfani da ita kai tsaye ka ƙirƙiri mahaɗin shiga zai bayyana "ba memba ba".
Saboda haka skill bayan tabbatar da `paid` / PayPal `ACTIVE` da farko na gudanar da `refresh-login` (sake shiga musanya JWT sabuwa, da'awar na canzawa zuwa ACTIVE),
sannan ta ƙirƙiri mahaɗi na 2. Wannan halin zane ne, ba gyaran rami ba.

## Hanyar membanci ta PayPal (agent tana kula da ita; yanar gizo, ba HarmonyOS ba)

Shiri ɗaya ne kawai, Premium Monthly (kusan $1/wata, kamar yadda `/api/subscription/plans` ya dawo); **yana sabunta kansa kowace wata**
kuma mai amfani na iya soke shi kowane lokaci a cikin asusun PayPal ɗinsa.

### Kwangilar API (an riga an naɗe ta a cikin script ɗin skill; agent kada ta haɗa buƙatu da kanta)

| Ƙarshen hanya | Hanya | Bayani |
|---|---|---|
| `/api/subscription/plans` | GET | Tabbatar da Bearer; yana dawo da jerin shirye-shirye da ake da su (yanzu 1 kawai) |
| `/api/subscription/create` | POST | Jiki `{planId}` → yana dawo da `{subscriptionId, approveUrl, status}`; `status` yawanci `APPROVAL_PENDING` ne |
| `/api/subscription/create` | GET | Tabbatar da Bearer; yana dawo da `{activeSubscription, allSubscriptions}`; agent na duba `activeSubscription.subscription.status === 'ACTIVE'` |
| `/api/subscription/verify` | POST | Shafin nasara na kira shi da kai (tare da cookie); yana kunnawa ta API na PayPal kai tsaye idan webhook bai iso ba |
| `/subscription/success` | Shafin dawowar burauza | Shafin sauka bayan izinin PayPal; yana duba verify da kai, sannan ya koma shafin gida / shafin asali |
| `/subscription/cancel` | Shafin burauza | Shafin sauka idan mai amfani ya soke ko ya gaza; ana iya fara sabon yunƙuri |

### Tsarin agent

```
create-order --provider paypal   # → yana dawo da approveUrl, an rubuta shi cikin fayil HTML na gida
open the HTML file               # → burauza ta koma shafin izinin PayPal
query (kowace daƙiƙa 10–15)      # → duba har sai ACTIVE
refresh-login                    # → musanya JWT sabuwa (da'awar membanci ACTIVE)
login-link --target home         # → ƙirƙiri mahaɗin shiga na hukuma
```

- Membancin PENDING da ba a kammala shi cikin sa'a 1 ba, ɓangaren baya na share shi da kai; ka sake farawa.
- Idan mai amfani ya sake gudanar da `create-order`, ɓangaren baya na sake amfani da membancin `APPROVAL_PENDING` da ke nan daram, yana guje wa 409.
- Kamar Alipay: shigar kuɗi yana sabunta DB ne kawai — tsohon JWT ba ya sabunta da kai, saboda haka **dole** ka gudanar da `refresh-login` kafin ka aika mahaɗin shafin gida.

## Hanyoyi huɗu na shafin membanci

Shafin membanci `src/app/(public)/subscription/page.tsx` yana nuna bisa yanayin aiki:

| Hanya | Yanayi | Tsari | Hanyar kunnawa |
|---|---|---|---|
| **Alipay (babbar)** | ɓangaren yanar gizo | `AlipayPaymentSection` tana bi ta tashar vibepay (teburin sama) | notify uwar garwa tana kunna ta kai, daƙiƙa kaɗan |
| Membancin PayPal | ɓangaren yanar gizo (ba Harmony ba) | `/api/subscription/create` → turawa izinin PayPal; biyan kowane wata na sabunta kansa za a iya soke a kowane lokaci (`/api/subscription/manage`) | PayPal Webhook (`BILLING.SUBSCRIPTION.*`) tana saka active ta kai |
| Membancin siffanta lambar QR ta WeChat | ɓangaren yanar gizo (ba Harmony ba) | ƙarshen shafi "微信扫码订阅" (membancin siffanta lambar QR ta WeChat): siffanta lambar turawa kuɗi | **tabbatarwa ta hannu**, kuɗi na iya yin jinkiri; bayan biya kada ka yanke hukunci da wuri |
| Siye na ciki na Huawei | a cikin manhaja ta Harmony | na asali `NativeBridge.purchaseSubscription()` | `/api/subscription/activate-huawei` tabbatar da oda Huawei sannan ta kunna |

Shirye-shirye da farashin PayPal ana karanta su daga `/api/subscription/plans` bisa canji; rubutun dauri na shafi: Auto-renews. Cancel anytime.

## Hali da turawa

- Alipay bayan biya → shafin dawowa yana nuna nasara; PayPal ta yi nasara → `/subscription/success` → asusu active →
  turawa ta kai ga shafin asali da `next` ya nuna (babu shi to shafin gida).
- Mai amfani da ya riga ya yi membanci idan ya koma shafin membanci → yana nuna "You're All Set!", bayan daƙiƙa 3 yana dawowa shafin gida ta kai.
- Biya ta gaza/an soke (PayPal) → `/subscription/cancel`, za a iya farawa sake.

## Bincike

| Alama | Yadda ake kula |
|---|---|
| Alipay bayan biya `query` har yanzu pending | notify na yin jinkiri kaɗan ne; ka jira daƙiƙa 30 sannan ka sake duba. Har yanzu bai yi ka tambayi mai amfani ya koma burauza ya duba halin shafin dawowa, har yanzu bai yi ka tuntubi taimakon dandalin (dongtao@outlook.com), ka ba da `outTradeNo` |
| Alipay ta biya, mahaɗi na 2 ya shiga har yanzu ana toshi | An tsallake `refresh-login` (da'awar JWT ta da ba a sabunta ba) — ka fara `refresh-login` sannan `login-link` |
| PayPal `query` ya ci gaba da PENDING | Mai amfani bai kammala izini a PayPal ba; ka tabbatar an buɗe mahaɗin izini a burauza. Idan har yanzu PENDING bayan izini, webhook na iya yin jinkiri — ka bar mai amfani ya jira ƴan daƙiƙu a shafin nasara ko ya sabunta |
| PayPal `query` ya dawo da 409 | Akwai membancin PENDING da ba a kammala ba; ka jira sa'a 1 ya ƙare, ko ka kammala izinin tsohon mahaɗi a burauza |
| An biya ta PayPal, amma mahaɗi na 2 har yanzu ana toshi | Kamar Alipay: ka fara `refresh-login` sannan `login-link` |
| Bayan biya har yanzu 403 (PayPal) | Webhook wani lokaci na yin jinkiri, ka sake shiga ka sabunta hali |
| WeChat ta biya ba a kunna ba | Tabbatarwa ta hannu ce asynchronous, a cikin sa'o'i kaɗan idan ba a kunna ba sai ka tuntubi taimakon dandalin |
| Shafin membanci yana nuna "No subscription plans available" | `/api/subscription/plans` ba shi da shirin PayPal mai samuwa, matsala ce ta saitin ɓangaren dandalin; masu amfani na China su canza su bi Alipay kawai |

## Rubutun tarihi

A cikin code akwai wata tsarin **tsohuwar** biya ta yanar gizo ta Alipay (`src/lib/alipay.ts`, `/api/payment/create-order`,
¥9.90/¥99 biya sau ɗaya, lokacin sandbox ba a saita makullai ba tana faduwa zuwa biyar da ƙarya), ba ta taɓa haɗawa da UI ɗin shafin membanci ba, ba ta da alaƙa da vibepay.
Skill kada ta taba shi; `alipay-vibepay.ts` ne hanyar da ake amfani da ita a yanzu.
