---
name: polymarket-micro-coin-lag-trader
description: Micro-trades altcoin 5-min Up/Down markets when BTC leads with strong directional bias and ETH/SOL/XRP haven't caught up yet.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: Micro Coin Lag Trader
  difficulty: advanced
---

# Micro Coin Lag Trader

> **This is a template.**
> The default signal detects BTC lead-lag patterns in 5-minute crypto Up/Down intervals and micro-trades altcoins that haven't caught up -- remix it with real-time BTC price feeds, multi-interval momentum, or altcoin beta weighting.
> The skill handles all the plumbing (market discovery, time window grouping, lead-lag detection, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

Polymarket lists 5-minute interval Up/Down markets for BTC, ETH, SOL, and XRP. These markets resolve based on whether each coin's price goes up or down in a specific 5-minute window. BTC leads the crypto market. When BTC shows strong directional bias in a given interval (>60% Up or >60% Down), altcoins in the same or next interval typically follow -- but with a 1-2 interval lag in price discovery on Polymarket. This creates a window where altcoin probabilities haven't yet absorbed BTC's move.

Example: BTC in the 10:05 AM ET slot is at 70% Up (strong lead signal, above 60% threshold). ETH in the same slot is only at 35% Up -- a 35% gap behind BTC. The skill detects this lag, computes conviction = min(1.0, 0.35 / 0.30) = 1.0, and places a YES trade at full size ($10). If ETH were at 62% instead, the gap would be only 8%, conviction = min(1.0, 0.08 / 0.30) = 0.27, and size = max($2, 0.27 * $10) = $2.67.

## Edge

BTC is the bellwether of crypto. When BTC's Polymarket 5-minute interval shows strong directional bias, the information propagates to altcoins with a delay. Each coin's Polymarket order book is independent -- different participants, different liquidity depths, different reaction speeds. This structural lag means altcoin probabilities systematically underreact to BTC moves in the first 1-2 intervals. The skill captures this by detecting the gap between BTC's strong signal and the altcoin's lagging probability, trading the catch-up before the market corrects.

## Signal Logic

1. Discover active crypto Up/Down 5-minute markets via keyword search + `get_markets(limit=200)` fallback
2. Parse each question: extract coin (BTC/ETH/SOL/XRP), date, and time window
3. Normalize time windows to 5-minute buckets and group by (date, time_bucket)
4. Detect BTC lead signals: BTC p > `LEAD_THRESHOLD` (strong Up) or BTC p < 1 - `LEAD_THRESHOLD` (strong Down)
5. For each BTC lead signal, scan same-slot and next-slot altcoins for lag:
   - BTC strong Up + altcoin gap >= 8% behind BTC -> BUY YES on altcoin
   - BTC strong Down + altcoin gap >= 8% above BTC -> SELL NO on altcoin
6. Conviction = min(1.0, gap / 0.30) -- a 30% gap means full conviction
7. Size = max(MIN_TRADE, conviction * MAX_POSITION) -- micro sizing (MAX_POSITION=10)

### Remix Signal Ideas

- **Real-time BTC price feed**: Wire Binance BTCUSDT websocket to detect BTC direction before the Polymarket probability updates -- front-run the lag with even tighter timing
- **Multi-interval momentum**: Track BTC direction across 3+ consecutive intervals; if BTC shows 3 strong-Up intervals in a row, the lag signal is even stronger for altcoins that haven't caught up
- **Altcoin beta weighting**: SOL has higher beta to BTC than ETH; weight SOL lag signals with higher conviction since SOL should move more when it catches up
- **Volume-weighted lag**: If BTC's interval has high volume and the altcoin's has low volume, the lag is more likely real (thin market hasn't absorbed the information yet)

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
| `SIMMER_MAX_POSITION` | `10` | Max USDC per trade at full conviction (micro) |
| `SIMMER_MIN_TRADE` | `2` | Floor for any trade |
| `SIMMER_MIN_VOLUME` | `1000` | Min market volume filter (USD) |
| `SIMMER_MAX_SPREAD` | `0.12` | Max bid-ask spread |
| `SIMMER_MIN_DAYS` | `0` | Min days until resolution (0 = allow same-day) |
| `SIMMER_MAX_POSITIONS` | `15` | Max concurrent open positions |
| `SIMMER_YES_THRESHOLD` | `0.42` | Buy YES only if market probability <= this |
| `SIMMER_NO_THRESHOLD` | `0.58` | Sell NO only if market probability >= this |
| `SIMMER_LEAD_THRESHOLD` | `0.60` | BTC must exceed this for a lead signal |

## Dependency

`simmer-sdk` by Simmer Markets (SpartanLabsXyz)
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
