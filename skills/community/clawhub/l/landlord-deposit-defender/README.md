# Landlord Deposit Defender 🛡️

**Your landlord kept $1,200 of your deposit for "repainting and carpet
replacement" after a three-year tenancy. What's actually lawful?**

## The problem

Security deposit disputes are among the most common rental conflicts, and
they are radically asymmetric: the landlord holds the money, names the
"damages", and often produces an invoice from their own contractor. Tenants
usually don't know that:

- **Normal wear and tear is not chargeable** in most jurisdictions — scuffed
  paint, worn carpet paths, faded blinds are the cost of doing business.
- **Even legitimate damage is depreciated.** If carpet has an 8-year useful
  life and you used 3 of those years, the maximum lawful deduction is the
  *remaining* value, not replacement price.
- **Deadlines are enforceable.** Landlords typically have 14–60 days
  (US states), 10 days (UK schemes), etc., to return the deposit or send an
  itemized statement. Miss it, and many jurisdictions void the deductions.

The winning tenant argument isn't louder — it's itemized, priced,
depreciated, and cites the rules. That's what this tool produces.

## What it does

`scripts/deposit_defender.py` (Python 3, stdlib only, no network):

| Command | What you get |
|---|---|
| `inventory` | Room-by-room condition records (grades 0–5 + notes), validated and exportable as JSON — do this at move-in, not just move-out |
| `diff` | Classifies every change between two inventories: improvement / fair wear / damage — with the item's age over the tenancy factored in |
| `prorate` | Useful-life math: `max deduction = value × (1 − years_used / useful_life)`. Carpet $1,200, 8-yr life, 2.5 years in → max $825, not $1,200 |
| `letter` | Full markdown demand letter: timeline, item-by-item rebuttal with prorated counter-figures, jurisdiction deadline citation, receipts demand, small-claims escalation notice |
| `jurisdictions` | Built-in table of typical deposit-return deadlines (~15 jurisdictions) |

## Quick start

```bash
python3 scripts/deposit_defender.py inventory --label move-in --date 2023-06-01 \
  --item "bedroom,carpet,1,nearly new" > move-in.json

python3 scripts/deposit_defender.py prorate --item "carpet,1200,8" --tenancy-years 2.5

python3 scripts/deposit_defender.py letter --move-in move-in.json \
  --move-out move-out.json --deposit 2400 --deductions deductions.json \
  --jurisdiction CA --tenant "Jordan Reyes" --landlord "Acme Property Mgmt"

python3 scripts/test_deposit_defender.py   # 39 assertions
```

## Who needs this

- Hundreds of millions of renters worldwide; deposits commonly equal 1–3
  months of rent — often the largest single sum a household has at stake.
- Students and first-time renters with no dispute experience.
- Anyone moving out who wants deductions predicted and priced *before* the
  landlord's letter arrives.
- Landlords who want to stay on the right side of wear-and-tear law.

## Honest limits

Decision support, not legal advice. Useful-life tables and deadlines are
typical conventions (property-industry depreciation norms; jurisdiction
statutes change) — the tool marks them as such and expects you to verify
current local law. See `references/deposit-model.md` for the full model.

MIT © 2026 Denis Voronin
