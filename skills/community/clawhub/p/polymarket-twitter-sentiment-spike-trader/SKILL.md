---
name: polymarket-twitter-sentiment-spike-trader
description: Detects crisis and news spikes across other Polymarket markets and adjusts expected posting rates upward for post-count bins. Requires SIMMER_API_KEY and simmer-sdk. Use when you want to exploit the correlation between global events and public figure posting frequency.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: Twitter Sentiment Spike Trader
  difficulty: advanced
  homepage: "https://simmer.markets/skills"
  repository: "https://github.com/SpartanLabsXyz/simmer-sdk"
  requires_env: "SIMMER_API_KEY"
  requires_pip: "simmer-sdk"
  default_mode: "paper"
  live_flag: "--live"
---

# Twitter Sentiment Spike Trader

> **This is a template.**  
> The default signal uses other Polymarket markets as a crisis barometer — remix it with VIX/fear indices, Google Trends velocity, news API sentiment, or social listening platforms.  
> The skill handles all the plumbing (market discovery, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

When a geopolitical crisis erupts, politicians tweet 50% more. When crypto crashes, Elon and CZ spike their posting rates. Post-count bin markets are priced on baseline cadence — they don't factor in real-time news intensity.

This skill uses OTHER Polymarket markets as a crisis detector. Extreme probabilities on war/crypto/health markets = crisis mode = higher posting rates expected.

## Signal Logic

### Crisis Detection

1. Scan all non-posting markets on the account
2. Identify markets at extreme probabilities (>85% or <15%) with crisis-adjacent keywords
3. Match crisis topics to person affinity (Trump reacts to war, Elon to crypto)
4. Compute per-person crisis multiplier

### Person Crisis Boosts

| Person | Max Crisis Boost | Top Triggers |
|--------|-----------------|-------------|
| Trump | 1.50x | War, sanctions, tariffs, impeachment |
| Elon | 1.40x | BTC, tariffs, bans, AI |
| CZ | 1.30x | BTC, Binance, SEC, hacks |
| Vitalik | 1.25x | ETH, BTC, DeFi, regulation |

### Cross-Market Intelligence

The skill reads your entire Simmer portfolio as a sentiment layer. The more extreme markets you have imported, the better the crisis signal.

### Remix Ideas

- **VIX correlation**: Track VIX changes as a universal fear proxy
- **Google Trends velocity**: Detect sudden search spikes on person-relevant topics
- **News API**: Real-time headline sentiment scoring
- **Twitter API**: Direct activity monitoring (mentions, replies, quote tweets)

## Risk Parameters

| Parameter | Default | Notes |
|-----------|---------|-------|
| Max position size | $40 USDC | Per market |
| Min market volume | $1,000 | Standard filter |
| Max bid-ask spread | 10% | Default threshold |
| Min days to resolution | 0 | Post-count markets are short-lived |
| Max open positions | 8 | Diversify across events |

## Installation & Setup

```bash
clawhub install polymarket-twitter-sentiment-spike-trader
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
