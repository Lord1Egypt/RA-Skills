#!/usr/bin/env python3
"""Styx query helper — read-only queries for consumer skills.

Usage:
    python3 query.py --category restaurant --limit 50
    python3 query.py --merchant "Starbucks"
    python3 query.py --unresolved
    python3 query.py --spending-by-merchant
    python3 query.py --summary
"""

import argparse
import json
import sqlite3
import sys

STYX_DB = '~/.hermes/data/styx.db'
TXN_DB = '~/.hermes/data/transactions.db'

def get_conn():
    conn = sqlite3.connect(STYX_DB)
    conn.execute(f'ATTACH DATABASE "{TXN_DB}" AS txndb')
    conn.row_factory = sqlite3.Row
    return conn

def query_by_category(category, limit=50, since=None):
    """Get enriched transactions for a merchant category."""
    conn = get_conn()
    query = '''
        SELECT t.transaction_id, t.name as raw_name, t.amount, t.date,
               t.personal_finance_category,
               m.name as merchant_name, m.category as merchant_category,
               m.city, m.state,
               tm.confidence, tm.match_method
        FROM transaction_merchants tm
        JOIN merchants m ON tm.merchant_id = m.id
        JOIN txndb.transactions t ON tm.transaction_id = t.transaction_id
        WHERE m.category = ?
    '''
    params = [category]
    if since:
        query += ' AND t.date >= ?'
        params.append(since)
    query += ' ORDER BY t.date DESC LIMIT ?'
    params.append(limit)
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def query_by_merchant(name):
    """Get all transactions for a specific merchant."""
    conn = get_conn()
    rows = conn.execute('''
        SELECT t.transaction_id, t.name as raw_name, t.amount, t.date,
               t.personal_finance_category,
               m.name as merchant_name, m.category as merchant_category,
               tm.confidence, tm.match_method
        FROM transaction_merchants tm
        JOIN merchants m ON tm.merchant_id = m.id
        JOIN txndb.transactions t ON tm.transaction_id = t.transaction_id
        WHERE m.normalized_name LIKE ?
        ORDER BY t.date DESC
    ''', (f'%{name.lower()}%',)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def query_unresolved(limit=100):
    """Get transactions that haven't been enriched yet."""
    conn = get_conn()
    rows = conn.execute('''
        SELECT t.transaction_id, t.name, t.merchant_name, t.amount, t.date,
               t.personal_finance_category, t.category
        FROM txndb.transactions t
        LEFT JOIN transaction_merchants tm ON t.transaction_id = tm.transaction_id
        WHERE tm.id IS NULL
        ORDER BY t.date DESC
        LIMIT ?
    ''', (limit,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def spending_by_merchant(limit=30):
    """Get total spending per merchant."""
    conn = get_conn()
    rows = conn.execute('''
        SELECT m.name, m.category, m.city,
               SUM(t.amount) as total_spent,
               COUNT(*) as transaction_count,
               MIN(t.date) as first_seen,
               MAX(t.date) as last_seen,
               AVG(tm.confidence) as avg_confidence
        FROM transaction_merchants tm
        JOIN merchants m ON tm.merchant_id = m.id
        JOIN txndb.transactions t ON tm.transaction_id = t.transaction_id
        WHERE tm.is_primary = 1
          AND t.amount > 0
        GROUP BY m.id
        ORDER BY total_spent DESC
        LIMIT ?
    ''', (limit,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def summary():
    """Get enrichment summary stats."""
    conn = get_conn()
    stats = {}

    stats['total_transactions'] = conn.execute(
        'SELECT COUNT(*) FROM txndb.transactions'
    ).fetchone()[0]

    stats['enriched_transactions'] = conn.execute(
        'SELECT COUNT(DISTINCT transaction_id) FROM transaction_merchants'
    ).fetchone()[0]

    stats['total_merchants'] = conn.execute(
        'SELECT COUNT(*) FROM merchants'
    ).fetchone()[0]

    stats['match_methods'] = dict(conn.execute('''
        SELECT match_method, COUNT(*) as cnt
        FROM transaction_merchants
        GROUP BY match_method
        ORDER BY cnt DESC
    ''').fetchall())

    stats['categories'] = dict(conn.execute('''
        SELECT m.category, COUNT(DISTINCT tm.transaction_id) as cnt
        FROM transaction_merchants tm
        JOIN merchants m ON tm.merchant_id = m.id
        GROUP BY m.category
        ORDER BY cnt DESC
    ''').fetchall())

    stats['avg_confidence'] = conn.execute(
        'SELECT AVG(confidence) FROM transaction_merchants'
    ).fetchone()[0]

    # Recent enrichment runs
    stats['recent_runs'] = [dict(r) for r in conn.execute('''
        SELECT * FROM enrichment_runs ORDER BY id DESC LIMIT 5
    ''').fetchall()]

    conn.close()
    return stats

def main():
    parser = argparse.ArgumentParser(description='Styx query helper')
    parser.add_argument('--category', help='Filter by merchant category')
    parser.add_argument('--merchant', help='Filter by merchant name (fuzzy)')
    parser.add_argument('--unresolved', action='store_true', help='Show unresolved transactions')
    parser.add_argument('--spending-by-merchant', action='store_true', help='Spending summary by merchant')
    parser.add_argument('--summary', action='store_true', help='Enrichment summary stats')
    parser.add_argument('--since', help='Start date (YYYY-MM-DD)')
    parser.add_argument('--limit', type=int, default=50, help='Result limit')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    args = parser.parse_args()

    if args.summary:
        result = summary()
    elif args.unresolved:
        result = query_unresolved(args.limit)
    elif args.spending_by_merchant:
        result = spending_by_merchant(args.limit)
    elif args.merchant:
        result = query_by_merchant(args.merchant)
    elif args.category:
        result = query_by_category(args.category, args.limit, args.since)
    else:
        parser.print_help()
        sys.exit(1)

    if args.json:
        print(json.dumps(result, indent=2, default=str))
    else:
        if isinstance(result, dict):
            for k, v in result.items():
                if k == 'recent_runs':
                    print(f"\n{k}:")
                    for run in v:
                        print(f"  {run}")
                elif isinstance(v, dict):
                    print(f"\n{k}:")
                    for kk, vv in v.items():
                        print(f"  {kk}: {vv}")
                else:
                    print(f"{k}: {v}")
        elif isinstance(result, list):
            for row in result:
                print(json.dumps(row, default=str))

if __name__ == '__main__':
    main()