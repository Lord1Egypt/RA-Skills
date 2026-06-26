---
name: polymarket-sports-live
description: >
  Exploits price lag between ESPN real-time scores and Polymarket sports markets.
  Uses Gaussian win-probability models for NBA/NFL/NHL and Poisson for soccer to
  calculate fair odds from live game state. Trades when model probability diverges
  more than 10% from Polymarket price.
metadata:
  author: "Mibayy"
  version: "2.0.5"
  displayName: "Live Sports Score Arbitrage"
  type: "automaton"
  difficulty: "intermediate"
---

# Live Sports Score Arbitrage

Real-time live score arbitrage against Polymarket sports markets using ESPN data.

## What It Does

Every 2 minutes, pulls live scores from ESPN's public API and calculates fair
win probabilities using sport-specific statistical models:

| Sport | Model | Key Parameter |
|-------|-------|--------------|
| **NBA** | Gaussian | sigma = 12.5 points |
| **NFL** | Gaussian | sigma = 13.5 points |
| **NHL** | Gaussian | sigma = 1.5 goals |
| **Soccer** | Poisson | lambda = 1.35 goals/90min |

**Gaussian model**: P(win) = CDF(lead / (sigma * sqrt(t_remaining / T)))

**Poisson model**: Calculates expected goals from current rate, sums probability
of all winning scorelines.

## Edge Source

Polymarket prices update slowly during live games - often 30-120 seconds behind
real scoring events. ESPN's API updates near-instantly. This latency gap is the edge.

## Scheduling

Runs every 2 minutes via cron (`*/2 * * * *`). Managed automaton (auto-executes on schedule).
Only trades when divergence exceeds 10%.

## Requirements

**pip dependencies:** `simmer-sdk`, `requests`

**Environment variables:**
- `SIMMER_API_KEY` (required) - get from simmer.markets/dashboard
- `TRADING_VENUE` (optional) - defaults to `sim` for paper trading, set to `polymarket` for real
- `SPORTS_DIVERGENCE_THRESHOLD` (optional) - minimum divergence to trigger trade, defaults to `0.10` (10%)
- `SPORTS_TRADE_SIZE` (optional) - trade size in USD, defaults to `20.0`

## Usage

```bash
python sports_live.py                  # dry run (default, no trades)
python sports_live.py --live           # real trades via SimmerClient
python sports_live.py --live --quiet   # cron mode
```

> Dry-run by default. Pass `--live` to execute real trades.

## Trade Execution Path

1. `sports_live.py` fetches live scores from ESPN public API (no auth needed)
2. Calculates fair win probability using Gaussian (NBA/NFL/NHL) or Poisson (soccer) models
3. Finds matching Polymarket markets via `SimmerClient.find_markets()`
4. Compares model probability to Polymarket price, applies >10% divergence threshold
5. If `--live`: calls `SimmerClient.trade()` with market_id, side, amount, reasoning
6. If dry-run (default): logs the signal but does NOT execute any trade

## Security

- All trades go through `SimmerClient.trade()` only. No direct CLOB or wallet access.
- Reads `SIMMER_API_KEY` and optionally `TRADING_VENUE` from env. No other secrets.
- No wallet private keys are required or read by this script.
- Dry-run is the default. The `--live` flag must be explicitly passed to execute trades.

> Remixable Template: Fork this skill to adjust sigma values, add new
> sports (MLB, tennis), change the divergence threshold, or plug in different
> live score sources.
