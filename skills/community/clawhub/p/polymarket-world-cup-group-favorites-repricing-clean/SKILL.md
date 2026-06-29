---
name: polymarket-world-cup-group-favorites-repricing-clean
description: Buy pre-tournament World Cup outright favorites and capture group-stage repricing before knockout phase.
metadata:
  author: Alyna + Hermes
  version: "0.1.0"
  displayName: Polymarket World Cup Group Favorites Repricing
  difficulty: beginner
  simmer:
    links:
      - https://x.com/airdrops_io/status/2061459289059754392
---

# Polymarket World Cup Group Favorites Repricing

Strategy source:
https://x.com/airdrops_io/status/2061459289059754392

## Thesis

Before kickoff, group-stage favorites can be underpriced to win the 2026 World Cup.
As the group stage starts and favorites top groups, outright prices can reprice upward.
This skill buys early and (optionally) exits around knockout start to realize repricing.

## What it does

- scans active World Cup 2026 outright-winner markets
- extracts team names from market question text
- estimates fair value as: `fair_yes = current_yes + team_group_stage_boost`
- enters only when `fair_yes - current_yes >= min_edge`
- applies spread/slippage/safeguard/cooldown/daily-budget checks
- supports `--venue` (`sim`, `polymarket`, `kalshi`)
- optional knockout exit workflow (`manage_exits=true`)

## Defaults

- dry-run by default
- max position: `$8`
- daily budget: `$30`
- max trades/run: `3`
- entry window closes at tournament start (`2026-06-11` default)
- optional exit trigger at knockout start (`2026-06-27` default)

## Run

```bash
cd skills/polymarket-world-cup-group-favorites-repricing
python world_cup_group_favorites_repricing.py --config
python world_cup_group_favorites_repricing.py --venue sim
python world_cup_group_favorites_repricing.py --venue sim --live
python world_cup_group_favorites_repricing.py --venue sim --positions
```

## Tune

```bash
python world_cup_group_favorites_repricing.py --set min_edge=0.04
python world_cup_group_favorites_repricing.py --set max_position_usd=10
python world_cup_group_favorites_repricing.py --set daily_budget_usd=50
python world_cup_group_favorites_repricing.py --set tournament_start_utc=2026-06-11T00:00:00Z
python world_cup_group_favorites_repricing.py --set knockout_start_utc=2026-06-27T00:00:00Z
```

## Deterministic spec (Skill Builder style)

### Signal
- Team is a World Cup outright favorite candidate
- Team price lies in candidate range (`min_yes_price`..`max_yes_price`)
- Repricing edge from group-stage boost exceeds `min_edge`

### Entry logic
- Pre-tournament only (`now < tournament_start_utc`)
- Buy YES when edge + quality gates pass

### Exit logic
- Optional: when `now >= knockout_start_utc`, sell YES shares on matching outright markets

### Market selection
- Active markets with World Cup 2026 outright winner intent

### Position sizing
- fixed `max_position_usd` per market

### Risk controls
- `max_spread`, `max_slippage_pct`
- `cooldown_hours`
- `max_trades_per_run`
- `daily_budget_usd`
- optional safeguards (`--no-safeguards` disables)
