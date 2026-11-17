# Hospital Discharge Planner

**Discharge day moves a patient from 24/7 monitored care to a home plan
decided in a 15-minute conversation. ~15% are readmitted within 30 days
— and the preventable part is almost always a question nobody asked
before the wheelchair reached the lobby.**

Every family eventually sits in a discharge suite holding a stack of
papers, "follow-up will call you," and a med list rewritten twice that
week. This skill is the patient-advocacy instrument for that day: the
7-question audit that catches unsafe discharges before signing, the
paperwork decode (AVS vs NOF vs MOON), the Medicare mechanics that
decide thousands of dollars (observation vs inpatient, the 3-night SNF
rule, day-21 coinsurance cliff, the free home-health lane nobody
offers), the 72-hour landing-zone build, and the caregiver handoff
card that stops plan-by-folklore.

## What it does

- **`audit`** — the 7 questions for the discharge order: meds
  reconciled line-by-line, follow-up BOOKED (not "will call"),
  equipment ordered AND trained, red flags with numbers, orders in
  writing, named responsible clinician, destination actually ready.
- **`paperwork`** — decodes the document stack and what each is for;
  the status-check question that protects SNF coverage.
- **`postacute`** — setting decision with the real math: home-with-help
  + $0 home health vs SNF (3-night rule flag, day 21–100 coinsurance,
  therapy-plateau pivot) vs IRF's 3-hour bar.
- **`landing`** — the 72-hour plan: med times-grid, floor setup for the
  REAL mobility, honest coverage-grid math from your help hours,
  red-flag sheet, first-follow-up logistics.
- **`handoff`** — prints the one-page caregiver card: meds+times,
  allergies, red-flag numbers, code status — for every caregiver,
  family or hired.

## Quick start

```bash
python3 scripts/discharge_planner.py audit
python3 scripts/discharge_planner.py paperwork
python3 scripts/discharge_planner.py postacute --nights 3 --setting home-with-help
python3 scripts/discharge_planner.py landing --help-hours 6 --floors 1
python3 scripts/discharge_planner.py handoff --patient "Mom 78, hip" \
    --contact "Ana (daughter) 555-0100"
```

Stdlib only, offline, no accounts. Patient-advocacy information, not
medical advice — when the clinical team says stay, stay; this tool is
for the administrative handoff around their medicine.

MIT © Denis Voronin
