---
name: polymarket-48h-sports-line-curve-trader
description: Trades structural mispricings in sports over/under markets by reconstructing the implied probability curve across multiple O/U line values for the same game and detecting monotonicity violations and set-vs-match inconsistencies in tennis.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: 48h Sports Line Curve Trader
  difficulty: advanced
---

# 48h Sports Line Curve Trader

> **This is a template.**
> The default signal is implied O/U curve violation detection across sports markets -- remix it with additional sports, line types, or cross-venue feeds.
> The skill handles all the plumbing (market discovery, curve construction, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

Polymarket lists multiple over/under lines for the same sporting event:

- "Team A vs Team B O/U 5.5" = 50%
- "Team A vs Team B O/U 6.5" = 46%
- "Team A vs Team B O/U 7.5" = 29%

Retail trades each market as an isolated bet. But together, these markets form an **implied probability curve** -- higher totals must always be less likely for the OVER side.

This skill reconstructs that curve and finds where it is **mathematically broken**.

## The Edge: Sports Line Curve Arbitrage

### Violation Type 1: Monotonicity Break

The probability of going OVER a lower line must always be greater than or equal to going OVER a higher line:

```
P(O/U 5.5 OVER) >= P(O/U 6.5 OVER) >= P(O/U 7.5 OVER)
```

If a higher line is priced above a lower line, the curve is broken -- pure structural arbitrage.

### Violation Type 2: Tennis Set vs Match Inconsistency

For tennis, the match total always equals or exceeds the Set 1 total. Therefore:

```
P(Match O/U X OVER) >= P(Set 1 O/U X OVER)
```

If a Set 1 O/U market is priced higher than the equivalent Match O/U market, the relationship is violated.

## Why This Works

1. **Retail trades in silos** -- most users view each O/U line independently and do not cross-reference the full line ladder
2. **No market maker enforcement** -- unlike sportsbooks, there is no central entity maintaining curve consistency across lines
3. **Mathematical, not opinion** -- the violations are provable inconsistencies in the implied distribution
4. **Applies across sports** -- football, basketball, tennis, esports (kills, maps), baseball, hockey

## Signal Logic

1. Discover all sports O/U markets via keyword search (O/U, total goals, total kills, etc.)
2. Parse each question: extract game/match name, O/U line value, scope (set or match)
3. Group into curves by (game, scope)
4. For each curve with 2+ points:
   - Check monotonicity: P(O/U X OVER) must decrease as X increases
   - Check tennis set-vs-match consistency
5. Rank violations by magnitude
6. Trade only violations that also pass threshold gates (`YES_THRESHOLD` / `NO_THRESHOLD`)
7. Size by conviction (violation magnitude), not flat amount

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
| `SIMMER_MIN_VIOLATION` | `0.03` | Min curve violation magnitude to trigger a trade |

## Edge Thesis

Traditional sportsbooks have professional line-setters who enforce consistency across O/U lines for the same game. Polymarket has no such mechanism -- each O/U market is priced by its own order book with its own liquidity pool. This creates systematic micro-inconsistencies in the implied distribution, especially when:

- New O/U lines are added at previously unlisted values
- Large directional flow pushes one line without propagating to neighbors
- Market makers leave gaps during low-liquidity hours
- Tennis set-level markets diverge from match-level markets

This skill treats the O/U line ladder as a probability curve and trades the repair.

## Dependency

`simmer-sdk` by Simmer Markets (SpartanLabsXyz)
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
