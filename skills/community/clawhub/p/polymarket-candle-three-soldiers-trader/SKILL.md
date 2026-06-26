---
name: polymarket-candle-three-soldiers-trader
description: Trades crypto "Up or Down" 5-minute interval markets on Polymarket by detecting Three White Soldiers (3+ consecutive strong UP intervals all p>0.57) and Three Black Crows (3+ consecutive strong DOWN intervals all p<0.43). Classic candlestick continuation patterns -- when the NEXT interval lags behind the established trend, there is edge in buying the continuation direction. Conviction scales with the lag distance from the trend.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: Candle Three Soldiers Trader
  difficulty: advanced
---

# Candle Three Soldiers Trader

> **This is a template.**
> The default signal detects Three White Soldiers and Three Black Crows patterns in crypto 5-min interval markets and trades continuation on lagging intervals -- remix it with volume confirmation, real-time price feeds, or volatility filters.
> The skill handles all the plumbing (market discovery, interval parsing, pattern detection, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

Polymarket lists hundreds of live crypto "Up or Down" 5-minute interval markets per day across Bitcoin, Ethereum, and Solana. Each asks whether a coin will go up or down in a specific 5-minute window (e.g. "Bitcoin Up or Down - March 29, 10:50AM-10:55AM ET").

"Three White Soldiers" is a classic candlestick continuation pattern: three consecutive intervals all showing strong UP bias (p > 0.57). When this pattern appears but the NEXT interval hasn't caught up yet (p < 0.55), the continuation hasn't been fully priced in. "Three Black Crows" is the bearish mirror: three consecutive strong DOWN intervals (p < 0.43), and the next interval hasn't caught down (p > 0.45).

The skill detects these patterns, identifies lagging next intervals, and trades the continuation direction with conviction scaled by the lag distance.

## Edge

Three consecutive strong-bias intervals establish a micro-trend that tends to persist one more interval:

1. **Momentum persistence** -- When three intervals all show >57% bias in one direction, the underlying move is real, not noise. The 4th interval often follows but market makers are slow to adjust its price
2. **Lag exploitation** -- The next interval's price lags because Polymarket participants price each interval somewhat independently rather than incorporating the trend from adjacent intervals
3. **Multi-coin coverage** -- Scanning Bitcoin, Ethereum, and Solana multiplies pattern opportunities by 3x
4. **Short resolution** -- 5-minute markets resolve quickly; capital is recycled fast and the edge compounds

## Signal Logic

1. Discover active crypto "Up or Down" 5-min interval markets via keyword search + `get_markets(limit=200)` fallback
2. Parse each question to extract coin, date, and time window (e.g. "Bitcoin", "March 29", "10:50AM", "10:55AM")
3. Group by (coin, date) and sort by time window
4. Scan sorted intervals for three consecutive where ALL > `SOLDIER_THRESHOLD` (default 0.57) or ALL < (1 - 0.57 = 0.43)
5. After detecting pattern, check the NEXT interval:
   - Three soldiers (UP) + next < 0.55: buy YES (hasn't caught up)
   - Three crows (DOWN) + next > 0.45: buy NO (hasn't caught down)
6. Conviction scales with lag distance from trend
7. Size = `max(MIN_TRADE, conviction * MAX_POSITION)`

### Remix Signal Ideas

- **Volume confirmation**: Only trade soldiers/crows patterns where the three intervals also show above-average volume -- filters out low-liquidity noise
- **Binance real-time feed**: Confirm the underlying coin is actually trending in the soldiers/crows direction on spot markets before entering
- **Acceleration filter**: Require the three intervals to show increasing bias (p1 < p2 < p3 for soldiers) -- an accelerating trend is more likely to continue
- **Time-of-day weighting**: Crypto trends are stronger during US market hours (14:00-21:00 UTC); weight continuation signals higher during these periods
- **Multi-timeframe confirmation**: If both 5-min and 15-min intervals show soldiers pattern, increase conviction

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
| `SIMMER_SOLDIER_THRESHOLD` | `0.57` | Min probability for a strong UP interval (crows = 1 - this) |

## Edge Thesis

Candlestick continuation patterns work because they identify intervals where a micro-trend has established but hasn't fully propagated to adjacent intervals. Three consecutive strong-bias intervals are statistically significant -- they represent genuine directional momentum rather than noise. Polymarket's interval pricing is somewhat independent across adjacent windows, meaning a strong trend in intervals N, N+1, N+2 doesn't automatically get priced into interval N+3. This lag creates a window where the continuation trade has positive expected value. The skill exploits this structural inefficiency in how Polymarket participants price sequential interval markets.

## Dependency

`simmer-sdk` by Simmer Markets (SpartanLabsXyz)
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
