#!/usr/bin/env python3
"""Pull full transaction history for all connected Plaid items."""

import sqlite3
import sys
import time
from datetime import datetime, timedelta

sys.path.insert(0, __import__('os').path.dirname(__file__))
from styx_common import plaid_post, store_transaction

_HELP_ARGS = {"--help", "-h"}
if set(sys.argv[1:]) & _HELP_ARGS:
    print((__doc__ or "").strip() or "Usage: python3 plaid_history.py")
    sys.exit(0)

DB_PATH = '~/.hermes/data/transactions.db'

def pull_transactions(access_token, account_ids, start_date, end_date):
    """Pull all transactions for given accounts using pagination."""
    all_transactions = []
    offset = 0
    page_size = 500  # Plaid max

    while True:
        result = plaid_post('/transactions/get', {
            'access_token': access_token,
            'start_date': start_date,
            'end_date': end_date,
            'options': {
                'account_ids': account_ids,
                'count': page_size,
                'offset': offset,
            }
        })

        if 'error' in result:
            print(f"  ERROR: {result['error']}", file=sys.stderr)
            return all_transactions

        txs = result.get('transactions', [])
        all_transactions.extend(txs)

        total = result.get('total_transactions', 0)
        offset += len(txs)
        print(f"  Fetched {offset}/{total} transactions...")

        if offset >= total or not txs:
            break

        time.sleep(0.5)  # Rate limit courtesy

    return all_transactions

def store_transactions(conn, transactions):
    """Store transactions in DB, skipping duplicates."""
    inserted = 0
    skipped = 0
    for tx in transactions:
        if store_transaction(conn, tx, tx.get('account_id')):
            inserted += 1
        else:
            skipped += 1
    conn.commit()
    return inserted, skipped

def main():
    conn = sqlite3.connect(DB_PATH)

    # Get all items with their access tokens and accounts
    items = conn.execute(
        'SELECT id, access_token, institution_name FROM plaid_items'
    ).fetchall()

    # Date range: last 24 months
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=730)).strftime('%Y-%m-%d')

    print(f"Pulling transactions from {start_date} to {end_date}")
    print(f"{'='*60}")

    grand_total = 0

    for item_id, access_token, inst_name in items:
        # Get accounts for this item
        accounts = conn.execute(
            'SELECT account_id, name, type FROM accounts WHERE plaid_item_id = ?',
            (item_id,)
        ).fetchall()

        if not accounts:
            print(f"\n{inst_name}: No accounts found, skipping")
            continue

        account_ids = [a[0] for a in accounts]
        acct_names = ', '.join(f"{a[1]} ({a[2]})" for a in accounts)
        print(f"\n{inst_name} — {acct_names}")

        txs = pull_transactions(access_token, account_ids, start_date, end_date)

        if txs:
            inserted, skipped = store_transactions(conn, txs)
            print(f"  Stored: {inserted} new, {skipped} duplicates")
            grand_total += inserted
        else:
            print("  No transactions returned")

    print(f"\n{'='*60}")
    print(f"Total new transactions stored: {grand_total}")

    # Summary
    print(f"\n{'='*60}")
    print("Transaction counts by institution:")
    rows = conn.execute('''
        SELECT p.institution_name, COUNT(t.id) as cnt
        FROM transactions t
        JOIN accounts a ON t.account_id = a.account_id
        JOIN plaid_items p ON a.plaid_item_id = p.id
        GROUP BY p.institution_name
        ORDER BY cnt DESC
    ''').fetchall()
    for name, cnt in rows:
        print(f"  {name}: {cnt}")

    total = conn.execute('SELECT COUNT(*) FROM transactions').fetchone()[0]
    print(f"\n  TOTAL: {total} transactions in database")

    conn.close()

if __name__ == '__main__':
    main()