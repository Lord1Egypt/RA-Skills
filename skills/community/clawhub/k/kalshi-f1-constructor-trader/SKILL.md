---
name: kalshi-f1-constructor-trader
description: Trades F1 Drivers Championship markets on Kalshi using constructor (team) car performance ratings. Drivers in faster cars have structurally higher championship probabilities. Requires SIMMER_API_KEY and simmer-sdk.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: Kalshi F1 Constructor Trader
  difficulty: advanced
  homepage: "https://simmer.markets/skills"
  repository: "https://github.com/SpartanLabsXyz/simmer-sdk"
  requires_env: "SIMMER_API_KEY"
  requires_pip: "simmer-sdk"
  default_mode: "paper"
  live_flag: "--live"
---

# Kalshi F1 Constructor Trader

> **This is a template.**
> The default signal uses static constructor ratings and driver skill modifiers -- remix it with live qualifying data, FP session lap times, or car development trajectory analysis.
> The skill handles all the plumbing (market discovery, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

Constructor (team) car speed is the single strongest predictor of F1 championship outcomes. A driver in the fastest car wins the championship ~70% of the time historically. This skill rates each constructor's car performance, applies individual driver skill modifiers, and computes fair championship probabilities using a power-law model.

Key advantages:
- **Car > driver** -- constructor advantage explains most championship variance
- **Stable signal** -- car performance changes slowly (major upgrades every 3-5 races)
- **Markets overweight narratives** -- retail traders overreact to single race results while ignoring underlying car pace
- **Power-law compounding** -- small car advantages compound over a 24-race season

## Signal Logic

### Constructor Model

1. Rate each constructor's car performance (0-100 scale)
2. Apply individual driver skill modifiers (teammate comparison)
3. Compute effective driver rating = constructor_base + skill_modifier
4. Convert to probabilities: P(win) proportional to rating^3 (power law)
5. Compare model probability to Kalshi market price
6. Trade when |model - market| >= entry_edge

### Constructor Ratings (2025)

| Constructor | Rating | Notes |
|-------------|--------|-------|
| Red Bull | 95 | Top pace, dominant qualifying |
| McLaren | 92 | Strong race pace, consistent |
| Ferrari | 90 | Great qualifier, variable race pace |
| Mercedes | 88 | Improving development trajectory |
| Aston Martin | 82 | Best of the rest |

### Conviction-Based Sizing

- `conviction = min(|edge| / entry_edge, 2.0) / 2.0`
- `size = max($1.00, conviction * MAX_POSITION_USD)`
- Larger edge = larger position, capped at MAX_POSITION_USD

## Risk Parameters

| Parameter | Default | Notes |
|-----------|---------|-------|
| Entry edge | 10% | Min model-vs-market divergence to trade |
| Exit threshold | 45% | Sell when position price reaches this |
| Max position size | $5.00 USDC | Per market |
| Max trades per run | 4 | Rate limiting |
| Max slippage | 15% | Skip if slippage exceeds |
| Min liquidity | $0 | Disabled by default |

## Installation & Setup

```bash
clawhub install kalshi-f1-constructor-trader
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
| `SIMMER_F1_CONSTR_ENTRY_EDGE` | `0.10` | Min divergence to trigger trade |
| `SIMMER_F1_CONSTR_EXIT_THRESHOLD` | `0.45` | Sell position when price reaches this level |
| `SIMMER_F1_CONSTR_MAX_POSITION_USD` | `5.00` | Max USDC per trade |
| `SIMMER_F1_CONSTR_MAX_TRADES_PER_RUN` | `4` | Max trades per execution cycle |
| `SIMMER_F1_CONSTR_SLIPPAGE_MAX` | `0.15` | Max slippage before skipping trade |
| `SIMMER_F1_CONSTR_MIN_LIQUIDITY` | `0` | Min market liquidity USD (0 = disabled) |

## Dependency

`simmer-sdk` is published on PyPI by Simmer Markets.
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
- Publisher: hello@simmer.markets
