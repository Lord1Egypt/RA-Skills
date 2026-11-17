# Load Science Behind Gym Load Planner

## 1. One-rep-max estimation

Two classic formulas, both from exercise science:

- **Epley (1985):** `1RM = w × (1 + r/30)` — the most widely used; slightly
  generous at higher rep counts.
- **Brzycki (1993):** `1RM = w × 36/(37 − r)` — slightly conservative.

Both assume **maximal-effort sets** (you could NOT have done another rep)
and rep counts ≤ 10–12. A set of 8 that stopped 3 reps short of failure
produces a garbage estimate; formulas predict *rep maxes*, not submaximal
work sets.

Accuracy: within ~5–10 % for reps ≤ 10 on most compound lifts. The tool
prints the disagreement between the two formulas — a large spread is a
signal the input is outside the reliable zone.

Rep-max inversion (used for tables): weight for R reps = `1RM/(1 + R/30)`.

## 2. Intensity zones

Widely used NSCA-style guidelines for loading by training goal:

| Goal | Intensity (%1RM) | Reps/set | Sets | Rest |
|---|---|---|---|---|
| Maximal strength | 80–90 % | 3–6 | 3–5 | 3–5 min |
| Hypertrophy | 65–80 % | 8–12 | 3–4 | 1.5–3 min |
| Muscular endurance | 50–65 % | 15–20 | 2–3 | 60–90 s |

Notes:
- Strength is a **skill of producing force**: heavy singles-to-triples at
  85 %+ with long rests; hypertrophy work at 65–80 % builds the cross-section
  that makes strength possible later.
- Volume drives hypertrophy; intensity drives neural adaptation. Programs
  should not blend everything into one moderate zone.
- Accessory/isolation lifts tolerate higher rep ranges (12–20) regardless
  of primary goal.

## 3. Progression models

### Linear progression (novice)
- Add a fixed increment **every session** the target reps are completed:
  squat/deadlift +2.5 kg, bench/overhead press/row +1.25–2.5 kg
  (5 lb / 2.5 lb in lb-land).
- Works for ~6–12 months of consistent training; then recovery can no
  longer keep pace and progress stalls (2–3 consecutive failed sessions
  on the same weight).

### Double progression (intermediate)
- Fix a rep range (e.g. 8–12). Keep the weight until **all sets** reach
  the top of the range, then add ~2.5–5 % and return to the bottom.
- Self-regulating: bad weeks automatically mean fewer reps, not failed
  loads.

### Deloads
- Every 3rd–5th week, cut working loads ~10 % (and/or a set) for a week.
- Rationale: the fatigue-fitness model (Banister fitness-fatigue, Cal Dietz
  triphasic practice) — accumulated fatigue masks expressed fitness. A
  planned down week expresses the adaptation and restores readiness.
- The `plan` command schedules a deload every 4th week automatically.

## 4. Plate math

Per-side loading: `(target − bar)/2`, then greedy largest-first over the
gym's plate inventory. Standard sets:

- kg gyms: 25 / 20 / 15 / 10 / 5 / 2.5 / 1.25 (bar 20 kg; sometimes 25 kg)
- lb gyms: 45 / 35 / 25 / 10 / 5 / 2.5 (bar 45 lb)

With 1.25 kg as the smallest plate, granularity per side is 1.25 kg →
total loadable weights differ by 2.5 kg steps from the bar up. Targets
off-grid (e.g. 93 kg) get the nearest loadable alternative printed.

## 5. Using e1RM as a progress metric

- Track e1RM from your *hardest set* per lift per session; trend over
  weeks, not sessions (daily readiness noise is real).
- A rising e1RM at the same bodyweight = relative strength up — the
  cleanest progress signal for recreational lifters.
- True 1RM testing is a skill event: reserve for the end of a block, after
  a taper, with a spotter — not a weekly ritual.

## 6. Limitations

- Formulas calibrated on healthy, resistance-trained adults; adolescents,
  older adults, and rehab contexts need professional guidance.
- Machines with cams/variable resistance violate the constant-gravity
  assumption — estimate from free weights where possible.
- Estimates are starting points: individual daily readiness varies ±5 %.
