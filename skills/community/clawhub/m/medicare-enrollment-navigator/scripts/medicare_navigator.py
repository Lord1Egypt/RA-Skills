#!/usr/bin/env python3
"""Medicare Enrollment Navigator — windows, deadlines, late-penalty math.

Prints your Initial Enrollment Period (or the 8-month SEP / GEP path),
computes the lifetime Part B penalty (10% per full 12 months late) and
Part D penalty (1% of base premium per month late) in dollars, dates your
6-month Medigap guaranteed-issue clock, and prints the trap checklist
(COBRA SEP clock, <20-employee employers, HSA contribution freeze,
spouse-dependent rules).

Usage:
  medicare_navigator.py --birth 1961-08
  medicare_navigator.py --birth 1961-08 --still-working --employer-size 40
  medicare_navigator.py --birth 1961-08 --coverage-ended 2026-06
  medicare_navigator.py --birth 1961-08 --now 2027-04 --months-without-drug-coverage 5

stdlib only. Premium constants are estimates — verify current figures at
medicare.gov (footer printed with every run). Not insurance advice.
"""
import argparse
import sys
from datetime import date

CONFIG = {
    "part_b_premium": 185.00,   # standard monthly premium (2025 actual; VERIFY)
    "part_d_base": 36.78,       # national base beneficiary premium (VERIFY)
    "sep_months": 8,            # SEP after employer coverage ends
    "medigap_oep_months": 6,
    "small_employer": 20,
    "b_penalty_pct": 0.10,      # per FULL 12-month period late, LIFETIME
    "d_penalty_pct": 0.01,      # per month late, LIFETIME
}


def ym(s):
    try:
        y, m = s.split("-")
        y, m = int(y), int(m)
        if not (1 <= m <= 12):
            raise ValueError
        return (y, m)
    except Exception:
        raise SystemExit(f"error: bad date '{s}' — use YYYY-MM (e.g. 1961-08)")


def add_months(idx, n):
    t = idx[0] * 12 + idx[1] - 1 + n
    return (t // 12, t % 12 + 1)


def months_between(a, b):
    return (b[0] - a[0]) * 12 + (b[1] - a[1])


def f(idx):
    return f"{idx[0]:04d}-{idx[1]:02d}"


def month_name(idx):
    names = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun",
             "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    return f"{names[idx[1]]} {idx[0]}"


def money(x, cents=False):
    return f"${x:,.2f}" if cents else f"${x:,.0f}"


def iep_window(birth):
    """IEP = 3 months before 65th birthday month, through 3 months after."""
    b65 = add_months(birth, 65 * 12)
    return add_months(b65, -3), b65, add_months(b65, 3)


def part_b_effective(enroll_month, iep_start, b65):
    """Enroll in IEP months 1-4 (3 before + birthday month) -> birthday month.
    Enroll in months 5-7 (the 3 after birthday) -> first of next month."""
    pos = months_between(iep_start, enroll_month)
    if pos <= 3:
        return b65
    return add_months(enroll_month, 1)


def next_gep(now):
    """General Enrollment Period: Jan 1 - Mar 31, coverage July 1."""
    if now[1] <= 3:
        return now, (now[0], 7), "open now"
    return (now[0] + 1, 1), (now[0] + 1, 7), "next January"


def sep_deadline(end_of_coverage):
    return add_months(end_of_coverage, CONFIG["sep_months"])


def penalty_b(late_months, premium):
    full_years = late_months // 12
    pct = full_years * CONFIG["b_penalty_pct"]
    return full_years, pct, premium * pct


def penalty_d(months, base):
    return months * CONFIG["d_penalty_pct"] * base


def hr(title):
    print("\n" + "=" * 64)
    print(title)
    print("=" * 64)


def main():
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--birth", required=True, help="birth month YYYY-MM")
    p.add_argument("--now", default=None,
                   help="current month YYYY-MM (default: real today)")
    p.add_argument("--still-working", action="store_true",
                   help="you are an ACTIVE employee with employer group coverage")
    p.add_argument("--employer-size", type=int, default=None,
                   help="employees at the firm (with --still-working)")
    p.add_argument("--spouse-covered", action="store_true",
                   help="you are covered as a DEPENDENT on spouse's active employer plan")
    p.add_argument("--coverage-ended", default=None,
                   help="YYYY-MM your employer plan/employment ended (SEP mode)")
    p.add_argument("--months-without-drug-coverage", type=int, default=None,
                   help="months since creditable drug coverage ended (Part D penalty)")
    p.add_argument("--creditable-drug", action="store_true",
                   help="you DO have creditable drug coverage now (zeroes Part D penalty)")
    p.add_argument("--premium-b", type=float, default=CONFIG["part_b_premium"])
    p.add_argument("--premium-d-base", type=float, default=CONFIG["part_d_base"])
    p.add_argument("--hsa", action="store_true",
                   help="you are currently contributing to an HSA")
    p.add_argument("--estimate-years", type=int, default=20,
                   help="horizon for lifetime penalty cost (default 20)")
    a = p.parse_args()

    birth = ym(a.birth)
    now = ym(a.now) if a.now else (date.today().year, date.today().month)
    iep_start, b65, iep_end = iep_window(birth)
    late_months = months_between(iep_end, now)
    drug_months = a.months_without_drug_coverage

    hr(f"MEDICARE ENROLLMENT MAP — born {f(birth)}")
    print(f"65th birthday month ........ {month_name(b65)}")
    print(f"Initial Enrollment Period ... {f(iep_start)}  →  {f(iep_end)}  (7 months)")
    print(f"Mode ....................... ", end="")
    if a.coverage_ended:
        print(f"SEP (employer coverage ended {f(ym(a.coverage_ended))})")
    elif a.still_working:
        print("working past 65 with employer coverage")
    else:
        print("default: not an active employee / no employer coverage")
    print(f"Today ...................... {month_name(now)}")

    # ---------------- mode: working ----------------
    if a.still_working:
        size = a.employer_size if a.employer_size is not None else 20
        hr("VERDICT")
        if size >= CONFIG["small_employer"] and not a.spouse_covered:
            print("DELAY PART B — OK (penalty-free while actively employed).")
            print(f"  Employer has {size} employees (≥ 20): the employer plan is")
            print("  primary; your 8-month SEP clock starts when employment OR")
            print("  the group plan ends — whichever comes FIRST.")
        elif a.spouse_covered:
            print("DELAY PART B — OK: covered as a dependent on your spouse's")
            print("  ACTIVE employer plan; the SEP protects you while it lasts.")
        else:
            print("ENROLL PART B NOW — DO NOT WAIT.")
            print(f"  Employer has fewer than {CONFIG['small_employer']} employees:")
            print("  Medicare pays PRIMARY. The employer plan can refuse or pay")
            print("  as secondary, leaving claims hanging. This is the classic")
            print("  small-employer trap — working is NOT protection below 20.")
        print("\nPART A: enroll anytime — free if you have 40 quarters of work.")
        if a.hsa:
            print("\n⚠ HSA FREEZE: with ANY Medicare enrollment (Part A counts)")
            print("  you may NOT contribute to an HSA — payroll + employer")
            print("  contributions too. Stop HSA contributions at least 6 months")
            print("  BEFORE you apply, or unwind the excess with the IRS.")
        hr("SEP TIMER (when you retire)")
        print(f"SEP = {CONFIG['sep_months']} months from the day employment/coverage ends.")
        print(f"Enroll in month X  →  Part B starts the 1st of month X+1.")
        print(f"Example: retire {month_name((2026, 9))} → SEP through "
              f"{month_name(add_months((2026, 9), 8))}.")
        hr("TRAPS (working mode)")
        print("1. COBRA does NOT extend the SEP. The 8-month clock starts at")
        print("   JOB end, not COBRA end. People on 18-month COBRA burn the SEP.")
        print("2. RETIREE health coverage (not active-employee) does not protect")
        print("   you from the Part B penalty either.")
        print("3. Medigap guaranteed issue opens for 6 months from your Part B")
        print(f"   start date — plan it so it does not lapse while you shop.")
        return footer(a)

    # ---------------- mode: SEP after coverage ended ----------------
    if a.coverage_ended:
        cov_end = ym(a.coverage_ended)
        dl = sep_deadline(cov_end)
        left = months_between(now, dl)
        late = max(0, months_between(cov_end, now) - CONFIG["sep_months"])
        hr("SEP WINDOW")
        print(f"Coverage ended ............. {month_name(cov_end)}")
        print(f"SEP deadline ............... {month_name(dl)}")
        print(f"Months remaining ........... {left}")
        hr("VERDICT")
        if left > 0:
            eff = add_months(now, 1)
            print(f"ENROLL NOW — SEP OPEN ({left} months left).")
            print(f"  Enroll this month → Part B effective {month_name(eff)}.")
            print("  Enrolling at the deadline still works, but every month")
            print("  uncovered after the SEP is a permanent penalty year.")
        else:
            gep, gep_eff, when = next_gep(now)
            print(f"SEP EXPIRED — you are {abs(left)} months past it.")
            print(f"  Next General Enrollment Period: {month_name(gep)} ({when})")
            print(f"  → coverage starts {month_name(gep_eff)}. No Part B until then.")
        if late > 0 or left <= 0:
            fy, pct, mo = penalty_b(max(late, 1), a.premium_b)
            if late > 0:
                print(f"\nLATE MONTHS EXPOSED ........ {late}")
                print(f"Part B penalty: {fy} full 12-month period(s) → +{pct:.0%} "
                      f"of premium for LIFE")
                print(f"  = {money(mo, True)}/mo  ≈ {money(mo * 12)}/yr  "
                      f"≈ {money(mo * 12 * a.estimate_years)} over {a.estimate_years} yr")
            else:
                print("\nNo penalty yet — enroll this month and the slate is clean.")
        if a.hsa:
            print("\n⚠ HSA: stop contributions 6 months before you apply.")
        if left > 0:
            eff = add_months(now, 1)
        else:
            gep, gep_eff, _ = next_gep(now)
            eff = gep_eff
        hr("MEDIGAP GUARANTEED-ISSUE CLOCK")
        gi_end = add_months(eff, CONFIG["medigap_oep_months"])
        print(f"6-month Medigap open enrollment from Part B start {month_name(eff)}")
        print(f"  → guaranteed issue (no health questions, no denial) through "
              f"{month_name(gi_end)}.")
        print("Outside that window insurers in most states can underwrite you —")
        print("pre-existing conditions can mean denial or 2-3x pricing.")
        hr("TRAP CHECKLIST (SEP mode)")
        print("1. COBRA is NOT creditable for the SEP — the clock ran from the")
        print("   job end you entered, even if COBRA is still paying claims.")
        print("2. Part D: penalty accrues 1%/month without creditable drug")
        print("   coverage — check the plan's creditable-coverage notice.")
        print("3. HSA: any Medicare entitlement (incl. Part A) blocks HSA")
        print("   contributions — stop 6 months before applying.")
        print("4. IRMAA: high income (roughly $106k+ single / $212k+ MFJ, 2-year")
        print("   lookback) surcharges Part B/D premiums.")
        hr("ACTION LIST (dated)")
        if left > 0:
            print(f"1. TODAY ({month_name(now)}) — enroll Parts A + B at SSA.gov;")
            print(f"   Part B effective {month_name(eff)}.")
            print(f"2. Same session — pick a Part D plan (avoid 1%/month penalty).")
            print(f"3. Through {month_name(gi_end)} — buy Medigap inside")
            print("   guaranteed issue.")
        else:
            gep, gep_eff, when = next_gep(now)
            print(f"1. {month_name(gep)} — General Enrollment ({when}).")
            print(f"2. {month_name(gep_eff)} — Part B starts; buy Medigap AT ONCE")
            print("   (the 6-month clock runs from Part B start).")
        return footer(a)

    # ---------------- mode: IEP (retired / no active coverage) ----------------
    hr("IEP STATUS")
    if months_between(now, iep_start) > 0:
        print(f"IEP hasn't opened yet — opens {month_name(iep_start)}.")
        print("Best move: enroll in the 3 months BEFORE your birthday month")
        print("→ coverage begins the first day of your birthday month.")
        print("Never wait for the birthday itself; later months push the")
        print("start date out by one month each.")
    elif months_between(now, iep_end) >= 0:
        pos = months_between(iep_start, now)
        eff = part_b_effective(now, iep_start, b65)
        print(f"IEP OPEN — you are in month {pos + 1} of 7.")
        if pos <= 3:
            print(f"Enrolling now → Part B effective {month_name(b65)} "
                  "(your birthday month). Ideal window — do it today.")
        else:
            print(f"Enrolling now → Part B effective {month_name(eff)}")
            print("  (post-birthday enrollments start coverage one month after")
            print("  the month you enroll — still penalty-free inside the IEP).")
    else:
        gep, gep_eff, when = next_gep(now)
        print(f"IEP ENDED {month_name(iep_end)} — {late_months} months ago.")
        print(f"Coverage path now: General Enrollment Period {month_name(gep)} "
              f"({when}) → Part B starts {month_name(gep_eff)}.")

    # penalties
    if months_between(now, iep_end) < 0:
        hr("PENALTY MATH (uncovered since IEP end)")
        if late_months <= 0:
            late_months = 0
        fy, pct, mo = penalty_b(late_months, a.premium_b)
        if late_months == 0:
            print("IEP not yet closed — no penalty possible today.")
        elif fy == 0:
            print(f"{late_months} months late — under 12, so no Part B penalty YET.")
            print(f"  At month 13 it becomes +10% of premium for LIFE. Months 1-12")
            print(f"  are the grace runway; they never reset.")
        else:
            print(f"{late_months} months late = {fy} full 12-month period(s).")
            print(f"Part B penalty: +{pct:.0%} of premium, for LIFE")
            print(f"  = {money(mo, True)}/mo  ≈ {money(mo * 12)}/yr  "
                  f"≈ {money(mo * 12 * a.estimate_years)} over {a.estimate_years} yr")
        if a.creditable_drug:
            print("Part D penalty: none — current drug coverage is creditable.")
        else:
            dm = drug_months if drug_months is not None else max(late_months, 0)
            dp = penalty_d(dm, a.premium_d_base)
            if dm > 0:
                print(f"Part D penalty: {dm} months × 1% × base premium "
                      f"= {money(dp, True)}/mo for LIFE")
                print(f"  ≈ {money(dp * 12)}/yr — even if you never take a drug.")
            else:
                print("Part D: no penalty yet if you enroll now.")

    # medigap clock
    hr("MEDIGAP GUARANTEED-ISSUE CLOCK")
    if months_between(now, iep_end) >= 0 and months_between(now, iep_start) <= 0:
        eff = part_b_effective(now, iep_start, b65)
    elif months_between(now, iep_end) < 0:
        # IEP already closed: Part B starts the July after the next GEP
        _, eff, _ = next_gep(now)
    else:
        # pre-IEP: enrolling in the 3 months before the birthday gives
        # birthday-month coverage
        eff = b65
    gi_end = add_months(eff, CONFIG["medigap_oep_months"])
    print(f"6-month Medigap open enrollment: Part B start {month_name(eff)}")
    print(f"  → guaranteed issue (no health questions, no denial) through "
          f"{month_name(gi_end)}.")
    print("Outside that window: insurers in most states can underwrite you —")
    print("pre-existing conditions can mean denial or 2-3x pricing. The clock")
    print("is real; missing it is the #1 expensive Medicare mistake.")

    hr("TRAP CHECKLIST (always)")
    print("1. COBRA: the 8-month SEP clock starts at JOB end, not COBRA end.")
    print("2. Small employer (<20): Medicare is primary even while working.")
    print("3. HSA: any Medicare entitlement (incl. Part A) blocks HSA")
    print("   contributions — stop 6 months before applying.")
    print("4. Part D: penalty accrues 1%/month even with zero prescriptions.")
    print("5. IRMAA: high income (roughly $106k+ single / $212k+ MFJ) adds a")
    print("   surcharge to Part B/D premiums based on a 2-year-lookback MAGI.")
    print("6. Part A is free with 40 work quarters — enroll even if you delay B.")
    print("7. Medigap 'guaranteed issue' only reliably exists inside the 6-month")
    print("   clock or after certain involuntarily-coverage-loss events.")

    hr("ACTION LIST (dated)")
    if months_between(now, iep_start) > 0:
        print(f"1. {month_name(add_months(b65, -3))} — IEP opens; enroll Parts A+B"
              f" that month for {month_name(b65)} coverage.")
        print(f"2. {month_name(add_months(b65, -2))} — pick Part D plan (drug")
        print("   coverage must start with the rest — no gap, no penalty).")
    elif months_between(now, iep_end) >= 0:
        print(f"1. TODAY ({month_name(now)}) — enroll Parts A + B + D.")
        print(f"2. {month_name(add_months(now, 1))} — coverage begins; keep every")
        print("   confirmation letter.")
        print(f"3. Through {month_name(gi_end)} — buy Medigap inside guaranteed issue.")
    else:
        gep, gep_eff, when = next_gep(now)
        print(f"1. {month_name(gep)} — General Enrollment (open {when}).")
        print(f"2. {month_name(gep_eff)} — Part B finally starts.")
        print("3. Same window — shop Medigap immediately; the 6-month clock runs")
        print("   from your Part B start, not from when you get around to it.")
        if a.hsa:
            print("4. HSA — stop contributions 6 months before the application.")
    footer(a)


def footer(a):
    print("\n" + "-" * 64)
    print(f"Constants used: Part B std premium {money(a.premium_b, True)}/mo, "
          f"Part D base {money(a.premium_d_base, True)}/mo.")
    print("VERIFY current-year figures at medicare.gov before acting — they")
    print("adjust annually (and with IRMAA). Educational tool, not advice.")
    print("-" * 64)
    return 0


if __name__ == "__main__":
    sys.exit(main())
