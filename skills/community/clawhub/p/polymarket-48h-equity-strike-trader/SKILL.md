---
name: polymarket-48h-equity-strike-trader
description: Trades structural mispricings in equity/stock price-threshold markets by reconstructing the implied probability curve across strike levels for the same company and period, detecting monotonicity breaks and range-sum inconsistencies in strike ladders for PLTR, MSFT, NVDA, TSLA, SpaceX, Nasdaq-100, and other equity markets.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: 48h Equity Strike Trader
  difficulty: advanced
---

# 48h Equity Strike Trader

> **This is a template.**
> The default signal is implied-CDF violation detection across equity price-threshold markets -- remix it with additional tickers, curve-fitting models, or cross-venue price feeds.
> The skill handles all the plumbing (market discovery, curve construction, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

Polymarket lists equity strike-ladder markets analogous to options chains:

- "Will Palantir (PLTR) finish week above $152?" = 7%
- "Will Palantir (PLTR) finish week above $153?" = 23.5%  <-- VIOLATION!
- "Will Palantir (PLTR) finish week above $154?" = 18.5%
- "Will Microsoft (MSFT) finish week above $370?" = 5%
- Tesla delivery bins: <350k=46%, 350-375k=47.5%, 375-400k=13.5%

Retail trades each market as an isolated bet. But together, these markets form an **implied probability distribution curve** across strike levels.

This skill reconstructs that curve and finds where it is **mathematically broken**.

## The Edge: Options-Chain Arbitrage for Prediction Markets

In traditional options markets, market makers enforce no-arbitrage pricing across strikes. Polymarket has no such mechanism -- each market is its own order book.

### Violation Type 1: Monotonicity Break

The probability of being above a lower price must always be >= being above a higher price:

```
P(PLTR > $152) >= P(PLTR > $153) >= P(PLTR > $154)
```

If a higher strike is priced above a lower strike, the curve is broken.

### Violation Type 2: Range-Sum Inconsistency

A "between" market's price must equal the difference of two "above" markets:

```
P($370 < MSFT < $380) == P(MSFT > $370) - P(MSFT > $380)
```

### Violation Type 3: Bin-Sum Overflow/Underflow

When a market has exhaustive bins (e.g., Tesla deliveries), all bins must sum to ~100%:

```
P(<350k) + P(350-375k) + P(375-400k) + P(>400k) ~= 100%
```

## Why This Works

1. **Retail trades in silos** -- most users view each market independently and don't cross-reference the full strike ladder
2. **No options infrastructure** -- unlike traditional markets, there's no market maker maintaining curve consistency across strikes
3. **Mathematical, not opinion** -- the violations are provable inconsistencies, not subjective edge calls
4. **Broad coverage** -- applies to any equity/index with multiple strike-level markets

## Signal Logic

1. Discover equity price-threshold markets via keyword search (MSFT, PLTR, NVDA, TSLA, SpaceX, Nasdaq, etc.)
2. Parse each question: extract ticker, strike price(s), date/period, and type (above/between/below)
3. Group into curves by (ticker, date/period)
4. For each curve with 2+ points:
   - Check monotonicity across "above" markets
   - Check range-sum consistency for "between" markets
   - Check bin-sum consistency for exhaustive bin sets
5. Rank violations by magnitude
6. Trade only violations that also pass threshold gates (`YES_THRESHOLD` / `NO_THRESHOLD`)
7. Size by conviction (violation magnitude), not flat amount

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
| `SIMMER_MIN_VIOLATION` | `0.03` | Min curve violation magnitude to trigger a trade |

## Edge Thesis

Traditional options markets have market makers who enforce curve consistency (no-arbitrage pricing). Polymarket has no such mechanism -- each market is priced by its own order book with its own liquidity pool. This creates systematic micro-inconsistencies in the implied distribution, especially when:

- New markets are created at previously unlisted strikes
- Large directional flow pushes one strike without propagating to neighbors
- Market makers leave gaps during low-liquidity hours
- Delivery/unit-count bin markets are added piecemeal without ensuring they sum correctly

This skill treats the equity strike ladder as a probability lattice and trades the repair.

## Dependency

`simmer-sdk` by Simmer Markets (SpartanLabsXyz)
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
