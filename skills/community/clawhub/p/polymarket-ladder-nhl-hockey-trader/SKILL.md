---
name: polymarket-ladder-nhl-hockey-trader
description: Trades monotonicity violations in NHL hockey O/U market ladders and spread-vs-total consistency on Polymarket. Each game spawns multiple O/U lines that must be monotonically decreasing — when the ladder is broken, the mispriced line reverts.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: Ladder NHL Hockey Curve Trader
  difficulty: advanced
---

# Ladder — NHL Hockey Curve Trader

> **This is a template.**
> The default signal detects monotonicity violations in NHL hockey O/U ladders and spread-vs-total inconsistencies -- remix it with additional leagues, period-based markets, or live odds feeds.
> The skill handles all the plumbing (market discovery, ladder grouping, monotonicity checks, spread consistency, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

Polymarket lists multiple O/U lines for each NHL game at different totals:

- **Wild vs Bruins**: O/U 4.5 = 62%, O/U 5.5 = 45%, O/U 7.5 = 12%
- **Maple Leafs vs Blues**: O/U 4.5 = 65%, O/U 5.5 = 50%, O/U 6.5 = 30%, O/U 7.5 = 15%
- **Spread markets**: "Spread: Wild (-1.5)" = 42%

These O/U markets form a **ladder** that must be monotonically decreasing:

```
P(O/U 4.5 OVER) >= P(O/U 5.5 OVER) >= P(O/U 6.5 OVER) >= P(O/U 7.5 OVER)
```

Additionally, spread markets constrain the O/U distribution -- a large spread (one team heavily favored) implies a scoring profile that must be consistent with the total.

This skill reconstructs each game's full ladder and trades where it is **mathematically broken**.

## The Edge: NHL Ladder Arbitrage

### Violation Type 1: O/U Monotonicity

Within the same game, the probability of going OVER must decrease as the line increases. If a higher line is priced above a lower line, the curve is broken -- pure structural arbitrage:

```
If P(O/U 5.5 OVER) > P(O/U 4.5 OVER):
    Buy YES on O/U 4.5 (underpriced)
    Buy NO on O/U 5.5 (overpriced)
```

This also checks non-adjacent pairs (e.g., O/U 7.5 vs O/U 4.5) for larger violations that span multiple rungs of the ladder.

### Violation Type 2: Spread-vs-Total Consistency

A large spread implies one team is heavily favored, which shifts the expected scoring distribution:

- If spread >= 2.5 goals, the game is expected to be high-scoring, so P(O/U 5.5 OVER) should be at least 40%
- If spread >= 1.5 goals, P(O/U 4.5 OVER) should be at least 50%

When the O/U curve is inconsistent with the spread, the total is likely mispriced.

## Why This Works

1. **Retail trades in silos** -- most users bet on individual O/U lines without cross-referencing the full ladder
2. **No market maker enforcement** -- unlike sportsbooks, there is no central entity maintaining consistency across O/U lines for the same game
3. **Mathematical, not opinion** -- monotonicity violations are provable inconsistencies in the implied probability distribution
4. **NHL-specific density** -- NHL games generate multiple O/U lines (4.5, 5.5, 6.5, 7.5) plus spread markets, creating a rich surface for inconsistencies
5. **Injury and lineup news** -- goalie changes and late scratches move individual lines without propagating to the full ladder

## Signal Logic

1. Discover all NHL-related markets via keyword search (team names, "NHL", "hockey", "O/U")
2. Fallback to `get_markets(limit=200)` if keyword search yields few results
3. Parse each question: extract (game_key, ou_line) for O/U markets; (game_key, spread_team, spread_value) for spread markets
4. Filter with NHL team regex, exclude non-hockey matches
5. Group O/U markets into ladders by game_key
6. Match spread markets to game ladders by team name overlap
7. For each game ladder with 2+ O/U markets:
   - Check monotonicity: P(OVER) must decrease as line increases
   - Check non-adjacent pairs for larger violations
8. For games with spread + O/U markets:
   - Check spread-vs-total consistency
9. Rank violations by magnitude
10. Trade only violations that also pass threshold gates (`YES_THRESHOLD` / `NO_THRESHOLD`)
11. Size by conviction, not flat amount

### Remix Signal Ideas

- **NHL API live stats**: Use the NHL API (api-web.nhle.com) for live game stats such as shot attempts, Corsi, and Fenwick ratings to predict whether a game is trending over or under before the O/U lines adjust
- **Expected goals (xG) model**: Incorporate MoneyPuck.com expected goals data to build an independent estimate of game totals and compare against Polymarket's implied distribution
- **Historical O/U line movement**: Track historical over/under line movement data from sportsbook APIs to detect when Polymarket's O/U ladder lags behind sharp market moves
- **Weather and arena conditions**: Factor in outdoor game conditions (Winter Classic, Stadium Series), altitude (Denver), and ice quality to adjust scoring expectations -- outdoor games and altitude historically produce different scoring profiles
- **Back-to-back scheduling fatigue**: Use the NHL schedule to identify teams playing on back-to-back nights, which correlates with weaker goaltending and higher totals -- trade the O/U ladder when fatigue is not yet priced in

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
| `SIMMER_MIN_VIOLATION` | `0.05` | Min ladder violation magnitude to trigger a trade |

## Edge Thesis

Traditional sportsbooks have professional line-setters who enforce consistency across all O/U lines for the same game. Polymarket has no such mechanism -- each O/U market (4.5, 5.5, 6.5, 7.5) is priced by its own order book with its own liquidity pool. This creates systematic micro-inconsistencies in the implied scoring distribution, especially when:

- Goalie changes or injury news moves one O/U line but not others
- New O/U lines are added at different totals without re-pricing existing ones
- Large directional flow on one line does not propagate to adjacent lines
- Spread markets move on team news but the O/U ladder does not adjust

This skill treats the full O/U ladder as a consistency curve and trades the repair.

## Dependency

`simmer-sdk` by Simmer Markets (SpartanLabsXyz)
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
