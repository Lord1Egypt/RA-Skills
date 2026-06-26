---
name: polymarket-bundle-crypto-hourly-trader
description: Trades crypto hourly Up/Down markets when sub-interval consensus disagrees with the hourly price on Polymarket. BTC/ETH/SOL 5-min interval markets within the same hour must be consistent with the hourly Up/Down market -- when majority sub-intervals show Up bias but the hourly is priced low, or vice versa, the hourly is mispriced. Conviction-based sizing scales with disagreement magnitude.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: Bundle Crypto Hourly Consensus Trader
  difficulty: advanced
---

# Bundle -- Crypto Hourly Consensus Trader

> **This is a template.**
> The default signal detects disagreement between 5-min sub-interval consensus and hourly crypto Up/Down markets -- remix it with additional coins, time windows, or volume-weighted consensus.
> The skill handles all the plumbing (market discovery, bundle construction, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

Polymarket lists crypto Up/Down markets at multiple time granularities for the same hour:

- "Bitcoin Up or Down - March 28, 11:00AM-11:05AM ET" = 62%
- "Bitcoin Up or Down - March 28, 11:05AM-11:10AM ET" = 58%
- "Bitcoin Up or Down - March 28, 11:10AM-11:15AM ET" = 60%
- "Bitcoin Up or Down - March 28, 11:15AM-11:20AM ET" = 57%
- "Bitcoin Up or Down - March 28, 11AM ET" = 42%  <-- MISPRICED

The sub-intervals form a **consensus bundle** -- if most 5-min intervals show Up bias, the hourly market should reflect that. When it doesn't, the hourly is mispriced.

## Edge

The hourly market price must be consistent with the aggregate signal from its sub-intervals. If 4 of 6 five-minute intervals show "Up" bias (>55%), the hourly market should also show Up bias. Retail traders price each interval independently without considering the bundle constraint, creating structural mispricings.

## Signal Logic

1. Discover crypto Up/Down markets via keyword search + bulk market fetch fallback
2. Parse each question: extract (coin, date, start_time, end_time) or (coin, date, hour) for hourly
3. Filter non-crypto noise with regex
4. Group into hourly bundles: one hourly market + its sub-interval markets
5. For each bundle with MIN_SUB_INTERVALS+ sub-intervals:
   - Count how many sub-intervals show Up bias (p > 0.55) vs Down bias (p < 0.45)
   - If majority are Up but hourly < 0.45: hourly underpriced for Up -> buy YES
   - If majority are Down but hourly > 0.55: hourly overpriced for Up -> buy NO
6. Size by conviction (CLAUDE.md formula), not flat amount

### Remix Signal Ideas

- **Volume-weighted consensus**: Weight each sub-interval's signal by its trading volume -- higher-volume intervals carry more information
- **Momentum detection**: Track sub-interval price changes over the last 10 minutes -- if the trend is accelerating, increase conviction
- **Cross-coin correlation**: If BTC sub-intervals are all Up and ETH hourly is still low, use BTC signal as additional confirmation for ETH
- **Exchange API spot price**: Compare Polymarket sub-interval prices with actual Binance/Coinbase 1-min candles for real-time validation

## Safety & Execution Mode

**The skill defaults to paper trading (`venue="sim"`). Real trades only with `--live` flag.**

| Scenario | Mode | Financial risk |
|---|---|---|
| `python trader.py` | Paper (sim) | None |
| Cron / automaton | Paper (sim) | None |
| `python trader.py --live` | Live (polymarket) | Real USDC |

`autostart: false` and `cron: null` mean nothing runs automatically until configured in Simmer UI.

## Required Credentials

| Variable | Required | Notes |
|---|---|---|
| `SIMMER_API_KEY` | Yes | Trading authority. Treat as a high-value credential. |

## Tunables (Risk Parameters)

All declared as `tunables` in `clawhub.json` and adjustable from the Simmer UI.

| Variable | Default | Purpose |
|---|---|---|
| `SIMMER_MAX_POSITION` | `40` | Max USDC per trade at full conviction |
| `SIMMER_MIN_TRADE` | `5` | Floor for any trade |
| `SIMMER_MIN_VOLUME` | `5000` | Min market volume filter (USD) |
| `SIMMER_MAX_SPREAD` | `0.08` | Max bid-ask spread |
| `SIMMER_MIN_DAYS` | `0` | Min days until resolution (0 = allow same-day) |
| `SIMMER_MAX_POSITIONS` | `8` | Max concurrent open positions |
| `SIMMER_YES_THRESHOLD` | `0.38` | Buy YES only if market probability <= this |
| `SIMMER_NO_THRESHOLD` | `0.62` | Sell NO only if market probability >= this |
| `SIMMER_MIN_SUB_INTERVALS` | `3` | Min sub-intervals needed to form consensus |

## Edge Thesis

Crypto Up/Down markets on Polymarket are listed at multiple time granularities -- 5-min intervals and hourly. Each market has its own order book and liquidity pool. Retail traders price each interval independently, creating structural inconsistencies between the sub-interval consensus and the hourly market. This skill aggregates the sub-interval signal and trades the hourly market when it diverges from the consensus. The edge exists because:

- Sub-interval markets react faster to real-time price action
- Hourly markets are less liquid and lag behind
- No market maker enforces cross-interval consistency on Polymarket
- Crypto volatility creates frequent consensus shifts within an hour
- The bundle constraint is mathematical -- if most sub-intervals are Up, the hour should be Up

## Dependency

`simmer-sdk` by Simmer Markets (SpartanLabsXyz)
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
