---
name: kr-crypto-intelligence
description: Korean crypto + news data + AI analysis for trading agents. 15 tools — dual-basis Kimchi Premium (official USD/KRW + USDT live rate) across 180+ tokens, exchange intelligence, AI sentiment analysis (world's first Korean-to-English), Global vs Korea divergence with structured AI breakdown, market alerts, plus Korean news (K-pop artists, semiconductor industry: Samsung/SK Hynix/HBM) translated to English with AI synthesis. x402 on Base, Polygon, and Solana. Every paid response includes a cryptographic receipt (ECDSA secp256k1) for agent accountability.
version: 1.5.0
homepage: https://github.com/bakyang2/kr-crypto-intelligence
repository: https://github.com/bakyang2/kr-crypto-intelligence
metadata:
  clawdbot:
    emoji: "🇰🇷"
    requires:
      env: []
---

# KR Crypto Intelligence

Korean data API for trading and content agents. South Korea ranks top 3 globally in crypto trading volume. 15 paid endpoints covering 180+ tokens, plus Korean news (K-pop, semiconductor industry) translated to English with AI synthesis.

## How to Use

MCP server — no local code, no API keys, no credentials needed.

### MCP Connection

```json
{
  "mcpServers": {
    "kr-crypto-intelligence": {
      "url": "https://mcp.printmoneylab.com/mcp"
    }
  }
}
```

### Available Tools (15 paid + 2 free)

| Tool | Price | Description |
|------|-------|-------------|
| `get_market_read` | **$0.10** | AI market analysis — 12+ sources + exchange intelligence + Claude AI token-level signals |
| `get_global_vs_korea_divergence_deep` | **$0.10** | Deep tier — light data + Korean news signals (Coinness Telegram) + structured AI breakdown |
| `get_kr_news_semiconductor_summary` | **$0.10** | Korean semiconductor news (Samsung, SK Hynix, HBM) + AI market signal (bullish/bearish), trending companies |
| `get_global_vs_korea_divergence` | $0.05 | Light tier — global vs Korean price premium + AI interpretation |
| `get_kr_sentiment` | $0.05 | Korean market sentiment in English — exchange intelligence + Korean news context |
| `get_kr_news_kpop_summary` | $0.05 | K-pop news (artists/groups/solo) + AI sentiment, key themes, trending artists |
| `get_kr_news_semiconductor` | $0.02 | Korean semiconductor industry news in English (headlines + translation) |
| `get_arbitrage_scanner` | $0.01 | Token-by-token Kimchi Premium for 180+ tokens, reverse premium, Upbit-Bithumb gaps |
| `get_exchange_alerts` | $0.01 | New listings/delistings, investment warnings, caution flags |
| `get_market_movers` | $0.01 | 1-min price surges/crashes, volume spikes, top 20 by volume |
| `get_kr_news_kpop` | $0.01 | K-pop news (artists/groups/solo) translated to English |
| `get_kimchi_premium` | $0.001 | **Dual-basis** Kimchi Premium — `premium_percent` (official USD/KRW) + `premium_pct_usdt` (Upbit USDT live rate). Gap = real arbitrage margin |
| `get_stablecoin_premium` | $0.001 | USDT/USDC premium (fund flow indicator) |
| `get_kr_prices` | $0.001 | KRW prices from Upbit/Bithumb |
| `get_fx_rate` | $0.001 | USD/KRW exchange rate |
| `get_available_symbols` | (free) | Tradeable symbols list |
| `check_health` | (free) | Service status |

### REST API (Alternative)
GET https://api.printmoneylab.com/api/v1/market-read                     → $0.10
GET https://api.printmoneylab.com/api/v1/global-vs-korea-divergence-deep → $0.10
GET https://api.printmoneylab.com/api/v1/kr-news/semiconductor-summary   → $0.10
GET https://api.printmoneylab.com/api/v1/global-vs-korea-divergence      → $0.05
GET https://api.printmoneylab.com/api/v1/kr-sentiment                    → $0.05
GET https://api.printmoneylab.com/api/v1/kr-news/kpop-summary            → $0.05
GET https://api.printmoneylab.com/api/v1/kr-news/semiconductor           → $0.02
GET https://api.printmoneylab.com/api/v1/arbitrage-scanner               → $0.01
GET https://api.printmoneylab.com/api/v1/exchange-alerts                 → $0.01
GET https://api.printmoneylab.com/api/v1/market-movers                   → $0.01
GET https://api.printmoneylab.com/api/v1/kr-news/kpop                    → $0.01
GET https://api.printmoneylab.com/api/v1/kimchi-premium                  → $0.001
GET https://api.printmoneylab.com/api/v1/stablecoin-premium              → $0.001
GET https://api.printmoneylab.com/api/v1/kr-prices                       → $0.001
GET https://api.printmoneylab.com/api/v1/fx-rate                         → $0.001
GET https://api.printmoneylab.com/api/v1/symbols                         (free)
GET https://api.printmoneylab.com/health                                 (free)

## Data Privacy & What Gets Sent

**The server requires only the tool call parameters listed below. What your MCP client actually transmits depends on the client implementation — please review your MCP client's privacy and transport settings to verify.**

Specifically, each tool requires:
- `get_kimchi_premium`, `get_global_vs_korea_divergence`, `get_global_vs_korea_divergence_deep`: `symbol` parameter only (e.g., "BTC")
- `get_kr_prices`: `symbol` and `exchange` parameters only
- `get_kr_news_kpop`, `get_kr_news_kpop_summary`, `get_kr_news_semiconductor`, `get_kr_news_semiconductor_summary`: optional `limit` parameter only (1-10, default 5)
- `get_arbitrage_scanner`, `get_exchange_alerts`, `get_market_movers`: no parameters — server computes from cached exchange data
- `get_market_read`: no parameters — server fetches all data internally and runs AI analysis server-side
- `get_kr_sentiment`: no parameters — server combines exchange data with Korean news context and runs AI sentiment analysis server-side
- `get_fx_rate`, `get_stablecoin_premium`, `get_available_symbols`, `check_health`: no parameters

Note: Like any HTTP service, the server receives standard HTTP metadata (IP address, user-agent) as part of normal network communication.

**Network calls only to:** `mcp.printmoneylab.com` and `api.printmoneylab.com`

## Payment Authorization (x402 Protocol)

**How x402 payment works — step by step:**

1. Agent calls a paid endpoint (e.g., `get_kimchi_premium`)
2. Server returns HTTP 402 with price in the `payment-required` header
3. **The MCP client or platform decides whether to pay** — this is NOT automatic
4. If the client approves, it signs a USDC transfer for the exact amount on Base, Polygon, or Solana
5. Client retries with payment proof in `X-PAYMENT` header
6. Server verifies payment and returns data

**Key points:**
- **Payment is NOT automatic.** The agent's MCP client (e.g., xpay Smart Proxy, Claude, Cursor) controls whether to authorize payment.
- **No wallet keys or credentials are stored in this skill.** Payment is handled entirely by the MCP client's x402 transport layer.
- **The skill cannot charge without explicit client-side authorization.** The x402 protocol requires a cryptographic signature from the buyer's wallet.
- **Cost per call:** $0.001 (basic data) to $0.10 (AI deep analysis). No subscriptions, no hidden fees.

## Receipt Verification

**Every paid response includes a signed receipt for agent accountability.** Bots can verify receipt authenticity using the merchant's public key.

The server returns a `receipt` field in every paid response:

```json
{
  "receipt": {
    "id": "rcpt_20260513_a3f9c1",
    "issued_at": "2026-05-13T07:30:00.000Z",
    "endpoint": "/api/v1/kimchi-premium",
    "amount": "0.001",
    "currency": "USDC",
    "network": "eip155:8453",
    "tx_hash": "0x...",
    "payer": "0x...",
    "merchant": "0xcF9223eCe895258dEa8D288AEBcf846Ab8E342fB",
    "signature": "0x...",
    "signer": "0x1AdF0f9e576E94a150208F08D2C31F791932E781"
  }
}
```

**Verification (Python):**
```python
from eth_account import Account
from eth_account.messages import encode_defunct

payload = "|".join([
    r["id"], r["endpoint"], r["amount"], r["currency"],
    r["network"], r["tx_hash"], r["payer"], r["merchant"], r["issued_at"]
])
recovered = Account.recover_message(
    encode_defunct(text=payload),
    signature=r["signature"]
)
# recovered.lower() == r["signer"].lower() → authentic
```

**Merchant public key** is published at:
`https://api.printmoneylab.com/.well-known/x402` under `receipt_signer.public_key`

Receipt verification is optional but recommended for agents that need to maintain audit logs or reconcile payments.

## Autonomous Invocation Advisory

This skill is designed to be invoked by the agent when the user asks about Korean crypto markets, Korean financial news, K-pop news, or Korean semiconductor industry news. If your platform supports invocation controls:
- **Recommended:** Set to "user-invoked only" until comfortable with billing behavior
- **Budget:** Configure your MCP client's spending limit
- **Maximum cost per session:** Bounded by your client's spending policy

## Security

- **No local code execution** — instruction-only skill
- **No credentials stored** — no API keys, no wallet keys, no env vars
- **No file system access** — all data from remote API
- **Open source:** https://github.com/bakyang2/kr-crypto-intelligence (MIT license)
- **API docs:** https://api.printmoneylab.com/docs (Swagger/OpenAPI)
- **Registered on:** Official MCP Registry, Glama, Smithery, xpay.tools, awesome-x402, awesome-mcp-servers, coinbase/x402 ecosystem, solana-foundation/awesome-solana-ai
