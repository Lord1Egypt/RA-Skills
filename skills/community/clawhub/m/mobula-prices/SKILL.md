---
name: mobula-prices
displayName: Mobula - Crypto Prices & Market Data
description: Real-time token prices, market caps, volume, and analytics across 88+ blockchains. Free tier, no credit card required.
version: 1.0.0
author: Mobula
category: crypto
tags:
  - crypto
  - prices
  - market-data
  - defi
  - real-time
requiredEnvVars:
  - MOBULA_API_KEY
homepage: https://mobula.io
docs: https://docs.mobula.io
repository: https://github.com/Flotapponnier/Crypto-date-openclaw
---

# Mobula - Crypto Prices & Market Data

Get real-time crypto prices, market data, and analytics across **88+ blockchains**. Oracle-grade pricing trusted by Chainlink, Supra, and API3.

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
- "What's the price of Bitcoin?"
- "Show me ETH market cap and volume"
- "Is PEPE pumping or dumping right now?"
- "Compare BTC, ETH, and SOL performance today"
- "What was the price of this token on January 1st?"

---

## Security

✅ **Read-only access** - No trading, no transactions
✅ **No private keys** - Only public blockchain data
✅ **Open source** - [View code on GitHub](https://github.com/Flotapponnier/Crypto-date-openclaw)
✅ **VirusTotal verified** - Benign scan results

---

## What This Skill Does

### Get Token Prices (`mobula_market_data`)

**Endpoint:** `GET https://api.mobula.io/api/1/market/data`

Get current price, volume, market cap, and liquidity for any token.

**Parameters:**
- `asset` (required): Token name, symbol, or contract address
  - Examples: "Bitcoin", "ETH", "0x532f27101965dd16442e59d40670faf5ebb142e4"
- `blockchain` (optional): Specific chain ("base", "ethereum", "solana", etc.)

**Returns:**
- Current price (USD)
- Price changes: 1h, 24h, 7d, 30d
- Volume (24h)
- Market cap & fully diluted valuation
- Liquidity
- ATH/ATL with dates
- Supply metrics

**Example prompts:**
- "What's the price of Bitcoin?"
- "Show me BRETT's market data on Base"
- "Is ETH pumping or dumping?"
- "What's the market cap of PEPE?"

---

### Compare Multiple Tokens (`mobula_market_multi`)

**Endpoint:** `GET https://api.mobula.io/api/1/market/multi-data`

Get market data for up to 500 tokens in one request.

**Parameters:**
- `assets` (required): Comma-separated list of tokens
  - Example: "Bitcoin,Ethereum,Solana"

**Returns:** Same data as `mobula_market_data` but for multiple tokens

**Example prompts:**
- "Compare BTC, ETH, and SOL performance today"
- "Show me the top movers from my watchlist"
- "Get prices for these 10 tokens: [list]"

---

### Historical Price Data (`mobula_market_history`)

**Endpoint:** `GET https://api.mobula.io/api/1/market/history`

Get historical price data for charts and trend analysis.

**Parameters:**
- `asset` (required): Token name, symbol, or address
- `from` (optional): Start timestamp (Unix seconds)
- `to` (optional): End timestamp (Unix seconds)
- `period` (optional): "1h", "1d", or "1w"

**Returns:** Array of price points with timestamps, volume, and market cap

**Example prompts:**
- "Show me ETH price for the last 30 days"
- "What was this token's price on January 1st?"
- "Has this token been pumping this week?"
- "Chart BTC price movement for the last 7 days"

---

### Recent Trades (`mobula_market_trades`)

**Endpoint:** `GET https://api.mobula.io/api/1/market/trades/pair`

Live trade feed for a specific liquidity pool.

**Parameters:**
- `address` (required): Liquidity pool address (not token address)
- `limit` (optional): Number of trades (default: 50, max: 300)

**Returns:**
- Recent trades with timestamps
- Buy/sell type
- Amounts (tokens and USD)
- Wallet addresses
- DEX and chain info
- Transaction hashes

**Note:** This endpoint requires the **pool/pair address**, not the token address. Pool addresses are not easily accessible via Mobula API. Consider using wallet transactions endpoint instead for trade history.

**Example prompts:**
- "Show recent trades for this pool: [pool_address]"

---

### Token Metadata (`mobula_metadata`)

**Endpoint:** `GET https://api.mobula.io/api/1/metadata`

Get detailed token information.

**Parameters:**
- `asset` (required): Token name, symbol, or address

**Returns:**
- Name, symbol, logo
- Description
- Official links (website, Twitter, Telegram, Discord)
- Contract addresses across all chains
- Launch date
- Categories/tags

**Example prompts:**
- "Tell me about this token"
- "What's the website for this project?"
- "Where can I find their community?"

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

### Prices
✅ "Price $0.042 (up 12% 24h, down 8% from ATH)"
❌ "Price is $0.003"

### Large Numbers
✅ "$1.23M", "$456K", "$45.6B"
❌ "$1234567"

### Context
Always show direction and timeframe:
- "up 12.4% (24h)"
- "down from ATH of $0.089 on Dec 1st"

---

## Error Handling

**API Key Issues:**
- "I need a Mobula API key. Get one free at https://mobula.io then set it: `export MOBULA_API_KEY='your_key'`"
- "Invalid API key. Check it at https://mobula.io"
- "Rate limit hit. Upgrade at https://mobula.io or retry in a few minutes"

**Token Not Found:**
- "Couldn't find that token. Try the contract address or check spelling?"
- Suggest similar tokens if possible

---

## Rate Limits

- **Free tier:** 100 requests/minute
- Use `mobula_market_multi` for batch queries (1 request for 500 tokens)
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
- Asks about token prices, volume, market cap, or changes
- Mentions a contract address and wants info
- Wants historical price data
- Needs batch data on multiple tokens
- Asks about liquidity, ATH, ATL, or trading volume
- Wants to compare token performance

**❌ DON'T USE WHEN:**
- User wants to execute trades (use trading skills)
- User wants swap quotes (use DEX skills)
- User asks about wallets or portfolio (use mobula-wallet skill)

---

## Related Skills

- **mobula-wallet** - Portfolio tracking and wallet analytics
- **mobula-alerts** - Smart monitoring and price alerts

---

## Resources

- **Get API Key:** [mobula.io](https://mobula.io)
- **API Docs:** [docs.mobula.io](https://docs.mobula.io)
- **GitHub:** [Mobula OpenClaw Skills](https://github.com/Flotapponnier/Crypto-date-openclaw)
- **Support:** Open issue on GitHub

---

## Version History

**1.0.1** (2026-03-28): Updated documentation
- Fixed trades endpoint: requires pool address (`/api/1/market/trades/pair`)

**1.0.0** (2024-03-25): Initial release
- Market data endpoint
- Multi-token batch queries
- Historical price data
- Token metadata
