---
name: kalshi-crypto-monotonicity-trader
description: Enforces monotonicity constraints on crypto price-level markets on Kalshi. P(BTC > $110k) must always >= P(BTC > $120k). Trades violations by buying underpriced lower-threshold contracts and selling overpriced higher-threshold ones. Requires SIMMER_API_KEY and simmer-sdk.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: Kalshi Crypto Monotonicity Trader
  difficulty: advanced
  homepage: "https://simmer.markets/skills"
  repository: "https://github.com/SpartanLabsXyz/simmer-sdk"
  requires_env: "SIMMER_API_KEY"
  requires_pip: "simmer-sdk"
  default_mode: "paper"
  live_flag: "--live"
---

# Kalshi Crypto Monotonicity Trader

> **This is a template.**  
> The default signal enforces monotonicity on crypto price-level bins -- remix it with real-time order book data, implied volatility surfaces, or cross-exchange price feeds.  
> The skill handles all the plumbing (market discovery, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

Crypto price-level markets on Kalshi price "Will BTC be above $X?" for various thresholds. By definition, P(BTC > $110k) >= P(BTC > $120k) because the first event subsumes the second. When the market violates this, we capture the arbitrage by buying the underpriced contract and selling the overpriced one.

Key advantages:
- **Pure math arbitrage** -- no model or opinion needed, just logical consistency
- **Works for BTC and ETH** -- any asset with multiple price-level markets
- **Self-correcting** -- violations close quickly, so early detection matters

## Signal Logic

### Monotonicity Check

1. Fetch all crypto price-level markets (BTC above $X, ETH above $Y)
2. Group by asset, sort by price level ascending
3. Verify P(above lower level) >= P(above higher level) for all pairs
4. When violation exceeds `violation_threshold`, generate paired trades

### Example (with defaults)

| Market | Level | Market P | Expected | Violation |
|--------|-------|----------|----------|-----------|
| BTC > $100k | $100,000 | 45% | >= 35% | -- |
| BTC > $110k | $110,000 | 35% | >= 20% | -- |
| BTC > $120k | $120,000 | 38% | <= 35% | 3% |

In the last row, P(>$120k) = 38% > P(>$110k) = 35%, violating monotonicity by 3%.

### Remix Ideas

- **Order book depth**: Weight violations by available liquidity at each level
- **Implied vol surface**: Use violation patterns to infer mispriced implied volatility
- **Cross-exchange arb**: Compare Kalshi levels to Deribit options strikes

## Risk Parameters

| Parameter | Default | Notes |
|-----------|---------|-------|
| Violation threshold | 3% | Min probability gap to trigger trade |
| Exit threshold | 45% | Sell when position price reaches this |
| Max position size | $5.00 USDC | Per market |
| Max trades per run | 3 | Rate limiting |
| Max slippage | 15% | Skip if slippage exceeds |
| Min liquidity | $0 | Disabled by default |

## Installation & Setup

```bash
clawhub install kalshi-crypto-monotonicity-trader
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
| `SIMMER_CRYPTO_MONO_VIOLATION_THRESHOLD` | `0.03` | Min probability gap between adjacent levels to trigger trade |
| `SIMMER_CRYPTO_MONO_EXIT_THRESHOLD` | `0.45` | Sell position when price reaches this level |
| `SIMMER_CRYPTO_MONO_MAX_POSITION_USD` | `5.00` | Max USDC per trade |
| `SIMMER_CRYPTO_MONO_MAX_TRADES_PER_RUN` | `3` | Max trades per execution cycle |
| `SIMMER_CRYPTO_MONO_SLIPPAGE_MAX` | `0.15` | Max slippage before skipping (0.15 = 15%) |
| `SIMMER_CRYPTO_MONO_MIN_LIQUIDITY` | `0` | Min market liquidity USD (0 = disabled) |

## Dependency

`simmer-sdk` is published on PyPI by Simmer Markets.
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
- Publisher: hello@simmer.markets

Review the source before providing live credentials if you require full auditability.
