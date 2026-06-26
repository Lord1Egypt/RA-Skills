---
name: polymarket-bundle-tennis-set-match-trader
description: Trades cross-market constraint violations in tennis Set 1 Games O/U, Match Games O/U, Total Sets O/U, Set Handicap, and Set/Match Winner bundles on Polymarket. Match total always exceeds Set 1 total so P(Match O/U X OVER) must be >= P(Set 1 O/U X OVER) and Total Sets O/U 2.5 constrains set handicap pricing. Violations are structural arbitrage sized by conviction.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: Bundle Tennis Set-Match Constraint Trader
  difficulty: advanced
---

# Bundle -- Tennis Set-Match Constraint Trader

> **This is a template.**
> The default signal detects cross-market constraint violations between tennis Set 1 O/U, Match O/U, Total Sets O/U, and Set Handicap props -- remix it with live score feeds, surface-specific models, or player fatigue data.
> The skill handles all the plumbing (market discovery, bundle construction, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

Tennis matches on Polymarket spawn multiple correlated prop markets: Set 1 Games O/U, Match Games O/U, Total Sets O/U, Set Handicap, and Set/Match Winner. These props are mathematically constrained -- match total games must always exceed Set 1 total games, and Total Sets O/U 2.5 directly implies the probability of a straight-sets finish which constrains set handicap pricing. When Polymarket prices violate these structural constraints, it is pure arbitrage.

## Edge

Each tennis match prop is priced by its own order book with independent liquidity. Retail traders view each prop in isolation -- they price "Set 1 Games O/U 9.5" and "Match Games O/U 9.5" independently, ignoring the mathematical certainty that Match total >= Set 1 total. Similarly, "Total Sets O/U 2.5 OVER" at 60% means there is a 40% chance of a straight-sets finish, which directly bounds what "Set Handicap -1.5" should price at. No sportsbook would allow these constraints to be violated, but Polymarket has no central line-setter enforcing cross-prop consistency.

## Signal Logic

1. Discover active tennis markets via keyword search + `get_markets(limit=200)` fallback
2. Parse each question: extract match_key, prop_type (set1_ou, match_ou, total_sets, set_handicap, set_winner), line_value
3. Filter non-tennis markets with regex
4. Group into bundles by match_key (normalized player names)
5. Check constraint 1: P(Match O/U X OVER) >= P(Set 1 O/U X OVER) for same line X
6. Check constraint 2: if Total Sets O/U 2.5 > 50% (likely 3 sets), Set Handicap -1.5 should be < P(straight sets)
7. Rank violations by magnitude, trade the most mispriced prop
8. Size by conviction (violation magnitude), not flat amount

### Remix Signal Ideas

- **Live score feeds**: During a match, if Set 1 goes to a tiebreak (7-6), the remaining sets likely follow similar tempo -- adjust Match O/U expectations in real-time
- **Surface-specific models**: Clay court matches average more games per set than grass -- weight violations differently by surface
- **Head-to-head data**: Some player matchups consistently produce straight-set results -- use H2H history to sharpen Total Sets O/U constraint bounds
- **Player fatigue tracking**: Late-round tournament matches after 5-setters create fatigue patterns that shift set handicap probabilities

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
| `SIMMER_MIN_VOLUME` | `3000` | Min market volume filter (USD) |
| `SIMMER_MAX_SPREAD` | `0.08` | Max bid-ask spread |
| `SIMMER_MIN_DAYS` | `1` | Min days until resolution |
| `SIMMER_MAX_POSITIONS` | `8` | Max concurrent open positions |
| `SIMMER_YES_THRESHOLD` | `0.38` | Buy YES only if market probability <= this |
| `SIMMER_NO_THRESHOLD` | `0.62` | Sell NO only if market probability >= this |
| `SIMMER_MIN_VIOLATION` | `0.03` | Min constraint violation magnitude to trigger a trade |

## Edge Thesis

Traditional sportsbooks employ professional line-setters who enforce mathematical consistency across all props within the same match. Polymarket has no such mechanism -- each prop is priced by its own order book. Tennis is especially vulnerable because:

- Set 1 and Match totals have a strict mathematical relationship (match total >= set 1 total)
- Total Sets O/U 2.5 directly implies the probability distribution of set scores, constraining set handicap
- Tennis prop markets are thinner than mainstream match winner markets, widening violations
- Retail traders price each prop independently without cross-checking the bundle
- New props added mid-tournament inherit no pricing from related markets

This skill treats the tennis prop bundle as a system of constraints and trades the repair when any constraint is violated.

## Dependency

`simmer-sdk` by Simmer Markets (SpartanLabsXyz)
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
