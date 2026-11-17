---
name: gym-load-planner
description: Use when lifting weights and wondering what load to use — estimates true 1RM from reps@weight (Epley + Brzycki consensus), builds %-1RM loading tables per goal (strength 80-90%, hypertrophy 65-80%, endurance 50-65%), plans progressive-overload blocks with automatic deload weeks, solves barbell plate math for any plate set, and tracks e1RM trend with next-session load suggestions.
version: 1.0.1
author: Denis Voronin
license: MIT
tags: [strength-training, gym, one-rep-max, progressive-overload, powerlifting, fitness, plate-calculator]
---

# Gym Load Planner

## Overview

The gym has two universal questions: **"how much should I lift?"** and
**"how much did I get stronger?"** Most people answer both by guessing —
they add weight when it feels easy and stall for months.

This skill answers both with arithmetic instead of vibes:

1. **1RM estimation** — Epley (`w × (1 + r/30)`) and Brzycki
   (`w × 36/(37−r)`) formulas, averaged, valid for reps ≤ 12, with a
   range showing the disagreement between the two models.
2. **Loading tables** — exact weights and rep targets per goal from the
   classic %-1RM zones, plus the "rep-max" column (what you could lift
   for 5, 8, 12 …).
3. **Progression planning** — a linear-progression block (novice: +2.5 kg
   on lower-body lifts, +1.25–2.5 kg upper, each session the previous load
   is completed at target reps) and a double-progression block
   (intermediate: fix the weight, add reps 8→12, then raise weight and
   reset reps), each with a **deload week every 4th week (−10 %)**.
4. **Plate math** — exact per-side plate stacks for a target bar weight,
   kg or lb, with remainder warnings when the target isn't loadable.
5. **Progress log** — record sets, watch estimated 1RM trend, and get the
   next session's working loads according to your progression rule.

## When to Use

- "I squatted 100 kg × 8 — what's my 1RM / what weight for 5×5?"
- Starting a program: which loads, how do they progress week to week?
- "Bar + which plates = 92.5 kg per my gym's plate set?"
- Stalled progress: when to switch from linear to double progression?
- Reviewing a training log: is e1RM actually trending up?

**Don't use for:** 1RMs estimated from reps > 12 (formula error grows
fast — treat such estimates as rough), coaching elite athletes (they need
individualized periodization), or medical/rehab loading decisions.

## Quick Start

```bash
# 1RM estimate + full percentage table from a rep max
python3 scripts/gym_load.py one-rm --weight 100 --reps 8

# Training loads for a goal (from known or estimated 1RM)
python3 scripts/gym_load.py table --one-rm 125 --goal strength

# 8-week progressive overload block
python3 scripts/gym_load.py plan --one-rm 125 --goal strength \
    --weeks 8 --increment 2.5 --top-reps 5

# What plates per side for 92.5 kg (20 kg bar)?
python3 scripts/gym_load.py plates --target 92.5 --bar 20
python3 scripts/gym_load.py plates --target 225 --unit lb

# Log sets and get next-session loads
python3 scripts/gym_load.py log add --lift "bench press" --weight 80 --reps 8
python3 scripts/gym_load.py log add --lift "bench press" --weight 80 --reps 10
python3 scripts/gym_load.py log next --lift "bench press" --rule double
```

## The Science in Brief

### 1RM formulas

| Formula | Equation | Best for |
|---|---|---|
| Epley | `1RM = w × (1 + r/30)` | ≤ 10 reps, most lifts |
| Brzycki | `1RM = w × 36 / (37 − r)` | ≤ 10 reps, slightly lower estimates |

The tool reports both plus their mean. When the two disagree by > ~5 %
your rep count is outside the reliable zone — trust it less.

### %-1RM zones by goal

| Goal | %1RM | Reps/set | Rest | Sets |
|---|---|---|---|---|
| Strength | 80–90 % | 3–6 | 3–5 min | 3–5 |
| Hypertrophy | 65–80 % | 8–12 | 1.5–3 min | 3–4 |
| Endurance | 50–65 % | 15–20 | 60–90 s | 2–3 |

Rep-max conversion (Epley inverse): weight for R reps =
`1RM / (1 + R/30)`.

### Progression models

- **Linear progression (novice, ~first 6–12 months):** add a fixed
  increment every session you hit all target reps. Squat/deadlift +2.5 kg,
  bench/row +1.25–2.5 kg. Fails 2–3 sessions in a row → time for the
  intermediate model.
- **Double progression (intermediate):** pick a rep range (e.g. 8–12).
  Work at a fixed weight until you hit the top of the range on ALL sets,
  then add weight (~2.5–5 %) and return to the bottom of the range.
- **Deload:** every 4th week drop working loads ~10 % and reps; the plan
  command schedules this automatically. Deloads are when the adaptation
  you stimulated gets realized.

### Plate math

Greedy largest-plate-first per side; warns if the target is unreachable
with your plates (e.g. 93 kg with 2.5 kg granularity and a 20 kg bar →
you can do 92.5 or 95, not 93).

## Common Pitfalls

1. **Estimating 1RM from high-rep sets.** A 20-rep max estimate can be off
   by 10 %+; the tool flags disagreement but honesty starts with the input.
2. **Skipping deloads.** Fatigue masks fitness; 8 weeks without a down
   week is how linear progression dies at week 6.
3. **Adding weight when reps weren't hit.** The rule is progression
   *contingent on completing the target*; the `log next` command encodes it.
4. **Jumps too big.** +2.5 kg on bench is ~2–3 % — correct. +10 kg is a
   plateau generator.
5. **Testing actual 1RM too often.** Estimate it monthly from a 5–8 rep
   set; true max singles are a skill and a fatigue event, not a metric.

## Verification Checklist

- [ ] one-rm prints Epley, Brzycki, mean, and flags disagreement > 5 %
- [ ] table weights are consistent across zones (strength > hypertrophy > endurance)
- [ ] plan inserts a deload every 4th week at −10 % loads
- [ ] plate stacks load the target exactly, or a nearest-loadable warning appears
- [ ] `log next --rule linear` adds increment only when top reps were completed

## Examples

```
$ python3 scripts/gym_load.py one-rm --weight 100 --reps 8
Epley:    126.7 kg
Brzycki:  123.8 kg
Mean:     125.2 kg   (formulas agree within 2.3% — good)

$ python3 scripts/gym_load.py plates --target 92.5 --bar 20
Per side: 25 + 10 + 1.25 kg  →  total 92.5 kg  ✓
```

Formulas: Epley (1985), Brzycki (1993) — both established exercise-science
1RM predictors. Zones reflect widely used NSCA-style guidelines. Individual
response varies; loads are starting points, not prescriptions.
