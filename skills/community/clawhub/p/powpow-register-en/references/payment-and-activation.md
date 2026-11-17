# Subscription Activation and Payment — powpow-register

## Conclusion (the answer first)
> **Free testing period (starting 2026-10-18; actual platform behavior prevails)**: during this period a registered account can use every feature directly, and **subscribing is an optional upgrade rather than a requirement** — only follow this file's flow when the user actively wants membership. When the testing period ends, unsubscribed accounts visiting content pages will be redirected to the subscription page; just complete the subscription per this file.


**Both Alipay and PayPal subscriptions can now be handled by the agent — order creation and arrival tracking included.**
Alipay is a one-time purchase with no auto-renewal, for mainland-China users and users with Alipay; PayPal auto-renews monthly and can be cancelled anytime,
for overseas users and users without Alipay. WeChat QR code (manual confirmation) and Huawei IAP remain available, but the skill doesn't handle them.

Responsibility boundary for the payment step: the agent may **create orders, open the cashier, and query arrival**; it **never** touches the user's Alipay/PayPal
account/payment credentials and never promises to "pay on their behalf". The payment action is always completed by the user in person at the official cashier.

## Alipay Channel (vibepay, primary)

One-time purchase model: pay once to unlock the corresponding duration, **no auto-renewal**. Plans are hard-coded in
`src/lib/alipay-vibepay.ts` (`ALIPAY_PACKAGES`):

| key | planId | Name | Price | Duration |
|---|---|---|---|---|
| `monthly` | alipay-monthly | Monthly membership | ¥6.99 | 30 days |
| `quarterly` | alipay-quarterly | Quarterly membership | ¥19.99 | 90 days |
| `yearly` | alipay-yearly | Yearly membership | ¥69.99 | 365 days |

### API Contract (already wrapped by the skill script; the agent never assembles requests directly)

| Endpoint | Method | Notes |
|---|---|---|
| `/api/payment/alipay/create-order` | POST | Requires `Authorization: Bearer <JWT>` (pending users are fine). Body `{package}` → returns `{paymentHtml, outTradeNo, amount, planName}`; `paymentHtml` is a form page that auto-submits to the Alipay gateway |
| `/api/payment/alipay/query` | GET `?outTradeNo=` | Same Bearer auth. Returns `paid` / `pending` / `closed` / `unknown` |
| `/api/payment/alipay/notify` | POST (Alipay server callback) | Verifies five elements (signature, app_id, amount match, TRADE_SUCCESS/TRADE_FINISHED, merchant uniqueness) → **idempotently** updates the order + creates the subscription + activates the account. The skill never touches this endpoint |
| `/payment/alipay/return` | Browser return page | Public path; shows the "Payment successful" confirmation after paying, polls the backend for the real status |

- Unpaid orders **auto-close after 2 hours**; if the user abandons midway → just `create-order` again, the old order can be ignored.
- The script writes `paymentHtml` into a temporary HTML file; the agent opens it with a system command to reach the Alipay cashier
  (pay by scanning the QR code or logging into Alipay).

### Activation Chain (automatic, no human step)

notify passes verification → `paymentOrders` marked paid → `user_subscriptions` created/extended
(`planId`, `currentPeriodEnd` computed from durationDays; renewals extend from the original expiry date) →
`users.accountStatus: active` + `subscriptionStatus: ACTIVE` → the return page polls until paid and shows success.

### A Fresh Login State Is Required After Payment (important)

The JWT carries the subscription claim (`NONE` for a pending account). **Payment arrival only updates the database — it does not modify an
already-issued JWT** — the old token's claim is still NONE, and generating a login link with it looks like "no membership".
So after confirming `paid` / PayPal `ACTIVE`, the skill first runs `refresh-login` (logs in again for a new JWT with the ACTIVE claim),
then generates Link 2. This is by design, not a bug fix.

## PayPal Subscription Channel (handled by the agent; web, non-HarmonyOS)

There is only one plan, Premium Monthly (about $1/month, as returned by `/api/subscription/plans`); it **auto-renews monthly**
and the user can cancel anytime in their PayPal account.

### API Contract (already wrapped by the skill script; the agent never assembles requests directly)

| Endpoint | Method | Notes |
|---|---|---|
| `/api/subscription/plans` | GET | Bearer auth; returns the list of available plans (currently only 1) |
| `/api/subscription/create` | POST | Body `{planId}` → returns `{subscriptionId, approveUrl, status}`; `status` is usually `APPROVAL_PENDING` |
| `/api/subscription/create` | GET | Bearer auth; returns `{activeSubscription, allSubscriptions}`; the agent polls `activeSubscription.subscription.status === 'ACTIVE'` |
| `/api/subscription/verify` | POST | Called automatically by the success page (with the cookie); activates through the PayPal API directly when the webhook hasn't arrived |
| `/subscription/success` | Browser return page | Landing page after PayPal authorization; polls verify automatically, then returns to the home page / original page |
| `/subscription/cancel` | Browser page | Landing page when the user cancels or it fails; a new attempt can be started |

### Agent Flow

```
create-order --provider paypal   # → returns approveUrl, written into a local HTML file
open the HTML file               # → the browser jumps to the PayPal authorization page
query (every 10–15s)             # → poll until ACTIVE
refresh-login                    # → exchange for a new JWT (subscription claim ACTIVE)
login-link --target home         # → generate the formal login link
```

- PENDING subscriptions that aren't finished within 1 hour are cleaned up automatically by the backend; just start over.
- If the user runs `create-order` again, the backend reuses the still-valid `APPROVAL_PENDING` subscription, avoiding a 409.
- Same as Alipay: arrival only updates the DB — an old JWT is not refreshed automatically, so you **must** run `refresh-login` before sending the home-page link.

## The Four Channels on the Subscription Page

The subscription page `src/app/(public)/subscription/page.tsx` shows channels based on the runtime environment:

| Channel | Environment | Mechanism | Activation |
|---|---|---|---|
| **Alipay (primary)** | Web | `AlipayPaymentSection` goes through the vibepay endpoints (table above) | notify activates automatically server-side, within seconds |
| PayPal subscription | Web (non-HarmonyOS) | `/api/subscription/create` → redirect to PayPal for authorization; auto-renews monthly, cancel anytime (`/api/subscription/manage`) | PayPal Webhook (`BILLING.SUBSCRIPTION.*`) automatically sets active |
| WeChat QR-code subscription | Web (non-HarmonyOS) | "Scan WeChat to subscribe" section at the bottom of the page: scan to transfer money | **Manual confirmation**; the funds may arrive with a delay — don't rush to call it a failure right after the user pays |
| Huawei in-app purchase | Inside the HarmonyOS App | Native `NativeBridge.purchaseSubscription()` | `/api/subscription/activate-huawei` verifies the Huawei order and then activates |

PayPal plans and prices are read dynamically from `/api/subscription/plans`; the page's fixed copy reads: Auto-renews. Cancel anytime.

## Status and Redirects

- Alipay payment complete → the return page shows success; PayPal success → `/subscription/success` → account active →
  auto-return to the original page specified by the `next` parameter (home page if none).
- An already-subscribed user visiting the subscription page → shows "You're All Set!", auto-returns to home after 3 seconds.
- Payment failure/cancellation (PayPal) → `/subscription/cancel`, a new attempt can be started.

## Troubleshooting

| Symptom | Handling |
|---|---|
| Alipay paid but `query` still pending | notify is rarely delayed; wait 30 seconds and query again. If it still fails, have the user check the return page status in the browser; if that fails too, contact platform support (dongtao@outlook.com) with the `outTradeNo` |
| Alipay paid, but Link 2 still gets walled | `refresh-login` was skipped (the old JWT claim wasn't updated) — run `refresh-login` first, then `login-link` |
| PayPal `query` stays PENDING | The user hasn't finished authorization in PayPal; confirm the authorization link was opened in the browser. If it's still PENDING after authorizing, the webhook may be delayed — have the user wait a few more seconds on the success page or refresh |
| PayPal `query` returns 409 | There is already an unfinished PENDING subscription; wait 1 hour for it to expire, or complete the authorization of the old link in the browser |
| PayPal paid, but Link 2 still gets walled | Same as Alipay: run `refresh-login` first, then `login-link` |
| Still 403 after paying (PayPal) | The Webhook is occasionally delayed; log in again to refresh the status |
| Paid via WeChat but not activated | Manual confirmation is asynchronous; if it hasn't been activated within a few hours, contact platform support |
| Subscription page shows "No subscription plans available" | No usable PayPal plans on `/api/subscription/plans` — a platform-side configuration issue; mainland-China users can use Alipay instead |

## Historical Note

The codebase also contains an **older** Alipay web payment (`src/lib/alipay.ts`, `/api/payment/create-order`,
¥9.90/¥99 one-time purchase, auto-degrades to mock payment when the sandbox key is unset) that was never wired into the
subscription page UI and is unrelated to vibepay. The skill never touches it; `alipay-vibepay.ts` is the live channel.
