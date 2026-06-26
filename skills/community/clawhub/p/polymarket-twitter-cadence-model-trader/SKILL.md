---
name: polymarket-twitter-cadence-model-trader
description: Trades post-count bin markets using a Poisson statistical model to predict the most likely bins based on historical posting rates. Requires SIMMER_API_KEY and simmer-sdk. Use when you want to price Twitter post-count bins with math instead of gut feeling.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: Twitter Cadence Model Trader
  difficulty: advanced
  homepage: "https://simmer.markets/skills"
  repository: "https://github.com/SpartanLabsXyz/simmer-sdk"
  requires_env: "SIMMER_API_KEY"
  requires_pip: "simmer-sdk"
  default_mode: "paper"
  live_flag: "--live"
---

# Twitter Cadence Model Trader

> **This is a template.**  
> The default signal is a Poisson model based on historical posting rates — remix it with Twitter/X API v2 real-time post counts, time-of-day distributions, or NLP topic-burst detection.  
> The skill handles all the plumbing (market discovery, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

Post-count bin markets (e.g., "Will Elon Musk post 190-214 tweets from March 30 to April 1?") are perfect for statistical modeling because **the number of posts in a time interval follows a Poisson distribution**.

Retail traders price these bins by gut feeling. This skill prices them with math.

## Signal Logic

### Poisson Model

1. Parse the person, bin range, and time period from the market question
2. Compute lambda = person's historical daily rate x period days
3. Calculate P(bin) = sum of Poisson PMF from bin_lower to bin_upper
4. Compare model probability to market price
5. Trade when model diverges from market AND price is in threshold band

### Person Baselines

| Person | Daily Rate | Platform |
|--------|-----------|----------|
| Elon Musk | ~65 tweets/day | X/Twitter |
| Donald Trump | ~23 posts/day | Truth Social |
| Vitalik Buterin | ~8 posts/day | X/Twitter |
| CZ | ~12 posts/day | X/Twitter |

### Model Bias

The Poisson model acts as a conviction multiplier:
- If model says bin is 2x more likely than market → 2x conviction boost
- If model says bin is 0.5x less likely → signal vetoed (don't trade against math)

### Remix Ideas

- **Twitter API v2**: Replace baseline daily_rate with real-time 7-day rolling average
- **Time-of-day model**: Elon posts 60% of tweets between 6PM-2AM Pacific — use hourly Poisson
- **Negative binomial**: Better than Poisson for overdispersed counts (bursty posters)
- **Topic burst NLP**: Detect thread-mode (3x rate) vs normal mode

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
clawhub install polymarket-twitter-cadence-model-trader
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
