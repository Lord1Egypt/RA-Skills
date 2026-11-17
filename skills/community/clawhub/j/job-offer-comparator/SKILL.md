---
name: job-offer-comparator
description: "Use when comparing two or more job offers, deciding between a remote and on-site role, weighing a higher salary against a long commute, moving cities for a job, pricing the real value of benefits, or preparing a salary negotiation counter-offer. Computes true total compensation — base + expected bonus + capped retirement match + risk-discounted equity − health premiums − commute cost (km + parking) − cost-of-living adjustment — then effective hourly rate on REAL hours (contracted + overtime + commute), PTO valuation, and the exact break-even base salary the losing offer needs to match the winner. Outputs a negotiation-ready target number."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [career, job-offer, compensation, negotiation, relocation, decision, salary]
---

# Job Offer Comparator ⚖️

A $115k on-site offer can lose to a $95k remote one. Salary is the number
companies make easiest to see; everything that actually decides your life —
commute hours, health premiums, retirement match caps, equity that may never
liquify, and the cost of living in the offer's city — hides in attachments
and footnotes.

This skill makes offers comparable by computing, per offer: **true total
compensation** (all cash + benefits − deductions, COL-adjusted), **effective
hourly rate on real hours** (including commute), the **$ value of PTO**, and
the **break-even base salary** — the exact number to say in a negotiation:
"I'd need $X base to say yes."

## Overview

Four commands in `scripts/offer_compare.py`:

1. **`compare`** — side-by-side table: raw comp lines → deductions →
   risk-adjusted → COL-adjusted true comp; then derived metrics (real weekly
   hours, effective hourly, PTO value) and a plain-language verdict,
   including the marginal hourly rate of the extra hours the money-rich offer
   demands. `--json` for agents.
2. **`breakeven`** — for exactly two offers: the base salary the loser needs
   to match the winner's true comp (holding its own bonus/match/deductions
   constant) — your negotiation target. Also shows the reverse: how far the
   winner could drop and still win.
3. **`annotate`** — field-by-field guide: typical values and where to find
   each number in an offer letter/benefits PDF.
4. **`example`** — a filled sample `offers.json` to copy.

## When to Use

- "I have two offers — which is actually better?"
- "Is $115k in the office worth it vs $95k fully remote?"
- "The offer is in Austin — how does cost of living change the math?"
- "What salary should I counter with?" (→ `breakeven` gives the number)
- "Contractor day-rate vs salary — which wins?" (model the contract as an
  offer with no benefits, high gross)
- "They offer 0.5% equity — how do I account for it?" (risk-discount it)

**Don't use for:** tax advice (gross-of-tax model), pre-IPO equity valuation
(use a 409A/secondary-price approach), or deciding between job families —
it prices offers, it doesn't rank careers.

## Quick Start

```bash
# 0. Get a filled sample and edit it
python3 scripts/offer_compare.py example > offers.json

# 1. Full comparison (remote $95k vs big-city $115k)
python3 scripts/offer_compare.py compare --file offers.json

# 2. Negotiation target: what base makes the loser match the winner?
python3 scripts/offer_compare.py breakeven --file offers.json

# 3. Inline, no file — two quick offers
python3 scripts/offer_compare.py compare \
  --offer '{"name":"Stay","base":90000,"commute_km_each_way":25,"commute_days_per_week":4}' \
  --offer '{"name":"Go","base":104000,"commute_km_each_way":0,"col_index":108}'

# 4. Where does each number come from?
python3 scripts/offer_compare.py annotate

# 5. Machine-readable
python3 scripts/offer_compare.py compare --file offers.json --json
```

## How It Works

```
gross = base + base×bonus_pct + min(base×match_pct, match_cap)
      + equity_value×(1−equity_risk) + other_benefits×12 + relocation
risk_adj = gross − health_premium×12 − commute_cost
commute_cost = km×2×days×52×cost_per_km + parking×12
TRUE COMP = risk_adj ÷ (col_index/100)
real hours/wk = hours_per_week + overtime + 2×days×(km ÷ 28 km/h)
effective hourly = true comp ÷ (52 × real hours/wk)
PTO value = pto_days × (true comp ÷ 260)
```

Every assumption is **printed above the table**, never hidden: 28 km/h
door-to-door commute speed, 52 working weeks / 260 working days, equity risk
default 0.50 for illiquid private-company grants. The retirement match cap
is honored (`min(base×pct, cap)`) — caps bind more often than people think
once base passes ~$80–100k. Taxes are deliberately out of scope: they shift
with filing status and jurisdiction; the model compares offers, not tax
strategies.

**Breakeven** solves by bisection on base (handles the match-cap kink where
a closed-form would break): find base B such that the losing offer's true
comp at B equals the winner's true comp.

## Offer Field Reference

| Field | Typical | Where to find it |
|---|---|---|
| `base` | 60k–250k | offer letter headline number |
| `bonus_pct` | 0–0.20 | "annual bonus target, up to X%" — enter the *expected* value |
| `equity_annual_value` | 0–100k+/yr | annual grant ÷ vest years (RSU $ value/yr) |
| `equity_risk` | 0.0–0.9 | 0–0.2 public RSUs; 0.5 private; 0.9+ early startup |
| `retirement_match_pct` | 0–0.06 | benefits PDF, "401(k) match" |
| `retirement_match_cap` | 0–15k | the small print — often caps the match |
| `health_premium_monthly` | 0–800 | employee share of premiums (paycheck deduction) |
| `pto_days` + `holidays` | 10–30 / 8–12 | PTO policy page |
| `hours_per_week` + `overtime_hours_per_week` | 40 / 0–15 | ask the team, trust Glassdoor norm |
| `commute_km_each_way` + `commute_days_per_week` | 0–60 / 0–5 | map home↔office |
| `commute_cost_per_km` | 0.05–0.50 | default 0.30 (all-in car); transit fare÷km |
| `monthly_parking_or_transit` | 0–400 | parking spot / transit pass price |
| `col_index` | 85–130 | Numbeo/BEA index vs your baseline = 100 |
| `relocation_bonus` | 0–20k | one-time; flagged, first-year only |

## Workflow

1. Collect both offers into JSON (start from `example`, use `annotate` for
   any unclear field).
2. Enter **expected** bonus (not "up to"), risk-discount equity honestly.
3. Run `compare` — read the verdict block first, then the table.
4. Run `breakeven` — get the counter-offer number for the losing side.
5. Negotiate with that number; re-run after every revised offer.
6. Sanity-check hours assumptions — the model is only as honest as the
   overtime you admit to.

## Common Pitfalls

1. **Comparing nominal salaries across cities.** $115k at COL 115 is
   $100k-equivalent. Set `col_index` before reading the verdict.
2. **Trusting "up to 20% bonus".** Enter the expected (usually 50–70% of
   max, or the 3-year historical payout) — not the maximum.
3. **Ignoring the match cap.** 6% match capped at $4k on $115k pays $4k, not
   $6.9k. The table flags a `*` where the cap binds.
4. **Forgetting commute TIME, not just cost.** 10 h/week of commuting at a
   $50/h effective rate is $26k/yr of your life — often bigger than the
   salary gap itself.
5. **Counting equity at face value.** A 0.5% private grant is a lottery
   ticket; risk-discount it (default 0.5) or it will dominate every
   decision.
6. **One-time money as recurring.** Relocation/signing bonuses inflate
   year-one comparisons — the tool flags them; exclude them from long-run
   decisions.

## Verification Checklist

- [ ] `example > offers.json` then `compare --file` runs and prints
      assumptions + table + verdict
- [ ] Verdict names a money winner AND an hours/life winner
- [ ] `breakeven` prints a target base, and its verification line
      ("at that base … == target ✓") holds
- [ ] Changing `col_index` from 100 → 115 visibly reduces true comp
- [ ] Setting `retirement_match_cap` below base×match% shows the `*`
      capped flag
- [ ] `compare --json` output parses and rows include `true_comp` and
      `effective_hourly`
- [ ] `python3 scripts/test_offer_compare.py` → ALL TESTS PASSED

## One-Shot Recipes

**Remote vs office, same city:**
```bash
python3 scripts/offer_compare.py compare \
  --offer '{"name":"Remote","base":95000,"commute_km_each_way":0,"commute_days_per_week":0,"health_premium_monthly":150,"retirement_match_pct":0.04,"retirement_match_cap":10000,"equity_annual_value":12000}' \
  --offer '{"name":"Office","base":115000,"commute_km_each_way":30,"commute_days_per_week":5,"monthly_parking_or_transit":250,"health_premium_monthly":600,"bonus_pct":0.15}'
```

**Same job, different cities (COL):**
```bash
python3 scripts/offer_compare.py compare \
  --offer '{"name":"Denver","base":105000,"col_index":100}' \
  --offer '{"name":"SF","base":140000,"col_index":165,"commute_km_each_way":40,"commute_days_per_week":3}'
```

**Contractor day-rate vs permanent salary:** model the contract as gross =
day-rate × billable days (e.g. $650×220 = $143k), zero match/equity/PTO,
full health premium, and compare effective hourlies.
```bash
python3 scripts/offer_compare.py compare \
  --offer '{"name":"Contract","base":143000,"bonus_pct":0,"retirement_match_pct":0,"health_premium_monthly":650,"pto_days":0,"hours_per_week":45}' \
  --offer '{"name":"Staff","base":118000,"bonus_pct":0.08,"retirement_match_pct":0.05,"retirement_match_cap":9000,"health_premium_monthly":180,"pto_days":24}'
```

---
*Decision support, not financial advice. Gross-of-tax model; verify offer
terms against the actual documents before negotiating.*
