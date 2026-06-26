# Paytm Payment Links

> _Companion to **`SKILL.md`** - load this file alongside `SKILL.md`, never instead of it._

Server-generated short URLs that open Paytm-hosted checkout. No client SDK; works in SMS, WhatsApp, email. Use for invoices, manual collections, social-commerce, agent-assisted sales.

> **⚠️ READ THIS FIRST - common mistakes that cause silent failures and 400 errors:**
>
> 1. The link identifier **`linkId` must be sent as a JSON number (long integer)**, NOT a quoted string. `"linkId": "31309"` fails. `"linkId": 31309` works.
> 2. **Read the response link id defensively** - current Paytm responses return `linkId` (camelCase); older docs / staging environments may still return `LinkID` (capitalized). Use `body.linkId ?? body.LinkID`. Always send it back to Paytm as `linkId` (camelCase) on subsequent calls.
> 3. The **resend** endpoint is `/link/resendNotification`, NOT `/link/resend`.
> 4. **Every link API call requires `head.tokenType: "AES"`**, not just `signature`. Omitting it returns `"Invalid tokenType"`. Applies to create / fetch / update / resend / expire - all of them.
> 5. **`linkName` and `linkDescription` have *different* charset rules in practice — sanitize them separately:**
>    - **`linkName`: alphanumerics ONLY (no spaces).** Paytm docs say spaces are allowed, but several MIDs reject space as a special character with `"link name contains special character"`. Stripping spaces is the safe cross-MID default.
>    - **`linkDescription`: alphanumerics + spaces.**
>    Both must be ≥ 3 chars. `-`, `_`, `.`, `#`, `@`, `&`, `/`, `:`, `'`, `"`, etc. fail in both fields. Sanitize on the server before sending; never pass raw user input through.
> 6. **Fetch response wraps the link in `body.links[0]`**, not `body` directly. Reading `json.body.linkStatus` returns `undefined` - read `json.body.links[0].linkStatus`.
> 7. **Customer phone / email / name go inside a `customerContact` object** - they are **NOT** top-level body fields. Putting `customerMobile` / `customerEmail` at the top of `body` is silently accepted but Paytm never sends the SMS/email.
> 8. **`amount` in create-link is a JSON number** (e.g. `100.00`), not a string - different from `txnAmount.value` in Initiate Transaction. Quoting it as a string can fail validation.
> 9. **`head` should include a `timestamp`** (Unix epoch seconds as a string) alongside `tokenType` + `signature` per the official Create Link doc.
> 10. **`expiryDate` format is MID-dependent.** Most MIDs accept `DD/MM/YYYY HH:MM:SS` (returns error code `5021: Date should be in format DD/MM/YYYY` when wrong). The Paytm doc shows `yyyy-MM-dd HH:mm:ss` for some. **Default to `DD/MM/YYYY HH:MM:SS`** - switch only if your MID rejects it.
> 11. **Use `linkType: "FIXED"` for fixed-amount, single-payer links.** `"GENERIC"` is an open-amount link - it silently ignores `amount` on create (fetch shows `amount: null`) AND rejects amount updates with error `5082`. Don't use GENERIC unless you actually want payer-chosen amount.
> 12. **Create response key is `linkId` (camelCase)** in current Paytm responses - older docs / earlier versions of this skill said `LinkID`. Read defensively: `const id = body.linkId ?? body.LinkID;`
> 13. **Reconcile a Payment Link via `/link/fetchTransaction`, NOT `/v3/order/status`.** The link product has a dedicated transactions endpoint that returns every payer's order(s) under `body.orders[]`. Use it for Payment Link reconciliation; `/v3/order/status` is for one-time-payment / JS-Checkout flows.

Reference: <https://www.paytmpayments.com/docs/api/create-link-api?ref=paymentLinks>

---

## Create a link

```
POST {pgDomain}/link/create
Content-Type: application/json
```

```json
{
  "head": {
    "tokenType": "AES",
    "signature": "<sig>",
    "timestamp": "1714464000"
  },
  "body": {
    "mid": "YOUR_MID",
    "linkType": "FIXED",
    "linkName": "Invoice001",
    "linkDescription": "Payment for Invoice 001",
    "amount": 499.00,
    "sendSms": true,
    "sendEmail": true,
    "customerContact": {
      "customerName": "Buyer Name",
      "customerEmail": "buyer@example.com",
      "customerMobile": "9999999999",
      "customerId": "CUST_001"
    },
    "expiryDate": "30/12/2026 23:59:59",
    "orderId": "ORD_INV_001",
    "callbackUrl": "https://yoursite.com/paytm/link-callback",
    "merchantUniqueReference": "INV-001-v1"
  }
}
```

| Field | Required | Notes |
|---|---|---|
| `mid` | ✅ | Merchant ID |
| `linkName` | ✅ | **Min 3 chars, alphanumerics ONLY — no spaces, no special chars.** Paytm docs say spaces are allowed; several MIDs reject them as `"link name contains special character"`. Strip with `s.replace(/[^A-Za-z0-9]/g, "")`. Examples: `Invoice001`, `OrderABC123` |
| `linkDescription` | ✅ | **Min 3 chars, alphanumerics + spaces.** Spaces ARE allowed here (unlike `linkName`). No `!`, `@`, `#`, `$`, `&`, `-`, `_`, `.`, `/`, `:`, `'`, `"`. Strip with `s.replace(/[^A-Za-z0-9 ]/g, " ")`. Examples: `"Invoice 001"`, `"Gym membership"` |
| `linkType` | ✅ | `"FIXED"` for single-payer fixed-amount (most common), `"GENERIC"` for open-amount payer-chosen. **Don't use GENERIC for fixed amounts** - it ignores `amount` on create and rejects updates with error `5082` |
| `amount` | conditional | **JSON number** (`499.00`), NOT a string. Required for `FIXED`; ignored for `GENERIC` |
| `head.tokenType` | ✅ | Always `"AES"` |
| `head.signature` | ✅ | CHECKSUMHASH over the body |
| `head.timestamp` | ✅ | Unix epoch seconds as string (e.g. `"1714464000"`) |
| `sendSms` / `sendEmail` | optional | Booleans - instruct Paytm to dispatch to `customerContact.customerMobile` / `customerContact.customerEmail` |
| `customerContact` | optional | **Nested object** - see below. Required for SMS / email dispatch |
| `customerContact.customerName` | optional | Display name |
| `customerContact.customerEmail` | optional | Required if `sendEmail: true` |
| `customerContact.customerMobile` | optional | Required if `sendSms: true` |
| `customerContact.customerId` | optional | Your customer ID for reconciliation |
| `expiryDate` | optional | `DD/MM/YYYY HH:MM:SS` IST (most MIDs). Max ~1 year out. If MID rejects this format try `yyyy-MM-dd HH:mm:ss` |
| `orderId` | optional | **Strongly recommended** - lets you reconcile via `/v3/order/status` |
| `callbackUrl` | optional | Same semantics as JS Checkout callback (browser POST after payment) |
| `merchantUniqueReference` | optional | Echoed back; useful for invoice ↔ link mapping |

For payer-chosen amount: omit `amount` and provide `minAmount` / `maxAmount` as numbers (`10.00`, `10000.00`). Confirm support with your account manager - some Paytm MIDs don't allow open-amount links.

### Response

```json
{
  "head": { "responseTimestamp": "...", "version": "v1", "signature": "..." },
  "body": {
    "resultInfo": { "resultStatus": "SUCCESS", "resultCode": "200", "resultMsg": "Success" },
    "linkId": 31309,
    "shortUrl": "https://paytm.me/XXXXXXX",
    "longUrl": "https://secure.paytmpayments.com/link/...",
    "isActive": true
  }
}
```

> **Read the link id defensively.** Production Paytm currently returns `linkId` (camelCase); older docs / some staging environments may still return `LinkID` (capitalized). Use:
>
> ```js
> const linkId = body.linkId ?? body.LinkID;   // works for both
> ```
>
> **Persist the value as an integer**, not a string - JavaScript will silently widen large IDs into floats; use `BigInt` or a string-of-digits internally if your stack mishandles long integers, but always send it back to Paytm as a JSON number.

> **Status field varies by MID.** Some MIDs return `linkStatus: "ACTIVE"` (string); others return `isActive: true` (boolean). Normalize on read:
>
> ```js
> const linkStatus = body.linkStatus
>   ?? (body.isActive === true ? "ACTIVE" : body.isActive === false ? "INACTIVE" : "UNKNOWN");
> ```
>
> Same dual-shape applies in the `/link/fetch` response below.

Send `shortUrl` to the customer via your own channels, or rely on Paytm's SMS/email dispatch.

---

## Fetch link details

```
POST {pgDomain}/link/fetch
```

```json
{
  "head": { "tokenType": "AES", "signature": "<sig>" },
  "body": {
    "mid": "YOUR_MID",
    "linkId": 31309
  }
}
```

`linkId` is a **JSON number**. Quoting it (`"31309"`) returns "invalid link id".

### Fetch response shape - read carefully

```json
{
  "head": { "responseTimestamp": "...", "signature": "..." },
  "body": {
    "resultInfo": { "resultStatus": "SUCCESS", "resultCode": "200", "resultMsg": "Success" },
    "links": [
      {
        "linkId": 31309,
        "linkType": "FIXED",
        "isActive": true,           // some MIDs use this; others return linkStatus: "ACTIVE"
        "amount": "499.00",
        "shortUrl": "https://paytm.me/XXXXXXX",
        "longUrl": "https://...",
        "expiryDate": "30/12/2026 23:59:59",
        "transactions": [],
        "merchantUniqueReference": "INV-001-v1"
      }
    ]
  }
}
```

> **⚠️ The link is wrapped in `body.links[0]`, not `body` directly.** Reading `json.body.linkStatus` returns `undefined`. Read `json.body.links[0]` first (and similarly for every other link field). The array is always length 1 for fetch (single-link lookup) but the wrapper is always there.
>
> **Status field is dual-shape — normalize on read:**
>
> ```js
> const link = body.links?.[0];
> const linkStatus = link?.linkStatus
>   ?? (link?.isActive === true ? "ACTIVE" : link?.isActive === false ? "INACTIVE" : "UNKNOWN");
> ```

---

## Update a link

```
POST {pgDomain}/link/update
```

```json
{
  "head": { "tokenType": "AES", "signature": "<sig>" },
  "body": {
    "mid": "YOUR_MID",
    "linkId": 31309,
    "amount": "599.00",
    "expiryDate": "15/01/2027 23:59:59",
    "linkDescription": "Updated invoice description"
  }
}
```

Only some fields are mutable post-creation (amount, expiry, description, customer contact). Trying to change `linkType` or `orderId` returns an error.

---

## Resend the link notification (SMS / email)

```
POST {pgDomain}/link/resendNotification
```

> **Endpoint slug is `resendNotification`, NOT `resend`.** Wrong path → 404 / invalid endpoint error.

```json
{
  "head": { "tokenType": "AES", "signature": "<sig>" },
  "body": {
    "mid": "YOUR_MID",
    "linkId": 31309,
    "sendSms": true,
    "notifyContact": {
      "customerMobile": "9999999999",
      "customerEmail": "buyer@example.com"
    }
  }
}
```

Use this if the original SMS/email didn't reach the customer, or to nudge unpaid invoices. Same DLT-template caveat as `create` - SMS may be silently dropped if templates aren't approved.

---

## Expire / cancel a link

```
POST {pgDomain}/link/expire
```

```json
{
  "head": { "tokenType": "AES", "signature": "<sig>" },
  "body": {
    "mid": "YOUR_MID",
    "linkId": 31309
  }
}
```

Idempotent. Once expired, payers see "link no longer active". You cannot un-expire - create a new link.

---

## Fetch transactions for a link (reconciliation)

> **Use this for Payment Link reconciliation, not `/v3/order/status`.** `/v3/order/status` exists for one-time-payment / JS-Checkout flows where you already know the merchant `orderId`. For Payment Links - especially `REUSABLE` and `OPEN` types where many payers may pay against the same link - `/link/fetchTransaction` is the right endpoint. It returns every order made against the link in a single call, paginated.

```
POST {pgDomain}/link/fetchTransaction
```

Doc: <https://www.paytmpayments.com/docs/api/fetch-transaction-link-api?ref=paymentLinks>

```json
{
  "head": {
    "tokenType": "AES",
    "signature": "<sig>"
  },
  "body": {
    "mid": "YOUR_MID",
    "linkId": 31309,
    "pageNo": 1,
    "pageSize": 10,
    "fetchAllTxns": true
  }
}
```

| Field | Required | Notes |
|---|---|---|
| `mid` | ✅ | Merchant ID |
| `linkId` | ✅ | **JSON number** (long), NOT a string - same rule as fetch / update / expire |
| `pageNo` | optional | 1-indexed; defaults to 1 |
| `pageSize` | optional | Up to ~50; defaults vary by MID |
| `fetchAllTxns` | optional | `true` returns all orders against the link; `false` (default) returns only successful ones |
| `head.tokenType` | ✅ | Always `"AES"` |
| `head.signature` | ✅ | CHECKSUMHASH over `body` |
| `head.timestamp` / `clientId` / `version` / `channelId` | optional | Standard Paytm head extras |

### Response shape - orders are wrapped in `body.orders[]`

```json
{
  "head": { "tokenType": "AES", "signature": "..." },
  "body": {
    "resultInfo": {
      "resultCode": "200",
      "resultStatus": "SUCCESS",
      "resultMessage": "Success"
    },
    "orders": [
      {
        "txnId": "20260504000000000001",
        "orderId": "ORD_INV_001",
        "mercUniqRef": "INV-001-v1",
        "orderStatus": "SUCCESS",
        "txnAmount": 499.00,
        "orderCreatedTime": "2026-05-04 14:32:11",
        "customerName": "Buyer Name",
        "customerEmail": "buyer@example.com",
        "customerPhoneNumber": "9999999999",
        "customerId": "CUST_001",
        "payableAmount": 499.00
      }
    ]
  }
}
```

> **`body.orders[]` is always an array**, even when only one order exists. Iterate; don't index by ordinal in production code.
>
> **⚠️ `orderStatus` is dual-shape — match BOTH `"SUCCESS"` and `"TXN_SUCCESS"`.** The `/link/fetchTransaction` endpoint returns `orderStatus: "SUCCESS"` for paid links on most MIDs; some return `"TXN_SUCCESS"` (the value you'd see from `/v3/order/status` and the JS Checkout `transactionStatus` callback). The two surfaces are not normalised on Paytm's side. Match both in your reconciliation:
>
> ```js
> const PAID = new Set(["SUCCESS", "TXN_SUCCESS"]);
> const FAILED = new Set(["FAILURE", "TXN_FAILURE", "FAILED"]);
> const paidOrders = orders.filter(o => PAID.has(o.orderStatus));
> ```
>
> Hard-coding only `"TXN_SUCCESS"` (as some older snippets show) silently classifies every paid link as unpaid on these MIDs — money is received but your DB never marks it. **Verify with both values before fulfilling.**

### Error codes (Payment Link APIs)

| `resultCode` | Where | Meaning | Action |
|---|---|---|---|
| `200` | All | Success | Proceed |
| `404` | Fetch Transaction | Data Not Found - no transactions yet for this link | Treat as "not paid yet"; poll later or wait for webhook |
| `5007` | Create / Update | `link name contains special character` | `linkName` must be alphanumerics ONLY on this MID — strip spaces too. See warning #5 |
| `5021` | Create / Update | `Date should be in format DD/MM/YYYY` | Switch `expiryDate` to `DD/MM/YYYY HH:MM:SS` |
| `5028` | All | Checksum invalid | Re-sign the body; check that you're hashing the same bytes you POST |
| `5082` | Update | Amount-update rejected | You're trying to update `amount` on a `GENERIC` (open-amount) link; switch to `FIXED` on create |
| `501` | All | Internal Server Error | Transient; retry |

---

## After payment

The post-payment flow for Payment Links:

1. Customer opens the link → Paytm-hosted checkout → pays.
2. Paytm POSTs to your `callbackUrl` (browser redirect) with the same UPPERCASE field set as JS Checkout: `ORDERID`, `TXNID`, `STATUS`, `RESPCODE`, `CHECKSUMHASH`, etc.
3. **Verify CHECKSUMHASH**, then call **`/link/fetchTransaction`** server-to-server to confirm - it returns the order(s) in `body.orders[]` with `orderStatus`, `txnAmount`, `txnId`, customer details. Use that as the source of truth before fulfilling. **Treat the order as paid if `orderStatus` matches EITHER `"SUCCESS"` OR `"TXN_SUCCESS"`** — the value depends on MID and is not normalized by Paytm. (Do NOT use `/v3/order/status` for Payment Link reconciliation - that endpoint is for one-time-payment / JS-Checkout flows.)
4. Webhook (if configured) gives you the same data reliably without polling.

---

## Endpoint reference

| Action | Path | Identifier |
|---|---|---|
| Create | `POST /link/create` | n/a |
| Fetch link details | `POST /link/fetch` | `linkId` (number) |
| Update | `POST /link/update` | `linkId` (number) |
| Resend notification | `POST /link/resendNotification` | `linkId` (number) |
| Expire | `POST /link/expire` | `linkId` (number) |
| **Fetch transactions (reconcile)** | `POST /link/fetchTransaction` | `linkId` (number) |

---

## Pitfalls

1. **`linkId` MUST be a JSON number** in fetch / update / resend / expire calls. Quoting it as a string is the #1 cause of "invalid link id" responses.
2. **Response key is `linkId` (camelCase)** in current Paytm responses; some legacy / staging variants return `LinkID`. Read defensively (`body.linkId ?? body.LinkID`); always send `linkId` on subsequent calls.
3. **`head.tokenType: "AES"` is required on every call.** Omitting it returns `"Invalid tokenType"`. Easy to miss because the field isn't called out in older Paytm samples.
4. **`linkName` and `linkDescription` have different charset rules in practice — sanitize separately.** `linkName` accepts alphanumerics ONLY (some MIDs reject space as a special character despite Paytm docs claiming it's allowed). `linkDescription` accepts alphanumerics + spaces. Both ≥ 3 chars. Never pass raw user input through.
5. **Fetch response wraps the link in `body.links[0]`**, not `body` directly. `json.body.linkStatus` is `undefined`; you must read `json.body.links[0]` first. The status field within is **dual-shape**: `linkStatus: "ACTIVE"` on some MIDs, `isActive: true` on others. Normalize: `link.linkStatus ?? (link.isActive ? "ACTIVE" : "INACTIVE")`.
6. **Customer details must be nested in `customerContact`.** Putting `customerMobile` / `customerEmail` / `customerName` at the top level of `body` is silently accepted but Paytm never dispatches the SMS / email. The link is created but the customer is never notified.
7. **Create-link `amount` is a JSON number**, not a string. `499.00` works; `"499.00"` may fail validation. (Different from `txnAmount.value` in Initiate Transaction, which IS a string.)
8. **`head.timestamp` is required on create-link** per the official doc - Unix epoch seconds as a string.
9. **`orderId` reconciles to a single payment for one-shot links** - for reusable/multi-payer links iterate `transactions[]` from the fetch response.
10. **Expired links can't be charged.** Build a renewal job for unpaid invoices instead of relying on long expiry windows.
11. **Open-amount links** (no fixed `amount`, only `minAmount`/`maxAmount`) are fraud-prone - set tight bounds and verify the paid amount server-side.
12. **SMS dispatch requires DLT-registered templates** on the Paytm side (Indian regulation). New merchants may see SMS silently dropped until templates are approved on the dashboard.
13. **`shortUrl` redirects to a long URL on the PG host** - link previews (WhatsApp, iMessage) hit the long URL, which can affect link analytics if you depend on click-through tracking.
14. **Update can't change `linkType` or `orderId`** - only mutable fields (amount, expiry, description, contact).
15. **Reconcile via `/link/fetchTransaction`, not `/v3/order/status`.** The link product has its own transactions endpoint that returns every order (paginated) under `body.orders[]`. `/v3/order/status` is for one-time-payment / JS-Checkout flows where you already know the merchant `orderId`; for Payment Links - especially `REUSABLE` / `OPEN` links with multiple payers - `/link/fetchTransaction` gives you the full list in a single call.
16. **Fetch-transaction response wraps orders in `body.orders[]`**, always an array (even when one order). Iterate; don't index by ordinal.
17. **`404` from fetch-transaction is "no transactions yet" - not an error.** Treat as "link not paid yet" and poll later or wait for the webhook.
18. **`orderStatus` from `/link/fetchTransaction` is dual-shape — match BOTH `"SUCCESS"` AND `"TXN_SUCCESS"`.** Hard-coding only `"TXN_SUCCESS"` (the value JS Checkout / `/v3/order/status` use) silently classifies every paid link as unpaid on MIDs that return `"SUCCESS"` here. Money received, system says no — a silent business bug.
19. **`isActive` (boolean) vs `linkStatus` (string)** — both create-link and fetch-link responses use one or the other depending on MID. Read defensively (`linkStatus ?? (isActive ? "ACTIVE" : "INACTIVE")`).
20. **Error code `5007`: "link name contains special character"** — `linkName` rejected. On many MIDs, **space is treated as a special character** even though Paytm's docs say spaces are allowed. Strip spaces from `linkName` (use `[A-Za-z0-9]` only); keep them only in `linkDescription`.
