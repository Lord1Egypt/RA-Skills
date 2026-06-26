---
name: kalshi-crypto-momentum-trader
description: Uses 7-day and 30-day price trend extrapolation to trade crypto year-end price target markets on Kalshi. Requires SIMMER_API_KEY and simmer-sdk.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: Kalshi Crypto Momentum Trader
  difficulty: advanced
  homepage: "https://simmer.markets/skills"
  repository: "https://github.com/SpartanLabsXyz/simmer-sdk"
  requires_env: "SIMMER_API_KEY"
  requires_pip: "simmer-sdk"
  default_mode: "paper"
  live_flag: "--live"
---

# Kalshi Crypto Momentum Trader

> **This is a template.**  
> The default signal uses static 7d/30d momentum parameters -- remix it with live price API feeds, multiple timeframes, or volume-weighted momentum.  
> The skill handles all the plumbing (market discovery, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

Crypto markets on Kalshi price year-end targets. Price momentum (7d/30d trends) is a strong predictor of whether targets will be reached. This skill extrapolates recent price trends to compute probability that each target is hit by year-end.

## Signal Logic

### Momentum Trend Model

1. Compute 7-day and 30-day price change ratios for BTC/ETH
2. Extrapolate current trend to year-end using exponential projection
3. Compute probability of reaching each price target under trend assumption
4. Compare model probability to Kalshi market price
5. Trade when `|model - market| >= entry_edge`

### Remix Ideas

- **Live price API**: CoinGecko/Binance for real-time trend computation
- **Multiple timeframe ensemble**: 1d, 7d, 30d, 90d momentum signals
- **Volume-weighted momentum**: Higher conviction when volume confirms
- **Mean-reversion overlay**: Dampen extreme trend signals

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
clawhub install kalshi-crypto-momentum-trader
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

| Variable | Default | Purpose |
|----------|---------|---------|
| `SIMMER_CRYPTO_MOM_ENTRY_EDGE` | `0.10` | Min divergence to trigger trade |
| `SIMMER_CRYPTO_MOM_EXIT_THRESHOLD` | `0.45` | Sell position when price reaches this level |
| `SIMMER_CRYPTO_MOM_MAX_POSITION_USD` | `5.00` | Max USDC per trade |
| `SIMMER_CRYPTO_MOM_MAX_TRADES_PER_RUN` | `3` | Max trades per execution cycle |
| `SIMMER_CRYPTO_MOM_SLIPPAGE_MAX` | `0.15` | Max slippage before skipping |
| `SIMMER_CRYPTO_MOM_MIN_LIQUIDITY` | `0` | Min market liquidity USD (0 = disabled) |

## Dependency

`simmer-sdk` is published on PyPI by Simmer Markets.
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
- Publisher: hello@simmer.markets

Review the source before providing live credentials if you require full auditability.
