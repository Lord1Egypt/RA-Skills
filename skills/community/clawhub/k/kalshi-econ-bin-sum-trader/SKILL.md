---
name: kalshi-econ-bin-sum-trader
description: Trades CPI range bin markets on Kalshi using the constraint that mutually exclusive bins must sum to ~100%. Normalizes and trades the most mispriced bin when deviation exceeds tolerance. Requires SIMMER_API_KEY and simmer-sdk.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: Kalshi Econ Bin Sum Trader
  difficulty: intermediate
  homepage: "https://simmer.markets/skills"
  repository: "https://github.com/SpartanLabsXyz/simmer-sdk"
  requires_env: "SIMMER_API_KEY"
  requires_pip: "simmer-sdk"
  default_mode: "paper"
  live_flag: "--live"
---

# Kalshi Econ Bin Sum Trader

> **This is a template.**  
> The default signal uses the fundamental constraint that mutually exclusive outcome bins must sum to 100% -- remix it with Bayesian priors, consensus forecasts, or cross-event correlation models.  
> The skill handles all the plumbing (market discovery, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

CPI range bin markets on Kalshi price each outcome bin independently. Since exactly one bin must resolve YES, the probabilities must sum to 100%. When the market sum deviates beyond tolerance, at least one bin is mispriced. This skill normalizes the distribution and trades the most mispriced bin.

Key advantages:
- **Mathematical certainty** -- bins MUST sum to 100%, any deviation is a guaranteed mispricing
- **No forecasting needed** -- the strategy is model-free, relying purely on arbitrage math
- **Self-correcting** -- as the sum approaches 100%, signals disappear (no stale trades)
- **Works across any bin-style market** -- CPI, GDP, unemployment, any mutually exclusive set

## Signal Logic

### Bin Sum Normalization

1. Group CPI bin markets by event (e.g., "March 2026 CPI")
2. Sum all bin prices in the group
3. If `|sum - 1.0| > sum_tolerance`, normalize: `fair_prob = price / sum`
4. Compute edge per bin: `edge = fair_prob - market_price`
5. Trade the bin with the largest absolute edge

### Example

| Bin | Market Price | Fair (normalized) | Edge | Action |
|-----|-------------|-------------------|------|--------|
| CPI < 2.0% | 5% | 4.8% | -0.2% | Hold |
| CPI 2.0-2.5% | 25% | 23.8% | -1.2% | Hold |
| CPI 2.5-3.0% | 35% | 33.3% | -1.7% | BUY NO |
| CPI 3.0-3.5% | 30% | 28.6% | -1.4% | Hold |
| CPI > 3.5% | 10% | 9.5% | -0.5% | Hold |
| **Sum** | **105%** | **100%** | | |

### Conviction-Based Sizing

- `conviction = min(|edge| / deviation, 2.0) / 2.0`
- `size = max($1.00, conviction * MAX_POSITION_USD)`
- Larger edge relative to total deviation = larger position

### Remix Ideas

- **Cross-event sum**: Apply same logic to GDP, unemployment, or Fed rate bins
- **Consensus prior**: Weight normalization toward consensus CPI forecasts
- **Multi-bin arbitrage**: Trade multiple bins simultaneously for hedged positions
- **Rolling rebalance**: Re-run as market moves to capture dynamic mispricing

## Risk Parameters

| Parameter | Default | Notes |
|-----------|---------|-------|
| Sum tolerance | 5% | Min deviation from 100% before trading |
| Exit threshold | 45% | Sell when position price reaches this |
| Max position size | $5.00 USDC | Per market |
| Max trades per run | 3 | Rate limiting |
| Max slippage | 15% | Skip if slippage exceeds |
| Min liquidity | $0 | Disabled by default |

## Installation & Setup

```bash
clawhub install kalshi-econ-bin-sum-trader
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

The automaton cron is set to `null` -- it does not run on a schedule until you configure it in the Simmer UI. `autostart: false` means it won't start automatically on install.

## Required Credentials

| Variable | Required | Notes |
|----------|----------|-------|
| `SIMMER_API_KEY` | Yes | Trading authority. Treat as a high-value credential. |
| `SOLANA_PRIVATE_KEY` | Yes | Base58-encoded Solana private key for live trading. |

## Tunables (Risk Parameters)

All risk parameters are declared in `clawhub.json` as `tunables` and adjustable from the Simmer UI without code changes.

| Variable | Default | Purpose |
|----------|---------|---------|
| `SIMMER_ECON_BINSUM_SUM_TOLERANCE` | `0.05` | Min deviation from 100% sum before trading |
| `SIMMER_ECON_BINSUM_EXIT_THRESHOLD` | `0.45` | Sell position when price reaches this level |
| `SIMMER_ECON_BINSUM_MAX_POSITION_USD` | `5.00` | Max USDC per trade |
| `SIMMER_ECON_BINSUM_MAX_TRADES_PER_RUN` | `3` | Max trades per execution cycle |
| `SIMMER_ECON_BINSUM_SLIPPAGE_MAX` | `0.15` | Max slippage before skipping (0.15 = 15%) |
| `SIMMER_ECON_BINSUM_MIN_LIQUIDITY` | `0` | Min market liquidity USD (0 = disabled) |

## Dependency

`simmer-sdk` is published on PyPI by Simmer Markets.
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
- Publisher: hello@simmer.markets

Review the source before providing live credentials if you require full auditability.
