#!/usr/bin/env python3
"""Seed the Styx merchants table from known-clean transaction data.

This bootstraps the enrichment pipeline by:
1. Extracting all unique merchant_name values from transactions
2. Creating merchant records for each unique name
3. Linking transactions that already have clean merchant_names

Run this before the main enrichment pipeline.
"""

import os
import sqlite3
import sys

sys.path.insert(0, __import__('os').path.dirname(__file__))
from styx_common import CATEGORY_MAP, init_styx_db, normalize

_HELP_ARGS = {"--help", "-h"}
if set(sys.argv[1:]) & _HELP_ARGS:
    print((__doc__ or "").strip() or "Usage: python3 seed.py")
    sys.exit(0)


STYX_DB = os.path.expanduser('~/.hermes/data/styx.db')
TXN_DB = os.path.expanduser('~/.hermes/data/transactions.db')

def main():
    styx_conn = init_styx_db(STYX_DB)
    txn_conn = sqlite3.connect(TXN_DB)

    # Get all transactions with their merchant_name and personal_finance_category
    rows = txn_conn.execute('''
        SELECT transaction_id, name, merchant_name, personal_finance_category, amount, date
        FROM transactions
        ORDER BY date DESC
    ''').fetchall()

    # Phase 1: Create merchants from clean merchant_name values
    merchants_created = 0
    merchants_skipped = 0

    # Collect unique merchant names
    unique_merchants = {}
    for txn_id, name, merchant_name, pfc, amount, date in rows:
        if merchant_name and merchant_name.strip() and merchant_name != 'None':
            clean = merchant_name.strip()
            norm = normalize(clean)
            if norm and norm not in unique_merchants:
                cat = CATEGORY_MAP.get(pfc, 'other')
                unique_merchants[norm] = (clean, cat)

    print(f"Found {len(unique_merchants)} unique merchant names")

    for norm, (name, cat) in unique_merchants.items():
        try:
            styx_conn.execute(
                'INSERT OR IGNORE INTO merchants (name, normalized_name, category, source, confidence) VALUES (?, ?, ?, ?, ?)',
                (name, norm, cat, 'plaid_merchant_name', 1.0)
            )
            if styx_conn.total_changes:
                merchants_created += 1
            else:
                merchants_skipped += 1
        except Exception as e:
            print(f"  Error creating merchant '{name}': {e}")
            merchants_skipped += 1

    styx_conn.commit()
    print(f"Merchants created: {merchants_created}, skipped (duplicates): {merchants_skipped}")

    # Phase 2: Link transactions that have clean merchant_names
    links_created = 0
    for txn_id, name, merchant_name, pfc, amount, date in rows:
        if not merchant_name or not merchant_name.strip() or merchant_name == 'None':
            continue
        norm = normalize(merchant_name.strip())
        row = styx_conn.execute(
            'SELECT id FROM merchants WHERE normalized_name = ?', (norm,)
        ).fetchone()
        if row:
            try:
                styx_conn.execute(
                    '''INSERT OR IGNORE INTO transaction_merchants
                    (transaction_id, merchant_id, raw_name, match_method, confidence, is_primary)
                    VALUES (?, ?, ?, ?, ?, 1)''',
                    (txn_id, row[0], name or merchant_name, 'exact', 1.0)
                )
                links_created += 1
            except Exception:
                pass

    styx_conn.commit()
    print(f"Transaction-merchant links created: {links_created}")

    # Summary
    total_merchants = styx_conn.execute('SELECT COUNT(*) FROM merchants').fetchone()[0]
    total_links = styx_conn.execute('SELECT COUNT(*) FROM transaction_merchants').fetchone()[0]
    total_txns = txn_conn.execute('SELECT COUNT(*) FROM transactions').fetchone()[0]
    unlinked = total_txns - total_links

    print(f"\n{'='*60}")
    print("Seeding complete:")
    print(f"  Total transactions: {total_txns}")
    print(f"  Merchants: {total_merchants}")
    print(f"  Linked: {total_links}")
    print(f"  Unlinked (need enrichment): {unlinked}")

    # Show unlinked count by category
    print("\nUnlinked transactions by category:")
    styx_conn.execute(f'ATTACH DATABASE "{TXN_DB}" AS txndb')
    rows = styx_conn.execute('''
        SELECT t.personal_finance_category, COUNT(*) as cnt
        FROM txndb.transactions t
        LEFT JOIN transaction_merchants tm ON t.transaction_id = tm.transaction_id
        WHERE tm.id IS NULL
        GROUP BY t.personal_finance_category
        ORDER BY cnt DESC
    ''').fetchall()
    for cat, cnt in rows:
        print(f"  {cat or 'Unknown'}: {cnt}")

    styx_conn.close()
    txn_conn.close()

if __name__ == '__main__':
    main()