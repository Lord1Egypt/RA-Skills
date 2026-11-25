# Household Illness Containment

**Problem.** One kid brings norovirus home Friday; by Wednesday the
parents, the sibling, and the grandparent are down. Households run
smoke detectors but no containment protocol — they share the bathroom,
the hand towel, and the doomed cook shift. The knowledge that stops
household spread is pathogen-specific and counterintuitive (alcohol
hand sanitizer does NOT kill norovirus; bleach dilutions and contact
times matter; food handlers carry a 48–72 h extra clock), and nobody
recites it correctly while holding a bucket at 2 AM.

**What it does.** `scripts/containment_planner.py` from an illness +
first-symptom date prints a dated, illness-specific protocol:

- **phase + exposure-watch window**: where today sits on the course
  and the incubation band in which everyone else is on the clock;
- **pathogen-matched disinfection**: norovirus-class gets exact bleach
  math (¾ cup/gallon ≈ 5000 ppm for vomit events, ⅓ cup ≈ 1000 ppm
  routine, ≥1–5 min contact, mixed fresh) + the quat/sanitizer
  failure warning; enveloped viruses get the simple route;
- **house rules**: sick room, shared-bathroom rotation (sick-last +
  bleach pass, per-person towels, capped toothbrushes), kitchen,
  laundry (hot + no shaking), dishes;
- **return clocks** (fever-free 24 h / 48 h post-norovirus /
  food-handler override / 24 h antibiotics) dated, condition-based;
- **high-risk routing** (infant/pregnant/65+/immunocompromised),
  illness-specific red flags, and the one-store-run containment kit.

**Why broadly useful.** US households absorb tens of millions of
norovirus, flu and COVID cases a year; household secondary attack
rates of 10–40% mean the second through fifth cases are largely
preventable with five boring rules applied for the right days with
the right chemistry. This is the protocol nobody has taped inside the
bathroom cabinet.

**Example.**

```bash
python3 scripts/containment_planner.py --illness norovirus \
    --first-symptom 2026-11-22 --today 2026-11-24 \
    --shared-bathroom --food-handler
# → day 2/ACUTE, exposure watch through 2026-11-24, bleach 5000 ppm
#   recipe, bathroom rotation, 48-72 h food-handler return override.
```

Educational tool from public-health guidance; not medical advice —
clinician, school policy and local health rules outrank the script.
MIT license.
