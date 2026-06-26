---
name: kalshi-f1-race-momentum-trader
description: Trades F1 Drivers Championship markets on Kalshi using recent race results weighted by recency. Hot streaks boost championship probability, cold streaks reduce it. Requires SIMMER_API_KEY and simmer-sdk.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: Kalshi F1 Race Momentum Trader
  difficulty: advanced
  homepage: "https://simmer.markets/skills"
  repository: "https://github.com/SpartanLabsXyz/simmer-sdk"
  requires_env: "SIMMER_API_KEY"
  requires_pip: "simmer-sdk"
  default_mode: "paper"
  live_flag: "--live"
---

# Kalshi F1 Race Momentum Trader

> **This is a template.**
> The default signal uses static recent results -- remix it with live F1 API data for automatic momentum recalculation after each race weekend.
> The skill handles all the plumbing (market discovery, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

Recent form matters in F1. A driver on a hot streak (wins, podiums in the last 3 races) has demonstrably higher championship probability than their season-long average suggests. Markets are slow to fully price in momentum shifts -- they anchor to pre-season expectations and lag behind recent performance changes.

Key advantages:
- **Recency bias is real and quantifiable** -- last 3 races predict next-race performance better than season average
- **Markets anchor to narratives** -- "Verstappen always wins" persists even during cold streaks
- **Weighted recency** -- most recent race gets 3x weight, capturing acceleration/deceleration in form
- **Hot/cold classification** -- simple trend labels (HOT/COLD/FLAT) identify tradeable regimes

## Signal Logic

### Momentum Model

1. Collect last 3 race results per driver (position finished)
2. Convert positions to performance scores: P1=1.0, P20=0.0
3. Apply recency weights: [3x, 2x, 1x] for [most recent, second, third]
4. Compute momentum score: normalized to [-1.0, +1.0]
5. Adjust base probability: `adjusted = base + momentum * SCALE * base`
6. Compare adjusted probability to Kalshi market price
7. Trade when |adjusted - market| >= entry_edge

### Momentum Categories

| Momentum Score | Category | Meaning |
|---------------|----------|---------|
| > +0.3 | HOT | Driver outperforming, probability should be higher |
| -0.3 to +0.3 | FLAT | Stable form, no momentum edge |
| < -0.3 | COLD | Driver underperforming, probability should be lower |

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
| Max trades per run | 5 | Rate limiting |
| Max slippage | 15% | Skip if slippage exceeds |
| Min liquidity | $0 | Disabled by default |

## Installation & Setup

```bash
clawhub install kalshi-f1-race-momentum-trader
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
| `SIMMER_F1_RACEMOM_ENTRY_EDGE` | `0.10` | Min divergence to trigger trade |
| `SIMMER_F1_RACEMOM_EXIT_THRESHOLD` | `0.45` | Sell position when price reaches this level |
| `SIMMER_F1_RACEMOM_MAX_POSITION_USD` | `5.00` | Max USDC per trade |
| `SIMMER_F1_RACEMOM_MAX_TRADES_PER_RUN` | `5` | Max trades per execution cycle |
| `SIMMER_F1_RACEMOM_SLIPPAGE_MAX` | `0.15` | Max slippage before skipping trade |
| `SIMMER_F1_RACEMOM_MIN_LIQUIDITY` | `0` | Min market liquidity USD (0 = disabled) |

## Dependency

`simmer-sdk` is published on PyPI by Simmer Markets.
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
- Publisher: hello@simmer.markets
