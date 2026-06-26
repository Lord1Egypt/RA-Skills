---
name: kalshi-fed-futures-arb-trader
description: Compares CME FedWatch implied rate probabilities to Kalshi Fed rate decision market prices and trades when divergence exceeds threshold. Requires SIMMER_API_KEY and simmer-sdk. Use when you want to capture alpha from FedWatch-vs-Kalshi pricing gaps on rate decisions.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: Kalshi Fed Futures Arb Trader
  difficulty: advanced
  homepage: "https://simmer.markets/skills"
  repository: "https://github.com/SpartanLabsXyz/simmer-sdk"
  requires_env: "SIMMER_API_KEY"
  requires_pip: "simmer-sdk"
  default_mode: "paper"
  live_flag: "--live"
---

# Kalshi Fed Futures Arb Trader

> **This is a template.**  
> The default signal uses static CME FedWatch probabilities -- remix it with live FedWatch scraping, OIS curve extraction, or SOFR futures-implied paths.  
> The skill handles all the plumbing (market discovery, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

CME FedWatch Tool derives rate-cut probabilities from fed funds futures -- a deep, institutional market. Kalshi lists the same events as prediction markets. This skill compares the two and trades when Kalshi diverges from the futures-implied fair value.

Key advantages:
- **Futures are the institutional benchmark** -- deep liquidity and professional pricing
- **Kalshi retail flow creates mispricing** -- especially around FOMC meetings
- **Multiple meetings** -- signals across the entire rate path

## Signal Logic

### FedWatch Arbitrage Model

1. Load CME FedWatch implied probabilities per FOMC meeting
2. Fetch Kalshi Fed rate decision markets
3. Match markets to meetings and detect direction (cut vs hike)
4. Compute edge: `fair_yes - market_price`
5. Trade when `|edge| >= entry_edge`

### Example (with defaults)

| Meeting | FedWatch P(cut) | Kalshi P | Edge | Action |
|---------|----------------|----------|------|--------|
| Jun 2026 | 35% | 25% | +10% | BUY YES |
| Sep 2026 | 68% | 70% | -2% | Hold |
| Dec 2026 | 82% | 65% | +17% | BUY YES |

### Remix Ideas

- **Live FedWatch scraper**: Auto-refresh from CME website
- **OIS curve extraction**: Derive probabilities from overnight index swaps
- **SOFR futures**: Use SOFR futures strips for higher precision
- **Cross-meeting consistency**: Enforce temporal monotonicity across meetings

## Risk Parameters

| Parameter | Default | Notes |
|-----------|---------|-------|
| Entry edge | 8% | Min FedWatch-vs-Kalshi divergence to trade |
| Exit threshold | 45% | Sell when position price reaches this |
| Max position size | $5.00 USDC | Per market |
| Max trades per run | 3 | Rate limiting |
| Max slippage | 15% | Skip if slippage exceeds |
| Min liquidity | $0 | Disabled by default |

## Installation & Setup

```bash
clawhub install kalshi-fed-futures-arb-trader
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
| `SIMMER_FED_FUT_ENTRY_EDGE` | `0.08` | Min divergence between FedWatch and market to trigger trade |
| `SIMMER_FED_FUT_EXIT_THRESHOLD` | `0.45` | Sell position when price reaches this level |
| `SIMMER_FED_FUT_MAX_POSITION_USD` | `5.00` | Max USDC per trade |
| `SIMMER_FED_FUT_MAX_TRADES_PER_RUN` | `3` | Max trades per execution cycle |
| `SIMMER_FED_FUT_SLIPPAGE_MAX` | `0.15` | Max slippage before skipping (0.15 = 15%) |
| `SIMMER_FED_FUT_MIN_LIQUIDITY` | `0` | Min market liquidity USD (0 = disabled) |

## Dependency

`simmer-sdk` is published on PyPI by Simmer Markets.
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
- Publisher: hello@simmer.markets

Review the source before providing live credentials if you require full auditability.
