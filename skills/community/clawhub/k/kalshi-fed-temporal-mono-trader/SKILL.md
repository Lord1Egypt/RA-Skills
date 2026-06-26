---
name: kalshi-fed-temporal-mono-trader
description: Exploits temporal monotonicity violations in Fed rate markets on Kalshi. P(rate cut by June) >= P(rate cut by April) always -- if April is priced higher than June, that's an arbitrage. Requires SIMMER_API_KEY and simmer-sdk.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: Kalshi Fed Temporal Monotonicity Trader
  difficulty: advanced
  homepage: "https://simmer.markets/skills"
  repository: "https://github.com/SpartanLabsXyz/simmer-sdk"
  requires_env: "SIMMER_API_KEY"
  requires_pip: "simmer-sdk"
  default_mode: "paper"
  live_flag: "--live"
---

# Kalshi Fed Temporal Monotonicity Trader

> **This is a template.**
> The default signal detects temporal monotonicity violations in Fed rate markets -- remix it with live yield curve data, Fed funds futures, or options-implied probabilities.
> The skill handles all the plumbing (market discovery, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

Fed rate cut/hike markets across different meeting dates must satisfy temporal monotonicity: the probability of a cut "by June" must be >= the probability of a cut "by April", since June includes April. When this invariant is violated, we have a pure structural arbitrage.

Key advantages:
- **Mathematical certainty** -- this is a logical invariant, not a statistical edge
- **No model risk** -- the relationship P(by later) >= P(by earlier) is always true
- **Self-correcting** -- violations are temporary mispricings that must converge

## Signal Logic

### Temporal Monotonicity

1. Scan all Fed rate cut/hike markets on Kalshi
2. Group by year and type (cut vs hike)
3. Sort chronologically by FOMC meeting date
4. Compare: if P(cut by April) > P(cut by June) + threshold, violation detected
5. Buy YES on the later (underpriced) date market

### Conviction-Based Sizing

- `conviction = min(violation_size / violation_threshold, 2.0) / 2.0`
- `size = max($1.00, conviction * MAX_POSITION_USD)`
- Larger violations = larger positions, capped at MAX_POSITION_USD

## Risk Parameters

| Parameter | Default | Notes |
|-----------|---------|-------|
| Violation threshold | 3% | Min difference to trigger trade |
| Exit threshold | 45% | Sell when position price reaches this |
| Max position size | $5.00 USDC | Per market |
| Max trades per run | 3 | Rate limiting |
| Max slippage | 15% | Skip if slippage exceeds |
| Min liquidity | $0 | Disabled by default |

## Installation & Setup

```bash
clawhub install kalshi-fed-temporal-mono-trader
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
| `SIMMER_FED_TEMP_VIOLATION_THRESHOLD` | `0.03` | Min violation size to trigger trade |
| `SIMMER_FED_TEMP_EXIT_THRESHOLD` | `0.45` | Sell position when price reaches this level |
| `SIMMER_FED_TEMP_MAX_POSITION_USD` | `5.00` | Max USDC per trade |
| `SIMMER_FED_TEMP_MAX_TRADES_PER_RUN` | `3` | Max trades per execution cycle |
| `SIMMER_FED_TEMP_SLIPPAGE_MAX` | `0.15` | Max slippage before skipping trade |
| `SIMMER_FED_TEMP_MIN_LIQUIDITY` | `0` | Min market liquidity USD (0 = disabled) |

## Dependency

`simmer-sdk` is published on PyPI by Simmer Markets.
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
- Publisher: hello@simmer.markets

Review the source before providing live credentials if you require full auditability.
