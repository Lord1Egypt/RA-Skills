# Medicare Enrollment Navigator

**Problem.** ~11,000 Americans turn 65 every day, and Medicare's
enrollment rules punish lateness **for life**: Part B gets +10% of the
premium for every full 12 months you're late (forever), Part D gets +1%
of the base per month (forever, even with no prescriptions). The
protective windows are month-sized and full of traps — COBRA does NOT
extend the 8-month SEP, employers under 20 make Medicare primary even
while you're working, and the only guaranteed-issue Medigap window is 6
months long. People learn these rules from a penalty letter.

**What it does.** `scripts/medicare_navigator.py` with your birth month
and work situation:

- **window engine**: your 7-month IEP (with the coverage-start rule per
  enrollment month), the 8-month SEP after employer coverage ends, or
  the GEP fallback with its July 1 start;
- **mode verdict**: working at 20+ employees → delay is safe; under 20 →
  enroll NOW because Medicare pays primary; SEP open / expired; IEP
  pre / inside / missed;
- **penalty pricing in dollars**: 26 months late at a $185 premium =
  +20% = $37/mo, $444/yr, **$8,880 over 20 years** — plus the Part D
  meter;
- **Medigap guaranteed-issue clock** dated from your Part B start;
- **trap checklist** (COBRA, small employers, HSA freeze, IRMAA,
  retiree-coverage illusion) and a dated action list.

**Why broadly useful.** 10,000+ daily birthdays × a system where the
default action (do nothing until 65 + confusion) silently costs 4-5
figures over retirement. The math is simple; nobody has the window
table in their head. Any adult with an aging parent or their own 65th
birthday approaching is in the audience.

**Example.**

```bash
python3 scripts/medicare_navigator.py --birth 1961-08 \
    --coverage-ended 2026-06 --now 2026-11
# SEP OPEN, 3 months left → enroll now → Part B effective Dec 2026,
# Medigap guaranteed issue through Jun 2027, no penalties.
```

Not insurance advice; premium constants are overridable and flagged for
verification at medicare.gov. MIT license.
