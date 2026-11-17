# Fertility — Conceiving and Avoiding (opt-in)

Load only when `fertility_tracking` is set or she explicitly asks. Everything here is advise-mode: she decides, you compute and explain.

## The Window Itself

- Egg survives 12-24 hours after ovulation; sperm survive up to 5 days in fertile mucus. The biologically fertile window is therefore ~6 days ending on ovulation day (Wilcox) — matching SKILL.md: ovulation −5 through ovulation day.
- Probability is not flat across the window: it peaks the 1-2 days before ovulation and drops sharply after. Conception from intercourse the day after ovulation is unlikely; from 5 days before, possible.
- The calendar estimate (SKILL.md rule 4) locates the window only as well as her cycles are stable. Live signals below override the calendar whenever they disagree.

## Signals, Ranked

| Signal | What it tells you | Protocol |
|--------|-------------------|----------|
| LH surge (OPK) | Ovulation in ~24-36h — best forward predictor | Start testing at predicted ovulation −4 days; test twice daily near the expected surge (surges can last <24h and a once-daily test misses them) |
| Cervical mucus | Peak fertility now — clear, stretchy, egg-white texture; last day of it ("peak day") is ~ovulation | Observe daily, log texture on her terms; arousal fluid and semen residue confound same-day readings |
| BBT | Ovulation already happened — sustained rise of 0.3-0.5 C (0.5-0.9 F when `temperature_unit: fahrenheit`) | Measure immediately on waking, same time daily, after 3+ hours of sleep; mark and discount disturbed readings (alcohol, illness, short sleep). Confirm with 3 consecutive higher days |
| Wearable temperature | BBT-equivalent, algorithm opaque | Treat as confirmation like BBT, never as forward prediction |

## Conceive Mode (`fertility_tracking: conceive`)

- Timing: intercourse every 1-2 days across the fertile window beats trying to hit one perfect day; the highest-probability days are the 2 before ovulation.
- Don't over-optimize: daily scheduling pressure is a known libido killer and the gain over every-other-day is marginal.
- Track BBT shift + positive OPK per cycle: together they confirm ovulation actually occurred, which is the first question a fertility clinic asks.
- Base rates to set expectations honestly: most couples conceive within a year; not conceiving in the first few months is normal, not a signal.
- When to stop tracking and see a clinician (ACOG): 12 months of trying under 35; 6 months at 35 or older; immediately if cycles suggest no ovulation (`irregular.md`) — bring the log, it shortens the workup.

## Avoid Mode (`fertility_tracking: avoid`)

- Be honest about the tiers: calendar-only estimation is the weakest form of fertility awareness. Symptothermal method (mucus + temperature, taught protocol) reaches ~0.4 failures per 100 woman-years in perfect use (Frank-Herrmann); typical use across fertility-awareness methods runs far higher — 2-23 per 100 woman-years depending on method and adherence.
- Conservative window for avoidance: treat as fertile from the first fertile-quality mucus (or predicted ovulation −5, whichever is earlier) until 3 consecutive days past the confirmed temperature shift.
- Do not support calendar-based avoidance when cycles are irregular (>9-day spread), postpartum, perimenopausal, or recently post-pill — the signals and math both degrade. Say so plainly and suggest she discuss methods with a clinician.
- Emergency contraception note: levonorgestrel EC can shift the next period up to a week either way — recompute nothing until the next real Day 1.

## Pregnancy Test Timing

- Test from the first day of the missed period, or 21 days after the sex in question if cycles are too irregular to define "missed."
- Negative test but still no period: retest in one week; two negatives a week apart with no period → late-period chain in `irregular.md`.
- Positive test: congratulate or acknowledge on her cue — never assume which it is. Pain or bleeding with a positive test is an emergency (SKILL.md Red Flags). Ongoing tracking moves to the `pregnancy` skill.

Numbers home: window and signal thresholds here; cycle classification stays in SKILL.md §Classifying.
