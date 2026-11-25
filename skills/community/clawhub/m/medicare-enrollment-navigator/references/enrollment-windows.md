# Medicare Enrollment — Reference

## 1. The problem in one number
Medicare's late-enrollment penalties are **lifetime**, and the windows
that protect you are measured in months. People routinely discover at 67
that a 2-year delay costs +20% of their Part B premium every month for
the rest of their life, or that their COBRA coverage silently burned
their Special Enrollment Period. The rules are simple arithmetic; nobody
does the arithmetic.

## 2. The windows

### Initial Enrollment Period (IEP)
7 months, centered on the 65th birthday month:

| Position | Months |
|---|---|
| 1–3 | the 3 months BEFORE the birthday month |
| 4 | the birthday month itself |
| 5–7 | the 3 months AFTER the birthday month |

**Coverage-start rule**: enroll in months 1–4 → coverage begins the
first day of the birthday month. Enroll in months 5–7 → coverage begins
the first day of the month AFTER you enroll (so waiting inside the IEP
delays coverage month-for-month, even though no penalty is due).

### Special Enrollment Period (SEP)
For people covered by **active employment** (own or spouse's):
- 8 months long, starting when employment **or** group health coverage
  ends — whichever comes **first**;
- enroll in any SEP month → coverage starts the 1st of the next month;
- **no late penalty** while covered as an active employee.

### General Enrollment Period (GEP)
The fallback when IEP and SEP are gone: Jan 1 – Mar 31 every year,
coverage starts July 1. Late-enrollment penalties are assessed at GEP
enrollment.

## 3. The penalties (both lifetime)

### Part B — 10% per full 12 months
- `penalty_pct = floor(months_uncovered / 12) × 10%`
- added to the Part B premium **permanently**;
- "uncovered" = months eligible without Part B and without active
  employer coverage (employer ≥ 20 employees);
- months 1–12 cost nothing — then at month 13 the whole first year
  rounds up to +10%. The runway never resets.

Worked example (premium $185.00, from the script):
- 26 months late = 2 full periods → **+20%** → $37.00/mo → $444/yr →
  **$8,880 over 20 years**.

### Part D — 1% per month
- `penalty = months_without_creditable_coverage × 1% × national_base_premium`
- rounded to the nearest $0.10, added to your plan premium **permanently**;
- accrues even if you take zero prescriptions — "creditable coverage"
  (an employer/other plan at least as good as standard Part D) is what
  stops the clock, not your health;
- at enrollment you'll be asked to prove prior creditable coverage —
  keep the annual notice letters from former employers.

## 4. Medigap guaranteed-issue clock
- 6 months starting the first day of your Part B coverage;
- during it: any Medigap (supplement) policy must be sold to you at the
  standard price, **no health questions, no denial for pre-existing**;
- outside it: most states allow full medical underwriting — diabetics,
  cancer survivors, anyone with a chart can be declined or priced 2–3×;
- some states extend protections (NY, CT, ME, MA are community-rated
  year-round); federal floor is the 6-month clock;
- plan the Part B start so the Medigap window doesn't lapse while you
  shop — it runs from coverage start, not from when you feel ready.

## 5. Primary-payer rules (who pays first)
| Your situation | Primary payer |
|---|---|
| Active employee, employer ≥ 20 | employer plan (delay Part B safely) |
| Active employee, employer < 20 | **Medicare — enroll now** |
| Dependent on spouse's plan, employer ≥ 20 | employer plan (delay OK) |
| Dependent, employer < 20 | Medicare primary |
| COBRA | **Medicare primary** — and COBRA doesn't extend the SEP |
| Retiree coverage | plan may pay secondary; retiree plans are NOT active-employee coverage for SEP/penalty purposes |

## 6. HSA interaction
- Medicare entitlement of any kind — including **Part A alone** — makes
  you ineligible to contribute to an HSA (employer and payroll
  contributions too);
- Part A can be granted retroactively up to 6 months, so the IRS-safe
  practice is to stop HSA contributions **6 months before** applying;
- excess contributions after entitlement: excise tax + amend.

## 7. IRMAA (income-related surcharge)
- Part B and D premiums are surcharged above income thresholds
  (~$106k single / ~$212k MFJ and up, indexed), based on MAGI from the
  tax return **two years prior**;
- life-changing events (retirement, death of spouse) justify an appeal
  with form SSA-44.

## 8. Constants & verification
The script's defaults (Part B standard premium $185.00, Part D national
base $36.78) are recent published figures; both are adjusted annually
and surcharged by IRMAA. Override with `--premium-b` / `--premium-d-base`,
verify current-year values at medicare.gov. Educational tool, not
insurance or tax advice.
