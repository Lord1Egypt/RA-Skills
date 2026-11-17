#!/usr/bin/env python3
"""Shared utilities for Styx scripts.

Import from any styx script:
    from styx_common import normalize, is_redacted, CATEGORY_MAP,
                           init_styx_db, get_or_create_merchant, link_transaction,
                           load_env, plaid_post, store_transaction
"""

import json
import os
import re
import sqlite3
import sys
import urllib.error
import urllib.request

_HELP_ARGS = {"--help", "-h"}
if set(sys.argv[1:]) & _HELP_ARGS:
    print((__doc__ or "").strip() or "Usage: python3 styx_common.py")
    sys.exit(0)


# ── Category mapping ─────────────────────────────────────────────────────────

CATEGORY_MAP = {
    'FOOD_AND_DRINK': 'restaurant',
    'GENERAL_MERCHANDISE': 'retail',
    'TRANSPORTATION': 'transport',
    'GENERAL_SERVICES': 'service',
    'ENTERTAINMENT': 'entertainment',
    'MEDICAL': 'medical',
    'HOME_IMPROVEMENT': 'home',
    'LOAN_PAYMENTS': 'finance',
    'PERSONAL_CARE': 'personal_care',
    'TRANSFER_OUT': 'transfer',
    'INCOME': 'income',
    'BANK_FEES': 'finance',
    'GOVERNMENT_AND_NON_PROFIT': 'government',
    'TRANSFER_IN': 'transfer',
    'RENT_AND_UTILITIES': 'housing',
    'LOAN_DISBURSEMENTS': 'finance',
    'TRAVEL': 'travel',
}

# ── Name utilities ────────────────────────────────────────────────────────────

def normalize(name):
    """Normalize a name for matching: lowercase, strip punctuation, collapse spaces."""
    if not name:
        return ''
    n = name.lower()
    n = re.sub(r'[^a-z0-9\s]', '', n)
    n = re.sub(r'\s+', ' ', n).strip()
    return n

def is_redacted(name):
    """Check if a name is too redacted to be useful."""
    if not name:
        return True
    if re.search(r'^\*+$', name.strip()):
        return True
    asterisks = name.count('*')
    if asterisks > 0 and asterisks / len(name) > 0.3:
        return True
    return False

# ── Database schema ───────────────────────────────────────────────────────────

SCHEMA_DDL = [
    '''CREATE TABLE IF NOT EXISTS merchants (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        normalized_name TEXT NOT NULL,
        category TEXT,
        subcategory TEXT,
        address TEXT,
        city TEXT,
        state TEXT,
        zip TEXT,
        phone TEXT,
        website TEXT,
        source TEXT,
        confidence REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(normalized_name)
    )''',
    '''CREATE TABLE IF NOT EXISTS transaction_merchants (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        transaction_id TEXT NOT NULL,
        merchant_id INTEGER NOT NULL,
        raw_name TEXT NOT NULL,
        match_method TEXT,
        confidence REAL,
        is_primary INTEGER DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (merchant_id) REFERENCES merchants(id),
        UNIQUE(transaction_id, merchant_id)
    )''',
    '''CREATE TABLE IF NOT EXISTS enrichment_runs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        started_at TIMESTAMP,
        completed_at TIMESTAMP,
        transactions_processed INTEGER DEFAULT 0,
        merchants_found INTEGER DEFAULT 0,
        merchants_created INTEGER DEFAULT 0,
        status TEXT DEFAULT 'running',
        error TEXT
    )''',
]

def init_styx_db(db_path=None):
    """Initialize Styx database schema. Returns connection."""
    # Allow scripts to set STYX_DB before calling
    if db_path is None:
        db_path = os.environ.get('STYX_DB', '~/.hermes/data/styx.db')
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    for ddl in SCHEMA_DDL:
        conn.execute(ddl)
    conn.commit()
    return conn

def get_or_create_merchant(conn, name, category=None, source='enrichment', confidence=0.8):
    """Get existing merchant or create a new one. Returns (id, created)."""
    norm = normalize(name)
    row = conn.execute('SELECT id FROM merchants WHERE normalized_name = ?', (norm,)).fetchone()
    if row:
        return row[0], False
    cur = conn.execute(
        'INSERT INTO merchants (name, normalized_name, category, source, confidence) VALUES (?, ?, ?, ?, ?)',
        (name, norm, category, source, confidence)
    )
    return cur.lastrowid, True

def link_transaction(conn, transaction_id, merchant_id, raw_name, method, confidence):
    """Create a transaction-merchant link."""
    conn.execute(
        '''INSERT OR REPLACE INTO transaction_merchants
        (transaction_id, merchant_id, raw_name, match_method, confidence, is_primary)
        VALUES (?, ?, ?, ?, ?, 1)''',
        (transaction_id, merchant_id, raw_name, method, confidence)
    )

# ── Plaid helpers ─────────────────────────────────────────────────────────────

def load_env(path):
    """Load environment variables from a .env file."""
    env = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                k, v = line.split('=', 1)
                env[k.strip()] = v.strip()
    return env

def get_plaid_env():
    """Load Plaid credentials from the default secrets path."""
    env = load_env('~/.hermes/secrets/plaid.env')
    return env['PLAID_CLIENT_ID'], env['PLAID_SECRET'], 'https://production.plaid.com'

def plaid_post(endpoint, payload, client_id=None, secret=None, base_url=None):
    """Make a POST request to the Plaid API."""
    if client_id is None:
        client_id, secret, base_url = get_plaid_env()
    payload['client_id'] = client_id
    payload['secret'] = secret
    data = json.dumps(payload).encode()
    req = urllib.request.Request(base_url + endpoint, data=data,
                                  headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        return {'error': f'HTTP {e.code}: {body}'}

def store_transaction(conn, tx, account_id):
    """Upsert a single transaction. Returns True on success."""
    try:
        conn.execute(
            '''INSERT OR REPLACE INTO transactions
            (account_id, transaction_id, amount, currency, date, authorized_date,
             name, merchant_name, category, category_id, pending, payment_channel,
             personal_finance_category)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (
                account_id,
                tx.get('transaction_id'),
                tx.get('amount'),
                tx.get('iso_currency_code', 'USD'),
                tx.get('date'),
                tx.get('authorized_date'),
                tx.get('name'),
                tx.get('merchant_name'),
                json.dumps(tx.get('category')) if tx.get('category') else None,
                tx.get('category_id'),
                1 if tx.get('pending') else 0,
                tx.get('payment_channel'),
                tx.get('personal_finance_category', {}).get('primary') if tx.get('personal_finance_category') else None,
            )
        )
        return True
    except Exception as e:
        print(f"  Error storing tx {tx.get('transaction_id')}: {e}", file=sys.stderr)
        return False