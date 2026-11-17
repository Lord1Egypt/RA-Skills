#!/usr/bin/env python3
"""Layoff deadline tracker — deadline cascade, severance math, COBRA option,
401(k) loan trap, week-one checklist.

Subcommands:
  map        Dated deadline cascade from termination day
  severance  Offer benchmark + WARN + ADEA windows
  cobra      COBRA-vs-marketplace decision with retroactive-window math
  401kloan   Deemed-distribution cost + repayment options
  checklist  Final-pay + week-one structure

Stdlib only. Offline. General information, not legal/financial advice.
"""
import argparse
import json
from datetime import date, timedelta

PTO_STATES = {  # accrued PTO payout required at termination (non-exhaustive)
    "ca": "required (wages)",
    "co": "required per policy/contract",
    "il": "no state requirement",
    "ny": "required per policy",
    "tx": "no state requirement (policy governs)",
    "wa": "required if policy promises it",
    "ma": "required (wages)",
    "nj": "required per policy",
    "fl": "no state requirement",
    "pa": "no state requirement",
    "oh": "no state requirement",
    "ga": "no state requirement",
    "nc": "no state requirement",
    "az": "required if policy promises it",
    "nv": "required if policy promises it",
    "md": "required if policy promises it",
    "mn": "required if policy promises it",
    "or": "required (wages)",
    "wi": "no state requirement",
    "mi": "no state requirement",
    "va": "no state requirement",
    "ut": "no state requirement",
    "in": "no state requirement",
    "mo": "no state requirement",
    "tn": "no state requirement",
    "az2": "required if policy promises it",
}
NC_BAN = {"ca", "ok", "nd", "dc"}


def daterange_str(d):
    return d.isoformat()


def cmd_map(a):
    d0 = date.fromisoformat(a.date)
    rows = []
    rows.append((d0, "TERMINATION DAY",
                 "collect: signed offer letter, plan documents, equity grant agreements, policy manual; personal copies of everything (contacts, files, email addresses)"))
    rows.append((d0 + timedelta(days=1), "FILE UNEMPLOYMENT",
                 "most states do NOT backdate; benefits start from the filing week. Severance interplay varies by state — file, let them adjudicate"))
    rows.append((d0 + timedelta(days=14), "EQUITY AUDIT",
                 "pull every grant agreement: post-termination exercise windows (options commonly 90 days; ISO status + AMT -> CPA before exercising)"))
    if a.over40:
        rows.append((d0 + timedelta(days=21), "ADEA CONSIDERATION ENDS",
                     "21 days to consider the release (45 for group layoffs); +7-day revocation after signing — nothing final for a week"))
    rows.append((d0 + timedelta(days=30), "401(k) LOAN CURE PERIOD ALARM",
                 "plan-document deadline for loan repayment — if shorter than the tax-date rule, this is when it bites. Deemed distribution = income + 10% penalty"))
    rows.append((d0 + timedelta(days=45), "COBRA CHECKPOINT 1",
                 "any big claims so far? if yes -> elect (retroactive). if no -> stay the course"))
    rows.append((d0 + timedelta(days=55), "COBRA CHECKPOINT 2 — DECIDE",
                 "elect only if claims occurred; marketplace special enrollment also lapses ~day 60 (no retroactive coverage there)"))
    rows.append((d0 + timedelta(days=60), "COBRA ELECTION DEADLINE",
                 "60 days from loss or notice, whichever later. Miss it = no retroactive safety net"))
    rows.append((d0 + timedelta(days=60), "MARKETPLACE SEP DEADLINE",
                 "special enrollment for losing coverage — coverage starts only going forward"))
    rows.append((d0 + timedelta(days=90), "EQUITY EXERCISE WINDOW (typical)",
                 "common default for vested options; check YOUR grant agreement — ISO/NSO tax split matters"))
    rows.append((date(d0.year + 1, 4, 15), "TAX DATE",
                 "1099-R/RSA income lands here: severance flat withholding 22/37% may under-withhold; 401k deemed distributions show up; consider estimated payment"))
    rows.sort(key=lambda r: r[0])
    print(f"LAYOFF DEADLINE MAP — terminated {d0.isoformat()} ({a.state.upper()})")
    for when, what, why in rows:
        print(f"  {when.isoformat()}  {what}")
        print(f"    -> {why}")
    pto = PTO_STATES.get(a.state.lower())
    if pto:
        print()
        print(f"PTO payout ({a.state.upper()}): {pto} — verify final paycheck line items")
    if a.state.lower() in NC_BAN:
        print(f"NON-COMPETE ({a.state.upper()}): banned for most workers — if the release contains one, that's a negotiation flag")
    print()
    print("WARN Act: 0 days' notice + group layoff of 50+ at your site (employer 100+) =>")
    print("  60 days' back pay may be OWED — benchmark your severance against it.")
    return {"deadlines": len(rows)}


def cmd_severance(a):
    weekly = a.salary if a.salary else 0
    print("SEVERANCE BENCHMARK")
    if weekly and a.weeks:
        per_week = a.offer / a.weeks
        print(f"  Offer ${a.offer:,} over {a.weeks} weeks = ${per_week:,.0f}/week")
        if weekly:
            print(f"  Your weekly salary ${weekly:,.0f} -> offer = {per_week/weekly:.1f}x weekly pay")
    print("  Common band: 1-2 weeks of pay per year of service (exec higher).")
    print("  Below band + no notice pay + group layoff -> WARN Act math applies.")
    if a.notice:
        print(f"  Notice pay provided: {a.notice} days (WARN floor = 60 for covered group events)")
    print()
    print("OWED REGARDLESS OF SIGNING (not consideration):")
    for line in (
        "  - accrued PTO (state law / policy)",
        "  - completed bonus + proration per plan",
        "  - vested equity + expense reimbursements",
    ):
        print(line)
    print()
    print("WHAT THE RELEASE BUYS (price each): non-disparagement, reference")
    print("terms, benefits extension, outplacement, equity exercise-window")
    print("extension, no-rehire clause REMOVAL.")
    return {"offer": a.offer, "weeks": a.weeks}


def cmd_cobra(a):
    full = a.cost * a.months
    print("COBRA vs MARKETPLACE — the option-pricing view")
    print(f"  COBRA full cost if elected for max term: ${full:,.0f} "
          f"(${a.cost:,.0f}/mo x {a.months})")
    print()
    print("THE PLAY: the 60-day election window is a FREE LOOK.")
    print(f"  Scenario A — no big claims in window: pay $0, enroll marketplace")
    print(f"    (severance-year income usually qualifies for premium tax credits)")
    # electing retroactively means paying premiums from loss date onward
    elect_outlay = a.cost * max(1, min(a.months, 3))  # ~3 months typical bridge
    print(f"  Scenario B — ${a.events:,.0f} of claims happen on day 20: elect on")
    print(f"    day 55, premiums back-dated (~${elect_outlay:,.0f} for a 3-month")
    print(f"    bridge), claim covered — electing beats eating ${a.events:,.0f}")
    print(f"    whenever claims > the back-paid premiums.")
    if a.events <= elect_outlay:
        print(f"    NOTE: ${a.events:,.0f} of claims < ${elect_outlay:,.0f} bridge")
        print(f"    premiums — in THIS scenario eating it (or negotiating) is cheaper.")
    print()
    print("MARKETPLACE: special enrollment 60 days; NOT retroactive.")
    print("  Estimate credits at healthcare.gov with severance-only income;")
    print("  a Silver plan is often near-free where COBRA costs full price.")
    print("DECISION CALENDAR: day 45 checkpoint, day 55 decide, day 60 hard stop.")
    return {"cobra_full": full, "claims": a.events}


def cmd_401kloan(a):
    print("401(k) LOAN AT TERMINATION — the silent conversion")
    tax = a.loan * (a.taxrate / 100.0)
    penalty = a.loan * 0.10 if a.age < 59.5 else 0.0
    print(f"  Outstanding loan: ${a.loan:,}")
    print(f"  If deemed distributed: tax ${tax:,.0f} ({a.taxrate}%) + penalty "
          f"${penalty:,.0f} = ${tax+penalty:,.0f} gone")
    print()
    print("OPTIONS")
    for line in (
        "  1. Lump-sum repay from severance (usually cheapest)",
        f"     -> cost ${a.loan:,} of cash but saves ${tax+penalty:,.0f} tax hit + keeps compounding",
        "  2. Loan-offset rollover into IRA by extended tax due date (if plan reports offset)",
        "  3. New employer plan accepting loan rollovers (rare)",
        "  4. Do nothing -> 1099-R next January, taxed as above",
    ):
        print(line)
    print()
    print("READ THE PLAN DOCUMENT TONIGHT: cure periods vary (30-90 days in many")
    print("plans; older plans allow repayment by the tax-return due date).")
    if a.age >= 55:
        print()
        print(f"AGE {a.age} BONUS: separator rule — leave money IN the employer plan")
        print("  and withdrawals after separation at 55+ skip the 10% penalty.")
        print("  Rolling everything to an IRA DESTROYS this. Split the rollover.")
    return {"loan": a.loan, "deemed_cost": round(tax + penalty, 2)}


def cmd_checklist(a):
    print("WEEK-ONE CHECKLIST")
    for i, line in enumerate((
        "File unemployment (first eligible week — most states don't backdate)",
        "Copy plan documents, equity grants, handbook, performance reviews",
        "Personal-data export: contacts, files, email (before access dies)",
        "Final-pay audit: PTO payout (state rule), bonus proration, expenses",
        "References: 2-3 people who will vouch; LinkedIn 'Open to Work' (recruiter-only mode if stealth)",
        "Health: refill prescriptions at plan rates NOW; transfer records",
        "FSA: spend it down (use-it-or-lose-it; HSA survives forever)",
        "Budget: severance runway math (fixed costs x months)",
        "Calendar: every date from `map` output into phone + paper",
    ), 1):
        print(f"  {i}. {line}")
    return {"items": 9}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--json", action="store_true")
    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("map")
    sp.add_argument("--date", required=True)
    sp.add_argument("--state", default="ca")
    sp.add_argument("--over40", action="store_true")
    sp.set_defaults(fn=cmd_map)

    sp = sub.add_parser("severance")
    sp.add_argument("--offer", type=float, required=True)
    sp.add_argument("--weeks", type=int, required=True)
    sp.add_argument("--salary", type=float, default=None, help="weekly salary")
    sp.add_argument("--notice", type=int, default=0, help="notice days provided")
    sp.set_defaults(fn=cmd_severance)

    sp = sub.add_parser("cobra")
    sp.add_argument("--cost", type=float, required=True, help="monthly premium")
    sp.add_argument("--months", type=int, default=18)
    sp.add_argument("--events", type=float, default=2500,
                    help="hypothetical claim size inside window")
    sp.set_defaults(fn=cmd_cobra)

    sp = sub.add_parser("401kloan")
    sp.add_argument("--balance", type=float, default=0)
    sp.add_argument("--loan", type=float, required=True)
    sp.add_argument("--age", type=int, required=True)
    sp.add_argument("--taxrate", type=float, default=24)
    sp.set_defaults(fn=cmd_401kloan)

    sp = sub.add_parser("checklist")
    sp.set_defaults(fn=cmd_checklist)

    a = p.parse_args()
    out = a.fn(a)
    if a.json:
        print(json.dumps(out, indent=2, default=str))


if __name__ == "__main__":
    main()
