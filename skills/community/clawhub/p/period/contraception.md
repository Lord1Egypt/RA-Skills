# Bleeding on Contraception — What Tracking Means on Each Method

On hormonal contraception, bleeding is a method effect, not an ovulatory cycle (SKILL.md rule 7). Keep logging — pattern changes still carry signal — but prediction rules change per method. Set `contraception` in config the moment she names her method.

## Per-Method Rules

| Method | Expected bleeding pattern | Prediction | Watch for |
|--------|---------------------------|------------|-----------|
| Combined pill / patch / ring | Withdrawal bleed on the scheduled break; spotting common in the first 3 months or after missed doses | Bleed timing is schedule math, not cycle math; ovulation back-count suspended | New breakthrough bleeding after months of stability (missed doses? interaction?) |
| Continuous/skipped-break use | No bleed by design — skipping breaks is safe; the monthly bleed has no health function | Nothing to predict | Persistent unscheduled bleeding |
| Progestogen-only pill | Irregular spotting, infrequent bleeding, or none — all normal | None | Pattern change after stability |
| Hormonal IUD (52 mg) | Irregular spotting first 3-6 months, then much lighter; roughly 1 in 5 users has no bleeding at 1 year | None; absent periods are expected, not amenorrhea to flag | Sudden pain or heavy bleeding after a quiet stretch — expulsion/displacement check, clinician |
| Copper IUD | Real ovulatory cycles — full SKILL.md prediction applies | Rules 1-6 apply unchanged | Heavier, longer periods, worst in the first 3-6 months; heavy-flow Red Flags still apply, and this method is the common tracked cause |
| Implant | Unpredictable: no bleeding, infrequent, or prolonged spotting — no pattern to learn | None; refuse politely and explain why | Bleeding plus severe pelvic pain |
| Depo shot | Bleeding decreases with each injection; no bleeding by 1 year is common | None; fertility return lags after stopping (`irregular.md`) | Bleeding restarting late into use |

## What Still Gets Flagged on Any Method

The method changes bleeding, not these:
- Bleeding after sex
- Soaking hourly for 2h+ or clots >2.5 cm (SKILL.md Red Flags)
- New severe pelvic pain
- Positive pregnancy test with pain or bleeding — emergency row
- On the copper IUD only: 90+ days with no period (on hormonal methods absence is expected)

## Emergency Contraception

- Levonorgestrel EC shifts the next period up to a week in either direction. Log the EC date, widen the expected range, and predict nothing firm until the next real Day 1.
- More than 7 days late after EC → pregnancy test (`fertility.md` timing).

## Starting and Stopping

- First 3 months on any new hormonal method: spotting is expected — log it, flag nothing unless a Red Flags row fires.
- Stopping any method → the post-pill reset in `irregular.md`: prior on-method "cycles" say nothing about her natural baseline; set `prediction_window: 3` and rebuild.
- Method choice itself (which pill, IUD vs implant) is a clinician conversation — provide her bleeding log as input, not a recommendation.
