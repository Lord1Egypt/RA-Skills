---
name: medicare-enrollment-navigator
description: Medicare enrollment-window engine for people turning 65 or leaving employer coverage — computes the 7-month IEP, the 8-month SEP, GEP fallback dates, and prices the LIFETIME late penalties in dollars (Part B +10% of premium per full 12 months late, Part D +1% of base per month). Dates the 6-month Medigap guaranteed-issue clock and encodes the classic traps — COBRA does not extend the SEP, employers under 20 employees make Medicare primary even while you work, any Part A entitlement freezes HSA contributions.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [medicare, retirement, health-insurance, enrollment, seniors, penalties]
---

# Medicare Enrollment Navigator

Turning 65 comes with a 7-month window most people discover too late, a
penalty structure that compounds **for life**, and a guaranteed-issue
Medigap clock that quietly expires. This skill turns the rules into dated
verdicts with your birth month and your work situation.

## When to trigger
- "I'm turning 65 soon — when do I sign up for Medicare?"
- "I retired / got laid off — how long do I have to enroll?"
- "I'm still working — do I need Medicare now or can I wait?"
- "I think I missed my enrollment window — what does it cost me?"
- "What's this COBRA / HSA / Medigap thing people warn me about?"

## How it works

1. **Collect inputs**: birth month (`YYYY-MM`), and the work situation —
   `--still-working --employer-size N`, `--spouse-covered`,
   `--coverage-ended YYYY-MM` (job/plan end), `--hsa`, and
   `--months-without-drug-coverage N` if drug coverage lapsed.
2. **Run** `scripts/medicare_navigator.py --birth 1961-08 --now 2026-11`.
3. **Window engine** computes the 7-month IEP around the 65th birthday
   month (3 before → 3 after), the 8-month SEP after employer coverage
   ends, or the GEP fallback (Jan–Mar enrollment → July 1 coverage), with
   the coverage-start rule for the month you'd enroll in.
4. **Mode verdict**:
   - working at 20+ employees → **DELAY Part B is safe** (SEP protects
     you) — but enroll in free Part A unless you're on an HSA;
   - working at <20 employees → **ENROLL NOW**: Medicare pays primary
     even while employed, and the employer plan can hang you out;
   - SEP mode → months left on the 8-month clock, or the GEP path plus
     the penalty bill for burning it;
   - IEP mode → pre-IEP / inside / expired, with the penalty math.
5. **Penalty pricing** (lifetime, named in dollars): Part B
   `floor(months_late / 12) × 10%` of the premium — $185 premium, 26
   months late = +20% = $444/yr for life ≈ $8,880 over 20 years; Part D
   `months × 1%` of the base premium, even if you never take a drug.
6. **Medigap clock**: 6 months from your Part B start date — the only
   window where insurers must sell to you without health questions.
7. **Trap checklist + dated action list** close every run.

## Pitfalls encoded
- **COBRA is not creditable for the SEP**: the 8-month clock starts at
  JOB end, not COBRA end — an 18-month COBRA run can eat the entire SEP.
- **Small employers (<20)**: Medicare is primary even for active
  employees; "but I'm still working" is not protection below 20.
- **HSA freeze**: any Medicare entitlement — including Part A — blocks
  HSA contributions; stop contributing ≥6 months before applying.
- **Part D penalty is silent**: it accrues 1%/month with no drug use at
  all, so "I don't take medications" is exactly how people collect it.
- Penalties are **lifetime**, not one-time — the tool prices them over
  a 20-year horizon (`--estimate-years`).
- Retiree coverage ≠ active-employee coverage: only active employment
  protects the Part B delay.

## Examples

```bash
# Turning 65 in Aug 2026, still working at a 40-person company
python3 scripts/medicare_navigator.py --birth 1961-08 --still-working \
    --employer-size 40 --hsa
# → DELAY B OK + HSA freeze warning + SEP timer

# Laid off in June 2026, birthday Aug 1961
python3 scripts/medicare_navigator.py --birth 1961-08 \
    --coverage-ended 2026-06 --now 2026-11
# → SEP OPEN, 3 months left, Part B effective Dec 2026

# Missed the window entirely: 65 in 2024, no drug coverage since
python3 scripts/medicare_navigator.py --birth 1959-06 --now 2026-11 \
    --months-without-drug-coverage 14
# → GEP Jan 2027 → Part B Jul 2027; +20% B penalty ($8,880/20yr) + D
```

## Output contract
- enrollment window table with real dates (IEP / SEP / GEP)
- one-line mode verdict (ENROLL NOW / DELAY OK / SEP EXPIRED)
- penalty math in dollars: per-month, per-year, lifetime horizon
- Medigap guaranteed-issue window dates
- trap checklist + dated action list + verify-footer for premiums
