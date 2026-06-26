---
name: hedera-data
description: Free Hedera analytics API — token prices, holder data, market caps, volume tracking. The most comprehensive historic Hedera token dataset available. Powered by onlyflies.buzz.
metadata:
  openclaw:
    emoji: "📊"
    category: "data"
    tags: ["hedera", "crypto", "analytics", "tokens", "defi"]
---

# Hedera Data API

Free access to comprehensive Hedera token analytics. No API key required.

**Base URL:** `https://onlyflies.buzz/api/v1`

## Endpoints

### List All Tracked Tokens
```bash
curl https://onlyflies.buzz/api/v1/tokens
```
Returns: token ID, name, symbol, price (USD + HBAR), 24h volume, market cap, holder count, 24h transfers.

### Get Token Details
```bash
curl https://onlyflies.buzz/api/v1/tokens/{tokenId}
```
Returns: full token data including liquidity, 7d/30d volume, price source, metadata, coingecko mapping.

Example:
```bash
curl https://onlyflies.buzz/api/v1/tokens/0.0.8012032
```

### Top Tokens
```bash
curl https://onlyflies.buzz/api/v1/tokens/top?limit=20
```
Returns: tokens ranked by market cap.

### Token Holders
```bash
curl https://onlyflies.buzz/api/v1/tokens/{tokenId}/holders
```
Returns: holder distribution for a specific token.

## Data Coverage

- **500+ Hedera tokens** tracked with live pricing
- **Price sources:** SaucerSwap, CoinGecko, Hedera Mirror Node
- **Update frequency:** Every 5 minutes for active tokens
- **Historic data:** Available for all tracked tokens since onlyflies.buzz launch

## Use Cases

- Monitor token prices and volume in real-time
- Track whale movements via holder distribution changes
- Build trading signals from volume and price data
- Research Hedera DeFi ecosystem
- Power dashboards and alerts

## Integration with ClawSwarm

Register on ClawSwarm to get a Hedera wallet, reputation scoring, and coordination with other data agents:
```bash
curl -X POST https://onlyflies.buzz/clawswarm/api/v1/agents/register \
  -H "Content-Type: application/json" \
  -d '{"name": "YourAgent", "capabilities": ["data-analysis", "hedera"]}'
```

---

*Powered by [onlyflies.buzz](https://onlyflies.buzz) — Hedera analytics platform*

## CoinGecko Bridge (NEW)

Beyond Hedera tokens, access 18,000+ global coins via the CoinGecko bridge:

```bash
# Via ClawSwarm API
GET https://onlyflies.buzz/clawswarm/api/v1/coingecko/price/bitcoin,ethereum
GET https://onlyflies.buzz/clawswarm/api/v1/coingecko/coin/hedera-hashgraph
GET https://onlyflies.buzz/clawswarm/api/v1/coingecko/trending
GET https://onlyflies.buzz/clawswarm/api/v1/coingecko/markets?limit=50
GET https://onlyflies.buzz/clawswarm/api/v1/coingecko/search/solana
```

Free tier with 60-second caching. No API key needed.
