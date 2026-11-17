# Pantry Moth Eliminator

**You saw a moth in the kitchen. Now there's webbing in the rice.**

The Indian meal moth is the world's most common household food pest: one
fertilized female seeds ~400 eggs into your dry goods; a warm kitchen
completes a generation in 4 weeks. Most people throw out the visibly
infested bag, see moths "come back" a month later, and fight them for a
year — because the larvae were already pupating in the ceiling corner and
inside the seams of unopened boxes.

This skill turns elimination into a dated, thresholded protocol:

- **Level triage** (mild/moderate/severe) → full staged protocol
- **Disposition engine** — freeze / toss / keep for every food category,
  including the non-obvious (unopened boxes are NOT safe; spices, tea,
  chocolate, pet food are classic hidden nurseries)
- **Kill math** — freeze at −18°C/0°F ≥4 days, or oven 60°C/140F × 30 min
- **Trap plan** — pheromone traps as a *scoreboard* (they catch males
  only), with placement rules
- **Timeline + watch verdicts** — day 7/14/30 thresholds and the 3-zero-
  weeks moth-free declaration, dated from your start date

## Quick start

```bash
python3 scripts/moths.py protocol --level moderate
python3 scripts/moths.py disposition --item "unopened cereal box"
python3 scripts/moths.py timeline --start 2026-10-04 --level moderate
python3 scripts/moths.py watch --start 2026-10-04 --catch-day7 3 --catch-day14 0
```

Stdlib-only Python 3, offline.

## Example

Day 0, moderate infestation, started 2026-10-04:

```
Timeline:
  2026-10-04  +  0d  Pull + freeze/toss + deep clean + traps out
  2026-10-11  +  7d  Trap check 1; repeat crack-vacuum
  2026-10-18  + 14d  Trap check 2 — the verdict point
  2026-11-03  + 30d  first possible 'clean' if 3 zero weeks

watch --catch-day7 3 --catch-day14 0:
  day 7: ON TRACK (tail) — residual males from pre-pull eggs
  day 14: PASS — collapse confirmed
  Earliest moth-free declaration: 2026-11-08
```

`disposition --item "unopened cereal box"` returns the rule people get
wrong: unopened ≠ safe — larvae enter through folded carton seams; freeze
or toss it anyway.

Full biology, kill-method validation, and failure autopsies in
`references/moth-biology.md`.
