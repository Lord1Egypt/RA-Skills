# kids-allowance-ledger

Turn allowance into a money-education system: jar splits (Spend/Save/Share),
parent-paid compound interest, 401(k)-style matching, wishlist goals with real
ETAs, kid-readable monthly statements, and a parent audit that flags raid
patterns before they become habits.

## The real-world problem

Parents hand kids money with no structure — and the money teaches nothing.
Financial-literacy frameworks (CFPB "Money as You Grow", Kobliner, Jump$tart)
agree on what actually works at ages 5–18:

1. **Partitioning** — split money the moment it arrives, visibly.
2. **Visible growth** — compound interest at a scale a child can *watch* beat
   spending (real bank rates of 0.1%/mo are invisible at $2/week).
3. **Goal friction** — a real wishlist with real weeks-to-purchase math.

This skill runs all three as a single-file Python ledger. Every deposit
auto-splits into jars; the Save jar earns parent-paid interest and/or a
parent match; `project` prints the compounding curve; `statement` gives the
kid a monthly win-report; `audit` gives the parent early-warning flags
(raid frequency, stagnant Share jar, unclaimed match).

## Install

Requires Python 3.9+ (stdlib only). No dependencies.

## Quick start

```bash
cd scripts
python3 allowance_ledger.py init --name Mia --age 8 --weekly 5 \
  --split 50/40/10 --interest 5 --match 50 --match-cap 10
python3 allowance_ledger.py chore --add "walk dog=1.50"
python3 allowance_ledger.py chore --add "car wash=5.00"
python3 allowance_ledger.py deposit 5.00 --note "weekly allowance" --weekly
python3 allowance_ledger.py earn "walk dog"
python3 allowance_ledger.py goal --add "LEGO set=89.99"
python3 allowance_ledger.py project --years 2
python3 allowance_ledger.py statement
python3 allowance_ledger.py audit
```

## How it works

- **Income** = weekly allowance + chore commissions (above-baseline tasks only).
- **Split** = configurable spend/save/share percentages per child.
- **Growth** = monthly interest on Save balance and/or %-match on Save deposits
  with a monthly cap (a literal 401(k) demo: "every $1 you save becomes $1.50").
- **Goals** = price − balance ÷ weekly Save inflow (8-week rolling) = ETA.
- **Raid pricing** = spending from Save prints the 12-month future value
  destroyed — the single strongest teaching moment in the tool.
- **Audit** = flags: deposit gaps > 21d, 3+ Save raids/90d, Share jar unused
  > 90 days, match underused late in month.

Data lives in `allowance_ledger.json` next to the script (`--store` to override).

## Age-banded defaults

| Age | Weekly base | Split (S/S/Sh) | Engine |
|-----|-------------|----------------|--------|
| 5–7  | age/2 $/wk  | 30/60/10 | 3 jars, counting only |
| 8–11 | $1/yr of age| 50/40/10 | 5%/mo interest |
| 12–15| 1.5×age     | 40/50/10 | 50% match up to cap |
| 16–18| 2×age       | 30/60/10 | match + budget categories |

## License

MIT © Denis Voronin
