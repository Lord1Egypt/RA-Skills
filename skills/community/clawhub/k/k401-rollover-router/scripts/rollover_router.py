#!/usr/bin/env python3
"""k401 Rollover Router — leave vs roll-to-IRA vs roll-to-new-plan vs Roth.

Projects fee-drag differences over your real horizon, prices a Roth
conversion at your marginal bracket, and prints the trap checklist
(20% indirect-withholding, 60-day window, age-55 rule, pro-rata, NUA).

stdlib only. Not tax advice - verify brackets/RMD ages against current IRS
publications.
"""
import argparse
import sys

CONFIG = {
    "rmd_age_note": "RMDs: 73 if born 1951-1959, 75 if born 1960+ (SECURE 2.0)",
    "penalty_age_ira": 59.5,
    "separator_age": 55,
    "indirect_withholding": 0.20,
    "indirect_window_days": 60,
}


def fv(balance, r, fee, years):
    return balance * (1 + r - fee) ** years


def fmt(n):
    return f"${n:,.0f}"


def route(args):
    f_plan = args.plan_fee_bps / 10000
    f_ira = args.ira_fee_bps / 10000
    r = args.return_pct / 100
    N = args.years_to_draw
    B = args.balance

    print("=" * 66)
    print(f"OLD 401(k) DECISION  balance {fmt(B)}  age {args.age}  "
          f"draw in {N}y (age {args.age + N})")
    print(f"fees: plan {args.plan_fee_bps:.0f} bps vs IRA "
          f"{args.ira_fee_bps:.0f} bps, expected return {args.return_pct}%")
    print("=" * 66)

    # --- fee drag table ---
    print("\nFEE-DRAG (plan stays invested vs IRA-cost equivalent)")
    v_plan0 = B
    for yrs in (10, 20, 30, N) if N not in (10, 20, 30) else (10, 20, 30):
        if yrs <= 0:
            continue
        v_plan = fv(v_plan0, r, f_plan, yrs)
        v_ira = fv(v_plan0, r, f_ira, yrs)
        print(f"  {yrs:>2}y: plan {fmt(v_plan)}  IRA {fmt(v_ira)}  "
              f"IRA ahead by {fmt(v_ira - v_plan)}")

    drag_horizon = fv(B, r, f_ira, N) - fv(B, r, f_plan, N)
    fee_gap_bps = args.plan_fee_bps - args.ira_fee_bps

    # --- route scoring ---
    reasons = []
    roll_score = 0.0
    if fee_gap_bps >= 30 and N >= 15:
        roll_score += 2
        reasons.append(f"fee gap {fee_gap_bps:.0f} bps over {N}y = "
                       f"{fmt(drag_horizon)} of compounding lost by staying")
    elif fee_gap_bps >= 30:
        roll_score += 1
        reasons.append(f"fee gap {fee_gap_bps:.0f} bps but only {N}y left; "
                       f"drag {fmt(drag_horizon)}")
    elif fee_gap_bps < 10:
        roll_score -= 1
        reasons.append(f"fees nearly equal ({fee_gap_bps:+.0f} bps) - fee "
                       "drag is NOT the driver here")

    age_to_59_5 = 59.5 - args.age
    if args.age < 55 and N >= age_to_59_5:
        reasons.append(f"IRA keeps money locked to 59.5 "
                       f"({age_to_59_5:.0f}y away); rule-of-55 dies in an IRA")
    if args.new_plan_accepts:
        reasons.append("new plan ACCEPTS rollovers: consolidation there "
                       "keeps age-55 + ERISA protection")

    # Roth overlay
    if args.bracket_now < args.bracket_retire:
        roth_tax = B * args.bracket_now / 100
        reasons.append(f"Roth partial/full: bracket now {args.bracket_now}% < "
                       f"retire {args.bracket_retire}% - conversion tax "
                       f"{fmt(roth_tax)}; pay from OUTSIDE cash, never from "
                       "the rollover")
        roth_rec = "ROLL-ROTH-PARTIAL"
    else:
        roth_rec = None

    # --- verdict ---
    print("\nDECISIVE FACTORS")
    for x in reasons:
        print(f"  - {x}")

    print("\nROUTE VERDICT")
    if roll_score >= 2:
        base = ("ROLL -> IRA" if not args.new_plan_accepts
                else "ROLL -> IRA (or new plan if its menu is as cheap)")
    elif roll_score >= 1:
        base = "ROLL (either destination; compare fund menus)"
    else:
        base = ("LEAVE (or roll to new plan if consolidating)" )
    print(f"  {base}")
    if roth_rec:
        print(f"  overlay: {roth_rec} - convert a slice sized to fill the "
              f"{args.bracket_now}% bracket headroom")
    if args.balance < 7000:
        print("  NOTE: balance may be below plan force-out thresholds "
              "($5k-$7k) - the plan may cash you out or move to an IRA "
              "automatically; act before they do")

    # --- cashout damage (deterrence) ---
    if args.bracket_now and args.age < 55:
        tax = B * args.bracket_now / 100
        pen = B * 0.10
        print(f"\nCASHING OUT (for reference, NOT recommended): "
              f"tax {fmt(tax)} + 10% penalty {fmt(pen)} = "
              f"{fmt(B - tax - pen)} net, and {fmt(fv(B, r, f_ira, N))} "
              f"of {N}-y growth surrendered")

    # --- traps ---
    print("\nTRAP CHECKLIST")
    print(f"  1. DIRECT (trustee-to-trustee) rollover only - indirect "
          f"triggers {CONFIG['indirect_withholding']:.0%} federal "
          f"withholding and a {CONFIG['indirect_window_days']}-day clock")
    print(f"  2. age-55 rule: penalty-free 401(k) access if you left that "
          f"employer at {CONFIG['separator_age']}+; IRA waits to "
          f"{CONFIG['penalty_age_ira']}")
    print("  3. pro-rata: any pre-tax IRA balance taxes your backdoor Roth; "
          "rolling INTO a 401(k) keeps the backdoor clean")
    print("  4. employer stock in plan? NUA treatment dies if you blind-roll")
    print(f"  5. {CONFIG['rmd_age_note']}")
    print("\nVerify current brackets/RMD ages: IRS Pub 590-A + plan fee "
          "disclosure. Not tax advice.")
    return 0


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--balance", type=float, required=True)
    p.add_argument("--age", type=float, required=True)
    p.add_argument("--plan-fee-bps", type=float, required=True,
                   help="all-in old-plan fee in basis points")
    p.add_argument("--ira-fee-bps", type=float, default=8,
                   help="achievable IRA all-in fee (bps)")
    p.add_argument("--return", dest="return_pct", type=float, default=6.5)
    p.add_argument("--years-to-draw", type=int, required=True)
    p.add_argument("--bracket-now", type=float, default=24)
    p.add_argument("--bracket-retire", type=float, default=22)
    p.add_argument("--new-plan-accepts", action="store_true")
    a = p.parse_args()
    if not 1 <= a.plan_fee_bps <= 300:
        p.error("--plan-fee-bps realistic range 1-300")
    return route(a)


if __name__ == "__main__":
    sys.exit(main())
