---
name: polymarket-24h-price-curve-arb-trader
description: Trades structural mispricings in crypto price-threshold markets by reconstructing the implied probability distribution curve across multiple strike levels and detecting mathematical violations such as monotonicity breaks and range-sum inconsistencies.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: 24h Price Curve Arbitrage Trader
  difficulty: advanced
---

# 24h Price Curve Arbitrage Trader

> **This is a template.**
> The default signal is implied-CDF violation detection across crypto price-threshold markets — remix it with additional assets, curve-fitting models, or cross-venue price feeds.
> The skill handles all the plumbing (market discovery, curve construction, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

Polymarket lists dozens of price-threshold markets for the same asset and date:

- "Will BTC be above $64,000 on March 27?"
- "Will BTC be above $68,000 on March 27?"
- "Will BTC be between $68,000 and $70,000 on March 27?"
- "Will BTC be above $70,000 on March 27?"

Retail trades each market as an isolated bet. But together, these markets form an **implied probability distribution curve** — a CDF of where the market thinks the price will be.

This skill reconstructs that curve and finds where it is **mathematically broken**.

## The Edge: Butterfly Arbitrage for Prediction Markets

In options markets, quant traders analyze the implied volatility surface across strikes to find mispriced options. This is the prediction market equivalent.

### Violation Type 1: Monotonicity Break

The probability of being above a lower price must always be greater than or equal to being above a higher price:

```
P(BTC > $68k) >= P(BTC > $70k) >= P(BTC > $74k)
```

If a higher strike is priced above a lower strike, the curve is broken.

### Violation Type 2: Range-Sum Inconsistency

A "between" market's price must equal the difference of two "above" markets:

```
P($68k < BTC < $70k) == P(BTC > $68k) - P(BTC > $70k)
```

If the market prices the range at 54% but the above-markets imply 48%, that's 6% of mathematical arbitrage.

## Why This Works

1. **Retail trades in silos** — most users view each market independently and don't cross-reference the full strike ladder
2. **No options infrastructure** — unlike traditional markets, there's no market maker maintaining curve consistency across strikes
3. **Mathematical, not opinion** — the violations are provable inconsistencies, not subjective edge calls
4. **High volume** — BTC price markets are the most actively traded category on Polymarket

## Signal Logic

1. Discover all crypto price-threshold markets via keyword search
2. Parse each question: extract asset (BTC/ETH), strike price(s), date, and type (above/between/dip)
3. Group into curves by (asset, date)
4. For each curve with 2+ points:
   - Check monotonicity across "above" markets
   - Check range-sum consistency for "between" markets
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
| `SIMMER_MIN_VIOLATION` | `0.04` | Min curve violation magnitude to trigger a trade |

## Edge Thesis

Traditional options markets have market makers who enforce curve consistency (no-arbitrage pricing). Polymarket has no such mechanism — each market is priced by its own order book with its own liquidity pool. This creates systematic micro-inconsistencies in the implied distribution, especially when:

- New markets are created at previously unlisted strikes
- Large directional flow pushes one strike without propagating to neighbors
- Market makers leave gaps during low-liquidity hours

This skill treats the strike ladder as a probability lattice and trades the repair.

## Dependency

`simmer-sdk` by Simmer Markets (SpartanLabsXyz)
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
