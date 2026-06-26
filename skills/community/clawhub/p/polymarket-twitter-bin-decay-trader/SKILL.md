---
name: polymarket-twitter-bin-decay-trader
description: Trades post-count bin markets by tracking elapsed time to identify mathematically dead bins that still hold residual probability. Requires SIMMER_API_KEY and simmer-sdk. Use when you want to exploit time-decay mispricing in Twitter post-count markets where bins can no longer resolve YES.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: Twitter Bin Decay Trader
  difficulty: advanced
  homepage: "https://simmer.markets/skills"
  repository: "https://github.com/SpartanLabsXyz/simmer-sdk"
  requires_env: "SIMMER_API_KEY"
  requires_pip: "simmer-sdk"
  default_mode: "paper"
  live_flag: "--live"
---

# Twitter Bin Decay Trader

> **This is a template.**  
> The default signal estimates posts-so-far from elapsed time and daily rate — remix it with real-time post counting via Twitter API, Social Blade scrapers, or Polymarket order flow analysis.  
> The skill handles all the plumbing (market discovery, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

As a posting period progresses, bins become mathematically eliminable. If Elon has estimated ~130 tweets after 2 of 3 days, the "40-64" bin is dead — but it might still trade at 5-10% because the market is slow to update.

This skill tracks the **elapsed fraction** of each market's period and computes which bins are still viable, which are dead, and which are on-trajectory.

## Signal Logic

### Viability Computation

1. Parse start/end dates from market question
2. Compute `elapsed_fraction = (now - start) / (end - start)`
3. Estimate `posts_so_far = elapsed_fraction * daily_rate * period_days`
4. Calculate reachable range:
   - `max_total = posts_so_far + max_daily_rate * remaining_days`
   - `min_total = posts_so_far + 0.3 * daily_rate * remaining_days`
5. If `bin_lower > max_total` → bin is **dead** (unreachable)
6. If `bin_upper < min_total` → bin is **dead** (already surpassed)

### Max Daily Rates (Historical Extremes)

| Person | Avg Daily | Max Daily | Notes |
|--------|-----------|-----------|-------|
| Elon Musk | 65 | 120 | Thread storms can 2x rate |
| Donald Trump | 23 | 50 | Rally days spike |
| Vitalik | 8 | 20 | Conference days |
| CZ | 12 | 30 | Exchange drama days |

### Trading Dead Bins

- Dead bin priced >62% → strong NO signal (sell the corpse)
- Viable bin priced <38% and on-trajectory → YES signal (buy the survivor)
- Conviction scales with both threshold distance AND viability confidence

### Remix Ideas

- **Real-time post counting**: Replace estimation with actual count from Twitter API
- **Velocity tracking**: Track rate changes within the period (accelerating vs decelerating)
- **Multi-bin portfolio**: Short dead bins and long viable bins simultaneously for hedge

## Risk Parameters

| Parameter | Default | Notes |
|-----------|---------|-------|
| Max position size | $40 USDC | Per market |
| Min market volume | $1,000 | Standard filter |
| Max bid-ask spread | 10% | Default threshold |
| Min days to resolution | 0 | Post-count markets are short-lived |
| Max open positions | 8 | Diversify across bins |

## Installation & Setup

```bash
clawhub install polymarket-twitter-bin-decay-trader
```

Requires: `SIMMER_API_KEY` environment variable.

## Cron Schedule

Cron is set to `null` — the skill does not run on a schedule until you configure it in the Simmer UI.

## Safety & Execution Mode

**The skill defaults to paper trading (`venue="sim"`). Real trades only execute when `--live` is passed explicitly.**

| Scenario | Mode | Financial risk |
|----------|------|----------------|
| `python trader.py` | Paper (sim) | None |
| Cron / automaton | Paper (sim) | None |
| `python trader.py --live` | Live (polymarket) | Real USDC |

The automaton cron is set to `null` — it does not run on a schedule until you configure it in the Simmer UI. `autostart: false` means it won't start automatically on install.

## Required Credentials

| Variable | Required | Notes |
|----------|----------|-------|
| `SIMMER_API_KEY` | Yes | Trading authority — keep this credential private. Do not place a live-capable key in any environment where automated code could call `--live`. |

## Tunables (Risk Parameters)

All risk parameters are declared in `clawhub.json` as `tunables` and adjustable from the Simmer UI without code changes. They use `SIMMER_`-prefixed env vars so `apply_skill_config()` can load them securely.

| Variable | Default | Purpose |
|----------|---------|---------|
| `SIMMER_MAX_POSITION` | `40` | Max USDC per trade (reached at 100% conviction) |
| `SIMMER_MIN_VOLUME` | `1000` | Min market volume filter (USD) |
| `SIMMER_MAX_SPREAD` | `0.10` | Max bid-ask spread (0.10 = 10%) |
| `SIMMER_MIN_DAYS` | `0` | Min days until market resolves |
| `SIMMER_MAX_POSITIONS` | `8` | Max concurrent open positions |
| `SIMMER_YES_THRESHOLD` | `0.38` | Buy YES if market price ≤ this value |
| `SIMMER_NO_THRESHOLD` | `0.62` | Sell NO if market price ≥ this value |
| `SIMMER_MIN_TRADE` | `5` | Floor for any trade (min USDC regardless of conviction) |

## Dependency

`simmer-sdk` is published on PyPI by Simmer Markets.
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
- Publisher: hello@simmer.markets

Review the source before providing live credentials if you require full auditability.
