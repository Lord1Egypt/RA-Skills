# Paytm Subscriptions / UPI Autopay (Native Create Subscription)

> _Companion to **`SKILL.md`** - load this file alongside `SKILL.md`, never instead of it._

Recurring debits with one user-consented mandate. Supported rails: **UPI Autopay** (NPCI), **Cards** (RBI e-mandate), **Net Banking** (limited issuers).

> **⚠️ READ THIS FIRST - common mistakes that break subscription integrations:**
>
> 1. **Endpoints differ between staging and production:**
>    - Staging: `POST https://securestage.paytmpayments.com/subscription/create`
>    - Production: `POST https://secure.paytmpayments.com/theia/api/v1/subscription/create`
>    Production has the extra `/theia/api/v1/` prefix. Most teams set this once via `PAYTM_PG_DOMAIN` and forget - double-check on first prod deploy.
> 2. **Three query params are required:** `mid`, `orderId`, **and `traceId`**. `traceId` is alphanumeric + hyphens / underscores only.
> 3. **`head` requires `clientId` (e.g. `"C11"`) and `channelId` (`"WEB"` / `"WAP"`)** in addition to `signature`. Missing either → request rejected before it reaches business logic.
> 4. **`requestType`** is **`"NATIVE_SUBSCRIPTION"`** for standard subscriptions, **`"NATIVE_MF_SIP"`** for mutual-fund SIPs. Not `"SUBSCRIPTION"`, not `"Payment"`.
> 5. Subscription fields are **flat inside `body`** - DO NOT wrap them in a `subscriptionDetails` / `subscriptionInfo` object. Wrapping returns HTTP 400.
> 6. **Both `subscriptionFrequency` AND `subscriptionFrequencyUnit` are required.** Frequency is the number ("2"), unit is the period ("MONTH"). Together: every 2 months. Earlier versions of this skill said "no subscriptionFrequency field" - that was wrong.
> 7. **`subscriptionPaymentMode` - default to `"UNKNOWN"`.** Doc says required and lists `CC` / `DC` / `BANK_MANDATE`. In practice the safest cross-MID value is **`"UNKNOWN"`** - Paytm then renders all enabled rails on the consent screen and the user picks. Send a specific value (`"CC"`, `"DC"`, `"BANK_MANDATE"`, etc.) only when restricting to one rail and confirmed for your MID. `"BANK_MANDATE"` additionally needs `mandateType: "E_MANDATE"` + bank-account details.
> 8. **`subscriptionEnableRetry` is a string `"1"` / `"0"`** (not boolean). If you set it to `"0"`, **also omit `subscriptionRetryCount`** - sending a retry count with retry disabled returns `"Invalid subscription retry count"`. If retry is enabled (`"1"`), supply a count.
> 9. **`autoRenewal` / `autoRetry` / `communicationManager` ARE booleans** (true/false). Inconsistent with `subscriptionEnableRetry`, but that's how the API is.
> 10. Dates (`subscriptionStartDate`, `subscriptionExpiryDate`) are `YYYY-MM-DD`.
> 11. `subscriptionStartDate` and `subscriptionGraceDays` are **conditionally paired** - if you send one, send both.
> 12. **`userInfo.custId` must be sanitized** - alphanumerics + `_` `@` `!` `$` `.` are accepted; spaces, special characters, and unicode otherwise are rejected with `"Invalid Customer ID"`. Safest: `custId.replace(/[^a-zA-Z0-9_]/g, "_")`.
> 13. **"No payment options available" on the consent screen** = subscription product is not enabled on the MID. Ask Paytm support / KAM to enable Subscription / UPI Autopay; the API will let you generate `txnToken` even when the product isn't entitled, so it surfaces only at JS Checkout time.
> 14. **CC / DC mandates have stricter rules than UPI / BANK_MANDATE:**
>     - `txnAmount.value` must be **> ₹1** (use `"2.00"` or higher; ₹1 is rejected for card mandates).
>     - `subscriptionGraceDays` must be **≤ 3** (`"3"` max; values like `"5"` or `"7"` are rejected).
>     If you don't know which rail the user will pick (i.e. `subscriptionPaymentMode: "UNKNOWN"`), use the stricter limits to stay compatible with all rails: amount ≥ `"2.00"`, graceDays ≤ `"3"`.
> 15. **Don't send `renewalAmount`** by default. It's optional in the API and most flows don't need it; sending it can cause unexpected behaviour at consent time. Only add it if you explicitly want to surface a different recurring amount on the consent screen than `txnAmount.value`.
> 16. **`subscriptionStartDate` defaults to today (IST).** Paytm rejects past dates; tomorrow / future is fine but pushes the first debit out. Today (`new Date()` formatted `YYYY-MM-DD` in IST) is the safest default.
> 17. **`subscriptionGraceDays` must be STRICTLY LESS than the cycle length** (cycle = `subscriptionFrequency × subscriptionFrequencyUnit` in days). Violating this returns error `4001` with message `Grace days cannot be greater than the frequency set against the subscription`. The skill's default `graceDays: "3"` works for monthly / yearly cycles but **breaks for any cycle ≤ 3 days**:
>
>     | frequency × unit | cycle (days) | safe graceDays |
>     |---|---|---|
>     | `"1"` × `DAY` | 1 | omit (or `"0"`) |
>     | `"2"` × `DAY` | 2 | `"1"` |
>     | `"1"` × `WEEK` | 7 | up to `"6"` (or `"3"` for CC/DC compat) |
>     | `"1"` × `MONTH` | ~30 | `"3"` (CC/DC cap) or up to `"29"` for UPI |
>     | `"1"` × `YEAR` | ~365 | `"3"` (CC/DC cap) or higher for UPI |
>
>     When you change `subscriptionFrequencyUnit` from `MONTH` to anything shorter, **also drop `graceDays` to ≤ cycle − 1**. Daily mandates: omit `graceDays` entirely.

---

## Scope of this skill

This skill covers **only** the mandate-creation flow:
1. Server calls `/subscription/create` to get a `txnToken` + `subscriptionId`.
2. Browser invokes JS Checkout with that `txnToken` so the user can complete the mandate consent.

Subsequent operations (status check, recurring debit, edit, cancel) are intentionally **out of scope**. Refer to live Paytm docs and validate paths before implementing those.

---

## Concepts

| Term | Meaning |
|---|---|
| **Mandate** | One-time user authorization at a maximum amount, frequency, and validity window |
| **Subscription ID** | Paytm-issued ID for the mandate, returned in the create response |
| **Mandate state** | `INITIATED` → `ACTIVE` → `EXPIRED` / `CANCELLED` / `REJECTED` |
| **traceId** | Per-request unique id for tracing on Paytm's side. Generate one per call (UUID-like) |
| **clientId** | Paytm-issued identifier for the merchant key (`"C11"` for single-key merchants) |
| **Pre-notification** | NPCI rule: notify user 24h before debit on UPI Autopay (Paytm handles this) |

---

## Step 1 - Create the mandate (server-side)

### Endpoint

| Environment | Full URL |
|---|---|
| Staging | `POST https://securestage.paytmpayments.com/subscription/create?mid={MID}&orderId={ORDER_ID}&traceId={TRACE_ID}` |
| Production | `POST https://secure.paytmpayments.com/theia/api/v1/subscription/create?mid={MID}&orderId={ORDER_ID}&traceId={TRACE_ID}` |

`Content-Type: application/json`

### Request

```json
{
  "head": {
    "clientId": "C11",
    "channelId": "WEB",
    "version": "v1",
    "requestTimestamp": "1714464000000",   // Unix epoch ms - generate at request time
    "signature": "<CHECKSUMHASH over JSON.stringify(body)>"
  },
  "body": {
    "requestType": "NATIVE_SUBSCRIPTION",
    "mid": "YOUR_MID",
    "orderId": "SUB_ORD_001",
    "websiteName": "WEBSTAGING",
    "txnAmount": { "value": "2.00", "currency": "INR" },

    "subscriptionPaymentMode": "UNKNOWN",
    "subscriptionAmountType": "FIX",
    "subscriptionMaxAmount": "499.00",
    "subscriptionFrequency": "1",
    "subscriptionFrequencyUnit": "MONTH",
    "subscriptionStartDate": "2026-04-30",
    "subscriptionExpiryDate": "2027-04-30",
    "subscriptionGraceDays": "3",
    "subscriptionEnableRetry": "0",

    "userInfo": {
      "custId": "CUST_001",
      "mobile": "9999999999",
      "email": "buyer@example.com",
      "firstName": "Buyer",
      "lastName": "Name"
    },

    "callbackUrl": "https://yoursite.com/paytm/callback",
    "extendInfo": { "mercUnqRef": "INVOICE-INV-001" }
  }
}
```

> **Defaults baked into this example (applied unless the user explicitly overrides):**
> - `subscriptionPaymentMode: "UNKNOWN"` - lets Paytm render all enabled rails on consent. Don't hard-code a specific rail unless you want to restrict.
> - `txnAmount.value: "2.00"` - first-debit amount must be **> ₹1** for CC/DC mandates. `"2.00"` is the safe minimum that works across all rails.
> - `subscriptionGraceDays: "3"` - CC/DC reject values > 3, AND must be < cycle length (`subscriptionFrequency × unit-in-days`). Safe for monthly+ cycles. **Drop or omit for daily / sub-3-day cycles** (else Paytm returns `4001: Grace days cannot be greater than the frequency`).
> - `subscriptionStartDate` - today (IST), formatted `YYYY-MM-DD`. Generate at request time, don't hard-code.
> - `subscriptionEnableRetry: "0"` - retry disabled.
>
> **What's NOT in this example, intentionally:**
> - `subscriptionRetryCount` - omitted because retry is disabled. Sending a count with retry off returns `"Invalid subscription retry count"`. To enable retry, set `subscriptionEnableRetry: "1"` AND add `subscriptionRetryCount: "3"`.
> - `mandateType` - omitted. Only needed when `subscriptionPaymentMode: "BANK_MANDATE"` (which we're not using).
> - `renewalAmount` - omitted. Optional field; most flows don't need it. Only add when you specifically want to surface a different recurring amount than `txnAmount.value` on the consent screen.

### Field reference

**`head`**

| Field | Required | Notes |
|---|---|---|
| `clientId` | ✅ | **Per-merchant - issued by Paytm during onboarding.** `"C11"` is the common value for single-merchant-key setups but is NOT a universal default. Multi-key merchants get a different `clientId` per key. Confirm yours with your Paytm KAM before going live; staging often accepts `"C11"` even when prod rejects it |
| `channelId` | ✅ | `"WEB"` (web server) or `"WAP"` (mobile) |
| `signature` | ✅ | CHECKSUMHASH over `JSON.stringify(body)` |
| `version` | optional | `"v1"` |
| `requestTimestamp` | optional | UNIX epoch in **milliseconds** as a string |

**`body` - core**

| Field | Required | Notes |
|---|---|---|
| `requestType` | ✅ | `"NATIVE_SUBSCRIPTION"` (standard) or `"NATIVE_MF_SIP"` (mutual-fund SIPs) |
| `mid` | ✅ | Same value as the `mid` query param |
| `orderId` | ✅ | Same value as the `orderId` query param |
| `websiteName` | ✅ | `"WEBSTAGING"` for staging; per-MID for prod (e.g. `"DEFAULT"`, `"retail"`) |
| `txnAmount.value` | ✅ | First-debit amount as **string** with two decimals. **Default `"2.00"`** - must be > ₹1 for CC/DC mandates; `"1.00"` works for UPI/BANK_MANDATE only |
| `txnAmount.currency` | ✅ | `"INR"` |
| `userInfo.custId` | ✅ | Sanitize first - see callout above. Allowed extras: `@ ! _ $ .` |
| `userInfo.mobile` / `email` / `firstName` / `lastName` | optional | Strongly recommended - pre-fills consent screen |

**`body` - subscription**

| Field | Required | Notes |
|---|---|---|
| `subscriptionPaymentMode` | ✅ | **Default `"UNKNOWN"`** - Paytm renders all enabled rails on consent. Send a specific value (`"CC"` / `"DC"` / `"BANK_MANDATE"`) only when restricting to one rail. `"BANK_MANDATE"` requires `mandateType: "E_MANDATE"` + bank details (advanced) |
| `subscriptionAmountType` | ✅ | `"FIX"` (same amount each cycle) or `"VARIABLE"` (variable, ≤ `subscriptionMaxAmount`) |
| `subscriptionMaxAmount` | conditional | **Required** when `subscriptionAmountType: "VARIABLE"`. For FIX, set to the per-cycle amount |
| `subscriptionFrequency` | ✅ | The **number** of `Unit`s per cycle, as string. `"1"` + unit `MONTH` = monthly; `"15"` + `DAY` = every 15 days |
| `subscriptionFrequencyUnit` | ✅ | Per Paytm doc: daily / weekly / monthly / yearly. Examples seen: `"DAY"`, `"WEEK"`, `"MONTH"`, `"YEAR"`, `"ONDEMAND"`. Confirm with your Paytm KAM if unsure |
| `subscriptionStartDate` | conditional | `YYYY-MM-DD` IST. **Default = today**, generated at request time. Cannot be in the past. Required if `subscriptionGraceDays` is set |
| `subscriptionGraceDays` | conditional | String. **Default `"3"`** (max allowed for CC/DC). UPI/BANK_MANDATE accept higher values, but `"3"` is the safe cross-rail default. Required if `subscriptionStartDate` is set |
| `subscriptionExpiryDate` | ✅ | `YYYY-MM-DD` IST |
| `subscriptionEnableRetry` | ✅ | **String** `"1"` (enable) / `"0"` (disable). **Default `"0"`** - retry off |
| `subscriptionRetryCount` | conditional | String, number of retries. **Default: omit entirely** (matches default `subscriptionEnableRetry: "0"`). Send ONLY when retry is enabled (`"1"`); sending alongside `"0"` returns `"Invalid subscription retry count"` |
| `mandateType` | conditional | `"E_MANDATE"` or `"PAPER_MANDATE"` - required ONLY when `subscriptionPaymentMode: "BANK_MANDATE"`. Omit when `subscriptionPaymentMode` is omitted |
| `autoRenewal` | optional | **Boolean** (true/false) |
| `autoRetry` | optional | **Boolean** (true/false) |
| `communicationManager` | optional | **Boolean** (true/false). Enables Paytm-side notifications |
| `subsGoodsInfo` | conditional | Required when `communicationManager: true` |
| `renewalAmount` | optional | Recurring amount surfaced to the user / used for auto-renewal. **Default: omit** - most flows don't need it. Only add when you specifically want a different value than `txnAmount.value` on the consent screen |
| `subscriptionPurpose` | optional | Free text, e.g. `"Loan Payments"` |
| `enablePaymentMode` / `disablePaymentMode` | optional | Arrays of `{ "mode": "CREDIT_CARD" \| ... }` to restrict / exclude payment options |
| `mandateAccountDetails` | optional | Bank mandate account details (advanced) |
| `callbackUrl` | optional | Where Paytm redirects the user after consent |
| `extendInfo.udf1` / `udf2` / `udf3` | optional | Free-form merchant fields |
| `extendInfo.mercUnqRef` | optional | Echoed in the UMP dashboard for filtering |
| `extendInfo.comments` | optional | Free-form |

### Response

```json
{
  "head": {
    "responseTimestamp": "1714464000000",   // Unix epoch ms - server-supplied
    "version": "v1",
    "clientId": "C11",
    "signature": "..."
  },
  "body": {
    "resultInfo": {
      "resultStatus": "S",
      "resultCode": "0000",
      "resultMsg": "SUCCESS"
    },
    "txnToken": "abc123...",
    "subscriptionId": "<paytm subscriptionId>",
    "authenticated": "False",
    "isPromoCodeValid": false
  }
}
```

| Field | Notes |
|---|---|
| `resultInfo.resultStatus` | `"S"` = success, `"F"` = failure |
| `resultInfo.resultCode` | 4-character code; see error table below |
| `txnToken` | Single-use, **15-min TTL** - pass to JS Checkout in Step 2 |
| `subscriptionId` | Persist this; it identifies the mandate for any future operations |
| `authenticated` | String `"True"` / `"False"` (note: string, not boolean) |

### Sanitize `userInfo.custId` before sending

Paytm rejects custIds with characters outside `[A-Za-z0-9_@!$.]` with `"Invalid Customer ID"`. Safest path is to normalize to `[A-Za-z0-9_]` only:

```javascript
// Node
const safeCustId = (rawCustId || "CUST_DEMO").replace(/[^a-zA-Z0-9_]/g, "_");
```

```python
# Python
import re
safe_cust_id = re.sub(r"[^a-zA-Z0-9_]", "_", raw_cust_id or "CUST_DEMO")
```

```java
// Java
String safeCustId = (rawCustId == null ? "CUST_DEMO" : rawCustId).replaceAll("[^a-zA-Z0-9_]", "_");
```

`"Rahul Sharma"` → `"Rahul_Sharma"`. Persist the sanitized form so future calls stay consistent.

---

## Step 2 - Invoke JS Checkout for consent

Same JS Checkout flow as a one-time payment - only the `txnToken` source differs (it came from `/subscription/create`):

```html
<script src="{pgDomain}/merchantpgpui/checkoutjs/merchants/{MID}.js"
        type="application/javascript" crossorigin="anonymous"></script>
<script>
  window.Paytm.CheckoutJS.onLoad(function () {
    window.Paytm.CheckoutJS.init({
      root: "",
      flow: "DEFAULT",
      data: {
        orderId: "SUB_ORD_001",
        token: "<txnToken from /subscription/create>",
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

The user sees the consent screen showing the recurring amount + frequency, approves the mandate, then Paytm POSTs to your `callbackUrl` with the standard fields plus `subscriptionId`. **Verify `CHECKSUMHASH` on the callback** before treating the mandate as set up. Full callback details in `references/js-checkout.md`.

---

## Error codes (Native Create Subscription)

| `resultCode` | `resultMsg` | What to fix |
|---|---|---|
| `0000` | Subscription initiated successfully | Success - proceed to JS Checkout |
| `1007` | Missing mandatory element | Look at `resultMsg` - usually a missing required field; cross-check the field-reference table above |
| `1008` | Pipe character is not allowed | A field contains `\|`; sanitize input |
| `2004` | SSO Token is invalid | Only relevant if you set `paytmSsoToken`; remove it for non-Paytm-ecosystem flows |
| `2007` | Txn amount is invalid | `txnAmount.value` formatting issue (must be string, two decimals, ≥ minimum) |
| `2009` | Duplicate request, same orderId already in progress | Generate a fresh `orderId` |
| `2013` | Mid in query param doesn't match Mid in request | `mid` value must be identical in `?mid=` and in `body.mid` |
| `2014` | OrderId in query param doesn't match OrderId in request | Same - keep `?orderId=` and `body.orderId` identical |
| `4001` | `Invalid Frequency Unit` / `Invalid Subscription Amount Type` / **`Grace days cannot be greater than the frequency set against the subscription`** | Verify `subscriptionFrequencyUnit` enum value; verify `subscriptionAmountType` is `FIX`/`VARIABLE`; **verify `subscriptionGraceDays` < cycle length** (`subscriptionFrequency × unit-in-days`) — see warning #17. Daily mandates: omit `graceDays`. |
| `900` | System error | Paytm-side; retry with the same `orderId` |

---

## Troubleshooting

### "No payment options available" on the consent screen

`/subscription/create` returned a `txnToken` and JS Checkout opened, but the modal shows **"No payment options available"** (or an empty list of payment options).

**This is not a code bug - it's a dashboard provisioning issue.** Subscription / UPI Autopay must be explicitly enabled on the MID by Paytm. The API and JS Checkout will let you create tokens against the MID even when the product isn't enabled, so the failure surfaces only at render time.

**Fix:** Contact your Paytm KAM / support and ask them to enable the **Subscription / UPI Autopay** product on the MID. Allow up to 24h for propagation.

### "Invalid subscription retry count"

You sent `subscriptionRetryCount` but `subscriptionEnableRetry: "0"` (or vice versa - incompatible pair). Two valid combinations:

```jsonc
// Retry disabled - omit retryCount
{ "subscriptionEnableRetry": "0" }

// Retry enabled - supply a count
{ "subscriptionEnableRetry": "1", "subscriptionRetryCount": "3" }
```

Don't mix `"0"` + a count.

### "Invalid Customer ID"

Sanitize `custId` (see "Sanitize `userInfo.custId`" above). Most common cause: passing the customer's name (`"Rahul Sharma"`) directly as the custId.

### `2013` / `2014` - query-param vs body mismatch

Easy to hit when you put `mid` / `orderId` in the URL but forget them in the body (or vice versa). Both are required and must match.

### Wrong endpoint in production

Staging path is `/subscription/create`; production path is `/theia/api/v1/subscription/create`. If your `PAYTM_PG_DOMAIN` switch flips the host but not the path, prod will 404.

---

## Pitfalls

1. **Wrong endpoint.** `/theia/api/v1/initiateTransaction` is for one-time Payment. Subscriptions use `/subscription/create` (staging) or `/theia/api/v1/subscription/create` (prod) - different validators, different responses.
2. **`requestType` must be `"NATIVE_SUBSCRIPTION"` or `"NATIVE_MF_SIP"`** exactly. `"SUBSCRIPTION"` and `"Payment"` both fail.
3. **No `subscriptionDetails` wrapper** - fields are flat inside `body`. Wrapping → 400.
4. **Both `subscriptionFrequency` AND `subscriptionFrequencyUnit` are required.** Earlier versions of this skill said "no subscriptionFrequency field" - that was wrong; restore both.
5. **`subscriptionPaymentMode` default is `"UNKNOWN"`.** Lets Paytm render all enabled rails on consent. Send `"CC"` / `"DC"` / `"BANK_MANDATE"` only when restricting to a specific rail. `"BANK_MANDATE"` requires extra `mandateType` + bank-account fields.
6. **Mixed types:** `subscriptionEnableRetry` is string `"1"`/`"0"`; `autoRenewal` / `autoRetry` / `communicationManager` are real booleans. Don't normalize one shape across the board.
7. **`subscriptionRetryCount` only with retry enabled.** `subscriptionEnableRetry: "0"` + `subscriptionRetryCount: "3"` → `"Invalid subscription retry count"`. Omit retry count when retry is off.
8. **`subscriptionStartDate` cannot be in the past** and is conditionally paired with `subscriptionGraceDays` - send both or neither.
9. **`mid` and `orderId` must match** between query string and body - `2013` / `2014` errors otherwise.
10. **`traceId` is required as a query param**, alphanumeric + hyphens / underscores only. Generate one per call.
11. **`txnToken` is single-use, 15-min TTL** - same as one-time payment tokens.
12. **`userInfo.custId` must be sanitized** - most teams hit `"Invalid Customer ID"` by passing real names.
13. **"No payment options available"** at consent time means the MID doesn't have Subscription / UPI Autopay enabled - see Troubleshooting above.
14. **`response.body.authenticated` is the string `"True"` / `"False"`**, not a boolean. Compare as strings.
15. **CC / DC mandate constraints:** `txnAmount.value` must be **> ₹1** (use `"2.00"` minimum); `subscriptionGraceDays` must be **≤ 3**. When using `subscriptionPaymentMode: "UNKNOWN"`, apply the stricter limits to stay compatible with whatever rail the user picks.
16. **Don't send `renewalAmount`** by default - optional field, most flows don't need it. Only add if you want a different recurring amount than `txnAmount.value` shown on consent.
17. **`subscriptionStartDate` defaults to today.** Generate at request time: `new Date().toISOString().slice(0, 10)` (Node) or equivalent. Don't hard-code a date.
