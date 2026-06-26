---
name: polymarket-48h-weather-distribution-trader
description: Trades mispricings in weather temperature-bin markets by reconstructing the implied probability distribution across bins for the same city and date, detecting sum violations (bins not summing to 100%) and monotonicity breaks on cumulative markets. Covers 14 cities including Munich, Dallas, Seoul, Miami, NYC, and more.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: 48h Weather Distribution Trader
  difficulty: advanced
---

# 48h Weather Distribution Trader

> **This is a template.**
> The default signal is distribution-sum and monotonicity violation detection across weather temperature-bin markets — remix it with weather API feeds, ensemble forecasts, or cross-city correlation models.
> The skill handles all the plumbing (market discovery, distribution construction, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

Polymarket lists multiple temperature bins for the same city and date:

- "Will the highest temperature in Munich be 8C on March 28?" = 40%
- "Will the highest temperature in Munich be 9C on March 28?" = 45%
- "Will the highest temperature in Munich be 10C on March 28?" = 16%

These bins form a **probability distribution** that must sum to ~100%. When they don't, individual bins are mispriced. Additionally, cumulative markets ("X C or below", "X C or higher") impose monotonicity constraints.

## The Edge: Distribution Arbitrage for Temperature Markets

In traditional markets, discrete outcome probabilities must sum to 1.0 — this is a fundamental axiom. On Polymarket, each temperature bin trades independently with its own order book and liquidity. Retail treats each bin as an isolated bet without checking the full distribution.

### Violation Type 1: Sum Deviation

All exact bins for a (city, date) must sum to ~100%:

```
P(8C) + P(9C) + P(10C) + P(11C) + ... = 100%
```

If the sum is 108%, at least one bin is overpriced. If the sum is 92%, at least one bin is underpriced.

### Violation Type 2: Cumulative Monotonicity Break

Cumulative markets must be monotonic:

```
P(<=8C) <= P(<=9C) <= P(<=10C)    [or_below: increasing]
P(>=10C) >= P(>=9C) >= P(>=8C)    [or_higher: decreasing with temp]
```

If a lower threshold has a higher "or below" probability than a higher threshold, the curve is broken.

## Why This Works

1. **Retail trades in silos** — most users view each temperature bin independently and don't cross-reference the full distribution
2. **No market maker enforcing consistency** — unlike bookmakers who balance their book, Polymarket has no mechanism to keep bins summing to 100%
3. **Mathematical, not opinion** — the violations are provable inconsistencies in the probability axioms
4. **Many cities, daily resolution** — 14 cities with daily temperature markets create a large opportunity surface

## Signal Logic

1. Discover all weather temperature markets via keyword search
2. Parse each question: extract city, temperature value, date, and type (exact/or_below/or_higher)
3. Group into distributions by (city, date)
4. For each distribution with 2+ bins:
   - Check if exact bins sum to ~100% (tolerance configurable via `SIMMER_SUM_TOLERANCE`)
   - If sum > 105%: identify and sell the most overpriced bin (highest relative to neighbors)
   - If sum < 95%: identify and buy the most underpriced bin (lowest relative to neighbors)
   - Check monotonicity on cumulative bins
5. Rank violations by magnitude
6. Trade only violations that also pass threshold gates (`YES_THRESHOLD` / `NO_THRESHOLD`)
7. Size by conviction (violation magnitude + threshold distance), not flat amount

## Supported Cities

Chengdu, Shenzhen, Munich, Dallas, Austin, San Francisco, Seoul, Chicago, Wuhan, Miami, Seattle, Los Angeles, Denver, New York City.

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
| `SIMMER_MIN_VOLUME` | `5000` | Min market volume filter (USD) |
| `SIMMER_MAX_SPREAD` | `0.08` | Max bid-ask spread |
| `SIMMER_MIN_DAYS` | `0` | Min days until resolution (0 = allow same-day) |
| `SIMMER_MAX_POSITIONS` | `8` | Max concurrent open positions |
| `SIMMER_YES_THRESHOLD` | `0.38` | Buy YES only if market probability <= this |
| `SIMMER_NO_THRESHOLD` | `0.62` | Sell NO only if market probability >= this |
| `SIMMER_SUM_TOLERANCE` | `0.05` | Allowed deviation from 100% sum before trading |

## Edge Thesis

Weather temperature markets on Polymarket are structured as discrete probability distributions. Each bin trades independently, but they are mathematically constrained to sum to 100%. When retail order flow pushes individual bins without propagating to the full distribution, the sum deviates — creating pure mathematical arbitrage. This skill reconstructs the distribution, finds where the axioms break, and trades the repair.

## Dependency

`simmer-sdk` by Simmer Markets (SpartanLabsXyz)
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
