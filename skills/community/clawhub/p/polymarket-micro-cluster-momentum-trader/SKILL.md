---
name: polymarket-micro-cluster-momentum-trader
description: Trades cluster momentum continuation in 5-minute crypto Up/Down bundles on Polymarket. When 2+ coins (BTC, ETH, SOL, XRP) all show the same directional bias in one time slot, trades continuation on the next slot at micro sizes.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: Micro Cluster Momentum Trader
  difficulty: advanced
---

# Micro Cluster Momentum Trader

> **This is a template.**
> The default signal is cross-coin cluster momentum detection in 5-minute crypto Up/Down bundles -- remix it with volume confirmation, on-chain flow data, or additional time horizons.
> The skill handles all the plumbing (market discovery, time window grouping, cluster detection, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

Polymarket lists "Bitcoin Up or Down", "Ethereum Up or Down", "Solana Up or Down", and "XRP Up or Down" markets for the same 5-minute windows throughout the day. When 2 or more of these coins ALL show the same directional bias in one time slot, this cross-coin convergence is a strong momentum confirmation signal. The skill trades continuation in the NEXT 5-minute slot at micro sizes.

Example: In the 10:05 AM ET window, BTC=Up(58%), ETH=Up(60%), SOL=Up(57%), XRP=Up(54%). Two or more coins show Up bias (p > 0.53). This is an Up cluster. The skill then looks at the 10:10 AM window and trades YES on any coin where p <= YES_THRESHOLD (continuation bet).

## Edge

This is a CONVERGENCE play -- the opposite of divergence-based skills like bundle-cross-coin-5min. When the entire crypto market agrees on a direction within a short window, that momentum tends to carry over. The key insight: independent Polymarket order books for different coins reaching the same conclusion simultaneously is a stronger signal than any single coin's price action. Three separate groups of traders, trading three separate order books, all arriving at the same directional view -- that is cross-validated momentum.

## Signal Logic

1. Discover active crypto Up/Down 5-minute markets via keyword search + `get_markets(limit=200)` fallback
2. Parse each question: extract coin (BTC/ETH/SOL/XRP), date, and time window
3. Normalize time windows to 5-minute buckets and group by (date, time_bucket)
4. For each window with 2+ coins: check directional bias
   - Up bias: p > `CLUSTER_BIAS` (default 0.53)
   - Down bias: p < 1 - `CLUSTER_BIAS` (default 0.47)
5. If Up cluster >= `MIN_CLUSTER_SIZE` (default 2): look at NEXT 5-min slot, trade YES where p <= `YES_THRESHOLD`
6. If Down cluster >= `MIN_CLUSTER_SIZE`: look at NEXT slot, trade NO where p >= `NO_THRESHOLD`
7. Conviction scales with threshold distance AND cluster strength (more coins = higher multiplier)
8. Size by conviction, not flat amount -- micro sizing (MAX_POSITION=10)

### Remix Signal Ideas

- **Volume confirmation**: Only count a coin toward the cluster if its Polymarket volume in that window exceeds a threshold
- **Gradient strength**: Weight cluster signal by how far above CLUSTER_BIAS each coin is (stronger consensus = higher conviction)
- **Multi-window persistence**: Require the cluster to persist across 2 consecutive windows before trading the 3rd
- **Exchange correlation feed**: Pull real-time BTC/ETH/SOL/XRP prices from Binance to confirm the on-chain momentum matches Polymarket consensus

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
| `SIMMER_CLUSTER_BIAS` | `0.53` | Cluster directional bias threshold |
| `SIMMER_MIN_CLUSTER_SIZE` | `2` | Min coins agreeing for a cluster signal |

## Edge Thesis

Individual coin price movements on Polymarket can be noisy -- retail flow, timing differences, order book depth all create short-term noise. But when 2 or more separate coins ALL independently converge on the same directional view within the same 5-minute window, that is meaningful signal. Each coin's market is an independent order book with its own participants. Cross-coin agreement is like having 2+ independent confirmations of the same thesis.

Momentum carries across adjacent 5-minute windows because:
- Macro crypto moves (BTC dominance, risk-on/off shifts) persist longer than 5 minutes
- Retail participants who pushed one window's prices will likely participate in the next
- Information propagation is not instant -- some participants are still reacting when the next window opens
- The cluster signal filters out noise: a single coin moving is inconclusive, but 2+ coins moving together is structural

## Dependency

`simmer-sdk` by Simmer Markets (SpartanLabsXyz)
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
