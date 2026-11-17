---
name: maternity-leave-planner
description: "Use when a baby is coming (or adopting) and you need to plan parental leave in the US: checks FMLA eligibility, layers state paid-leave programs (CA/NY/NJ/RI/CO/MA/OR/WA/CT/DE/MN/MD...), employer STD and PTO into a week-by-week dated plan, sequences pay sources to maximize paid weeks, and flags job-protection gaps. Solves the 'I have 4 benefit programs and no idea how to stack them' problem."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [parental-leave, fmla, benefits, pregnancy, hr, family, career]
---

# Maternity / Paternity Leave Planner (US)

## Overview

Having a baby in the United States means navigating at least four overlapping systems that almost nobody understands until they're in the middle of it: **FMLA** (federal unpaid job protection), **state paid family & medical leave programs** (a dozen states now have them, each with different lengths, wage-replacement rates and caps), **employer short-term disability (STD)** which may cover the physical recovery weeks, and **PTO** that can plug gaps. The order in which you take these matters enormously — take state bonding leave first in the wrong state and you can burn your best-paid weeks while FMLA protection runs idle; mis-sequence PTO and you lose paid holidays.

The median American parent takes far less leave than they're entitled to, simply because they can't compute what they actually have. This skill turns a handful of inputs (state, due date, pay, employer size, STD plan, PTO balance) into a **week-by-week dated leave plan** with pay source, replacement percentage, and protection status for every week — plus the gap weeks where you're unpaid but protected, and the paperwork deadlines for each program.

## When to Use

- Pregnancy is announced and leave planning starts (ideally in the **second trimester** — notice deadlines are 30 days before leave for FMLA)
- Adopting or fostering (bonding leave applies; recovery/STD does not)
- A partner wants to plan their (often shorter) non-birthing-parent leave
- Reviewing a benefits offer: "how many paid weeks would I actually get here?"
- Diagnosing a past leave that went wrong ("I got 6 weeks paid, was that all?")
- Figuring out intermittent leave for childcare gaps after paid leave ends

**Don't use for:** non-US leave systems (each country has statutory schemes — this skill is US-only), or medical advice about working while pregnant (that's a doctor + HR conversation about accommodations).

## How the Systems Stack

1. **FMLA (federal, unpaid, job-protecting).** 12 weeks per 12-month period for bonding with a new child. Eligibility gate: 12 months employed + 1,250 hours in the last year + 50+ employees within 75 miles of your worksite. Bonding leave must finish within 12 months of birth. Intermittent use allowed with employer agreement. It runs **concurrently** with paid programs — it is not 12 extra weeks.
2. **State paid programs.** Two shapes: pregnancy **disability** (covers physical recovery, typically 6 weeks vaginal / 8 weeks C-section, sometimes plus pre-birth weeks) and **paid family leave** (bonding, typically 6–12 weeks, gender-neutral, also covers adopting parents and partners). States with programs (verify current-year parameters — weeks/caps change annually): CA, CO, CT, DE, MA, MD (started 2026), MN (started 2026), NJ, NY, OR, RI, WA, plus DC. Wage replacement 50–90% with weekly caps.
3. **Employer STD.** If your state has no disability program, an STD plan usually covers the recovery weeks (60–100% of pay, often with a waiting period). Company "parental leave" policies stack on top of everything — always ask HR for the policy document, not a summary.
4. **PTO.** Fills unpaid weeks. Two traps: (a) some states force accrual during leave, some don't; (b) if holidays fall during unpaid leave you may lose them — schedule unpaid weeks around holidays or take them as paid holidays.

**Sequencing doctrine:** recovery first (STD/disability), then paid bonding, then PTO, then unpaid-but-protected FMLA remainder. In states whose family leave job protection exceeds 12 weeks, bonding can extend beyond FMLA without losing your job.

## What to Tell the User to Check (10-minute intake)

1. State of employment (where the paycheck comes from, not where you live — usually)
2. Due date (or adoption placement date) and birth method if known (C-section adds recovery weeks)
3. Gross weekly/biweekly pay + average over the last 12 months (state benefits use averages, some use highest quarter)
4. Employer headcount and your tenure + hours (FMLA gate)
5. STD plan: yes/no, waiting period, % and weeks
6. Any employer-paid parental leave policy: weeks and whether it runs concurrently or atop state programs
7. PTO balance in days
8. Partner's benefits (for the non-birthing parent's plan — run the tool twice)

## Common Pitfalls

1. **Counting FMLA as extra weeks.** It runs concurrently with paid leave. Total protected time is 12 weeks (or more in ~10 states), not 12 + paid weeks.
2. **Missing the 30-day FMLA notice.** Leave foreseeable ≥30 days out requires notice; failing it can delay the start of leave.
3. **Not meeting the state work-history test.** State programs have base-period earnings tests (e.g., wages in 2+ quarters of the base period). Recently job-switched parents sometimes qualify in the *old* state — file where the wages were earned.
4. **Burning PTO first.** In several states you can't double-dip (PTO on top of state benefits), and spending PTO early leaves the FMLA tail unpaid. Sequence PTO into the *unpaid* weeks only.
5. **Assuming the state cap doesn't apply.** A 90% replacement rate with a $1,200/week cap can be a 40% pay cut for high earners. Always compute capped dollars.
6. **Forgetting job protection ≠ pay.** After paid weeks end, protection may continue (state law) — the weeks are unpaid but your job is safe; plan childcare around the true end date.
7. **Waiting to file.** State claims typically can't be filed more than a few days before leave and take 1–3 weeks to pay. File the disability claim the week leave starts, the bonding claim the week recovery ends.
8. **Adoption/foster:** no recovery weeks, but bonding applies — and placement dates can move suddenly; FMLA's 30-day notice is waived when impossible.

## Verification Checklist

- [ ] FMLA eligibility verdict stated explicitly (eligible / not + which gate failed)
- [ ] Every week of the plan has: dates, phase, pay source, % + capped $ estimate, protection status
- [ ] Paid-weeks total and effective replacement income over the whole leave computed
- [ ] Gap (unpaid) weeks named with dates, not hidden
- [ ] State program parameters flagged as "verify current year" (weeks, caps, replacement change annually)
- [ ] Filing-order checklist: employer notice → state disability → state bonding → STD claim
- [ ] Partner's leave planned separately if requested

## One-Shot Recipe: first plan in 5 minutes

```bash
python3 scripts/maternity_plan.py plan \
  --state CA --due 2026-03-15 --pay 1150/week \
  --c-section --pto-days 10
# → dated week table: SDI recovery 8wk (60-70%) → PFL bonding 8wk → PTO-plugged gap → unpaid CFRA tail
```

Then: ask HR for the written parental-leave policy (it may pay weeks on top), and rerun with `--std-weeks`/`--employer-weeks` to see the delta. Compare against `--partner` mode for the non-birthing parent.
