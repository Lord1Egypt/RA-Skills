#!/usr/bin/env python3
"""Render a concise status report from data/positions.json."""

import argparse, json
from datetime import datetime, timezone
from pathlib import Path


def load_positions(path):
    p = Path(path)
    if not p.exists():
        return []
    with open(p) as f:
        return json.load(f)


def main():
    p = argparse.ArgumentParser(description='Report Pendle PT position status')
    p.add_argument('--positions-file', default='data/positions.json')
    args = p.parse_args()

    positions = load_positions(args.positions_file)
    active = [x for x in positions if x.get('status') == 'active']

    print('Pendle PT Status')
    print('================')
    print(f'Checked at: {datetime.now(timezone.utc).isoformat()}')
    print(f'Active positions: {len(active)}')
    print()

    if not active:
        print('No active positions.')
        return

    total_deployed = 0.0
    total_expected_yield = 0.0
    for pos in active:
        deposit = float(pos.get('deposit_amount_usd', 0) or 0)
        expected = float(pos.get('expected_value_at_maturity_usd', deposit) or deposit)
        total_deployed += deposit
        total_expected_yield += (expected - deposit)
        print(f"- {pos.get('market_name', pos.get('market_address', '?'))} ({pos.get('chain', '?')})")
        print(f"  deposited: ${deposit:,.2f}")
        print(f"  apy: {float(pos.get('effective_apy_at_entry', 0) or 0)*100:.2f}%")
        print(f"  maturity: {pos.get('maturity_date', '?')}")
        print(f"  expected at maturity: ${expected:,.2f}")
        print()

    print('Aggregate')
    print(f'- deployed: ${total_deployed:,.2f}')
    print(f'- expected yield: ${total_expected_yield:,.2f}')


if __name__ == '__main__':
    main()
