---
name: polymarket-24h-nba-game-structure-trader
description: Trades structural inconsistencies across correlated NBA game markets on Polymarket by grouping moneyline, spread, O/U (full-game and 1H), and 1H moneyline markets for the same game and detecting cross-market mispricings including monotonicity violations, 1H-vs-full divergences, and spread-moneyline directional conflicts.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: 24h NBA Game Structure Trader
  difficulty: advanced
---

# 24h NBA Game Structure Trader

> **This is a template.**
> The default signal detects structural inconsistencies across correlated NBA game markets -- remix it with additional sports, league-specific heuristics, or live odds feeds.
> The skill handles all the plumbing (market discovery, game grouping, cross-market checks, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

Polymarket lists multiple correlated markets for each NBA game:

- **Moneyline**: "Clippers vs. Pacers" = 79.7%
- **1H Moneyline**: "Clippers vs. Pacers: 1H Moneyline" = 50.5%
- **Full-game O/U**: "Clippers vs. Pacers: O/U 235.5" = 56.7%, O/U 236.5 = 55.2%, O/U 237.5 = 52%
- **1H O/U**: "Clippers vs. Pacers: 1H O/U 114.5" = 50.5%
- **Spreads**: "Spread: Clippers (-8.5)" = 41%, "1H Spread: Clippers (-5.5)" = 50.5%

Retail trades each market as an isolated bet. But together, these markets form a **structural web** that must be internally consistent.

This skill reconstructs the full game structure and finds where it is **mathematically broken**.

## The Edge: NBA Game Structure Arbitrage

### Inconsistency Type 1: Moneyline vs 1H Moneyline

If the full-game moneyline says a team is an 80% favorite, the 1H moneyline cannot be a coin-flip. The expected 1H advantage is dampened but must exist:

```
If ML_full > 70%, then ML_1h > 50% + (ML_full - 50%) * dampening
```

When the 1H moneyline diverges too far from what the full-game moneyline implies, the 1H market is mispriced.

### Inconsistency Type 2: O/U Monotonicity

Within the same game, the probability of going OVER must decrease as the line increases:

```
P(O/U 235.5 OVER) >= P(O/U 236.5 OVER) >= P(O/U 237.5 OVER)
```

If a higher line is priced above a lower line, the curve is broken -- pure structural arbitrage.

### Inconsistency Type 3: 1H O/U vs Full-Game O/U

At the same line value, the full-game total always exceeds the 1H total, so:

```
P(Full O/U X OVER) >= P(1H O/U X OVER)
```

If a 1H O/U market is priced higher than the equivalent full-game O/U market, the relationship is violated.

### Inconsistency Type 4: Spread vs Moneyline Direction

The spread favorite (negative line) must be the moneyline favorite. If the spread says Clippers (-8.5) but the moneyline says Pacers are favored, the markets contradict each other.

## Why This Works

1. **Retail trades in silos** -- most users view each market independently and do not cross-reference the full game structure
2. **No market maker enforcement** -- unlike sportsbooks, there is no central entity maintaining consistency across related markets
3. **Mathematical, not opinion** -- the violations are provable inconsistencies in the implied game model
4. **NBA-specific density** -- NBA games generate 5-15+ correlated markets per game, creating more surface area for inconsistencies
5. **Rapid line movement** -- NBA spreads and totals move on injury news, creating temporary cross-market divergences

## Signal Logic

1. Discover all NBA-related markets via keyword and team name search
2. Parse each question: extract teams, market type (moneyline/spread/O/U), scope (full/1H), line value
3. Group ALL markets for the same game into a GameGroup
4. For each game with 2+ markets:
   - Check moneyline vs 1H moneyline consistency
   - Check O/U monotonicity within full-game and 1H lines
   - Check 1H O/U vs full-game O/U at matching lines
   - Check spread direction vs moneyline direction
5. Rank inconsistencies by magnitude
6. Trade only inconsistencies that also pass threshold gates (`YES_THRESHOLD` / `NO_THRESHOLD`)
7. Size by conviction, not flat amount

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
| `SIMMER_MIN_INCONSISTENCY` | `0.05` | Min structural inconsistency magnitude to trigger a trade |

## Edge Thesis

Traditional sportsbooks have professional line-setters who enforce consistency across all markets for the same game. Polymarket has no such mechanism -- each market (moneyline, spread, O/U, 1H variants) is priced by its own order book with its own liquidity pool. This creates systematic micro-inconsistencies in the implied game model, especially when:

- Injury news moves the moneyline but not the 1H moneyline
- O/U lines are added at new values without re-pricing existing ones
- Large directional flow on spreads does not propagate to correlated markets
- 1H markets diverge from full-game markets during low-liquidity hours

This skill treats the full game structure as a consistency web and trades the repair.

## Dependency

`simmer-sdk` by Simmer Markets (SpartanLabsXyz)
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
