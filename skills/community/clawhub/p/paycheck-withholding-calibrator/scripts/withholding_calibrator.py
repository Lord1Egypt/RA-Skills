#!/usr/bin/env python3
"""Paycheck Withholding Calibrator — project your refund/owe BEFORE April.

From one paystub (YTD gross, YTD federal withholding, per-pay numbers,
paychecks left) it projects the tax-year federal liability with 2026-shaped
brackets, compares it to your withholding trajectory, prices the result
(a $4,000 refund is an interest-free loan; a $2,500 owe can add an
underpayment penalty), checks the safe harbors, and prints the exact
W-4 fix: the per-paycheck number for Step 4(c) or the Step 3 credit
adjustment to land on your target refund.

Usage:
  withholding_calibrator.py --ytd-gross 82000 --ytd-withheld 9400 \
      --per-pay-gross 6300 --per-pay-withheld 1080 --paychecks-left 8
  withholding_calibrator.py --ytd-gross 82000 --ytd-withheld 9400 \
      --per-pay-gross 6300 --paychecks-left 8 --filing mfj --dependents 2 \
      --other-income 3000 --target-refund 300 --last-year-tax 11500

stdlib only; federal only (state/local excluded). Bracket constants are
2026-shaped estimates — verify against IRS publications (footer printed).
Not tax advice.
"""
import argparse
import sys

# --- 2026-shaped federal constants (est., consistent with quarterly-tax-ranger) ---
STD_DEDUCTION = {"single": 15000, "mfj": 30000, "hoh": 22500}
BRACKETS = {
    "single": [(11925, .10), (48475, .12), (103350, .22), (197300, .24),
               (250525, .32), (626350, .35), (float("inf"), .37)],
    "mfj": [(23850, .10), (96950, .12), (206700, .22), (394600, .24),
            (501050, .32), (751600, .35), (float("inf"), .37)],
    "hoh": [(17000, .10), (64900, .12), (103350, .22), (197300, .24),
            (250500, .32), (626350, .35), (float("inf"), .37)],
}
CTC_PER_CHILD = 2000          # child tax credit (phaseouts not modeled)
CTC_PHASEOUT_START = {"single": 200000, "mfj": 400000, "hoh": 200000}
UNDERPAY_THRESHOLD = 1000     # owe more than this + fail harbors = penalty
SAFETY_RATE_CURRENT = 0.90
SAFETY_RATE_PRIOR = 1.00
SAFETY_RATE_PRIOR_HIGH_AGI = 1.10
HIGH_AGI = 150000
EST_PENALTY_RATE = 0.08       # annualized, for the rough penalty price
HYSA_RATE = 0.04              # opportunity cost of a big refund


def tax_liability(taxable, filing):
    tax, prev = 0.0, 0.0
    for upper, rate in BRACKETS[filing]:
        if taxable > prev:
            tax += (min(taxable, upper) - prev) * rate
            prev = upper
        else:
            break
    return tax


def ctc(dependents, filing, agi):
    if dependents <= 0:
        return 0.0
    start = CTC_PHASEOUT_START[filing]
    excess = max(0, agi - start)
    reduce = (excess // 1000) * 50   # $50 per $1,000 over
    return max(0.0, dependents * CTC_PER_CHILD - reduce)


def money(x, cents=False):
    return f"${x:,.2f}" if cents else f"${x:,.0f}"


def hr(title):
    print("\n" + "=" * 62)
    print(title)
    print("=" * 62)


def main():
    p = argparse.ArgumentParser(description=(__doc__ or "Paycheck Withholding Calibrator").split("\n")[0])
    p.add_argument("--ytd-gross", type=float, required=True)
    p.add_argument("--ytd-withheld", type=float, required=True)
    p.add_argument("--per-pay-gross", type=float, required=True)
    p.add_argument("--per-pay-withheld", type=float, default=None,
                   help="federal withholding per remaining paycheck "
                        "(default: YTD average rate applied to pay)")
    p.add_argument("--paychecks-left", type=int, required=True)
    p.add_argument("--filing", choices=list(BRACKETS), default="single")
    p.add_argument("--dependents", type=int, default=0)
    p.add_argument("--other-income", type=float, default=0.0,
                   help="self-employment / interest / gains / spouse wages "
                        "not in the paystub (annual)")
    p.add_argument("--itemized", type=float, default=None,
                   help="itemized deductions if larger than standard")
    p.add_argument("--target-refund", type=float, default=0.0,
                   help="aim for this refund at filing (default $0)")
    p.add_argument("--last-year-tax", type=float, default=None,
                   help="last year's total tax (safe-harbor check)")
    p.add_argument("--hyssa-rate", type=float, default=HYSA_RATE)
    a = p.parse_args()

    # --- trajectory ---
    if a.per_pay_withheld is None:
        rate = a.ytd_withheld / a.ytd_gross if a.ytd_gross else 0.0
        per_pay_wh = a.per_pay_gross * rate
        wh_note = f"derived from YTD rate ({rate:.1%})"
    else:
        per_pay_wh = a.per_pay_withheld
        wh_note = "from your paystub"

    proj_gross = a.ytd_gross + a.per_pay_gross * a.paychecks_left
    proj_wh = a.ytd_withheld + per_pay_wh * a.paychecks_left
    agi = proj_gross + a.other_income
    deduction = a.itemized if (a.itemized is not None and
                               a.itemized > STD_DEDUCTION[a.filing]) \
        else STD_DEDUCTION[a.filing]
    taxable = max(0.0, agi - deduction)
    liability = max(0.0, tax_liability(taxable, a.filing)
                    - ctc(a.dependents, a.filing, agi))

    delta = proj_wh - liability            # >0 refund, <0 owe
    refund = max(0.0, delta)
    owe = max(0.0, -delta)

    hr("TAX-YEAR PROJECTION")
    print(f"Projected gross (paystub) .... {money(proj_gross)}")
    if a.other_income:
        print(f"Other income ................ {money(a.other_income)}")
    print(f"Deduction applied ............ {money(deduction)} "
          f"({'itemized' if a.itemized and a.itemized > STD_DEDUCTION[a.filing] else 'standard'})")
    print(f"Projected taxable income ..... {money(taxable)}")
    print(f"Child tax credit ............. {money(ctc(a.dependents, a.filing, agi))}"
          + (" (0 dependents)" if a.dependents == 0 else ""))
    print(f"Projected federal liability .. {money(liability)}")
    print(f"Projected withholding ........ {money(proj_wh)}")
    print(f"  per-paycheck fed withheld .. {money(per_pay_wh, True)} ({wh_note})")

    hr("VERDICT")
    if refund > 1500:
        op_cost = refund / 2 * a.hyssa_rate
        print(f"BIG REFUND COMING: {money(refund)}.")
        print(f"  This is an interest-free loan to the Treasury for ~half a")
        print(f"  year — at {a.hyssa_rate:.0%} it costs you ≈ {money(op_cost)} of")
        print(f"  lost interest every year you keep this W-4.")
    elif refund > 300:
        print(f"REFUND: {money(refund)} — modest; fine if you like it.")
    elif owe < 300:
        print(f"ON TRACK: projected refund {money(refund)}, owe {money(owe)}.")
        print("  This is the calibrated outcome — file and forget.")
    elif owe < UNDERPAY_THRESHOLD:
        print(f"SMALL BALANCE DUE: {money(owe)} — under the "
              f"{money(UNDERPAY_THRESHOLD)} penalty threshold.")
        print("  Pay at filing; no penalty risk. Still fix next year's W-4.")
    else:
        print(f"OWE AT FILING: {money(owe)}.")

    # safe harbor
    if owe >= UNDERPAY_THRESHOLD:
        print("\nUNDERPAYMENT-PENALTY CHECK (Form 2210):")
        harbor_90 = SAFETY_RATE_CURRENT * liability
        lines = [f"  90% of current liability ........ {money(harbor_90)}"]
        need_prior = True
        if a.last_year_tax is not None:
            rate_prior = (SAFETY_RATE_PRIOR_HIGH_AGI if agi > HIGH_AGI
                          else SAFETY_RATE_PRIOR)
            harbor_prior = rate_prior * a.last_year_tax
            lines.append(f"  {rate_prior:.0%} of last year's tax "
                         f"........ {money(harbor_prior)}")
        else:
            harbor_prior = float("inf")
            lines.append("  prior-year harbor: supply --last-year-tax")
        safe = proj_wh >= min(harbor_90, harbor_prior)
        for ln in lines:
            print(ln)
        if safe:
            print("  → WITHIN a safe harbor: penalty avoided even though you owe.")
        else:
            gap = min(harbor_90, harbor_prior) - proj_wh
            rough = max(0.0, gap) * EST_PENALTY_RATE / 2
            print(f"  → NO safe harbor. Est. shortfall {money(gap)};")
            print(f"    rough penalty ≈ {money(rough)} (annualized-8% estimate).")
            print(f"    Fix: add extra withholding OR make a Q4 estimated")
            print(f"    payment (due Jan 15) — withholding is dated as paid")
            print(f"    evenly, estimates aren't.")

    # ---- the fix ----
    hr("W-4 FIX (to hit target refund "
       f"{money(a.target_refund)})")
    need = liability + a.target_refund - proj_wh  # + withhold more
    if need > 0.5:
        per_pay = need / a.paychecks_left
        print(f"UNDER-withheld by {money(need)}.")
        print(f"  W-4 Step 4(c) 'Extra withholding' = "
              f"{money(per_pay, True)} per paycheck")
        print(f"  ({money(need)} across {a.paychecks_left} paychecks)")
        print(f"  Alternative: one estimated-tax payment of {money(need)} by")
        print(f"  Jan 15 (Jan payment only — withholding timing is gentler).")
    elif need < -0.5:
        over = -need
        per_pay = over / a.paychecks_left
        annual = over
        print(f"OVER-withheld by {money(over)}.")
        print(f"  Raise take-home by {money(per_pay, True)}/paycheck:")
        print(f"  - W-4 Step 3: add {money(annual)} of credits you're entitled")
        print(f"    to but haven't claimed (child/dependent/other);")
        print(f"  - W-4 Step 4(b): deductions you itemize (mortgage interest,")
        print(f"    etc. — the {money(deduction)} deduction is only partially")
        print(f"    built into the default W-4);")
        print(f"  - or just enjoy the forced savings — it costs ≈ "
              f"{money(over / 2 * a.hyssa_rate)}/yr in lost interest.")
    else:
        print("Calibrated within $1 — change nothing.")

    print("\n" + "-" * 62)
    print("Federal income tax only — state/local and FICA excluded.")
    print("2026-shaped brackets/deduction are estimates: VERIFY against")
    print("current IRS tables before acting. Educational, not tax advice.")
    print("-" * 62)
    return 0


if __name__ == "__main__":
    sys.exit(main())
