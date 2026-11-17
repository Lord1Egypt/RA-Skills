#!/usr/bin/env python3
"""Home office deduction planner: gate test, dual-method math, recapture pricing.

Commands:
  gate      --exclusive-room yes|no --dual-use yes|no --principal-place yes|no
            [--separate-structure yes|no] [--storage-only yes|no]
  compute   --status employee|self-employed --sqft N --home-sqft N --income N
            [--rent-year N] [--utilities-year N] [--insurance-year N]
            [--repairs-year N] [--internet-year N] [--own] [--home-value N]
            [--land-share F] [--sale-years N]
  evidence  --sqft N [--home-sqft N]   (audit evidence worksheet)
All rates exposed as constants; edit, don't fork.
"""
import argparse

SIMPLIFIED_RATE = 5.0        # $ per sqft
SIMPLIFIED_MAX_SQFT = 300
DEP_YEARS = 39               # residential nonresidential-property straight line
RECAPTURE_RATE = 0.25        # unrecaptured 1250 gain ceiling
TCJA_EMPLOYEE_SUSPENDED = True   # verify each filing season


def yn(v: str) -> bool:
    if v not in ("yes", "no"):
        raise SystemExit("--exclusive-room/--dual-use/--principal-place take yes|no")
    return v == "yes"


def cmd_gate(args) -> None:
    exclusive = yn(args.exclusive_room)
    dual = yn(args.dual_use)
    principal = yn(args.principal_place)
    separate = yn(args.separate_structure)
    storage = yn(args.storage_only)

    if separate:
        print("GATE: PASS (separate free-standing structure — exclusivity of the")
        print("whole structure is not required; still must be used regularly")
        print("and exclusively for the business in the work area).")
        return
    if storage:
        print("GATE: PASS-conditional (inventory storage: exclusive-use NOT required,")
        print("but the home must be the business's only fixed location and the")
        print("storage area must be a separately identifiable space, used regularly).")
        return
    if dual:
        print("GATE: FAIL — dual-use area (guest bed, kids' desk, media corner).")
        print("The ENTIRE deduction dies on exclusive-use failure, not a fraction.")
        print("Fix: dedicate the room, or claim a separately identifiable area")
        print("you can photograph as 100% business (weaker in audit).")
        return
    if not exclusive:
        print("GATE: FAIL — space not exclusively business. Same consequence as")
        print("dual-use: $0. Reconfigure the room before claiming.")
        return
    if not principal:
        print("GATE: CONDITIONAL — not principal place of business. Still passes if")
        print("you materially meet clients there, or use it for admin/management")
        print("work of the business. Otherwise deduction $0.")
        return
    print("GATE: PASS — exclusive, regular, principal place. Proceed to compute.")


def cmd_compute(args) -> None:
    if args.sqft <= 0 or args.home_sqft <= 0:
        raise SystemExit("Need positive --sqft and --home-sqft.")
    pct = min(args.sqft / args.home_sqft, 1.0)

    if args.status == "employee":
        if TCJA_EMPLOYEE_SUSPENDED:
            print("STATUS: W-2 employee -> federal home-office deduction = $0")
            print("(TCJA suspension; verify it hasn't lapsed for the filing year).")
            print("Still check: (a) employer accountable-plan reimbursement,")
            print("(b) CA unreimbursed employee expenses, NY telecommuting")
            print("allowance, PA employee expenses on the STATE return.")
        else:
            print("Employee route open this year — apply convenience-of-employer")
            print("test before the exclusive-use gate.")
        return

    if not args.income or args.income <= 0:
        raise SystemExit("--income (gross business income) required for the cap.")

    # --- regular method ---
    indirect = (args.rent_year or 0.0) + (args.utilities_year or 0.0) \
        + (args.insurance_year or 0.0) + (args.repair_year or 0.0)
    reg_lines = []
    if args.rent_year:
        reg_lines.append(("rent", args.rent_year * pct))
    if args.utilities_year:
        reg_lines.append(("utilities", args.utilities_year * pct))
    if args.insurance_year:
        reg_lines.append(("insurance", args.insurance_year * pct))
    if args.repair_year:
        reg_lines.append(("repairs", args.repair_year * pct))

    depreciation = 0.0
    if args.own:
        if not args.home_value:
            raise SystemExit("--own needs --home-value.")
        basis = args.home_value * (1.0 - (args.land_share or 0.0))
        depreciation = basis / DEP_YEARS * pct
        reg_lines.append(("depreciation", depreciation))

    regular = sum(v for _, v in reg_lines)
    internet = args.internet_year or 0.0    # direct expense, 100% if business line
    regular_total = regular + internet

    # --- simplified method ---
    simplified = SIMPLIFIED_RATE * min(args.sqft, SIMPLIFIED_MAX_SQFT)

    print(f"Business-use %: {pct*100:.1f}%  (office {args.sqft} / home {args.home_sqft} sqft)")
    print(f"\n  REGULAR method:")
    for name, v in reg_lines:
        print(f"    {name:<13} ${v:>9,.0f}")
    if internet:
        print(f"    {'internet':<13} ${internet:>9,.0f}  (direct business expense)")
    print(f"    total        ${regular_total:>9,.0f}")
    print(f"\n  SIMPLIFIED method: {min(args.sqft, SIMPLIFIED_MAX_SQFT)} sqft x "
          f"${SIMPLIFIED_RATE:.0f} = ${simplified:,.0f}")

    # --- income cap ---
    cap = args.income
    reg_capped = min(regular_total, cap)
    simp_capped = min(simplified, cap)
    carry = max(regular_total - cap, 0.0)
    print(f"\nIncome cap ${cap:,.0f}: regular ${reg_capped:,.0f}"
          + (f" (carryforward ${carry:,.0f})" if carry else "")
          + f"; simplified ${simp_capped:,.0f}"
          + (" (excess LOST)" if simplified > cap else ""))

    # --- recapture pricing for owners ---
    recapture_note = ""
    if args.own and depreciation > 0:
        yrs = args.sale_years or 10
        dep_pool = depreciation * yrs
        recapture = dep_pool * RECAPTURE_RATE
        delta = reg_capped - simp_capped
        horizon_gain = delta * yrs - recapture
        recapture_note = (
            f"\nRecapture (owner): depreciation ${dep_pool:,.0f} over {yrs} yrs -> "
            f"up to ~${recapture:,.0f} tax at sale (25% cap). "
        )
        if delta > 0:
            recapture_note += (
                f"Regular beats simplified by ${delta:,.0f}/yr = ${delta*yrs:,.0f} "
                f"over {yrs} yrs; net of recapture: ${horizon_gain:,.0f}. "
                + ("REGULAR still wins at this horizon."
                   if horizon_gain > 0 else
                   "SIMPLIFIED wins net at this horizon (short hold or thin margin).")
            )
        print(recapture_note)

    # --- verdict ---
    if reg_capped > simp_capped:
        margin = reg_capped - simp_capped
        print(f"\nVERDICT: REGULAR by ${margin:,.0f}/yr. Requires the expense log +")
        print("floor-plan evidence pack; carryforward tracked. Form 8829.")
    elif simp_capped > reg_capped:
        print(f"\nVERDICT: SIMPLIFIED by ${simp_capped-reg_capped:,.0f}/yr. Floor plan")
        print("only; zero recapture exposure. Schedule C line 30 worksheet.")
    else:
        print("\nVERDICT: TIE -> simplified (no records burden, no recapture).")


def cmd_evidence(args) -> None:
    pct = (args.sqft / args.home_sqft) if args.home_sqft else None
    print("HOME OFFICE EVIDENCE WORKSHEET — tax year ______")
    print("=" * 52)
    print(f"Date prepared: ________  Method: regular / simplified (circle)")
    print(f"Office dimensions: ____ x ____ ft  = {args.sqft} sqft")
    if args.home_sqft:
        print(f"Home total: {args.home_sqft} sqft  -> business-use %: {pct*100:.1f}%")
    print("\nPHOTO CHECKLIST (attach to tax-year folder):")
    print("  [ ] wide shot of room showing exclusive business use")
    print("  [ ] desk / equipment / monitor arrangement")
    print("  [ ] storage shelving (inventory/product storage)")
    print("  [ ] doorway shot — no bed, no guest furniture, no toys")
    print("\nEXPENSE LOG COLUMNS (keep 7 years):")
    print("  date | payee | category (rent/util/ins/repairs) | amount | % applied")
    print("\nCORROBORATION:")
    print("  [ ] client invoices issued from this address")
    print("  [ ] calendar showing regular work pattern")
    print("  [ ] business license / registration address")
    print("\nForm mapping: regular -> Form 8829 | simplified -> Sch C line 30")
    if args.home_sqft:
        print("NOTE (owner): keep annual depreciation worksheet until 3 yrs AFTER")
        print("sale settles — recapture follows the allowed/allowable ledger.")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("gate")
    for f in ("exclusive_room", "dual_use", "principal_place",
              "separate_structure", "storage_only"):
        p.add_argument(f"--{f.replace('_','-')}", dest=f,
                       default="no", choices=["yes", "no"])
    p.set_defaults(func=cmd_gate)

    p = sub.add_parser("compute")
    p.add_argument("--status", required=True, choices=["employee", "self-employed"])
    p.add_argument("--sqft", type=float, required=True)
    p.add_argument("--home-sqft", type=float, required=True)
    p.add_argument("--income", type=float, default=0.0)
    p.add_argument("--rent-year", type=float, default=0.0)
    p.add_argument("--utilities-year", type=float, default=0.0)
    p.add_argument("--insurance-year", type=float, default=0.0)
    p.add_argument("--repair-year", type=float, default=0.0)
    p.add_argument("--internet-year", type=float, default=0.0)
    p.add_argument("--own", action="store_true")
    p.add_argument("--home-value", type=float, default=0.0)
    p.add_argument("--land-share", type=float, default=0.25)
    p.add_argument("--sale-years", type=int, default=10)
    p.set_defaults(func=cmd_compute)

    p = sub.add_parser("evidence")
    p.add_argument("--sqft", type=float, required=True)
    p.add_argument("--home-sqft", type=float, default=0.0)
    p.set_defaults(func=cmd_evidence)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
