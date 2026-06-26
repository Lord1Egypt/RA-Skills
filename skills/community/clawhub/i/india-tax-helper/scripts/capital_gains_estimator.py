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
        dump(blocked(str(e), ['verified capital gains rules JSON']))
        return

    fy = data.get('fy')
    asset_type = data.get('asset_type')
    gain = data.get('gain')
    holding_days = data.get('holding_days')
    if not fy or not asset_type:
        dump(blocked('Missing FY or asset_type', ['fy', 'asset_type']))
        return
    if gain is None:
        dump(blocked('Missing gain/loss amount', ['gain']))
        return

    rule = rules.get('capital_gains', {}).get(fy, {}).get(asset_type)
    if not rule:
        dump(blocked(f'No verified capital-gains rule for FY={fy}, asset_type={asset_type}', ['matching rules entry']))
        return

    assumptions = []
    if holding_days is None:
        assumptions.append('Holding period missing; classification may only be indicative')
        holding_days = 0

    gain = float(gain)
    holding_days = int(holding_days)
    long_term = holding_days >= int(rule['long_term_days'])
    rate = float(rule['lt_rate'] if long_term else rule['st_rate'])
    taxable = max(0.0, gain)
    tax = round(taxable * rate, 2)

    dump(estimate_payload(
        'capital_gains',
        data,
        assumptions,
        {
            'classification': 'long_term' if long_term else 'short_term',
            'applied_rate': rate,
            'taxable_gain_used': taxable,
            'estimated_tax': tax,
        },
    ))


if __name__ == '__main__':
    main()
