---
name: kalshi-eth-bin-distribution-trader
description: Trades ETH price bin markets on Kalshi by exploiting the constraint that all bins must sum to 100%. When the sum deviates, identifies mispriced bins and trades toward rebalance. Requires SIMMER_API_KEY and simmer-sdk.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: Kalshi ETH Bin Distribution Trader
  difficulty: advanced
  homepage: "https://simmer.markets/skills"
  repository: "https://github.com/SpartanLabsXyz/simmer-sdk"
  requires_env: "SIMMER_API_KEY"
  requires_pip: "simmer-sdk"
  default_mode: "paper"
  live_flag: "--live"
---

# Kalshi ETH Bin Distribution Trader

> **This is a template.**
> The default signal uses the 100% sum constraint on price bins -- remix it with implied distribution fitting, volatility smile analysis, or cross-venue arbitrage.
> The skill handles all the plumbing (market discovery, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

Kalshi ETH price markets are structured as mutually exclusive bins (e.g., "ETH above $3000", "ETH $2500-$3000") that must sum to exactly 100%. When retail flow pushes individual bins out of alignment, the sum deviates from 100% and creates structural arbitrage.

Key advantages:
- **Mathematical certainty** -- bins MUST sum to 100%, deviations are temporary
- **No external data needed** -- pure internal consistency check
- **Self-correcting** -- market makers eventually re-align bins

## Signal Logic

### Sum Constraint Model

1. Fetch all active ETH price bin markets from Kalshi
2. Group bins by resolution date (weekly, monthly)
3. Sum probabilities across all bins in each group
4. If sum deviates > `sum_tolerance` from 100%, flag the group
5. Normalize each bin: `fair = current / total_sum`
6. Trade bins where `|fair - market| >= entry_edge`

### Example (with defaults)

| Bin | Market P | Fair P (normalized) | Edge | Action |
|-----|----------|-------------------|------|--------|
| ETH $2000-$2500 | 25% | 23.1% | -1.9% | Hold |
| ETH $2500-$3000 | 35% | 32.4% | -2.6% | Hold |
| ETH $3000-$3500 | 30% | 27.8% | -2.2% | Hold |
| ETH above $3500 | 18% | 16.7% | -1.3% | Hold |
| **Sum** | **108%** | **100%** | | Overpriced |

### Conviction-Based Sizing

- `conviction = min(|edge| / entry_edge, 2.0) / 2.0`
- `size = max($5.00, conviction * MAX_POSITION_USD)`
- Larger edge = larger position, capped at MAX_POSITION_USD

### Remix Ideas

- **Implied volatility fitting**: Fit a lognormal distribution to bin prices
- **Cross-venue arb**: Compare Kalshi bin structure to Polymarket/Betfair
- **Historical mean reversion**: Track how fast bin sums revert to 100%
- **Options-implied distribution**: Use ETH options chain for fair bin prices

## Risk Parameters

| Parameter | Default | Notes |
|-----------|---------|-------|
| Entry edge | 8% | Min per-bin edge to trade |
| Exit threshold | 45% | Sell when position price reaches this |
| Max position size | $5.00 USDC | Per market |
| Max trades per run | 3 | Rate limiting |
| Sum tolerance | 5% | Min sum deviation to trigger analysis |
| Max slippage | 15% | Skip if slippage exceeds |
| Min liquidity | $0 | Disabled by default |

## Installation & Setup

```bash
clawhub install kalshi-eth-bin-distribution-trader
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
| `SIMMER_API_KEY` | Yes | Trading authority -- keep this credential private. |
| `SOLANA_PRIVATE_KEY` | For live | Base58-encoded Solana private key for DFlow transactions. |

## Tunables (Risk Parameters)

All risk parameters are declared in `clawhub.json` as `tunables` and adjustable from the Simmer UI without code changes.

| Variable | Default | Purpose |
|----------|---------|---------|
| `SIMMER_ETH_BINDIST_ENTRY_EDGE` | `0.08` | Min per-bin edge to trigger trade |
| `SIMMER_ETH_BINDIST_EXIT_THRESHOLD` | `0.45` | Sell position when price reaches this level |
| `SIMMER_ETH_BINDIST_MAX_POSITION_USD` | `5.00` | Max USDC per trade |
| `SIMMER_ETH_BINDIST_MAX_TRADES_PER_RUN` | `3` | Max trades per execution cycle |
| `SIMMER_ETH_BINDIST_SLIPPAGE_MAX` | `0.15` | Max slippage before skipping (15%) |
| `SIMMER_ETH_BINDIST_MIN_LIQUIDITY` | `0` | Min market liquidity USD (0 = disabled) |
| `SIMMER_ETH_BINDIST_SUM_TOLERANCE` | `0.05` | Min bin sum deviation to trigger analysis |

## Dependency

`simmer-sdk` is published on PyPI by Simmer Markets.
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
- Publisher: hello@simmer.markets

Review the source before providing live credentials if you require full auditability.
