#!/usr/bin/env python3
import argparse
import json
import sys

MORTGAGE_RATE_DEFAULT = 0.035
DOWN_PAYMENT_RATIO = 0.20
VACANCY_RATE = 0.05
MAINTENANCE_RATIO = 0.01
INSURANCE_MONTHLY = 150
APPRECIATION_RATE = 0.035
MARGINAL_TAX_RATE = 0.46
LOC_RATE = 0.0495

WELCOME_TAX_BRACKETS = [
    (50000, 0.005),
    (250000, 0.010),
    (500000, 0.015),
    (999999, 0.020),
    (float("inf"), 0.025),
]


def calc_welcome_tax(price):
    tax = 0
    prev = 0
    for limit, rate in WELCOME_TAX_BRACKETS:
        band = min(price, limit) - prev
        if band <= 0:
            break
        tax += band * rate
        prev = limit
    return tax


def calc_monthly_mortgage(principal, annual_rate, amort_years=25):
    r = annual_rate / 12
    n = amort_years * 12
    if r == 0:
        return principal / n
    return principal * r * (1 + r) ** n / ((1 + r) ** n - 1)


def analyze(price, monthly_rent, property_tax_annual, units=1, mortgage_rate=MORTGAGE_RATE_DEFAULT):
    down = price * DOWN_PAYMENT_RATIO
    loan = price - down
    welcome_tax = calc_welcome_tax(price)
    total_acquisition_cost = down + welcome_tax

    monthly_mortgage = calc_monthly_mortgage(loan, mortgage_rate)
    effective_rent = monthly_rent * (1 - VACANCY_RATE)
    maintenance_monthly = price * MAINTENANCE_RATIO / 12
    property_tax_monthly = property_tax_annual / 12

    total_monthly_expenses = (
        monthly_mortgage
        + maintenance_monthly
        + property_tax_monthly
        + INSURANCE_MONTHLY
    )

    monthly_cash_flow = effective_rent - total_monthly_expenses
    annual_cash_flow = monthly_cash_flow * 12

    noi = (effective_rent - maintenance_monthly - property_tax_monthly - INSURANCE_MONTHLY) * 12
    cap_rate = noi / price
    coc = annual_cash_flow / total_acquisition_cost
    grm = price / (monthly_rent * 12)
    annual_appreciation = price * APPRECIATION_RATE
    total_annual_return = annual_cash_flow + annual_appreciation
    total_return_pct = total_annual_return / total_acquisition_cost

    after_tax_cash_flow = annual_cash_flow * (1 - MARGINAL_TAX_RATE) if annual_cash_flow > 0 else annual_cash_flow

    result = {
        "inputs": {
            "purchase_price": price,
            "monthly_rent": monthly_rent,
            "property_tax_annual": property_tax_annual,
            "units": units,
            "mortgage_rate_pct": round(mortgage_rate * 100, 2),
        },
        "acquisition": {
            "down_payment": round(down),
            "welcome_tax": round(welcome_tax),
            "total_upfront_cost": round(total_acquisition_cost),
            "loan_amount": round(loan),
        },
        "monthly": {
            "gross_rent": round(monthly_rent),
            "effective_rent_after_vacancy": round(effective_rent),
            "mortgage_payment": round(monthly_mortgage),
            "property_tax": round(property_tax_monthly),
            "maintenance_reserve": round(maintenance_monthly),
            "insurance": INSURANCE_MONTHLY,
            "total_expenses": round(total_monthly_expenses),
            "net_cash_flow": round(monthly_cash_flow),
        },
        "annual": {
            "cash_flow": round(annual_cash_flow),
            "after_tax_cash_flow": round(after_tax_cash_flow),
            "appreciation_estimate": round(annual_appreciation),
            "total_return": round(total_annual_return),
        },
        "metrics": {
            "cap_rate_pct": round(cap_rate * 100, 2),
            "cash_on_cash_pct": round(coc * 100, 2),
            "gross_rent_multiplier": round(grm, 1),
            "total_return_on_equity_pct": round(total_return_pct * 100, 2),
        },
    }

    thresholds = {
        "cash_flow_ok": monthly_cash_flow > 0,
        "coc_ok": coc >= 0.05,
        "cap_rate_ok": cap_rate >= 0.045,
        "grm_ok": grm < 20,
    }
    passed = sum(thresholds.values())

    if passed == 4:
        verdict = "✅ BUY"
        reason = "All thresholds met. Positive cash flow and solid returns."
    elif passed >= 2 and thresholds["cash_flow_ok"]:
        verdict = "⚠️ INVESTIGATE"
        reason = "Positive cash flow but some metrics below target. Verify actuals before proceeding."
    else:
        verdict = "❌ PASS"
        reason = "Does not meet minimum investment criteria."

    result["thresholds"] = thresholds
    result["conclusion"] = {"verdict": verdict, "reason": reason}
    return result


def main():
    parser = argparse.ArgumentParser(description="Analyze a rental property investment.")
    parser.add_argument("--price", type=float, required=True, help="Purchase price in CAD")
    parser.add_argument("--rent", type=float, required=True, help="Total monthly gross rent in CAD")
    parser.add_argument("--tax", type=float, default=3600, help="Annual property tax in CAD (default: 3600)")
    parser.add_argument("--units", type=int, default=1, help="Number of units")
    parser.add_argument("--rate", type=float, default=MORTGAGE_RATE_DEFAULT, help="Mortgage annual rate (default: 0.035)")
    args = parser.parse_args()

    result = analyze(args.price, args.rent, args.tax, args.units, args.rate)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()

