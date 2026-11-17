---
name: group-expense-settler
description: "Split group expenses fairly (equal or weighted shares) and compute the minimum number of money transfers to settle up. Reads a simple ledger of who paid for what, handles non-even splits, weights, and shared vs personal items, then produces an optimal settlement plan (who pays whom, how much) plus a fairness audit. Use when settling trip costs with friends, splitting rent and utilities among roommates, or running any shared-expense pool without a dedicated app."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [finance, splitting, shared-expenses, roommates, travel, settlements, fair-division]
---

# Group Expense Settler 👥💰

You went on a trip with five friends. Everyone paid for something — hotels,
gas, dinners, tickets. Now there's a tangle of "I paid for you there, you
paid for me here" that nobody can untangle. This skill reduces the whole mess
to **the fewest possible payments that make everyone whole**.

## Overview

Settling shared expenses has two separate problems, and most people conflate
them:

1. **Fairness** — how much *should* each person have contributed? (Split a
   dinner 5 ways; the grocery run only 3 ways; the rental car by days
   present.)
2. **Settlement** — given what everyone actually paid vs. their fair share,
   what's the cheapest set of transfers to square everything?

For #2 the naive approach ("everyone who underpaid pays the person who
overpaid the most") generates O(n²) transfers. The **min-cash-flow**
algorithm — greedy matching of the largest creditor against the largest
debtor — provably needs at most **n−1 transfers** and typically far fewer.
For a 6-person trip: 15 possible payment edges → usually **4 or 5 actual
transfers**.

`scripts/settle_up.py` implements:

- Ledger format: `payer,amount,people...` (+ optional `--weights` or per-item
  exclusions)
- **Net-position math**: for each person, `paid − fair_share = net`. Positive
  net = is owed money; negative = owes.
- **Min-cash-flow settlement** (max-creditor ↔ max-debtor greedy, exact to
  the cent, no rounding residue)
- Fairness audit table: paid / share / net per person
- Tolerance handling (± a cent) and "everyone's square within X" check
- JSON export for receipts and chat-pasteable settlement lines

## When to Use

- Settling after a group trip / weekend cabin / festival
- Monthly roommate settle-up: rent is uneven, utilities split evenly,
  someone bought shared groceries
- Any "we really don't need another app for this" moment — this runs offline
  from a terminal with a 3-line ledger
- Recurring clubs: gaming group, sports team dues, communal equipment

**Don't use for:** continuous running balances you want synced with a bank
(Splitwise et al.), or formal bookkeeping/double-entry accounting.

## How It Works — Steps

1. **Write the ledger** — one line per expense: who paid, total, who shares it:
   ```
   Ana,450,Ana Ben Cho Dan      # hotel, 4-way
   Ben,120,Ben Cho               # taxi, 2-way
   Cho,80,Ana Ben Cho Dan        # groceries all
   ```
2. **Run**:
   ```bash
   python3 scripts/settle_up.py --ledger trip.txt
   ```
3. **Read the net table** (who's owed / owes what) and the **settlement
   plan** — minimum transfers, each printed as a chat-ready sentence.
4. **Weighted splits** (room sizes, income shares, days attended):
   ```bash
   python3 scripts/settle_up.py --ledger rent.txt --weights "Ana:2,Ben:1,Cho:1"
   ```
5. **Audit** with `--show-items` to see every person's share of every line —
   settle arguments with arithmetic, not vibes.

## Algorithm (min-cash-flow, exact)

1. Compute each person's **net** = total paid − total fair share (integer
   cents).
2. Split into creditors (net > 0) and debtors (net < 0). Sum of both sides is
   equal — money is conserved.
3. Repeat: take **max creditor** and **max debtor**. Transfer
   `min(creditor.net, −debtor.net)`. One of them reaches exactly 0 and leaves
   the pool. Append the transfer.
4. Stop when all nets are 0. Transfers ≤ n−1, and the greedy choice
   maximizes the chance that each transfer zeroes someone out — the
   well-known heuristic used in payment-netting systems.
5. Cent-exactness: everything is integer cents from input onward; the split
   of an expense among k people distributes the remainder cents
   deterministically (earlier-listed people get the extra cent), so nets
   always sum to zero with **no leftover dust**.

## Worked Example

Ledger:
```
Ana,450,Ana Ben Cho Dan
Ben,120,Ben Cho
Cho,80,Ana Ben Cho Dan
Dan,60,Ben Cho Dan
```
Nets: Ana paid 450 / share 132.50 → **+317.50** · Ben paid 120 / share
212.50 → **−92.50** · Cho paid 80 / share 212.50 → **−132.50** · Dan paid
60 / share 152.50 → **−92.50**. (Check: 317.50 − 92.50 − 132.50 − 92.50 = 0 ✓)

Settlement (3 transfers, not up to 6):
```
Ben  pays Ana  $92.50
Cho  pays Ana  $132.50
Dan  pays Ana  $92.50
```
Everyone else is done — no "you pay me and I pay her" chains.

## Common Pitfalls

1. **Including the payer in the split list.** `Ana,450,Ana Ben Cho Dan`
   splits among all four *including Ana* — usually right. If Ana paid but
   isn't consuming, list only the consumers: `Ana,450,Ben Cho Dan`.
2. **Currency commas vs CSV commas.** Write `1200.50` not `1,200,50` —
   the ledger is comma-separated.
3. **Rounding debt.** The script is cent-exact; if you hand-round each
   person's share to whole dollars, nets won't sum to zero and someone will
   be a few cents short. Keep cents.
4. **Mixing currencies in one ledger.** All lines must be one currency.
   Convert first, note the rate.
5. **Trust but audit.** Run `--show-items` before announcing numbers; a typo
   in one amount silently shifts everyone's net.
6. **Weights must cover everyone in the ledger.** A person missing from
   `--weights` gets weight 1 silently — check the printed weight table.

## Verification Checklist

- [ ] Net column sums to exactly 0 (script asserts this internally)
- [ ] Number of transfers ≤ people − 1
- [ ] Every person appears at most once as payer in settlements (a person
      should never both pay and receive — script avoids this by design)
- [ ] `--show-items` totals match your receipts
- [ ] Same currency across all ledger lines

## One-Shot Recipes

**Trip settle-up with per-line participants:**
```bash
python3 scripts/settle_up.py --ledger trip.txt --show-items
```

**Roommates — rent weighted by room, utilities even:**
```
Ana,2400,Ana Ben Cho
utility,180,Ana Ben Cho
```
```bash
python3 scripts/settle_up.py --weights "Ana:2,Ben:1,Cho:1" --ledger rent.txt
```

**Paste-ready plan for the group chat:**
```bash
python3 scripts/settle_up.py --ledger trip.txt --json | python3 -c \
  "import json,sys; [print(t['line']) for t in json.load(sys.stdin)['transfers']]"
```
