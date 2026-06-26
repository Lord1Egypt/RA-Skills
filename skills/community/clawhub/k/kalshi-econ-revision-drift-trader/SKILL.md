---
name: kalshi-econ-revision-drift-trader
description: Trades CPI bin markets on Kalshi accounting for systematic upward revision bias (~0.03 pp) in initial CPI releases. Markets pricing off initial releases underprice higher CPI bins. Requires SIMMER_API_KEY and simmer-sdk.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: Kalshi Econ Revision Drift Trader
  difficulty: advanced
  homepage: "https://simmer.markets/skills"
  repository: "https://github.com/SpartanLabsXyz/simmer-sdk"
  requires_env: "SIMMER_API_KEY"
  requires_pip: "simmer-sdk"
  default_mode: "paper"
  live_flag: "--live"
---

# Kalshi Econ Revision Drift Trader

> **This is a template.**  
> The default signal uses the well-documented CPI revision bias (+0.03 pp) to shift the fair probability distribution -- remix it with seasonal adjustment patterns, BLS methodology changes, or real-time nowcast data.  
> The skill handles all the plumbing (market discovery, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

BLS CPI initial releases are systematically revised upward by approximately 0.03 percentage points. Markets that resolve on the initial release effectively ignore this revision bias, creating a persistent edge. This skill shifts the CPI probability distribution by the revision bias and trades bins where the shift creates meaningful mispricing.

Key advantages:
- **Documented statistical bias** -- BLS revision history from 2000-2024 confirms the upward drift
- **Structural edge** -- as long as markets price off initial releases, the bias persists
- **Directional prediction** -- higher CPI bins are systematically underpriced
- **No timing dependency** -- the bias exists regardless of the current CPI level

## Signal Logic

### Revision Drift Model

1. Parse CPI bin markets and extract probability-weighted expected CPI mean
2. Compute "initial release" bin probabilities using normal distribution
3. Compute "revision-adjusted" bin probabilities by shifting mean +0.03 pp
4. Edge = `revised_prob - market_price` for each bin
5. Trade when `|edge| >= entry_edge`

### Revision Statistics

| Metric | Value | Source |
|--------|-------|--------|
| Mean revision | +0.03 pp | BLS CPI revision history 2000-2024 |
| Revision std | 0.05 pp | Same dataset |
| Direction | Upward | Consistent across decades |
| Impact | Higher bins underpriced | Shifts CDF right |

### Example

If CPI market-implied mean is 2.80%:

| Bin | Initial Prob | Revised Prob | Revision Edge |
|-----|-------------|-------------|---------------|
| < 2.0% | 5.5% | 4.9% | -0.6% |
| 2.0-2.5% | 22.7% | 21.5% | -1.2% |
| 2.5-3.0% | 38.3% | 38.2% | -0.1% |
| 3.0-3.5% | 24.6% | 25.8% | +1.2% |
| > 3.5% | 8.9% | 9.6% | +0.7% |

### Conviction-Based Sizing

- `conviction = min(|edge| / entry_edge, 2.0) / 2.0`
- `size = max($1.00, conviction * MAX_POSITION_USD)`
- Larger edge = larger position, capped at MAX_POSITION_USD

### Remix Ideas

- **Seasonal adjustment**: CPI revisions vary by month (e.g., January effect)
- **BLS methodology tracking**: New CPI basket weights change revision patterns
- **Nowcast overlay**: Combine revision bias with Cleveland Fed CPI nowcast
- **Multi-release**: Track preliminary, final, and revised releases separately

## Risk Parameters

| Parameter | Default | Notes |
|-----------|---------|-------|
| Entry edge | 8% | Min revised-vs-market divergence to trade |
| Exit threshold | 45% | Sell when position price reaches this |
| Max position size | $5.00 USDC | Per market |
| Max trades per run | 3 | Rate limiting |
| Max slippage | 15% | Skip if slippage exceeds |
| Min liquidity | $0 | Disabled by default |

## Installation & Setup

```bash
clawhub install kalshi-econ-revision-drift-trader
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
| `SIMMER_ECON_REV_ENTRY_EDGE` | `0.08` | Min divergence between revised fair and market to trigger trade |
| `SIMMER_ECON_REV_EXIT_THRESHOLD` | `0.45` | Sell position when price reaches this level |
| `SIMMER_ECON_REV_MAX_POSITION_USD` | `5.00` | Max USDC per trade |
| `SIMMER_ECON_REV_MAX_TRADES_PER_RUN` | `3` | Max trades per execution cycle |
| `SIMMER_ECON_REV_SLIPPAGE_MAX` | `0.15` | Max slippage before skipping (0.15 = 15%) |
| `SIMMER_ECON_REV_MIN_LIQUIDITY` | `0` | Min market liquidity USD (0 = disabled) |

## Dependency

`simmer-sdk` is published on PyPI by Simmer Markets.
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
- Publisher: hello@simmer.markets

Review the source before providing live credentials if you require full auditability.
