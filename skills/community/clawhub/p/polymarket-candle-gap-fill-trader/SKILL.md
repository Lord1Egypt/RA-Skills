---
name: polymarket-candle-gap-fill-trader
description: Trades gap-fill reversions on Polymarket 5-minute crypto interval markets. When consecutive intervals have contradictory strong signals -- prior interval resolves strongly one direction, next opens strongly the other -- the outlier tends to revert toward neutral. A classic gap-fill pattern adapted from traditional candlestick analysis to Polymarket microstructure with conviction-based position sizing scaled by gap magnitude.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: Candle Gap Fill Trader
  difficulty: advanced
---

# Candle -- Gap Fill Trader

> **This is a template.**
> The default signal detects price gaps between consecutive crypto 5-minute interval markets and trades the reversion using conviction-based sizing. The skill handles all the plumbing (interval parsing, gap detection, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

Polymarket lists 5-minute interval markets for BTC, ETH, SOL, and XRP: "Will BTC be Up or Down in the 10:50AM-10:55AM ET interval?" These resolve to YES (up) or NO (down) based on actual price movement. A "gap" occurs when consecutive intervals have contradictory strong signals -- interval N at 62% (strong UP) followed by interval N+1 at 38% (strong DOWN). In traditional candlestick analysis, gaps tend to "fill" as price reverts to close the discontinuity. On Polymarket, when consecutive intervals disagree strongly, the outlier tends to revert toward 0.50.

## Edge

Unlike generic mean-reversion strategies that trade any low-probability market, this skill specifically targets **structural gaps** between consecutive intervals -- cases where the market pricing implies an abrupt directional reversal that exceeds a minimum gap size. The gap-fill is structurally sound because:

1. **Microstructure continuity** -- consecutive 5-minute intervals share overlapping information sets; a sharp reversal in pricing implies either new information (rare) or noise (common)
2. **Retail overreaction** -- Polymarket participants observe one strong interval and overcorrect in the opposite direction for the next, creating systematic mispricing at gap boundaries
3. **Mean-reversion at extremes** -- when two consecutive intervals disagree by >12 percentage points, the second interval is statistically more likely to resolve closer to 50% than its current pricing suggests
4. **Independent resolution** -- each interval resolves based on actual price movement, so a gap in market pricing does not reflect a genuine structural shift in the underlying asset's trajectory

## Signal Logic

1. Discover crypto interval markets via keyword search (`Bitcoin Up or Down`, `Ethereum Up or Down`, `Solana Up or Down`, `XRP Up or Down`) with a `get_markets(limit=200)` fallback
2. Parse each question to extract (coin, date_str, start_time_minutes) using regex
3. Group intervals by (coin, date) and sort by time
4. Scan consecutive pairs for gaps: prior is UP (p>0.55) and current is DOWN (p<0.45), or vice versa, with |p_current - p_prior| > `GAP_SIZE`
5. Trade the gap fill:
   - **Current is DOWN outlier after prior UP** -> buy YES (gap fill upward toward 0.50)
   - **Current is UP outlier after prior DOWN** -> buy NO (gap fill downward toward 0.50)
6. Size by conviction (distance from threshold), not flat amount

### Remix Signal Ideas

- **Volume-weighted gaps** -- weight gap significance by the trading volume in both intervals; high-volume gaps are more meaningful than low-volume ones
- **Multi-interval gap confirmation** -- require 2+ prior intervals to agree before classifying the current interval as a gap outlier
- **Binance tick data** -- use real-time price data to confirm whether the gap reflects genuine new information or is pure noise
- **Cross-coin gap correlation** -- if BTC and ETH both gap in the same direction simultaneously, it may reflect genuine macro news rather than noise
- **Time-of-day filter** -- gaps during low-volume hours (e.g., early morning ET) may be noisier and less likely to fill

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
| `SIMMER_MIN_TRADE` | `5` | Floor for any trade (min USDC regardless of conviction) |
| `SIMMER_MIN_VOLUME` | `3000` | Min market volume filter (USD) |
| `SIMMER_MAX_SPREAD` | `0.10` | Max bid-ask spread |
| `SIMMER_MIN_DAYS` | `1` | Min days until resolution |
| `SIMMER_MAX_POSITIONS` | `10` | Max concurrent open positions |
| `SIMMER_YES_THRESHOLD` | `0.38` | Buy YES only if market probability <= this |
| `SIMMER_NO_THRESHOLD` | `0.62` | Sell NO only if market probability >= this |
| `SIMMER_GAP_SIZE` | `0.12` | Min probability gap between consecutive intervals to trigger trade |

## Edge Thesis

Crypto 5-minute interval markets on Polymarket exhibit gap-fill behavior analogous to traditional candlestick markets. When consecutive intervals have contradictory strong signals -- one priced strongly UP and the next strongly DOWN (or vice versa) with a gap exceeding 12 percentage points -- the outlier interval systematically overestimates the directional reversal. This is because consecutive 5-minute windows share overlapping market conditions, and abrupt pricing reversals between adjacent intervals more often reflect retail overreaction than genuine new information. The gap-fill trade exploits this by buying the reversion with conviction-based sizing that scales with the distance from the trading threshold.

## Dependency

`simmer-sdk` by Simmer Markets (SpartanLabsXyz)
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
