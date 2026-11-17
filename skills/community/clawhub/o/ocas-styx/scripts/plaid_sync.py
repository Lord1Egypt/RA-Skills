#!/usr/bin/env python3
"""Incremental transaction sync using Plaid's /transactions/sync endpoint.

Uses cursor-based sync for efficient incremental updates.
Run daily via cron.
"""

import sqlite3
import sys
import time

sys.path.insert(0, __import__('os').path.dirname(__file__))
from styx_common import plaid_post, store_transaction

_HELP_ARGS = {"--help", "-h"}
if set(sys.argv[1:]) & _HELP_ARGS:
    print((__doc__ or "").strip() or "Usage: python3 plaid_sync.py")
    sys.exit(0)


DB_PATH = '~/.hermes/data/transactions.db'

def sync_item(conn, item_id, access_token, institution_name):
    """Sync transactions for a single item using cursor-based pagination."""
    # Get stored cursor
    cursor_row = conn.execute(
        'SELECT cursor FROM sync_cursor WHERE item_id = ?', (item_id,)
    ).fetchone()
    cursor = cursor_row[0] if cursor_row else None

    # Get account IDs for this item
    accounts = conn.execute(
        'SELECT account_id FROM accounts WHERE plaid_item_id = ?', (item_id,)
    ).fetchall()
    account_map = {a[0]: True for a in accounts}

    added = 0
    modified = 0
    removed = 0
    has_more = True

    while has_more:
        payload = {'access_token': access_token}
        if cursor:
            payload['cursor'] = cursor

        result = plaid_post('/transactions/sync', payload)

        if 'error' in result:
            print(f"  {institution_name} ERROR: {result['error']}", file=sys.stderr)
            return added, modified, removed

        # Process added
        for tx in result.get('added', []):
            if tx.get('account_id') in account_map:
                if store_transaction(conn, tx, tx['account_id']):
                    added += 1

        # Process modified
        for tx in result.get('modified', []):
            if tx.get('account_id') in account_map:
                if store_transaction(conn, tx, tx['account_id']):
                    modified += 1

        # Process removed
        for tx in result.get('removed', []):
            tx_id = tx.get('transaction_id')
            if tx_id:
                conn.execute('DELETE FROM transactions WHERE transaction_id = ?', (tx_id,))
                removed += 1

        cursor = result.get('next_cursor')
        has_more = result.get('has_more', False)

        # Update cursor after each page
        conn.execute(
            'INSERT OR REPLACE INTO sync_cursor (item_id, cursor, updated_at) VALUES (?, ?, datetime("now"))',
            (item_id, cursor)
        )
        conn.commit()

        if has_more:
            time.sleep(0.3)

    return added, modified, removed

def main():
    conn = sqlite3.connect(DB_PATH)

    items = conn.execute(
        'SELECT id, access_token, item_id, institution_name FROM plaid_items'
    ).fetchall()

    total_added = 0
    total_modified = 0
    total_removed = 0

    print(f"Incremental sync started at {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}")

    for item_id, access_token, plaid_item_id, inst_name in items:
        print(f"\n{inst_name}...")
        try:
            added, modified, removed = sync_item(conn, plaid_item_id, access_token, inst_name)
            print(f"  +{added} added, ~{modified} modified, -{removed} removed")
            total_added += added
            total_modified += modified
            total_removed += removed
        except Exception as e:
            print(f"  FAILED: {e}", file=sys.stderr)

    print(f"\n{'='*60}")
    print(f"Sync complete: +{total_added} added, ~{total_modified} modified, -{total_removed} removed")

    # Update account balances
    print("\nUpdating balances...")
    for item_id, access_token, plaid_item_id, inst_name in items:
        result = plaid_post('/accounts/balance/get', {'access_token': access_token})
        if 'accounts' in result:
            for acct in result['accounts']:
                conn.execute(
                    '''UPDATE accounts SET
                        current_balance = ?,
                        available_balance = ?
                    WHERE account_id = ?''',
                    (acct.get('balances', {}).get('current'),
                     acct.get('balances', {}).get('available'),
                     acct['account_id'])
                )
    conn.commit()

    total_tx = conn.execute('SELECT COUNT(*) FROM transactions').fetchone()[0]
    print(f"Total transactions in DB: {total_tx}")

    conn.close()

if __name__ == '__main__':
    main()