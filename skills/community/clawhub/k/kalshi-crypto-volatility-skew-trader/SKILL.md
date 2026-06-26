---
name: kalshi-crypto-volatility-skew-trader
description: Trades Bitcoin price bin markets on Kalshi by comparing market-implied volatility to BTC historical ~60% annualized vol using a lognormal model. Requires SIMMER_API_KEY and simmer-sdk. Use when you want to capture alpha from volatility skew mispricing.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: Kalshi Crypto Volatility Skew Trader
  difficulty: advanced
  homepage: "https://simmer.markets/skills"
  repository: "https://github.com/SpartanLabsXyz/simmer-sdk"
  requires_env: "SIMMER_API_KEY"
  requires_pip: "simmer-sdk"
  default_mode: "paper"
  live_flag: "--live"
---

# Kalshi Crypto Volatility Skew Trader

> **This is a template.**  
> The default signal uses BTC historical annualized vol (~60%) to compute fair bin probabilities via lognormal model -- remix it with options-implied vol surface, realized vol regimes, or GARCH models.  
> The skill handles all the plumbing (market discovery, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

Bitcoin price bin markets on Kalshi imply a probability distribution over future BTC prices. This skill compares that implied distribution to a lognormal model calibrated on BTC's historical ~60% annualized volatility. When the market implies a different vol, the bins are mispriced.

Key advantages:
- **Historical vol is well-documented** -- BTC trailing 1-year vol has consistently averaged ~60%
- **Lognormal model is standard** -- same framework used by options traders worldwide
- **Vol skew detection** -- estimates implied vol from market prices and identifies directional skew
- **Bin-level edge** -- finds the specific bins most mispriced by the vol mismatch

## Signal Logic

### Volatility Skew Model

1. Parse BTC price bin boundaries from market questions
2. Estimate market-implied vol via grid search over lognormal model
3. Compute fair bin probabilities using historical 60% vol
4. Compare fair probability to market price per bin
5. Trade when `|fair - market| >= entry_edge`

### Conviction-Based Sizing

- `conviction = min(|edge| / entry_edge, 2.0) / 2.0`
- `size = max($1.00, conviction * MAX_POSITION_USD)`
- Larger edge = larger position, capped at MAX_POSITION_USD

### Remix Ideas

- **Deribit options surface**: Use actual options-implied vol instead of historical
- **Realized vol regimes**: Switch between high/low vol regimes based on recent price action
- **GARCH forecasting**: Use GARCH(1,1) to forecast forward vol dynamically
- **Correlation with macro**: Adjust vol for Fed meetings, CPI releases, halving proximity

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
clawhub install kalshi-crypto-volatility-skew-trader
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
| `SIMMER_CRYPTO_VSKEW_ENTRY_EDGE` | `0.08` | Min divergence between fair and market to trigger trade |
| `SIMMER_CRYPTO_VSKEW_EXIT_THRESHOLD` | `0.45` | Sell position when price reaches this level |
| `SIMMER_CRYPTO_VSKEW_MAX_POSITION_USD` | `5.00` | Max USDC per trade |
| `SIMMER_CRYPTO_VSKEW_MAX_TRADES_PER_RUN` | `4` | Max trades per execution cycle |
| `SIMMER_CRYPTO_VSKEW_SLIPPAGE_MAX` | `0.15` | Max slippage before skipping (0.15 = 15%) |
| `SIMMER_CRYPTO_VSKEW_MIN_LIQUIDITY` | `0` | Min market liquidity USD (0 = disabled) |

## Dependency

`simmer-sdk` is published on PyPI by Simmer Markets.
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
- Publisher: hello@simmer.markets

Review the source before providing live credentials if you require full auditability.
