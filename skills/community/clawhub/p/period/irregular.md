# Irregular, Late, and Shifting Cycles

Different life stages have different normals. Classify against the right baseline before calling anything irregular — and remember irregular is a description, not a defect (SKILL.md rule 5).

## The Late-Period Chain

Work in order; each step can end the conversation.

1. **Late against HER range, not 28.** Late = past `predicted date + half-spread` (SKILL.md rule 3). A day past the textbook date but inside her own range is not late — say so and stop.
2. **Pregnancy possible?** If yes and she wants to know: test timing rules in `fertility.md` (first day of missed period, or 21 days after the sex in question). Never assume which result she is hoping for.
3. **One-off disruptors.** Stress, illness with fever, travel across time zones, rapid weight change, new medication, a big training block — all delay OVULATION, and the luteal phase stays ~10-16 days (rule 4), so the whole cycle stretches. One stretched cycle after a disrupted month is expected; log it, exclude nothing, wait for the next Day 1.
4. **Second consecutive odd cycle** → sustained-shift check (rule 6) and the sections below for a matching life-stage pattern.
5. **90+ days with no period** (not pregnant, not on suppressive contraception) → Red Flags row: secondary amenorrhea, recommend evaluation.

## Teens and First Years (post-menarche)

- Irregularity in the first 1-2 gynecologic years is the norm, not a problem: many early cycles are anovulatory. Adolescent normal is 21-45 days (ACOG); adult FIGO ranges apply roughly 3 years post-menarche.
- Still worth attention at any age: bleeding >8 days, soaking hourly, or no period for 90+ days (SKILL.md Red Flags).
- Prediction: use wider ranges and say the baseline is still forming; a teen's median stabilizes late, so never present early estimates as reliable.

## Postpartum

- Not breastfeeding: ovulation can return as early as ~6 weeks — before the first period, so "no period yet" is not contraception.
- Exclusively breastfeeding: lactational amenorrhea suppresses ovulation ~98% effectively only while ALL LAM criteria hold — under 6 months postpartum, no period yet, exclusive round-the-clock breastfeeding. Any criterion breaks, the protection ends.
- First cycles back are often anovulatory and erratic. Treat prior history as expired: set `prediction_window: 3` and rebuild the baseline from scratch.

## Stopping the Pill (or any hormonal method)

- Cycles typically resume within 3 months of stopping. No period by 3-6 months post-stop → evaluation (the Red Flags 90-day clock starts at the first missed expected period, not at the stop date).
- The pill masks, it does not fix: pre-pill irregularity returns. Cycles logged on the method say nothing about the natural baseline — reset `prediction_window: 3`.
- After the depo shot specifically, ovulation can lag many months after the last injection (median near 10 months) — a long gap here is expected, not amenorrhea to flag.

## Perimenopause

- Staging markers (STRAW+10): a persistent difference of >=7 days between consecutive cycle lengths marks the early transition; gaps of >=60 days mark the late transition; 12 months with no period = menopause.
- Any bleeding after those 12 months is the postmenopausal Red Flags row — urgent, always evaluated.
- Track alongside cycles: hot flashes, night sweats, sleep disruption — they date the transition better than cycle length alone.
- Prediction degrades honestly here: widen ranges, drop hard dates, and say why. Never keep issuing confident predictions against a shifting baseline.

## PCOS Pattern

- The trackable pattern: cycles chronically >38 days or fewer than ~9 periods a year, often with acne, excess facial/body hair, or scalp-hair thinning (`symptoms.md`).
- Diagnosis (Rotterdam criteria) needs a clinician — labs and ultrasound, 2 of 3 criteria. Your job: surface the pattern, hand over clean cycle data, never name the diagnosis.
- Long PCOS cycles can still ovulate — late and unpredictably. Calendar fertility math is unreliable here; live signals only (`fertility.md`), and say the confidence is low.

## Energy Deficit and Overtraining

- Missing periods during heavy training with low fueling is functional hypothalamic amenorrhea (the RED-S pattern) — a health signal with bone-density consequences, never a fitness milestone. If she frames it as convenient, state the risk once, without lecturing.
- Reversible with restored energy availability; route to a clinician plus the 90-day Red Flags row when it persists.

## Thyroid and Medications

- Both hyper- and hypothyroidism shift cycle length and flow; so can antipsychotics, chemotherapy, and some antiepileptics. You track the change; the workup names the cause. When a sustained shift coincides with a new medication, put that fact in the doctor-visit summary (`privacy.md`).
