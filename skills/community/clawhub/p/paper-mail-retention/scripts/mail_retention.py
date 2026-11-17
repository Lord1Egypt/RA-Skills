#!/usr/bin/env python3
"""Paper Mail Retention — how long to keep each document type, purge triage
with dates, forever-list, filing blueprint. Pure stdlib.

Examples:
    python3 mail_retention.py keep --thing "tax return"
    python3 mail_retention.py purge --items "utility bill:2021-03" "bank statement:2024-06" "tax return:2019"
    python3 mail_retention.py archive
    python3 mail_retention.py list
"""
import argparse
import datetime as dt
import json
import re

# name: (years, clock_event, disposition, why, aliases)
# years = None -> forever; disposition in KEEP/SHRED/SCAN_SHRED/SAFE
TABLE = {
    "tax return": (None, "forever", "SCAN_SHRED",
                   "proves filing, carryforwards; keep paper 7yr then scan", ["taxes", "1040"]),
    "tax supporting documents": (7, "filing date", "SHRED",
                                 "IRS audit window 3yr, 6yr if >25% underreport", ["receipts tax", "tax receipts"]),
    "paystub": (0, "until W-2 matches", "SHRED",
                "keep newest from each year until W-2 confirms totals", ["pay stub", "payslip"]),
    "w-2": (7, "filing date", "KEEP",
            "files with the return; 7yr", ["w2", "1099", "1099 form"]),
    "bank statement": (1, "statement date", "SHRED",
                       "7yr only if tax-relevant", ["checking statement"]),
    "credit card statement": (1, "statement date", "SHRED",
                              "7yr if deductions claimed from it", []),
    "utility bill": (1, "bill date", "SHRED",
                     "keep latest only (proof of address/residency)", ["electric bill", "gas bill", "water bill"]),
    "internet bill": (1, "bill date", "SHRED", "keep latest only", ["phone bill"]),
    "medical bill": (3, "payment date", "SHRED",
                     "until dispute window closes; 7yr if claiming deduction", ["eob", "hospital bill"]),
    "immunization record": (None, "forever", "FOREVER",
                            "school, travel, adult boosters — irreplaceable", ["vaccination record", "shot record"]),
    "insurance policy": (None, "life of policy", "KEEP",
                         "keep current; expired+no claims pending = shred", ["car insurance", "home insurance"]),
    "closing documents": (None, "ownership+7yr", "SAFE",
                          "home purchase/sale; basis for capital gains", ["house closing", "settlement statement"]),
    "property deed": (None, "forever", "SAFE", "ownership proof", ["deed"]),
    "mortgage statement": (0, "until annual matches", "SHRED",
                           "keep annual statements w/ tax docs if deducting", []),
    "receipt": (0, "until warranty/return ends", "SHRED",
                "big purchases + tax-deductible + insurance-value: longer", ["sales receipt"]),
    "warranty": (0, "until expiry", "SHRED",
                 "keep stapled to receipt while product owned", ["manual", "guarantee"]),
    "vehicle title": (None, "forever", "SAFE", "ownership", ["car title"]),
    "maintenance record": (None, "while owned", "KEEP",
                           "proves care, boosts resale", ["service record", "car maintenance"]),
    "lease agreement": (1, "move-out", "SHRED",
                        "until deposit returned + disputes closed", ["rental lease"]),
    "birth certificate": (None, "forever", "SAFE", "irreplaceable core ID", []),
    "marriage certificate": (None, "forever", "SAFE", "irreplaceable", []),
    "death certificate": (None, "forever", "SAFE", "estate handling needs many copies", []),
    "divorce decree": (None, "forever", "SAFE", "custody/property terms never expire", ["custody order"]),
    "adoption papers": (None, "forever", "SAFE", "irreplaceable", []),
    "immigration document": (None, "forever", "SAFE", "green card/citizenship/naturalization", ["green card", "passport"]),
    "military discharge": (None, "forever", "SAFE", "DD-214 unlocks benefits", ["dd214", "dd-214"]),
    "pension document": (None, "forever", "KEEP",
                         "plan rules, benefit proofs", ["401k plan", "retirement plan"]),
    "social security statement": (0, "until superseded", "SHRED", "keep newest", ["ssa statement"]),
    "will": (None, "forever", "KEEP",
             "current version; lawyer keeps original typically", ["power of attorney", "directive", "trust"]),
    "transcript": (None, "forever", "KEEP", "diplomas, degrees", ["diploma"]),
    "investment confirmation": (7, "after sale", "KEEP",
                                "cost basis; keep until 7yr after you SELL", ["brokerage statement"]),
    "savings bond": (None, "until redeemed", "SAFE", "worth money", ["treasury bond"]),
    "guarantee contract": (1, "contract end", "SHRED", "service contracts", ["service contract"]),
}

DISPO_LABEL = {"KEEP": "KEEP (file)", "SHRED": "SHRED", "SCAN_SHRED": "SCAN then SHRED",
               "SAFE": "SAFE-DEPOSIT/fireproof", "FOREVER": "KEEP FOREVER"}


def match_key(thing):
    t = thing.lower().strip()
    for k, (_, _, _, _, aliases) in TABLE.items():
        if t == k or t in aliases:
            return k
    # fuzzy: word overlap
    t_words = set(t.split())
    best, best_score = None, 0
    for k, (_, _, _, _, aliases) in TABLE.items():
        k_words = set(k.split()) | set(" ".join(aliases).split())
        score = len(t_words & k_words)
        if score > best_score:
            best, best_score = k, score
    return best if best_score > 0 else None


def parse_date(s):
    s = s.strip().lower()
    if s in ("current", "now", "active", ""):
        return None
    m = re.match(r"^(\d{4})(?:-(\d{2}))?(?:-(\d{2}))?$", s)
    if m:
        y, mo, d = m.groups()
        return dt.date(int(y), int(mo or 1), int(d or 1))
    return None


def main():
    ap = argparse.ArgumentParser(description="Paper document retention lookup & purge triage")
    sub = ap.add_subparsers(dest="cmd")

    p = sub.add_parser("keep")
    p.add_argument("--thing", required=True)

    p = sub.add_parser("purge")
    p.add_argument("--items", nargs="+", required=True,
                   help="'category:date' e.g. 'utility bill:2021-03' 'tax return:2019'")
    p.add_argument("--today", default=None)

    sub.add_parser("archive")

    p = sub.add_parser("list")

    a = ap.parse_args()
    today = dt.date.fromisoformat(a.today) if getattr(a, "today", None) else dt.date.today()

    if a.cmd == "keep":
        k = match_key(a.thing)
        if not k:
            print(f"No match for '{a.thing}'. Try `list` for categories.")
            raise SystemExit(2)
        years, clock, dispo, why, _ = TABLE[k]
        dur = "FOREVER" if years is None else (f"{years} yr" if years else f"until {clock}")
        print(f"{k.upper()}")
        print(f"  keep: {dur}")
        print(f"  clock starts: {clock}")
        print(f"  disposition: {DISPO_LABEL[dispo]}")
        print(f"  why: {why}")
        return

    if a.cmd == "list":
        print(f"{'category':26s} {'keep':>12s}  disposition")
        for k, (years, clock, dispo, _, _) in sorted(TABLE.items()):
            dur = "FOREVER" if years is None else (f"{years}yr" if years else "until " + clock.split()[-1] if clock else "—")
            print(f"{k:26s} {dur:>12s}  {DISPO_LABEL[dispo]}")
        return

    if a.cmd == "archive":
        print("=" * 62)
        print("FILING BLUEPRINT (year-digit system)")
        print("=" * 62)
        print("ACTIVE tray: to-pay, to-file, current policies, this year's")
        print("  tax folder, active warranties stapled to receipts.")
        print("YEAR folders: one per year, time-limited items only.")
        print(f"  Keep {today.year - 7}..{today.year}; after tax day shred the 8th.")
        print("TOPIC folders (no clock): vehicles, house/basis, medical-forever,")
        print("  manuals for appliances you still own.")
        print("FOREVER box (fireproof) / safe-deposit: certificates, deeds,")
        print("  DD-214, will, bonds, immigration papers.")
        print()
        print("FOREVER LIST (never purge):")
        for k, (years, _, dispo, _, _) in sorted(TABLE.items()):
            if years is None:
                print(f"  - {k}  [{DISPO_LABEL[dispo]}]")
        print()
        print("Purge ritual: tax day + 1 week, 30 minutes, one folder to shred.")
        return

    if a.cmd == "purge":
        results = []
        for spec in a.items:
            if ":" not in spec:
                results.append((spec, "?", "no date given — conservative: treat as current", ""))
                continue
            thing, date_s = spec.rsplit(":", 1)
            k = match_key(thing)
            if not k:
                results.append((thing, date_s, "UNKNOWN category — manual call", ""))
                continue
            years, clock, dispo, why, _ = TABLE[k]
            d = parse_date(date_s)
            if years is None:
                verdict = f"KEEP FOREVER — {why}"
                results.append((thing, date_s, verdict, DISPO_LABEL[dispo]))
                continue
            if d is None:
                verdict = f"date unclear — treat as current: keep per rule ({why})"
                results.append((thing, date_s, verdict, DISPO_LABEL[dispo]))
                continue
            # clock: years from date
            cutoff = dt.date(d.year + years, d.month, min(d.day, 28)) if years else d
            age_days = (today - d).days
            limit_days = years * 365.25 if years else 0
            if age_days >= limit_days and years > 0:
                overdue = (today - cutoff).days / 365.25
                verdict = f"SHRED — {years}yr clock ran out ({overdue:.1f} yr overdue)"
                results.append((thing, date_s, verdict, "SHRED"))
            elif years == 0:
                # until-event rules: assume event passed if doc older than a year
                if age_days > 365:
                    verdict = f"SHRED — event window passed ({clock})"
                    results.append((thing, date_s, verdict, "SHRED"))
                else:
                    verdict = f"KEEP — {clock} (doc {age_days//30} months old)"
                    results.append((thing, date_s, verdict, DISPO_LABEL[dispo]))
            else:
                remain = limit_days - age_days
                verdict = f"KEEP — {remain/365.25:.1f} yr left of {years}yr clock"
                results.append((thing, date_s, verdict, DISPO_LABEL[dispo]))
        print("=" * 62)
        print("PURGE TRIAGE")
        print("=" * 62)
        for thing, date_s, verdict, dispo in results:
            print(f"  {thing:<28s} {date_s:<10s} {verdict}")
        print()
        shred = sum(1 for r in results if r[2].startswith("SHRED"))
        print(f"{shred}/{len(results)} items cleared for the cross-cut shredder.")
        print("Reminder: SSN/account-bearing papers shred, never recycle.")
        return

    ap.print_help()


if __name__ == "__main__":
    main()
