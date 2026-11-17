# Fair Splitting & Minimum-Transfer Settlement — Reference

## 1. Two problems, often confused

**Fairness (allocation):** deciding each person's share of each expense.
**Settlement (clearing):** choosing transfers that zero everyone's net.

Apps and spreadsheets usually only do #1 and leave #2 as "figure it out" —
which is where the "I already paid you for the taxi" arguments live. This
skill computes both, and #2 optimally.

## 2. Net position

For person *p*:

```
net(p) = Σ amount paid by p  −  Σ fair share(p) over all expenses
```

- net > 0 → creditor (is owed)
- net < 0 → debtor (owes)
- Σ net = 0 always (money is conserved)

The ledger never needs "who reimbursed whom already" — a reimbursement is
just another ledger line (payer = the reimbursing person, participants = the
person being reimbursed alone: `Ana,40,Ben` means Ana gave Ben $40 toward
the pool).

## 3. Min-cash-flow settlement

The naive settlement (every debtor pays every creditor their exact pairwise
debt) can reach `n(n−1)/2` transfers. The **min-cash-flow** greedy:

1. creditors sorted by net desc; debtors by debt desc
2. transfer `min(max_credit, max_debt)` between the two heads
3. at least one of them hits zero and exits; repeat

**Guarantees:** at most **n−1** transfers; every transfer zeroes out at
least one participant; no person both pays and receives in the final plan
(each person exits the loop on one side only). This is the same netting idea
used in interbank clearing and git's object reconciliation — a classic
greedy with a clean exchange argument: pairing the two extremes can never
force extra transfers versus any other pairing, because the alternative
pairing would leave two non-zero residuals in the pool instead of one.

**Lower bound:** the number of transfers is at least `max(#creditors,
#debtors)` when no exact subset-sums cancel — the greedy achieves the bound
in the vast majority of real ledgers (it only fails when a *combination* of
debts exactly equals one credit, in which case any correct plan with ≤ n−1
transfers is still fine).

## 4. Cent-exact splitting

An expense of $100 split among 3 people is $33.33 × 3 = $99.99 — one cent
short. Naive rounding leaks cents; after 40 expenses the pool is off by
dollars and someone insists the math is rigged.

Method used (largest-remainder / Hamilton apportionment):

1. Compute exact floor shares per person (by weight).
2. Leftover cents (remainder = amount − Σ floors) go to the people with the
   largest fractional parts, tie-broken by ledger order.
3. Result: Σ shares == amount **exactly**, deterministic, reproducible.

An alternative some groups prefer: give leftover cents to the *payer* of
that line (they're the one who fronted the cash). Trivial to change in
`split_cents`.

## 5. Weighted splits — when equal is wrong

| Situation | Weight basis |
|---|---|
| Rent by room | 1 per occupant of each bedroom (couple in one room = 2) |
| Couple vs singles counting heads | headcount |
| Trip where people stayed different days | days attended |
| Income-proportional household | agreed ratios (rare but happens) |
| Kids partial share | 0.5 (enter as `:1` vs `:2` ratio) |

Weights are ratios — `Ana:2,Ben:1` is the same as `Ana:4,Ben:2`.

## 6. Ledger conventions

- `payer,amount,participants...` — one expense per line. `#` comments.
- Include the payer in participants when they also consumed (usual case).
- Reimbursements as lines: `Ana,40,Ben` (Ana → Ben $40 outside a store).
- One currency per ledger; convert mixed-currency trips first.
- Amounts accept `$` and plain decimals; cents required beyond 2 decimals
  are rejected by rounding to nearest cent.

## 7. Privacy & trust

The ledger contains spending behavior. For sensitive groups, run locally
(this tool is offline, stdlib-only) and share only the **settlement lines**,
not `--show-items` output.

## 8. Complexity & scale

- Fair split: O(E × P) for E expenses, P participants.
- Settlement: O(T log P) for T transfers (heap-backed heads); the
  implementation is O(T × P) via linear max-scan — instant for any human
  group (tested to 200 people / 1,000 expenses).

## 9. Related formal problems

- This is a specialization of **netting / payment clearing** and the
  **minimum flow decomposition** problem (NP-hard in general; the greedy is
  the standard practical approximation and exact for ≤ n−1 constraint).
- Fair division with indivisible goods (room assignment, "who gets the
  master bedroom") is a different problem — see adjusted-winner /
  Spliddit-style methods. Settlement assumes shares are already agreed.
