#!/usr/bin/env python3
"""Offline rental cost comparison. Original A3 application arithmetic, packaged
by OpenAI Codex GPT-6 for standalone skill use. No network or account access.
"""
import argparse
import json
from decimal import Decimal, InvalidOperation
from pathlib import Path


def compare(listings, budget=2200):
    result = []
    for item in listings:
        def amount(key):
            raw = item.get(key)
            if raw is None:
                return None
            value = Decimal(str(raw))
            if not value.is_finite() or value < 0:
                raise ValueError('Costs must be finite and nonnegative')
            return value
        rent, fees, deposit = amount('rent'), amount('monthly_fees'), amount('deposit')
        monthly = rent + fees if rent is not None and fees is not None else None
        result.append({**item, 'known_monthly_total': str(monthly) if monthly is not None else None,
                       'known_upfront_deposit': str(deposit) if deposit is not None else None,
                       'within_budget': monthly <= Decimal(str(budget)) if monthly is not None else None,
                       'missing': [k for k in ('rent', 'monthly_fees', 'deposit', 'source_url', 'retrieved_at') if item.get(k) is None]})
    return sorted(result, key=lambda i: (i['known_monthly_total'] is None, Decimal(i['known_monthly_total'] or 'Infinity')))



def main():
    parser = argparse.ArgumentParser(description='Compare monthly rental costs without adding refundable deposits.')
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--budget', default='2200')
    args = parser.parse_args()
    try:
        budget = Decimal(args.budget)
        if not budget.is_finite() or budget < 0:
            raise ValueError('Budget must be finite and nonnegative')
        listings = json.loads(args.input.read_text())
        if not isinstance(listings, list) or any(not isinstance(row, dict) for row in listings):
            raise ValueError('Input must be a JSON array of listing objects')
        result = compare(listings, budget)
    except (ValueError, TypeError, OSError, InvalidOperation) as error:
        parser.error(str(error))
    print(json.dumps({'budget': str(budget), 'ranked_listings': result}, indent=2))

if __name__ == '__main__':
    main()
