# Paycheck Withholding Calibrator

**Problem.** The W-4 has no feedback loop. People sign one at hire,
never touch it again, and then every April either celebrate a $3,000+
refund (an interest-free loan of their own money — ~$250/month of lost
take-home) or get ambushed by a balance due that can carry Form 2210
underpayment penalties. Raises that cross brackets, second earners,
side income, and kids all silently break the original withholding
assumptions.

**What it does.** `scripts/withholding_calibrator.py` turns one paystub
into an April forecast:

- **liability projection** with 2026-shaped brackets, standard vs
  itemized deduction, and child-tax credits (constants shared with the
  quarterly-tax-ranger skill, verify-flagged);
- **withholding trajectory** from YTD + remaining paychecks (per-pay
  derived from your actual YTD rate when not typed in);
- **verdict with framing**: BIG REFUND = the interest-free loan priced
  in dollars/year at your savings rate; OWE = safe-harbor check (90%
  current / 100% / 110% of last year when AGI > $150k) so you know
  whether a $12k balance due is penalty-free or penalty-priced;
- **the exact W-4 fix**: the per-paycheck dollars for Step 4(c) extra
  withholding, or the Step 3/4(b) adjustments to raise take-home —
  including the withholding-vs-estimated-payment timing doctrine.

**Why broadly useful.** Every wage earner in the country files a W-4;
IRS data shows ~70%+ get refunds averaging ~$3k (the loan) while
millions more owe unexpectedly (the ambush). A five-minute projection
from numbers already printed on the paystub is the entire fix, and
nobody has a tool that closes the loop mid-year.

**Example.**

```bash
python3 scripts/withholding_calibrator.py --ytd-gross 92000 \
    --ytd-withheld 6800 --per-pay-gross 6300 --per-pay-withheld 460 \
    --paychecks-left 8 --last-year-tax 9200
# → OWE $12,943, but WITHIN the 100%-of-prior-year safe harbor:
#   no penalty; W-4 Step 4(c) fix $1,618/paycheck going forward.
```

Federal income tax only; not tax advice; verify constants. MIT license.
