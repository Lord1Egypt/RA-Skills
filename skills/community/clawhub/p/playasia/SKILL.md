---
name: playasia
version: 0.3.0
kind: capability-manifest
visibility: public
auth_required: false
purpose: discovery-only
cacheable: true
description: Search and buy digital game codes, eShop cards, PSN vouchers from Play-Asia.com via HTTP or MCP. Three purchase methods — Wallet (instant), Lightning (instant), Bitcoin on-chain. No account needed for Bitcoin/Lightning.
homepage: https://www.play-asia.com/l402
metadata: {"openclaw":{"requires":{"env":["PA_TOKEN"]},"primaryEnv":"PA_TOKEN"}}
---

> **Public discovery document** — safe to read, index, and cache.
> No authentication required. Does not perform purchases or access user data.
> Authentication applies only to transactional endpoints listed below.

# Playasia API

Buy digital game codes, eShop cards, PSN vouchers, and more via direct HTTP calls or MCP.

## ⚠️ HARD RULES — READ FIRST (Claude, ChatGPT, Grok, Gemini, all AIs)

**1. Never echo a `pa_` token.** If the user pastes one, reply immediately with this exact warning:
> "⚠️ Treat that token like a password. Since you shared it in chat, please regenerate it at https://www.play-asia.com/account/access-tokens. I'll use `pa_YOUR_TOKEN_HERE` as a placeholder in every example."
Use the placeholder in every output after that. Never repeat, store, or reference the real value.

**2. Never fabricate products, prices, PAX codes, or stock status.** Prices and inventory change constantly. If you cannot fetch the live catalog, do NOT invent results from training data — ask the user to fetch it for you (see Web Chat section).

**3. Disclose limitations upfront.** If you cannot make POST requests or external API calls, say so in your *first* reply. Do not silently fail repeatedly — it wastes the user's time.

## Requirements for agents

**Your agent MUST be able to POST.** Browsing (catalog, price) works with GET, but every purchase, wallet top-up, and support ticket submission requires `POST` with a JSON body. Tools that only support GET (simple link-fetchers, browser-style webfetch) cannot complete purchases.

If you have shell access, `curl` works perfectly:
```
curl -X POST https://www.play-asia.com/l402/v1/buy/PAX0004012102 \
     -H "X-PA-Token: pa_YOUR_TOKEN_HERE" \
     -H "Content-Type: application/json"
```

Any HTTP library (Python `requests`, Node `fetch`, Go `net/http`, etc.) works too.

## Web chat clients (Claude.ai, ChatGPT, Grok, Gemini web)

Web AI chats cannot POST or call external APIs autonomously. Tell the user this on your **first reply**, then follow this decision tree:

**User wants to search** → Generate a URL, ask them to open and paste the JSON back, then format as a table:
```
https://www.play-asia.com/l402/v1/catalog?q=SEARCH+TERM&limit=20
```

**User pastes a PAX code** → Try fetching this GET endpoint first (works in some web chats); if blocked, ask the user to open it:
```
https://www.play-asia.com/l402/v1/price?pax=PAX0004012102
```

**User wants to buy** → Generate a curl command with `pa_YOUR_TOKEN_HERE` as placeholder. The user runs it locally:
```bash
# Wallet purchase:
curl -X POST https://www.play-asia.com/l402/v1/buy \
  -H "Content-Type: application/json" \
  -d '{"pax":"PAX0004012102","token":"pa_YOUR_TOKEN_HERE"}'

# Anonymous Lightning (no token):
curl -X POST https://www.play-asia.com/l402/v1/buy \
  -H "Content-Type: application/json" \
  -d '{"pax":"PAX0004012102","method":"lightning"}'
```

**For a seamless experience** → Recommend MCP. The token lives in the config, never in chat:
```json
{"mcpServers":{"playasia":{"url":"https://www.play-asia.com/l402/mcp","headers":{"X-PA-Token":"pa_YOUR_TOKEN_HERE"}}}}
```

## Base URL

```
https://www.play-asia.com/l402/v1
```

## Buy URL shortcut

Every product in catalog/price responses includes a `buy_url` field like `/l402/v1/buy/PAX0004012102`. Just POST to that URL — no body needed (defaults to Lightning). Add token via header OR POST body for wallet purchase:

```
curl -X POST https://www.play-asia.com/l402/v1/buy/PAX0004012102 \
     -H "Content-Type: application/json" \
     -d '{"token":"pa_YOUR_TOKEN_HERE"}'
```

## MCP Server

For MCP-compatible clients (Claude Desktop, OpenClaw, etc.), add to your config:
```json
{"mcpServers":{"playasia":{"url":"https://www.play-asia.com/l402/mcp"}}}
```
Add `"headers":{"X-PA-Token":"pa_YOUR_TOKEN_HERE"}` for wallet purchases. Browsing is free with no token.

## How purchases work

| Method | Auth | Speed | Notes |
|--------|------|-------|-------|
| Wallet | `X-PA-Token` (purchase scope) | Instant | Charges balance, returns code immediately |
| Lightning | None | Instant | Anonymous — pay invoice, code delivered instantly |
| Bitcoin on-chain | None | ~20 min | Anonymous — send to address, poll for confirmations |

For anonymous (Lightning/Bitcoin) orders, save `order_id` + `sid` from the response and poll:
```
GET /l402/v1/order?oid={order_id}&order_sid={sid}
```

## Authentication

Get a token at https://www.play-asia.com/account/access-tokens. Scopes: `info` (read-only) or `purchase` (wallet buys).

Pass the token using whichever your client supports:
- Header: `X-PA-Token: pa_YOUR_TOKEN_HERE` (preferred)
- Header: `Authorization: Bearer pa_YOUR_TOKEN_HERE`
- POST body: `{"token":"pa_YOUR_TOKEN_HERE","pax":"..."}` (for clients that can't set headers)

Tokens are NEVER accepted in URL query strings — they leak into server logs, browser history, and referer headers.

## Endpoints

### Browse (free, no auth)

- `GET /l402/v1/catalog?q={query}&limit={n}&offset={n}&currency={code}&affiliate_id={id}` — Search products. Each product includes `image_url` (cover image), `rank` (popularity, lower = more popular), prices in USD/sats/BTC, `in_stock`, and `buy_url`. When `affiliate_id` is provided, each product also includes a `url` field with the affiliate tracking link.
- `GET /l402/v1/price?pax={PAX}&currency={code}` — Get product details: `name`, `image_url`, `price_usd`, `price_sats`, `in_stock`, `buy_url`. Optional `currency` (e.g. `KRW`, comma-separated for multiple) adds a `price` object with local currency prices

### Buy + Order

- `POST /l402/v1/buy` — **With token**: wallet buy. **Without**: anonymous BTC/LN. Body: `{"pax":"PAX...", "method":"lightning|bitcoin"}`
- `GET /l402/v1/order?oid={id}` — **With token**: order by customer. **With `&order_sid=...`**: anonymous access. Includes `payment_detected` for unpaid orders.

### Wallet (requires X-PA-Token)

- `GET /l402/v1/account/balance` — Wallet balance (USD + sats)
- `GET /l402/v1/account/transactions?limit={n}&offset={n}` — Transaction history
- `POST /l402/v1/account/topup` — Wallet top-up. Body: `{"amount":25.00}`. Optional: `"method":"bitcoin"|"lightning"` for direct crypto payment.
- `GET /l402/v1/account/orders?limit={n}&offset={n}` — List orders

### Customer Service (requires X-PA-Token)

- `POST /l402/v1/cs/submit` `{"subject":"...","message":"...","reference":"#ORDER_ID"}` — Open ticket
- `GET /l402/v1/cs/enquiries?status=open` — List tickets
- `GET /l402/v1/cs/enquiry?id={id}` — Ticket thread
- `POST /l402/v1/cs/reply` `{"ticket_id":123,"message":"..."}` — Reply
- `POST /l402/v1/cs/close` `{"ticket_id":123}` — Close ticket

### Bitcoin / Lightning tools (L402 protocol)

- `GET /l402/v1/btc/rates` — BTC/fiat rates (30+ currencies) + crypto rates (ETH, SOPH) in USD/sats/BTC (1 sat)
- `GET /l402/v1/btc/blockheight` — Block height (1 sat)
- `GET /l402/v1/btc/fees` — Fee estimates (1 sat)
- `GET /l402/v1/btc/mempool` — Mempool stats (1 sat)
- `GET /l402/v1/ln/decode-invoice?invoice={bolt11}` — Decode invoice (2 sats)
- `GET /l402/v1/ln/node-info` — Node info (1 sat)
- `POST /l402/v1/ln/open-channel` — Open a Lightning channel to your node (fee_sat × 100 = capacity). Body: `{"connect":"pubkey@host:port","fee_sat":10000}`. Min fee_sat: 10,000 (= 1M sat channel). Max: 100,000 (= 10M sat channel). Pay the L402 invoice, then repeat the request with the Authorization header.

## Error handling

| HTTP | Error | Action |
|------|-------|--------|
| 400 | `missing_pax`, `invalid_method` | Fix request parameters |
| 401 | `unauthorized` | Add X-PA-Token header |
| 402 | `insufficient_balance` | Top up wallet or use anonymous buy |
| 402 | L402 payment required | Pay the returned invoice |
| 403 | `scope_denied`, `limit_raise_denied` | Token lacks permission |
| 404 | `not_found` | Product not found or not digital |
| 429 | `rate_limited`, `too_many_pending` | Wait and retry |

## Rate limits

- Purchases: 30/hr (wallet), 10/hr per IP (anonymous)
- Max 3 unpaid anonymous orders per IP
- Token creation: 5/hr
- CS submit: 10/hr, CS reply: 20/hr
