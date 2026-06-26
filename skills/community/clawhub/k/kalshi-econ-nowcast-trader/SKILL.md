---
name: kalshi-econ-nowcast-trader
description: Trades CPI bin markets on Kalshi using the Cleveland Fed CPI Nowcast to compute fair bin probabilities via a normal distribution model. Requires SIMMER_API_KEY and simmer-sdk. Use when you want to capture alpha from nowcast-vs-market divergence on CPI outcomes.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: Kalshi Economic Nowcast Trader
  difficulty: advanced
  homepage: "https://simmer.markets/skills"
  repository: "https://github.com/SpartanLabsXyz/simmer-sdk"
  requires_env: "SIMMER_API_KEY"
  requires_pip: "simmer-sdk"
  default_mode: "paper"
  live_flag: "--live"
---

# Kalshi Economic Nowcast Trader

> **This is a template.**  
> The default signal uses the Cleveland Fed CPI Nowcast point estimate and standard deviation to price CPI bins -- remix it with real-time nowcast scraping, multiple nowcast sources, or Bayesian updating as data arrives.  
> The skill handles all the plumbing (market discovery, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

Kalshi lists CPI bin markets ("Will CPI be between 0.2% and 0.3%?"). This skill prices each bin using the Cleveland Fed's CPI Nowcast as the mean of a normal distribution, then trades when the market price diverges from the model probability.

Key advantages:
- **Cleveland Fed Nowcast is free and public** -- updated regularly with high accuracy
- **Normal distribution is well-calibrated** for CPI -- historically fits actual outcomes
- **Multiple bins per release** -- diversified signal across the distribution

## Signal Logic

### Nowcast-to-Bin Model

1. Load Cleveland Fed CPI Nowcast estimate and standard deviation
2. Compute P(CPI in [low, high]) = Phi(z_high) - Phi(z_low) for each bin
3. Compare model probability to Kalshi market price
4. Trade when `|model - market| >= entry_edge`

### Example (with defaults: estimate=0.3%, stddev=0.15%)

| Bin | Model P | Market P | Edge | Action |
|-----|---------|----------|------|--------|
| 0.1%-0.2% | 9.2% | 15% | -5.8% | Hold |
| 0.2%-0.3% | 34.1% | 20% | +14.1% | BUY YES |
| 0.4%-0.5% | 9.2% | 22% | -12.8% | BUY NO |

### Remix Ideas

- **Live nowcast scraper**: Auto-refresh from Cleveland Fed website
- **Multi-source ensemble**: Average Cleveland Fed, NY Fed, and Atlanta Fed nowcasts
- **Bayesian updates**: Incorporate PPI, import prices, and other leading indicators
- **Volatility scaling**: Widen stddev near data release dates

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
clawhub install kalshi-econ-nowcast-trader
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
| `SIMMER_ECON_NOW_ENTRY_EDGE` | `0.10` | Min divergence between nowcast model and market to trigger trade |
| `SIMMER_ECON_NOW_EXIT_THRESHOLD` | `0.45` | Sell position when price reaches this level |
| `SIMMER_ECON_NOW_MAX_POSITION_USD` | `5.00` | Max USDC per trade |
| `SIMMER_ECON_NOW_MAX_TRADES_PER_RUN` | `3` | Max trades per execution cycle |
| `SIMMER_ECON_NOW_SLIPPAGE_MAX` | `0.15` | Max slippage before skipping (0.15 = 15%) |
| `SIMMER_ECON_NOW_MIN_LIQUIDITY` | `0` | Min market liquidity USD (0 = disabled) |

## Dependency

`simmer-sdk` is published on PyPI by Simmer Markets.
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
- Publisher: hello@simmer.markets

Review the source before providing live credentials if you require full auditability.
