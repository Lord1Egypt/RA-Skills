---
name: mcp-crypto-data
description: Real-time cryptocurrency prices, network fee estimates, and Lightning Network statistics via L402 API. Use when agents need crypto market data, fee planning, or Lightning network health checks.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - npx
      env:
        - L402_API_BASE_URL
    emoji: ₿
---

# Crypto Data (L402)

Real-time cryptocurrency data — prices, fees, and Lightning Network stats.

## Setup

```json
{
  "mcpServers": {
    "crypto-data": {
      "command": "npx",
      "args": ["-y", "@vbotholemu/mcp-crypto-data"],
      "env": {
        "L402_API_BASE_URL": "https://api.nautdev.com"
      }
    }
  }
}
```

## Tools

### `get_crypto_price`
Real-time price for any supported cryptocurrency.

### `get_network_fees`
Current transaction fee estimates for Bitcoin and other networks.

### `get_lightning_stats`
Lightning Network statistics — node count, channel count, total capacity.

## When to Use

- Portfolio monitoring and price checks
- Transaction fee estimation before sends
- Lightning Network health monitoring
- Market data for trading agents
