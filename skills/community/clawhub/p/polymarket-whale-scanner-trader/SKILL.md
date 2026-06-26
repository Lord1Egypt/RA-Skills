---
name: polymarket-whale-scanner-trader
description: Scans public Polymarket leaderboards to identify top-performing whale wallets by SmartScore, then trades markets where these whales have high-conviction positions. Dynamically discovers the best traders -- no manual wallet configuration needed.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: Whale Scanner Trader
  difficulty: advanced
---

# Whale Scanner Trader

> **This is a template.**
> The default signal follows top Polymarket whales ranked by SmartScore -- remix it with on-chain analysis, wallet clustering, or time-weighted activity decay.
> The skill handles all the plumbing (leaderboard fetching, whale scoring, consensus building, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

Top Polymarket traders have an edge. The public predicting.top leaderboard ranks wallets by SmartScore -- a composite of win rate, Sharpe ratio, profit factor, and consistency. This skill dynamically discovers the best-performing traders, fetches their recent activity, and builds a consensus map of what the whales are betting on.

When multiple high-scoring whales agree on a direction AND the conviction-based signal independently confirms that direction, the skill trades. This dual-confirmation requirement filters out noise and only acts on high-confidence setups.

## Signal Logic

### Step 1: Fetch and Filter Leaderboard

Top traders are fetched from `predicting.top/api/leaderboard` and filtered by:

| Filter | Default | Purpose |
|---|---|---|
| SmartScore | >= 70 | Only follow proven traders |
| Win rate | >= 55% | Must have positive edge |

### Step 2: Build Whale Consensus

For each qualifying whale, recent activity is fetched from the Polymarket data API. Net positions are extracted (buy YES vs buy NO volume per market), then aggregated across all whales:

```
whale_consensus[market] = {yes_votes, no_votes, total_size, whales}
```

Markets are ranked by total whale size -- strongest conviction first.

### Step 3: Match and Confirm

For each whale consensus market:
1. Find matching Simmer market via keyword/title matching
2. Run `compute_signal()` -- standard conviction-based sizing per CLAUDE.md
3. Only trade if whale direction (YES/NO) aligns with signal direction
4. Check `context_ok()` for flip-flop and slippage safeguards

### Conviction Sizing

Standard conviction-based sizing from CLAUDE.md:

| p | conviction | size |
|---|-----------|------|
| 38% | 0% | $5 (floor) |
| 30% | 21% | $8 |
| 20% | 47% | $19 |
| 0% | 100% | $40 |

### Remix Ideas

- **On-chain clustering**: Group wallets by transaction patterns to identify whale syndicates
- **Time decay**: Weight recent whale activity more heavily than older positions
- **Size-weighted votes**: A whale's $50k position counts more than a $1k position
- **Contrarian mode**: Fade the whales when SmartScore drops (they're losing their edge)
- **Sector filtering**: Only follow whales in categories they historically perform best in

## Risk Parameters

| Parameter | Default | Notes |
|-----------|---------|-------|
| Max position size | $40 USDC | Per market, reached at max conviction |
| Min market volume | $3,000 | Liquidity filter |
| Max bid-ask spread | 10% | Avoid illiquid markets |
| Min days to resolution | 7 | Need time for the trade to work |
| Max open positions | 8 | Concentrated whale-aligned bets |

## Installation & Setup

```bash
clawhub install polymarket-whale-scanner-trader
```

Requires: `SIMMER_API_KEY` environment variable.

## Cron Schedule

Runs on demand or via automaton. Cron is set to `null` -- configure it in the Simmer UI when ready.

## Safety & Execution Mode

**The skill defaults to paper trading (`venue="sim"`). Real trades only execute when `--live` is passed explicitly.**

| Scenario | Mode | Financial risk |
|----------|------|----------------|
| `python trader.py` | Paper (sim) | None |
| Cron / automaton | Paper (sim) | None |
| `python trader.py --live` | Live (polymarket) | Real USDC |

The automaton cron is set to `null` -- it does not run on a schedule until you configure it in the Simmer UI. `autostart: false` means it won't start automatically on install.

## Required Credentials

| Variable | Required | Notes |
|----------|----------|-------|
| `SIMMER_API_KEY` | Yes | Trading authority -- keep this credential private. |

## Tunables (Risk Parameters)

All risk parameters are declared in `clawhub.json` as `tunables` and adjustable from the Simmer UI without code changes. They use `SIMMER_`-prefixed env vars so `apply_skill_config()` can load them securely.

| Variable | Default | Purpose |
|----------|---------|---------|
| `SIMMER_MAX_POSITION` | `40` | Max USDC per trade (reached at 100% conviction) |
| `SIMMER_MIN_TRADE` | `5` | Floor for any trade (min USDC regardless of conviction) |
| `SIMMER_MIN_VOLUME` | `3000` | Min market volume filter (USD) |
| `SIMMER_MAX_SPREAD` | `0.10` | Max bid-ask spread (0.10 = 10%) |
| `SIMMER_MIN_DAYS` | `7` | Min days until market resolves |
| `SIMMER_MAX_POSITIONS` | `8` | Max concurrent open positions |
| `SIMMER_YES_THRESHOLD` | `0.38` | Buy YES if market price <= this value |
| `SIMMER_NO_THRESHOLD` | `0.62` | Sell NO if market price >= this value |
| `SIMMER_MIN_SMART_SCORE` | `70` | Min SmartScore to qualify as a whale to follow |
| `SIMMER_MIN_WIN_RATE` | `0.55` | Min win rate to qualify as a whale to follow |
| `SIMMER_LEADERBOARD_LIMIT` | `20` | How many traders to fetch from the leaderboard |

## Dependency

`simmer-sdk` is published on PyPI by Simmer Markets.
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
- Publisher: hello@simmer.markets

Review the source before providing live credentials if you require full auditability.
