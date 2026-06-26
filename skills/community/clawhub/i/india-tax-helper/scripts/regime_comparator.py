#!/usr/bin/env python3
"""
Compare old vs new regime for a given income profile.
Outputs which is better and by how much.
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import load_json, load_rules, blocked, estimate_payload, dump, RulesError


def compute_tax_from_slabs(taxable_income: float, slabs: list[dict]) -> float:
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


def compute_regime_tax(taxable_income: float, regime: str, age: int, rules: dict):
    fy_rules = rules.get('salary_regimes', {}).get('FY-2026-27', {}).get(regime)
    if not fy_rules:
        return None

    if regime == 'old':
        if age >= 80:
            slabs = fy_rules['age_80_plus']['slabs']
        elif age >= 60:
            slabs = fy_rules['age_60_to_79']['slabs']
        else:
            slabs = fy_rules['age_less_than_60']['slabs']
    else:
        slabs = fy_rules['slabs']

    base_tax = compute_tax_from_slabs(taxable_income, slabs)

    rebate = 0.0
    rebate_rule = fy_rules.get('rebate_87a')
    if rebate_rule and taxable_income <= rebate_rule['taxable_income_limit']:
        rebate = min(base_tax, rebate_rule['max_rebate'])

    post_rebate = max(0.0, base_tax - rebate)

    surcharge = 0.0
    if 'surcharge' in rules:
        key = 'new_regime' if regime == 'new' else 'old_regime'
        surcharge = compute_surcharge(taxable_income, post_rebate, rules['surcharge'][key])

    cess_rate = rules.get('cess', {}).get('health_and_education', 0.0)
    cess = round((post_rebate + surcharge) * cess_rate, 2)

    return {
        'base_tax': base_tax,
        'rebate_87a': rebate,
        'post_rebate': post_rebate,
        'surcharge': surcharge,
        'cess': cess,
        'total_tax': round(post_rebate + surcharge + cess, 2),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', required=True)
    ap.add_argument('--rules')
    args = ap.parse_args()

    data = load_json(args.input)
    try:
        rules = load_rules(args.rules)
    except RulesError as e:
        dump(blocked(str(e), ['verified rules JSON']))
        return

    fy = data.get('fy', 'FY-2026-27')
    age = int(data.get('age', 30))
    gross_salary = float(data.get('gross_salary', 0))

    # New regime: only standard deduction
    std_new = rules.get('standard_deduction', {}).get('new_regime', 75000)
    taxable_new = max(0.0, gross_salary - std_new)
    new_result = compute_regime_tax(taxable_new, 'new', age, rules)

    # Old regime: standard deduction + Chapter VIA deductions
    std_old = rules.get('standard_deduction', {}).get('old_regime', 50000)
    deductions = float(data.get('deductions', 0))
    taxable_old = max(0.0, gross_salary - deductions - std_old)
    old_result = compute_regime_tax(taxable_old, 'old', age, rules)

    if not new_result or not old_result:
        dump(blocked('Could not compute one or both regimes', ['rules']))
        return

    diff = round(old_result['total_tax'] - new_result['total_tax'], 2)
    if diff > 0:
        winner = 'new'
        savings = diff
    elif diff < 0:
        winner = 'old'
        savings = -diff
    else:
        winner = 'tie'
        savings = 0.0

    assumptions = []
    if not deductions:
        assumptions.append('No deductions provided; old regime may look worse than it could be')

    dump(estimate_payload(
        'regime_comparison',
        data,
        assumptions,
        {
            'fy': fy,
            'age': age,
            'gross_salary': gross_salary,
            'new_regime': {
                'taxable_income': round(taxable_new, 2),
                **new_result,
            },
            'old_regime': {
                'taxable_income': round(taxable_old, 2),
                'deductions_claimed': deductions,
                **old_result,
            },
            'winner': winner,
            'savings_in_winner': round(savings, 2),
            'note': 'Old regime value depends heavily on deductions. This is a point-in-time comparison only.'
        }
    ))


if __name__ == '__main__':
    main()
