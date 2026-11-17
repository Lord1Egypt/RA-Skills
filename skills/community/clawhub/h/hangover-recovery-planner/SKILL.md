---
name: hangover-recovery-planner
description: Use when someone drank too much and needs an evidence-based recovery plan, or mid-session wants to know if the next drink is worth it — Widmark BAC tracking, fluid/electrolyte deficit math from actual drinks consumed, congener load scoring, staged rehydration/food/light/sleep protocol, symptom-to-mechanism router, medication warnings (acetaminophen, NSAIDs), and red flags that mean ER not electrolytes.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [hangover, alcohol, recovery, hydration, bac, harm-reduction, health]
---

# Hangover Recovery Planner

The hangover is not one condition — it's at least six mechanisms
stacked: diuresis-driven dehydration (ethanol suppresses vasopressin),
acetaldehyde load, slow methanol metabolism (its byproducts are worse),
gastritis, REM-destroyed sleep, and a genuine inflammatory response.
Each wants a different countermeasure, and the folk canon is full of
backfires: hair-of-the-dog measurably delays recovery, acetaminophen
adds a hepatotoxic load to a liver already oxidizing ethanol, and
"sweating it out" adds dehydration to dehydration.

This skill turns "I drank X over Y hours, I weigh Z" into: current BAC
estimate and time-to-zero, fluid and sodium deficit from the actual
ethanol dose, a staged hour-by-hour protocol, a symptom router that
names the mechanism behind each complaint, medication warnings, ER red
flags, and a personalized next-time card.

## When to Use

- Morning after: full recovery plan from session facts
- Mid-session: `drink` verdict — is the next one worth it?
- Fluid math only: `rehydrate` for the water/electrolyte targets
- Recurring hangover anxiety or flushing: ALDH2 flag explanation
- Planning a big night: run `plan` beforehand to see the pacing math

**Don't use for:** alcohol poisoning (that's the red-flag section —
call emergency services), or as a drinking encouragement tool; the
next-time card exists to reduce dose, not rationalize it.

## The Physics (what the math is doing)

| Step | Model |
|---|---|
| Ethanol dose | drink-type table: grams of ethanol per serving (US standard = 14 g) |
| Peak BAC | Widmark: grams ÷ (weight × r), r = 0.68 M / 0.55 F, per-mille ÷ 10 = %BAC |
| Current BAC | peak − 0.015%/h average elimination (range 0.010–0.020; zero-order kinetics) |
| Fluid deficit | 10 mL net loss per gram ethanol, minus water consumed during |
| Rehydration | 1.5 × deficit over 4–6 h (chugging just produces urine) |
| Sodium | ~0.7 g/L rehydration fluid (1.0 if sweating — dancing/heat) |
| Congener score | per-type index 0 (vodka/seltzer) – 4 (brandy, fortified wine); ≥2.5 avg = dark, worse per gram |

## Commands

```bash
# morning after: 4 craft beers + 3 whiskeys, 80 kg male, started 11h ago
python3 scripts/recovery_planner.py plan \
  --drinks "craft-beer:4,whiskey:3" --weight 80 --sex male \
  --start 2026-10-20T21:00 --water-during 2

# mid-session verdict
python3 scripts/recovery_planner.py drink --drinks "wine:3" \
  --weight 62 --sex female --start 2026-10-21T20:00

# fluid math only
python3 scripts/recovery_planner.py rehydrate --drinks "beer:6" --water-during 1
```

## Output Sections

1. **SESSION** — ethanol grams, standard-drink count, congener index
2. **BAC** — estimate now, drive verdict, hours-to-zero
3. **FLUIDS** — deficit, rehydration volume, sodium target
4. **STAGED PLAN** — NOW / +30-60m / +1-2h / +2-4h / sleep / avoid
5. **SYMPTOM ROUTER** — headache, nausea, shakes, wired-exhaustion,
   flushing → mechanism + what actually helps
6. **RED FLAGS** — the ER list
7. **NEXT TIME** — personalized pacing, congener, hydration, food advice

## Common Pitfalls

1. **Trusting the BAC number as legal truth.** Widmark is a population
   average ±25%; food, medication, and tolerance shift it. Never use
   it to decide "legal to drive" — only "definitely not".
2. **Acetaminophen after drinking.** Both compete for CYP2E1; the
   combination generates the hepatotoxic NAPQI metabolite at higher
   rates. If a painkiller is needed: ibuprofen WITH food, after
   rehydration, at label dose — and the plan says so.
3. **Hair of the dog.** Adding ethanol prioritizes ethanol metabolism
   and directly delays methanol clearance into formaldehyde/formate —
   the actual biochemical mechanism behind the temporary relief.
4. **Chugging water.** Rapid plain-water loading suppresses ADH further
   and produces urine; the plan's 4–6 h sip schedule exists for a
   reason. Add sodium or it doesn't stay.
5. **Coffee first.** Caffeine is a mild diuretic on a dehydrated
   system and masks fatigue without fixing it. After rehydration,
   fine — as a substitute, counterproductive.
6. **Ignoring the every-time flush.** Recurrent flushing/tachycardia
   suggests ALDH2 deficiency (≈40% of East Asians): acetaldehyde
   accumulates and the cancer risk association is established. The
   symptom router flags it every time because it matters.

## Verification Checklist

- [ ] BAC section read before any driving/machine decision (and
      ignored in the permissive direction)
- [ ] Rehydration target spread over hours, with sodium, not chugged
- [ ] No acetaminophen; NSAIDs only with food after fluids
- [ ] Red-flag list checked against actual symptoms
- [ ] Nap capped at 20 min before 15:00 to protect night sleep

## References

- `references/mechanisms.md` — the six mechanisms, evidence grades for
  each countermeasure, drink congener table, ALDH2 details, and the
  CAGE/AUDIT-C screening question for when this tool is used weekly.
