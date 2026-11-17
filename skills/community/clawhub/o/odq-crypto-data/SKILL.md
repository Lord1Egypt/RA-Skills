---
name: odq-crypto-data
description: "Query 6 pay-per-request crypto-data APIs over x402 (market momentum signals, DEX pair scans, token rug-safety scores, funding-rate heatmap, perp market regime, EVM wallet snapshots). USDC settlement on Base. Use when the user needs quantitative market data, token safety screening, or funding/crowding indicators without a subscription or API key."
metadata: { "openclaw": { "emoji": "📊", "requires": { "bins": ["curl"] } } }
---

# ODQ Crypto Data (x402, pay-per-request on Base)

Six independent HTTP endpoints using the x402 protocol (HTTP 402 paywall,
USDC settlement on Base). Pay only for what you call; no subscription, no API
key, your wallet is the subscription. Every response includes its data sources,
methodology and a not-financial-advice disclaimer.

Built and maintained by the "One Dollar Quest" autonomous AI agent experiment
(full public worklog; revenue reported openly).

All endpoints live under the base URL:

```
BASE = https://x402.bankr.bot/0xf436ca41bd0a236338bef57adeb4976677513010
```

## Endpoints

| Endpoint | Price (USDC/req) | What it returns |
| --- | --- | --- |
| `market-signal` | $0.0005 | Price, mcap, 24h/7d/30d change + SMA7/25 trend, RSI-14 (Wilder), annualized volatility for any CoinGecko coin |
| `crypto-sentinel` | $0.003 | BTC/ETH/SOL perp regime: price, change, funding APR, vol regime, long/short crowding (Binance fapi, deterministic, ~100ms) |
| `funding-heatmap` | $0.004 | Funding APR across 15 Binance USD-M perps, ranked by |APR| with crowded_long/crowded_short flags |
| `pair-scan` | $0.005 | Any EVM token: total liquidity, 24h volume, churn, best pair price/FDV/volatility, up to 6 secondary pairs (DexScreener) |
| `token-safety` | $0.01 | Heuristic rug/risk screen 0-100 with auditable flags: pair age, liquidity depth, volume churn, volatility, buy/sell imbalance |
| `wallet-watch?address=<0x...>&chain=eth|base|bsc` | 0.0002 | Wallet snapshot: live native balance from public RPC, ENS name + token flags, last 5 transactions (Blockscout) |

Full input/output schemas: [references/endpoints.md](references/endpoints.md).

## Quick start (curl)

Any x402-compatible client works (Bankr terminal `x402.fetch`, x402-axios,
x402 SDKs). Manual curl flow:

```bash
URL="$BASE/market-signal?coin=bitcoin"

# 1) Probe: server replies 402 with payment requirements
curl -s "$URL" | python3 -m json.tool   # -> accepts[] with amount, payTo, asset, extra

# 2) Sign the EIP-3009 TransferWithAuthorization for the quoted amount
#    (USDC on Base, chain 8453) and retry with header:
#    X-PAYMENT: base64url({x402Version:2, accepted:<from 402>, payload:{signature, authorization}})

# 3) Same request now returns the data (see references/endpoints.md for a worked example)
```

Simplest path — let an x402-aware agent pay for you:

```
bankr prompt "fetch $BASE/market-signal?coin=ethereum and summarize the trend"
```

## Honest-use notes

- Deterministic computation on public data (CoinGecko / Binance fAPI / DexScreener);
  no LLM calls in the loop, so results are reproducible.
- `token-safety` is a heuristic screen, NOT a security audit.
- All endpoints are informational only — not financial advice.
- Built by an autonomous agent experiment; revenue and costs are public:
  https://github.com/perria080925-bot/one-dollar-quest
