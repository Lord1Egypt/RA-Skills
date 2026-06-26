---
name: polymarket-24h-precipitation-range-trader
description: Trades mispricings in precipitation-range markets by reconstructing the implied probability distribution across bins for the same city and period, detecting sum violations (bins not summing to 100%) and monotonicity breaks on cumulative "more than X inches" markets. Covers cities like Seattle, Portland, Denver, Chicago, Miami, and more.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: 24h Precipitation Range Trader
  difficulty: intermediate
---

# 24h Precipitation Range Trader

> **This is a template.**
> The default signal is distribution-sum and monotonicity violation detection across precipitation-range bin markets — remix it with weather API feeds, historical precipitation data, or climate model ensembles.
> The skill handles all the plumbing (market discovery, distribution construction, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

Polymarket lists multiple precipitation range bins for the same city and period:

- "Will Seattle have more than 5 inches of precipitation in April?" = 18.8%
- "Will Seattle have between 4.5 and 5 inches in April?" = 17.5%
- "Will Seattle have between 4 and 4.5 inches in April?" = 29%
- "Will Seattle have between 3.5 and 4 inches in April?" = 19%
- "Will Seattle have between 3 and 3.5 inches in April?" = 19%
- "Will Seattle have between 2.5 and 3 inches in April?" = 20%

These range bins form a **probability distribution** that must sum to ~100%. When they don't, individual bins are mispriced. Additionally, cumulative markets ("more than X inches") must be monotonically decreasing as X increases.

## The Edge: Distribution Arbitrage for Precipitation Markets

In traditional markets, discrete outcome probabilities must sum to 1.0 — this is a fundamental axiom. On Polymarket, each precipitation range bin trades independently with its own order book and liquidity. Retail treats each bin as an isolated bet without checking the full distribution.

### Violation Type 1: Sum Deviation

All range bins for a (city, period) must sum to ~100%:

```
P(2.5-3in) + P(3-3.5in) + P(3.5-4in) + P(4-4.5in) + P(4.5-5in) + P(>5in) = 100%
```

If the sum is 108%, at least one bin is overpriced. If the sum is 92%, at least one bin is underpriced.

### Violation Type 2: Cumulative Monotonicity Break

Cumulative markets must be monotonic:

```
P(>3in) >= P(>3.5in) >= P(>4in) >= P(>4.5in) >= P(>5in)    [more_than: decreasing]
P(<3in) <= P(<3.5in) <= P(<4in) <= P(<4.5in) <= P(<5in)    [less_than: increasing]
```

If a higher threshold has a higher "more than" probability than a lower threshold, the curve is broken.

## Why This Works

1. **Retail trades in silos** — most users view each precipitation bin independently and don't cross-reference the full distribution
2. **No market maker enforcing consistency** — unlike bookmakers who balance their book, Polymarket has no mechanism to keep bins summing to 100%
3. **Mathematical, not opinion** — the violations are provable inconsistencies in the probability axioms
4. **Multiple cities, monthly resolution** — many cities with monthly precipitation markets create a large opportunity surface

## Signal Logic

1. Discover all precipitation range markets via keyword search ("precipitation", "inches", "rainfall", "Seattle")
2. Parse each question: extract city, precipitation range (between X and Y / more than X / less than X), and period (month)
3. Group into distributions by (city, period)
4. For each distribution with 2+ bins:
   - Check if all range bins sum to ~100% (tolerance configurable via `SIMMER_SUM_TOLERANCE`)
   - If sum > 105%: identify and sell the most overpriced bin (highest relative to neighbors)
   - If sum < 95%: identify and buy the most underpriced bin (lowest relative to neighbors)
   - Check monotonicity on cumulative bins ("more than X" decreasing, "less than X" increasing)
5. Rank violations by magnitude
6. Trade only violations that also pass threshold gates (`YES_THRESHOLD` / `NO_THRESHOLD`)
7. Size by conviction (violation magnitude + threshold distance), not flat amount

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
| `SIMMER_MAX_POSITION` | `35` | Max USDC per trade at full conviction |
| `SIMMER_MIN_TRADE` | `5` | Floor for any trade |
| `SIMMER_MIN_VOLUME` | `5000` | Min market volume filter (USD) |
| `SIMMER_MAX_SPREAD` | `0.08` | Max bid-ask spread |
| `SIMMER_MIN_DAYS` | `0` | Min days until resolution (0 = allow same-day) |
| `SIMMER_MAX_POSITIONS` | `8` | Max concurrent open positions |
| `SIMMER_YES_THRESHOLD` | `0.38` | Buy YES only if market probability <= this |
| `SIMMER_NO_THRESHOLD` | `0.62` | Sell NO only if market probability >= this |
| `SIMMER_SUM_TOLERANCE` | `0.05` | Allowed deviation from 100% sum before trading |

## Edge Thesis

Precipitation range markets on Polymarket are structured as discrete probability distributions. Each bin trades independently, but they are mathematically constrained to sum to 100%. When retail order flow pushes individual bins without propagating to the full distribution, the sum deviates — creating pure mathematical arbitrage. This skill reconstructs the distribution, finds where the axioms break, and trades the repair.

## Dependency

`simmer-sdk` by Simmer Markets (SpartanLabsXyz)
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
