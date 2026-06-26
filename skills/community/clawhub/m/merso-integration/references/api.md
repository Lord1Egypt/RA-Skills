# Merso API Reference & Integration Guide

## Base URLs
- **Production:** `https://api2.merso.io`
- **Development:** `https://api2.dev.merso.io`

---

## Authentication

```http
POST /auth
Content-Type: application/json

{ "game_id": "<MERSO_GAME_ID>", "api_key": "<MERSO_API_KEY>" }
```

Response:
```json
{ "authResult": { "token": "...", "expires_at": "..." } }
```

- Use as `Authorization: Bearer <token>` on all subsequent requests
- Cache the token; auto-renew 30 min before `expires_at`

---

## Initiate Purchase

```http
POST /merso-buy-item
Authorization: Bearer <token>
Content-Type: application/json

{
  "itemPrice": 9.99,
  "itemId": "GAME-1712345678-AB3X",
  "itemName": "Gold Pack 1000",
  "playerEmail": "user@example.com",
  "playerLevel": "3",
  "playerCountry": "ESP",
  "paymentMode": "UPFRONT"
}
```

Response:
```json
{ "paymentIntentId": "pi_xxx", "clientSecret": "pi_xxx_secret_yyy", "totalAmount": 9.99 }
```

**Field notes:**
- `itemId` — must be **unique per purchase**. Generate as `{PREFIX}-{timestamp}-{random}` (e.g. `DG-1712345678-AB3X`) — API requirement
- `playerLevel` — string `"1"` to `"5"`
- `playerCountry` — ISO 3166-1 alpha-3 (e.g. `"ESP"`, `"USA"`, `"IDN"`)
- `paymentMode` — `"UPFRONT"` (pay full amount now) or `"INSTALLMENTS"` (PNPL flow — see below)
- `itemPrice` — in EUR or USD depending on merchant config

---

## INSTALLMENTS Mode (PNPL Flow)

Use `paymentMode: "INSTALLMENTS"` to enable the Play Now, Pay Later flow.

### How it works
- Player pays **first installment upfront** (typically ~50% of total price)
- Merso automatically charges remaining installments on a weekly schedule
- **License is granted immediately** after the first payment — player gets access right away
- If a subsequent payment fails → license expires automatically (no merchant action needed)
- Ownership fully transfers once all installments complete

### API call — same endpoint, different mode

```http
POST /merso-buy-item
Authorization: Bearer <token>
Content-Type: application/json

{
  "itemPrice": 19.99,
  "itemId": "GAME-1712345678-CD7Y",
  "itemName": "Premium Hero Pack",
  "playerEmail": "user@example.com",
  "playerLevel": "4",
  "playerCountry": "ESP",
  "paymentMode": "INSTALLMENTS"
}
```

Response is identical to UPFRONT:
```json
{ "paymentIntentId": "pi_xxx", "clientSecret": "pi_xxx_secret_yyy", "totalAmount": 19.99 }
```

- `totalAmount` is the **full item price** — Merso splits it internally
- Use `clientSecret` the same way with Stripe Elements on the frontend
- Player sees the installment plan breakdown in the Merso-powered payment UI

### Frontend — Stripe Elements (same as UPFRONT)

```js
const stripe = Stripe('<your-publishable-key>');
const elements = stripe.elements({ clientSecret });
// Mount card element and confirm payment as normal
// Merso handles the installment schedule from here
```

### Webhook events for INSTALLMENTS

Merso fires a webhook for **each individual payment event** in the installment schedule:

| Event | Action |
|---|---|
| First `payment.succeeded` | Grant item/license access to player |
| Subsequent `payment.succeeded` | Log / extend license — usually no action required |
| `payment.refunded` | Revoke license, deduct item/credits |
| `payment.failed` (via verify endpoint) | License expires automatically — optionally notify player |

> Merso handles license expiry enforcement automatically.

### UPFRONT vs INSTALLMENTS — when to use each

| Scenario | Mode |
|---|---|
| Low-price items (<$10) | `UPFRONT` |
| High-ticket items ($15+) where price is limiting conversion | `INSTALLMENTS` |
| Web3 / NFT assets with high upfront cost | `INSTALLMENTS` |
| Quick one-time purchases | `UPFRONT` |

---

## Verify Payment

```http
GET /verify-payment-intent/:paymentIntentId
Authorization: Bearer <token>
```

Use as fallback if webhook doesn't arrive within expected time.

---

## Configure Webhook

```http
POST /set-webhook-url
Authorization: Bearer <token>
Content-Type: application/json

{ "url": "https://yourdomain.com/api/payments/webhook" }
```

---

## Webhook Payload (Incoming)

```json
{
  "paymentIntentId": "pi_xxx",
  "status": "succeeded",
  "type": "payment.succeeded"
}
```

Possible values:
- `type`: `payment.succeeded` | `payment.refunded`
- `status`: `succeeded` | `refunded` | `failed`

---

## Webhook Security & Verification

Before processing any webhook event, verify that the request genuinely comes from Merso.

- Merso may include a signature header (e.g. `X-Merso-Signature`) with an HMAC-SHA256 of the raw request body signed with your `MERSO_API_KEY`. Confirm with Merso whether this is available.
- If signatures are supported, always verify before acting:

```js
const crypto = require('crypto');

function verifyMersoWebhook(rawBody, signatureHeader, secret) {
  const expected = crypto
    .createHmac('sha256', secret)
    .update(rawBody)
    .digest('hex');
  return crypto.timingSafeEqual(
    Buffer.from(expected),
    Buffer.from(signatureHeader)
  );
}

app.post('/api/payments/webhook', express.raw({ type: 'application/json' }), (req, res) => {
  const sig = req.headers['x-merso-signature'];
  if (sig && !verifyMersoWebhook(req.body, sig, process.env.MERSO_API_KEY)) {
    return res.status(401).json({ error: 'Invalid signature' });
  }
  // process event
});
```

- If Merso does not provide signatures, restrict your webhook endpoint by IP allowlist (ask Merso for their outbound IP ranges).

---

## Full Integration Flow

```
1. Player selects item → frontend calls POST /api/your-initiate-endpoint
2. Backend authenticates with Merso (cached token)
3. Backend calls POST /merso-buy-item → receives { paymentIntentId, clientSecret }
4. Frontend shows payment UI (Stripe Elements with clientSecret)
5. Player completes payment
6. Merso fires POST /your-webhook-url with payment result
7. Backend grants item/license to player
8. Fallback: if webhook not received, poll GET /verify-payment-intent/:id
```

---

## DB Schema (Reference)

```sql
-- Payment records
CREATE TABLE merso_payments (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL,
  payment_intent_id VARCHAR(255) UNIQUE NOT NULL,
  item_id VARCHAR(255),
  amount DECIMAL(10,2),
  player_email VARCHAR(255),
  status VARCHAR(50) DEFAULT 'pending', -- pending | completed | failed | refunded
  completed_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Ledger
CREATE TABLE item_transactions (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL,
  type VARCHAR(50),  -- purchase | refund | spend
  reference_id INTEGER,
  created_at TIMESTAMP DEFAULT NOW()
);
```

---

## Environment Variables

```env
MERSO_ENV=production          # or: development
MERSO_GAME_ID=your_game_id
MERSO_API_KEY=your_api_key
```
