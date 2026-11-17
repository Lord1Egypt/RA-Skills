#!/usr/bin/env python3
"""maternity_plan.py — US parental-leave week-by-week planner (stdlib only).

Builds a dated leave plan from state programs + STD + employer policy + PTO,
sequences pay sources, and prints a week table with pay %, capped $, and
job-protection status. Verdicts are ESTIMATES using approximate 2026 program
parameters — always verify current-year rules on the state program website.

Subcommands:
  plan     build the dated week-by-week plan
  compare  two states side by side (same inputs)
  fmla     FMLA eligibility verdict only
"""
import argparse
import sys
from datetime import date, timedelta

# ---------------------------------------------------------------------------
# Approximate program parameters (2026 shape). VERIFY annually — weeks, rates
# and caps change. cap = max weekly benefit $; pct tiers: (threshold_weekly,
# pct_below, pct_above); flat pct otherwise.
# ---------------------------------------------------------------------------
STATES = {
    # state: dict(recovery_pre, recovery_vag, recovery_cs, bond_weeks,
    #             pct, cap, protect_weeks, name, tier=(thr, lo, hi) optional)
    "CA": dict(pre=4, vag=6, cs=8, bond=8, pct=0.65, cap=1681, prot=12 + 8,
               prog="CA SDI + PFL", tier=(1681 / 0.7, 0.60, 0.70)),
    "CO": dict(pre=0, vag=12, cs=14, bond=12, pct=0.90, cap=1091, prot=12,
               prog="CO FAMLI", tier=(1142, 0.90, 0.50)),
    "CT": dict(pre=0, vag=12, cs=12, bond=12, pct=0.95, cap=1032, prot=12,
               prog="CT PFML", tier=(1032 / 0.95, 0.95, 0.60)),
    "DE": dict(pre=0, vag=11, cs=11, bond=12, pct=0.80, cap=850, prot=6,
               prog="DE PFML"),
    "MA": dict(pre=0, vag=8, cs=8, bond=12, pct=0.80, cap=1200, prot=26,
               prog="MA PFML", tier=(1200 / 0.80, 0.80, 0.50)),
    "MD": dict(pre=0, vag=12, cs=12, bond=12, pct=0.60, cap=1000, prot=24,
               prog="MD FAMLI (2026 rollout)"),
    "MN": dict(pre=0, vag=12, cs=12, bond=12, pct=0.67, cap=1000, prot=12,
               prog="MN PFML (2026 rollout)"),
    "NJ": dict(pre=4, vag=6, cs=8, bond=12, pct=0.85, cap=1053, prot=12,
               prog="NJ TDI + FLI"),
    "NY": dict(pre=0, vag=6, cs=6, bond=12, pct=0.67, cap=1007, prot=12,
               prog="NY DBL + PFL"),
    "OR": dict(pre=0, vag=12, cs=14, bond=12, pct=0.90, cap=1459, prot=12,
               prog="OR PFOL", tier=(1459 / 1.0, 1.00, 0.67)),
    "RI": dict(pre=4, vag=4, cs=6, bond=5, pct=0.60, cap=1014, prot=13,
               prog="RI TDI + TCI"),
    "WA": dict(pre=0, vag=12, cs=12, bond=12, pct=0.90, cap=1621, prot=12,
               prog="WA PFML", tier=(1167, 0.90, 0.50)),
    "DC": dict(pre=0, vag=8, cs=8, bond=12, pct=0.90, cap=1090, prot=16,
               prog="DC PFPL"),
}
NO_STATE_MSG = ("No state paid program (verify: MD/MN 2026 rollout, small-"
                "employer carve-outs). Pay comes from STD/employer/PTO only.")

FMLA_GATE = dict(months=12, hours=1250, emp50=50)

def pdate(d): return d.isoformat()

def parse_pay(s):
    s = s.strip().lower()
    if s.endswith("/week"):
        return float(s[:-5]), 1
    if s.endswith("/biweekly"):
        return float(s[:-10]), 2
    if s.endswith("/mo"):
        return float(s[:-3] * 12 / 52.0)
    if s.endswith("/hr") and "@" in s:
        rate, hrs = s[:-3].split("@")
        return float(rate) * float(hrs), 1
    try:
        return float(s), 1  # assume weekly
    except ValueError:
        raise SystemExit(f"cannot parse pay '{s}' (use 1150/week, 2300/biweekly)")

def state_benefit_weekly(pay_wk, st):
    """Weekly benefit for one week under state program (capped, tiered)."""
    p = STATES[st]
    if "tier" in p:
        thr, lo, hi = p["tier"]
        pct = lo if pay_wk <= thr else hi
    else:
        pct = p["pct"]
    return min(pay_wk * pct, p["cap"]), pct

def fmla_verdict(tenure_mo, hours_yr, employees):
    fails = []
    if tenure_mo < FMLA_GATE["months"]:
        fails.append(f"tenure {tenure_mo}mo < 12mo")
    if hours_yr < FMLA_GATE["hours"]:
        fails.append(f"hours {hours_yr} < 1250")
    if employees < FMLA_GATE["emp50"]:
        fails.append(f"employees {employees} < 50 within 75mi")
    return (not fails), fails

def build_plan(state, due, pay_wk, cs, pto_days, std=None, emp_weeks=0,
               emp_pct=1.0, pre_start=0, partner=False):
    p = STATES.get(state)
    weeks = []  # (start, end, phase, source, benefit$, pct, protected)
    cur = due if not partner else due
    paid_total = 0.0
    protected_until = None

    # --- pre-birth weeks (state disability) ------------------------------
    if p and p["pre"] > 0 and pre_start and not partner:
        for i in range(p["pre"]):
            b, pct = state_benefit_weekly(pay_wk, state)
            weeks.append((cur - timedelta(days=7), cur, "pre-birth", p["prog"] + " disability",
                          b, pct, "FMLA if eligible"))
            paid_total += b
            cur -= timedelta(days=7)
        weeks.reverse()
        cur = due
    # pre-birth blocks handled: reposition cursor
    if weeks:
        cur = weeks[-1][1]

    # --- recovery ---------------------------------------------------------
    rec_wk = (p["cs"] if cs else p["vag"]) if p else (std["weeks_cs"] if cs else std["weeks_vag"]) if std else 0
    rec_src = (p["prog"].split(" + ")[0] + " disability") if p else ("employer STD" if std else "unpaid")
    rec_pct = None
    if not p and std:
        rec_pct = std["pct"]
    for i in range(int(rec_wk)):
        if p:
            b, pct = state_benefit_weekly(pay_wk, state)
        elif std:
            b, pct = pay_wk * std["pct"], std["pct"]
        else:
            b, pct = 0.0, 0.0
        weeks.append((cur, cur + timedelta(days=7), "recovery", rec_src if b else "UNPAID (protected)",
                      b, pct, "FMLA" ))
        paid_total += b
        cur = cur + timedelta(days=7)

    # --- employer parental policy (runs alongside or instead; model as    -
    #     paid-at-100% weeks that substitute for state bonding first) ------
    for i in range(int(emp_weeks)):
        take = i < int(rec_wk)  # overlapping recovery: employer tops up to 100%
        b = max(0.0, pay_wk - (state_benefit_weekly(pay_wk, state)[0] if p else 0.0)) if (p and take) else pay_wk
        src = "employer policy (top-up)" if (p and take) else "employer policy"
        # replace state pay in this recovery/bonding week rather than adding
        if take and weeks and weeks[-1][2] == "recovery":
            w = weeks[-1]
            weeks[-1] = (w[0], w[1], w[2], w[3] + " + " + src, pay_wk, 1.0, w[6])
            paid_total += b - w[4]
        else:
            weeks.append((cur, cur + timedelta(days=7), "bonding", src, pay_wk, 1.0, "FMLA"))
            paid_total += pay_wk
            cur += timedelta(days=7)

    # --- state bonding -----------------------------------------------------
    if p:
        bond_src = p["prog"].split(" + ")[-1] + " bonding"
        for i in range(int(p["bond"])):
            b, pct = state_benefit_weekly(pay_wk, state)
            weeks.append((cur, cur + timedelta(days=7), "bonding", bond_src, b, pct,
                          "state protection"))
            paid_total += b
            cur += timedelta(days=7)

    # --- PTO plug into unpaid weeks ----------------------------------------
    pto_weeks = int(pto_days // 5) if pto_days else 0
    fmla_left = max(0, 12 - len([w for w in weeks if w[6] == "FMLA"]))
    for i in range(pto_weeks):
        weeks.append((cur, cur + timedelta(days=7), "PTO-plug", "PTO", pay_wk, 1.0,
                      "FMLA" if i < fmla_left else "state protection" if p else "none"))
        paid_total += pay_wk
        cur += timedelta(days=7)

    # --- unpaid protected tail ---------------------------------------------
    prot = p["prot"] if p else 12
    used_prot = len([w for w in weeks if w[6] != "none"])
    tail = max(0, int(prot - used_prot))
    for i in range(tail):
        weeks.append((cur, cur + timedelta(days=7), "unpaid tail", "UNPAID", 0.0, 0.0,
                      "state protection" if p else "FMLA"))
        cur += timedelta(days=7)

    return weeks, paid_total

def cmd_plan(a):
    pay_wk, _ = parse_pay(a.pay)
    std = dict(weeks_vag=a.std_weeks or 0, weeks_cs=a.std_weeks or 0, pct=a.std_pct or 0.6) \
        if (a.std_weeks or 0) > 0 else None
    ok, fails = fmla_verdict(a.tenure_mo, a.hours_yr, a.employees)
    weeks, paid = build_plan(a.state.upper(), a.due, pay_wk, a.c_section,
                             a.pto_days, std=std, emp_weeks=a.employer_weeks,
                             pre_start=a.pre_weeks, partner=a.partner)
    print(f"=== Leave plan: {a.state.upper()} | due {a.due} | "
          f"{'C-section' if a.c_section else 'vaginal'} | pay ${pay_wk:,.0f}/wk ===")
    if not ok:
        print(f"!! FMLA NOT ELIGIBLE ({'; '.join(fails)}) — job protection depends on state law/employer policy")
    else:
        print("FMLA eligible: 12 wk job-protected (runs concurrent with paid programs)")
    print(f"{'wk':>2} {'dates':23} {'phase':12} {'source':34} {'pct':>5} {'$/wk':>8}  protection")
    total = len(weeks)
    paid_wks = sum(1 for w in weeks if w[4] > 0)
    for i, (s, e, ph, src, b, pct, prot) in enumerate(weeks, 1):
        print(f"{i:>2} {pdate(s):>10}→{pdate(e - timedelta(days=1)):<12} {ph:12} {src:34} "
              f"{pct * 100 if pct else 0:>4.0f}% {b:>8,.0f}  {prot}")
    months = total / 4.33
    print(f"\nTotal leave: {total} wk ({months:.1f} mo) | paid: {paid_wks} wk "
          f"(${paid:,.0f} = {paid / (pay_wk * total) * 100 if total else 0:.0f}% of salary)")
    print("NOTE: parameters are approximate 2026 values — verify weeks/caps on the "
          "state program site; employer policy may stack. File disability at leave "
          "start, bonding when recovery ends.")
    return 0

def cmd_compare(a):
    pay_wk, _ = parse_pay(a.pay)
    print(f"{'state':6} {'program':32} {'recovery':>8} {'bond':>5} {'wk benefit':>10} "
          f"{'cap hit?':>8} {'prot':>4}")
    for st in a.states:
        st = st.upper()
        if st not in STATES:
            print(f"{st:6} {NO_STATE_MSG[:32]:32} {'-':>8} {'-':>5} {'-':>10} {'-':>8} {'12':>4}")
            continue
        p = STATES[st]
        b, pct = state_benefit_weekly(pay_wk, st)
        print(f"{st:6} {p['prog']:32} {p['cs']:>7}wk {p['bond']:>4}wk {b:>10,.0f} "
              f"{'YES' if b >= p['cap'] else 'no':>8} {p['prot']:>3}wk")
    return 0

def cmd_fmla(a):
    ok, fails = fmla_verdict(a.tenure_mo, a.hours_yr, a.employees)
    if ok:
        print("FMLA ELIGIBLE — 12 weeks unpaid job protection; bonding must complete "
              "within 12 months of birth; give 30-day notice.")
    else:
        print("FMLA NOT ELIGIBLE: " + "; ".join(fails))
        print("Check: state small-medical-leave laws, employer policy; some states "
              "(CA/NJ/MA...) protect leave at smaller employers.")
    return 0

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("plan")
    p.add_argument("--state", required=True)
    p.add_argument("--due", type=date.fromisoformat, required=True)
    p.add_argument("--pay", required=True, help="e.g. 1150/week, 2300/biweekly")
    p.add_argument("--c-section", action="store_true")
    p.add_argument("--pto-days", type=float, default=0)
    p.add_argument("--std-weeks", type=int, default=0, help="employer STD weeks")
    p.add_argument("--std-pct", type=float, default=0.6)
    p.add_argument("--employer-weeks", type=int, default=0, help="paid parental policy weeks")
    p.add_argument("--pre-weeks", type=int, default=0, help="pre-birth weeks taken")
    p.add_argument("--tenure-mo", type=int, default=14)
    p.add_argument("--hours-yr", type=int, default=2000)
    p.add_argument("--employees", type=int, default=500)
    p.add_argument("--partner", action="store_true", help="non-birthing/adoptive parent")
    p.set_defaults(fn=cmd_plan)

    c = sub.add_parser("compare")
    c.add_argument("--states", nargs="+", required=True)
    c.add_argument("--pay", default="1150/week")
    c.set_defaults(fn=cmd_compare)

    f = sub.add_parser("fmla")
    f.add_argument("--tenure-mo", type=int, default=14)
    f.add_argument("--hours-yr", type=int, default=2000)
    f.add_argument("--employees", type=int, default=500)
    f.set_defaults(fn=cmd_fmla)

    a = ap.parse_args()
    sys.exit(a.fn(a))

if __name__ == "__main__":
    main()
