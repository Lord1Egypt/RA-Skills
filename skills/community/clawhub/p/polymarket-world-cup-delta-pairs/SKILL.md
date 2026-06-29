---
name: polymarket-world-cup-delta-pairs
description: Pair NO-advance with YES-winner legs for the same 2026 World Cup team to trade cross-market mispricing.
metadata:
  author: Alyna + Hermes
  version: "0.1.0"
  displayName: Polymarket World Cup Delta Pairs
  difficulty: intermediate
  simmer:
    links:
      - https://x.com/zETHerka/status/2061162222156460540
---

# Polymarket World Cup Delta Pairs

Strategy source:
https://x.com/zETHerka/status/2061162222156460540

## Thesis

This skill links two related market types for the same team:
- group-stage advancement
- outright World Cup winner

It enters a pair:
- buy **NO** on "team to advance"
- buy **YES** on "team to win World Cup"

The goal is to monetize structural mispricing and event-driven repricing between connected markets.

## What it does

- scans active 2026 World Cup advance + winner markets
- pairs markets by normalized team name
- computes pair economics:
  - `pair_cost = (1 - advance_yes) + winner_yes`
  - settle edge if team fails to advance: `1 - pair_cost`
  - reprice edge if team advances: `(winner_yes + boost) - pair_cost`
- enters only when both edge thresholds pass
- applies spread/slippage safeguards + cooldown + daily budget
- supports `--venue` (`sim`, `polymarket`, `kalshi`)

## Defaults

- dry-run by default
- per leg: `$4` (pair spend = `$8`)
- daily budget: `$30`
- max pairs/run: `2`
- winner repricing boost: `+0.10`
- team universe seeded with 15 national teams (editable via `team_universe`)

## Run

```bash
cd skills/polymarket-world-cup-delta-pairs
python world_cup_delta_pairs.py --config
python world_cup_delta_pairs.py --venue sim
python world_cup_delta_pairs.py --venue sim --live
python world_cup_delta_pairs.py --venue sim --positions
```

## Tune

```bash
python world_cup_delta_pairs.py --set per_leg_usd=5
python world_cup_delta_pairs.py --set winner_reprice_boost=0.12
python world_cup_delta_pairs.py --set min_settle_edge=0.03
python world_cup_delta_pairs.py --set min_cross_gap=0.25
python world_cup_delta_pairs.py --set min_reprice_edge=-0.30
```

## Deterministic spec (Skill Builder style)

### Signal
- Team appears in both advance + winner market sets
- Pair has positive floor in fail-advance and advance+reprice scenarios

### Entry logic
- Buy NO on advance leg and YES on winner leg for same team
- Require both `settle_edge` and `reprice_edge` thresholds

### Exit logic
- v0.1 focuses on disciplined pair entry
- explicit exit rules can be added in future revision

### Market selection
- Active 2026 FIFA World Cup team-advance and outright-winner markets

### Position sizing
- fixed `per_leg_usd` on each leg

### Risk controls
- `max_spread`, `max_slippage_pct`
- `cooldown_hours`
- `max_pairs_per_run`
- `daily_budget_usd`
- optional safeguards (`--no-safeguards` disables)
