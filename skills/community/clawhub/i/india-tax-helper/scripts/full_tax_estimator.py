#!/usr/bin/env python3
"""
End-to-end tax estimator for resident salaried individuals.
Combines salary, deductions, FD/RD interest, and capital gains.
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
    regime = data.get('regime')
    age = data.get('age', 30)
    if not regime:
        dump(blocked('Missing regime', ['regime']))
        return

    fy_rules = rules.get('salary_regimes', {}).get(fy)
    if not fy_rules:
        dump(blocked(f'No verified salary rules for FY={fy}', ['matching rules entry']))
        return

    regime_rules = fy_rules.get(regime)
    if not regime_rules:
        dump(blocked(f'No verified salary rules for FY={fy}, regime={regime}', ['matching rules entry']))
        return

    # Select slabs
    if regime == 'old':
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
    tds_salary = float(data.get('tds_salary', 0))
    deductions = float(data.get('deductions', 0))
    std_ded = float(regime_rules.get('standard_deduction', 0))

    # FD/RD interest
    fd_interest = float(data.get('fd_interest', 0))
    fd_tds = float(data.get('fd_tds', 0))

    # Capital gains
    stcg = float(data.get('stcg', 0))
    ltcg = float(data.get('ltcg', 0))
    cg_type = data.get('capital_gains_type', 'equity_stt_paid')

    assumptions = []
    if not gross_salary:
        assumptions.append('Gross salary missing or zero')
    if not data.get('tds_salary'):
        assumptions.append('TDS on salary missing; refund/payable will be incomplete')

    # Salary tax
    taxable_salary = max(0.0, gross_salary - deductions - std_ded)
    salary_base_tax = compute_tax_from_slabs(taxable_salary, slabs)

    # Rebate 87A on salary tax only (simplified; technically on total tax)
    rebate = 0.0
    rebate_rule = regime_rules.get('rebate_87a')
    total_income_for_rebate = taxable_salary + other_income + fd_interest
    if rebate_rule and total_income_for_rebate <= rebate_rule['taxable_income_limit']:
        rebate = min(salary_base_tax, rebate_rule['max_rebate'])

    post_rebate = max(0.0, salary_base_tax - rebate)

    # Surcharge (simplified: on total income)
    total_income = taxable_salary + other_income + fd_interest + stcg + max(0.0, ltcg - 125000)
    surcharge = 0.0
    if 'surcharge' in rules:
        key = 'new_regime' if regime == 'new' else 'old_regime'
        surcharge = compute_surcharge(total_income, post_rebate, rules['surcharge'][key])

    # Cess
    cess_rate = rules.get('cess', {}).get('health_and_education', 0.0)
    cess = round((post_rebate + surcharge) * cess_rate, 2)
    total_salary_tax = round(post_rebate + surcharge + cess, 2)

    # Other income tax (at slab rates for old regime; slab rates for new regime too)
    other_tax = 0.0
    if other_income > 0:
        other_tax = compute_tax_from_slabs(other_income, slabs)

    # FD interest: taxed at slab rate (no special rate)
    fd_tax = 0.0
    if fd_interest > 0:
        fd_tax = compute_tax_from_slabs(fd_interest, slabs)

    # Capital gains
    cg_tax = 0.0
    cg_rules = rules.get('capital_gains', {}).get(fy, {}).get(cg_type)
    if cg_rules:
        if stcg > 0:
            st_rate = cg_rules.get('st_rate', 'slab')
            if st_rate == 'slab':
                cg_tax += compute_tax_from_slabs(stcg, slabs)
            else:
                cg_tax += round(stcg * float(st_rate), 2)
        if ltcg > 0:
            lt_exemption = cg_rules.get('lt_exemption_limit', 0)
            taxable_ltcg = max(0.0, ltcg - lt_exemption)
            lt_rate = cg_rules.get('lt_rate', 'slab')
            if lt_rate == 'slab':
                cg_tax += compute_tax_from_slabs(taxable_ltcg, slabs)
            else:
                cg_tax += round(taxable_ltcg * float(lt_rate), 2)
    else:
        assumptions.append(f'No verified capital gains rules for {cg_type}; CG tax omitted')

    total_tax = round(total_salary_tax + other_tax + fd_tax + cg_tax, 2)
    total_tds = round(tds_salary + fd_tds, 2)
    refund_or_payable = round(total_tds - total_tax, 2)

    dump(estimate_payload(
        'full_tax_estimate',
        data,
        assumptions,
        {
            'fy': fy,
            'regime': regime,
            'age': age,
            'components': {
                'salary': {
                    'gross': gross_salary,
                    'deductions': deductions,
                    'standard_deduction': std_ded,
                    'taxable': round(taxable_salary, 2),
                    'base_tax': salary_base_tax,
                    'rebate_87a': round(rebate, 2),
                    'post_rebate': round(post_rebate, 2),
                    'surcharge': round(surcharge, 2),
                    'cess': cess,
                    'total_salary_tax': total_salary_tax,
                },
                'other_income': {
                    'amount': other_income,
                    'tax_at_slab': other_tax,
                },
                'fd_interest': {
                    'amount': fd_interest,
                    'tds_deducted': fd_tds,
                    'tax_at_slab': fd_tax,
                },
                'capital_gains': {
                    'stcg': stcg,
                    'ltcg': ltcg,
                    'type': cg_type,
                    'tax': cg_tax,
                },
            },
            'summary': {
                'total_tax_liability': total_tax,
                'total_tds_paid': total_tds,
                'refund_if_positive_else_additional_tax': refund_or_payable,
            }
        }
    ))


if __name__ == '__main__':
    main()
