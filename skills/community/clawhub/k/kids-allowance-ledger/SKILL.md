---
name: kids-allowance-ledger
description: Use when setting up or running a child's allowance system — jar splits, chore commissions, parent 401(k) match, compound-interest projections, and wishlist save-up tracking that teaches real money habits.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [allowance, kids, finance, parenting, education, savings]
---

# Kids Allowance Ledger

## Overview

A double-entry allowance engine that turns a weekly handout into a money-education
system: every deposit auto-splits into Spend / Save / Share jars, the Save jar earns
parent-paid interest (or a 401(k)-style match), goals track days-to-purchase, and
the ledger produces kid-readable statements. The point is not accounting — it is
making compound growth, delayed gratification, and trade-offs *visible* to a 6–16
year old.

## When to Use

- Parent asks "how much allowance should I give", "how do I teach my kid to save", "chore chart that pays"
- Setting up jar splits, interest, or a parent match for a child's money
- Answering the kid-classic "when can I buy the PS5?" with a real ETA
- Reviewing what the child earned/spent/saved over a month or year
- Comparing chore-commission vs fixed allowance models

Don't use for: adult budgeting (see debt-blitz-planner), family shared expenses
(roommate-rules-referee), or tax-deductible tracking (tax-doc-collector).

## Core Model

1. **Income events** — weekly allowance (fixed) and/or chore commissions
   (per-task payouts). Both append to the ledger with a date and source.
2. **Jar split** — each income auto-divides by percentages (default 50 Spend /
   40 Save / 10 Share). Percentages are per-child and change with age.
3. **Growth engine** (choose one or both):
   - **Interest mode**: monthly % on the Save jar balance (5%/mo ≈ 80%/yr —
     deliberately exaggerated vs real banks so the curve is *felt*).
   - **Match mode**: parent matches Save-jar deposits up to a monthly cap —
     a literal 401(k) demo.
4. **Goals** — wishlist items with price; the tool computes weeks-to-goal at the
   current Save-jar inflow rate and after any match.
5. **Spend events** — deduct from Spend (or Save with an explicit raid that
     shows the future value destroyed — the strongest teaching moment in the tool).

## Numbered Workflow

1. `init` the ledger: child name, age, weekly allowance, jar split, growth mode.
2. `chore add` the commission menu (name → payout), sized against the weekly base.
3. Each week (or live): `deposit` allowance, `earn <chore>` payouts.
4. `goal add` the wishlist with price and link to a jar.
5. Run `project --years 3` to show the child the compounding curve.
6. Monthly: `statement` → kid-readable summary; `audit` → parent sanity check
   on raid frequency and Share-jar usage.
7. On birthdays: bump `age`, widen the Save %, raise the match cap.

## Commands

```
python3 scripts/allowance_ledger.py init --name Mia --age 8 \
  --weekly 5 --split 50/40/10 --interest 5 --match-cap 10
python3 scripts/allowance_ledger.py chore add "walk dog" 1.50
python3 scripts/allowance_ledger.py deposit 5.00 --note "weekly allowance"
python3 scripts/allowance_ledger.py earn "walk dog"
python3 scripts/allowance_ledger.py spend 12.99 --note "comic book" --jar spend
python3 scripts/allowance_ledger.py goal add "LEGO set" 89.99
python3 scripts/allowance_ledger.py project --years 2
python3 scripts/allowance_ledger.py statement
python3 scripts/allowance_ledger.py audit
```

Store lives in `allowance_ledger.json` next to the script (override: `--store PATH`).

## Age Banding (guidance baked into references)

| Age | Weekly base | Split S/S/Sh | Engine |
|-----|-------------|--------------|--------|
| 5–7  | age/2 $/wk  | 30/60/10 | 3 jars, no interest yet — counting first |
| 8–11 | $1/yr age   | 50/40/10 | interest 5%/mo on Save |
| 12–15| 1.5×age $/wk| 40/50/10 | match 50% up to cap + interest |
| 16–18| 2×age $/wk  | 30/60/10 | match + budget categories, near-adult ledger |

## Pitfalls

1. **Paying for everything** — grades, teeth brushing, existing family duties
   stay unpaid; commissions are for above-baseline work only. The chore menu
   should exclude "make your bed".
2. **Bailing out raids** — if a Save raid has no consequence display, the lesson
   dies. Always show `--show-future-cost` on Save spends.
3. **Realistic interest** — 0.1%/mo real-bank rates teach nothing at kid scale;
   pay generous fake rates and say so ("I'm the bank and I'm inflationary").
4. **Split changes mid-week** — change splits only at deposit boundaries or the
   jar math and the child's trust both break.
5. **Share jar as decoration** — schedule its use (birthday donations, class
   fundraisers) or kids learn charity is a shelf.

## Example

8-year-old, $5/week, 50/40/10, 5%/mo interest on Save, $90 LEGO goal:
the Save jar nets $2/wk + interest; `project` shows ≈ $125 by month 12 and the
goal ETA slips from 45 weeks to 34 once a 50% match up to $10/mo is switched on —
the kid sees the match, not the parent, close the gap.
