# Layoff Deadline Tracker

**Five clocks start ticking the day you're laid off: COBRA's 60-day
election, the 401(k) loan cure period, the equity exercise window,
unemployment's no-backdate filing week, and the ADEA 21+7-day signing
window. Miss one and a layoff gets thousands of dollars more expensive.**

Layoffs hit millions of workers a year, and the expensive mistakes are
administrative, not emotional: the COBRA window that was a free option
gets declined-or-paid on day one instead of played to day 55; the 401(k)
loan silently converts to a taxed distribution with a 10% penalty; the
unemployment claim filed "when things settle" forfeits every delayed
week; the options expire unexercised at day 90. This skill extracts the
deadline map from the termination date, prices the decisions
(COA "elect vs eat", loan "repay vs distribute", severance benchmark),
and orders everything by what expires first.

## What it does

- **`map`** — dated deadline cascade: benefits end, COBRA 45/55/60-day
  checkpoints, marketplace SEP, unemployment week-one rule, 401(k) loan
  alarm, ADEA windows if 40+, equity audit + typical 90-day exercise,
  the tax-date reckoning. State overlays: PTO payout rules, non-compete
  ban states.
- **`severance`** — offer benchmark (weeks × multiple of weekly pay),
  WARN Act 60-day back-pay check for group events, "owed regardless of
  signing" inventory, what the release actually buys.
- **`cobra`** — the option-pricing view: window as free look, scenario
  math for claims vs back-paid premiums, marketplace-credit direction
  for the severance-income year.
- **`401kloan`** — deemed-distribution cost (tax + penalty at YOUR
  numbers), repayment options ranked, and the age-55 separator-rule
  warning that saves a five-figure mistake on rollovers.
- **`checklist`** — week-one structure: unemployment filing, document
  copies, personal-data export, FSA spend-down, runway math.

## Quick start

```bash
python3 scripts/layoff_deadlines.py map --date 2026-10-16 --state ca --over40
python3 scripts/layoff_deadlines.py severance --offer 21000 --weeks 10 --salary 2100
python3 scripts/layoff_deadlines.py cobra --cost 720 --months 18 --events 45000
python3 scripts/layoff_deadlines.py 401kloan --loan 8000 --age 47 --taxrate 24
python3 scripts/layoff_deadlines.py checklist
```

Stdlib only, offline, no accounts. General information, not legal or
financial advice — ADEA/WARN/equity specifics belong to an employment
attorney or CPA when the amounts are real.

MIT © Denis Voronin
