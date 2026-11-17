---
name: period
slug: period
version: 1.0.3
description: >-
  Tracks menstrual cycles, logs symptoms, and predicts periods, ovulation, and fertile
  windows from her own logged data. Use when a period starts, is late, or is missed, when
  logging cramps, PMS, PMDD, mood, spotting, or flow, when asking whether a cycle is
  irregular, heavy, or too long, when tracking basal temperature, LH tests, or cervical
  mucus to conceive or avoid pregnancy, when bleeding changes on the pill, IUD, or implant,
  or when cycles shift in perimenopause, postpartum, or after stopping contraception. Not
  for prenatal tracking once pregnancy is confirmed.
homepage: https://clawic.com/skills/period
changelog: "Full coverage pass: deeper guides, situation-named files, and per-user configuration"
metadata:
  clawdbot:
    emoji: "🩸"
    displayName: Period Tracker
    configPaths:
    - ~/Clawic/data/period/
---

All data lives locally in `~/Clawic/data/period/` (`log-template.md` for file formats, `setup.md` on first use). If you have data at an old location (`~/period/` or `~/clawic/period/`), move it to `~/Clawic/data/period/`. Never sync it, never mention cycle content outside a session she opened. This skill acts directly (logs, predicts, flags); it advises, it does not diagnose.

## Configuration

User-dependent variables. Defaults apply until the user states a preference; store them in `~/Clawic/data/period/config.yaml`.

| Variable | Type | Default | Effect |
|---|---|---|---|
| fertility_tracking | off \| conceive \| avoid | off | Gates Fertility Signals and `fertility.md`; `conceive` centers timing on the window, `avoid` adds buffer days and effectiveness caveats |
| contraception | text (method) or none | none | Hormonal methods reroute prediction to `contraception.md`; the ovulation back-count (rule 4) is suspended on suppressive methods |
| prediction_window | number (3-6 cycles) | 6 | How many recent cycles feed the median (rule 2); reset to 3 after a life change (postpartum, stopping the pill) invalidates the old baseline |
| temperature_unit | celsius \| fahrenheit | celsius | Converts BBT thresholds in `fertility.md` (0.3-0.5 C = 0.5-0.9 F) |
| heads_up_days | number (0-7) | 0 | 0 = predictions only when asked; N = if she opens a session within N days of a predicted start, mention it once |

Preference areas to record as she reveals them:

- **wording** — plain vs clinical vocabulary and how she refers to her own body; affects every reply, never the stored data
- **flow scale** — how she reports flow (light/medium/heavy, product counts, or mL); affects logging prompts and how her reports map to the heavy-flow thresholds
- **proactivity** — surface pattern changes unprompted vs only on request; Red Flags are always surfaced regardless
- **off-limits topics** — subjects never to raise unprompted (fertility, weight, pregnancy); recorded once, honored everywhere

## When To Use

- She reports a period start, flow, or symptom and wants it recorded
- She asks when her next period, fertile window, or ovulation is likely
- She wants a cycle classified (regular, irregular, heavy, long) against real thresholds, not "28 days"
- Her period is late or missed and she wants to reason through it
- Bleeding changed after starting or stopping contraception, or cycles are shifting (teens, postpartum, perimenopause)
- Not for: prenatal tracking after a confirmed pregnancy, diagnosing PCOS/endometriosis, or choosing a contraception method — route to `pregnancy` or a clinician

## Quick Reference

| Situation | Play |
|-----------|------|
| "My period started" | Log Day 1 = first day of full flow (not prior spotting). Timestamp it. |
| "When is my next period?" | >=3 logged cycles: last Day 1 + median cycle length, with range (§Prediction Math). Fewer: wide estimate, keep logging. |
| "Am I regular?" | Spread of logged cycles: <=9 days = regular; >9 = irregular (FIGO) — a description, not a defect. |
| "My period is late" / no period | Days late against HER range first, then the late-period chain in `irregular.md`. |
| "When can I get pregnant?" / avoiding | Fertile window = ovulation −5 through ovulation day. Opt-in only → `fertility.md`. |
| "Is this too heavy / too long?" | Bleeding >8 days, soaking hourly for 2h+, or clots >2.5 cm → Red Flags row. |
| Cramps, period pain | Log against cycle day; relief playbook and the endometriosis pattern → `pain.md`. |
| Mood swings, "is this PMS?" | Log; luteal-pattern assessment → `pms-pmdd.md`. Never attribute her mood to her cycle before she does. |
| On the pill, IUD, implant, shot | Bleeding is method-driven, not a cycle; per-method rules → `contraception.md`. |
| Teens, postpartum, post-pill, perimenopause | Different normal ranges and resets → `irregular.md`. |
| "Delete my data" / "who sees this?" | Confirm scope, delete, verify, report → `privacy.md`. |
| Anything else | Log what she shared, check Red Flags, answer from her baseline — never from textbook averages. |

Depth on demand: `symptoms.md` trackable catalog and phase clustering · `fertility.md` conception and avoidance signals · `irregular.md` late, missed, and shifting cycles · `contraception.md` bleeding on each method · `pain.md` cramp relief and escalation · `pms-pmdd.md` cyclical mood tracking · `privacy.md` storage, export, deletion · `log-template.md` data formats · `setup.md` first use.

## Core Rules

1. **Day 1 is the first day of full flow, not spotting.** Prediction math anchors on Day 1; counting spotting as Day 1 shifts every downstream date by 1-2 days.
2. **Predict from her median, never a textbook constant.** `next start = last Day 1 + median(last prediction_window cycle lengths)`. Median resists the one outlier cycle a mean would drag. Below 3 cycles there is no baseline: say so.
3. **Attach a range, not a point.** `range = ± (longest − shortest)/2` over the window, rounded up. A woman with cycles 26-34 gets "predicted day X, plus or minus 4 days," never a false-precision single date.
4. **Ovulation is back-counted, not forward-counted.** `ovulation ≈ next predicted period − 14`. The luteal phase is relatively fixed (~10-16 days); the follicular phase is what varies. This is why long cycles delay ovulation but keep the luteal length.
5. **Classify against FIGO ranges (§Classifying), not against 28.** 24-38 day cycles are normal frequency; irregular is a description, not a defect. PCOS and perimenopause produce genuinely long cycles.
6. **Flag against HER baseline once >=3 cycles set it.** A sustained shift of >9 days in cycle length, or any Red Flag signal, is worth surfacing. A single off cycle is noise, not a flag.
7. **On hormonal contraception, bleeding is not a cycle.** Withdrawal and breakthrough bleeds are method effects, not ovulation — never run rules 2-4 on them (`contraception.md`).

## Prediction Math (worked)

Logged Day 1 dates: Jan 3, Jan 31, Feb 26, Mar 27. Cycle lengths: 28, 26, 29 days.
- Median = 28. Shortest 26, longest 29 → half-spread = (29−26)/2 = 1.5, round to 2.
- Next period = Mar 27 + 28 = **Apr 24, plus or minus 2 days**.
- Ovulation = Apr 24 − 14 = **~Apr 10**. Fertile window = Apr 5 through Apr 10.

If she has only 2 cycles, report "roughly late April, still learning your pattern" and refuse a hard date. Recompute the median every new cycle. The window is the last `prediction_window` cycles (default 6) and never includes cycles older than 12 months — storage keeps everything (her data), but stale drift never re-enters the estimate.

## Classifying A Cycle (FIGO thresholds)

| Axis | Normal | Outside normal |
|------|--------|----------------|
| Frequency (Day 1 to Day 1) | 24-38 days | <24 frequent; >38 infrequent |
| Regularity (spread over 12 cycles) | <=9 days | >9 days = irregular |
| Duration (days of bleeding) | 2-8 days | >8 prolonged; <2 very short |
| Flow | soaks a normal pad/tampon in 3-6h | hourly for 2h+, clots >2.5 cm, or >80 mL/cycle = heavy |

These are adult ranges; adolescent and perimenopausal normals differ (`irregular.md`). Irregular by these axes is common with PCOS, perimenopause, thyroid issues, or high stress. Report the classification; do not name the cause.

## Fertility Signals (opt-in only)

Enable only when `fertility_tracking` is set or she explicitly asks. Three confirming signals, ranked by predictive value:
- **LH surge (ovulation predictor kit):** positive means ovulation in ~24-36 hours. Best forward predictor.
- **Cervical mucus:** clear, stretchy, egg-white texture marks peak fertility (the 1-2 days before ovulation).
- **Basal body temperature:** a sustained rise of 0.3-0.5 C confirms ovulation already happened — retrospective, so it verifies a cycle but cannot predict the current one.
Cross-check the calendar estimate (rule 4) against these; when they disagree, live signals win. Protocols, conceive/avoid modes, and test timing: `fertility.md`.

## Red Flags

Anything in this table suspends prediction and coaching: surface it plainly and route to a clinician.

| Signal (observable) | Suspicion | Action |
|---------------------|-----------|--------|
| Soaking a pad/tampon hourly for 2h+, or clots >2.5 cm | Heavy menstrual bleeding, anemia risk | Flag now; suggest same-week clinical review |
| Bleeding >8 days, or between periods, or after sex | Prolonged/intermenstrual bleeding | Flag; recommend evaluation |
| No period for 90+ days (not pregnant, not on suppressive contraception) | Secondary amenorrhea | Flag; recommend evaluation |
| Any bleeding 12+ months after periods stopped | Postmenopausal bleeding | Urgent: always evaluated, clinician-first |
| Pain that OTC relief does not touch or that stops daily activity | Possible endometriosis/other | Flag; recommend evaluation (`pain.md`) |
| Sudden severe one-sided pelvic pain, or pain/bleeding with a positive pregnancy test | Ectopic pregnancy or ovarian torsion | Emergency: same-day care, stop routine tracking |
| High fever with rash, vomiting, or faintness during tampon/cup use | Toxic shock syndrome | Emergency: remove product, immediate care |
| Bleeding during a known pregnancy | Obstetric emergency risk | Emergency guidance first, then stop routine tracking |
| Premenstrual thoughts of self-harm | Severe PMDD pattern | Crisis resources now, not tracking (`pms-pmdd.md`) |

## Output Gates

Before answering a cycle question, verify:

- Day 1 anchored on full flow, not spotting?
- Every prediction carries a range computed from her spread, not a bare date?
- What she just reported checked against the Red Flags table?
- Comparing against her baseline, not a textbook 28?
- If `contraception` is a hormonal method, did `contraception.md` rules replace ovulation math?
- Mood or symptoms not attributed to her cycle unless she drew the link first?
- Fertility content gated on `fertility_tracking` or an explicit ask?

## Traps

| Trap | Why it fails | Do instead |
|------|--------------|------------|
| Assuming a 28-day cycle to predict | Her follicular phase varies; a 34-day cycle ovulates ~day 20, not 14 | Back-count 14 from her predicted next period (rule 4) |
| Predicting from 1-2 cycles | No stable baseline; a false hard date erodes trust when it misses | Log without predicting until >=3 cycles, then predict with a range |
| Using the mean cycle length | One 45-day stress cycle skews it upward | Use the median (rule 2) |
| Attributing her mood to her cycle | Correlation she has not endorsed feels like being told how she feels | Log the symptom against the day; let her draw the link |
| Calling irregular cycles "broken" | 60+ day cycles are normal in PCOS/perimenopause | Classify with FIGO axes; irregular is a description |
| Counting spotting as Day 1 | Shifts every predicted date 1-2 days | Day 1 = first full flow only |
| Treating a pill withdrawal bleed as a period | It is hormone withdrawal on the pill schedule, not ovulation | Log it as method bleeding; rules in `contraception.md` |
| Jumping from "late" to "pregnant" | Stress, illness, and travel delay ovulation and stretch the whole cycle | Run the late-period chain in `irregular.md`; test timing lives there |
| Volunteering predictions or fertile days unprompted | Unsolicited fertility content reads as surveillance | Only on request, or within `heads_up_days` if she set it |

## Where Experts Disagree

- **Cycle syncing (training/diet by phase).** Popular, but generic phase plans rest on weak evidence. Default: her own logged patterns beat any template; offer phase framing only if her data shows the pattern.
- **Fertile window width.** Calendar-only estimates are the weakest; symptothermal confirmation narrows honestly. Default: calendar for orientation, live signals for decisions — and say which one an answer is based on.
- **BBT in the wearable era.** Manual BBT is fussy but interpretable; wearable temperature detects the shift with opaque algorithms. Default: treat wearables as BBT-equivalent confirmation, never as forward prediction.

## Related Skills

More Clawic skills, get them at https://clawic.com/skills/period (install if the user confirms):
- `symptoms` — general (non-cycle) symptom tracking and doctor-visit prep
- `pregnancy` — once a pregnancy is confirmed and tracking shifts to prenatal
- `doctor` — turn flagged signals into a structured question list for an appointment
- `health` — longitudinal wellness habits beyond the cycle

## Feedback

- If useful, star it: https://clawic.com/skills/period
- Latest version: https://clawic.com/skills/period

Part of [Clawic](https://clawic.com), the verified skill library. Get this skill: https://clawic.com/skills/period.
