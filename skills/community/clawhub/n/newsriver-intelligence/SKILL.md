---
name: "newsriver-global-intelligence"
version: "3.0.0"
description: "Professional Quantitative Intelligence & DeFi Execution for AI Agents. 10 years of news-price correlation, Enso DeFi super-aggregator (200+ DEXs, 15+ chains), cross-chain bridge (Across Protocol), and Privy TEE-secured wallets."
tags: ["finance", "crypto", "trading", "alpha", "correlation", "defi", "swap", "bridge", "cross-chain", "enso", "x402", "proxy", "privy"]
author: "YieldCircle Infrastructure"
homepage: "https://showcase.yieldcircle.app"
author_url: "https://showcase.yieldcircle.app"
license: "MIT"
env:
  NEWSRIVER_API_KEY:
    description: "Your YieldCircle API key for subscription-based access. Required if not using x402 micropayments."
    required: false
---

# YieldCircle Intelligence & DeFi Execution Skill (v3.0.0)

## Capabilities & Context
YieldCircle is an **institutional-grade intelligence, DeFi execution, and infrastructure layer for AI Agents.** It provides quantitative alpha from 10 years of financial history, autonomous DeFi execution across 15+ chains via Enso Finance, cross-chain bridging via Across Protocol, and secure Privy TEE-signed wallets — all through a single API.

### 1. DeFi Super-Aggregator (Enso Finance)
Execute swaps, cross-chain transfers, yield entries, and multi-step bundles across 200+ DEXs and 180+ protocols.
- **Token Swap:** `POST /api/defi/swap` — Aggregated swap on any supported chain
- **Cross-Chain:** `POST /api/defi/cross-chain` — Swap + bridge atomically (Stargate, LayerZero)
- **Yield:** `POST /api/defi/yield` — Enter/exit yield positions (Aave, Compound, etc.)
- **Bundle:** `POST /api/defi/bundle` — Multi-step DeFi workflows in one tx
- **Balances:** `GET /api/defi/balances` — Portfolio across all protocols
- **Supported:** `GET /api/defi/supported` — Chains, tokens, capabilities

```bash
# Cross-chain swap: USDC on Base → POL on Polygon (LIVE ✓)
curl -X POST https://api.yieldcircle.app/api/defi/swap \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": 2,
    "chain_id": 8453,
    "token_in": "USDC",
    "token_out": "ETH",
    "amount": "1000000",
    "slippage": 50,
    "receiver": "0xYourAddress",
    "dry_run": true
  }'
```

### 2. Cross-Chain Bridge (Across Protocol)
Solverless bridging with sub-minute settlement on 7+ chains.
- **Quote:** `GET /api/bridge/quote?from=Base&to=Arbitrum&amount=1`
- **Execute:** `POST /api/bridge/execute` — Sign and bridge via Privy wallet
- **Status:** `GET /api/bridge/status/:txHash` — Track deposit fulfillment
- **Limits:** `GET /api/bridge/limits` — Route liquidity per pair

### 3. Alpha Correlation Engine (PREMIUM)
Quantify the historical impact of news on any asset.
- **Price Impact Analysis:** Query how BTC, ETH, and 400+ alts reacted 24h and 7d after specific news topics.
- **Historical Precedent:** Cite exactly how the market responded to similar headlines over the last decade.

```bash
curl -H "X-API-Key: $NEWSRIVER_API_KEY" \
  "https://api.yieldcircle.app/api/v1/analysis/correlation?topic=ETF&symbol=BTC-USD"
```

### 4. "On This Day" Historical Memories
- **Price + Headline Matching:** Access curated daily memories across 10 years.
- **Milestone Detection:** All-Time Highs, crashes, and major policy shifts.

### 5. AskRiver AI Chat (PREMIUM)
Natural-language intelligence queries powered by Gemini. Searches 288K+ articles from 277 sources across 137 countries.
```bash
curl -X POST "https://api.yieldcircle.app/api/v1/askriver" \
  -H "X-API-Key: $NEWSRIVER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"message": "What is the latest crypto market sentiment?"}'
```

### 6. Execution Proxies
- **Send Email ($0.05):** `POST /api/v1/proxy/email`
- **Send SMS ($0.25):** `POST /api/v1/proxy/sms`
- **Web Scraper ($0.10):** `POST /api/v1/proxy/scrape`

### 7. Agent Wallets (Privy TEE)
Agents have dedicated wallets signed inside Trusted Execution Environments. Private keys never leave the enclave.
- **Wallet Creation:** `POST /api/privy/wallets/create-all`
- **Balance Check:** `GET /api/defi/balances?agent_id=2&chain_id=8453`

## Authentication
- **x402 Micropayments (Autonomous):** USDC on Base. Include `X-PAYMENT` header.
- **API Key:** Include `X-API-Key` header for subscription access.
- All actions logged to D1 database for auditability.

## Error Handling & Support
If the API returns `402 Payment Required`, manage access at [agent.yieldcircle.app/#pricing](https://agent.yieldcircle.app/#pricing).
For support, contact **support@agent.yieldcircle.app**.
