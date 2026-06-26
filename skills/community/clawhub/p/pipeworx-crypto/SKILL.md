---
name: pipeworx-crypto
description: Cryptocurrency prices, market cap rankings, and fiat currency conversion via CoinGecko
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
    emoji: "₿"
    homepage: https://pipeworx.io/packs/crypto
---

# Crypto & Currency

Real-time cryptocurrency prices from CoinGecko plus fiat currency conversion. Check the price of Bitcoin, get the top 100 coins by market cap, or convert between currencies like USD, EUR, and GBP.

## Tools

| Tool | Description |
|------|-------------|
| `get_crypto_price` | Current price for a specific cryptocurrency by CoinGecko ID (e.g., "bitcoin", "ethereum", "solana") |
| `get_crypto_market` | Top cryptocurrencies ranked by market cap with prices and 24h changes |
| `get_exchange_rate` | Fiat-to-fiat exchange rate conversion (e.g., USD to EUR) |

## Scenarios

- "What's the current price of Ethereum?" — use `get_crypto_price` with id `"ethereum"`
- Building a portfolio tracker that needs live prices
- Converting currencies for international pricing calculations
- Displaying a market overview with top gainers and losers

## Example: Bitcoin price

```bash
curl -s -X POST https://gateway.pipeworx.io/crypto/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"get_crypto_price","arguments":{"id":"bitcoin"}}}'
```

```json
{
  "name": "Bitcoin",
  "symbol": "btc",
  "price_usd": 67234.12,
  "market_cap": 1320000000000,
  "volume_24h": 28500000000,
  "change_24h": 2.34
}
```

## MCP config

```json
{
  "mcpServers": {
    "pipeworx-crypto": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "https://gateway.pipeworx.io/crypto/mcp"]
    }
  }
}
```
