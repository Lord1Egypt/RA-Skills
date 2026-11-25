---
name: paycheck-withholding-calibrator
description: W-4 feedback loop from one paystub — projects the tax-year federal liability (2026-shaped brackets, standard deduction, child credits), compares it to your withholding trajectory, and names the outcome in dollars (a big refund is an interest-free loan to the IRS; a big owe risks Form 2210 penalties). Checks the 90%/100%/110% safe harbors and prints the exact W-4 fix — the per-paycheck number for Step 4(c) extra withholding or the Step 3 credit adjustment — to land on your target refund.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [taxes, withholding, w4, paycheck, refund, personal-finance]
---

# Paycheck Withholding Calibrator

The W-4 you signed years ago has no feedback loop. This skill is the
loop: feed it one paystub, get the April forecast and the exact
per-paycheck correction.

## When to trigger
- "I keep getting huge refunds — is that bad?"
- "I got hit with a surprise tax bill — how do I stop owing?"
- "I changed jobs / got a raise / added a side income — check my
  withholding before year-end"
- "Will I owe an underpayment penalty?"
- year-end (Oct–Dec) withholding checkups

## How it works

1. **Collect inputs** from the latest paystub: YTD gross, YTD federal
   withholding, gross per pay, federal withheld per pay, paychecks left
   this year. Plus filing status, dependents, other income (side
   business, interest, spouse's separate paystub), optional itemized
   deductions, optional last-year total tax, and a target refund
   (default $0).
2. **Run** `scripts/withholding_calibrator.py --ytd-gross 82000
   --ytd-withheld 9400 --per-pay-gross 6300 --per-pay-withheld 1080
   --paychecks-left 8 --filing mfj --dependents 2`
3. **Liability projection**: `gross + other income − deduction →
   brackets → child credits → liability`. 2026-shaped constants are
   shared with the quarterly-tax-ranger skill and flagged for
   verification.
4. **Trajectory**: `projected withholding = YTD + per-pay × paychecks
   left` (per-pay derived from your YTD average rate if not supplied).
5. **Verdict** with the framing people never get: a $4,000 refund is a
   half-year interest-free loan (priced at your savings rate), a $2,500
   balance due triggers the **safe-harbor check** — 90% of current
   liability, or 100%/110% of last year's (110% when AGI > $150k) — and
   a rough penalty price if no harbor holds.
6. **The fix**: under-withheld → the exact extra-withholding number for
   **W-4 Step 4(c)** per paycheck (or the Jan-15 estimated payment
   alternative, with the timing caveat that withholding is deemed paid
   evenly); over-withheld → the Step 3 credits / Step 4(b) deductions
   that raise take-home, or the honest "keep it as forced savings" price
   tag.

## Pitfalls encoded
- **Withholding is dated as paid evenly through the year**; estimated
  payments only count when made — so a December W-4 fix is gentler than
  a December estimated payment for the same dollars.
- **Safe harbors rescue big balances due**: owing $12k with 100% of
  last year's tax withheld is penalty-free; the tool checks instead of
  panicking.
- **Bracket creep after raises/bonuses**: the projection uses your real
  per-pay trajectory, so a mid-year raise is caught before April.
- The default W-4 knows nothing about itemizing, side income, or
  two-earner households — the classic under-withholding triple.
- State/local and FICA are explicitly out of scope (stated in output).
- Constants are estimates: verify against current IRS tables before
  acting (footer on every run).

## Examples

```bash
# Over-withheld couple (2 kids, some side income) — the refund loan
python3 scripts/withholding_calibrator.py --ytd-gross 82000 \
    --ytd-withheld 9400 --per-pay-gross 6300 --per-pay-withheld 1080 \
    --paychecks-left 8 --filing mfj --dependents 2 --other-income 3000
# → BIG REFUND $9,024 ≈ $180/yr lost interest; Step 3 fix $1,090/paycheck

# Under-withheld single after a raise — penalty risk check
python3 scripts/withholding_calibrator.py --ytd-gross 92000 \
    --ytd-withheld 6800 --per-pay-gross 6300 --per-pay-withheld 460 \
    --paychecks-left 8 --last-year-tax 9200
# → OWE $12,943 but WITHIN the 100%-prior-year harbor: no penalty
```

## Output contract
- tax-year projection table (gross → taxable → liability vs withholding)
- one-line verdict with the refund-loan or penalty-risk framing
- safe-harbor check with the three thresholds and pass/fail
- exact W-4 fix (Step 4(c) dollars per paycheck / Step 3 credits)
- scope + verify footer
