---
name: polymarket-ladder-esports-kills-trader
description: Trades monotonicity violations in esports Total Kills O/U market ladders on Polymarket. Each esports match spawns multiple kill total thresholds that must be monotonically decreasing — when they are not, it is structural arbitrage. Sizes by conviction with violation magnitude scaling.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: Ladder Esports Kills Curve Trader
  difficulty: advanced
---

# Ladder — Esports Kills Curve Trader

> **This is a template.**
> The default signal is kill total O/U ladder violation detection for esports markets -- remix it with additional titles, map types, or live match data feeds.
> The skill handles all the plumbing (market discovery, ladder construction, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

Esports matches (Dota 2, CS2, Overwatch) list multiple kill total thresholds for the same game:

- "Team A vs Team B Total Kills O/U 47.5" = 58%
- "Team A vs Team B Total Kills O/U 48.5" = 55%
- "Team A vs Team B Total Kills O/U 49.5" = 52%
- "Team A vs Team B Total Kills O/U 50.5" = 54%  <-- VIOLATION

These form a **kill total ladder** -- higher thresholds must always have lower OVER probability. When they don't, it is structural arbitrage.

## The Edge: Kill Ladder Monotonicity Arbitrage

The probability of going OVER a lower kill threshold must always be greater than or equal to going OVER a higher threshold:

```
P(O/U 47.5 OVER) >= P(O/U 48.5 OVER) >= P(O/U 49.5 OVER) >= P(O/U 50.5 OVER)
```

If a higher threshold is priced above a lower one, the ladder is broken -- pure structural arbitrage.

### Why Esports Kill Markets Are Especially Mispriced

1. **Narrow thresholds** -- Dota 2 kill ladders use 1.0 increments (47.5, 48.5, 49.5) creating many adjacent rungs where violations can form
2. **Retail trades in silos** -- most users view each O/U line independently, not the full ladder
3. **No market maker enforcement** -- unlike sportsbooks, Polymarket has no central entity maintaining ladder consistency
4. **Game-specific volatility** -- Dota 2 average kills per game is ~55 with high variance, meaning the ladder spans a wide range of plausible outcomes
5. **Multi-game series** -- BO3 matches create separate ladders for Game 1, Game 2, Game 3, tripling the surface area for violations

## Signal Logic

1. Discover esports kills O/U markets via keyword search + bulk market fetch fallback
2. Parse each question: extract match_key, game_number, kill_threshold
3. Filter non-esports markets with regex (remove crypto, politics, weather noise)
4. Group into ladders by (match_key, game_number)
5. For each ladder with 2+ points:
   - Sort by kill threshold ascending
   - Check monotonicity: P(O/U X OVER) must decrease as X increases
6. Rank violations by magnitude
7. Trade only violations that pass threshold gates (YES_THRESHOLD / NO_THRESHOLD)
8. Size by conviction (violation magnitude), not flat amount

### Remix Signal Ideas

- **Liquipedia API**: Pull team Elo ratings and recent match history — teams with high-variance playstyles create wider kill distributions, meaning more O/U lines and more violation opportunities
- **Dotabuff / OpenDota API**: Fetch hero pick/ban data and lane matchups for the specific game — aggressive drafts with teamfight heroes predict higher kill totals, letting you weight which side of the monotonicity break to trade
- **Live match data (PandaScore API)**: Stream real-time kill counts during a BO3 — if Game 1 had 60 kills, Game 2 O/U lines should shift up; if the market hasn't adjusted, that's an additional timing edge
- **Map/patch meta analysis**: After major game patches, kill totals shift systematically — track patch notes and historical post-patch kill averages to predict which direction the curve should move

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
| `SIMMER_MIN_VIOLATION` | `0.03` | Min ladder violation magnitude to trigger a trade |

## Edge Thesis

Traditional sportsbooks have professional line-setters who enforce consistency across O/U lines for the same game. Polymarket has no such mechanism -- each kill total O/U market is priced by its own order book with its own liquidity pool. Esports kill markets are particularly vulnerable because:

- Kill thresholds are tightly spaced (1.0 increments), creating many adjacent rungs
- Multi-game series (BO3/BO5) multiply the number of ladders per match
- Esports-specific liquidity is thinner than mainstream sports, widening violations
- New thresholds added mid-match don't inherit pricing from neighbors
- Large directional flow on one threshold doesn't propagate to adjacent ones

This skill treats the kill total O/U ladder as a monotonic probability curve and trades the repair.

## Dependency

`simmer-sdk` by Simmer Markets (SpartanLabsXyz)
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
