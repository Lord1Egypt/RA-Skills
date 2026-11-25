#!/usr/bin/env python3
"""passport_radar.py — family travel-document validity radar.

Subcommands:
  demo            run against a built-in demo family registry
  add             add a document to the registry (interactive flags)
  status          days-to-expiry bands for every document
  check           trip check: applies destination validity rules per passport
Registry default: ~/.passport_radar.json  (override with --registry PATH)
Stdlib only. Dates are ISO YYYY-MM-DD.
"""
import argparse
import json
import sys
from datetime import date, timedelta
from pathlib import Path

REGISTRY_DEFAULT = Path.home() / ".passport_radar.json"

# --- destination entry rules -------------------------------------------------
# kind: 'beyond_arrival' months / 'beyond_exit' months / 'valid_for_stay'
# pages: minimum blank pages sometimes enforced
DESTINATION_RULES = {
    "TH": {"name": "Thailand", "kind": "beyond_arrival", "months": 6, "pages": 1},
    "CN": {"name": "China", "kind": "beyond_arrival", "months": 6, "pages": 2},
    "EG": {"name": "Egypt", "kind": "beyond_arrival", "months": 6, "pages": 1},
    "TR": {"name": "Turkey", "kind": "beyond_arrival", "months": 5, "pages": 1},
    "ID": {"name": "Indonesia", "kind": "beyond_arrival", "months": 6, "pages": 1},
    "AE": {"name": "UAE", "kind": "beyond_arrival", "months": 6, "pages": 1},
    "VN": {"name": "Vietnam", "kind": "beyond_arrival", "months": 6, "pages": 1},
    "SG": {"name": "Singapore", "kind": "beyond_arrival", "months": 6, "pages": 1},
    "MX": {"name": "Mexico", "kind": "valid_for_stay", "months": 0, "pages": 1},
    "US": {"name": "United States", "kind": "valid_for_stay", "months": 0, "pages": 1},
    "CA": {"name": "Canada", "kind": "valid_for_stay", "months": 0, "pages": 1},
    "GB": {"name": "United Kingdom", "kind": "valid_for_stay", "months": 0, "pages": 1},
    "JP": {"name": "Japan", "kind": "valid_for_stay", "months": 0, "pages": 1},
    "CR": {"name": "Costa Rica", "kind": "valid_for_stay", "months": 0, "pages": 1},
    "ZA": {"name": "South Africa", "kind": "beyond_arrival", "months": 0, "pages": 2},  # 2 facing blank pages
    "BR": {"name": "Brazil", "kind": "valid_for_stay", "months": 0, "pages": 1},
    "AR": {"name": "Argentina", "kind": "valid_for_stay", "months": 0, "pages": 1},
    "IN": {"name": "India", "kind": "beyond_arrival", "months": 6, "pages": 2},
    "MA": {"name": "Morocco", "kind": "valid_for_stay", "months": 0, "pages": 1},
    "AU": {"name": "Australia", "kind": "valid_for_stay", "months": 0, "pages": 1},
    "NZ": {"name": "New Zealand", "kind": "valid_for_stay", "months": 0, "pages": 1},
    # Schengen (3 months beyond intended EXIT, issued within last 10 years)
    "FR": {"name": "France (Schengen)", "kind": "beyond_exit", "months": 3, "pages": 1, "schengen": True},
    "DE": {"name": "Germany (Schengen)", "kind": "beyond_exit", "months": 3, "pages": 1, "schengen": True},
    "IT": {"name": "Italy (Schengen)", "kind": "beyond_exit", "months": 3, "pages": 1, "schengen": True},
    "ES": {"name": "Spain (Schengen)", "kind": "beyond_exit", "months": 3, "pages": 1, "schengen": True},
    "GR": {"name": "Greece (Schengen)", "kind": "beyond_exit", "months": 3, "pages": 1, "schengen": True},
    "PT": {"name": "Portugal (Schengen)", "kind": "beyond_exit", "months": 3, "pages": 1, "schengen": True},
    "NL": {"name": "Netherlands (Schengen)", "kind": "beyond_exit", "months": 3, "pages": 1, "schengen": True},
    "CH": {"name": "Switzerland (Schengen)", "kind": "beyond_exit", "months": 3, "pages": 1, "schengen": True},
    "AT": {"name": "Austria (Schengen)", "kind": "beyond_exit", "months": 3, "pages": 1, "schengen": True},
    "NO": {"name": "Norway (Schengen)", "kind": "beyond_exit", "months": 3, "pages": 1, "schengen": True},
    "IS": {"name": "Iceland (Schengen)", "kind": "beyond_exit", "months": 3, "pages": 1, "schengen": True},
}

# renewal processing bands (weeks) — US example; see references for other issuers
RENEWAL_TIERS = [
    ("routine", 8),      # submit at least 8 weeks before needed
    ("expedited (+$60)", 3),
    ("urgent agency appt (<=14 days before travel)", 2),
]

BANDS = [  # (label, max_days)
    ("EXPIRED", 0), ("RENEW NOW", 90), ("PLAN", 180), ("OK", 10**6),
]

DEMO_REGISTRY = {
    "family": [
        {"traveler": "Mom", "type": "passport", "issuer": "US", "number_tail": "4821",
         "expires": "2029-03-01", "blank_pages": 12},
        {"traveler": "Dad", "type": "passport", "issuer": "US", "number_tail": "9917",
         "expires": "2027-04-02", "blank_pages": 8},
        {"traveler": "Kid", "type": "passport", "issuer": "US", "number_tail": "3320",
         "expires": "2026-12-15", "blank_pages": 6, "child": True},
        {"traveler": "Mom", "type": "drivers_license", "issuer": "US-CA", "number_tail": "7712",
         "expires": "2027-01-30"},
        {"traveler": "Dad", "type": "global_entry", "issuer": "US", "number_tail": "0055",
         "expires": "2028-06-11"},
    ]
}


def parse_d(s: str) -> date:
    return date.fromisoformat(s)


def load_registry(path: Path) -> dict:
    if not path.exists():
        sys.exit(f"No registry at {path}. Create one with `add` or run `demo`.")
    return json.loads(path.read_text())


def band_for(days_left: int) -> str:
    for label, mx in BANDS:
        if days_left < mx if mx != 0 else days_left < 0:
            return label
    for label, mx in BANDS:  # fallback ordering
        if days_left <= mx:
            return label
    return "OK"


def cmd_status(args):
    reg = load_registry(Path(args.registry))
    today = date.today()
    print(f"DOCUMENT STATUS — {today} (registry: {args.registry})")
    print("=" * 72)
    rows = []
    for d in reg["family"]:
        exp = parse_d(d["expires"])
        days = (exp - today).days
        rows.append((days, d, exp))
    for days, d, exp in sorted(rows, key=lambda r: r[0]):
        tag = " CHILD" if d.get("child") else ""
        print(f"{d['traveler']:<6} {d['type']:<15} exp {d['expires']}  "
              f"{days:>6} days  [{band_for(days)}]{tag}")
    # renewal back-plans for anything under 180 days
    print("-" * 72)
    for days, d, exp in rows:
        if days <= 180:
            for tier, weeks in RENEWAL_TIERS:
                deadline = today + timedelta(days=days - 7 * (weeks + 1))
                print(f"{d['traveler']} {d['type']}: {tier:<42} submit by {deadline}")
            break


def cmd_check(args):
    rule = DESTINATION_RULES.get(args.dest.upper())
    if not rule:
        sys.exit(f"Unknown destination '{args.dest}'. Known: {', '.join(sorted(DESTINATION_RULES))} "
                 "(see references/destination-rules.md for the full list and how to verify)")
    arrival, exit_ = parse_d(args.arrival), parse_d(args.exit or args.arrival)
    if rule["kind"] == "beyond_arrival":
        required_through = arrival + timedelta(days=30 * rule["months"])
        req_txt = f"valid >= {rule['months']} months beyond arrival ({required_through})"
    elif rule["kind"] == "beyond_exit":
        required_through = exit_ + timedelta(days=30 * rule["months"])
        req_txt = (f"valid >= {rule['months']} months beyond exit "
                   f"({required_through}); issued within last 10 years")
    else:
        required_through = exit_
        req_txt = f"valid for duration of stay (through {required_through})"

    print(f"{rule['name'].upper()}: passport must be {req_txt}")
    print("=" * 72)
    reg = load_registry(Path(args.registry))
    today = date.today()
    blockers = 0
    for d in reg["family"]:
        if d["type"] != "passport":
            continue
        exp = parse_d(d["expires"])
        tail = d.get("number_tail", "****")
        if exp < arrival:
            verdict, why = "BLOCKED", "expires before arrival"
            blockers += 1
        elif exp < required_through:
            short = (required_through - exp).days
            verdict = "RENEW-FIRST"
            why = f"expires {short} days before required validity date"
            blockers += 1
        else:
            verdict, why = "CLEARED", f"valid past {required_through} (+{(exp-required_through).days}d margin)"
        pages_ok = d.get("blank_pages", 99) >= rule["pages"]
        page_note = "" if pages_ok else f"  !! blank pages < {rule['pages']}"
        tag = " CHILD" if d.get("child") else ""
        print(f"{d['traveler']:<6} P***{tail} exp {d['expires']}  {verdict:<12} {why}{tag}{page_note}")

    # renewal tier feasibility for the worst document
    print("-" * 72)
    for d in reg["family"]:
        if d["type"] != "passport":
            continue
        exp = parse_d(d["expires"])
        if exp >= required_through:
            continue
        for tier, weeks in RENEWAL_TIERS:
            latest = arrival - timedelta(days=7) - timedelta(weeks=weeks)
            print(f"{d['traveler']}: {tier:<42} must submit by {latest}")
        break
    print(f"\nTRIP VERDICT: {'GO — all documents cleared' if blockers == 0 else f'NO-GO until {blockers} document(s) renewed'}")


def cmd_add(args):
    p = Path(args.registry)
    reg = load_registry(p) if p.exists() else {"family": []}
    reg["family"].append({
        "traveler": args.traveler, "type": args.type, "issuer": args.issuer,
        "number_tail": args.tail or "", "expires": args.expires,
        "blank_pages": args.pages, "child": args.child,
    })
    p.write_text(json.dumps(reg, indent=2))
    print(f"Added {args.traveler}/{args.type} exp {args.expires} → {p}")


def cmd_demo(args):
    import tempfile, os
    fd, tmp = tempfile.mkstemp(suffix=".json", dir=".")
    os.close(fd)
    Path(tmp).write_text(json.dumps(DEMO_REGISTRY, indent=2))
    print(f"[demo registry: {tmp}]\n")
    args.registry = tmp
    cmd_status(args)
    print()
    args.dest, args.arrival, args.exit = "TH", "2027-02-10", "2027-02-24"
    cmd_check(args)
    os.unlink(tmp)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--registry", default=str(REGISTRY_DEFAULT))
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("status").set_defaults(fn=cmd_status)
    ck = sub.add_parser("check")
    ck.add_argument("--dest", required=True)
    ck.add_argument("--arrival", required=True)
    ck.add_argument("--exit", dest="exit_")
    ck.set_defaults(fn=cmd_check)
    a = sub.add_parser("add")
    a.add_argument("--traveler", required=True)
    a.add_argument("--type", default="passport")
    a.add_argument("--issuer", default="US")
    a.add_argument("--tail", default="")
    a.add_argument("--expires", required=True)
    a.add_argument("--pages", type=int, default=12)
    a.add_argument("--child", action="store_true")
    a.set_defaults(fn=cmd_add)
    sub.add_parser("demo").set_defaults(fn=cmd_demo)
    args = ap.parse_args()
    if args.cmd == "check":
        args.exit = args.exit_
    args.fn(args)


if __name__ == "__main__":
    main()
