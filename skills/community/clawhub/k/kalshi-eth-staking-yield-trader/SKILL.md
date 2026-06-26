---
name: kalshi-eth-staking-yield-trader
description: Trades ETH price markets on Kalshi using the 4% staking yield as a fundamental price floor. When markets underprice ETH relative to the yield-implied floor, buy YES. Requires SIMMER_API_KEY and simmer-sdk.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: Kalshi ETH Staking Yield Trader
  difficulty: advanced
  homepage: "https://simmer.markets/skills"
  repository: "https://github.com/SpartanLabsXyz/simmer-sdk"
  requires_env: "SIMMER_API_KEY"
  requires_pip: "simmer-sdk"
  default_mode: "paper"
  live_flag: "--live"
---

# Kalshi ETH Staking Yield Trader

> **This is a template.**
> The default signal uses a static 4% staking yield as a price floor -- remix it with live Lido/Rocket Pool yield data, validator queue depth, or MEV reward estimates.
> The skill handles all the plumbing (market discovery, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

ETH staking yields approximately 4% APR, creating a fundamental floor for ETH price. Rational stakers will not sell below the yield-implied value. This skill computes that floor for each market's time horizon and trades when Kalshi prices imply ETH below the floor.

Key advantages:
- **Fundamental floor** -- staking yield provides a minimum return that supports price
- **Time-adjusted** -- yield floor scales with days to market resolution
- **Conservative model** -- only accounts for yield, not price appreciation upside

## Signal Logic

### Yield Floor Model

1. Fetch active ETH price markets from Kalshi
2. Extract price target from each market question
3. Compute yield floor: `floor = base_price * (1 + yield% * days/365)`
4. Compute fair probability based on target vs floor relationship
5. Trade when `|fair - market| >= entry_edge`

### Example (with defaults, base=$3500, yield=4%)

| Market | Target | Days | Floor | Fair P | Market P | Action |
|--------|--------|------|-------|--------|----------|--------|
| ETH above $3000 | $3000 | 30 | $3511 | 85% | 72% | BUY YES |
| ETH above $4000 | $4000 | 30 | $3511 | 40% | 45% | Hold |
| ETH above $5000 | $5000 | 30 | $3511 | 15% | 28% | BUY NO |

### Conviction-Based Sizing

- `conviction = min(|edge| / entry_edge, 2.0) / 2.0`
- `size = max($5.00, conviction * MAX_POSITION_USD)`

### Remix Ideas

- **Live yield API**: Pull real-time staking yield from Lido/Rocket Pool
- **Validator queue depth**: Queue length affects future yield expectations
- **MEV rewards**: Include MEV as additional yield component
- **Macro overlay**: Adjust floor based on Fed rate decisions

## Risk Parameters

| Parameter | Default | Notes |
|-----------|---------|-------|
| Entry edge | 8% | Min model-vs-market divergence to trade |
| Exit threshold | 45% | Sell when position price reaches this |
| Max position size | $5.00 USDC | Per market |
| Max trades per run | 3 | Rate limiting |
| Staking yield | 4.0% | Annual staking yield assumption |
| Base ETH price | $3500 | Current ETH price baseline |

## Installation & Setup

```bash
clawhub install kalshi-eth-staking-yield-trader
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
| `SIMMER_ETH_STAKE_ENTRY_EDGE` | `0.08` | Min divergence to trigger trade |
| `SIMMER_ETH_STAKE_EXIT_THRESHOLD` | `0.45` | Sell position when price reaches this level |
| `SIMMER_ETH_STAKE_MAX_POSITION_USD` | `5.00` | Max USDC per trade |
| `SIMMER_ETH_STAKE_MAX_TRADES_PER_RUN` | `3` | Max trades per execution cycle |
| `SIMMER_ETH_STAKE_SLIPPAGE_MAX` | `0.15` | Max slippage before skipping (15%) |
| `SIMMER_ETH_STAKE_MIN_LIQUIDITY` | `0` | Min market liquidity USD (0 = disabled) |
| `SIMMER_ETH_STAKE_YIELD_PCT` | `4.0` | Annual staking yield assumption |
| `SIMMER_ETH_STAKE_BASE_PRICE` | `3500` | Current ETH price baseline |

## Dependency

`simmer-sdk` is published on PyPI by Simmer Markets.
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
- Publisher: hello@simmer.markets

Review the source before providing live credentials if you require full auditability.
