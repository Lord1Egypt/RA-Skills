---
name: kalshi-f1-elimination-trader
description: Trades F1 Drivers Championship markets on Kalshi by identifying mathematically eliminated drivers still priced above zero. Sells NO on eliminated drivers for guaranteed edge. Requires SIMMER_API_KEY and simmer-sdk.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: Kalshi F1 Elimination Trader
  difficulty: intermediate
  homepage: "https://simmer.markets/skills"
  repository: "https://github.com/SpartanLabsXyz/simmer-sdk"
  requires_env: "SIMMER_API_KEY"
  requires_pip: "simmer-sdk"
  default_mode: "paper"
  live_flag: "--live"
---

# Kalshi F1 Elimination Trader

> **This is a template.**
> The default signal uses static championship standings -- remix it with live F1 API data for real-time elimination detection as races complete.
> The skill handles all the plumbing (market discovery, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

As the F1 season progresses, drivers become mathematically eliminated from the championship. A driver is eliminated when their maximum possible points (current + MAX_POINTS_PER_RACE * remaining races) is less than the leader's current total. Yet Kalshi markets often still price eliminated drivers above 0% -- this is free money.

Key advantages:
- **Mathematical certainty** -- elimination is a provable fact, not a prediction
- **Low entry edge** -- even 3% market price on an eliminated driver is pure edge
- **Markets lag reality** -- retail traders forget to update stale positions
- **Zero-risk thesis** -- the only risk is execution/timing, not model error

## Signal Logic

### Elimination Detection

1. Track championship standings (points per driver)
2. Calculate remaining races in the season
3. For each driver: `max_possible = current_points + 26 * remaining_races`
4. Driver is eliminated if `max_possible < leader_points`
5. If eliminated AND market price > entry_edge -> BUY NO

### Points per Race

| Component | Points |
|-----------|--------|
| Win | 25 |
| Fastest lap | 1 |
| **Max per race** | **26** |

### Conviction-Based Sizing

- `conviction = min(market_price / entry_edge, 2.0) / 2.0`
- `size = max($1.00, conviction * MAX_POSITION_USD)`
- Higher market price on eliminated driver = more conviction = larger position

## Risk Parameters

| Parameter | Default | Notes |
|-----------|---------|-------|
| Entry edge | 3% | Min market price on eliminated driver to trade |
| Exit threshold | 45% | Sell when position price reaches this |
| Max position size | $5.00 USDC | Per market |
| Max trades per run | 5 | Rate limiting |
| Max slippage | 15% | Skip if slippage exceeds |
| Min liquidity | $0 | Disabled by default |

## Installation & Setup

```bash
clawhub install kalshi-f1-elimination-trader
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
| `SIMMER_F1_ELIM_ENTRY_EDGE` | `0.03` | Min market price on eliminated driver to trade |
| `SIMMER_F1_ELIM_EXIT_THRESHOLD` | `0.45` | Sell position when price reaches this level |
| `SIMMER_F1_ELIM_MAX_POSITION_USD` | `5.00` | Max USDC per trade |
| `SIMMER_F1_ELIM_MAX_TRADES_PER_RUN` | `5` | Max trades per execution cycle |
| `SIMMER_F1_ELIM_SLIPPAGE_MAX` | `0.15` | Max slippage before skipping trade |
| `SIMMER_F1_ELIM_MIN_LIQUIDITY` | `0` | Min market liquidity USD (0 = disabled) |

## Dependency

`simmer-sdk` is published on PyPI by Simmer Markets.
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
- Publisher: hello@simmer.markets
