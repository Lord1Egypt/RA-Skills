#!/usr/bin/env python3
"""mortgage_math.py — true ownership cost, DTI verdicts, rate shock, rent-vs-buy break-even.

Stdlib only. Example:
  python3 mortgage_math.py --price 450000 --down 45000 --rate 6.5 --income 8500 \
      --other-debt 400 --rent 2100
"""
import argparse
import json
import sys


def monthly_pi(principal: float, apr_pct: float, years: int) -> float:
    r = apr_pct / 100.0 / 12.0
    n = years * 12
    if r == 0:
        return principal / n
    f = (1 + r) ** n
    return principal * r * f / (f - 1)


def schedule_balance(principal, apr_pct, years, month):
    """Remaining balance after `month` payments."""
    r = apr_pct / 100.0 / 12.0
    n = years * 12
    if r == 0:
        return principal * (1 - month / n)
    f = (1 + r) ** month
    return principal * f - monthly_pi(principal, apr_pct, years) * (f - 1) / r


def pmi_exit_month(principal, apr_pct, years, price, apprec_pct):
    """First month where equity >= 20% of appreciated value (PMI off)."""
    for m in range(1, years * 12 + 1):
        val = price * (1 + apprec_pct / 100.0 / 12.0) ** m
        bal = schedule_balance(principal, apr_pct, years, m)
        if (val - bal) / val >= 0.20:
            return m
    return years * 12


def fv(pv, annual_pct, years):
    r = annual_pct / 100.0
    return pv * (1 + r) ** years


def rent_vs_buy(price, down, apr_pct, years, tax_pct, ins_pct, hoa, pmi_pct, maint_pct,
                closing_pct, sell_pct, apprec_pct, invest_pct, rent, rent_growth_pct):
    """Equal-outlay model: both sides spend own_m/month (buyer on the house,
    renter rent + investing the difference). Terminal wealth: buyer = sale
    proceeds net of selling costs; renter = grown portfolio."""
    loan = price - down
    closing = price * closing_pct / 100.0
    pi = monthly_pi(loan, apr_pct, years)
    tax_m = price * tax_pct / 100.0 / 12.0
    ins_m = price * ins_pct / 100.0 / 12.0
    maint_m = price * maint_pct / 100.0 / 12.0
    pmi_m = loan * pmi_pct / 100.0 / 12.0
    exit_m = pmi_exit_month(loan, apr_pct, years, price, apprec_pct)
    ir = invest_pct / 100.0 / 12.0

    def own_cost(m):
        return pi + tax_m + ins_m + hoa + maint_m + (pmi_m if m <= exit_m else 0.0)

    breakeven = None
    rows = []
    for y in range(1, 31):
        renter = down + closing  # renter invests the buyer's initial cash outlay
        for m in range(1, y * 12 + 1):
            r_m = rent * (1 + rent_growth_pct / 100.0 / 12.0) ** (m - 1)
            renter = renter * (1 + ir) + (own_cost(m) - r_m) * (1 + ir)
        home_val = price * (1 + apprec_pct / 100.0) ** y
        bal = schedule_balance(loan, apr_pct, years, min(y * 12, years * 12))
        buyer = home_val - bal - home_val * sell_pct / 100.0
        rows.append((y, buyer, renter, buyer - renter))
        if breakeven is None and buyer - renter > 0:
            breakeven = y
    return {"pi": pi, "pmi_exit_month": exit_m, "breakeven_year": breakeven,
            "rows": rows}


def main():
    p = argparse.ArgumentParser(description="True-cost mortgage affordability + rent-vs-buy.")
    p.add_argument("--price", type=float, required=True)
    p.add_argument("--down", type=float, required=True)
    p.add_argument("--rate", type=float, default=6.5, help="APR %%")
    p.add_argument("--term", type=int, default=30)
    p.add_argument("--tax-pct", type=float, default=1.1, help="property tax %%/yr")
    p.add_argument("--insurance-pct", type=float, default=0.35, help="insurance %%/yr of price")
    p.add_argument("--insurance", type=float, default=None, help="insurance $/yr (overrides pct)")
    p.add_argument("--hoa", type=float, default=0.0)
    p.add_argument("--pmi-pct", type=float, default=0.5, help="PMI %%/yr of loan")
    p.add_argument("--maint-pct", type=float, default=1.0, help="maintenance %%/yr of price")
    p.add_argument("--income", type=float, required=True, help="gross monthly income")
    p.add_argument("--other-debt", type=float, default=0.0)
    p.add_argument("--rent", type=float, default=None, help="current rent for comparison")
    p.add_argument("--appreciation", type=float, default=3.0)
    p.add_argument("--invest-return", type=float, default=6.0)
    p.add_argument("--rent-growth", type=float, default=3.0)
    p.add_argument("--closing-pct", type=float, default=3.0)
    p.add_argument("--sell-pct", type=float, default=6.5)
    p.add_argument("--json", action="store_true")
    a = p.parse_args()

    loan = a.price - a.down
    ltv = loan / a.price
    pmi_applies = ltv > 0.80
    ins_yr = a.insurance if a.insurance is not None else a.price * a.insurance_pct / 100.0

    pi = monthly_pi(loan, a.rate, a.term)
    tax_m = a.price * a.tax_pct / 100.0 / 12.0
    ins_m = ins_yr / 12.0
    pmi_m = (loan * a.pmi_pct / 100.0 / 12.0) if pmi_applies else 0.0
    maint_m = a.price * a.maint_pct / 100.0 / 12.0
    true_m = pi + tax_m + ins_m + a.hoa + pmi_m + maint_m

    front = true_m / a.income
    back = (true_m + a.other_debt) / a.income

    def verdict(x):
        return "PASS" if x <= 0.28 + 1e-9 or (x <= 0.36) else ("TIGHT" if x <= 0.43 else "FAIL")

    shock = {}
    for d in (0, 1, 2):
        s_pi = monthly_pi(loan, a.rate + d, a.term)
        s_true = s_pi + tax_m + ins_m + a.hoa + pmi_m + maint_m
        shock[f"+{d}%"] = {"pi": round(s_pi), "true_monthly": round(s_true),
                           "back_dti": round((s_true + a.other_debt) / a.income * 100, 1)}

    # Max price that passes back-end 36%: binary search
    lo, hi = 50000.0, a.price * 2
    def back_at(px):
        l = px - a.down
        if l <= 0:
            return 0.0
        pm = (l * a.pmi_pct / 100.0 / 12.0) if l / px > 0.80 else 0.0
        return (monthly_pi(l, a.rate, a.term) + px * a.tax_pct / 100.0 / 12.0 +
                px * a.insurance_pct / 100.0 / 12.0 + a.hoa + pm +
                px * a.maint_pct / 100.0 / 12.0 + a.other_debt) / a.income

    for _ in range(50):
        mid = (lo + hi) / 2
        if back_at(mid) <= 0.36:
            lo = mid
        else:
            hi = mid
    max_price = lo if back_at(lo) <= 0.36 else 0

    rvb = None
    if a.rent:
        rvb = rent_vs_buy(a.price, a.down, a.rate, a.term, a.tax_pct,
                          a.insurance_pct, a.hoa, a.pmi_pct if pmi_applies else 0,
                          a.maint_pct, a.closing_pct, a.sell_pct, a.appreciation,
                          a.invest_return, a.rent, a.rent_growth)
        rvb["rows"] = rvb["rows"][:30]

    out = {
        "loan": loan, "ltv_pct": round(ltv * 100, 1),
        "monthly": {"pi": round(pi), "tax": round(tax_m), "insurance": round(ins_m),
                    "pmi": round(pmi_m) if pmi_m else 0, "hoa": round(a.hoa),
                    "maintenance": round(maint_m), "true_total": round(true_m)},
        "dti": {"front_pct": round(front * 100, 1), "front_verdict": "PASS" if front <= 0.28 else ("TIGHT" if front <= 0.31 else "FAIL"),
                "back_pct": round(back * 100, 1), "back_verdict": "PASS" if back <= 0.36 else ("TIGHT" if back <= 0.43 else "FAIL")},
        "rate_shock": shock,
        "max_price_at_36_backdti": round(max_price),
        "rent_vs_buy": ({"breakeven_year": rvb["breakeven_year"],
                         "pmi_exit_month": rvb["pmi_exit_month"],
                         "year5_gap": round(rvb["rows"][4][3]),
                         "year10_gap": round(rvb["rows"][9][3])} if rvb else None),
    }
    if a.json:
        print(json.dumps(out, indent=2))
        return

    m = out["monthly"]
    print(f"Loan ${loan:,.0f}  LTV {out['ltv_pct']}%")
    print(f"P&I ............... ${m['pi']:>8,}/mo")
    print(f"Property tax ...... ${m['tax']:>8,}/mo")
    print(f"Insurance ......... ${m['insurance']:>8,}/mo")
    if m["pmi"]:
        print(f"PMI ............... ${m['pmi']:>8,}/mo  (until ~month {out['rent_vs_buy']['pmi_exit_month'] if out['rent_vs_buy'] else '?'})")
    if m["hoa"]:
        print(f"HOA ............... ${m['hoa']:>8,}/mo")
    print(f"Maintenance ....... ${m['maintenance']:>8,}/mo  (1%/yr rule)")
    print(f"TRUE MONTHLY ...... ${m['true_total']:>8,}/mo")
    d = out["dti"]
    print(f"\nFront-end DTI {d['front_pct']}% [{d['front_verdict']}]   Back-end DTI {d['back_pct']}% [{d['back_verdict']}]  (targets 28/36)")
    if back > 0.36:
        print(f"→ Max price passing 36% back-end at this down payment: ${out['max_price_at_36_backdti']:,.0f}")
    print("\nRate shock:")
    for k, v in out["rate_shock"].items():
        print(f"  {k:>3}: true ${v['true_monthly']:,}/mo  back-DTI {v['back_dti']}%")
    if out["rent_vs_buy"]:
        r = out["rent_vs_buy"]
        be = r["breakeven_year"]
        print(f"\nRent ${a.rent:,.0f}/mo vs buy: break-even at year {be if be else 'NEVER (>30y)'}")
        print(f"  Year 5 gap (buy−rent wealth): ${r['year5_gap']:,}   Year 10: ${r['year10_gap']:,}")


if __name__ == "__main__":
    main()
