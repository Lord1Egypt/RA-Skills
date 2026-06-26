---
name: hyre-defi
description: "AI-powered DeFi intelligence on Solana — 24 endpoints for token launches, wallet analytics, LP yields, and cross-chain data. Pay per request via x402 USDC. Use when user asks about trading signals, new tokens, whale tracking, or DeFi data."
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
    emoji: "🔍"
    homepage: https://hyreagent.fun
---

# HYRE Agent — AI DeFi Intelligence

Use this skill when the user wants:
- New token launch data (sniping, bonding curves)
- Wallet analytics (PnL, positions, whale tracking)
- LP pool recommendations and yield farming
- Cross-chain DeFi data
- AI-powered trading signals

## Payment

- Protocol: x402 (HTTP 402 Payment Required)
- Currency: USDC
- No API keys needed — pay per request

## Chain Routing

| Chain | Prefix | Example |
|-------|--------|---------|
| Solana | `/` (root) | `POST /defi/tvl` |
| Base | `/base/` | `POST /base/defi/tvl` |
| SKALE | `/skale/` | `POST /skale/defi/tvl` |

## Key Endpoints

### Token Launches (Trenches)
- `POST /trenches/new-tokens` ($0.008) — Latest token launches
- `POST /trenches/token-verdict` ($0.015) — Full AI verdict with risk score
- `POST /trenches/graduating` ($0.003) — Tokens near graduation (>70%)
- `POST /trenches/token-snipers` ($0.004) — Detect early buyers

### Wallet Analytics (Traders)
- `POST /traders/wallet-pnl` ($0.005) — Wallet PnL
- `POST /traders/top-wallets` ($0.008) — Top performing wallets
- `POST /traders/wallet-intel` ($0.012) — 30-day wallet intelligence

### LP Data
- `POST /lp/pools` ($0.001) — Meteora DLMM pools with APR/TVL
- `POST /lp/pools-recommend` ($0.008) — AI pool recommendation
- `POST /lp/pools-strategy` ($0.020) — Full LP strategy advisor

### DeFi
- `POST /defi/tvl` ($0.001) — Total Value Locked
- `POST /defi/yields` ($0.002) — Top yield pools

### Cross-Chain
- `POST /debridge/quote` ($0.002) — Cross-chain USDC quote
- `POST /debridge/yield-migrate` ($0.005) — Yield migration advisor

### Natural Language
- `POST /ask` ($0.025) — AI orchestrates data sources

## Example: Snipe New Token

```bash
# Get latest launches
curl -X POST https://hyreagent.fun/trenches/new-tokens \
  -H "Content-Type: application/json" \
  -d '{"limit": 5}'

# Get AI verdict on a token
curl -X POST https://hyreagent.fun/trenches/token-verdict \
  -H "Content-Type: application/json" \
  -d '{"mint": "TOKEN_MINT_ADDRESS"}'
```

## Response Format

Every endpoint returns:
```json
{
  "data": {},
  "insight": "AI-generated analysis",
  "signal": "snipe/watch/avoid",
  "confidence": 0.85,
  "sources": ["jupiter", "defillama"],
  "model_used": "claude-3.5-haiku"
}
```

## Signal Vocabulary
- **Trenches**: snipe / watch / avoid
- **Traders**: follow / ignore
- **LPs**: add_liquidity / rebalance / hold
- **DeFi**: high_yield / low_yield

## Trading Bot Pattern

1. Poll `/trenches/new-tokens` every 30s
2. Run `/trenches/token-verdict` on each (AI risk score)
3. Auto-buy tokens with signal="snipe" and confidence>0.7
4. Track via `/traders/wallet-pnl`
5. Exit on signal="avoid" or stop-loss
