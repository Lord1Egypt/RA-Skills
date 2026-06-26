# Paytm QR Codes (Dynamic & Static)

> _Companion to **`SKILL.md`** - load this file alongside `SKILL.md`, never instead of it._

For in-person, kiosk, table-top, or social-commerce flows where the customer scans with any UPI app.

---

## Static vs Dynamic

| | Static QR | Dynamic QR |
|---|---|---|
| Amount | Customer enters | Pre-set per QR |
| Reuse | Many payments per QR | One QR per intended payment |
| API | Generated once on dashboard | Generated per order via API |
| Reconciliation | All payments to same VPA - disambiguate via webhook `orderId` (if you encode one) or amount + time | Each QR has a unique orderId |
| Use case | Counter, menu, tip jar | Restaurant bill, kiosk, invoice scan |

---

## Generate a Dynamic QR

> **⚠️ Common 400 causes (read first):**
> - **`posId` is REQUIRED** - omitting it returns HTTP 400. Use any non-empty terminal identifier (`"POS001"`, `"COUNTER_07"`, etc.) even for software-only setups.
> - **`amount` MUST be a string** with two decimals (`"499.00"`), not a number (`499` / `499.00`).
> - **`head` requires `clientId` and `version`** in addition to `signature`.
> - **`businessType` must be exactly `"UPI_QR_CODE"`** - case-sensitive.
>
> **⚠️ Don't forget post-payment polling.** Generating a QR doesn't auto-notify the browser when the customer pays - your page will be stuck on "Processing…" forever unless you poll Transaction Status (or wire up a webhook). See "Detecting payment completion" below.

```
POST {pgDomain}/paymentservices/qr/create
Content-Type: application/json
```

```json
{
  "head": {
    "clientId": "C11",
    "version": "v1",
    "signature": "<CHECKSUMHASH over JSON.stringify(body)>"
  },
  "body": {
    "mid": "YOUR_MID",
    "orderId": "QR_ORD_001",
    "amount": "499.00",
    "businessType": "UPI_QR_CODE",
    "posId": "POS001"
  }
}
```

| Field | Required | Notes |
|---|---|---|
| `mid` | ✅ | Merchant ID |
| `orderId` | ✅ | Unique per QR (single-use semantics) |
| `amount` | ✅ | **String**, two decimals; INR only (`"499.00"`, not `499`) |
| `businessType` | ✅ | Exactly `"UPI_QR_CODE"` |
| `posId` | ✅ | Terminal / store identifier - **must be non-empty** even if you don't have physical POS |
| `head.clientId` | ✅ | **Per-merchant - issued by Paytm during onboarding.** `"C11"` is common for single-merchant-key setups but NOT a universal default. Confirm yours with your Paytm KAM; staging often accepts `"C11"` even when prod rejects it |
| `head.version` | ✅ | `"v1"` |
| `displayName` | optional | What the customer sees in their UPI app (≤ 30 chars) |
| `expiryDate` | optional | `yyyy-MM-dd HH:mm:ss` IST |
| `imageRequired` | optional | Boolean - when `true`, response includes base64 PNG |
| `orderDetails` / `invoiceDetails` | optional | Free-form objects for receipt context |
| `additionalInfo` / `gstInformation` | optional | Per-merchant metadata |

### Response

```json
{
  "head": { "responseTimestamp": "...", "signature": "..." },
  "body": {
    "resultInfo": { "resultStatus": "SUCCESS", "resultCode": "QR_0001" },
    "qrCodeId": "<paytm qrCodeId>",
    "qrData": "upi://pay?pa=...&pn=...&am=499.00&tr=...",
    "image": "iVBORw0KGgoAAAANSUhEUgAA..."
  }
}
```

> **⚠️ `image` is RAW base64 - no data-URI prefix.** Paytm returns the string `iVBOR...` (the bare base64 payload), **not** `data:image/png;base64,iVBOR...`. Pasting it directly into an `<img src>` tag silently fails to render. You must add the prefix yourself before serving it to the browser.

### Rendering the QR - the right way

**Server-side** (recommended - fix once, frontend stays simple):

```javascript
// Node example - in your /paytm/create-qr handler
const json = await paytmCreateQr(...);
const rawImage = json.body.image;
res.json({
  qrCodeId: json.body.qrCodeId,
  qrData: json.body.qrData,
  image: `data:image/png;base64,${rawImage}`   // <-- add prefix here
});
```

```python
# Flask example
out = paytm_create_qr(...)
return jsonify({
    "qrCodeId": out["body"]["qrCodeId"],
    "qrData": out["body"]["qrData"],
    "image": f"data:image/png;base64,{out['body']['image']}"
})
```

```java
// Spring example
String img = "data:image/png;base64," + json.path("body").path("image").asText();
```

**Frontend** then just does:

```html
<img src="<image-from-backend>" alt="Scan to pay" />
```

Alternatively, ignore `image` entirely and generate your own QR from `qrData` using any QR library - `qrData` is a standard UPI deep-link (`upi://pay?pa=...&pn=...&am=499.00&tr=...`).

---

## Fetch QR status

```
POST {pgDomain}/paymentservices/qr/status
```

```json
{
  "head": { "signature": "<sig>" },
  "body": { "mid": "YOUR_MID", "qrCodeId": "<paytm qrCodeId>" }
}
```

Response carries `qrCodeStatus` and (once paid) the underlying `txnId` / `orderId` of the completed payment.

---

## Detecting payment completion (the "stuck on Processing…" fix)

**Symptom:** Customer scans the QR, pays via UPI, but the merchant page is stuck showing "Payment processing…" indefinitely.

**Cause:** Generating a Dynamic QR doesn't open any merchant-side payment session - there's no JS Checkout, no `transactionStatus` callback, no automatic browser-side notification when payment completes. Your screen has no way of knowing the customer paid unless **your code asks**.

**Two ways to close the loop, pick one:**

### Option A - Frontend polling (simplest, recommended for in-store / kiosk UX)

After rendering the QR, poll your backend's status endpoint every 3–5 seconds. Backend forwards the call to Paytm's `/v3/order/status` (or `/paymentservices/qr/status`).

```javascript
// Frontend, after rendering the QR image
const orderId = "QR_ORD_001";
const POLL_INTERVAL_MS = 3000;
const POLL_TIMEOUT_MS = 5 * 60 * 1000;   // 5 min - match QR expiry
const startedAt = Date.now();

async function pollOnce() {
  if (Date.now() - startedAt > POLL_TIMEOUT_MS) {
    setUi("EXPIRED", "QR expired. Please request a new one.");
    return;
  }
  const r = await fetch("/paytm/qr-status", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ orderId })
  });
  const data = await r.json();
  // Paytm Transaction Status response - look at body.resultInfo.resultStatus
  const status = data?.body?.resultInfo?.resultStatus;
  if (status === "TXN_SUCCESS") {
    setUi("PAID", "Payment received. Thank you!");
    return;
  }
  if (status === "TXN_FAILURE") {
    setUi("FAILED", "Payment failed. Please try again.");
    return;
  }
  // PENDING or no-txn-yet - keep polling
  setTimeout(pollOnce, POLL_INTERVAL_MS);
}
pollOnce();
```

The backend `/paytm/qr-status` route is just a thin wrapper that calls Paytm's Transaction Status API server-side (so the merchant key never reaches the browser):

```javascript
// Node - backend route
app.post("/paytm/qr-status", async (req, res) => {
  const { orderId } = req.body;
  const body = { mid: cfg.mid, orderId };
  const signature = await PaytmChecksum.generateSignature(JSON.stringify(body), cfg.merchantKey);
  const r = await fetch(`${cfg.pgDomain}/v3/order/status`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ head: { signature }, body })
  });
  res.type("application/json").send(await r.text());
});
```

**Always stop polling on a terminal state** (`TXN_SUCCESS` / `TXN_FAILURE`) and on timeout - runaway pollers are the second-most-common bug after the original "stuck screen".

### Option B - Webhook + SSE / WebSocket push (best UX, more setup)

Configure Paytm's QR Payment webhook on the dashboard. When Paytm POSTs payment confirmation to your backend, push the event over SSE / WebSocket / Pusher / Ably to the open browser session keyed by `orderId`. The screen updates instantly with no polling.

Use Option A for vibe-coded kiosks and demo flows; Option B when polling cost / latency matters.

---

## Static QR

Generate once on the dashboard → print → mount. All payments to it land in the same Paytm-side merchant VPA, surfaced via:

- Webhook `STATIC_QR_PAYMENT` event with the customer's UPI ref + amount + time
- Daily Settlement Report

For "which customer paid?" you have to use customer-supplied context (table number on receipt, name in UPI note) since the merchant cannot pre-bind an orderId.

---

## Pitfalls

1. **`posId` is required** - most common cause of HTTP 400 on QR generation. Always send a non-empty value.
2. **`amount` must be a string with two decimals.** `"499.00"` works; `499`, `499.0`, `"499"` all fail.
3. **`head.clientId` and `head.version` are required**, not just `signature`.
4. **`image` field is raw base64 with NO `data:image/png;base64,` prefix** - pasting it straight into `<img src>` renders nothing. Prepend the prefix in your backend handler before sending the response to the frontend (see "Rendering the QR - the right way" above).
5. **`orderId` is single-use** for dynamic QRs even if the customer never pays - generate a new one for retry.
6. **UPI deep-links are time-sensitive.** Some apps cache; always re-render on retry rather than reusing an old `qrData`.
7. **Don't expose `qrCodeId` as a customer-facing reference** - use your own `orderId`.
8. **Static QR amount changes** on the dashboard apply going forward only - in-flight scans use the value at scan time.
9. **Refunds for QR payments** go through the standard `/refund/apply` flow using the resulting `orderId` + `txnId`.
10. **Some UPI apps strip `displayName`** and show only the merchant VPA - don't put critical info there.
11. **No automatic post-payment notification.** Unlike JS Checkout (which fires `transactionStatus` in the browser), QR generation gives you no client-side hook for payment completion. You must poll `/v3/order/status` from the frontend or wire up a webhook + push channel - otherwise your "Payment processing…" screen stays up forever.
