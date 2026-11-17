# Paper Mail Retention

**Retention isn't a personality trait — it's a lookup table.** Tax
supporting docs: 7 years. Paystubs: until the W-2 matches. Warranties:
until expiry. Immunization records: forever. The pile exists because
nobody has the table.

## The Problem

- Households keep 95% of paper far too long (old utility bills, dead
  warranties, expired policies) while shredding the 5% that matters
  (returns, basis documents, deeds).
- Purges take whole Saturdays because files aren't organized by year —
  every document gets re-read and re-decided.
- "Keep it for taxes" is applied to everything, but only supporting
  documents ride the 7-year audit window; the rest is clutter with a
  false alibi.
- The wrong things go in recycling: utility bills and statements carry
  enough for account takeover — they belong in a cross-cut shredder.

## What This Skill Does

`scripts/mail_retention.py` — a 35-category retention table with clock
start events and the WHY for each rule:

```bash
python3 scripts/mail_retention.py keep --thing "tax return"
python3 scripts/mail_retention.py purge \
  --items "utility bill:2021-03" "bank statement:2024-06" \
          "tax return:2019" "warranty:2023-05"
python3 scripts/mail_retention.py archive   # filing blueprint + forever list
```

- `keep` — duration, clock event, disposition, reason for any category
- `purge` — item-by-item triage with dates: SHRED/KEEP verdicts with
  remaining or overdue clock
- `archive` — the year-folder blueprint that makes next purge a
  30-minute job, plus the never-purge list

## Who Needs This

- Any household with a paper pile that has become structural
- Annual/moving purge planners
- People setting up a first filing system
- Anyone inheriting a relative's paperwork boxes

## Example

Purge a mixed pile: `utility bill:2021-03` → SHRED, 4.7 years overdue.
`bank statement:2024-06` → SHRED, 1-yr clock done. `tax return:2019` →
KEEP FOREVER (scan then shred the paper). `paystub:2026-09` → KEEP
until the W-2 matches. One pass, every item decided by rule instead of
anxiety.

## License

MIT — see LICENSE.
