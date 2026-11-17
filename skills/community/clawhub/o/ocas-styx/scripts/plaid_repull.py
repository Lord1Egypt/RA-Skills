#!/usr/bin/env python3
"""Re-pull redacted transactions from Plaid and update the database."""

import sqlite3
import sys

sys.path.insert(0, __import__('os').path.dirname(__file__))
from styx_common import plaid_post

_HELP_ARGS = {"--help", "-h"}
if set(sys.argv[1:]) & _HELP_ARGS:
    print((__doc__ or "").strip() or "Usage: python3 plaid_repull.py")
    sys.exit(0)


TXN_DB = '~/.hermes/data/transactions.db'

def main():
    txn_conn = sqlite3.connect(TXN_DB)

    # Get redacted transaction IDs and dates
    redacted = txn_conn.execute('''
        SELECT transaction_id, date, amount
        FROM transactions
        WHERE name LIKE '%*%' AND merchant_name IS NULL
        ORDER BY date DESC
    ''').fetchall()

    print(f"Found {len(redacted)} redacted transactions")

    # Get all access tokens
    tokens = txn_conn.execute('SELECT access_token FROM plaid_items').fetchall()

    # For each token, pull recent transactions
    updates = []
    for (token,) in tokens:
        result = plaid_post('/transactions/get', {
            'access_token': token,
            'start_date': '2026-02-01',
            'end_date': '2026-05-21',
            'options': {'count': 500, 'offset': 0}
        })

        if 'error' in result:
            print(f"Error: {result['error'][:100]}")
            continue

        txns = result.get('transactions', [])
        for t in txns:
            name = t.get('name', '')
            merchant = t.get('merchant_name', '')
            txn_id = t['transaction_id']

            # Check if this transaction ID is in our redacted list
            for red_id, red_date, red_amount in redacted:
                if txn_id == red_id:
                    # Check if the new data is better
                    if name and name != '***************' and name != '**************':
                        print(f"  FOUND: {red_date} ${red_amount} → {name} (merchant: {merchant})")
                        updates.append((txn_id, name, merchant, red_date, red_amount))
                    else:
                        print(f"  STILL REDACTED: {red_date} ${red_amount} (name: '{name}', merchant: '{merchant}')")

    if updates:
        print(f"\nUpdating {len(updates)} transactions...")
        for txn_id, name, merchant, date, amount in updates:
            txn_conn.execute(
                'UPDATE transactions SET name = ?, merchant_name = ? WHERE transaction_id = ?',
                (name, merchant, txn_id)
            )
        txn_conn.commit()
        print("Done!")
    else:
        print("\nNo new data available from Plaid for redacted transactions.")

    # Show remaining redacted
    remaining = txn_conn.execute('''
        SELECT date, amount, name FROM transactions
        WHERE name LIKE '%*%' AND merchant_name IS NULL
        ORDER BY date DESC
    ''').fetchall()

    if remaining:
        print(f"\n{len(remaining)} still redacted:")
        for date, amount, name in remaining:
            print(f"  {date}  ${amount:>8.2f}  {name}")

    txn_conn.close()

if __name__ == '__main__':
    main()