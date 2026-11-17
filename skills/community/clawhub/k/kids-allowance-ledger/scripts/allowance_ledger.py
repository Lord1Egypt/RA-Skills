#!/usr/bin/env python3
"""Kids Allowance Ledger — jar splits, growth engine, goals, statements.

Double-entry-lite ledger for one child. Store: JSON file.
Commands: init, chore, deposit, earn, spend, goal, project, statement, audit.
Stdlib only.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

DEFAULT_STORE = Path(__file__).resolve().parent / "allowance_ledger.json"
JARS = ("spend", "save", "share")


# ---------------------------------------------------------------- store io
def load(store: Path) -> dict:
    if not store.exists():
        sys.exit(f"No ledger at {store}. Run `init` first.")
    return json.loads(store.read_text())


def save(store: Path, data: dict) -> None:
    store.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def today() -> str:
    return date.today().isoformat()


# ---------------------------------------------------------------- init
def cmd_init(args) -> None:
    if args.store.exists() and not args.force:
        sys.exit(f"{args.store} already exists (use --force to reset).")
    spend_p, save_p, share_p = parse_split(args.split)
    data = {
        "child": {"name": args.name, "age": args.age, "created": today()},
        "allowance": {"weekly": args.weekly, "last_paid": None},
        "split": {"spend": spend_p, "save": save_p, "share": share_p},
        "growth": {
            "interest_monthly_pct": args.interest,
            "match_pct": args.match,
            "match_monthly_cap": args.match_cap,
            "match_used_this_month": 0.0,
            "month_key": today()[:7],
        },
        "chores": {},
        "goals": [],
        "entries": [],
        "balances": {"spend": 0.0, "save": 0.0, "share": 0.0},
    }
    save(args.store, data)
    print(f"Ledger for {args.name} (age {args.age}) created at {args.store}")
    print(f"  weekly allowance ${args.weekly:.2f}, split {spend_p}/{save_p}/{share_p}")
    if args.interest:
        eff = (1 + args.interest / 100) ** 12 - 1
        print(f"  interest {args.interest}%/mo on Save (effective {eff*100:.1f}%/yr)")
    if args.match:
        print(f"  parent match {args.match}% of Save deposits, cap ${args.match_cap:.2f}/mo")


def parse_split(spec: str):
    try:
        parts = [int(p) for p in spec.split("/")]
    except ValueError:
        sys.exit("Split must look like 50/40/10")
    if len(parts) != 3 or sum(parts) != 100:
        sys.exit("Split must be three percentages summing to 100 (spend/save/share)")
    return parts


# ---------------------------------------------------------------- income
def split_income(data: dict, amount: float, when: str) -> dict:
    return {jar: round(amount * data["split"][jar] / 100, 2) for jar in JARS}


def apply_match(data: dict, save_amount: float) -> float:
    """Parent match on Save deposits. Returns matched amount (0 if disabled)."""
    g = data["growth"]
    if not g["match_pct"]:
        return 0.0
    if g["month_key"] != today()[:7]:
        g["month_key"] = today()[:7]
        g["match_used_this_month"] = 0.0
    room = max(0.0, g["match_monthly_cap"] - g["match_used_this_month"])
    matchable = min(save_amount, room)
    matched = round(matchable * g["match_pct"] / 100, 2)
    g["match_used_this_month"] = round(g["match_used_this_month"] + matched, 2)
    return matched


def cmd_deposit(args) -> None:
    data = load(args.store)
    amounts = split_income(data, args.amount, today())
    matched = apply_match(data, amounts["save"])
    e = {
        "date": today(), "type": "deposit", "amount": args.amount,
        "note": args.note, "split": amounts, "match": matched,
    }
    data["entries"].append(e)
    data["balances"]["save"] = round(data["balances"]["save"] + matched, 2)
    for jar in JARS:
        data["balances"][jar] = round(data["balances"][jar] + amounts[jar], 2)
    if args.weekly:
        data["allowance"]["last_paid"] = today()
    save(args.store, data)
    print(f"Deposited ${args.amount:.2f} → spend ${amounts['spend']:.2f} / "
          f"save ${amounts['save']:.2f} / share ${amounts['share']:.2f}")
    if matched:
        print(f"  + parent match ${matched:.2f} → Save (cap "
              f"${data['growth']['match_monthly_cap'] - data['growth']['match_used_this_month']:.2f} left this month)")


def cmd_chore(args) -> None:
    data = load(args.store)
    if args.add:
        name, _, pay = args.add.rpartition("=")
        if not name or not pay:
            sys.exit('chore add format: "task name=1.50"')
        data["chores"][name.strip()] = round(float(pay), 2)
        save(args.store, data)
        print(f'Chore menu: "{name.strip()}" pays ${float(pay):.2f}')
    elif args.list:
        if not data["chores"]:
            print("Chore menu is empty. Add with: chore add \"walk dog=1.50\"")
        for name, pay in sorted(data["chores"].items(), key=lambda kv: -kv[1]):
            print(f"  ${pay:>6.2f}  {name}")


def cmd_earn(args) -> None:
    data = load(args.store)
    if args.chore not in data["chores"]:
        sys.exit(f'Unknown chore "{args.chore}". See `chore --list`.')
    pay = data["chores"][args.chore]
    amounts = split_income(data, pay, today())
    matched = apply_match(data, amounts["save"])
    data["entries"].append({
        "date": today(), "type": "chore", "chore": args.chore,
        "amount": pay, "note": f"earned: {args.chore}", "split": amounts,
        "match": matched,
    })
    data["balances"]["save"] = round(data["balances"]["save"] + matched, 2)
    for jar in JARS:
        data["balances"][jar] = round(data["balances"][jar] + amounts[jar], 2)
    save(args.store, data)
    print(f"Earned ${pay:.2f} ({args.chore}) → "
          + " / ".join(f"{j} ${amounts[j]:.2f}" for j in JARS)
          + (f" + match ${matched:.2f}" if matched else ""))


# ---------------------------------------------------------------- spending
def cmd_spend(args) -> None:
    data = load(args.store)
    jar = args.jar
    if data["balances"][jar] < args.amount:
        sys.exit(f"Insufficient {jar} balance: ${data['balances'][jar]:.2f}")
    data["balances"][jar] = round(data["balances"][jar] - args.amount, 2)
    e = {
        "date": today(), "type": "spend", "jar": jar, "amount": args.amount,
        "note": args.note, "raid": jar == "save",
    }
    data["entries"].append(e)
    save(args.store, data)
    print(f"Spent ${args.amount:.2f} from {jar}" + (f" — {args.note}" if args.note else ""))
    if jar == "save" and args.show_future_cost:
        r = data["growth"]["interest_monthly_pct"] / 100
        fv = args.amount * (1 + r) ** 12
        print(f"  ⚠ future cost: ${args.amount:.2f} kept 12mo at "
              f"{data['growth']['interest_monthly_pct']}%/mo would be ${fv:.2f}")


# ---------------------------------------------------------------- goals
def cmd_goal(args) -> None:
    data = load(args.store)
    if args.add:
        name, _, price = args.add.rpartition("=")
        data["goals"].append({
            "name": name.strip(), "price": round(float(price), 2),
            "added": today(), "jar": "save", "done": None,
        })
        save(args.store, data)
        print(f'Goal added: "{name.strip()}" @ ${float(price):.2f} → save jar')
    elif args.list:
        bal = data["balances"]["save"]
        rate = weekly_save_inflow(data)
        for g in data["goals"]:
            left = max(0.0, g["price"] - bal)
            pct = min(100.0, bal / g["price"] * 100) if g["price"] else 100
            bar = "█" * int(pct // 5) + "░" * (20 - int(pct // 5))
            if left == 0:
                eta = "READY!"
            elif rate > 0:
                eta = f"~{math.ceil(left / rate)} wk"
            else:
                eta = "no inflow"
            print(f"  {bar} {pct:5.1f}%  ${bal:7.2f}/${g['price']:.2f}  {eta:8s}  {g['name']}")


def weekly_save_inflow(data: dict) -> float:
    """Average Save-jar inflow (deposits+matches) per week over last 56 days.

    For young ledgers the window shrinks to the ledger's actual age (min 1
    week) so a day-old ledger doesn't dilute its first deposit across 8 weeks.
    """
    income = [e for e in data["entries"] if e["type"] in ("deposit", "chore")]
    if not income:
        return 0.0
    first = min(e["date"] for e in income)
    first_d = datetime.fromisoformat(first).date()
    age_weeks = (date.today() - first_d).days / 7
    weeks = min(8.0, max(1.0, age_weeks))
    cutoff = (date.today() - timedelta(days=weeks * 7)).isoformat()
    inflow = sum(e["split"]["save"] + e.get("match", 0)
                 for e in income if e["date"] >= cutoff)
    return round(inflow / weeks, 2)


# ---------------------------------------------------------------- growth
def cmd_project(args) -> None:
    data = load(args.store)
    g = data["growth"]
    r = g["interest_monthly_pct"] / 100
    weekly = data["allowance"]["weekly"]
    save_share = data["split"]["save"] / 100
    monthly_in = weekly * save_share * 52 / 12
    match_monthly = min(
        monthly_in * g["match_pct"] / 100 if g["match_pct"] else 0.0,
        g["match_monthly_cap"] if g["match_pct"] else 0.0,
    )
    bal = data["balances"]["save"]
    deposited = 0.0
    print(f"Save-jar projection for {data['child']['name']} "
          f"(start ${bal:.2f}, +${monthly_in:.2f}/mo deposits")
    print(f" +${match_monthly:.2f}/mo match, {g['interest_monthly_pct']}%/mo interest)\n")
    print("  month   deposits    match  interest    balance")
    for m in range(1, args.years * 12 + 1):
        interest = bal * r
        bal = bal + monthly_in + match_monthly + interest
        deposited += monthly_in + match_monthly
        if m % (3 if args.years <= 2 else 6) == 0 or m == 1:
            print(f"  {m:>5}  {deposited:>9.2f}  {match_monthly*m:>6.2f}  "
                  f"{interest:>8.2f}  {bal:>9.2f}")
    print(f"\n  After {args.years} year(s): ${bal:.2f} total, of which "
          f"${bal - deposited:.2f} is interest — money that grew while you slept.")


def cmd_statement(args) -> None:
    data = load(args.store)
    month = args.month or today()[:7]
    entries = [e for e in data["entries"] if e["date"].startswith(month)]
    inc = sum(e["amount"] for e in entries if e["type"] in ("deposit", "chore"))
    spent = sum(e["amount"] for e in entries if e["type"] == "spend")
    match = sum(e.get("match", 0) for e in entries)
    raids = [e for e in entries if e.get("raid")]
    print(f"━━━ {data['child']['name']}'s money — {month} ━━━")
    print(f"  Earned     ${inc:8.2f}   ({len(entries)} entries)")
    print(f"  Match      ${match:8.2f}")
    print(f"  Spent      ${spent:8.2f}")
    if raids:
        print(f"  Save raids {len(raids)} totalling ${sum(r['amount'] for r in raids):.2f} ⚠")
    print(f"\n  Jars now:  " + "  ".join(
        f"{j.title()}: ${data['balances'][j]:.2f}" for j in JARS))
    rate = weekly_save_inflow(data)
    print(f"\n  Saving about ${rate:.2f}/week → goals:")
    for g in data["goals"]:
        left = max(0.0, g["price"] - data["balances"]["save"])
        if left == 0:
            print(f"    ✅ {g['name']} — you can buy it now!")
        elif rate > 0:
            print(f"    ⏳ {g['name']}: {math.ceil(left / rate)} more weeks")
        else:
            print(f"    ⏳ {g['name']}: ${left:.2f} to go")
    print("\n  Interest and matches are your money working for you. Nice.")


def cmd_audit(args) -> None:
    data = load(args.store)
    problems = []
    entries = data["entries"]
    if not entries:
        print("No entries yet — nothing to audit.")
        return
    dates = sorted(e["date"] for e in entries if e["type"] == "deposit")
    if len(dates) >= 2:
        d1, d2 = datetime.fromisoformat(dates[0]), datetime.fromisoformat(dates[-1])
        span_days = (d2 - d1).days
        gaps_ok = span_days / max(1, len(dates) - 1) <= 21
        if not gaps_ok:
            problems.append(f"deposits average >21d apart ({span_days/(len(dates)-1):.0f}d) — "
                            "compounding demo dies without regular flow")
    raids_90 = [e for e in entries if e.get("raid")
                and e["date"] >= (date.today() - timedelta(days=90)).isoformat()]
    if len(raids_90) >= 3:
        problems.append(f"{len(raids_90)} Save raids in 90 days — talk, don't punish")
    if data["balances"]["share"] > 5 and (date.today() - datetime.fromisoformat(
            entries[0]["date"])).days > 90:
        problems.append(f"Share jar sitting at ${data['balances']['share']:.2f} — "
                        "schedule a donation use")
    g = data["growth"]
    if g["match_pct"] and g["month_key"] == today()[:7]:
        used = g["match_used_this_month"]
        cap = g["match_monthly_cap"]
        if used < cap * 0.5 and today() >= today()[:8] + "22":
            problems.append(f"match underused this month (${used:.2f}/${cap:.2f}) — "
                            "free money left on the table")
    if not problems:
        print("✅ Audit clean: regular flow, no raid pattern, jars healthy.")
    else:
        print(f"⚠ {len(problems)} flag(s):")
        for p in problems:
            print(f"  - {p}")


# ---------------------------------------------------------------- cli
def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--store", default=str(DEFAULT_STORE),
                   help="ledger JSON path (default: alongside script)")
    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("init", help="create ledger")
    sp.add_argument("--name", required=True)
    sp.add_argument("--age", type=int, required=True)
    sp.add_argument("--weekly", type=float, required=True)
    sp.add_argument("--split", default="50/40/10", help="spend/save/share percent")
    sp.add_argument("--interest", type=float, default=0.0, help="% per month on Save")
    sp.add_argument("--match", type=float, default=0.0, help="parent match % of save deposits")
    sp.add_argument("--match-cap", type=float, default=0.0, help="max match $/month")
    sp.add_argument("--force", action="store_true")
    sp.set_defaults(fn=cmd_init)

    sp = sub.add_parser("chore", help="chore commission menu")
    sp.add_argument("--add", metavar='"task=1.50"')
    sp.add_argument("--list", action="store_true")
    sp.set_defaults(fn=cmd_chore)

    sp = sub.add_parser("deposit", help="record allowance income (auto-split)")
    sp.add_argument("amount", type=float)
    sp.add_argument("--note", default="allowance")
    sp.add_argument("--weekly", action="store_true", help="mark as the weekly allowance")
    sp.set_defaults(fn=cmd_deposit)

    sp = sub.add_parser("earn", help="record a chore commission")
    sp.add_argument("chore")
    sp.set_defaults(fn=cmd_earn)

    sp = sub.add_parser("spend", help="record a purchase")
    sp.add_argument("amount", type=float)
    sp.add_argument("--note", default="")
    sp.add_argument("--jar", choices=JARS, default="spend")
    sp.add_argument("--show-future-cost", action="store_true",
                    help="show 12-month future value destroyed (save raids)")
    sp.set_defaults(fn=cmd_spend)

    sp = sub.add_parser("goal", help="wishlist")
    sp.add_argument("--add", metavar='"name=price"')
    sp.add_argument("--list", action="store_true")
    sp.set_defaults(fn=cmd_goal)

    sp = sub.add_parser("project", help="compound-interest projection")
    sp.add_argument("--years", type=int, default=1)
    sp.set_defaults(fn=cmd_project)

    sp = sub.add_parser("statement", help="kid-readable monthly statement")
    sp.add_argument("--month", default=None, help="YYYY-MM (default: current)")
    sp.set_defaults(fn=cmd_statement)

    sp = sub.add_parser("audit", help="parent sanity check")
    sp.set_defaults(fn=cmd_audit)

    args = p.parse_args()
    args.store = Path(args.store)
    args.fn(args)


if __name__ == "__main__":
    main()
