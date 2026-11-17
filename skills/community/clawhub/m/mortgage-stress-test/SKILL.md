---
name: mortgage-stress-test
description: "Use when buying a home, comparing rent vs buy, or checking how much house you can honestly afford. Computes true monthly cost (PMI, tax, insurance, maintenance), 28/36 DTI verdicts, rate-shock stress (+1/+2%), and rent-vs-buy break-even horizon."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [mortgage, home-buying, rent-vs-buy, affordability, personal-finance]
---

# Mortgage Stress Test

## Overview
The listed price of a home is not the cost of a home. Lenders pre-approve you to the
maximum they can profitably lend, not to what leaves room for life. This skill computes
the **true monthly ownership cost** (principal+interest, property tax, insurance, PMI,
HOA, and the 1%/year maintenance reality), checks it against the 28/36 DTI rule and a
50/30/20 sanity check, stress-tests the payment against +1% and +2% rate shocks (for
ARMs and refinances), and answers the only fair rent-vs-buy question: *at what holding
horizon does buying beat renting, if ever, given opportunity cost of the down payment?*

## When to Use
- "Can I afford this house?" / "How much should I spend?" — before offering
- Comparing a specific purchase against continuing to rent
- Deciding between a bigger down payment vs keeping investments
- ARM vs fixed stress check ("what if rates rise at reset?")
- Evaluating whether to wait and save more down payment
- **Don't use for:** investment-property cash-flow analysis (needs rental income model),
  commercial mortgages, or non-US tax specifics without adapting tax assumptions.

## Inputs You Need
| Input | Typical source | If unknown |
|---|---|---|
| Home price | listing | — |
| Down payment | savings | 20% is the PMI-free target |
| Interest rate % | lender quote | use current 30-yr fixed average |
| Term years | loan offer | 30 |
| Property tax %/yr | county assessor (often 0.5–2.5%) | 1.1% of price |
| Insurance $/yr | quote | 0.35% of price |
| HOA $/mo | listing | 0 |
| Other debt $/mo | credit reports | 0 |
| Gross monthly income | pay stubs | — |
| Rent (comparison) | current lease | — |
| Investment return % | — | 6% (long-run balanced) |
| Appreciation %/yr | — | 3% (long-run national norm; do not use boom years) |

## Steps
1. Run the calculator with the borrower's numbers:
   ```bash
   python3 scripts/mortgage_math.py --price 450000 --down 45000 --rate 6.5 \
       --tax-pct 1.1 --insurance 1600 --income 8500 --other-debt 400 \
       --rent 2100 --appreciation 3.0 --invest-return 6.0
   ```
2. Read the **verdict block**: PASS / TIGHT / FAIL on front-end (28%) and back-end (36%)
   DTI, plus the true monthly cost vs the naive "mortgage payment" people quote.
3. Check the **rate shock** table — if +2% breaks the budget, the ARM is a trap.
4. Read the **rent-vs-buy break-even** — buying loses money for the first N years due to
   closing costs and slow principal paydown; the horizon must be shorter than the
   planned stay.
5. If FAIL or TIGHT: rerun with bigger down payment, cheaper price, or longer horizon
   until PASS, and report the max price that passes.

## Worked Example
$450k home, 10% down ($45k), 6.5% / 30yr, $8500/mo income, $400 other debt, rent $2100:

- P&I ≈ **$2,560** — but true monthly ≈ **$3,485** (P&I + $412 tax + $133 insurance +
  $169 PMI (0.5%) + $375 maintenance) — 36% *more* than the payment people budget for.
- Back-end DTI ≈ **45.8%** → **FAIL** (36% rule; $3,485+$400 = $3,885 vs $3,060 cap).
- Max affordable price at these terms ≈ **$340k** (income-capped), or raise down payment
  to ~$135k to kill PMI and pass at $450k.
- Rent-vs-buy break-even ≈ **year 4** at 3% appreciation — fine if staying 7 years,
  a loss if moving in 2.

## The Math (summary — full detail in references/mortgage-math.md)
- Payment: `M = P·r(1+r)ⁿ / ((1+r)ⁿ − 1)`, r = APR/12
- PMI: 0.5–1.5% of loan/yr while equity < 20% (approximate exit year computed from
  amortization + appreciation)
- Maintenance: 1%/yr of price (older homes: 1.5–2%)
- Closing costs: 2–5% (buyer side); selling costs ~6–7% (both sides' commissions + closing)
- Break-even year y: wealth if buying = equity(y) − Σownership costs − selling costs,
  compared against renting + investing (down payment + monthly difference) at the
  investment return. First year where buying wins = break-even horizon.

## Common Pitfalls
1. **Budgeting the P&I, not the PITI+M.** Taxes/insurance/PMI/maintenance add 25–50%.
   The calculator prints both — always quote the true number.
2. **Using boom-year appreciation (8–15%).** Long-run national real appreciation is
   ~3–4%; run break-even at 0% and 3% to see how fragile the case is.
3. **Forgetting selling costs.** ~6–7% exit cost means short holds almost always lose;
   break-even horizons under 3 years are rare even in normal markets.
4. **Counting the down payment as "spending" but not its opportunity cost.** $90k not
   invested at 6% is ~$5.4k/yr foregone — the model charges this.
5. **Treating PMI as forever or as nothing.** It ends at ~20% equity — the script
   estimates the exit year and stops charging it after.
6. **Lender pre-approval ≠ affordability.** Pre-approval uses gross income and 43–50%
   back-end DTI ceilings; the 36% rule exists because retirement, childcare, and
   repairs don't appear on the lender's worksheet.

## Verification Checklist
- [ ] True monthly cost (PITI+M+maintenance) printed and used in DTI
- [ ] Front-end ≤28% and back-end ≤36% checked with explicit PASS/FAIL
- [ ] Rate shock table (+1%, +2%) present
- [ ] Break-even horizon vs planned stay compared
- [ ] If FAIL: max passing price or required down payment reported
- [ ] Assumptions (appreciation, return, tax %) stated in the answer
