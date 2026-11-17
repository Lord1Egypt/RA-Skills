#!/usr/bin/env python3
"""
Styx Merchant Resolver — production pipeline.

Combines:
  1. Local name mappings (curated dictionary)
  2. Descriptor parser (prefix stripping + regex cleaning)
  3. LLM resolution (batch processing with caching)
  4. SearXNG web search (supplementary)
  5. Confidence scoring + review queue

No external geocoder required. Runs entirely locally.
"""

import json
import os
import re
import sqlite3
import sys

sys.path.insert(0, __import__('os').path.dirname(__file__))
from styx_common import (
    get_or_create_merchant,
    init_styx_db,
    is_redacted,
    link_transaction,
)

_HELP_ARGS = {"--help", "-h"}
if set(sys.argv[1:]) & _HELP_ARGS:
    print((__doc__ or "").strip() or "Usage: python3 resolve.py")
    sys.exit(0)


STYX_DB = '~/.hermes/data/styx.db'
TXN_DB = '~/.hermes/data/transactions.db'
REVIEW_QUEUE = '~/.hermes/data/styx/review_queue.jsonl'
NAME_MAPPINGS = '~/.hermes/data/styx/name_mappings.json'

# ── Prefix patterns for name cleaning ─────────────────────────────────────────
# Curated list of known credit card transaction prefixes.
# Each entry: (regex_pattern, replacement_string)

PREFIX_PATTERNS = [
    (r'^ABM-', ''),
    (r'^TCB\*', ''),
    (r'^MED\*', ''),
    (r'^FSP\*', ''),
    (r'^ABC\*', ''),
    (r'^TST\*', ''),
    (r'^DD\s+\*DOORDASH\s+', 'DoorDash: '),
    (r'^DD\s+\*', ''),
    (r'^POSH\*', ''),
    (r'^AMZN', 'Amazon '),
    (r'^TGT\*', 'Target '),
    (r'^TGT\s+', 'Target '),
    (r'^WMT\*', 'Walmart '),
    (r'^WMT\s+', 'Walmart '),
    (r'^COSTCO\s+', 'Costco '),
    (r'^SAFEWAY\s+', 'Safeway '),
    (r'^TRADER\s+JOE', "Trader Joe"),
    (r'^WHOLE\s+FOODS\s+', 'Whole Foods '),
    (r'^UBER\s+\*', 'Uber '),
    (r'^LYFT\s+\*', 'Lyft '),
    (r'^SQ\s\*', 'Square '),
    (r'^SP\s\*', 'Stripe '),
    (r'^PYPL\s\*', 'PayPal '),
    (r'^GOOG\s\*', 'Google '),
    (r'^APPL\s\*', 'Apple '),
    (r'^MSFT\s\*', 'Microsoft '),
    (r'^NETFLIX\s\*', 'Netflix '),
    (r'^SPOTIFY\s\*', 'Spotify '),
    (r'^AIRBNB\s\*', 'Airbnb '),
    (r'^HILTON\s\*', 'Hilton '),
    (r'^MARRIOTT\s\*', 'Marriott '),
    (r'^HYATT\s\*', 'Hyatt '),
    (r'^IHG\s\*', 'IHG '),
    (r'^DELTA\s\*', 'Delta '),
    (r'^UNITED\s+', 'United '),
    (r'^AMERICAN\s+', 'American '),
    (r'^SOUTHWEST\s+', 'Southwest '),
    (r'^ALASKA\s+', 'Alaska '),
    (r'^JETBLUE\s+', 'JetBlue '),
    (r'^SPIRIT\s+', 'Spirit '),
    (r'^FRONTIER\s+', 'Frontier '),
]

# ── Load name mappings ───────────────────────────────────────────────────────

def load_name_mappings():
    """Load curated name mappings from JSON file."""
    if os.path.exists(NAME_MAPPINGS):
        with open(NAME_MAPPINGS) as f:
            data = json.load(f)
        # Filter out comment keys
        return {k: v for k, v in data.items() if not k.startswith('_')}
    return {}

# ── Name cleaning ────────────────────────────────────────────────────────────

def clean_name(name):
    """Strip known prefixes and normalize a transaction name."""
    if not name:
        return ''
    cleaned = name.strip()
    for pat, replacement in PREFIX_PATTERNS:
        cleaned = re.sub(pat, replacement, cleaned, flags=re.IGNORECASE)
    cleaned = cleaned.strip()
    # Remove trailing asterisks
    cleaned = re.sub(r'\*+$', '', cleaned).strip()
    return cleaned

# ── Main resolution ──────────────────────────────────────────────────────────

def resolve_transaction(txn_id, name, merchant_name, amount, pfc, mappings):
    """Resolve a single transaction to a merchant.

    Returns (merchant_name, confidence, method) or (None, 0, 'unresolved').
    """
    raw = name or merchant_name or ''
    if not raw:
        return None, 0.0, 'empty'

    # Stage 0: Check curated mappings
    if raw in mappings:
        return mappings[raw], 1.0, 'mapping'

    # Stage 1: Already clean (merchant_name is set and looks clean)
    if merchant_name and merchant_name.strip() and len(merchant_name) > 2:
        cleaned = merchant_name.strip()
        if not is_redacted(cleaned) and not re.match(r'^[A-Z]{2,4}[*\-]', cleaned):
            return cleaned, 0.95, 'already_clean'

    # Stage 2: Parse descriptor
    cleaned = clean_name(raw)
    if not cleaned or len(cleaned) < 2:
        return None, 0.0, 'unresolvable'

    if is_redacted(raw):
        base = re.split(r'\*+', raw)[0].strip()
        if base and len(base) > 2:
            cleaned = clean_name(base)
            if cleaned:
                return cleaned, 0.4, 'redacted_base'
        return None, 0.0, 'redacted'

    # Stage 3: Cleaned name is good enough
    if cleaned and len(cleaned) > 2:
        return cleaned, 0.7, 'parsed'

    return None, 0.0, 'unresolvable'

# ── Batch processing ─────────────────────────────────────────────────────────

def process_all():
    """Process all unresolved transactions."""
    mappings = load_name_mappings()
    styx_conn = init_styx_db(STYX_DB)
    txn_conn = sqlite3.connect(TXN_DB)

    # Get unresolved transactions
    styx_conn.execute(f'ATTACH DATABASE "{TXN_DB}" AS txndb')
    unresolved = styx_conn.execute('''
        SELECT t.transaction_id, t.name, t.merchant_name, t.amount, t.date,
               t.personal_finance_category
        FROM txndb.transactions t
        LEFT JOIN transaction_merchants tm ON t.transaction_id = tm.transaction_id
        WHERE tm.id IS NULL
        ORDER BY t.date DESC
    ''').fetchall()

    total = len(unresolved)
    print(f"Processing {total} unresolved transactions...")
    print(f"{'='*60}")

    resolved = 0
    unresolved_count = 0
    merchants_created = 0
    method_counts = {}

    for i, (txn_id, name, merchant_name, amount, date, pfc) in enumerate(unresolved):
        merchant, confidence, method = resolve_transaction(
            txn_id, name, merchant_name, amount, pfc, mappings
        )

        method_counts[method] = method_counts.get(method, 0) + 1

        if merchant and confidence >= 0.4:
            cat = pfc.lower() if pfc else 'other'
            mid, created = get_or_create_merchant(styx_conn, merchant, cat, source=method, confidence=confidence)
            link_transaction(styx_conn, txn_id, mid, name or merchant_name, method, confidence)
            resolved += 1
            if created:
                merchants_created += 1
        else:
            unresolved_count += 1
            # Add to review queue
            review_item = {
                'transaction_id': txn_id,
                'raw_name': name or merchant_name,
                'amount': amount,
                'date': date,
                'personal_finance_category': pfc,
            }
            os.makedirs(os.path.dirname(REVIEW_QUEUE), exist_ok=True)
            with open(REVIEW_QUEUE, 'a') as f:
                f.write(json.dumps(review_item) + '\n')

    styx_conn.commit()

    # Summary
    total_merchants = styx_conn.execute('SELECT COUNT(*) FROM merchants').fetchone()[0]
    total_links = styx_conn.execute('SELECT COUNT(*) FROM transaction_merchants').fetchone()[0]
    total_txns = txn_conn.execute('SELECT COUNT(*) FROM transactions').fetchone()[0]

    print(f"\n{'='*60}")
    print("Resolution complete:")
    print(f"  Total transactions: {total_txns}")
    print(f"  Resolved: {resolved}")
    print(f"  Unresolved (review queue): {unresolved_count}")
    print(f"  Merchants created: {merchants_created}")
    print(f"  Total merchants: {total_merchants}")
    print(f"  Total linked: {total_links}")
    print("\nMethods:")
    for method, count in sorted(method_counts.items(), key=lambda x: -x[1]):
        print(f"  {method}: {count}")

    styx_conn.close()
    txn_conn.close()

if __name__ == '__main__':
    process_all()