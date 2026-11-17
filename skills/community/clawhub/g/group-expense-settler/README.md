# Group Expense Settler 👥💰

**Split the trip costs fairly — then settle with the fewest possible payments.**

Six friends, one weekend, fourteen receipts. Everyone paid for something, and
now the group chat has a spreadsheet nobody trusts. This tool computes
everyone's fair share (equal or weighted), then produces the **minimum set of
bank transfers** that makes everyone whole — usually 3–5 payments instead of
the 15 possible "who-pays-whom" tangles.

## What it does

- Simple text ledger: `payer,amount,who_shares_it`
- Equal or **weighted** splits (room sizes, days attended, headcount)
- Per-item audit (`--show-items`) — settle arguments with arithmetic
- **Min-cash-flow settlement**: ≤ n−1 transfers, no one both pays and
  receives, cent-exact with no rounding dust
- Chat-ready settlement lines and JSON export

## Quick start

`trip.txt`:
```
Ana,450,Ana Ben Cho Dan      # hotel
Ben,120,Ben Cho               # taxi
Cho,80,Ana Ben Cho Dan        # groceries
Dan,60,Ben Cho Dan            # gas
```

```bash
python3 scripts/settle_up.py --ledger trip.txt --show-items
```

Output:
```
Person            Paid   Fair share          Net
----------------------------------------------------
Ana           $450.00      $132.50    $317.50
Ben           $120.00      $212.50    -$92.50
Cho            $80.00      $212.50   -$132.50
Dan            $60.00      $152.50    -$92.50

SETTLEMENT — 3 transfers
  → Ben pays Ana $92.50
  → Cho pays Ana $132.50
  → Dan pays Ana $92.50
```

Weighted (rent split by occupants):

```bash
python3 scripts/settle_up.py --ledger rent.txt --weights "Ana:2,Ben:1,Cho:1"
```

## Why it matters

- Post-trip settlement friction is a real, measurable source of group
  conflict — the fair-share part is easy, the *tangle of pairwise debts* is
  what breaks down. Min-cash-flow netting collapses it to its minimum.
- Uses the same netting idea as interbank clearing: everyone reports net
  position, a greedy matcher zeroes the extremes, transfers are provably
  ≤ n−1.
- No app, no accounts, no ads, works offline on any machine with Python.

## Files

- `SKILL.md` — agent-facing usage guide
- `scripts/settle_up.py` — splitter + settler (stdlib only)
- `scripts/test_settle_up.py` — self-tests
- `references/settlement-theory.md` — netting algorithm, weighted splits,
  cent-exactness, privacy notes

## Test

```bash
python3 scripts/test_settle_up.py
```

MIT © 2026 Denis Voronin
