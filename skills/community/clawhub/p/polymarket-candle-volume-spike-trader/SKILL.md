---
name: polymarket-candle-volume-spike-trader
description: Cross-coin volume spike detection for crypto Up or Down markets on Polymarket. When 3+ coins (BTC, ETH, SOL, XRP) simultaneously show strong same-direction candles above 58% in the same 5-minute window, it confirms cross-market conviction. Trades lagging coins in the next interval that havent caught up to the confirmed directional move.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: Candle Volume Spike Trader
  difficulty: advanced
---

# Candle Volume Spike Trader

> **This is a template.**
> The default signal detects cross-coin volume spikes in 5-min crypto candle markets and trades lagging coins in the next interval -- remix it with real-time exchange volume data, order book depth, or funding rate signals.
> The skill handles all the plumbing (market discovery, interval parsing, spike detection, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

Polymarket lists 5-minute "Up or Down" interval markets for multiple cryptocurrencies (BTC, ETH, SOL, XRP). Each market asks whether a specific coin will go up or down in a 5-minute window (e.g. "Bitcoin Up or Down - March 29, 10:50AM-10:55AM ET").

A single coin showing 58% directional bias might be noise -- idiosyncratic flow, a large limit order, or thin liquidity. But when 3+ coins ALL show strong same-direction bias (>58%) in the same 5-minute window, it reflects a genuine cross-market move: a macro catalyst (rate decision, whale liquidation, exchange outage) driving all crypto in the same direction.

The skill detects these cross-coin "volume spikes" and then checks the NEXT 5-minute interval. Any coin that hasn't caught up to the confirmed direction is a trade -- it will converge.

## Edge

Cross-asset confirmation filters noise from signal in short-timeframe crypto markets:

1. **Noise filtering** -- A single coin at 58% could be anything; 3+ coins at 58%+ in the same direction is statistically significant cross-market confirmation
2. **Macro catalyst detection** -- Cross-coin moves are driven by macro events that affect all crypto simultaneously; these events persist beyond a single 5-min interval
3. **Laggard convergence** -- When BTC, ETH, and SOL all spike UP but XRP hasn't moved yet, XRP is mispriced and will catch up in the next interval
4. **Short resolution** -- 5-minute markets resolve quickly; capital isn't tied up waiting for convergence

## Signal Logic

1. Discover active crypto "Up or Down" markets (BTC, ETH, SOL, XRP) via keyword search + `get_markets(limit=200)` fallback
2. Parse each question to extract coin, date, and start time in minutes
3. Group markets by (date, time_window) to create cross-coin snapshots
4. For each window: count coins with strong directional bias:
   - UP if p > `SPIKE_THRESHOLD` (default 0.58)
   - DOWN if p < 1 - `SPIKE_THRESHOLD` (default 0.42)
5. If `MIN_COINS`+ (default 3) coins agree on direction: volume spike confirmed
6. Check the NEXT time window (+5 minutes) for each coin:
   - If a coin hasn't caught up (not yet showing strong direction), trade it
   - UP spike + lagging coin: buy YES
   - DOWN spike + lagging coin: buy NO
7. Conviction scales with number of confirming coins (3/4 = base, 4/4 = full)
8. Size = `max(MIN_TRADE, conviction * MAX_POSITION)`

### Remix Signal Ideas

- **Exchange volume overlay**: Wire Binance/Coinbase real-time volume into the signal -- if total exchange volume is 3x normal during the spike, conviction increases significantly
- **Funding rate confirmation**: Check perpetual futures funding rates; if funding rate aligns with the spike direction, the move has legs and laggards will converge faster
- **Order book depth asymmetry**: If the lagging coin has 5x more bid depth than ask depth during a DOWN spike, the convergence might fail -- reduce conviction
- **Spike magnitude weighting**: Not all spikes are equal; if the average bias across confirming coins is 65% vs 59%, the stronger spike deserves higher conviction on the laggard trade
- **Time decay filter**: Only trade laggards within 1-2 intervals of the spike; after 3+ intervals, the information is stale and convergence may not happen

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
| `SIMMER_SPIKE_THRESHOLD` | `0.58` | Min conviction for a coin to count as strong directional |
| `SIMMER_MIN_COINS` | `3` | Min coins agreeing on direction for spike confirmation |

## Edge Thesis

Single-coin directional signals in 5-minute crypto markets are noisy. But crypto assets are highly correlated -- when a macro catalyst hits, all coins move together. The key insight is that not all coins react at the same speed. BTC and ETH, with deeper liquidity, often lead. SOL and XRP, with thinner Polymarket books, lag by one or two intervals. When 3+ coins confirm a direction simultaneously, the signal-to-noise ratio jumps dramatically. Any coin that hasn't caught up is mispriced relative to the cross-market consensus. This skill captures that convergence trade -- buying the laggard before it catches up to the pack.

## Dependency

`simmer-sdk` by Simmer Markets (SpartanLabsXyz)
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
