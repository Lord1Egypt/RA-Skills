---
name: kalshi-eth-gas-correlation-trader
description: Trades ETH price markets on Kalshi using on-chain gas prices as a bullish/bearish signal. High gas = strong demand = bullish for ETH. Requires SIMMER_API_KEY and simmer-sdk.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: Kalshi ETH Gas Correlation Trader
  difficulty: advanced
  homepage: "https://simmer.markets/skills"
  repository: "https://github.com/SpartanLabsXyz/simmer-sdk"
  requires_env: "SIMMER_API_KEY"
  requires_pip: "simmer-sdk"
  default_mode: "paper"
  live_flag: "--live"
---

# Kalshi ETH Gas Correlation Trader

> **This is a template.**
> The default signal uses gas price regimes as a directional indicator -- remix it with live Etherscan gas API, EIP-1559 base fee tracking, or L2 activity metrics.
> The skill handles all the plumbing (market discovery, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

High on-chain gas prices indicate strong demand for Ethereum block space (DeFi activity, NFT mints, token launches). This demand correlates positively with ETH price. This skill classifies gas into regimes and applies a directional bias to ETH price market probabilities.

Key advantages:
- **Leading indicator** -- gas spikes often precede price moves
- **On-chain verifiable** -- gas data is public and real-time
- **Regime-based** -- avoids noise by classifying into discrete regimes

## Signal Logic

### Gas Regime Model

1. Classify current gas price into regime (extreme/high/normal/low/dead)
2. Map regime to directional bias (+15% to -10%)
3. Apply bias to each ETH price market probability
4. Trade when `|fair - market| >= entry_edge`

### Gas Regimes

| Regime | Gas (gwei) | Bias | Interpretation |
|--------|-----------|------|----------------|
| Extreme | >100 | +15% | Very bullish |
| High | >50 | +8% | Bullish |
| Normal | >20 | 0% | Neutral |
| Low | >10 | -5% | Bearish |
| Dead | <10 | -10% | Very bearish |

### Remix Ideas

- **Live Etherscan API**: Real-time gas price feed instead of estimates
- **EIP-1559 base fee**: More accurate demand metric post-merge
- **L2 activity**: Track Arbitrum/Optimism activity for full picture
- **DeFi TVL overlay**: Combine gas with total value locked trends

## Risk Parameters

| Parameter | Default | Notes |
|-----------|---------|-------|
| Entry edge | 10% | Min model-vs-market divergence to trade |
| Exit threshold | 45% | Sell when position price reaches this |
| Max position size | $5.00 USDC | Per market |
| Max trades per run | 3 | Rate limiting |
| Gas high threshold | 50 gwei | Above this = high demand regime |
| Gas low threshold | 10 gwei | Below this = dead regime |

## Installation & Setup

```bash
clawhub install kalshi-eth-gas-correlation-trader
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
| `SIMMER_ETH_GAS_ENTRY_EDGE` | `0.10` | Min divergence to trigger trade |
| `SIMMER_ETH_GAS_EXIT_THRESHOLD` | `0.45` | Sell position when price reaches this level |
| `SIMMER_ETH_GAS_MAX_POSITION_USD` | `5.00` | Max USDC per trade |
| `SIMMER_ETH_GAS_MAX_TRADES_PER_RUN` | `3` | Max trades per execution cycle |
| `SIMMER_ETH_GAS_SLIPPAGE_MAX` | `0.15` | Max slippage before skipping (15%) |
| `SIMMER_ETH_GAS_MIN_LIQUIDITY` | `0` | Min market liquidity USD (0 = disabled) |
| `SIMMER_ETH_GAS_HIGH_GWEI` | `50` | Gas threshold for high-demand regime |
| `SIMMER_ETH_GAS_LOW_GWEI` | `10` | Gas threshold for dead regime |

## Dependency

`simmer-sdk` is published on PyPI by Simmer Markets.
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
- Publisher: hello@simmer.markets

Review the source before providing live credentials if you require full auditability.
