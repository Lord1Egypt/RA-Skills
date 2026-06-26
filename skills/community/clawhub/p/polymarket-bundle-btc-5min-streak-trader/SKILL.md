---
name: polymarket-bundle-btc-5min-streak-trader
description: Trades BTC "Up or Down" 5-minute interval markets on Polymarket by detecting streaks of 3+ consecutive same-direction intervals and trading mean-reversion on the next interval. Exploits negative autocorrelation in BTC 5-min microstructure returns where retail momentum chasers systematically overprice streak continuation. Conviction scales with streak length beyond minimum threshold.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: Bundle BTC 5-Min Streak Trader
  difficulty: advanced
---

# Bundle BTC 5-Min Streak Trader

> **This is a template.**
> The default signal detects directional streaks in BTC 5-min interval markets and trades mean-reversion on the next interval -- remix it with live BTC price feeds, order flow data, or momentum-following mode.
> The skill handles all the plumbing (market discovery, interval parsing, streak detection, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

Polymarket lists ~103 live BTC "Up or Down" 5-minute interval markets per day, each asking whether Bitcoin will go up or down in a specific 5-minute window (e.g. "Bitcoin Up or Down - March 28, 11:00AM-11:05AM ET").

When 3+ consecutive intervals show the same directional bias (all Up or all Down), retail momentum chasers pile into the streak direction for the next interval. But BTC 5-minute returns exhibit negative autocorrelation at lag 1-3 (coefficient approximately -0.04 to -0.08) -- meaning streaks are more likely to reverse than continue at this timeframe.

The skill detects these streaks, identifies the next unresolved interval, and trades the contrarian direction with conviction scaled by streak length.

## Edge

BTC 5-min microstructure returns are mean-reverting, not trending. This is well-documented in market microstructure literature:

1. **Negative autocorrelation** -- 5-min BTC returns show statistically significant negative lag-1 correlation, meaning a series of Up moves makes the next Down move more likely (and vice versa)
2. **Retail momentum bias** -- Polymarket participants see 3+ consecutive Up intervals and extrapolate; this is the gambler's fallacy in reverse -- they bet on continuation when the statistics favor reversion
3. **Bundle density** -- With 103+ intervals per day, streaks of 3+ occur multiple times daily, providing consistent trading opportunities
4. **Short resolution** -- 5-minute markets resolve quickly, so capital isn't tied up; the edge compounds across many small trades

## Signal Logic

1. Discover active BTC "Up or Down" 5-min interval markets via keyword search + `get_markets(limit=200)` fallback
2. Parse each question to extract date and time window (e.g. "March 28", "11:00AM", "11:05AM")
3. Group by date and sort by time window
4. Classify each interval's directional bias: p > 0.55 = Up, p < 0.45 = Down, else Neutral
5. Walk sorted intervals looking for streaks of `STREAK_LENGTH`+ (default 3) same-direction bias
6. After a streak, evaluate the NEXT interval for mean-reversion:
   - After Up streak: sell NO (bet on Down / reversion)
   - After Down streak: buy YES (bet on Up / reversion)
7. Conviction scales with streak length beyond minimum (bonus +0.1 per extra streak interval, capped)
8. Size = `max(MIN_TRADE, conviction * MAX_POSITION)`

### Remix Signal Ideas

- **Binance real-time BTC price feed**: Compare the actual price movement during the streak intervals against the market probabilities -- if price moved 0.5% up in 15 minutes but the market only shows 55% Up bias, the streak might continue (switch to momentum mode)
- **Order flow imbalance**: Wire Binance order book depth into the signal -- if bid depth is 3x ask depth during a Down streak, the reversion is more likely and conviction should increase
- **Volatility regime filter**: In high-vol regimes (VIX > 25, BTC realized vol > 80%), streaks are longer and reversion is sharper; in low-vol regimes, streaks are noise and reversion is weaker -- scale conviction accordingly
- **Time-of-day pattern**: BTC 5-min autocorrelation is strongest during Asian session (00:00-08:00 UTC) and weakest during US equity hours (14:00-21:00 UTC); weight streak signals by session
- **Momentum mode toggle**: Set `SIMMER_STREAK_MODE=momentum` to trade WITH the streak instead of against it -- useful during strong trend days when the daily candle is >3% in one direction

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
| `SIMMER_STREAK_LENGTH` | `3` | Minimum consecutive same-direction intervals to trigger |

## Edge Thesis

BTC 5-minute interval markets are the highest-frequency prediction markets on Polymarket. With 103+ markets per day, the statistical properties of BTC microstructure returns dominate over any single market's noise. Negative autocorrelation at the 5-min timeframe is a robust empirical finding across crypto exchanges -- it reflects the bid-ask bounce, inventory management by market makers, and mean-reversion in order flow. Retail Polymarket participants don't know this. They see 3 consecutive Up intervals and bet on a 4th. The statistics say the 4th is more likely Down. This skill trades that gap.

## Dependency

`simmer-sdk` by Simmer Markets (SpartanLabsXyz)
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
