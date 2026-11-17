# FSA / HSA Decision Guide

## FSA — use-it-or-lose-it pricing

Health FSA (2026 limit ~$3,300, inflation-indexed; verify current year):
- Money is use-it-or-lose-it at year end, softened by ONE of:
  - **Grace period**: ~2.5 extra months to spend
  - **Carryover**: ~$660+ (indexed) rolls into next year
- You specify the election; the FULL amount is available January 1 (interest-free loan from
  your employer's future-you). Leaving mid-year: you keep spend-to-date, owe nothing back
  (FSA is winner-favorable on early-year big claims — a legit strategy for planned procedures
  in Q1 followed by a job change is legal but reads as sharp practice; use with awareness).

**Electing well:** election = expected qualifying spend, minus carryover available, with
forfeiture risk priced:

```
expected value = tax_rate × min(election, actual_spend) − (election − spend) × P(spend < election)
```

The `--fsa` mode of the script computes break-even utilization and forfeiture exposure.

Qualifying spend inventory (annualize yours): copays/coinsurance/deductibles, glasses/contacts,
dental (cleanings, fillings, ortho), OTC meds (no prescription needed since 2020), sunscreen,
first-aid, braces for the kid, LASIK (planned? elect exactly that), hearing aids, mileage to
medical appointments at the medical mileage rate.

**Dependent-care FSA** is separate: ~$5,000 cap, both parents must have childcare need, wins vs
child tax credit for marginal rate > ~22–24% usually. It is NOT use-it-or-lose-it the same way:
expenses must be incurred while you're at work during the year — summer camp qualifies, overnight
camp doesn't.

## HSA — the triple tax account

Available ONLY with an HSA-eligible HDHP (2026: deductible ≥ $1,700 single / $3,400 family —
verify annually; no-first-dollar-benefit rules apply).

1. **Deductible** (payroll) → skips income tax AND FICA
2. **Growth** → tax-free (invest after surpassing the cash buffer, typically $1–2k)
3. **Withdrawal for medical** → tax-free, ANY time — including decades later against kept receipts

The third point is the superpower: pay today's $500 bill out-of-pocket, keep the receipt,
reimburse yourself at 60 from an account that compounded tax-free for 35 years. Effectively an
extra traditional-IRA-shaped bucket with no RMDs.

Numbers the script computes (`--hsa`):
- N-year balance difference vs taxable investing at same gross contribution
- The "pay out-of-pocket + save receipts" strategy's terminal advantage at a real return

Limits (2026-family): $4,300 single / $8,550 family + $1,000 catch-up 55+. Employer seed counts
inside the limit. Max it before taxable investing in almost every personal-finance ordering
(after 401k match, alongside IRA).

## FSA vs HSA quick table

| | FSA | HSA |
|---|---|---|
| Own the money | no (employer plan) | **yes, portable forever** |
| Roll over | ~$660 or grace | everything, always |
| Investment growth | none | tax-free investing |
| Requires HDHP | no | yes |
| Change election mid-year | only with qualifying event | anytime |
| Payroll FICA dodge | yes | yes |

## Election-day checklist

- [ ] HDHP? Elect full HSA (seed + own = limit) — payroll deduction for FICA dodge
- [ ] Not HDHP? Elect FSA = expected spend − carryover credit
- [ ] Planned procedure next year (LASIK, ortho, birth)? Elect exactly it in FSA/HSA-aware plan
- [ ] Dependent-care FSA vs child-tax-credit comparison if kids in daycare
- [ ] Don't stack: general FSA makes you HSA-ineligible (limited-purpose FSA for dental/vision
      is the compatible kind)
