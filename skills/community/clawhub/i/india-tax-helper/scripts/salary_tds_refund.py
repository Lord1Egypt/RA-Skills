#!/usr/bin/env python3
import argparse
from common import load_json, load_rules, blocked, estimate_payload, dump, RulesError


def compute_tax(taxable_income: float, slabs: list[dict]) -> float:
    tax = 0.0
    prev_limit = 0.0
    for slab in slabs:
        upper = slab.get('up_to')
        rate = slab['rate']
        if upper is None:
            taxable = max(0.0, taxable_income - prev_limit)
        else:
            taxable = max(0.0, min(taxable_income, upper) - prev_limit)
        tax += taxable * rate
        prev_limit = upper if upper is not None else prev_limit
    return round(tax, 2)


def compute_surcharge(taxable_income: float, base_tax: float, surcharge_rules: list[dict]) -> float:
    for band in surcharge_rules:
        lower = band['income_above']
        upper = band.get('up_to')
        if taxable_income > lower and (upper is None or taxable_income <= upper):
            return round(base_tax * band['rate'], 2)
    return 0.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', required=True)
    ap.add_argument('--rules')
    args = ap.parse_args()

    data = load_json(args.input)
    try:
        rules = load_rules(args.rules)
    except RulesError as e:
        dump(blocked(str(e), ['verified salary tax rules JSON']))
        return

    fy = data.get('fy')
    regime = data.get('regime')
    if not fy or not regime:
        dump(blocked('Missing FY or regime', ['fy', 'regime']))
        return

    fy_rules = rules.get('salary_regimes', {}).get(fy)
    if not fy_rules:
        dump(blocked(f'No verified salary rules for FY={fy}', ['matching rules entry']))
        return

    regime_rules = fy_rules.get(regime)
    if not regime_rules:
        dump(blocked(f'No verified salary rules for FY={fy}, regime={regime}', ['matching rules entry']))
        return

    # Old regime has age-based slabs
    slabs = None
    if regime == 'old':
        age = data.get('age')
        if age is None:
            dump(blocked('Age required for old regime slab selection', ['age']))
            return
        age = int(age)
        if age >= 80:
            slabs = regime_rules['age_80_plus']['slabs']
        elif age >= 60:
            slabs = regime_rules['age_60_to_79']['slabs']
        else:
            slabs = regime_rules['age_less_than_60']['slabs']
    else:
        slabs = regime_rules['slabs']

    gross_salary = float(data.get('gross_salary', 0))
    other_income = float(data.get('other_income', 0))
    tds = float(data.get('tds', 0))
    deductions = float(data.get('deductions', 0))
    standard_deduction = float(regime_rules.get('standard_deduction', 0))

    assumptions = []
    if not data.get('gross_salary'):
        dump(blocked('Missing gross salary', ['gross_salary']))
        return
    if not data.get('tds'):
        assumptions.append('TDS missing or zero; refund/payable estimate may be incomplete')

    taxable_income = max(0.0, gross_salary + other_income - deductions - standard_deduction)
    base_tax = compute_tax(taxable_income, slabs)

    # Rebate 87A
    rebate = 0.0
    rebate_rule = regime_rules.get('rebate_87a')
    if rebate_rule and taxable_income <= rebate_rule['taxable_income_limit']:
        rebate = min(base_tax, rebate_rule['max_rebate'])

    post_rebate = max(0.0, base_tax - rebate)

    # Surcharge
    surcharge = 0.0
    if regime == 'new' and 'surcharge' in rules:
        surcharge = compute_surcharge(taxable_income, post_rebate, rules['surcharge']['new_regime'])
    elif regime == 'old' and 'surcharge' in rules:
        surcharge = compute_surcharge(taxable_income, post_rebate, rules['surcharge']['old_regime'])

    # Cess
    cess_rate = rules.get('cess', {}).get('health_and_education', 0.0)
    cess = round((post_rebate + surcharge) * cess_rate, 2)

    total_tax = round(post_rebate + surcharge + cess, 2)
    refund_or_payable = round(tds - total_tax, 2)

    dump(estimate_payload(
        'salary_tds_refund',
        data,
        assumptions,
        {
            'taxable_income': round(taxable_income, 2),
            'base_tax': base_tax,
            'rebate_87a': round(rebate, 2),
            'post_rebate_tax': round(post_rebate, 2),
            'surcharge': round(surcharge, 2),
            'cess': cess,
            'total_tax': total_tax,
            'tds': round(tds, 2),
            'refund_if_positive_else_additional_tax': refund_or_payable,
        },
    ))


if __name__ == '__main__':
    main()
