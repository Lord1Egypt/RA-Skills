#!/usr/bin/env python3
"""Property Tax Appeal Kit — equalization math, record-card error audit,
comparable-sales grading, savings computation, and a dated appeal timeline.
Stdlib only."""
import argparse
import datetime as dt
import statistics


def cmd_equalize(a):
    ratio = a.assessed / a.market_est
    rel = ratio / a.town_avg_ratio
    fair = a.market_est * a.town_avg_ratio
    tax_now = a.assessed * a.millage / 1000.0
    tax_fair = fair * a.millage / 1000.0
    savings = tax_now - tax_fair
    print("EQUALIZATION CHECK")
    print(f"  your assessment:  ${a.assessed:,.0f}   your market estimate: "
          f"${a.market_est:,.0f}")
    print(f"  your ratio:       {ratio:.3f}  vs town average {a.town_avg_ratio:.3f}")
    if rel > 1:
        print(f"  you are assessed {100 * (rel - 1):.1f}% ABOVE the typical "
              f"town ratio")
    else:
        print(f"  you are assessed {100 * (1 - rel):.1f}% BELOW the typical "
              f"town ratio")
    print(f"  implied fair assessment: ${a.market_est:,.0f} x "
          f"{a.town_avg_ratio} = ${fair:,.0f}")
    print(f"  tax now:     ${a.assessed:,.0f} x {a.millage} mills = "
          f"${tax_now:,.0f}/yr")
    print(f"  tax at fair: ${fair:,.0f} x {a.millage} mills = "
          f"${tax_fair:,.0f}/yr")
    if rel > 1.10:
        v = "STRONG UNEQUALITY — appeal-ready"
        extra = ("File with the uniformity argument + record-card audit; "
                 "request ${:,.0f}".format(fair))
    elif rel >= 1.03:
        v = "WORTH FILING — pair with record-card audit"
        extra = "Marginal alone; a card error tips it."
    elif rel >= 0.97:
        v = "IN LINE — only appeal on factual errors"
        extra = ("Run the card audit; equalization won't carry an appeal.")
    else:
        v = ("UNDERASSESSED — do NOT appeal (you invite a raise)")
        extra = ("A hearing can end with your value raised. Stand pat;")
        extra += " audit quietly and recheck next year."
    if savings > 0:
        print(f"  SAVINGS IF WON: ~${savings:,.0f}/yr")
    print(f"VERDICT: {v}. {extra}")
    if savings > 0:
        print(f"  multi-year effect: assessments persist until the next")
        print(f"  reassessment cycle — ${savings:,.0f}/yr compounds quietly.")
    else:
        print(f"  RISK EXPOSURE: ~${-savings:,.0f}/yr MORE if corrected —")
        print(f"  appealing would hand the board the raise.")


def cmd_card(a):
    print("RECORD-CARD AUDIT")
    errs = 0
    if a.card_sqft and a.actual_sqft and a.card_sqft != a.actual_sqft:
        d = a.actual_sqft - a.card_sqft
        ppsf = a.market_est / a.actual_sqft if a.market_est else 180
        impact = abs(d) * ppsf
        errs += 1
        print(f"  [ERROR] square footage: card {a.card_sqft} vs measured "
              f"{a.actual_sqft} ({d:+.0f} sqft, {100 * d / a.card_sqft:+.1f}%)")
        print(f"          value impact at ${ppsf:.0f}/sqft: ~${impact:,.0f}")
    if a.card_baths and a.actual_baths and a.card_baths != a.actual_baths:
        errs += 1
        print(f"  [ERROR] bathrooms: card {a.card_baths} vs actual "
              f"{a.actual_baths}")
        print("          value impact: ~$5,000 (half-bath counted full)")
    if errs == 0:
        print("  no discrepancies found in provided fields — pull the full")
        print("  card and check lot size, garage, basement finish, decks,")
        print("  outbuildings, and year built too.")
        return
    print(f"  this is a FACTUAL-ERROR appeal — strongest class, no comps")
    print("  required. Packet: card copy, photos, sketch with dimensions,")
    print("  this math. Requested value = current assessment minus impacts.")


def cmd_comps(a):
    print("COMPARABLE-SALES EVIDENCE")
    if len(a.sales) < 3:
        print("  need >=3 sales; 5 is the sweet spot. Boards discount")
        print("  single-comp arguments.")
        return
    rows = []
    for spec in a.sales:
        price_s, sqft_s = spec.split(",")
        rows.append((float(price_s), float(sqft_s)))
    ppsfs = [p / s for p, s in rows]
    med = statistics.median(ppsfs)
    subject_est = med * a.subject_sqft
    print("  sale                 $/sqft   grade")
    graded = []
    for (price, sqft), ppsf in zip(rows, ppsfs):
        size_ok = abs(sqft - a.subject_sqft) / a.subject_sqft <= 0.25
        spread_ok = abs(ppsf - med) / med <= 0.20
        if size_ok and spread_ok:
            g = "USE (strong)"
        elif size_ok or spread_ok:
            g = "USE (note adjustments)"
        else:
            g = "DROP (outlier)"
        graded.append(g != "DROP (outlier)")
        print(f"  ${price:>9,.0f} / {sqft:>5,.0f} = {ppsf:6.0f}   {g}")
    used = [p for p, keep in zip(ppsfs, graded) if keep]
    med_used = statistics.median(used) if used else med
    est = med_used * a.subject_sqft
    print(f"\n  median $/sqft (used comps): ${med_used:,.0f}")
    print(f"  subject value estimate: {med_used:,.0f} x {a.subject_sqft} = "
          f"${est:,.0f}")
    delta = a.assessed - est
    print(f"  assessed ${a.assessed:,.0f} vs comp evidence ${est:,.0f}: "
          f"assessment is {delta:+,.0f} ({100 * delta / est:+.1f}%)")
    if delta / est > 0.05:
        print("  -> market-value argument available; combine with the")
        print("     uniformity (equalization) math for a two-front case.")
    elif delta / est < -0.05:
        print("  -> comps support the assessment; do NOT lead with market")
        print("     value (you'd argue yourself upward). Card errors only.")
    else:
        print("  -> assessment consistent with comps; only card errors")
        print("     carry an appeal here.")


def cmd_timeline(a):
    notice = dt.date.fromisoformat(a.notice)
    win = a.window
    deadline = notice + dt.timedelta(days=win)
    print(f"APPEAL TIMELINE — notice {notice.isoformat()}, "
          f"{win}-day window")
    steps = []
    d0 = notice
    if a.informal:
        steps.append((d0 + dt.timedelta(days=3),
                      "Call assessor's office: request the property record "
                      "card + recent sales list (public). Ask about informal "
                      "review — many towns fix card errors on the phone, "
                      "no hearing needed."))
    steps.append((d0 + dt.timedelta(days=7),
                  "Card audit done: measure sqft, count baths, photograph "
                  "every discrepancy."))
    steps.append((d0 + dt.timedelta(days=14),
                  "Evidence packet assembled: graded comps table, "
                  "equalization math, photos, card copy."))
    if a.informal:
        steps.append((d0 + dt.timedelta(days=18),
                      "Informal review held/declined — if declined, file "
                      "the formal appeal NOW (don't wait for the deadline)."))
    steps.append((d0 + dt.timedelta(days=21),
                  "Formal appeal FILED (keep the stamped copy + confirmation "
                  "number). Verify the hearing date when noticed."))
    steps.append((deadline - dt.timedelta(days=3),
                  "SAFETY MARGIN: if not yet filed, file today. Deadline "
                  f"{deadline.isoformat()} is hard; late = wait a year."))
    steps.append((deadline + dt.timedelta(days=14),
                  "Hearing prep: rehearse the script — lead with factual "
                  "errors, then uniformity, then market value; end with the "
                  "requested number."))
    for date, text in sorted(steps):
        marker = "** DEADLINE-3 **" if "SAFETY MARGIN" in text else ""
        # wrap step text at ~72 chars after the date column
        words, lines, cur = text.split(), [], ""
        for w in words:
            if len(cur) + len(w) + 1 > 72:
                lines.append(cur)
                cur = w
            else:
                cur = (cur + " " + w).strip()
        lines.append(cur)
        print(f"  {date.isoformat()}  {lines[0]}")
        for ln in lines[1:]:
            print(f"            {ln}")
        if marker:
            print(f"            {marker}")
    print("\n  board hearing rule: 5-10 minutes typical. Bring 3 copies of")
    print("  everything (board members, assessor, you). Numbers they can")
    print("  recompute beat adjectives every time.")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("equalize", help="uniformity math + savings")
    s.add_argument("--assessed", type=float, required=True)
    s.add_argument("--market-est", type=float, required=True,
                   help="your evidence-based market value estimate")
    s.add_argument("--town-avg-ratio", type=float, required=True,
                   help="municipality average assessment ratio (assessor/"
                        "state equalization report)")
    s.add_argument("--millage", type=float, required=True,
                   help="total millage rate (mills)")
    s.set_defaults(fn=cmd_equalize)

    s = sub.add_parser("card", help="record-card error audit")
    s.add_argument("--card-sqft", type=float)
    s.add_argument("--actual-sqft", type=float)
    s.add_argument("--card-baths", type=float)
    s.add_argument("--actual-baths", type=float)
    s.add_argument("--assessed", type=float)
    s.add_argument("--market-est", type=float)
    s.set_defaults(fn=cmd_card)

    s = sub.add_parser("comps", help="comparable sales grading")
    s.add_argument("--assessed", type=float, required=True)
    s.add_argument("--subject-sqft", type=float, required=True)
    s.add_argument("--sales", nargs="+", required=True,
                   metavar="PRICE,SQLIKE",
                   help="e.g. 385000,2400 322000,1900 ...")
    s.set_defaults(fn=cmd_comps)

    s = sub.add_parser("timeline", help="dated steps from notice")
    s.add_argument("--notice", required=True, help="notice date YYYY-MM-DD")
    s.add_argument("--window", type=int, default=30,
                   help="filing window in days (check your jurisdiction)")
    s.add_argument("--informal", default="yes",
                   help="'yes' if informal review available")
    s.set_defaults(fn=cmd_timeline)

    a = p.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
