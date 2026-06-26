---
name: kalshi-crypto-cycle-model-trader
description: Trades Bitcoin year-end price markets on Kalshi using the 4-year halving cycle pattern to compute fair price probabilities. Requires SIMMER_API_KEY and simmer-sdk. Use when you want to capture alpha from halving-cycle mispricing on BTC price bin markets.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: Kalshi Crypto Cycle Model Trader
  difficulty: advanced
  homepage: "https://simmer.markets/skills"
  repository: "https://github.com/SpartanLabsXyz/simmer-sdk"
  requires_env: "SIMMER_API_KEY"
  requires_pip: "simmer-sdk"
  default_mode: "paper"
  live_flag: "--live"
---

# Kalshi Crypto Cycle Model Trader

> **This is a template.**  
> The default signal uses Bitcoin's 4-year halving cycle with diminishing returns to project fair year-end price probabilities -- remix it with on-chain metrics, options-implied vol, or macro regime models.  
> The skill handles all the plumbing (market discovery, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

Bitcoin year-end price bin markets on Kalshi price outcomes independently. This skill prices them using the well-documented 4-year halving cycle pattern, where each post-halving cycle delivers diminishing but still substantial returns.

Key advantages:
- **Halving cycle is public and verifiable** -- historical pattern of 100x/30x/8x/3x post-halving returns
- **Lognormal model** -- converts expected price and volatility into bin probabilities
- **Cycle position awareness** -- April 2024 halving means we are in year 2 of cycle 4, approaching the historically strongest phase

## Signal Logic

### Halving Cycle Model

1. Determine current position in the 4-year halving cycle (year 2 of cycle 4)
2. Project year-end price from cycle ROI pattern with diminishing returns
3. Use lognormal distribution to compute probability for each price bin
4. Compare model probability to Kalshi market price
5. Trade when `|model - market| >= entry_edge`

### Historical Cycle Returns

| Cycle | Halving Date | Pre-Halving Price | Peak | ROI |
|-------|-------------|-------------------|------|-----|
| 1 | Nov 2012 | $12 | $1,200 | 100x |
| 2 | Jul 2016 | $650 | $20,000 | 30x |
| 3 | May 2020 | $8,500 | $69,000 | 8x |
| 4 | Apr 2024 | $64,000 | ~$192,000 (proj) | ~3x |

### Conviction-Based Sizing

- `conviction = min(|edge| / entry_edge, 2.0) / 2.0`
- `size = max($1.00, conviction * MAX_POSITION_USD)`
- Larger edge = larger position, capped at MAX_POSITION_USD

### Remix Ideas

- **On-chain metrics**: Hash rate, active addresses, MVRV ratio for cycle confirmation
- **Options-implied distribution**: Compare model to Deribit options implied vol
- **Macro regime overlay**: Adjust volatility/expected return based on Fed policy, DXY
- **Multi-cycle ensemble**: Weight multiple cycle models for more robust estimates

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
clawhub install kalshi-crypto-cycle-model-trader
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
| `SIMMER_CRYPTO_CYCLE_ENTRY_EDGE` | `0.10` | Min divergence between model and market to trigger trade |
| `SIMMER_CRYPTO_CYCLE_EXIT_THRESHOLD` | `0.45` | Sell position when price reaches this level |
| `SIMMER_CRYPTO_CYCLE_MAX_POSITION_USD` | `5.00` | Max USDC per trade |
| `SIMMER_CRYPTO_CYCLE_MAX_TRADES_PER_RUN` | `5` | Max trades per execution cycle |
| `SIMMER_CRYPTO_CYCLE_SLIPPAGE_MAX` | `0.15` | Max slippage before skipping (0.15 = 15%) |
| `SIMMER_CRYPTO_CYCLE_MIN_LIQUIDITY` | `0` | Min market liquidity USD (0 = disabled) |

## Dependency

`simmer-sdk` is published on PyPI by Simmer Markets.
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
- Publisher: hello@simmer.markets

Review the source before providing live credentials if you require full auditability.
