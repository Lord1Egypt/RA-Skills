#!/usr/bin/env python3
"""Group Expense Settler — fair split + minimum-transfer settlement.

Pipeline:
  1. Parse ledger lines: payer,amount,participants...
  2. Split each expense among its participants (equal or weighted shares),
     cent-exact with deterministic remainder distribution.
  3. Net = paid - fair_share per person.
  4. Min-cash-flow: repeatedly match max creditor with max debtor.
  5. Print audit table + settlement plan (chat-ready lines).

All money is integer cents. No external dependencies.
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from fractions import Fraction


# ---------------------------------------------------------------------------
# Ledger parsing

@dataclass
class Expense:
    payer: str
    amount_c: int
    participants: list[str]

    def __str__(self):
        return f"{self.payer} paid {self.amount_c/100:.2f} for {', '.join(self.participants)}"


def parse_amount(s: str) -> int:
    s = s.strip().replace("$", "")
    cents = round(float(s) * 100)
    if cents < 0:
        raise ValueError(f"negative amount: {s}")
    return cents


def parse_ledger(text: str) -> list[Expense]:
    expenses = []
    for lineno, raw in enumerate(text.splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        parts = [p.strip() for p in line.split(",") if p.strip()]
        if len(parts) < 3:
            raise ValueError(f"line {lineno}: need payer,amount,participants — got {line!r}")
        payer, amount = parts[0], parse_amount(parts[1])
        # participants: space-separated within one field, or extra CSV fields
        people = [p for chunk in parts[2:] for p in chunk.split()]
        if not people:
            raise ValueError(f"line {lineno}: no participants in {line!r}")
        if len(set(people)) != len(people):
            raise ValueError(f"line {lineno}: duplicate participant in {line!r}")
        expenses.append(Expense(payer, amount, people))
    if not expenses:
        raise ValueError("ledger is empty")
    return expenses


# ---------------------------------------------------------------------------
# Fair split (cent-exact)

def split_cents(amount_c: int, people: list[str], weights: dict[str, int]) -> dict[str, int]:
    """Split amount among people ∝ weights, distributing remainder cents to
    the earliest-listed people. Sum of shares == amount exactly."""
    total_w = sum(weights.get(p, 1) for p in people)
    exact = {p: Fraction(amount_c * weights.get(p, 1), total_w) for p in people}
    shares = {p: int(v) for p, v in exact.items()}  # floor
    remainder = amount_c - sum(shares.values())
    # give leftover cents to people with largest fractional parts (stable)
    order = sorted(people, key=lambda p: (-(exact[p] - shares[p]), people.index(p)))
    for p in order[:remainder]:
        shares[p] += 1
    assert sum(shares.values()) == amount_c
    return shares


# ---------------------------------------------------------------------------
# Net + settlement

def compute_nets(expenses: list[Expense], weights: dict[str, int]):
    people = set()
    paid = {}
    share = {}
    item_shares = []
    for e in expenses:
        people.update(e.participants)
        paid[e.payer] = paid.get(e.payer, 0) + e.amount_c
        sh = split_cents(e.amount_c, e.participants, weights)
        item_shares.append((e, sh))
        for p, c in sh.items():
            share[p] = share.get(p, 0) + c
    people.update(paid)
    nets = {p: paid.get(p, 0) - share.get(p, 0) for p in people}
    assert sum(nets.values()) == 0, "nets must sum to zero"
    return sorted(people), paid, share, nets, item_shares


def min_cash_flow(nets: dict[str, int]) -> list[dict]:
    """Greedy max-creditor vs max-debtor. ≤ n-1 transfers, cent-exact."""
    creditors = {p: n for p, n in nets.items() if n > 0}
    debtors = {p: -n for p, n in nets.items() if n < 0}
    transfers = []
    while creditors and debtors:
        c = max(creditors, key=lambda p: (creditors[p], p))
        d = max(debtors, key=lambda p: (debtors[p], p))
        amount = min(creditors[c], debtors[d])
        transfers.append({
            "from": d, "to": c, "amount_c": amount,
            "line": f"{d} pays {c} ${amount/100:.2f}",
        })
        creditors[c] -= amount
        debtors[d] -= amount
        if creditors[c] == 0:
            del creditors[c]
        if debtors[d] == 0:
            del debtors[d]
    assert not creditors and not debtors, "settlement did not converge"
    return transfers


# ---------------------------------------------------------------------------
# Reporting

def fmt(c: int) -> str:
    sign = "-" if c < 0 else ""
    return f"{sign}${abs(c)/100:,.2f}"


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Split group expenses and settle with minimum transfers")
    p.add_argument("--ledger", required=True, help="file with lines: payer,amount,participant1,participant2,...")
    p.add_argument("--weights", help="e.g. 'Ana:2,Ben:1,Cho:1' — split proportional to weights")
    p.add_argument("--show-items", action="store_true", help="show each person's share of each expense")
    p.add_argument("--json", action="store_true", help="machine-readable output")
    args = p.parse_args(argv)

    weights = {}
    if args.weights:
        for pair in args.weights.split(","):
            name, _, w = pair.partition(":")
            weights[name.strip()] = int(w)

    try:
        text = open(args.ledger, encoding="utf-8").read()
        expenses = parse_ledger(text)
        people, paid, share, nets, item_shares = compute_nets(expenses, weights)
    except (OSError, ValueError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2

    transfers = min_cash_flow(nets)

    if args.json:
        print(json.dumps({
            "people": people,
            "paid": {p: paid.get(p, 0) / 100 for p in people},
            "fair_share": {p: share.get(p, 0) / 100 for p in people},
            "net": {p: nets[p] / 100 for p in people},
            "transfers": [{"from": t["from"], "to": t["to"], "amount": t["amount_c"] / 100, "line": t["line"]} for t in transfers],
        }, indent=2))
        return 0

    W = 68
    print("=" * W)
    print("GROUP EXPENSE SETTLER")
    print("=" * W)
    if weights:
        wparts = ", ".join(f"{k}×{v}" for k, v in weights.items())
        print(f"weights: {wparts}   (missing people = weight 1)")
    if args.show_items:
        print("\nITEM DETAIL")
        for e, sh in item_shares:
            print(f"  {e}")
            for person, c in sh.items():
                print(f"      {person:<10} {fmt(c):>12}")
    print(f"\n{'Person':<12}{'Paid':>13}{'Fair share':>13}{'Net':>13}")
    print("-" * W)
    for person in people:
        print(f"{person:<12}{fmt(paid.get(person,0)):>13}{fmt(share.get(person,0)):>13}{fmt(nets[person]):>13}")
    print("-" * W)
    print(f"{'TOTAL':<12}{fmt(sum(paid.values())):>13}{fmt(sum(share.values())):>13}{fmt(sum(nets.values())):>13}")

    print(f"\nSETTLEMENT — {len(transfers)} transfer{'s' if len(transfers)!=1 else ''}"
          f" (minimum possible ≤ {len(people)-1})")
    for t in transfers:
        print(f"  → {t['line']}")
    if not transfers:
        print("  everyone is already square 🎉")
    print("=" * W)
    return 0


if __name__ == "__main__":
    sys.exit(main())
