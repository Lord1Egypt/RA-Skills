---
name: kalshi-fed-data-reaction-trader
description: Trades Fed rate markets on Kalshi based on macro data releases (CPI, jobs). Scans CPI bin markets for implied CPI, adjusts rate cut probabilities using data sensitivity model. Requires SIMMER_API_KEY and simmer-sdk.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: Kalshi Fed Data Reaction Trader
  difficulty: advanced
  homepage: "https://simmer.markets/skills"
  repository: "https://github.com/SpartanLabsXyz/simmer-sdk"
  requires_env: "SIMMER_API_KEY"
  requires_pip: "simmer-sdk"
  default_mode: "paper"
  live_flag: "--live"
---

# Kalshi Fed Data Reaction Trader

> **This is a template.**
> The default signal uses static data sensitivity coefficients -- remix it with live BLS data feeds, real-time CPI nowcasts, or Fed funds futures reactions.
> The skill handles all the plumbing (market discovery, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

After CPI/jobs data releases, Fed rate probabilities adjust predictably. This skill scans Kalshi CPI bin markets to compute the market-implied CPI, classifies the data regime (high CPI, low CPI, neutral), and adjusts the fair probability of a rate cut accordingly. When the adjustment creates a gap vs. rate cut market prices, it trades.

Key advantages:
- **Data-driven** -- uses market-implied CPI from Kalshi's own CPI bin markets
- **Predictable reaction function** -- high CPI is hawkish, low CPI is dovish
- **Cross-market information** -- extracts signal from CPI markets to trade rate markets

## Signal Logic

### Data Sensitivity Model

1. Scan CPI bin markets to compute probability-weighted implied CPI
2. Classify regime: high_cpi (>3.5%), low_cpi (<2.5%), or neutral
3. Apply sensitivity shift to baseline cut probability (50%)
4. Compare adjusted fair probability to rate cut market prices
5. Trade when `|fair - market| >= entry_edge`

### Sensitivity Coefficients

| Regime | Cut Probability Shift |
|--------|----------------------|
| High CPI | -15% (hawkish) |
| Low CPI | +10% (dovish) |
| Strong jobs | -10% (hawkish) |
| Weak jobs | +15% (dovish) |

### Conviction-Based Sizing

- `conviction = min(|edge| / entry_edge, 2.0) / 2.0`
- `size = max($1.00, conviction * MAX_POSITION_USD)`
- Larger edge = larger position, capped at MAX_POSITION_USD

## Risk Parameters

| Parameter | Default | Notes |
|-----------|---------|-------|
| Entry edge | 10% | Min fair-vs-market divergence to trade |
| Exit threshold | 45% | Sell when position price reaches this |
| Max position size | $5.00 USDC | Per market |
| Max trades per run | 3 | Rate limiting |
| Max slippage | 15% | Skip if slippage exceeds |
| Min liquidity | $0 | Disabled by default |

## Installation & Setup

```bash
clawhub install kalshi-fed-data-reaction-trader
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
| `SIMMER_FED_DATA_ENTRY_EDGE` | `0.10` | Min divergence to trigger trade |
| `SIMMER_FED_DATA_EXIT_THRESHOLD` | `0.45` | Sell position when price reaches this level |
| `SIMMER_FED_DATA_MAX_POSITION_USD` | `5.00` | Max USDC per trade |
| `SIMMER_FED_DATA_MAX_TRADES_PER_RUN` | `3` | Max trades per execution cycle |
| `SIMMER_FED_DATA_SLIPPAGE_MAX` | `0.15` | Max slippage before skipping trade |
| `SIMMER_FED_DATA_MIN_LIQUIDITY` | `0` | Min market liquidity USD (0 = disabled) |

## Dependency

`simmer-sdk` is published on PyPI by Simmer Markets.
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
- Publisher: hello@simmer.markets

Review the source before providing live credentials if you require full auditability.
