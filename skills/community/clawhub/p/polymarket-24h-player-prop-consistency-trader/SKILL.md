---
name: polymarket-24h-player-prop-consistency-trader
description: Trades NBA player prop mispricings on Polymarket by detecting cross-stat consistency or divergence for the same player (Points, Rebounds, Assists O/U) and identifying outlier stats that disagree with the consensus direction.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: 24h Player Prop Consistency Trader
  difficulty: advanced
---

# 24h Player Prop Consistency Trader

> **This is a template.**
> The default signal is cross-stat consistency analysis for NBA player props -- remix it with additional sports, stat types, or team-level hierarchy checks.
> The skill handles all the plumbing (market discovery, player grouping, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

Polymarket lists multiple stat lines for the same NBA player:

- "Jayson Tatum: Points O/U 23.5" = 51.5%
- "Jayson Tatum: Rebounds O/U 8.5" = 51.5%
- "Jayson Tatum: Assists O/U 4.5" = 51.0%

Retail trades each stat in isolation. But these stats share the same underlying game context -- minutes played, matchup difficulty, pace, injury status. When all stats for a player deviate in the same direction, it is a confirmed signal. When one stat diverges, it is likely mispriced.

## The Edge: Cross-Stat Consistency

### Signal Type 1: Confirmation (All Stats Agree)

When all of a player's stats deviate from 50% in the same direction:

```
Derrick White: Points O/U 16.5 = 22%   (below 50%)
Derrick White: Rebounds O/U 4.5 = 20.5% (below 50%)
Derrick White: Assists O/U 4.5 = 20.9%  (below 50%)
```

All three stats say "under is likely." This multi-stat confirmation boosts conviction on each individual market.

### Signal Type 2: Outlier Divergence (One Stat Disagrees)

When most stats agree but one diverges:

```
Player X: Points O/U 20.5 = 35%   (below 50% -- consensus: under)
Player X: Rebounds O/U 6.5 = 33%   (below 50% -- consensus: under)
Player X: Assists O/U 5.5 = 65%    (above 50% -- OUTLIER!)
```

The assists line disagrees with the points and rebounds consensus. This outlier is likely mispriced -- trade it toward the consensus direction.

## Why This Works

1. **Retail trades in silos** -- most users evaluate each stat line independently without cross-referencing other stats for the same player
2. **Shared game context** -- a player's minutes, matchup, and pace affect all stat categories simultaneously
3. **No cross-stat enforcement** -- unlike sportsbooks, Polymarket has no mechanism to maintain consistency across a player's prop lines
4. **Statistical confirmation** -- when 2-3 stats agree, the probability of the consensus being correct is significantly higher than any single stat alone

## Signal Logic

1. Discover all NBA player prop markets via keyword search (Points O/U, Rebounds O/U, Assists O/U)
2. Parse each question: extract player name, stat type, O/U line value
3. Group markets by player
4. For each player with 2+ stat lines:
   - Check if all stats deviate from 50% in the same direction (confirmation)
   - If not, identify the outlier stat that disagrees with the consensus
5. Trade outliers toward the consensus direction; boost conviction on confirmed signals
6. Size by conviction (divergence magnitude + cross-stat boost), not flat amount

## Safety & Execution Mode

**The skill defaults to paper trading (`venue="sim"`). Real trades only with `--live` flag.**

| Scenario | Mode | Financial risk |
|---|---|---|
| `python trader.py` | Paper (sim) | None |
| Cron / automaton | Paper (sim) | None |
| `python trader.py --live` | Live (polymarket) | Real USDC |

`autostart: false` and `cron: null` mean nothing runs automatically until configured in Simmer UI.

## Required Credentials

| Variable | Required | Notes |
|---|---|---|
| `SIMMER_API_KEY` | Yes | Trading authority. Treat as a high-value credential. |

## Tunables (Risk Parameters)

All declared as `tunables` in `clawhub.json` and adjustable from the Simmer UI.

| Variable | Default | Purpose |
|---|---|---|
| `SIMMER_MAX_POSITION` | `40` | Max USDC per trade at full conviction |
| `SIMMER_MIN_TRADE` | `5` | Floor for any trade |
| `SIMMER_MIN_VOLUME` | `5000` | Min market volume filter (USD) |
| `SIMMER_MAX_SPREAD` | `0.08` | Max bid-ask spread |
| `SIMMER_MIN_DAYS` | `0` | Min days until resolution (0 = allow same-day) |
| `SIMMER_MAX_POSITIONS` | `8` | Max concurrent open positions |
| `SIMMER_YES_THRESHOLD` | `0.38` | Buy YES only if market probability <= this |
| `SIMMER_NO_THRESHOLD` | `0.62` | Sell NO only if market probability >= this |
| `SIMMER_MIN_DIVERGENCE` | `0.05` | Min cross-stat divergence to trigger a trade |

## Edge Thesis

Traditional sportsbooks use correlated models that price a player's points, rebounds, and assists as a coherent package. Polymarket has no such mechanism -- each stat line is priced by its own order book with its own liquidity pool. This creates systematic inconsistencies when:

- A sharp bettor pushes one stat line without the others following
- New information (injury report, lineup change) propagates unevenly across stat types
- Low-liquidity stat lines (assists, rebounds) lag behind high-liquidity lines (points)
- Market makers leave cross-stat gaps during off-hours

This skill treats a player's stat lines as a correlated bundle and trades the repair when they diverge.

## Dependency

`simmer-sdk` by Simmer Markets (SpartanLabsXyz)
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
