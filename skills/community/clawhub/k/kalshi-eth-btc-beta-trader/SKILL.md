---
name: kalshi-eth-btc-beta-trader
description: Trades ETH price markets on Kalshi by exploiting the 1.3x beta relationship between ETH and BTC. When BTC odds shift, ETH markets lag behind -- this skill captures the catch-up. Requires SIMMER_API_KEY and simmer-sdk.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: Kalshi ETH-BTC Beta Trader
  difficulty: advanced
  homepage: "https://simmer.markets/skills"
  repository: "https://github.com/SpartanLabsXyz/simmer-sdk"
  requires_env: "SIMMER_API_KEY"
  requires_pip: "simmer-sdk"
  default_mode: "paper"
  live_flag: "--live"
---

# Kalshi ETH-BTC Beta Trader

> **This is a template.**
> The default signal uses a static 1.3x beta factor between ETH and BTC -- remix it with live correlation calculations, on-chain data feeds, or options-implied volatility surfaces.
> The skill handles all the plumbing (market discovery, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

ETH historically moves approximately 1.3x BTC on a percentage basis. When Kalshi BTC price markets shift, the corresponding ETH markets often lag by several hours. This skill detects the BTC shift, computes the expected ETH fair price using the beta multiplier, and trades when the ETH market has not yet caught up.

Key advantages:
- **Statistically documented beta relationship** -- ETH/BTC correlation is well-studied
- **Lag window is exploitable** -- Kalshi ETH markets update slower than BTC markets
- **Conviction-based sizing** -- larger edge = larger position

## Signal Logic

### Beta Model

1. Fetch active BTC and ETH price markets from Kalshi
2. Detect recent BTC probability shifts (>2% moves)
3. Apply beta factor: `ETH_expected_move = BTC_move * 1.3`
4. Compare expected ETH price to current ETH market price
5. Trade when `|fair - market| >= entry_edge`

### Example (with defaults)

| BTC Shift | ETH Expected | ETH Market | Edge | Action |
|-----------|-------------|------------|------|--------|
| +5% | +6.5% | +2% | +4.5% | BUY YES |
| -3% | -3.9% | -1% | -2.9% | BUY NO |
| +1% | +1.3% | +1% | +0.3% | Hold |

### Conviction-Based Sizing

- `conviction = min(|edge| / entry_edge, 2.0) / 2.0`
- `size = max($5.00, conviction * MAX_POSITION_USD)`
- Larger edge = larger position, capped at MAX_POSITION_USD

### Remix Ideas

- **Live correlation API**: Replace static beta with rolling 30-day correlation
- **Options-implied vol**: Use BTC/ETH options skew for better beta estimates
- **On-chain flows**: Track large ETH/BTC exchange deposits for directional signals
- **Multi-timeframe**: Use 1h, 4h, and 24h beta windows for different market regimes

## Risk Parameters

| Parameter | Default | Notes |
|-----------|---------|-------|
| Entry edge | 10% | Min model-vs-market divergence to trade |
| Exit threshold | 45% | Sell when position price reaches this |
| Max position size | $5.00 USDC | Per market |
| Max trades per run | 4 | Rate limiting |
| Max slippage | 15% | Skip if slippage exceeds |
| Min liquidity | $0 | Disabled by default |
| Beta factor | 1.3 | ETH/BTC beta multiplier |
| Lag window | 6h | Hours to look back for BTC shifts |

## Installation & Setup

```bash
clawhub install kalshi-eth-btc-beta-trader
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
| `SIMMER_ETH_BTCBETA_ENTRY_EDGE` | `0.10` | Min divergence to trigger trade |
| `SIMMER_ETH_BTCBETA_EXIT_THRESHOLD` | `0.45` | Sell position when price reaches this level |
| `SIMMER_ETH_BTCBETA_MAX_POSITION_USD` | `5.00` | Max USDC per trade |
| `SIMMER_ETH_BTCBETA_MAX_TRADES_PER_RUN` | `4` | Max trades per execution cycle |
| `SIMMER_ETH_BTCBETA_SLIPPAGE_MAX` | `0.15` | Max slippage before skipping (15%) |
| `SIMMER_ETH_BTCBETA_MIN_LIQUIDITY` | `0` | Min market liquidity USD (0 = disabled) |
| `SIMMER_ETH_BTCBETA_BETA` | `1.3` | ETH/BTC beta multiplier |
| `SIMMER_ETH_BTCBETA_LAG_HOURS` | `6.0` | Hours to look back for BTC shifts |

## Dependency

`simmer-sdk` is published on PyPI by Simmer Markets.
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
- Publisher: hello@simmer.markets

Review the source before providing live credentials if you require full auditability.
