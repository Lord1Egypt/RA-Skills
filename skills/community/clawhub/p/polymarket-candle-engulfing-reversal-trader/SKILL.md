---
name: polymarket-candle-engulfing-reversal-trader
description: Detects engulfing reversal patterns in crypto 5-minute interval markets on Polymarket. A bullish engulfing occurs when an interval completely reverses the prior interval with stronger conviction -- signaling a powerful reversal that the next interval should continue. Targets BTC, ETH, SOL, and XRP Up or Down bundles with conviction-based position sizing.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: Candle Engulfing Reversal Trader
  difficulty: advanced
---

# Candle -- Engulfing Reversal Trader

> **This is a template.**
> The default signal detects engulfing reversal patterns in crypto 5-minute interval markets and trades the post-engulfing continuation using conviction-based sizing. The skill handles all the plumbing (interval parsing, engulfing detection, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

Polymarket lists 5-minute interval markets for BTC, ETH, SOL, and XRP: "Will Bitcoin be Up or Down in the 10:50AM-10:55AM ET interval?" These resolve to YES (up) or NO (down) based on the actual price movement. An engulfing pattern occurs when one interval completely reverses the prior interval with stronger conviction. If interval N was DOWN (p=42%) and interval N+1 is UP (p=58%), and the UP move is larger than the DOWN move, that is a bullish engulfing -- one of the strongest reversal signals in candlestick analysis. The NEXT interval after the engulfing pair should continue the reversal direction.

## Edge

Unlike momentum or mean-reversion strategies that look at extended streaks, the engulfing pattern targets a specific two-bar structure that signals a decisive shift in market sentiment. The edge arises because:

1. **Conviction asymmetry** -- the engulfing interval does not merely reverse the prior direction; it does so with GREATER conviction, indicating that the new direction has stronger backing
2. **Reversal confirmation** -- a single reversal could be noise, but an engulfing (where the reversal is larger than the original move) statistically predicts continuation in the new direction
3. **Systematic underpricing** -- the post-engulfing interval is often priced near 50% because participants are uncertain whether the reversal will hold; the engulfing pattern provides evidence that it will
4. **Bundle independence** -- each 5-minute interval resolves independently, so the engulfing signal from intervals N and N+1 provides informational (not mechanical) alpha for interval N+2

## Signal Logic

1. Discover crypto interval markets via keyword search (`Bitcoin Up or Down`, `Ethereum Up or Down`, `Solana Up or Down`, `XRP Up or Down`) with a `get_markets(limit=200)` fallback
2. Parse each question to extract (coin, date, start_time_minutes, end_time_minutes) using regex
3. Group intervals by (coin, date) and sort by time
4. Classify each interval: UP if p > 0.55, DOWN if p < 0.45, NEUTRAL if 0.45-0.55
5. Scan consecutive pairs for engulfing patterns:
   - **Bullish engulfing**: prior p < 0.48, current p > 0.55, AND (current - 0.5) > (0.5 - prior), AND the conviction difference >= `ENGULF_THRESHOLD`
   - **Bearish engulfing**: prior p > 0.52, current p < 0.45, AND (0.5 - current) > (prior - 0.5), AND the conviction difference >= `ENGULF_THRESHOLD`
6. Check the NEXT interval after the engulfing pair:
   - **Bullish engulfing** -> next interval should continue UP; if priced <= YES_THRESHOLD, buy YES
   - **Bearish engulfing** -> next interval should continue DOWN; if priced >= NO_THRESHOLD, buy NO
7. Size by conviction (distance from threshold), not flat amount

### Remix Signal Ideas

- **Double engulfing** -- require two consecutive engulfing patterns (or engulfing followed by a strong same-direction interval) for a higher-confidence signal
- **Volume-weighted engulfing** -- weight the pattern by trading volume; high-volume engulfing is a much stronger signal than low-volume
- **Cross-coin engulfing** -- if BTC prints a bullish engulfing and ETH/SOL have not yet reversed, trade the lagging coins for a cross-coin engulfing play
- **Order flow confirmation** -- check Polymarket order book depth after the engulfing to see if large orders are backing the new direction
- **Engulfing + trend context** -- engulfing patterns at the end of a multi-interval trend (reversal after 3+ intervals in one direction) are stronger than engulfing in choppy conditions

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
| `SIMMER_ENGULF_THRESHOLD` | `0.06` | Min conviction difference for engulfing pattern |

## Edge Thesis

Crypto 5-minute interval markets on Polymarket exhibit a systematic mispricing after engulfing patterns. When a DOWN interval (p=42%) is followed by a stronger UP interval (p=58%), the post-engulfing interval is typically priced near 50% -- the market treats the reversal as uncertain. But the engulfing pattern, where the reversal exceeds the original move in magnitude, is one of the most reliable two-bar reversal signals in technical analysis. The conviction asymmetry (the new direction is stronger than the old) provides statistical evidence that the reversal will continue. This skill exploits the gap between the market-implied continuation probability and the pattern-implied probability, with conviction-based sizing that scales with the distance from the trading threshold.

## Dependency

`simmer-sdk` by Simmer Markets (SpartanLabsXyz)
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
