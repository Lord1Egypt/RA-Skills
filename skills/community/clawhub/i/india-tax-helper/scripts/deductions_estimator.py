#!/usr/bin/env python3
"""
Estimates deductions under Chapter VIA for old regime.
New regime has very limited deductions (80CCD(2), 80CCH, standard deduction).
"""
import argparse
from common import load_json, load_rules, blocked, estimate_payload, dump, RulesError


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

    regime = data.get('regime')
    if not regime:
        dump(blocked('Missing regime', ['regime']))
        return

    if regime == 'new':
        # New regime: very limited deductions
        employer_nps = float(data.get('employer_nps_80ccd2', 0))
        agnipath = float(data.get('agnipath_80cch', 0))
        std_ded = rules.get('standard_deduction', {}).get('new_regime', 75000)
        total = std_ded + employer_nps + agnipath
        dump(estimate_payload(
            'deductions',
            data,
            ['New regime: only 80CCD(2), 80CCH, and standard deduction considered'],
            {
                'standard_deduction': std_ded,
                'employer_nps_80ccd2': employer_nps,
                'agnipath_80cch': agnipath,
                'total_deductions': round(total, 2),
                'note': 'Old regime deductions (80C, 80D, etc.) are NOT available in new regime.'
            }
        ))
        return

    # Old regime: full Chapter VIA
    s80c = min(float(data.get('80c', 0)), 150000)
    s80ccc = min(float(data.get('80ccc', 0)), 150000)
    s80ccd1 = min(float(data.get('80ccd1', 0)), 150000)
    s80ccd1b = min(float(data.get('80ccd1b', 0)), 50000)
    employer_nps = float(data.get('employer_nps_80ccd2', 0))
    # 80CCD(2) limits: 10% for PSU/others, 14% for Central/State Govt
    employer_type = data.get('employer_type', 'other')
    nps_limit_pct = 0.14 if employer_type in ['central_govt', 'state_govt'] else 0.10
    salary_for_nps = float(data.get('salary_basic_da', data.get('gross_salary', 0)))
    max_80ccd2 = salary_for_nps * nps_limit_pct
    s80ccd2 = min(employer_nps, max_80ccd2)

    s80d_self = min(float(data.get('80d_self', 0)), 25000)
    if data.get('80d_self_senior'):
        s80d_self = min(float(data.get('80d_self', 0)), 50000)
    s80d_parents = min(float(data.get('80d_parents', 0)), 25000)
    if data.get('80d_parents_senior'):
        s80d_parents = min(float(data.get('80d_parents', 0)), 50000)
    s80d_preventive = min(float(data.get('80d_preventive', 0)), 5000)
    # Preventive included in overall 80D limits
    total_80d = min(s80d_self + s80d_parents, 75000 if (data.get('80d_self_senior') or data.get('80d_parents_senior')) else 50000)

    s80e = float(data.get('80e_education_loan_interest', 0))
    s80eea = min(float(data.get('80eea_home_loan_interest_first_time', 0)), 150000)
    s80eeb = min(float(data.get('80eeb_ev_loan_interest', 0)), 150000)
    s24b = min(float(data.get('24b_home_loan_interest_self_occupied', 0)), 200000)

    s80gg = 0.0
    if data.get('80gg_rent'):
        rent = float(data.get('80gg_rent', 0))
        income_before_80gg = float(data.get('income_before_80gg', 0))
        s80gg = min(rent - 0.10 * income_before_80gg, 60000, 0.25 * income_before_80gg)
        s80gg = max(0.0, s80gg)

    s80tta = min(float(data.get('80tta_savings_interest', 0)), 10000)
    s80ttb = min(float(data.get('80ttb_senior_deposit_interest', 0)), 50000) if data.get('age', 0) >= 60 else 0

    s80u = 75000 if data.get('80u_disability') else 0
    if data.get('80u_severe_disability'):
        s80u = 125000

    s80dd = 75000 if data.get('80dd_disabled_dependent') else 0
    if data.get('80dd_severe'):
        s80dd = 125000

    s80ddb = min(float(data.get('80ddb_medical_specified_disease', 0)), 100000 if data.get('age', 0) >= 60 else 40000)

    # 80C + 80CCC + 80CCD(1) combined limit
    combined_80c_ccc_ccd1 = min(s80c + s80ccc + s80ccd1, 150000)

    total = (
        combined_80c_ccc_ccd1 +
        s80ccd1b +
        s80ccd2 +
        total_80d +
        s80e +
        s80eea +
        s80eeb +
        s24b +
        s80gg +
        s80tta +
        s80ttb +
        s80u +
        s80dd +
        s80ddb +
        float(data.get('80g_donations', 0))
    )

    dump(estimate_payload(
        'deductions',
        data,
        [],
        {
            'regime': 'old',
            '80c_ccc_ccd1_combined': round(combined_80c_ccc_ccd1, 2),
            '80ccd1b': round(s80ccd1b, 2),
            '80ccd2_employer_nps': round(s80ccd2, 2),
            '80d_total': round(total_80d, 2),
            '80e_education_loan': round(s80e, 2),
            '80eea_home_loan': round(s80eea, 2),
            '80eeb_ev_loan': round(s80eeb, 2),
            '24b_home_loan_interest': round(s24b, 2),
            '80gg_rent': round(s80gg, 2),
            '80tta_savings': round(s80tta, 2),
            '80ttb_senior': round(s80ttb, 2),
            '80u_disability': round(s80u, 2),
            '80dd_dependent': round(s80dd, 2),
            '80ddb_medical': round(s80ddb, 2),
            'total_deductions': round(total, 2),
            'standard_deduction': 50000,
        }
    ))


if __name__ == '__main__':
    main()
