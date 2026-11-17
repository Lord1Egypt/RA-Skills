---
name: landlord-deposit-defender
description: "Use when a landlord withholds or deducts from a security deposit, when moving in or out and a room-by-room condition inventory is needed as evidence, or when deciding whether a claimed deduction (repainting, carpet replacement, cleaning) is fair wear-and-tear or chargeable damage. Grades condition 0-5, diffs move-in vs move-out inventories, prorates legitimate deductions by useful-life depreciation (paint 3yr, carpet 8yr...), cites jurisdiction deposit-return deadlines, and generates an itemized dispute letter with corrected amounts."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [renting, deposit, landlord, tenant, dispute, inventory, depreciation, moving]
---

# Landlord Deposit Defender 🛡️

Security deposits are one of the most common landlord–tenant flashpoints.
This skill structures the fight: a room-by-room condition inventory at
move-in and move-out, a diff that separates **fair wear and tear** (which
landlords must absorb) from **chargeable damage**, useful-life depreciation
math that prorates any legitimate deduction, jurisdiction deadlines for
returning deposits, and a generated itemized dispute letter.

## Overview

Four commands in `scripts/deposit_defender.py`:

1. **`inventory`** — record room/item/grade(0–5)/note entries with a date and
   label ("move-in"/"move-out"); validates grades; normalizes to JSON.
2. **`diff`** — compares two inventories; classifies each change as
   improvement / fair wear / damage using the grading rubric, item age over
   the tenancy, and defect-type rules; flags disputable deductions.
3. **`prorate`** — applies the useful-life formula
   `max_deduction = value × max(0, 1 − years_used / useful_life)`; shows the
   gap between a landlord's full-price demand and the lawful prorated amount.
4. **`letter`** — generates a full markdown demand letter: timeline,
   itemized rebuttal with prorated figures, jurisdiction deadline citation,
   request for itemized receipts, small-claims escalation notice.
   `jurisdictions` lists the built-in deadline table.

## When to Use

- Moving in: build the evidence baseline **before** unpacking.
- Moving out: document condition, predict the landlord's deductions.
- A deduction letter arrives: classify each item (wear vs damage), prorate,
  and draft the rebuttal.
- "Can my landlord charge me for repainting after 3 years?" (Usually: only a
  fraction — see proration.)

**Don't use for:** legal advice (it's decision support), eviction disputes,
rent-increase law, or small-claims court filing procedure — but the letter it
produces is the exhibit you'd bring to one.

## Quick Start

```bash
# Move-in inventory (repeat --item; grades 0 new … 5 destroyed)
python3 scripts/deposit_defender.py inventory --label move-in --date 2023-06-01 \
  --item "living room,paint,1,fresh repaint" \
  --item "bedroom,carpet,1,nearly new" \
  --item "kitchen,oven,2,light wear" --json > move-in.json

# Diff two inventories over the tenancy
python3 scripts/deposit_defender.py diff --move-in move-in.json \
  --move-out move-out.json --tenancy-start 2023-06-01 --tenancy-end 2026-02-15

# What is a carpet worth after 2 of its 8-year life, priced at $1,200?
python3 scripts/deposit_defender.py prorate \
  --item "carpet,1200,8" --tenancy-years 2.5

# Full dispute letter (California example)
python3 scripts/deposit_defender.py letter --move-in move-in.json \
  --move-out move-out.json --deposit 2400 \
  --deductions deductions.json --jurisdiction CA \
  --tenant "Jordan Reyes" --landlord "Acme Property Mgmt" > dispute-letter.md

# Deadline reference
python3 scripts/deposit_defender.py jurisdictions
```

## How It Works

**Grading rubric (0–5):** 0 new · 1 excellent · 2 minor wear · 3 noticeable
wear · 4 significant damage · 5 destroyed/missing.

**Wear vs damage.** A delta of ≤ 1 grade over a normal tenancy, or defects of
a type that come from ordinary use (scuffed paint, worn carpet paths, faded
blinds), classify as **fair wear and tear** — not chargeable in most
jurisdictions. Larger deltas, or defect types outside ordinary use (burns,
holes, missing fixtures, pet urine), classify as potential damage.

**Proration.** Even legitimate damage is limited by remaining useful life.
With carpet (8-yr life) valued $1,200 after 2.5 years of use:

```
max deduction = 1200 × (1 − 2.5/8) = $825
```

A landlord demanding the full $1,200 is over-claiming by $375.

**Deadlines.** Most jurisdictions cap the time a landlord has to return the
deposit or send an itemized statement — 14 to 60 days in the US, 10 days in
the UK (protection scheme), etc. Missed deadlines often forfeit deductions
entirely. The built-in table is a starting point; verify current local law.

## Common Pitfalls

1. **No move-in evidence.** A move-out inventory alone proves nothing about
   pre-existing condition. Photograph everything, dated, at move-in.
2. **Conceding "repaint" charges at face value.** Paint has a short useful
   life (≈3 yr); after a multi-year tenancy the lawful deduction is often a
   small fraction — or zero.
3. **Assuming the landlord's invoice is the fair price.** Demand itemized
   receipts; replacement-price for a depreciated item is double-dipping.
4. **Missing the deadline.** If the itemized statement arrives late, say so
   in writing immediately — many jurisdictions make late claims worthless.
5. **Arguing emotion, not items.** The letter works because it is itemized,
   dated, priced, and cites the rules — mirror that in any reply.

## Verification Checklist

- [ ] `inventory` rejects grades outside 0–5
- [ ] `diff` classifies a 1-grade paint change as wear, a burn as damage
- [ ] `prorate` on a fully-depreciated item returns 0 deduction
- [ ] `letter` contains timeline, itemized rebuttal, deadline citation
- [ ] `jurisdictions` lists your jurisdiction's typical window
- [ ] `python3 scripts/test_deposit_defender.py` → ALL TESTS PASSED

---
*Decision support, not legal advice. Jurisdiction rules change; verify
current local law before relying on any figure here.*

MIT © 2026 Denis Voronin
