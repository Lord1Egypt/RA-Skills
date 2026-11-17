---
name: home-office-tax-deduction
description: Use when a remote worker or freelancer asks about deducting a home office — regular vs simplified method math with the same inputs, exclusive-use gate test, income cap, depreciation-recapture pricing, and audit-proofing evidence pack.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [taxes, home-office, deduction, self-employed, remote-work]
---

# Home Office Tax Deduction Planner

## Overview
The home-office deduction is where remote workers split into three groups: those who skip it (leaving $500–$3,000/year on the table), those who claim it wrong (audit bait), and those who compute it once, properly, and reuse the worksheet. US rules fork hard: **W-2 employees cannot take it at all** (suspended 2018–2025 by TCJA), while **self-employed/freelancers** choose between the *regular method* (actual expenses × business-use %, with depreciation and carryover) and the *simplified method* ($5/sq ft, capped at 300 sq ft / $1,500, zero recordkeeping). The right choice depends on your rent, square footage, income cap, and whether you ever plan to sell your home (depreciation recapture).

This skill runs the whole decision in one pass: **gate test** (regular + exclusive use), **dual-method computation** from the same inputs, **income-cap enforcement** with carryover tracking, **recapture pricing** for owners, and an **evidence pack** (floor-plan worksheet, expense-log format, photo checklist) so the deduction survives an audit instead of evaporating in one.

## When to Use
- Freelancer/self-employed setting up a first home office or revisiting last year's method choice
- "My accountant asked: regular or simplified?" — produce the numbers both ways
- Remote W-2 employee hoping for a deduction — route to what IS available (accountable plans for owners, state allowances)
- Moving / changing homes: new square footage, new basis, method re-decision
- Audit-proofing: what photos, floor plan, and logs to keep and for how long

**Don't use for:** home-daycare providers (different exclusive-use waiver and hours-based math), rental-property home offices (Schedule E rules), or farmers (Schedule F nuances) — the core gate logic applies but the arithmetic differs; say so and specialize before computing.

## Quick Start
```bash
# 1. Gate first: is the space eligible at all?
python3 scripts/home_office_deduction.py gate --exclusive-room yes --dual-use no \
    --principal-place yes

# 2. Both methods from the same numbers (renter example)
python3 scripts/home_office_deduction.py compute --status self-employed \
    --sqft 140 --home-sqft 1000 --rent-year 24000 --utilities-year 2400 \
    --internet-year 720 --repairs-year 300 --income 62000

# 3. Owner: adds depreciation + recapture pricing to the comparison
python3 scripts/home_office_deduction.py compute --status self-employed \
    --sqft 180 --home-sqft 1800 --own --home-value 420000 --land-share 0.25 \
    --utilities-year 3000 --insurance-year 1500 --income 55000

# 4. Generate the audit evidence checklist/worksheet
python3 scripts/home_office_deduction.py evidence --sqft 140 > evidence_2026.txt
```

## Decision Logic (what the script encodes)
1. **Status gate**: W-2 employee → deduction $0 federally (2026 law status: TCJA suspension through 2025; verify current year); self-employed → continue. Note state exceptions (e.g., CA doesn't conform to some suspensions; PA allows employees unreimbursed business expenses).
2. **Exclusive-use gate**: dedicated room, regular use, principal place of business (or client-meeting site / separate structure). Fail → deduction $0 regardless of math.
3. **Business-use %** = office sqft ÷ home sqft. Capped implicitly by method: simplified maxes at 300 sqft regardless of home size.
4. **Regular method**: (rent + utilities + insurance + repairs + depreciation) × %. Renters often clear $2,500+; the depreciation line for owners = (home value × (1−land share)) ÷ 39 years × %.
5. **Simplified method**: $5 × min(sqft, 300) = up to $1,500. No depreciation, no recapture, no carryover.
6. **Income cap**: total deduction ≤ gross income from the business use of the home. Regular-method excess carries forward; simplified excess evaporates.
7. **Tie-breakers**: bigger regular number AND you'll keep the home 5+ years → regular (recapture is a later, smaller, tax-rate-capped bill). Thin records or small space → simplified. Renters with high rent share → almost always regular.

## The Recapture Trap (owners, read this)
Every year of regular-method depreciation gets "recaptured" as income (up to 25% rate) when you sell — **even depreciation you could have taken but didn't** (allowed/allowable). Simplified-method years never create recapture. The script prices this: annual depreciation × years-to-planned-sale × 25% vs the annual regular-vs-simplified delta, so a "$600/yr better" regular method can be a worse 10-year deal for someone planning to sell.

## Evidence Pack (what `evidence` emits)
- Dated floor-plan worksheet: room dimensions, home total, computed %
- Photo checklist: wide shot showing exclusive business use, desk/equipment, storage area (inventory storage also qualifies even if not exclusive-use *room*)
- Expense log columns: date, payee, category (rent/utilities/repairs/insurance), amount, % applied
- Retention: worksheets + logs 7 years; photos refreshed after any room change
- Form mapping: Form 8829 (regular) vs Schedule C line 30 simplified worksheet

## Common Pitfalls
1. **Claiming on a W-2** — federal $0; don't let a "tax tip" app talk you into it.
2. **Dual-use room** ("it's my office except when guests visit") — fails exclusive use; the entire deduction dies, not a fraction.
3. **Simplified with a big rent bill** — a $2,000/mo renter with a 15% office is leaving ~$2,000/yr behind.
4. **Forgetting the income cap carryover** — regular-method excess isn't lost, it carries; track it.
5. **Commute confusion**: driving from home office to a client is deductible mileage for self-employed; the office being the principal place of business is what makes the drive "business", not the deduction itself.
6. **Recapture surprise at sale** — see above; the script prices it rather than ignoring it.

## Verification Checklist
- [ ] Gate test passed (exclusive + regular + principal place) before any math
- [ ] Both methods computed from identical inputs
- [ ] Income cap applied; carryover noted if hit
- [ ] Owner path: recapture priced against method delta
- [ ] Evidence worksheet saved with current-year photos queued

## Example Session
```
$ python3 scripts/home_office_deduction.py compute --status self-employed \
    --sqft 140 --home-sqft 1000 --rent-year 24000 --utilities-year 2400 \
    --internet-year 720 --repairs-year 300 --income 62000
Business-use %: 14.0%
  REGULAR:  (24000+2400+300) x 14% = $3,738 + internet direct $720 = $4,458
  SIMPLIFIED: 140 sqft x $5 = $700
Income cap: $62,000 — not binding.
VERDICT: REGULAR by $3,758/yr. Keep the expense log; this survives audit with records.
```
