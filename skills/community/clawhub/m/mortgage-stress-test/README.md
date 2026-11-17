# mortgage-stress-test

**Can I actually afford this house?** The bank's pre-approval tells you the most they'll
lend you — not what leaves room for retirement, repairs, and rate shocks. This skill
computes the true monthly cost of ownership (P&I + tax + insurance + PMI + HOA +
1%/yr maintenance), judges it against 28/36 DTI rules, stress-tests the payment at
+1%/+2% rates, and tells you the honest year at which buying beats continuing to rent.

## The real-world problem
- Buyers budget the mortgage payment and discover the true cost is 25–50% higher.
- Lenders approve to 43–50% back-end DTI — leaving nothing for emergencies.
- ARM borrowers never check what +2% does to the payment.
- Rent-vs-buy debates ignore closing costs, selling costs (~6.5%), PMI exit timing, and
  the opportunity cost of the down payment.

## What it does
`scripts/mortgage_math.py` (stdlib only):

```
$ python3 scripts/mortgage_math.py --price 450000 --down 45000 --rate 6.5 --income 8500 \
    --other-debt 400 --rent 2100
Loan $405,000  LTV 90.0%
P&I ............... $  2,560/mo
...
TRUE MONTHLY ...... $  3,484/mo
Front-end DTI 41.0% [FAIL]   Back-end DTI 45.8% [FAIL]  (targets 28/36)
→ Max price passing 36% back-end at this down payment: $344,000
Rate shock: +2% → true $3,976/mo, back-DTI 51.4%
Rent $2,100/mo vs buy: break-even at year 4
```

- Full PITI+PMI+HOA+maintenance stack
- Front-end/back-end DTI verdicts (PASS/TIGHT/FAIL), max price at 36% via binary search
- Rate-shock table for ARM/refi decisions
- Rent-vs-buy break-even with opportunity cost of down payment, PMI exit month,
  6.5% selling costs, 3%/yr rent growth
- `--json` output for programmatic use

## Files
- `SKILL.md` — trigger conditions, steps, pitfalls, worked example
- `references/mortgage-math.md` — every formula, PMI exit rules, honest caveats
- `scripts/mortgage_math.py` — the calculator

Planning instrument, not a loan offer. Verify terms against your Loan Estimate.
