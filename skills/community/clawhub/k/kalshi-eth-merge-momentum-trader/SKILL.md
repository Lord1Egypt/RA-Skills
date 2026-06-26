---
name: kalshi-eth-merge-momentum-trader
description: Trades ETH price markets on Kalshi using the post-merge deflation thesis. ETH burns ~0.5% of supply annually via EIP-1559, creating structural upward pressure. Requires SIMMER_API_KEY and simmer-sdk.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: Kalshi ETH Merge Momentum Trader
  difficulty: advanced
  homepage: "https://simmer.markets/skills"
  repository: "https://github.com/SpartanLabsXyz/simmer-sdk"
  requires_env: "SIMMER_API_KEY"
  requires_pip: "simmer-sdk"
  default_mode: "paper"
  live_flag: "--live"
---

# Kalshi ETH Merge Momentum Trader

> **This is a template.**
> The default signal uses a static 0.5% annual burn rate -- remix it with live ultrasound.money data, dynamic burn rate tracking, or EIP-1559 base fee analysis.
> The skill handles all the plumbing (market discovery, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

Post-merge Ethereum burns approximately 0.5% of its total supply annually through the EIP-1559 fee burn mechanism. When gas usage exceeds issuance to validators, ETH becomes net deflationary. This skill computes a deflation-adjusted fair value and trades when markets underprice this structural supply reduction.

Key advantages:
- **Structural thesis** -- supply reduction is mechanical, not speculative
- **Time-sensitive** -- longer time horizons amplify the deflation effect
- **Verifiable** -- burn rate data is on-chain and public

## Signal Logic

### Deflation Model

1. Compute deflation-adjusted price: `adj = base * (1 + net_deflation * days/365 * 0.5)`
2. Convert price target to fair probability using logistic model
3. Compare fair probability to market price
4. Trade when `|fair - market| >= entry_edge`

### Remix Ideas

- **Live burn rate**: Track ultrasound.money for real-time ETH burn data
- **Dynamic issuance**: Adjust for changing validator count
- **Gas price correlation**: Higher gas = higher burn = more deflation
- **Macro overlay**: Fed rate expectations affect crypto demand

## Risk Parameters

| Parameter | Default | Notes |
|-----------|---------|-------|
| Entry edge | 10% | Min model-vs-market divergence to trade |
| Exit threshold | 45% | Sell when position price reaches this |
| Max position size | $5.00 USDC | Per market |
| Max trades per run | 3 | Rate limiting |
| Annual burn rate | 0.5% | ETH supply burn rate assumption |
| Base ETH price | $3500 | Current ETH price baseline |

## Installation & Setup

```bash
clawhub install kalshi-eth-merge-momentum-trader
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
| `SIMMER_ETH_MERGE_ENTRY_EDGE` | `0.10` | Min divergence to trigger trade |
| `SIMMER_ETH_MERGE_EXIT_THRESHOLD` | `0.45` | Sell position when price reaches this level |
| `SIMMER_ETH_MERGE_MAX_POSITION_USD` | `5.00` | Max USDC per trade |
| `SIMMER_ETH_MERGE_MAX_TRADES_PER_RUN` | `3` | Max trades per execution cycle |
| `SIMMER_ETH_MERGE_SLIPPAGE_MAX` | `0.15` | Max slippage before skipping (15%) |
| `SIMMER_ETH_MERGE_MIN_LIQUIDITY` | `0` | Min market liquidity USD (0 = disabled) |
| `SIMMER_ETH_MERGE_BURN_PCT` | `0.5` | Annual ETH supply burn rate (%) |
| `SIMMER_ETH_MERGE_BASE_PRICE` | `3500` | Current ETH price baseline ($) |

## Dependency

`simmer-sdk` is published on PyPI by Simmer Markets.
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
- Publisher: hello@simmer.markets

Review the source before providing live credentials if you require full auditability.
