---
name: kalshi-f1-teammate-anti-trader
description: Trades F1 Drivers Championship markets on Kalshi using teammate anti-correlation. Teammates share the same car so their probabilities are structurally linked -- when one rises, the other should fall. Requires SIMMER_API_KEY and simmer-sdk.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: Kalshi F1 Teammate Anti-Correlation Trader
  difficulty: advanced
  homepage: "https://simmer.markets/skills"
  repository: "https://github.com/SpartanLabsXyz/simmer-sdk"
  requires_env: "SIMMER_API_KEY"
  requires_pip: "simmer-sdk"
  default_mode: "paper"
  live_flag: "--live"
---

# Kalshi F1 Teammate Anti-Correlation Trader

> **This is a template.**
> The default signal uses static dominance ratios -- remix it with live head-to-head qualifying/race data for dynamic dominance estimation.
> The skill handles all the plumbing (market discovery, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

F1 teammates share the same car, meaning their championship probabilities are structurally anti-correlated. If Verstappen's probability rises, Lawson's should fall (they share Red Bull's probability budget). Markets are slow to adjust both sides of teammate pairs simultaneously, creating exploitable relative mispricings.

Key advantages:
- **Structural constraint** -- teammate probabilities must sum to roughly the team's total share
- **Dominance ratios are stable** -- intra-team hierarchy rarely changes mid-season
- **Markets adjust asymmetrically** -- one driver's price moves but teammate's lags
- **Pairs trading** -- natural hedge structure reduces directional risk

## Signal Logic

### Teammate Anti-Correlation Model

1. Define teammate pairs (same constructor)
2. Set dominance ratios (who captures what % of team total)
3. For each pair, sum their market prices = team_total
4. Compute fair split: `fair_A = team_total * dominance`, `fair_B = team_total * (1-dominance)`
5. Trade when |fair - market| >= entry_edge for either driver

### Teammate Pairs (2025)

| Pair | Constructor | Dominance | Team Total |
|------|-------------|-----------|------------|
| Verstappen / Lawson | Red Bull | 85%/15% | ~36% |
| Leclerc / Hamilton | Ferrari | 50%/50% | ~20% |
| Russell / Antonelli | Mercedes | 70%/30% | ~8% |
| Piastri / Norris | McLaren | 40%/60% | ~36% |

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
| Max trades per run | 4 | Rate limiting |
| Max slippage | 15% | Skip if slippage exceeds |
| Min liquidity | $0 | Disabled by default |

## Installation & Setup

```bash
clawhub install kalshi-f1-teammate-anti-trader
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
| `SIMMER_F1_TEAM_ENTRY_EDGE` | `0.08` | Min divergence to trigger trade |
| `SIMMER_F1_TEAM_EXIT_THRESHOLD` | `0.45` | Sell position when price reaches this level |
| `SIMMER_F1_TEAM_MAX_POSITION_USD` | `5.00` | Max USDC per trade |
| `SIMMER_F1_TEAM_MAX_TRADES_PER_RUN` | `4` | Max trades per execution cycle |
| `SIMMER_F1_TEAM_SLIPPAGE_MAX` | `0.15` | Max slippage before skipping trade |
| `SIMMER_F1_TEAM_MIN_LIQUIDITY` | `0` | Min market liquidity USD (0 = disabled) |

## Dependency

`simmer-sdk` is published on PyPI by Simmer Markets.
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
- Publisher: hello@simmer.markets
