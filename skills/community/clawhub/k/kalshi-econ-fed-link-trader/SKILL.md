---
name: kalshi-econ-fed-link-trader
description: Cross-market strategy that uses CPI bin prices to estimate CPI level, then adjusts Fed rate market positions via a sensitivity model. High CPI means Fed less likely to cut. Requires SIMMER_API_KEY and simmer-sdk.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: Kalshi Econ Fed Link Trader
  difficulty: advanced
  homepage: "https://simmer.markets/skills"
  repository: "https://github.com/SpartanLabsXyz/simmer-sdk"
  requires_env: "SIMMER_API_KEY"
  requires_pip: "simmer-sdk"
  default_mode: "paper"
  live_flag: "--live"
---

# Kalshi Econ Fed Link Trader

> **This is a template.**  
> The default signal uses a static CPI-to-Fed sensitivity table -- remix it with live CME FedWatch data, yield curve signals, or Taylor Rule models.  
> The skill handles all the plumbing (market discovery, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

CPI data and Fed rate decisions are deeply linked. This skill reads CPI bin market prices to estimate the current CPI level, then uses a DATA_SENSITIVITY table to compute fair probabilities for Fed rate cut/hold/hike markets. When the Fed market price diverges from the model, trade the edge.

Key advantages:
- **Cross-market signal** -- uses information from one market type to trade another
- **Fundamental economic linkage** -- CPI-to-Fed is the most documented macro relationship
- **DATA_SENSITIVITY table** -- calibrated from historical Fed reaction function
- **No external data needed** -- all inputs come from Kalshi market prices

## Signal Logic

### CPI-to-Fed Linkage Model

1. Scan CPI bin markets and extract probability-weighted expected CPI level
2. Look up model Fed probabilities from DATA_SENSITIVITY table
3. Interpolate between table entries for precise CPI levels
4. Compare model probability to Fed market price
5. Trade when `|model - market| >= entry_edge`

### DATA_SENSITIVITY Table

| CPI Level | P(Cut) | P(Hold) | P(Hike) |
|-----------|--------|---------|---------|
| 1.0% | 85% | 12% | 3% |
| 2.0% | 55% | 38% | 7% |
| 2.5% | 20% | 65% | 15% |
| 3.0% | 5% | 55% | 40% |
| 4.0% | 1% | 24% | 75% |
| 5.0% | 0% | 10% | 90% |

### Conviction-Based Sizing

- `conviction = min(|edge| / entry_edge, 2.0) / 2.0`
- `size = max($1.00, conviction * MAX_POSITION_USD)`
- Larger edge = larger position, capped at MAX_POSITION_USD

### Remix Ideas

- **CME FedWatch**: Compare model to CME futures-implied Fed probabilities
- **Yield curve signal**: Add 2y-10y spread as additional Fed predictor
- **Taylor Rule**: Replace sensitivity table with formal Taylor Rule computation
- **Real-time CPI nowcast**: Use Cleveland Fed nowcast instead of bin prices

## Risk Parameters

| Parameter | Default | Notes |
|-----------|---------|-------|
| Entry edge | 10% | Min model-vs-market divergence to trade |
| Exit threshold | 45% | Sell when position price reaches this |
| Max position size | $5.00 USDC | Per market |
| Max trades per run | 3 | Rate limiting |
| Max slippage | 15% | Skip if slippage exceeds |
| Min liquidity | $0 | Disabled by default |

## Installation & Setup

```bash
clawhub install kalshi-econ-fed-link-trader
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
| `SIMMER_ECON_FEDLINK_ENTRY_EDGE` | `0.10` | Min divergence between model and market to trigger trade |
| `SIMMER_ECON_FEDLINK_EXIT_THRESHOLD` | `0.45` | Sell position when price reaches this level |
| `SIMMER_ECON_FEDLINK_MAX_POSITION_USD` | `5.00` | Max USDC per trade |
| `SIMMER_ECON_FEDLINK_MAX_TRADES_PER_RUN` | `3` | Max trades per execution cycle |
| `SIMMER_ECON_FEDLINK_SLIPPAGE_MAX` | `0.15` | Max slippage before skipping (0.15 = 15%) |
| `SIMMER_ECON_FEDLINK_MIN_LIQUIDITY` | `0` | Min market liquidity USD (0 = disabled) |

## Dependency

`simmer-sdk` is published on PyPI by Simmer Markets.
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
- Publisher: hello@simmer.markets

Review the source before providing live credentials if you require full auditability.
