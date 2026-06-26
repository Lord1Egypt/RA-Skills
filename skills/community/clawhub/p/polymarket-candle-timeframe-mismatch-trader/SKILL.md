---
name: polymarket-candle-timeframe-mismatch-trader
description: Multi-timeframe analysis for crypto Up or Down markets on Polymarket. Detects when 5-minute candle consensus diverges from the hourly market and trades convergence. When 4+ of 6 sub-intervals show a clear directional pattern but the hourly market remains neutral, the 5-min intervals are leading indicators and the longer timeframe will converge.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: Candle Timeframe Mismatch Trader
  difficulty: advanced
---

# Candle Timeframe Mismatch Trader

> **This is a template.**
> The default signal detects timeframe mismatches between 5-min candle consensus and hourly markets -- remix it with real-time price feeds, volume data, or multi-coin correlation analysis.
> The skill handles all the plumbing (market discovery, interval parsing, consensus detection, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

Polymarket lists both hourly and 5-minute interval "Up or Down" markets for BTC, ETH, and SOL. An hourly market like "Bitcoin Up or Down - March 29, 11AM ET" covers the same period as twelve 5-minute sub-intervals (11:00AM-11:05AM through 11:55AM-12:00PM).

When 4+ of the 6 sub-intervals within an hour show a clear directional consensus (all biased UP or DOWN), but the hourly market is still priced in the neutral zone (0.45-0.55), there is a timeframe mismatch. The 5-minute markets are reacting faster to real-time price action while the hourly market lags. This skill trades the convergence -- the hourly market will catch up.

## Edge

Multi-timeframe divergence is a well-known signal in traditional markets:

1. **Information cascade** -- 5-min intervals react to real-time BTC price movements within minutes; hourly markets aggregate slower and price in less frequently
2. **Liquidity gap** -- Hourly markets have more liquidity but update slower; 5-min markets are thinner but more responsive to current price action
3. **Convergence guarantee** -- Both timeframes cover the same underlying asset movement; if BTC is trending up in 5-min increments, the hourly must eventually reflect that
4. **Statistical edge** -- When 4+ of 6 sub-intervals agree on direction, the probability of the hourly resolving in that direction exceeds 70%

## Signal Logic

1. Discover active crypto "Up or Down" markets (BTC, ETH, SOL) via keyword search + `get_markets(limit=200)` fallback
2. Separate markets into hourly (no time range in name) and 5-min intervals (time range like 10:50AM-10:55AM)
3. Map each 5-min interval to its containing hour
4. For each hour: classify each sub-interval as UP (p > 0.55), DOWN (p < 0.45), or NEUTRAL
5. Count directional consensus: if `MIN_CONSENSUS`+ sub-intervals agree on UP or DOWN, consensus is established
6. Check the hourly market: if it is NEUTRAL (0.45-0.55), a mismatch exists
7. Trade the hourly market in the consensus direction:
   - 5-min consensus UP + hourly neutral: buy YES on hourly
   - 5-min consensus DOWN + hourly neutral: buy NO on hourly
8. Conviction scales with consensus strength (4/6 = base, 6/6 = full conviction)
9. Size = `max(MIN_TRADE, conviction * MAX_POSITION)`

### Remix Signal Ideas

- **Real-time BTC price overlay**: Compare actual Binance price trend over the last 30 minutes against the 5-min consensus -- if price confirms the direction, increase conviction
- **Volume-weighted consensus**: Weight each sub-interval's vote by its market volume -- a high-volume sub-interval at 60% UP counts more than a thin one at 56%
- **Cross-coin confirmation**: If BTC, ETH, and SOL hourly markets all show the same mismatch, conviction increases (correlated crypto moves)
- **Momentum decay filter**: Check if the 5-min consensus is strengthening or weakening over time -- if the most recent intervals are reverting to neutral, skip the trade
- **Spread-adjusted entry**: Only trade when the hourly market spread narrows below 5 cents, indicating sufficient liquidity for the convergence trade

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
| `SIMMER_MIN_VOLUME` | `3000` | Min market volume filter (USD) |
| `SIMMER_MAX_SPREAD` | `0.08` | Max bid-ask spread |
| `SIMMER_MIN_DAYS` | `0` | Min days until resolution (0 = allow same-session) |
| `SIMMER_MAX_POSITIONS` | `8` | Max concurrent open positions |
| `SIMMER_YES_THRESHOLD` | `0.38` | Buy YES only if market probability <= this |
| `SIMMER_NO_THRESHOLD` | `0.62` | Sell NO only if market probability >= this |
| `SIMMER_MIN_CONSENSUS` | `4` | Min same-direction 5-min sub-intervals for consensus (out of 6) |

## Edge Thesis

Hourly crypto markets on Polymarket aggregate the same price action that 5-minute intervals react to in real time. When the majority of sub-intervals within an hour converge on a direction, the information is already priced into the granular markets but not yet into the hourly market. This is a structural lag -- hourly markets have more liquidity and update less frequently. The convergence is not a question of if, but when. By detecting the mismatch early and trading the hourly market before it catches up, this skill captures the informational edge embedded in the faster-reacting 5-minute markets.

## Dependency

`simmer-sdk` by Simmer Markets (SpartanLabsXyz)
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
