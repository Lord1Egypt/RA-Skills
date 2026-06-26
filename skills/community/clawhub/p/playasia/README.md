# @playasia/mcp

MCP server for [Play-Asia.com](https://www.play-asia.com) — agentic shopping for digital codes, game vouchers, and more.

## Install

### Claude Desktop / Claude Code

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "play-asia": {
      "command": "npx",
      "args": ["-y", "@playasia/mcp"],
      "env": {
        "PA_TOKEN": "pa_your_token_here"
      }
    }
  }
}
```

### OpenClaw

Install via ClawHub or add as an MCP server in your OpenClaw config.

## Authentication

This API uses **two different auth methods** depending on what you're accessing:

### 1. L402 (Lightning HTTP 402)
- For **paid resources** (products, BTC data, Lightning info)
- Flow: request → get 402 with invoice → pay → retry with `macaroon:preimage`
- Header: `Authorization: L402 macaroon:preimage`

### 2. Platform Token (X-PA-Token)
- For **account features** (wallet, orders, support tickets)
- Get your token at: https://www.play-asia.com/account/access-tokens
- Pass via header: `X-PA-Token: pa_xxx` (preferred) or `Authorization: Bearer pa_xxx`
- Or via POST body: `{"token":"pa_xxx", ...}` (for agents that cannot set headers)
- Token scopes:
  - `info` - read-only (balance, orders, tickets)
  - `purchase` - can buy with wallet balance

**Quick reference:**
| Need | Auth Method |
|------|-------------|
| Search catalog | None (free) |
| Buy with Lightning | L402 |
| Buy with Bitcoin | None (anonymous, track via `sid`) |
| Check wallet balance | Platform token (`info` scope) |
| Buy with wallet | Platform token (`purchase` scope) |
| View orders | Platform token |
| Support tickets | Platform token |

## Features

### No account needed (L402 / Lightning)

| Tool | Description |
|------|-------------|
| `search_products` | Search digital catalog — game codes, eShop cards, PSN, Roblox, etc. |
| `get_product_price` | Get price in USD + satoshis for any product |
| `buy_digital_product` | Purchase via Lightning — pay invoice, receive code |
| `get_pricing` | View L402 resource pricing |
| `get_exchange_rates` | BTC/fiat rates for 30+ currencies |

### With PA Platform token

Generate a token at: https://www.play-asia.com/account/access-tokens

| Tool | Description |
|------|-------------|
| `get_wallet_balance` | Check wallet balance |
| `get_transactions` | Wallet transaction history |
| `buy_with_wallet` | Buy using wallet balance (needs `purchase` scope) |
| `get_orders` | List your recent orders |
| `get_order` | Order details + digital codes + tracking |
| `submit_enquiry` | Open a customer service ticket |
| `get_enquiries` | List your tickets |
| `get_enquiry` | View ticket conversation |
| `reply_to_enquiry` | Reply to a ticket |
| `close_enquiry` | Close/resolve a ticket |

## How purchases work

### Option 1: Lightning Network (instant)
```
1. Agent calls: buy_digital_product({ pax: "PAX0004012102" })
   → Returns Lightning invoice (e.g. 58,694 sats)

2. Agent pays the invoice with any Lightning wallet
   → Receives the preimage (64-char hex)

3. Agent calls: buy_digital_product({ pax: "PAX0004012102", l402_token: "MACAROON:PREIMAGE" })
   → Receives the digital code instantly
```

### Option 2: Bitcoin on-chain (no wallet needed)
```
1. Agent calls: buy_digital_product({ pax: "PAX0004012102", method: "bitcoin" })
   → Returns Bitcoin address and amount (in sats)

2. Agent pays the address on-chain
   → Waits for ~20 min (2 confirmations)

3. Agent polls: get_order({ oid: ORDER_ID, sid: SESSION_ID })
   → Once confirmed, receives the digital code
   → Save the `sid` (session ID) from the initial response to track the order!
```

### Option 3: Wallet balance (requires platform token with purchase scope)
```
1. Agent calls: buy_with_wallet({ pax: "PAX0004012102" })
   → Instantly receives the digital code if sufficient balance
```

**Important:** For anonymous Bitcoin orders, always save the `sid` and `order_id` from the initial response to poll for the code later.

No signup. No account. No KYC. Just Bitcoin.

## Error handling

| HTTP Code | Meaning | What to do |
|-----------|---------|------------|
| 402 | Payment Required | Pay the invoice, then retry with `l402_token` |
| 429 | Rate Limited | Wait and retry (check `Retry-After` header) |
| 401 | Unauthorized | Invalid or missing token. Generate at `/account/access-tokens` |
| 403 | Scope Denied | Token lacks required scope (e.g., "purchase" for buying) |
| 404 | Not Found | Product/order/ticket doesn't exist |
| 500 | Server Error | Retry later or contact support |

### Common error responses

```json
// Insufficient wallet balance
{ "error": "insufficient_balance", "balance": 10.00, "price": 25.00, "shortfall": 15.00 }

// Rate limited
{ "error": "rate_limited", "message": "Too many requests. Try again later." }

// Token scope denied
{ "error": "scope_denied", "message": "Token needs purchase scope" }
```

## Environment variables

| Variable | Required | Description |
|----------|----------|-------------|
| `PA_TOKEN` | No | Platform token for account features (orders, CS) |
| `PA_BASE_URL` | No | Override API base URL (default: `https://www.play-asia.com`) |

## Build from source

```bash
npm install
npm run build
```

## License

MIT
