# Subscription activation and payment — powpow-register

## Conclusion (di answer first)
> **Free testing period (starting 2026-10-18; di platform real behavior dey prevail)**: during dis period account wey don register fit use every feature directly, and **subscribing na optional upgrade no be requirement** — only follow dis file flow wen di user by imself want membership. Wen di testing period end, accounts wey no subscribe and visit content pages go dey redirect to di subscription page; just complete di subscription per dis file.


**Both Alipay and PayPal subscription fit now dey handle by di agent — order creation and money-landing tracking included.**
Alipay na one-time buy with no auto-renew, for mainland-China users and users wey get Alipay; PayPal dey auto-renew monthly and fit cancel any time, for overseas users and users wey no get Alipay. WeChat scan code (manual confirm) and Huawei IAP still dey available, but di skill no dey handle dem.

Di duty boundary for di payment part: agent fit **create order, open cashier, check money landing**; **never** touch di user Alipay/PayPal account/payment credential, never promise say "e go pay for am". Di payment action always na di user imsef go do am for di official cashier.

## Alipay channel (vibepay, main push)

One-time buy system: pay once to open di corresponding time, **e no dey auto-renew**. Di packages dey fixed inside `src/lib/alipay-vibepay.ts` (`ALIPAY_PACKAGES`):

| key | planId | Name | Price | Duration |
|---|---|---|---|---|
| `monthly` | alipay-monthly | Monthly member | ¥6.99 | 30 days |
| `quarterly` | alipay-quarterly | Quarterly member | ¥19.99 | 90 days |
| `yearly` | alipay-yearly | Yearly member | ¥69.99 | 365 days |

### Endpoint contract (di skill script don wrap dem already, agent no dey build request direct)

| Endpoint | Method | Explanation |
|---|---|---|
| `/api/payment/alipay/create-order` | POST | E need `Authorization: Bearer <JWT>` (pending user dey okay). body `{package}` → e return `{paymentHtml, outTradeNo, amount, planName}`; `paymentHtml` na di form page wey dey submit to di Alipay gateway automatic |
| `/api/payment/alipay/query` | GET `?outTradeNo=` | Same Bearer authentication. E return `paid` / `pending` / `closed` / `unknown` |
| `/api/payment/alipay/notify` | POST (Alipay server callback) | Check signature five elements (signature, app_id, amount match, TRADE_SUCCESS/TRADE_FINISHED, merchant uniqueness) → **idempotent** update order + build subscription + activate account. Skill never touch dis endpoint |
| `/payment/alipay/return` | Browser return page | Public path, after payment e show 支付成功 (payment success) confirmation, inside di page e dey poll di backend real status |

- Order wey no pay **go close automatic after 2 hours**; if user give up for middle → just run `create-order` again, no mind di old order.
- Di script write `paymentHtml` into temporary HTML file, agent use system command open am to enter di Alipay cashier (scan code or login inside Alipay to pay).

### Activation chain (automatic, no need human)

notify signature check pass → `paymentOrders` mark as paid → `user_subscriptions` build/extend (`planId`, `currentPeriodEnd` dem calculate am based on durationDays, renewal dey extend on top di original expiry date) → `users.accountStatus: active` + `subscriptionStatus: ACTIVE` → di return page poll until paid then e show success.

### After payment you must change to new login state (important)

Di JWT carry subscription claim inside (pending account na `NONE`). **When payment land e only update di database, e no go change di JWT wey dem don already issue** — di old token claim still be NONE, if you use am direct to generate login link e go behave like "no member". So di skill after e confirm `paid` / PayPal `ACTIVE` first run `refresh-login` (login again to change to new JWT, claim change to ACTIVE), then generate link 2. Na design behavior be dis, e no be vulnerability fix.

## PayPal Subscription Channel (agent dey handle am; web, no be HarmonyOS)

Na only one plan dey, Premium Monthly (about $1/month, as `GET /api/subscription/plans` go return am); it **dey auto-renew every month**
and di user fit cancel any time for im PayPal account.

### API Contract (di skill script done wrap am already; di agent no dey assemble request direct)

| Endpoint | Method | Notes |
|---|---|---|
| `/api/subscription/plans` | GET | Bearer auth; e return di list of available plans (right now na only 1) |
| `/api/subscription/create` | POST | Body `{planId}` → e return `{subscriptionId, approveUrl, status}`; `status` most times na `APPROVAL_PENDING` |
| `/api/subscription/create` | GET | Bearer auth; e return `{activeSubscription, allSubscriptions}`; di agent dey poll `activeSubscription.subscription.status === 'ACTIVE'` |
| `/api/subscription/verify` | POST | Di success page dey call am automatic (with di cookie); e activate direct through PayPal API when di webhook never reach |
| `/subscription/success` | Browser return page | Landing page after PayPal authorization; e dey poll verify automatic, then e go return to home page / original page |
| `/subscription/cancel` | Browser page | Landing page when di user cancel or e fail; new attempt fit start |

### Agent Flow

```
create-order --provider paypal   # → e return approveUrl, dem write am into local HTML file
open di HTML file                # → di browser go jump to PayPal authorization page
query (every 10–15s)             # → poll until ACTIVE
refresh-login                    # → exchange for new JWT (subscription claim ACTIVE)
login-link --target home         # → generate di formal login link
```

- PENDING subscriptions wey dem no finish within 1 hour, di backend go clean dem automatically; just start over.
- If di user run `create-order` again, di backend go reuse di still-valid `APPROVAL_PENDING` subscription, e avoid 409.
- Same as Alipay: arrival only update di DB — old JWT no dey refresh automatic, so you **must** run `refresh-login` before you send di home-page link.

## Subscription page four channels

Di subscription page `src/app/(public)/subscription/page.tsx` dey show based on di running environment:

| Channel | Environment | Mechanism | How e activate |
|---|---|---|---|
| **Alipay (main push)** | Web side | `AlipayPaymentSection` pass through vibepay endpoint (di table above) | notify server-side activate automatic, seconds level |
| PayPal subscription | Web side (no be Harmony) | `/api/subscription/create` → jump to PayPal authorization; monthly auto-renew fit cancel anytime (`/api/subscription/manage`) | PayPal Webhook (`BILLING.SUBSCRIPTION.*`) set active automatic |
| 微信扫码订阅 (WeChat scan code subscribe) | Web side (no be Harmony) | Page bottom 微信扫码订阅 (WeChat scan code subscribe): scan code transfer money | **Human confirm**, money fit land late; after payment no rush judge say e fail |
| Huawei in-app purchase | Inside Harmony App | Native `NativeBridge.purchaseSubscription()` | `/api/subscription/activate-huawei` verify di Huawei order then activate |

PayPal plans and prices dey read from `/api/subscription/plans` dynamic; di page fixed text: Auto-renews. Cancel anytime.

## Status and redirect

- Alipay payment finish → di return page show success; PayPal success → `/subscription/success` → account active → e jump back to di original page wey di `next` parameter point (if no dey, homepage).
- User wey don subscribe visit di subscription page again → e show "You're All Set!", after 3 seconds e go back to homepage automatic.
- Payment fail/cancel (PayPal) → `/subscription/cancel`, you fit start am again.

## Troubleshooting

| Wetin you see | How to handle am |
|---|---|
| Alipay pay finish `query` still pending | notify delay rare rare; wait 30 seconds then check again. If e still no work, make di user go back to browser check di return page status; if e still no work contact platform support (dongtao@outlook.com), report `outTradeNo` |
| Alipay pay finish, link 2 enter still dey block | You miss run `refresh-login` (old JWT claim no update) — first `refresh-login` then `login-link` |
| PayPal `query` stay PENDING | Di user never finish authorization for PayPal; confirm say di authorization link open for browser. If e still dey PENDING after authorization, di webhook fit delay — make di user wait some seconds for di success page or refresh |
| PayPal `query` return 409 | Dem get unfinished PENDING subscription already; wait 1 hour for am to expire, or complete di old authorization for browser |
| PayPal pay finish but Link 2 still get wall | Same as Alipay: first run `refresh-login`, then `login-link` |
| Pay finish still 403 (PayPal) | Webhook sometimes get delay, login again to refresh di status |
| WeChat pay but e no activate | Human confirmation na asynchronous, if e no activate within few hours then contact platform support |
| Subscription page show "No subscription plans available" | `/api/subscription/plans` no get available PayPal plan, na platform side configuration problem; China users just switch to Alipay |

## History note

Inside di code still get one **old** Alipay web payment (`src/lib/alipay.ts`, `/api/payment/create-order`, ¥9.90/¥99 one-time buy, when sandbox no configure key e degrade to mock payment), dem never connect am to di subscription page UI at all, e no relate to vibepay. Skill no dey touch am at all; `alipay-vibepay.ts` na di current channel.
