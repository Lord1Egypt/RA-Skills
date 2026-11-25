#!/usr/bin/env python3
"""
India income tax: New vs Old regime comparison for resident individuals.
Tax Year 2026-27 (income earned 1 Apr 2026 - 31 Mar 2027), Income-tax Act, 2025.

Usage:
    python tax.py '{"salary": 1800000, "age": 30, "sec_80c": 150000}'
    python tax.py input.json
    python tax.py --example        # prints a sample input

All amounts are yearly, in rupees. Pure standard library, no network access.
Scope: salary / pension, interest, rent and other income taxed at normal slab
rates. NOT covered: capital gains at special rates, business income (44AD etc.),
non-residents, HUFs, agricultural income aggregation.
"""
import json, sys

RULES = {
    "tax_year": "2026-27",
    "new": {
        "slabs": [(400000, 0.0), (800000, 0.05), (1200000, 0.10), (1600000, 0.15),
                  (2000000, 0.20), (2400000, 0.25), (None, 0.30)],
        "standard_deduction": 75000,
        "rebate_limit": 1200000, "rebate_max": 60000,
        "surcharge": [(5000000, 0.10), (10000000, 0.15), (20000000, 0.25)],  # capped at 25%
    },
    "old": {
        "slabs_by_age": {
            "below_60": [(250000, 0.0), (500000, 0.05), (1000000, 0.20), (None, 0.30)],
            "60_to_79": [(300000, 0.0), (500000, 0.05), (1000000, 0.20), (None, 0.30)],
            "80_plus":  [(500000, 0.0), (1000000, 0.20), (None, 0.30)],
        },
        "standard_deduction": 50000,
        "rebate_limit": 500000, "rebate_max": 12500,
        "surcharge": [(5000000, 0.10), (10000000, 0.15), (20000000, 0.25), (50000000, 0.37)],
        "caps": {"sec_80c": 150000, "sec_80ccd_1b": 50000, "home_loan_interest": 200000},
    },
    "cess": 0.04,
    # 50% HRA cities (metro list as extended from Tax Year 2026-27)
    "hra_metros": ["delhi", "mumbai", "kolkata", "chennai",
                   "bengaluru", "bangalore", "hyderabad", "pune", "ahmedabad"],
}

EXAMPLE = {
    "salary": 1800000,            # gross salary incl. HRA, before any deduction
    "other_income": 20000,        # savings/FD interest, rent (after 30%), etc.
    "age": 30,
    "is_salaried": True,          # gets standard deduction (also true for pensioners)
    "basic_da": 720000,           # needed for HRA and employer-NPS limits
    "hra_received": 360000,
    "rent_paid": 300000,
    "city": "pune",
    "sec_80c": 150000,            # EPF, PPF, ELSS, LIC, tuition fees, home-loan principal
    "sec_80ccd_1b": 50000,        # own extra NPS
    "employer_nps": 0,            # 80CCD(2) - allowed in BOTH regimes
    "health_insurance_self": 25000,
    "health_insurance_parents": 0,
    "parents_senior": False,
    "home_loan_interest": 0,      # self-occupied house
    "professional_tax": 2500,
    "other_old_deductions": 0,    # 80E, 80G, 80TTA etc. (old regime only)
}


def slab_tax(income, slabs):
    tax, lower = 0.0, 0
    for upper, rate in slabs:
        if upper is None or income <= upper:
            tax += (income - lower) * rate
            return tax
        tax += (upper - lower) * rate
        lower = upper
    return tax


def surcharge_with_relief(income, base_tax, slabs_fn, surcharge_table):
    rate, threshold = 0.0, None
    for limit, r in surcharge_table:
        if income > limit:
            rate, threshold = r, limit
    if not rate:
        return 0.0
    sur = base_tax * rate
    # marginal relief: tax+surcharge may not exceed tax at threshold (with its own
    # lower surcharge) plus the income above the threshold
    lower_rate = 0.0
    for limit, r in surcharge_table:
        if limit < threshold:
            lower_rate = r
    at_threshold = slabs_fn(threshold) * (1 + lower_rate)
    cap = at_threshold + (income - threshold)
    return max(0.0, min(sur, cap - base_tax))


def finish(taxable, slabs, rebate_limit, rebate_max, surcharge_table, regime):
    base = slab_tax(taxable, slabs)
    rebate, relief = 0.0, 0.0
    if taxable <= rebate_limit:
        rebate = min(base, rebate_max)
    elif regime == "new":
        # marginal relief just above the rebate limit
        excess = taxable - rebate_limit
        if base > excess:
            relief = base - excess
    after = base - rebate - relief
    sur = surcharge_with_relief(taxable, after, lambda x: slab_tax(x, slabs), surcharge_table)
    cess = (after + sur) * RULES["cess"]
    total = after + sur + cess
    return {"taxable_income": round(taxable), "slab_tax": round(base),
            "rebate": round(rebate), "marginal_relief": round(relief),
            "surcharge": round(sur), "cess": round(cess),
            "total_tax": int(round(total / 10.0) * 10)}  # rounded to nearest Rs 10


def hra_exemption(d):
    hra, rent, basic = d.get("hra_received", 0), d.get("rent_paid", 0), d.get("basic_da", 0)
    if not (hra and rent and basic):
        return 0
    pct = 0.5 if str(d.get("city", "")).strip().lower() in RULES["hra_metros"] else 0.4
    return max(0, min(hra, rent - 0.1 * basic, pct * basic))


def compute(d):
    salary = float(d.get("salary", 0))
    other = float(d.get("other_income", 0))
    age = int(d.get("age", 30))
    salaried = d.get("is_salaried", salary > 0)
    gross = salary + other
    emp_nps = float(d.get("employer_nps", 0))
    basic = float(d.get("basic_da", 0))
    if basic:
        emp_nps_new = min(emp_nps, 0.14 * basic)
        emp_nps_old = min(emp_nps, 0.10 * basic)
    else:
        emp_nps_new = emp_nps_old = emp_nps

    # ---- new regime
    n = RULES["new"]
    sd_new = min(n["standard_deduction"], salary) if salaried else 0
    taxable_new = max(0, gross - sd_new - emp_nps_new)
    new = finish(taxable_new, n["slabs"], n["rebate_limit"], n["rebate_max"], n["surcharge"], "new")
    new["deductions_used"] = {"standard_deduction": round(sd_new), "employer_nps": round(emp_nps_new)}

    # ---- old regime
    o = RULES["old"]
    band = "80_plus" if age >= 80 else "60_to_79" if age >= 60 else "below_60"
    caps = o["caps"]
    sd_old = min(o["standard_deduction"], salary) if salaried else 0
    hra = hra_exemption(d)
    hi_self_cap = 50000 if age >= 60 else 25000
    hi_par_cap = 50000 if d.get("parents_senior") else 25000
    ded = {
        "standard_deduction": sd_old,
        "hra_exemption": hra,
        "professional_tax": min(float(d.get("professional_tax", 0)), 2500),
        "sec_80c": min(float(d.get("sec_80c", 0)), caps["sec_80c"]),
        "sec_80ccd_1b": min(float(d.get("sec_80ccd_1b", 0)), caps["sec_80ccd_1b"]),
        "employer_nps": emp_nps_old,
        "health_insurance": min(float(d.get("health_insurance_self", 0)), hi_self_cap)
                            + min(float(d.get("health_insurance_parents", 0)), hi_par_cap),
        "home_loan_interest": min(float(d.get("home_loan_interest", 0)), caps["home_loan_interest"]),
        "other": float(d.get("other_old_deductions", 0)),
    }
    taxable_old = max(0, gross - sum(ded.values()))
    slabs_old = o["slabs_by_age"][band]
    old = finish(taxable_old, slabs_old, o["rebate_limit"], o["rebate_max"], o["surcharge"], "old")
    old["deductions_used"] = {k: round(v) for k, v in ded.items() if v}

    # ---- break-even: extra old-regime deductions needed to match the new regime
    breakeven = None
    if old["total_tax"] > new["total_tax"]:
        lo, hi = 0.0, taxable_old
        for _ in range(60):
            mid = (lo + hi) / 2
            t = finish(max(0, taxable_old - mid), slabs_old, o["rebate_limit"], o["rebate_max"],
                       o["surcharge"], "old")["total_tax"]
            lo, hi = (mid, hi) if t > new["total_tax"] else (lo, mid)
        breakeven = int(round(hi / 1000.0) * 1000) if hi < taxable_old else None

    better = "new" if new["total_tax"] < old["total_tax"] else \
             "old" if old["total_tax"] < new["total_tax"] else "same"
    return {
        "tax_year": RULES["tax_year"],
        "gross_income": round(gross),
        "new_regime": new,
        "old_regime": old,
        "better_regime": better,
        "saving": abs(new["total_tax"] - old["total_tax"]),
        "extra_old_deductions_to_break_even": breakeven,
        "monthly_tds_estimate": {"new": round(new["total_tax"] / 12), "old": round(old["total_tax"] / 12)},
        "notes": [
            "Resident individual, normal-rate income only; capital gains at special rates are excluded.",
            "Estimate only - confirm on the official calculator at incometax.gov.in or with a CA.",
        ],
    }


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    arg = sys.argv[1]
    if arg == "--example":
        print(json.dumps(EXAMPLE, indent=2))
        return
    data = json.load(open(arg, encoding="utf-8")) if arg.endswith(".json") else json.loads(arg)
    print(json.dumps(compute(data), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
