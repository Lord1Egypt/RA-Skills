---
name: polymarket-candle-harami-trader
description: Detects harami (inside bar) candlestick patterns on Polymarket crypto 5-minute interval markets. A harami forms when a small-range interval (near 50%) appears after a large-range interval (far from 50%), signalling indecision after a strong move -- often followed by reversal. Targets BTC, ETH, SOL, and XRP Up or Down bundles with conviction-based position sizing.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: Candle Harami Pattern Trader
  difficulty: advanced
---

# Candle -- Harami Pattern Trader

> **This is a template.**
> The default signal detects harami (inside bar) candlestick patterns in crypto 5-minute interval markets and trades the expected reversal using conviction-based sizing. The skill handles all the plumbing (interval parsing, pattern detection, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

Polymarket lists 5-minute interval markets for BTC, ETH, SOL, and XRP: "Will Bitcoin be Up or Down in the 10:50AM-10:55AM ET interval?" These resolve to YES (up) or NO (down) based on actual price movement. A **harami** (inside bar) pattern forms when a large-range interval (probability far from 50%, indicating a strong directional move) is immediately followed by a small-range interval (probability near 50%, indicating indecision). The small candle is "contained" within the body of the large one. This classic candlestick pattern signals that the strong move has lost momentum, and a reversal is likely on the next interval.

## Edge

Unlike generic mean-reversion strategies that simply fade any extreme reading, this skill specifically targets the **harami pattern** -- a two-candle formation with a precise structural meaning:

1. **Pattern recognition** -- the harami is one of the most reliable reversal patterns in traditional technical analysis, adapted here to Polymarket's discrete 5-minute intervals
2. **Indecision after conviction** -- a large candle shows strong directional conviction; a subsequent small candle near 50% shows that conviction has evaporated, creating a structural reversal setup
3. **Confirmation gating** -- the skill checks the third interval (confirmation candle) and only trades if it hasn't already moved in the reversal direction, ensuring the edge hasn't been priced in
4. **Independent resolution** -- each 5-minute interval resolves independently, so the harami pattern captures genuine shifts in market microstructure rather than mechanical carry-over

## Signal Logic

1. Discover crypto interval markets via keyword search (`Bitcoin Up or Down`, `Ethereum Up or Down`, `Solana Up or Down`, `XRP Up or Down`) with a `get_markets(limit=200)` fallback
2. Parse each question to extract (coin, date, start_time_minutes) using regex
3. Group intervals by (coin, date) and sort by time
4. Scan each group for consecutive pairs where:
   - Interval N is **large**: probability < 0.40 or > 0.60 (distance from 0.5 exceeds `HARAMI_LARGE`)
   - Interval N+1 is **small**: probability between 0.48 and 0.52 (distance from 0.5 within `HARAMI_SMALL`)
5. Determine harami direction:
   - **Bullish harami**: large DOWN (p < 0.40) followed by small neutral -> reversal UP expected
   - **Bearish harami**: large UP (p > 0.60) followed by small neutral -> reversal DOWN expected
6. Check interval N+2 (confirmation): only trade if it hasn't already moved in the reversal direction
7. Size by conviction (distance from threshold), not flat amount

### Remix Signal Ideas

- **Volume-weighted harami** -- weight the pattern detection by trading volume; high-volume large candles followed by low-volume small candles produce stronger reversal signals
- **Multi-timeframe confirmation** -- check if the harami pattern aligns with a broader trend reversal across 15-minute or hourly aggregated intervals
- **Cross-coin harami** -- if BTC shows a harami and ETH/SOL show the same pattern simultaneously, the reversal signal is stronger (correlated exhaustion)
- **Doji refinement** -- distinguish between harami where the small candle is exactly 50% (doji) vs. slightly biased; true doji haramis have higher reversal rates
- **Engulfing follow-up** -- after a harami reversal, look for an engulfing pattern in the same direction to add to the position

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
| `SIMMER_HARAMI_LARGE` | `0.10` | Min distance from 0.5 for the large candle |
| `SIMMER_HARAMI_SMALL` | `0.02` | Max distance from 0.5 for the small candle |

## Edge Thesis

Crypto 5-minute interval markets on Polymarket exhibit classic candlestick reversal patterns. When a strong directional interval (far from 50%) is immediately followed by a neutral interval (near 50%), this harami formation signals that directional conviction has evaporated. The small candle represents market indecision after a strong move -- a well-known precursor to reversal in both traditional and crypto technical analysis. The skill exploits this by trading the confirmation interval in the reversal direction with conviction-based sizing that scales with the distance from the trading threshold.

## Dependency

`simmer-sdk` by Simmer Markets (SpartanLabsXyz)
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
