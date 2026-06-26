---
name: kalshi-f1-points-model-trader
description: Trades F1 Drivers Championship winner markets on Kalshi using current points standings and Monte Carlo simulation to compute win probabilities. Requires SIMMER_API_KEY and simmer-sdk. Use when you want to capture alpha from points-model mispricing on F1 championship markets.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: Kalshi F1 Points Model Trader
  difficulty: advanced
  homepage: "https://simmer.markets/skills"
  repository: "https://github.com/SpartanLabsXyz/simmer-sdk"
  requires_env: "SIMMER_API_KEY"
  requires_pip: "simmer-sdk"
  default_mode: "paper"
  live_flag: "--live"
---

# Kalshi F1 Points Model Trader

> **This is a template.**  
> The default signal uses static points standings and driver ratings to Monte Carlo simulate the remaining season -- remix it with live F1 API data, qualifying pace analysis, or weather-adjusted race models.  
> The skill handles all the plumbing (market discovery, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

F1 Drivers Championship markets on Kalshi price each driver's chance of winning the title. This skill runs Monte Carlo simulations using current points standings and driver skill ratings to compute fair win probabilities, then trades when the market diverges from the model.

Key advantages:
- **Points standings are public** -- no proprietary data needed
- **Monte Carlo captures non-linear dynamics** -- points gaps, remaining races, and driver variance
- **Driver ratings provide edge** -- market often misprices mid-field drivers

## Signal Logic

### Points-Based Monte Carlo Model

1. Load current F1 Drivers Championship standings
2. Assign driver skill ratings (affects finishing position distribution)
3. Simulate remaining races 10,000 times with weighted random finishes
4. Count championship wins per driver to get win probabilities
5. Compare model probability to Kalshi market price
6. Trade when `|model - market| >= entry_edge`

### Conviction-Based Sizing

- `conviction = min(|edge| / entry_edge, 2.0) / 2.0`
- `size = max($1.00, conviction * MAX_POSITION_USD)`
- Larger edge = larger position, capped at MAX_POSITION_USD

### Remix Ideas

- **Live F1 API**: Replace static standings with real-time Ergast/OpenF1 API
- **Qualifying pace model**: Weight recent qualifying gaps for more accurate finishing distributions
- **Constructor performance**: Factor in car development trajectory
- **Weather/track type**: Adjust driver ratings for rain races or street circuits

## Risk Parameters

| Parameter | Default | Notes |
|-----------|---------|-------|
| Entry edge | 10% | Min model-vs-market divergence to trade |
| Exit threshold | 45% | Sell when position price reaches this |
| Max position size | $5.00 USDC | Per market |
| Max trades per run | 5 | Rate limiting |
| Max slippage | 15% | Skip if slippage exceeds |
| Min liquidity | $0 | Disabled by default |

## Installation & Setup

```bash
clawhub install kalshi-f1-points-model-trader
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
| `SIMMER_F1_PTS_ENTRY_EDGE` | `0.10` | Min divergence between model and market to trigger trade |
| `SIMMER_F1_PTS_EXIT_THRESHOLD` | `0.45` | Sell position when price reaches this level |
| `SIMMER_F1_PTS_MAX_POSITION_USD` | `5.00` | Max USDC per trade |
| `SIMMER_F1_PTS_MAX_TRADES_PER_RUN` | `5` | Max trades per execution cycle |
| `SIMMER_F1_PTS_SLIPPAGE_MAX` | `0.15` | Max slippage before skipping (0.15 = 15%) |
| `SIMMER_F1_PTS_MIN_LIQUIDITY` | `0` | Min market liquidity USD (0 = disabled) |

## Dependency

`simmer-sdk` is published on PyPI by Simmer Markets.
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
- Publisher: hello@simmer.markets

Review the source before providing live credentials if you require full auditability.
