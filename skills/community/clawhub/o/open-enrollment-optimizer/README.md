# open-enrollment-optimizer

**Choose health plans, FSA/HSA elections, and benefits like an actuary — during the
2–6 week window when it actually matters.** Computes true annual cost of every
candidate plan across healthy / typical / bad-luck scenarios, finds the exact claims
crossover where the winner flips, prices FSA forfeiture risk, and quantifies the HSA
triple-tax advantage over a real horizon.

## The real-world problem

Open enrollment locks in ~$10,000–$30,000 of annual decisions (premiums + deductible
exposure + tax-advantaged accounts) in a short deadline window, from dense plan PDFs.
The classic mistakes:

- **Premium-shopping**: picking the cheapest paycheck deduction while ignoring that a
  $2,000 lower deductible saves more in any year you actually use care
- **FSA paralysis**: electing the same number every year, or forfeiting $500+ to
  use-it-or-lose-it
- **HDHP without funding the HSA**: a high deductible with none of the tax upside
- **Not noticing** the plan's network or formulary silently changed this year

There is no do-over until next November. Wrong elections cost $1,000–$5,000 per year
and get repeated annually out of inertia.

## What it does

| Capability | Detail |
|---|---|
| True Annual Cost model | premium × 12 + patient share of claims (deductible → coinsurance → OOP-max cap) per scenario |
| Scenario engine | healthy (~$600) / typical (~$3,200) / bad-luck (~$18,000 — exercises the OOP max) |
| Crossover finder | bisection solve: "under $X/yr claims Plan A wins, above it Plan B" — the honest answer |
| FSA election math | tax saved vs expected forfeiture, break-even utilization %, carryover-aware |
| HSA vs taxable | N-year balance difference at real returns — quantifies the triple-tax advantage |
| Medicare-ready | same method for Part D / MA vs Medigap during Oct 15 – Dec 7 |

## Quick start

```bash
python3 scripts/enrollment_optimizer.py --demo
python3 scripts/enrollment_optimizer.py --plans scripts/plans.example.json
python3 scripts/enrollment_optimizer.py --fsa 1600 1400 32
python3 scripts/enrollment_optimizer.py --hsa 4300 8 25 15
```

Stdlib only.

## Example output

```
SCENARIO     CLAIMS           PPO      HDHP+HSA   WINNER
---------------------------------------------------------
healthy         600          6,840        3,920   HDHP+HSA
typical       3,200          8,080        6,360   HDHP+HSA
bad-luck     18,000         11,040        9,320   HDHP+HSA

CROSSOVER PPO vs HDHP+HSA: none — HDHP+HSA wins across the whole range
ROBUST PICK: HDHP+HSA
```

Then the FSA/HSA mode tells you the $1,600 FSA election saves $448 in tax if spent,
risks $50 forfeiture at 25% underspend odds — GOOD BET, but you must spend >44% of it.

## Why it matters

~170M Americans with employer coverage make these elections every fall, and most
re-elect defaults. A one-hour structured comparison typically finds $500–$3,000/yr in
expected savings — plus the bad-luck scenario tells you exactly what a surgery year
costs under each option before you need to know.
