#!/usr/bin/env python3
"""Check Pendle positions for maturity / near-maturity and print actionable next steps.

This is the orchestration layer on top of the basic position tracker.
For now it is confirmation-driven: it does not auto-submit transactions by itself.
It prepares the exact next action a user can approve.
"""

import argparse, json
from datetime import datetime, timezone, timedelta
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
POSITIONS_PATH = SKILL_ROOT / 'data' / 'positions.json'


def load_positions():
    if not POSITIONS_PATH.exists():
        return []
    return json.loads(POSITIONS_PATH.read_text())


def main():
    p = argparse.ArgumentParser(description='Pendle auto-roll / maturity monitor')
    p.add_argument('--alert-hours', type=int, default=24)
    args = p.parse_args()

    positions = load_positions()
    active = [x for x in positions if x.get('status') == 'active']
    now = datetime.now(timezone.utc)
    alert_cutoff = now + timedelta(hours=args.alert_hours)

    print('Pendle auto-roll monitor')
    print('========================')
    print(f'Checked at: {now.isoformat()}')
    print(f'Active positions: {len(active)}')
    print()

    if not active:
        print('No active positions.')
        return

    any_alert = False
    for pos in active:
        market = pos.get('market_name', pos.get('market_address', '?'))
        maturity_raw = pos.get('maturity_date')
        if not maturity_raw:
            print(f'- {market}: missing maturity_date in tracker')
            any_alert = True
            continue

        maturity = datetime.fromisoformat(maturity_raw.replace('Z', '+00:00'))
        delta = maturity - now
        days_left = delta.total_seconds() / 86400

        print(f'- {market}')
        print(f'  chain: {pos.get("chain", "?")}')
        print(f'  deposited: ${float(pos.get("deposit_amount_usd", 0) or 0):,.2f}')
        print(f'  maturity: {maturity_raw}')
        print(f'  time left: {days_left:.2f} days')

        if maturity <= now:
            any_alert = True
            print('  status: MATURED')
            print(f'  next action: redeem position {pos.get("id")}')
            print(f'  confirm: Confirm redeem Pendle position {pos.get("id")}')
        elif maturity <= alert_cutoff:
            any_alert = True
            print(f'  status: MATURING WITHIN {args.alert_hours}h')
            print('  next action: prepare redeem preview, then scan for next candidate')
            print(f'  confirm: Confirm preview redeem Pendle position {pos.get("id")}')
        else:
            print('  status: HOLDING')
            print('  next action: none')
        print()

    if not any_alert:
        print('All active positions are healthy and outside the maturity alert window.')


if __name__ == '__main__':
    main()
