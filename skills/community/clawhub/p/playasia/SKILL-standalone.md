---
name: playasia-api
description: Search and buy digital game codes, eShop cards, PSN vouchers from Play-Asia.com via HTTP. Works with any agent — no MCP server needed. Browse the catalog, purchase with your wallet, track orders, retrieve codes, and contact customer service.
homepage: https://www.play-asia.com/l402
metadata: {"openclaw":{"requires":{"env":["PA_TOKEN"]},"primaryEnv":"PA_TOKEN"}}
---

# Playasia API — Standalone Skill

Buy digital game codes, eShop cards, PSN vouchers, and more via direct HTTP calls. No MCP server required.

## Base URL

```
https://www.play-asia.com/l402/v1
```

## Getting started

1. Generate a platform token at https://www.play-asia.com/account/access-tokens
2. Pass it as a header: `X-PA-Token: pa_xxx`

Browsing the catalog is free and needs no token. Purchasing, orders, and customer service require a token.

For Bitcoin Lightning users, anonymous purchases are also supported via the L402 protocol (see bottom of this document).

---

## Endpoints

### Search products (free, no auth)

```
GET /l402/v1/catalog?q={query}&limit={n}&offset={n}&currency={code}
```

Returns digital products with prices in USD and satoshis, cover image, and popularity rank.

Example: `GET /l402/v1/catalog?q=Nintendo+eShop&limit=5`

Response:
```json
{
  "products": [
    {
      "pax": "PAX0004012102",
      "name": "Nintendo eShop Card 5000 YEN",
      "image_url": "https://s.pacn.ws/1/p/...jpg",
      "rank": 1234,
      "price": { "usd": 40.55, "sats": 58694, "btc": "0.00058694" },
      "in_stock": 1,
      "buy_url": "/l402/v1/buy/PAX0004012102"
    }
  ],
  "count": 5, "total": 1843, "offset": 0, "limit": 5
}
```

`rank` is the popularity rank (lower = more popular, `null` if unranked). `image_url` is the product cover image (`null` if none).

### Get product price (free, no auth)

```
GET /l402/v1/price?pax={PAX_CODE}&currency={code}
```

`currency` is optional (e.g. `KRW`, `EUR`, `JPY` — comma-separated for multiple). When given, the response includes a `price` object with local currency prices.

Response (with `&currency=KRW`):
```json
{
  "product": {
    "pax": "PAX0004012102",
    "name": "Nintendo eShop Card 5000 YEN",
    "digital": 1,
    "image_url": "https://s.pacn.ws/1/p/...jpg",
    "price_usd": 40.55,
    "price_sats": 58694,
    "in_stock": 1,
    "buy_url": "/l402/v1/buy/PAX0004012102",
    "price": { "usd": 40.55, "sats": 58694, "krw": 63500 }
  }
}
```

### Get wallet balance (requires X-PA-Token)

```
GET /l402/v1/account/balance
X-PA-Token: pa_xxx
```

Response:
```json
{ "balances": [{ "currency": "USD", "amount": 150.00 }] }
```

### Wallet transaction history (requires X-PA-Token)

```
GET /l402/v1/account/transactions?limit=20&offset=0
X-PA-Token: pa_xxx
```

Response:
```json
{
  "transactions": [
    { "id": 443, "amount": 4.00, "text": "Top-up", "date": "2025-12-26 20:24:11", "currency": "USD", "source": null },
    { "id": 444, "amount": -38.99, "text": "L402 Platform: Order #64596629", "date": "2026-03-22 18:38:01", "currency": "USD", "source": "l402_platform" }
  ],
  "count": 2,
  "offset": 0
}
```

Positive = top-up, negative = purchase.

### Buy with wallet (requires X-PA-Token with "purchase" scope)

```
POST /l402/v1/account/buy
X-PA-Token: pa_xxx
Content-Type: application/json

{ "pax": "PAX0004012102" }
```

Response:
```json
{
  "order_id": 9876544,
  "product": "Nintendo eShop Card 5000 YEN",
  "price": 40.55,
  "status": "Digital Download",
  "delivery": { "type": "text", "code": "XXXX-XXXX-XXXX-XXXX" }
}
```

Token must have `purchase` scope. Daily/weekly spending limits are enforced if configured.

### List orders (requires X-PA-Token)

```
GET /l402/v1/account/orders?limit=20&offset=0
X-PA-Token: pa_xxx
```

### Get order detail + digital codes (requires X-PA-Token)

```
GET /l402/v1/account/order?oid={ORDER_ID}
X-PA-Token: pa_xxx
```

Returns items, status, shipping tracking, and purchased digital content:
```json
{
  "order_id": 64596629,
  "status": "Digital Download",
  "date": "2026-03-22 18:38:01",
  "total": "40.39",
  "currency": "USD",
  "items": [
    {
      "pax": "PAX0004012102",
      "name": "Nintendo eShop Card 5000 YEN",
      "quantity": 1,
      "price": "38.99",
      "delivery": { "type": "text", "code": "XXXX-XXXX-XXXX-XXXX" }
    }
  ],
  "tracking": [
    {
      "tracking_number": "1Z999AA10123456784",
      "method": "FedEx",
      "date": "2026-03-25 10:30:00",
      "progress": "DELIVERED",
      "delivered": "2026-03-27 14:22:00"
    }
  ]
}
```

`delivery` is present for fulfilled digital items. Image codes return `{ "type": "image", "content_type": "image/png", "data": "<base64>" }`. `tracking` is present for shipped physical orders.

### Submit customer service enquiry (requires X-PA-Token)

```
POST /l402/v1/cs/submit
X-PA-Token: pa_xxx
Content-Type: application/json

{
  "subject": "Wrong code received",
  "message": "I received an expired code for order #12345678.",
  "reference": "#12345678",
  "attachments": [
    {
      "filename": "screenshot.png",
      "content_type": "image/png",
      "data": "<base64-encoded file>"
    }
  ]
}
```

- `reference` is required. Use `#ORDER_ID` for order issues, or free text.
- `attachments` is optional. Max 5 files, max 5MB each, base64-encoded.
- If an open ticket with the same reference exists, the message is appended to it.

### List enquiries (requires X-PA-Token)

```
GET /l402/v1/cs/enquiries?status=open
X-PA-Token: pa_xxx
```

### Get enquiry thread (requires X-PA-Token)

```
GET /l402/v1/cs/enquiry?id={TICKET_ID}
X-PA-Token: pa_xxx
```

### Reply to enquiry (requires X-PA-Token)

```
POST /l402/v1/cs/reply
X-PA-Token: pa_xxx
Content-Type: application/json

{ "ticket_id": 123456, "message": "Here is the additional information you requested." }
```

### Close enquiry (requires X-PA-Token)

```
POST /l402/v1/cs/close
X-PA-Token: pa_xxx
Content-Type: application/json

{ "ticket_id": 123456 }
```

### L402 pricing (free)

```
GET /l402/v1/pricing
```

### Exchange rates (L402, ~1 sat)

```
GET /l402/v1/btc/rates
```

Returns BTC rates for 30+ fiat currencies, plus a `crypto` section with ETH and SOPH rates (each in USD, sats, and BTC).

---

## Bitcoin / Lightning tools (all via /l402/v1/)

| Endpoint | Price | Description |
|----------|-------|-------------|
| `/l402/v1/btc/blockheight` | 1 sat | Block height + chain info |
| `/l402/v1/btc/fees` | 1 sat | Fee estimates |
| `/l402/v1/btc/mempool` | 1 sat | Mempool stats |
| `/l402/v1/btc/rates` | 1 sat | BTC/fiat rates (30+ currencies) + ETH/SOPH crypto rates |
| `/l402/v1/btc/block?height={n}` | 2 sats | Block data |
| `/l402/v1/btc/validate-address?addr={addr}` | 1 sat | Validate address |
| `/l402/v1/btc/decode-tx?hex={rawtx}` | 2 sats | Decode transaction |
| `/l402/v1/btc/broadcast-tx` (POST) | 10 sats | Broadcast transaction |
| `/l402/v1/btc/utxo?txid={txid}&vout={n}` | 1 sat | Check UTXO |
| `/l402/v1/ln/decode-invoice?invoice={bolt11}` | 2 sats | Decode Lightning invoice |
| `/l402/v1/ln/node-info` | 1 sat | Node info + capacity |
| `/l402/v1/ln/node-lookup?pubkey={hex}` | 2 sats | Lookup Lightning node |
| `/l402/v1/ln/query-route?dest={pubkey}&amt={sats}` | 2 sats | Find route |

---

## Error responses

All errors return JSON:
```json
{ "error": "error_code", "message": "Human-readable description" }
```

| HTTP | Meaning |
|------|---------|
| 400 | Bad request (missing/invalid parameters) |
| 401 | Unauthorized (missing or invalid X-PA-Token) |
| 402 | Payment required (L402 — pay the returned invoice) |
| 404 | Not found |
| 429 | Rate limited |
| 503 | Service unavailable |

---

## Buy with Lightning (L402) — no account needed

For Bitcoin Lightning users. Two-step flow:

**Step 1** — request invoice:
```
GET /l402/v1/product?pax={PAX_CODE}
```
Response (HTTP 402):
```json
{
  "type": "payment_required",
  "price_sat": 58694,
  "invoice": "lnbc586940n1p...",
  "macaroon": "AgEFdGVzdA...",
  "payment_hash": "abc123..."
}
```

**Step 2** — pay the invoice with any Lightning wallet, get the preimage, then:
```
GET /l402/v1/product?pax={PAX_CODE}
Authorization: L402 AgEFdGVzdA...:def456...
```
Response:
```json
{
  "status": "delivered",
  "product": "Nintendo eShop Card 5000 YEN",
  "delivery": { "type": "text", "code": "XXXX-XXXX-XXXX-XXXX" },
  "order_id": 9876543
}
```

---

## Rate limits

- Token creation: 5/hour
- Purchases: 30/hour
- CS enquiry submission: 10/hour
- CS replies: 20/hour

## Getting a platform token

1. Go to https://www.play-asia.com/account/access-tokens
2. Log in if needed
3. Choose scope: **Info** (read-only) or **Purchase** (can spend wallet balance)
4. Set optional daily/weekly spending limits
5. Click **Generate Token** — copy it immediately (shown only once)
6. Pass as `X-PA-Token` header or set as `PA_TOKEN` environment variable
