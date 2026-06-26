#!/usr/bin/env python3
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
        dump(blocked(str(e), ['verified FD/RD rules JSON']))
        return

    fy = data.get('fy')
    rule = rules.get('fd_rd', {}).get(fy)
    if not fy or not rule:
        dump(blocked(f'No verified FD/RD rules for FY={fy}', ['matching rules entry']))
        return

    interest = data.get('interest_income')
    estimated_total_income = data.get('estimated_total_income')
    age_category = data.get('age_category')
    if interest is None:
        dump(blocked('Missing interest income', ['interest_income']))
        return

    assumptions = []
    if estimated_total_income is None:
        assumptions.append('Estimated total income missing; 15G/15H style guidance is only indicative')
    if age_category is None:
        assumptions.append('Age category missing; senior/non-senior threshold handling may differ')

    interest = float(interest)
    estimated_total_income = float(estimated_total_income or 0)
    regime = data.get('regime')
    tds_threshold_raw = rule.get('tds_threshold_senior') if age_category == 'senior' else rule.get('tds_threshold')
    tds_threshold = float(tds_threshold_raw or rule['tds_threshold'])
    tds_rate = float(rule['tds_rate'])
    likely_tds = interest > tds_threshold

    likely_15g15h_possible = None
    if estimated_total_income and regime:
        cutoff = rule.get('nil_tax_income_cutoff', {}).get(regime + '_regime')
        if cutoff and not isinstance(cutoff, dict):
            likely_15g15h_possible = estimated_total_income <= float(cutoff)
        elif not cutoff:
            assumptions.append('Nil-tax cutoff missing for regime; 15G/15H indicator unavailable')
    elif not regime:
        assumptions.append('Tax regime missing; 15G/15H eligibility cannot be determined')

    tds_amount = round(interest * tds_rate, 2) if likely_tds else 0.0

    dump(estimate_payload(
        'fd_rd_tds',
        data,
        assumptions,
        {
            'interest_income': interest,
            'likely_tds_threshold_crossed': likely_tds,
            'indicative_tds_amount': tds_amount,
            'likely_15g_15h_eligibility_indicator': likely_15g15h_possible,
            'note': 'This is an indicator only; actual form eligibility depends on verified FY rules and user facts.',
        },
    ))


if __name__ == '__main__':
    main()
