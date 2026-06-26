---
name: paytm-integration
description: >
  Expert guide for integrating Paytm Payment Gateway APIs and SDKs into websites, mobile apps, and backend systems.
  Use this skill whenever the user is working with Paytm payments - including setting up the payment gateway,
  generating checksums, calling Initiate Transaction / Transaction Status APIs, integrating the JS
  Checkout, handling callbacks, generating payment links, generating dynamic QR codes, implementing
  UPI Autopay subscriptions, or troubleshooting Paytm PG errors. Trigger when the question contains
  Paytm-specific tokens: "Paytm", "paytmchecksum", "txnToken", "CHECKSUMHASH",
  "paytmpayments.com", "/theia/api/", "subscription/create", "/link/create", "paymentservices/qr",
  "WEBSTAGING", "NATIVE_SUBSCRIPTION", or any path under `paytmpayments.com/docs`.
  Do NOT trigger on generic PSP terms ("MID", "merchant key", "checksum", "PG integration") in
  isolation - those overlap with other payment gateways and would mis-trigger the skill.
  Also trigger when the user explicitly mentions they are a Paytm merchant or developer.
---

# Paytm Payment Gateway Integration Skill

## Overview

Paytm Payment Gateway supports UPI, Credit/Debit Cards, Net Banking, and EMI.
Supported integration variants in this skill: **JS Checkout** (web), **Subscriptions / UPI Autopay**, **Payment Links**, and **Dynamic QR Codes** - all backed by Server-to-Server APIs.

---

## Key Concepts

| Concept | Description |
|---|---|
| **MID** | Merchant ID - unique identifier for your Paytm account |
| **Merchant Key** | Secret key used to generate/verify checksums |
| **txnToken** | Short-lived token returned by Initiate Transaction API; used in all subsequent steps |
| **CHECKSUMHASH** | HMAC-SHA256 signature generated with Merchant Key to authenticate API calls |
| **ORDER_ID** | Unique merchant-generated identifier per transaction |
| **callbackUrl** | URL where Paytm POSTs transaction result after payment |

---

## Environments

| Environment | Base URL |
|---|---|
| Staging | `https://securestage.paytmpayments.com` |
| Production | `https://secure.paytmpayments.com` |

---

## Core Integration Flow

> ### ⚡ Pick the right flow FIRST (read before generating any code)
>
> Map the user's intent to one of the four flows before writing anything. Picking wrong produces code that "works" but solves the wrong problem - the most expensive class of bugs in this skill.
>
> | User says… | Flow | Endpoint | Needs JS Checkout? | Reference |
> |---|---|---|---|---|
> | "checkout page", "pay button on website", "one-time payment", "buy" | **Payment** | `POST /theia/api/v1/initiateTransaction` (`requestType: "Payment"`) | ✅ Yes | Steps below + `references/js-checkout.md` |
> | "subscription", "monthly", "weekly", "yearly", "recurring", "auto-debit", "autopay", "mandate", "renew every…", "membership", "plan" | **Subscription** | `POST /subscription/create` (`requestType: "NATIVE_SUBSCRIPTION"`) | ✅ Yes (for consent screen) | `references/subscriptions.md` ← **MUST READ** |
> | "shareable link", "invoice link", "payment link via SMS / WhatsApp / email" | **Payment Link** | `POST /link/create` (then `POST /link/fetchTransaction` to reconcile - NOT `/v3/order/status`) | ❌ No - Paytm hosts the page | `references/payment-links.md` |
> | "QR code", "scan to pay", "in-store", "counter", "table-side", "print QR" | **Dynamic QR** | `POST /paymentservices/qr/create` | ❌ No - render image, customer scans with their UPI app | `references/qr-codes.md` |
>
> **The steps below describe Payment + JS Checkout only.** Do NOT extrapolate them to the other three flows - they have different endpoints, different request shapes, different validators. Load the matching reference file and follow its flow.
>
> **Critical mistakes that keep recurring:**
> - **Subscription:** endpoint is `/subscription/create` on staging, `/theia/api/v1/subscription/create` on prod. `requestType: "NATIVE_SUBSCRIPTION"` (or `"NATIVE_MF_SIP"` for SIPs). `head` requires `clientId` + `channelId` + `signature`. Query params include a required `traceId`. Subscription fields are flat in `body` - no `subscriptionDetails` wrapper. Both `subscriptionFrequency` (number) and `subscriptionFrequencyUnit` (period) are required. **Safe defaults:** `subscriptionPaymentMode: "UNKNOWN"`, `txnAmount.value: "2.00"` (min for CC/DC), `subscriptionGraceDays: "3"` (max for CC/DC, **AND must be < cycle length** — drop/omit for daily/sub-3-day cycles else Paytm returns `4001`), `subscriptionStartDate` = today, `subscriptionEnableRetry: "0"` with `subscriptionRetryCount` omitted, no `renewalAmount`.
> - **Payment Link:** identifier in fetch / update / resend / expire calls is `linkId` as a **JSON number**, NOT a string. Resend path is `/link/resendNotification`, NOT `/link/resend`. **Field charsets differ:** `linkName` is alphanumerics ONLY (no spaces — several MIDs reject space as a special character despite the docs, returning `5007`); `linkDescription` is alphanumerics + spaces. Both ≥ 3 chars. Sanitize each field with its own regex on the server. **Status fields are dual-shape:** create/fetch responses return either `linkStatus: "ACTIVE"` (string) OR `isActive: true` (boolean) depending on MID — read defensively. **`/link/fetchTransaction` `orderStatus` is dual-shape too:** match BOTH `"SUCCESS"` AND `"TXN_SUCCESS"` for paid orders — hard-coding only `"TXN_SUCCESS"` silently misses every paid link on MIDs that return `"SUCCESS"`. Reconcile via `/link/fetchTransaction`, NOT `/v3/order/status`.
> - **Dynamic QR:** `posId` is **required** (skipping it returns 400). `amount` is a **string** with two decimals.

### Step 1 – Generate Checksum (Server-side)

Every API call requires a `CHECKSUMHASH` in the request header (as `signature`).

**Use Paytm's official checksum library** - available for Java, PHP, Python, Node.js, .NET, Go:
- Docs: `https://www.paytmpayments.com/docs/checksum/`
- GitHub: `https://github.com/Paytm-Payments`

```python
# Python example
from paytmchecksum import PaytmChecksum
checksum = PaytmChecksum.generateSignature(json.dumps(body), MERCHANT_KEY)
```

```java
// Java example
String checksum = PaytmChecksum.generateSignature(body.toString(), MERCHANT_KEY);
```

**Verify response checksum** (server-side, before trusting any payment response):
```python
is_valid = PaytmChecksum.verifySignature(response_body, MERCHANT_KEY, checksumhash)
```

---

### Step 2 – Initiate Transaction API

Called server-side to get a `txnToken` before rendering the payment UI.

**Endpoint:**
```
POST {BASE_URL}/theia/api/v1/initiateTransaction?mid={MID}&orderId={ORDER_ID}
```

**Request body for one-time payment** (all top-level body fields shown are required):
```json
{
  "head": { "signature": "<CHECKSUMHASH over JSON.stringify(body)>" },
  "body": {
    "requestType": "Payment",
    "mid": "YOUR_MID",
    "websiteName": "YOUR_WEBSITE_NAME",
    "orderId": "ORD_ABC123",
    "callbackUrl": "https://yoursite.com/paytm/callback",
    "txnAmount": { "value": "1.00", "currency": "INR" },
    "userInfo": { "custId": "CUST_001", "mobile": "9999999999", "email": "buyer@example.com" }
  }
}
```

> **Building a subscription / recurring charge?** Do NOT use this endpoint or this body. Subscriptions use a **different endpoint** (`/subscription/create`, with a `/theia/api/v1/` prefix on prod), a **different `requestType`** (`"NATIVE_SUBSCRIPTION"` or `"NATIVE_MF_SIP"`), an extra `traceId` query param, **`head.clientId` + `head.channelId`**, a required `subscriptionPaymentMode`, and **flat subscription fields inside `body`** (no `subscriptionDetails` wrapper). Full correct payload + field reference + error codes in `references/subscriptions.md` - read it before writing any code.

`websiteName` is per-MID (dashboard value, e.g. `DEFAULT`, `WEBSTAGING`, `retail`). `channelId` (`WEB`/`WAP`) and `industryTypeId` are usually inherited from the dashboard but can be overridden in the body. **Response:** `body.txnToken` - single-use, **15-min TTL**.

---

### Step 3 – Render Payment Page

**Web – JS Checkout** (browser-only - never paste into a Next.js / Remix / RSC server component; wrap in `"use client"` or guard with `typeof window !== "undefined"`):
```html
<script src="{pgDomain}/merchantpgpui/checkoutjs/merchants/{MID}.js"
        type="application/javascript" crossorigin="anonymous"></script>
<script>
  window.Paytm.CheckoutJS.onLoad(function () {
    window.Paytm.CheckoutJS.init({
      root: "",
      flow: "DEFAULT",
      data: {
        orderId: "ORD_ABC123",
        token: "<txnToken>",
        tokenType: "TXN_TOKEN",
        amount: "1.00"
      },
      merchant: { redirect: false },
      handler: {
        notifyMerchant: function (e, d) { console.log(e, d); },
        transactionStatus: function (d) { window.Paytm.CheckoutJS.close(); }
      }
    }).then(function () { window.Paytm.CheckoutJS.invoke(); });
  });
</script>
```
Full reference + alternative config shape in `references/js-checkout.md`. Working copy-paste page at `scripts/frontend/checkout.html`.

---

### Step 4 – Handle Callback

Paytm POSTs to your `callbackUrl` with:

```
ORDERID, MID, TXNID, TXNAMOUNT, PAYMENTMODE, STATUS, RESPCODE, RESPMSG, CHECKSUMHASH, ...
```

**Always verify `CHECKSUMHASH`** server-side before trusting the response.
**Never rely solely on callback** - confirm via Transaction Status API (step 5).

Key status values:
- `TXN_SUCCESS` - payment successful
- `TXN_FAILURE` - payment failed
- `PENDING` - awaiting bank confirmation

---

### Step 5 – Transaction Status API (mandatory verification)

```
POST {BASE_URL}/v3/order/status
Content-Type: application/json
```

```json
{
  "head": { "signature": "<CHECKSUMHASH over JSON.stringify(body)>" },
  "body": { "mid": "YOUR_MID", "orderId": "ORDERID_98765" }
}
```

Treat this response as the **final authoritative status**. Call it server-to-server, not from the browser.

> **⚠️ `/v3/order/status` is for one-time-payment / JS-Checkout flows ONLY.** For Payment Link reconciliation use **`/link/fetchTransaction`** instead - see `references/payment-links.md`. The two endpoints have different head shapes; carrying over fields between them causes checksum-mismatch errors.
>
> - **`/v3/order/status`** uses `head: { signature }` ONLY. Do NOT add `tokenType` (`"AES"`) or `timestamp` - Paytm rejects them or silently ignores them, leading to checksum mismatches that look unrelated.
> - **`/link/*`** (create / fetch / update / resendNotification / expire / **fetchTransaction**) all use `head: { tokenType: "AES", signature, timestamp? }`.
>
> If your flow mixes both (rare - typically you'd pick one path), build each request's `head` from scratch. Don't copy the link-API head into a Transaction Status call. Bad request observed in the wild:
>
> ```json
> // ❌ WRONG - extra tokenType + timestamp leak from the link API
> { "head": { "tokenType": "AES", "timestamp": "1777662548", "signature": "..." },
>   "body": { "mid": "...", "orderId": "..." } }
> ```
> ```json
> // ✅ CORRECT
> { "head": { "signature": "..." },
>   "body": { "mid": "...", "orderId": "..." } }
> ```

---

## Server SDKs

Paytm provides server-side kits that wrap all major APIs + checksum generation:

| Language | Install |
|---|---|
| Java | Maven: `com.paytm.pg:merchant-sdk` |
| PHP | Composer: `paytm/pg-php-sdk` |
| Python | `pip install paytmchecksum` |
| Node.js | `npm install paytmchecksum` |
| .NET | NuGet: `Paytm.Checksum` |

SDK docs: `https://www.paytmpayments.com/docs/server-sdk/`

---

## UPI Autopay / Subscriptions

For recurring payments use Paytm's Subscription (UPI Autopay) product. **Different endpoint, different requestType, different field placement from one-time Payment** - see `references/subscriptions.md` for the correct payload.

- Endpoint: `POST /subscription/create` (staging) / `POST /theia/api/v1/subscription/create` (production), with required query params `mid`, `orderId`, `traceId`.
- Body: `requestType: "NATIVE_SUBSCRIPTION"` (or `"NATIVE_MF_SIP"` for SIPs); subscription fields **flat inside `body`** (no `subscriptionDetails` wrapper); `subscriptionPaymentMode` + `subscriptionAmountType` + both `subscriptionFrequency` & `subscriptionFrequencyUnit` are required.
- Head: `clientId` + `channelId` + `signature` are all required.
- The returned `txnToken` is consumed by JS Checkout exactly like a one-time payment, where the user approves the mandate.
- Recurring debit / status / edit / cancel operations are **out of scope for this skill** - refer to live Paytm docs and validate paths before implementing.
- Full field reference, error codes, and worked example: `references/subscriptions.md`.

---

## Common API Response Codes

| RESPCODE | Meaning |
|---|---|
| 01 | Success |
| 227 | Checksum mismatch |
| 330 | Invalid order ID |
| 334 | Duplicate order ID |
| 400 | Bad request / missing params |
| 501 | System error (retry) |

---

## Getting Your MID and Merchant Key

Both are issued from the Paytm dashboard - staging works immediately, production needs KYC + activation.

- *Staging (test mode):* https://dashboard.paytmpayments.com/next/apikeys -> Generate now (under Test API Details)
- *Production (Live Mode):* https://dashboard.paytmpayments.com/next/apikeys -> Get Merchant ID, Merchant Key from Production API details.

  (Production keys are issued only after KYC + account activation. If the tab is empty, finish onboarding or contact your Paytm KAM.)

When generating setup instructions for users, **always include the two links above verbatim** - discovering the dashboard path is the #1 friction point.

## Test Credentials (Staging)

Use these in any staging integration so users can complete a full payment flow without leaving their IDE.

**Test cards (staging):**

| Use case | Card number | Expiry | CVV |
|---|---|---|---|
| One-time payment | `4111 1111 1111 1111` | any future date (MM/YY, e.g. `12/29`) | `123` |
| Subscription / mandate | `4761 3600 7586 3216` | any future date (MM/YY) | `123` |

**Test Net Banking:** pick any bank in the staging selector → simulator page → click *Success* / *Failure* to force the outcome.

**Test UPI:** supported only via the Paytm staging consumer app - not any production UPI app. The merchant requests the staging app build from their Paytm KAM / support, installs it on a test device, and uses it to scan staging QRs or open staging UPI intent links.

If your MID rejects the values above, the MID's Test API Details tab has merchant-specific overrides at <https://dashboard.paytmpayments.com/next/apikeys>.

---

## Quick Reference: API Endpoints

| API | Endpoint |
|---|---|
| Initiate Transaction | `POST /theia/api/v1/initiateTransaction` |
| Transaction Status | `POST /v3/order/status` |
| Create Subscription | `POST /subscription/create` |
| Create Payment Link | `POST /link/create` |
| Fetch Link Transactions | `POST /link/fetchTransaction` |
| Create Dynamic QR | `POST /paymentservices/qr/create` |

All endpoints prefixed with the environment base URL.

---

## Pitfalls (read before shipping)

1. **`websiteName`** must match the dashboard exactly. Wrong value typically makes `initiateTransaction` itself fail with `body.resultInfo.resultStatus = "F"` and a generic message; in some legacy MID configs it returns a token that then fails at the JS Checkout step. Either way, check the dashboard value first.
2. **`txnAmount.value` is a string with two decimals** (`"1.00"`). `1`, `1.0`, `1.000` break things.
3. **`orderId` is single-use even on failure.** Generate a new one for every retry. Charset: `[A-Za-z0-9_@-]`, ≤ 50 chars.
4. **`txnToken`** is single-use, 15-minute TTL. Don't cache or pre-fetch.
5. **Don't mix PG hosts.** Staging MID + prod host (or vice versa) returns confusing 401/checksum errors.
6. **Browser callback ≠ webhook.** Callback can be lost (popup blockers, network drop). Always reconfirm via Transaction Status API or the S2S webhook before fulfilling.
7. **Callback verification** uses sorted form params *minus* `CHECKSUMHASH` - different shape from API checksum, and field names are UPPERCASE.
8. **JSON bytes used to sign must equal bytes sent.** Don't re-serialize between hashing and POSTing.
9. **INR only** for domestic Paytm PG.
10. Popup blockers kill the modal flow on mobile; offer `merchant.redirect: true` as a fallback.
11. **Callback URL must be reachable from the user's browser AND match what your backend listens on.** The reference backends default to `http://localhost:{3001|5001|8080/paytm-backend}` - when scaffolding a multi-service project (e.g. Next.js frontend on `:3000` + separate backend), set `PAYTM_CALLBACK_BASE` (or `PAYTM_CALLBACK_URL`) to the *backend's* public URL, not the frontend's. Never hard-code `localhost` for production.
12. **Frontend `fetch` calls are browser-only.** The reference HTML uses `new URL("paytm/create-order", document.baseURI)` which deliberately fails fast in SSR (no `document`). When using Next.js / RSC, isolate Paytm calls in client components or behind `typeof window` guards.

Symptom-driven debugging: `references/troubleshooting.md`.

---

## Common Integration Bugs (and how to avoid them)

These are real bugs Claude has produced when scaffolding Paytm integrations from prompts. Internalize the fixes - don't regenerate the broken patterns.

### 1. Hard-coded absolute paths to external certs / files

**Symptom:** Project ships with `NODE_EXTRA_CA_CERTS=/Users/someone-else/certs/corp-proxy-ca.crt` (or similar) baked into `.env` or code. Works on author's machine, breaks on every other machine.
**Fix:** Use **project-relative paths** for any cert / keystore / file the project owns. Place the cert inside the project (e.g. `./certs/corp-proxy-ca.crt`) and reference it relatively. Document in the README that users behind a corporate proxy may need to point this at their local proxy's CA bundle.
**For Node:** `NODE_EXTRA_CA_CERTS=./certs/corp-proxy-ca.crt` in `.env`, loaded via `dotenv`.

### 2. `https://localhost` in callback / dev URLs

**Symptom:** `PAYTM_CALLBACK_URL=https://localhost:3001/paytm/callback` - Paytm POSTs the callback, browser blocks the redirect because there's no SSL on localhost. Payment "succeeds" silently with no callback.
**Fix:** Use `http://localhost:3001` for local dev. Reserve `https://` for deployed environments where TLS is real. The reference backends already default to `http://localhost:{port}` - don't override unless you've actually set up local SSL (mkcert, Caddy, etc.).

### 3. ❗ `CheckoutJS.onLoad()` wrapped inside a button click handler

**This is the most common Paytm bug Claude generates.** It looks correct but never fires.

**Broken pattern (do not generate):**
```javascript
button.addEventListener("click", function () {
  fetch("/paytm/create-order", ...)
    .then(function (data) {
      window.Paytm.CheckoutJS.onLoad(function () {        // ❌ already fired
        window.Paytm.CheckoutJS.init(config).then(...);
      });
    });
});
```
`CheckoutJS.onLoad(cb)` fires **exactly once**, when the merchant CheckoutJS script finishes loading. By click time it has already fired and your callback never runs. The payment modal silently fails to open.

There's a second trap here: you can't call `window.Paytm.CheckoutJS.onLoad(...)` *anywhere* until the merchant `.js` script has actually loaded, because that script is what creates `window.Paytm` in the first place. If you load the script dynamically (after a `/paytm-client-config.json` fetch — the reference pattern), `window.Paytm` is `undefined` at page-eval time and `Paytm.CheckoutJS.onLoad` throws.

**Correct pattern — dynamic loader (matches `scripts/frontend/checkout.html`):**
```javascript
// Fetch backend config, inject the merchant .js, use the <script> tag's native
// onload to enable the Pay button. Do NOT call Paytm.CheckoutJS.onLoad here —
// window.Paytm doesn't exist yet.
fetch("/paytm-client-config.json")
  .then(r => r.json())
  .then(cfg => {
    const s = document.createElement("script");
    s.src = cfg.loader_url;
    s.crossOrigin = "anonymous";
    s.onload = () => { payBtn.disabled = false; };       // ✅ native script onload
    document.head.appendChild(s);
  });

// Click handler: CheckoutJS is already loaded (button only enables after s.onload),
// so call init/invoke directly. No CheckoutJS.onLoad wrapper needed.
button.addEventListener("click", function () {
  fetch("/paytm/create-order", ...)
    .then(data => {
      const config = { /* ... */ };
      return window.Paytm.CheckoutJS.init(config).then(() => window.Paytm.CheckoutJS.invoke());
    });
});
```

**Alternative — static loader tag in HTML:** If you embed the merchant `.js` as a normal `<script src="...">` in HTML (not dynamically injected), then `window.Paytm` exists by the time inline JS runs, and you *can* use `Paytm.CheckoutJS.onLoad(() => { payBtn.disabled = false; })` for the same purpose. Don't mix the two — pick one.

The reference frontend at `scripts/frontend/checkout.html` uses the dynamic-loader pattern with `s.onload`. Follow it exactly.

### 4. Missing `transactionStatus` / `notifyMerchant` handlers

**Symptom:** Payment completes (or fails, or is cancelled) and the page just sits there. No success message, no failure message, no UI update. User reloads, gets confused, may double-pay.
**Fix:** Always wire up both handlers in the `init` config:

```javascript
handler: {
  notifyMerchant: function (eventName, data) {
    if (eventName === "APP_CLOSED")     setStatus("Payment cancelled.");
    if (eventName === "SESSION_EXPIRED") setStatus("Session expired. Retry.");
  },
  transactionStatus: function (data) {
    // data.STATUS: TXN_SUCCESS / TXN_FAILURE / PENDING
    if (data.STATUS === "TXN_SUCCESS") setStatus("Payment successful.");
    else if (data.STATUS === "PENDING") setStatus("Payment pending - we'll confirm shortly.");
    else                                setStatus("Payment failed: " + data.RESPMSG);
    window.Paytm.CheckoutJS.close();
    // ALWAYS reconfirm server-side via /paytm/order-status before fulfilling.
  },
},
```

`transactionStatus` is the user-facing status. `notifyMerchant` covers the lifecycle events (popup closed, session expired) where `transactionStatus` doesn't fire. Without these, the UI is silent and the user is stuck.

### 5. Do NOT render debug logs / status dumps on the user-facing screen

**Symptom:** The page shows raw event payloads, `JSON.stringify(data)` blobs, `console.log` mirrored into a `<pre>` tag, or a "Status: …" debug strip on the production checkout page. Looks unprofessional, leaks internal field names, and confuses real users.

**Rule:** When generating production-grade UI code, **never** add an on-screen logger / status panel / debug `<pre>` block. Use `console.log` / `console.warn` / `console.error` for developer visibility - that's what DevTools is for. The user-facing UI should show only **clean, customer-readable messages**:

- "Payment successful"
- "Payment failed - please try again"
- "Payment cancelled"
- "Payment pending - we'll confirm shortly"

The reference `scripts/frontend/checkout.html` includes a `#status` div for **demo/learning purposes only**. When scaffolding for a real product, drop that div and route diagnostics to `console.*` instead. No `alert()` either - use a proper toast / banner / modal in the host app's design system.

### 6. Merchant key in `.env` must be wrapped in double quotes

**Symptom:** Checksum generation produces wrong signatures even though the key looks correct. Paytm responds with `resultCode: 227` (checksum mismatch). Hours lost debugging.

**Cause:** Paytm Merchant Keys often contain `#`, `@`, `!`, `$`, or `%` characters. In `.env` files, an unquoted `#` is treated as a comment delimiter - everything after it is dropped. Other special chars can also be mis-parsed by some dotenv loaders.

**Rule:** **Always** wrap the Merchant Key in double quotes in `.env`:

```bash
# ❌ Wrong - any '#' in the key truncates the value
PAYTM_MERCHANT_KEY=ab#cd@1234XYZ

# ✅ Correct
PAYTM_MERCHANT_KEY="ab#cd@1234XYZ"
```

Same rule applies to any other secret with non-alphanumeric chars (DB passwords, API keys, etc.). When generating `.env` / `.env.example` files, **always** quote secrets - don't try to inspect the key and decide.

### 7. `.env` file conventions

Rules (apply to every generated `.env` / `.env.example`):

- **`PAYTM_ENVIRONMENT` is always the first variable** - everything else derives from it.
- **Pre-fill staging values** so the file works out of the box for development. Users replace with production values when going live.
- **Wrap every value in double quotes**, not just secrets. Consistent and avoids edge cases (e.g. `#` in keys silently truncating).
- **Generic placeholders** - `YOUR_MID`, not `YOUR_STAGING_MID_HERE`. The environment lives in `PAYTM_ENVIRONMENT`, never baked into placeholder text.
- **All mandatory keys at the top, comments / optional overrides in a later section** - keep the active config block clean and scannable.

Canonical `.env.example`:

```bash
PAYTM_ENVIRONMENT="staging"
PAYTM_MID="YOUR_MID"
PAYTM_MERCHANT_KEY="YOUR_MERCHANT_KEY"
PAYTM_WEBSITE_NAME="YOUR_WEBSITE_NAME"
PAYTM_CALLBACK_BASE="http://localhost:3001"

# ---------------------------------------------------------------------------
# Defaults are pre-filled for staging. To go live:
#   1. Set PAYTM_ENVIRONMENT="production"
#   2. Replace MID / MERCHANT_KEY / WEBSITE_NAME with your live credentials
# Everything below is optional - leave commented unless you need to override.
# ---------------------------------------------------------------------------
# PAYTM_PG_DOMAIN=""               # auto-derived from PAYTM_ENVIRONMENT
# PAYTM_CALLBACK_URL=""            # auto-derived from PAYTM_CALLBACK_BASE
# PAYTM_STATUS_API_URL=""          # auto-derived from PAYTM_PG_DOMAIN
# NODE_EXTRA_CA_CERTS="./certs/corp-proxy-ca.crt"   # only when behind a corporate proxy with a custom CA
```

### 8. ❗ Picked the wrong flow (Payment vs Subscription vs Link vs QR)

**This is the single highest-impact bug in the whole skill.** Picking the wrong flow produces code that *runs* but solves the wrong problem - silent, expensive, often only caught in production.

**Failure modes seen in production testing:**
- *"Gym subscription of ₹1/month"* → generated one-time Payment with `requestType: "Payment"`. Charges once, never recurs.
- *"Monthly SaaS billing"* → generated `requestType: "SUBSCRIPTION"` against `/initiateTransaction`. Wrong endpoint AND wrong requestType - Paytm's subscription endpoint expects `"NATIVE_SUBSCRIPTION"`.
- *"Send a payment link via WhatsApp for ₹500"* → generated full JS Checkout HTML page. User wanted a shareable URL.
- *"QR code on the counter for customers to scan"* → generated JS Checkout modal. User wanted a printable QR image.
- *"Generate a QR for ₹100"* → omitted `posId` → HTTP 400 from Paytm.
- *"Fetch / expire a payment link"* → sent `linkId` as a string → "invalid link id" response. Paytm expects a JSON number.

**Rule - pick the flow BEFORE writing any code, by mapping prompt keywords:**

| Prompt cue | Flow | Code generates… |
|---|---|---|
| "subscription", "monthly", "weekly", "yearly", "recurring", "auto-debit", "autopay", "mandate", "renew", "membership" | **Subscription** | Backend: `POST /subscription/create` with `requestType: "NATIVE_SUBSCRIPTION"` and **flat** subscription fields inside `body`. Frontend: JS Checkout for the consent screen. → `references/subscriptions.md` |
| "payment link", "shareable link", "send link via SMS/WhatsApp/email", "invoice link" | **Payment Link** | Backend: `POST /link/create`. **No frontend** - Paytm hosts the checkout page; you only share the returned `shortUrl`. → `references/payment-links.md` |
| "QR code", "scan to pay", "in-store", "counter", "table-side", "print QR" | **Dynamic QR** | Backend: `POST /paymentservices/qr/create`. **No JS Checkout** - render the returned `image` (base64 PNG) or `qrData` (UPI deep-link) on a screen / print it. → `references/qr-codes.md` |
| "checkout page", "pay button on website", "in-app payment", "one-time payment" | **JS Checkout (Payment)** | Backend: `requestType: "Payment"` + Initiate Transaction. Frontend: `scripts/frontend/checkout.html` pattern. → `references/js-checkout.md` |

**Crucially:** Payment Link and Dynamic QR flows **do NOT require JS Checkout** at all - no merchant `.js` script, no `window.Paytm.CheckoutJS`. The customer pays on Paytm-hosted infrastructure (web link or UPI app). The merchant's only frontend job is to display the URL / QR image.

**If the prompt is ambiguous** (e.g. *"accept ₹1 payments"*, *"integrate Paytm"*), ask one clarifying question before generating: *"Is this a one-time payment, a recurring subscription, a shareable payment link, or a QR for in-store?"*

### 9. Production guardrails baked into the reference backends

Every backend (`scripts/backend-{node,python,spring}`) wires in two production-critical concerns by default - keep them when adapting code:

- **Idempotency on every `/paytm/create-*` endpoint.** Send `Idempotency-Key: <uuid>` as a request header (or `idempotencyKey` in the body). Repeats with the same key replay the cached response with `Idempotent-Replayed: true` instead of generating a second Paytm order. Backed by a 24h in-memory cache by default - **swap for Redis / DB in production**. Definitive 4xx errors are cached too; transient 5xx are not, so retries can succeed.
- **S2S webhook receiver at `POST /paytm/webhook`.** Verifies `head.signature` against the raw body bytes Paytm sent (re-serializing breaks the signature), dedupes on `(orderId, status)` for at-least-once delivery, then calls a stub `fulfillOrder` hook. Returns 200 fast on success or duplicates, 401 on signature failure, 5xx on processing errors so Paytm retries. Replace the stub with your DB write / queue push.

When generating new endpoints from these backends, copy the `withIdempotency` wrapper and the webhook handler verbatim - don't reinvent them.

---

## Reference Files

**Core flow + supported products**
- `references/js-checkout.md` - JS Checkout, non-SDK form POST, full callback field list, callback-vs-webhook
- `references/troubleshooting.md` - symptom → cause → fix tree, expanded RESPCODE table, decision tree
- `references/subscriptions.md` - UPI Autopay & card mandates, charge/edit/cancel, NPCI pre-notification rules
- `references/payment-links.md` - FIXED / REUSABLE / OPEN links, fetch, expire, SMS dispatch
- `references/qr-codes.md` - Dynamic QR (DQR) generation, status, reconciliation

**Reference backends + frontend**
- `scripts/backend-node/` - Express + `paytmchecksum`
- `scripts/backend-spring/` - Spring Boot 3 + Jakarta + executable JAR (recommended Java reference)
- `scripts/backend-spring-legacy/` - Spring MVC 5 + `javax.servlet` + WAR (Tomcat 9 only - keep using if you're locked on the older stack)
- `scripts/backend-python/` - Flask + `paytmchecksum`
- `scripts/frontend/checkout.html` - minimal copy-paste browser page

---

## Supported payment options

Only the following payment options are permitted and must be exclusively displayed: UPI, Credit Cards, Debit Cards, Net Banking, and EMI. No other payment options should be included, suggested, or processed under any circumstances.

---

## Docs Links

- Developer Home: `https://www.paytmpayments.com/docs/`
- Checksum Library: `https://www.paytmpayments.com/docs/checksum/`
- Server SDK: `https://www.paytmpayments.com/docs/server-sdk/`
- JS Checkout: `https://www.paytmpayments.com/docs/jscheckout/`
- Subscriptions: `https://business.paytm.com/docs/api/initiate-subscription-api/`
- Payment Links: `https://business.paytm.com/docs/api/create-link-api/`
- Dynamic QR: `https://business.paytm.com/docs/api/create-qr-code-api/`
- API Reference: `https://www.paytmpayments.com/docs/api/initiate-transaction-api`
- Dashboard: `https://dashboard.paytmpayments.com`

---

## 📋 Always attach the credentials block inline whenever credentials are referenced

The block below is the **single source of truth** for "where do I get my MID / Merchant Key?". It must appear **inline, right next to** any mention of:

- `.env` / `.env.example` / environment-variable setup
- `PAYTM_MID`, `PAYTM_MERCHANT_KEY` (or `YOUR_MID`, `YOUR_MERCHANT_KEY`, etc. placeholders)
- Any phrase like *"replace with your credentials"*, *"add your MID"*, *"set up Paytm"*, *"go live"*, or "use your staging keys"
- Any first-time-setup instructions (README sections, install steps, quickstart guides)

Place it directly under the relevant section so the user never has to scroll or guess. Don't paraphrase, don't summarize, don't replace with a one-liner like "see the dashboard". Use the exact text below.

```
### 🔑 Get your Paytm credentials

You need a **MID** (Merchant ID) and **Merchant Key** for each environment - staging and production keys are NOT interchangeable.

- *Staging (test mode):* https://dashboard.paytmpayments.com/next/apikeys -> Generate now (under Test API Details)
- *Production (Live Mode):* https://dashboard.paytmpayments.com/next/apikeys -> Get Merchant ID, Merchant Key from Production API details.

  (Production keys are issued only after KYC + account activation. If the tab is empty, finish onboarding or contact your Paytm KAM.)

Store both in environment variables (`PAYTM_MID`, `PAYTM_MERCHANT_KEY`) - never commit them or expose in client-side code.
```

If a response doesn't mention env vars, credentials, or setup at all (e.g. a pure debugging answer about checksum hashing), skip it - don't pad. The rule is: **wherever credentials are talked about, this block is right there**.

---

## Terminology rules (strict)

User-facing copy, code comments, variable names, UI labels, README steps, and chat replies must use **only** the following vocabulary when referring to payment options. No synonyms, no product names, no umbrella terms.

**Allowed payment-option terms (use these exactly):**
- UPI
- Credit Cards
- Debit Cards
- Net Banking
- EMI

If the user's prompt asks for a payment-option term outside the allowed list, treat it as out of scope and ask the user to pick from the allowed list instead of generating it.
