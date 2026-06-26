---
name: polymarket-twitter-weekend-drift-trader
description: Exploits systematic weekday/weekend posting rate differences in post-count bin markets. Requires SIMMER_API_KEY and simmer-sdk. Use when you want to capture alpha from weekend drift mispricing where markets reflect weekday cadence but the period spans weekends.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: Twitter Weekend Drift Trader
  difficulty: advanced
  homepage: "https://simmer.markets/skills"
  repository: "https://github.com/SpartanLabsXyz/simmer-sdk"
  requires_env: "SIMMER_API_KEY"
  requires_pip: "simmer-sdk"
  default_mode: "paper"
  live_flag: "--live"
---

# Twitter Weekend Drift Trader

> **This is a template.**  
> The default signal uses fixed weekday/weekend rate differentials — remix it with hourly posting distributions, holiday calendars, or timezone-aware activity windows.  
> The skill handles all the plumbing (market discovery, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

Public figures post 20-30% less on weekends. But market makers often set prices on Friday, reflecting weekday cadence. A 3-day period spanning Fri-Sun has very different expected post counts than Mon-Wed.

This skill counts the actual weekdays vs weekend days in each market's period and adjusts the expected rate accordingly.

## Signal Logic

### Weekend Rate Differentials

| Person | Weekday Rate | Weekend Rate | Drop |
|--------|-------------|-------------|------|
| Elon Musk | 72/day | 50/day | -31% |
| Donald Trump | 25/day | 20/day | -20% |
| Vitalik Buterin | 9/day | 7/day | -22% |
| CZ | 14/day | 10/day | -29% |

### How It Works

1. Parse the date range from the market question
2. Count actual weekdays and weekend days
3. Compute `adjusted_lambda = weekday_rate * weekdays + weekend_rate * weekends`
4. Compare to `naive_lambda = average_rate * total_days`
5. The drift determines which bins are over/underpriced

### Example

Elon Musk, March 28 (Fri) to March 30 (Sun) = 3 days:
- Naive: 65/day * 3 = 195 posts
- Adjusted: 72*1 + 50*2 = 172 posts
- **Drift: -12%** — lower bins underpriced, higher bins overpriced

### Remix Ideas

- **Holiday calendar**: Major holidays (Christmas, July 4th) suppress posting even more than weekends
- **Hourly distribution**: Model posting by hour-of-day for sub-daily market periods
- **Timezone awareness**: Elon posts Pacific time, Trump posts Eastern — periods crossing midnight differ
- **Rolling rate updates**: Re-estimate weekday/weekend split weekly from actual data

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
clawhub install polymarket-twitter-weekend-drift-trader
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
