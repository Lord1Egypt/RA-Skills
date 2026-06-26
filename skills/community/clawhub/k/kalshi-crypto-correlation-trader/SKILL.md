---
name: kalshi-crypto-correlation-trader
description: Exploits BTC/ETH correlation (beta=1.3) to trade ETH price-level markets when BTC makes a significant move. ETH tends to lag BTC moves, creating mispricing windows. Requires SIMMER_API_KEY and simmer-sdk.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: Kalshi Crypto Correlation Trader
  difficulty: advanced
  homepage: "https://simmer.markets/skills"
  repository: "https://github.com/SpartanLabsXyz/simmer-sdk"
  requires_env: "SIMMER_API_KEY"
  requires_pip: "simmer-sdk"
  default_mode: "paper"
  live_flag: "--live"
---

# Kalshi Crypto Correlation Trader

> **This is a template.**  
> The default signal uses a static BTC/ETH beta of 1.3 -- remix it with rolling correlation windows, multi-asset cointegration, or real-time price feed APIs.  
> The skill handles all the plumbing (market discovery, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

BTC and ETH are highly correlated, but ETH markets on Kalshi lag BTC moves by hours. This skill monitors BTC price-level markets as a leading indicator, computes ETH fair values using beta=1.3, and trades when ETH markets have not yet adjusted.

Key advantages:
- **Well-documented correlation** -- BTC/ETH beta is stable around 1.3
- **ETH lags BTC** -- retail-dominated Kalshi ETH markets update slowly
- **Cross-asset signal** -- uses BTC as a free leading indicator for ETH trades

## Signal Logic

### Correlation Model

1. Fetch BTC and ETH price-level markets
2. Compute BTC sentiment from average market probabilities
3. Apply beta=1.3 to derive ETH fair value adjustment
4. Compare adjusted fair value to ETH market price
5. Trade when `|fair - market| >= entry_edge`

### Remix Ideas

- **Rolling beta**: Compute 30-day rolling BTC/ETH beta from price data
- **Multi-asset**: Add SOL, AVAX correlations for broader signal
- **Real-time feeds**: Use CoinGecko/Binance API for live price correlation
- **Regime detection**: Different beta in bull vs bear markets

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
clawhub install kalshi-crypto-correlation-trader
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
| `SIMMER_CRYPTO_CORR_ENTRY_EDGE` | `0.10` | Min divergence between fair value and market to trigger trade |
| `SIMMER_CRYPTO_CORR_EXIT_THRESHOLD` | `0.45` | Sell position when price reaches this level |
| `SIMMER_CRYPTO_CORR_MAX_POSITION_USD` | `5.00` | Max USDC per trade |
| `SIMMER_CRYPTO_CORR_MAX_TRADES_PER_RUN` | `3` | Max trades per execution cycle |
| `SIMMER_CRYPTO_CORR_SLIPPAGE_MAX` | `0.15` | Max slippage before skipping (0.15 = 15%) |
| `SIMMER_CRYPTO_CORR_MIN_LIQUIDITY` | `0` | Min market liquidity USD (0 = disabled) |

## Dependency

`simmer-sdk` is published on PyPI by Simmer Markets.
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
- Publisher: hello@simmer.markets

Review the source before providing live credentials if you require full auditability.
