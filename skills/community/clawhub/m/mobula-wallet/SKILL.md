---
name: mobula-wallet
displayName: Mobula - Wallet Portfolio & Transactions
description: Track wallet portfolios and transaction history across 88+ blockchains. Monitor holdings, analyze trades, and follow whale wallets.
version: 1.0.0
author: Mobula
category: crypto
tags:
  - crypto
  - wallet
  - portfolio
  - blockchain
  - multi-chain
requiredEnvVars:
  - MOBULA_API_KEY
homepage: https://mobula.io
docs: https://docs.mobula.io
repository: https://github.com/Flotapponnier/Crypto-date-openclaw
---

# Mobula - Wallet Portfolio & Transactions

Track wallet portfolios and analyze transaction history across **88+ blockchains** in real-time. Perfect for portfolio tracking, whale watching, and wallet analytics.

## Quick Start

**1. Get your free API key** (no credit card required)
- Go to [mobula.io](https://mobula.io) and sign up
- Free tier: 100 requests/minute
- Copy your API key from the dashboard

**2. Set your API key**
```bash
export MOBULA_API_KEY="your_api_key_here"
```

**3. Try it**
Ask your agent:
- "Show portfolio for wallet 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"
- "What tokens does vitalik.eth hold?"
- "Check my wallet balance"
- "What did this wallet buy recently?"
- "Track this whale's activity"

---

## Security

✅ **Read-only access** - No trading, no transactions
✅ **No private keys** - Only public blockchain data
✅ **Open source** - [View code on GitHub](https://github.com/Flotapponnier/Crypto-date-openclaw)
✅ **VirusTotal verified** - Benign scan results

⚠️ **Privacy Note:**
- Only query public wallet addresses (e.g., vitalik.eth, well-known addresses)
- Wallet addresses are sent to Mobula's API for analysis
- On-chain data is already public, but querying it reveals your interest
- Don't query wallets you want to keep private

---

## What This Skill Does

### Wallet Portfolio (`mobula_wallet_portfolio`)

**Endpoint:** `GET https://api.mobula.io/api/1/wallet/portfolio`

Get complete portfolio for any wallet across all 88 chains in one call.

**Parameters:**
- `wallet` (required): Wallet address or ENS name
  - Format: "0x..." or "vitalik.eth"
- `blockchains` (optional): Filter specific chains (comma-separated)
- `cache` (optional): Use cached data (faster, slightly less fresh)

**Returns:**
- All tokens held with:
  - Token name, symbol, address
  - Balance (amount and USD value)
  - Current price
  - Price change 24h
  - Estimated profit/loss
  - Chain
- Total portfolio value (USD)
- Portfolio allocation by token (percentages)
- NFTs (if present)

**Example prompts:**
- "Show the portfolio for wallet 0x123..."
- "What tokens does vitalik.eth hold?"
- "Check my wallet balance"
- "What's the total value of this wallet?"
- "Show me the top 5 holdings in this wallet"

**Use cases:**
- Portfolio tracking
- Wallet analysis
- Checking holdings before/after trades
- Monitoring allocation
- Setting up portfolio alerts

---

### Wallet Transactions (`mobula_wallet_transactions`)

**Endpoint:** `GET https://api.mobula.io/api/1/wallet/transactions`

Full transaction history for any wallet across all chains.

**Parameters:**
- `wallet` (required): Wallet address
- `from` (optional): Start timestamp (Unix seconds)
- `to` (optional): End timestamp (Unix seconds)
- `asset` (optional): Filter by specific token
- `limit` (optional): Number of transactions (default: 100)

**Returns:**
- Array of transactions:
  - Type (swap, transfer, mint, burn)
  - Tokens involved (from/to)
  - Amounts
  - USD values at time of transaction
  - Timestamp
  - Chain
  - Transaction hash

**Example prompts:**
- "What did this wallet buy recently?"
- "Show me the last 10 transactions for 0x123..."
- "When did this wallet last sell ETH?"
- "Track this whale's activity"

**Use cases:**
- Wallet monitoring
- Whale tracking
- Pattern detection (what they buy/sell)
- Transaction verification
- Analyzing trading strategies

---

## Authentication

All requests require your API key in the `Authorization` header:
```
Authorization: ${MOBULA_API_KEY}
```

**If authentication fails (401/403):**
- Verify: `echo $MOBULA_API_KEY`
- Regenerate at [mobula.io](https://mobula.io) if expired
- Check rate limits (100 req/min free tier)

---

## Response Formatting Tips

### Portfolio Overview
```
Total Portfolio: $24,430

Holdings:
1. ETH: $12,340 (47%) — up 4% 24h
2. BRETT: $8,200 (31%) — up 12% 24h
3. DEGEN: $5,890 (22%) — down 3% 24h

⚠️ ETH allocation is high (47%). Consider rebalancing.
```

### Transaction History
```
Recent Activity:

2h ago: Bought $150K BRETT on Base
- Price: $0.089 (now up 23%)
- Size: Large buy (whale signal)

4h ago: Sold $80K ETH on Ethereum
- Price: $3,456

Note: Wallet has rotated from ETH to BRETT.
```

---

## Error Handling

**API Key Issues:**
- "I need a Mobula API key. Get one free at https://mobula.io then set it: `export MOBULA_API_KEY='your_key'`"
- "Invalid API key. Check it at https://mobula.io"
- "Rate limit hit. Upgrade at https://mobula.io or retry in a few minutes"

**Wallet Issues:**
- "Invalid wallet address. Should be 0x... (42 characters) or ENS name like vitalik.eth"
- "This wallet has no activity or balance. Is this the correct address and chain?"

---

## Common Use Cases

### Portfolio Guardian Pattern

Monitor your wallet 24/7 and get alerts on concentration risks:

1. Fetch portfolio via `mobula_wallet_portfolio`
2. Calculate allocation percentages
3. Check conditions:
   - Any token >40% of portfolio → suggest rebalancing
   - Any token down >15% in 24h → alert
   - Total portfolio changed >10% → notify
4. Store previous values to detect changes
5. Send daily summary

**Example prompt:**
> "Monitor my wallet 0x... and alert me on Telegram if any token drops more than 15% or my allocation exceeds 40% on one asset. Daily summary at 9am."

---

### Whale Watching Pattern

Track smart money movements:

1. Check transactions via `mobula_wallet_transactions`
2. If new significant transaction (>$50K):
   - Get token details
   - Check if other tracked whales bought same token
3. If multiple whales buying → priority alert

**Example prompt:**
> "Watch wallets 0xabc, 0xdef, 0x123. Alert if any buy/sell more than $50K. If multiple whales buy the same token within 6h, priority alert with full analysis."

---

## Rate Limits

- **Free tier:** 100 requests/minute
- Cache portfolio data when possible (doesn't change every second)
- Upgrade at [mobula.io](https://mobula.io) for higher limits

---

## Supported Blockchains

**88+ chains including:**
- Ethereum, Base, Arbitrum, Optimism, Polygon
- BNB Chain, Avalanche, Solana, Fantom, Cronos
- And many more...

Full list: [docs.mobula.io/blockchains](https://docs.mobula.io/blockchains)

---

## When to Use This Skill

**✅ USE WHEN the user:**
- Asks to check a wallet's holdings or portfolio value
- Wants cross-chain portfolio overview
- Wants to track whale wallets or monitor transactions
- Needs transaction history for analysis
- Asks about wallet activity or trading patterns

**❌ DON'T USE WHEN:**
- User wants token prices only (use mobula-prices skill)
- User wants to execute trades (use trading skills)
- User wants swap quotes (use DEX skills)

---

## Related Skills

- **mobula-prices** - Token prices and market data
- **mobula-alerts** - Smart monitoring and price alerts

---

## Resources

- **Get API Key:** [mobula.io](https://mobula.io)
- **API Docs:** [docs.mobula.io](https://docs.mobula.io)
- **GitHub:** [Mobula OpenClaw Skills](https://github.com/Flotapponnier/Crypto-date-openclaw)
- **Support:** Open issue on GitHub
- **Privacy Policy:** [mobula.io/privacy](https://mobula.io/privacy)

---

## Version History

**1.0.0** (2024-03-25): Initial release
- Wallet portfolio tracking across all chains
- Transaction history analysis
- Whale watching support
- Privacy guidelines
