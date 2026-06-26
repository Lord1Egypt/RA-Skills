---
name: kalshi-fed-dot-plot-trader
description: Trades Fed rate markets on Kalshi using FOMC dot plot median implied rate path. Computes fair probability of cut/hike per meeting and trades when market diverges. Requires SIMMER_API_KEY and simmer-sdk.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: Kalshi Fed Dot Plot Trader
  difficulty: advanced
  homepage: "https://simmer.markets/skills"
  repository: "https://github.com/SpartanLabsXyz/simmer-sdk"
  requires_env: "SIMMER_API_KEY"
  requires_pip: "simmer-sdk"
  default_mode: "paper"
  live_flag: "--live"
---

# Kalshi Fed Dot Plot Trader

> **This is a template.**
> The default signal uses a static dot plot to compute fair probabilities -- remix it with live SEP data, Fed funds futures, or OIS-implied rates.
> The skill handles all the plumbing (market discovery, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

The FOMC dot plot median implies a rate path for 2026. This skill computes fair probability of at least one rate cut (or hike) by each meeting date from the implied path, then trades when Kalshi market prices diverge from these fair values.

Key advantages:
- **Dot plot is the Fed's own forecast** -- strongest available signal for rate expectations
- **Updated quarterly** -- each SEP release provides fresh data
- **Mean-reverting** -- market prices tend to converge to dot-plot-implied probabilities between meetings

## Signal Logic

### Dot Plot to Fair Probability

1. Load FOMC dot plot median rate path (updated after each SEP)
2. Compute implied cuts from current rate to each quarterly endpoint
3. Map cut count to probability of "at least one cut" by each meeting
4. Compare fair probability to Kalshi market price
5. Trade when `|fair - market| >= entry_edge`

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
clawhub install kalshi-fed-dot-plot-trader
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
| `SIMMER_FED_DOT_ENTRY_EDGE` | `0.10` | Min divergence to trigger trade |
| `SIMMER_FED_DOT_EXIT_THRESHOLD` | `0.45` | Sell position when price reaches this level |
| `SIMMER_FED_DOT_MAX_POSITION_USD` | `5.00` | Max USDC per trade |
| `SIMMER_FED_DOT_MAX_TRADES_PER_RUN` | `3` | Max trades per execution cycle |
| `SIMMER_FED_DOT_SLIPPAGE_MAX` | `0.15` | Max slippage before skipping trade |
| `SIMMER_FED_DOT_MIN_LIQUIDITY` | `0` | Min market liquidity USD (0 = disabled) |

## Dependency

`simmer-sdk` is published on PyPI by Simmer Markets.
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
- Publisher: hello@simmer.markets

Review the source before providing live credentials if you require full auditability.
