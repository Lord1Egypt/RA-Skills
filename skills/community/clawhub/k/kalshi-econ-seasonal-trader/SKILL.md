---
name: kalshi-econ-seasonal-trader
description: Trades CPI/inflation markets on Kalshi using documented seasonal patterns in CPI data. Energy costs spike summer, housing adjustments January. Requires SIMMER_API_KEY and simmer-sdk.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: Kalshi CPI Seasonal Trader
  difficulty: advanced
  homepage: "https://simmer.markets/skills"
  repository: "https://github.com/SpartanLabsXyz/simmer-sdk"
  requires_env: "SIMMER_API_KEY"
  requires_pip: "simmer-sdk"
  default_mode: "paper"
  live_flag: "--live"
---

# Kalshi CPI Seasonal Trader

> **This is a template.**
> The default signal uses static seasonal adjustment factors for CPI bins -- remix it with real-time BLS data feeds, energy futures curves, or housing indices for live seasonal calibration.
> The skill handles all the plumbing (market discovery, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

CPI has well-documented seasonal patterns that retail traders ignore. Energy costs spike in summer (June peak), housing OER resets in January, and holiday demand lifts December. This skill biases CPI bin probabilities based on the current month's historical seasonal adjustment, then trades when Kalshi market prices diverge from the seasonally-adjusted fair value.

Key advantages:
- **Seasonal patterns are persistent** -- decades of BLS data confirm monthly CPI biases
- **Energy dominance** -- summer energy spikes are the strongest and most predictable signal
- **January housing reset** -- OER annual adjustment creates a reliable January hot-print bias
- **Bin structure exploitable** -- Kalshi CPI bins create discrete mispricings when seasonal effects shift probability mass

## Signal Logic

### Seasonal Adjustment Model

1. Look up current month's seasonal adjustment factor (+/- percentage points)
2. Classify each CPI market into a bin category (low, low_mid, mid, high_mid, high)
3. Shift probability mass: positive adj -> higher bins more likely, negative -> lower bins
4. Compare adjusted fair value to Kalshi market price
5. Trade when |fair_value - market| >= entry_edge

### Monthly Adjustments

| Month | Adj | Reason |
|-------|-----|--------|
| Jan | +0.10 | Housing OER annual reset |
| Feb | -0.05 | Post-holiday normalization |
| Mar | 0.00 | Neutral transition |
| Apr | +0.05 | Spring demand, gasoline blend switch |
| May | +0.05 | Summer driving begins |
| Jun | +0.10 | Peak summer energy |
| Jul | +0.05 | Continued summer, moderating |
| Aug | 0.00 | Back-to-school offsets energy |
| Sep | -0.05 | Summer demand fade |
| Oct | -0.05 | Autumn deflation |
| Nov | 0.00 | Pre-holiday neutral |
| Dec | +0.05 | Holiday demand |

### Conviction-Based Sizing

- `conviction = min(|edge| / entry_edge, 2.0) / 2.0`
- `size = max($1.00, conviction * MAX_POSITION_USD)`
- Larger edge = larger position, capped at MAX_POSITION_USD

## Risk Parameters

| Parameter | Default | Notes |
|-----------|---------|-------|
| Entry edge | 8% | Min fair-vs-market divergence to trade |
| Exit threshold | 45% | Sell when position price reaches this |
| Max position size | $5.00 USDC | Per market |
| Max trades per run | 3 | Rate limiting |
| Max slippage | 15% | Skip if slippage exceeds |
| Min liquidity | $0 | Disabled by default |

## Installation & Setup

```bash
clawhub install kalshi-econ-seasonal-trader
```

Requires: `SIMMER_API_KEY` and `SOLANA_PRIVATE_KEY` environment variables.

## Cron Schedule

Cron is set to `null` -- the skill does not run on a schedule until you configure it in the Simmer UI.

## Safety & Execution Mode

**The skill defaults to dry-run mode. Real trades only execute when `--live` is passed explicitly.**

| Scenario | Mode | Financial risk |
|----------|------|----------------|
| `python trader.py` | Dry run | None |
| Cron / automaton | Dry run | None |
| `python trader.py --live` | Live (Kalshi via DFlow) | Real USDC |

## Required Credentials

| Variable | Required | Notes |
|----------|----------|-------|
| `SIMMER_API_KEY` | Yes | Trading authority. Treat as a high-value credential. |
| `SOLANA_PRIVATE_KEY` | Yes | Base58-encoded Solana private key for live trading. |

## Tunables (Risk Parameters)

| Variable | Default | Purpose |
|----------|---------|---------|
| `SIMMER_ECON_SEAS_ENTRY_EDGE` | `0.08` | Min divergence to trigger trade |
| `SIMMER_ECON_SEAS_EXIT_THRESHOLD` | `0.45` | Sell position when price reaches this level |
| `SIMMER_ECON_SEAS_MAX_POSITION_USD` | `5.00` | Max USDC per trade |
| `SIMMER_ECON_SEAS_MAX_TRADES_PER_RUN` | `3` | Max trades per execution cycle |
| `SIMMER_ECON_SEAS_SLIPPAGE_MAX` | `0.15` | Max slippage before skipping trade |
| `SIMMER_ECON_SEAS_MIN_LIQUIDITY` | `0` | Min market liquidity USD (0 = disabled) |

## Dependency

`simmer-sdk` is published on PyPI by Simmer Markets.
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
- Publisher: hello@simmer.markets
