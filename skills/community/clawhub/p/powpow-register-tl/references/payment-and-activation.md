# Activation ng subscription at bayad — powpow-register

## Konklusyon (sagot muna)
> **Libreng panahon ng pagsubok (simula 2026-10-18; ang aktwal na pag-uugali ng platform ang masusunod)**: sa panahong ito ang rehistradong account ay maaaring gamitin ang lahat ng feature diretso, at **ang pag-subscribe ay opsyonal na upgrade hindi requirement** — sundin lamang ang daloy ng file na ito kapag nais ng user ng membership. Kapag tapos na ang panahon ng pagsubok, ang mga account na walang subscription na bumibisita sa content page ay ire-redirect sa subscription page; kumpletuhin lang ang subscription ayon sa file na ito.


**Ang Alipay at PayPal subscription ay parehong kayang hawakan ng agent para sa paggawa ng order at pagsubaybay sa pagdating ng bayad.**
Ang Alipay ay one-time purchase na hindi auto-renew, para sa mainland/may Alipay na gumagamit; ang PayPal ay buwanang auto-renew na maaaring kanselahin anumang oras, para sa ibang bansa/walang Alipay. Ang WeChat QR (manual confirmation) at Huawei IAP ay nananatili, ngunit hindi ina-asikaso ng skill.

Hangganan ng responsibilidad sa bahagi ng bayad: ang agent ay maaaring **gumawa ng order, buksan ang cashier, tingnan ang pagdating ng bayad**; **huwag kailanman** hawakan ang Alipay/PayPal
account/payment credentials ng gumagamit, huwag kailanman mangako ng "pagbabayad para sa kanya". Ang pagbabayad ay palaging ginagawa mismo ng gumagamit sa opisyal na cashier.

## Alipay channel (vibepay, pangunahi)

One-time purchase system: magbayad nang isang beses para sa kaukulang tagal, **hindi auto-renew**. Naka-hardcode ang mga package sa
`src/lib/alipay-vibepay.ts` (`ALIPAY_PACKAGES`):

| key | planId | Pangalan | Presyo | Tagal |
|---|---|---|---|---|
| `monthly` | alipay-monthly | Buwanang membership | ¥6.99 | 30 araw |
| `quarterly` | alipay-quarterly | Tatlong-buwang membership | ¥19.99 | 90 araw |
| `yearly` | alipay-yearly | Taunang membership | ¥69.99 | 365 araw |

### API contract (naka-encapsulate na sa skill script, hindi direktang nagbubuo ng request ang agent)

| Endpoint | Method | Paglalarawan |
|---|---|---|
| `/api/payment/alipay/create-order` | POST | Nangangailangan ng `Authorization: Bearer <JWT>` (sapat na ang pending user). body `{package}` → nagbabalik ng `{paymentHtml, outTradeNo, amount, planName}`; ang `paymentHtml` ay form page na awtomatikong nagse-submit sa Alipay gateway |
| `/api/payment/alipay/query` | GET `?outTradeNo=` | Bearer auth din. Nagbabalik ng `paid` / `pending` / `closed` / `unknown` |
| `/api/payment/alipay/notify` | POST (callback mula sa Alipay server) | Beripikasyon ng limang elemento ng signature (signature, app_id, katumbas na halaga, TRADE_SUCCESS/TRADE_FINISHED, uniqueness ng merchant) → **idempotent** na pag-update ng order + paggawa ng subscription + pag-activate ng account. Hindi kailanman gagalawin ng skill ang endpoint na ito |
| `/payment/alipay/return` | Browser return page | Pampublikong path; pagkatapos ng bayad ay ipinapakita ang 「支付成功」 (matagumpay na bayad) na kumpirmasyon, at nagpo-poll ang page sa totoong status ng back-end |

- Ang mga hindi pa nababayarang order ay **awtomatikong magsasara pagkatapos ng 2 oras**; kung tumigil ang gumagamit sa gitna → muling patakbuhin lang ang `create-order`, hindi na intindihin ang lumang order.
- Isinusulat ng script ang `paymentHtml` sa pansamantalang HTML file, at binubuksan ng agent gamit ang system command para makapasok sa Alipay cashier
  (mag-scan ng QR code o mag-log in sa Alipay para magbayad).

### Activation chain (awtomatiko, walang manual na gawain)

Matapos pumasa ang beripikasyon ng signature ng notify → mamamarkahang nabayaran ang `paymentOrders` → gagawa/magpapatuloy ang `user_subscriptions`
(`planId`, kinukwenta ang `currentPeriodEnd` ayon sa durationDays; sa pag-renew ay ipagpapatuloy mula sa orihinal na petsa ng pag-expire) →
`users.accountStatus: active` + `subscriptionStatus: ACTIVE` → kapag nakita ng return page ang paid, ipapakita ang success.

### Pagkatapos magbayad, kailangang palitan ang log-in status ng bago (mahalaga)

Nagdadala ang JWT ng subscription claim (para sa pending account ito ay `NONE`). **Ang pagdating ng bayad ay nag-a-update lang sa database, hindi nagbabago ng naibigay nang
JWT** — ang claim ng lumang token ay NONE pa rin; kung gagamitin ito nang direkta para gumawa ng log-in link, magiging "walang membership" ang dating.
Kaya ang skill, pagkatapos makumpirma ang `paid` / PayPal `ACTIVE`, ay patakbuhin muna ang `refresh-login` (mag-log in muli para sa bagong JWT, magiging ACTIVE ang claim),
bago gawin ang Link 2. Ito ay sadyang disenyo, hindi bug fix.

## PayPal subscription channel (agent-assisted; web, hindi HarmonyOS)

May iisang Premium Monthly plan lang (humigit-kumulang $1/buwan, ayon sa `/api/subscription/plans`), **buwanang auto-renew**,
maaaring kanselahin ng gumagamit anumang oras sa kanyang PayPal account.

### API contract (naka-encapsulate na sa skill script, hindi direktang nagbubuo ng request ang agent)

| Endpoint | Method | Paglalarawan |
|---|---|---|
| `/api/subscription/plans` | GET | Bearer auth; nagbabalik ng listahan ng available plans (kasalukuyang 1 lang) |
| `/api/subscription/create` | POST | body `{planId}` → nagbabalik ng `{subscriptionId, approveUrl, status}`; karaniwang `APPROVAL_PENDING` ang `status` |
| `/api/subscription/create` | GET | Bearer auth; nagbabalik ng `{activeSubscription, allSubscriptions}`; pine-poll ng agent ang `activeSubscription.subscription.status === 'ACTIVE'` |
| `/api/subscription/verify` | POST | awtomatikong tinatawag ng success page (kasama ang cookie); kapag hindi pa dumating ang webhook, direktang tinatawag ang PayPal API para i-activate |
| `/subscription/success` | Browser return page | landing page pagkatapos ng PayPal authorization; awtomatikong nire-poll ang verify; pagkatapos ay babalik sa home page / orihinal na page |
| `/subscription/cancel` | Browser page | landing page kapag kanselado o nabigo ang gumagamit; maaaring muling simulan |

### Daloy ng agent

```
create-order --provider paypal   # → nagbabalik ng approveUrl, isinusulat sa lokal na HTML file
buksan ang HTML file              # → dadako ang browser sa PayPal authorization page
query (kada 10–15s)               # → poll hanggang ACTIVE
refresh-login                     # → kumuha ng bagong JWT (ACTIVE subscription claim)
login-link --target home          # → gumawa ng opisyal na login link
```

- Ang PENDING subscription na hindi natapos sa loob ng 1 oras ay awtomatikong lilinisin ng backend; simulan lang muli.
- Kung muling patatakbuhin ng gumagamit ang `create-order`, gagamitin muli ng backend ang valid na `APPROVAL_PENDING` subscription, para iwas 409.
- Katulad ng Alipay: ang pagdating ng bayad ay nag-a-update lang sa DB — hindi awtomatikong nare-refresh ang lumang JWT, kaya **kailangang** patakbuhin muna ang `refresh-login` bago gumawa ng home page link.

## Apat na channel sa subscription page

Ipinapakita ng subscription page na `src/app/(public)/subscription/page.tsx` ayon sa running environment:

| Channel | Kapaligiran | Mekanismo | Paraan ng activation |
|---|---|---|---|
| **Alipay (pangunahi)** | Web | Ang `AlipayPaymentSection` ay gumagamit ng vibepay endpoint (talahanayan sa itaas) | Awtomatikong server-side activation sa pamamagitan ng notify, ilang segundo |
| PayPal subscription | Web (hindi Harmony) | `/api/subscription/create` → tumatalon sa PayPal authorization; buwanang auto-renew na maaaring kanselahin anumang oras (`/api/subscription/manage`) | Awtomatikong gagawing active ng PayPal Webhook (`BILLING.SUBSCRIPTION.*`) |
| 「微信扫码订阅」 (WeChat QR subscription) | Web (hindi Harmony) | 「微信扫码订阅」 sa ibaba ng page: mag-scan ng QR code para mag-transfer | **Manual na kumpirmasyon**, maaaring ma-delay ang pagdating ng bayad; huwag magmadaling maghukom na nabigo |
| Huawei in-app purchase | Sa loob ng Harmony app | Native `NativeBridge.purchaseSubscription()` | Bineripika ng `/api/subscription/activate-huawei` ang Huawei order bago i-activate |

Ang mga PayPal plan at presyo ay dinamikong binabasa mula sa `/api/subscription/plans`; nakatakdang text sa page: Auto-renews. Cancel anytime.

## Status at pag-redirect

- Pagkatapos magbayad sa Alipay → ipapakita ng return page ang success; kapag tagumpay sa PayPal → `/subscription/success` → magiging active ang account →
  awtomatikong babalik sa orihinal na page na tinutukoy ng `next` parameter (kung wala, home page).
- Kapag pumunta sa subscription page ang naka-subscribe na nang gumagamit → magpapakita ng "You're All Set!", at pagkatapos ng 3 segundo ay awtomatikong babalik sa home page.
- Nabigo/kanselado ang bayad (PayPal) → `/subscription/cancel`, maaaring muling simulan.

## Troubleshooting

| Sintomas | Paghawak |
|---|---|
| Pagkatapos magbayad sa Alipay, pending pa rin ang `query` | Bihirang ma-delay ang notify; maghintay ng 30 segundo at mag-query muli. Kung hindi pa rin, sabihan ang gumagamit na bumalik sa browser at tingnan ang status sa return page; kung hindi pa rin, kontakin ang platform support (dongtao@outlook.com) at ibigay ang `outTradeNo` |
| Pagkatapos magbayad sa Alipay, hinarang pa rin ng Link 2 | May nakaligtaang `refresh-login` (hindi na-update ang claim ng lumang JWT) — patakbuhin muna ang `refresh-login` bago ang `login-link` |
| PayPal `query` laging PENDING | Hindi pa natatapos ng gumagamit ang authorization sa PayPal; siguraduhing nabuksan ang authorization link sa browser. Kung PENDING pa rin pagkatapos mag-authorize, baka na-delay ang webhook — hayaang maghintay ang gumagamit ng ilang segundo sa success page o i-refresh |
| PayPal `query` nagbabalik ng 409 | May hindi pa natatapos na PENDING PayPal subscription; maghintay ng 1 oras para mag-expire, o tapusin ang lumang authorization sa browser |
| Nakabayad na sa PayPal ngunit hinarang pa rin ang Link 2 | Katulad ng Alipay: muna `refresh-login`, pagkatapos `login-link` |
| 403 pa rin pagkatapos magbayad (PayPal) | Minsan ma-delay ang Webhook; mag-log in muli para i-refresh ang status |
| Nagbayad sa WeChat ngunit hindi na-activate | Manual ang kumpirmasyon at asynchronous; kung hindi pa na-activate sa loob ng ilang oras, kontakin ang platform support |
| Nagpapakita ang subscription page ng "No subscription plans available" | Walang available na PayPal plan sa `/api/subscription/plans`, problema sa configuration sa gilid ng plataporma; para sa mga gumagamit sa China, lumipat lang sa Alipay |

## Makasaysayang tala

May isa pang **lumang** Alipay web payment sa code (`src/lib/alipay.ts`, `/api/payment/create-order`,
¥9.90/¥99 one-time purchase, bumabagsak sa simulated payment kapag walang naka-configure na sandbox key), ngunit hindi kailanman ikinonekta sa subscription page UI at walang kaugnayan sa vibepay.
Hindi ito gagalawin ng skill; ang `alipay-vibepay.ts` ang kasalukuyang gumaganang channel.
