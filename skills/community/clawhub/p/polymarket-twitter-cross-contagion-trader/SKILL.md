---
name: polymarket-twitter-cross-contagion-trader
description: Trades post-count bin markets by detecting cross-person contagion where one public figure posting heavily causes correlated figures to increase their rate. Requires SIMMER_API_KEY and simmer-sdk. Use when you want to exploit inter-person posting correlation that markets price independently.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: Twitter Cross-Contagion Trader
  difficulty: advanced
  homepage: "https://simmer.markets/skills"
  repository: "https://github.com/SpartanLabsXyz/simmer-sdk"
  requires_env: "SIMMER_API_KEY"
  requires_pip: "simmer-sdk"
  default_mode: "paper"
  live_flag: "--live"
---

# Twitter Cross-Contagion Trader

> **This is a template.**  
> The default signal detects cross-person posting correlation from market prices — remix it with real-time Twitter API monitoring, topic co-occurrence tracking, or network graph analysis of reply/quote-tweet chains.  
> The skill handles all the plumbing (market discovery, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

Public figures don't post in isolation. When Elon Musk enters a political debate, Trump often responds on Truth Social. When crypto crashes, both CZ and Vitalik spike their posting rates.

Markets price each person's bins independently. This skill exploits the **cross-person correlation** that markets miss.

## Signal Logic

### Phase 1: Detect Contagion

1. Group all post-count bin markets by person
2. Compute each person's "heat" — are the market prices shifted toward higher bins?
3. Positive heat = market expects more posts than baseline (person is "hot")

### Phase 2: Apply Contagion Coefficients

| Source | Target | Beta | Why |
|--------|--------|------|-----|
| Elon | Trump | 0.15 | Political overlap, mutual commentary |
| Trump | Elon | 0.12 | Elon reacts to executive orders |
| Elon | Vitalik | 0.08 | Crypto topic overlap |
| Vitalik | Elon | 0.06 | Elon sometimes responds to ETH news |
| Elon | CZ | 0.05 | Crypto/exchange overlap |

### Phase 3: Trade with Adjusted Conviction

When person A is hot and beta(A->B) > 0, boost conviction on person B's higher bins.

### Remix Ideas

- **Real-time monitoring**: Track actual post counts in real-time instead of inferring from market prices
- **Reply chain analysis**: @-mention graphs show direct contagion paths
- **Topic clustering**: NLP on recent posts to detect shared topics driving correlation
- **Dynamic beta**: Re-estimate contagion coefficients weekly from observed data

## Risk Parameters

| Parameter | Default | Notes |
|-----------|---------|-------|
| Max position size | $40 USDC | Per market |
| Min market volume | $1,000 | Standard filter |
| Max bid-ask spread | 10% | Default threshold |
| Min days to resolution | 0 | Post-count markets are short-lived |
| Max open positions | 8 | Diversify across persons |

## Installation & Setup

```bash
clawhub install polymarket-twitter-cross-contagion-trader
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
