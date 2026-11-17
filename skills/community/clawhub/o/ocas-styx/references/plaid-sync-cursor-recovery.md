# Plaid Backfill Pattern

## When to Use
- Plaid sync cron shows `last_status: "ok"` but `MAX(date)` in `transactions.db` is stale
- Bank shows transactions that don't appear in the database
- After a gateway outage or cron downtime

## Diagnosis
```python
import sqlite3, json, urllib.request

# 1. Check last sync date
conn = sqlite3.connect('<hermes-home>/data/transactions.db')
print("Last txn:", conn.execute('SELECT MAX(date) FROM transactions').fetchone())
print("Total:", conn.execute('SELECT COUNT(*) FROM transactions').fetchone())

# 2. Test Plaid API directly
env = {}
with open('<hermes-home>/secrets/plaid.env') as f:
    for line in f:
        if '=' in line and not line.startswith('#'):
            k, v = line.strip().split('=', 1)
            env[k] = v

# 3. Query /transactions/get for recent data
payload = {
    'client_id': env['PLAID_CLIENT_ID'],
    'secret': env['PLAID_SECRET'],
    'access_token': '<from plaid_items table>',
    'start_date': '2026-06-01',
    'end_date': '2026-06-15',
    'options': {'count': 500}
}
data = json.dumps(payload).encode()
req = urllib.request.Request('https://production.plaid.com/transactions/get', data=data, headers={'Content-Type': 'application/json'})
with urllib.request.urlopen(req, timeout=60) as resp:
    result = json.loads(resp.read())
print(f"API has {result.get('total_transactions')} transactions in range")
```

## Fix: Backfill via /transactions/get

```python
import json, urllib.request, sqlite3
from datetime import datetime

env = {}; 
with open('<hermes-home>/secrets/plaid.env') as f:
    for line in f:
        if '=' in line and not line.startswith('#'):
            k, v = line.strip().split('=', 1); env[k] = v

conn = sqlite3.connect('<hermes-home>/data/transactions.db')
existing = set(r[0] for r in conn.execute('SELECT transaction_id FROM transactions').fetchall())
items = conn.execute('SELECT item_id, access_token, institution_name FROM plaid_items').fetchall()

total_new = 0
for plaid_item_id, access_token, inst_name in items:
    offset = 0
    while True:
        payload = {
            'client_id': env['PLAID_CLIENT_ID'], 'secret': env['PLAID_SECRET'],
            'access_token': access_token,
            'start_date': '<start_of_gap>', 'end_date': '<today>',
            'options': {'count': 500, 'offset': offset}
        }
        data = json.dumps(payload).encode()
        req = urllib.request.Request('https://production.plaid.com/transactions/get', data=data, headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req, timeout=60) as resp:
            result = json.loads(resp.read())
        txs = result.get('transactions', [])
        total = result.get('total_transactions', 0)
        new_txs = [tx for tx in txs if tx.get('transaction_id') not in existing]
        for tx in new_txs:
            conn.execute('''INSERT OR REPLACE INTO transactions
                (account_id, transaction_id, amount, currency, date, authorized_date,
                 name, merchant_name, category, category_id, pending, payment_channel,
                 personal_finance_category)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                (tx.get('account_id'), tx.get('transaction_id'), tx.get('amount'),
                 tx.get('iso_currency_code','USD'), tx.get('date'), tx.get('authorized_date'),
                 tx.get('name'), tx.get('merchant_name'),
                 json.dumps(tx.get('category')) if tx.get('category') else None,
                 tx.get('category_id'), 1 if tx.get('pending') else 0,
                 tx.get('payment_channel'),
                 tx.get('personal_finance_category',{}).get('primary') if tx.get('personal_finance_category') else None))
            existing.add(tx.get('transaction_id')); total_new += 1
        conn.commit()
        offset += len(txs)
        if offset >= total or not txs: break
        print(f'{inst_name}: {total} total, {total_new} new so far')

# Reset sync cursors
conn.execute('DELETE FROM sync_cursor')
conn.commit()
print(f'Inserted {total_new} transactions, cursors reset')
conn.close()
```

## Key Points
- `/transactions/get` uses date ranges — always paginate with offset (max 500 per request)
- `/transactions/sync` uses cursors — cursor can get stuck if no transactions for a period
- After backfill, **always** `DELETE FROM sync_cursor` so the daily cron's sync works again
- Plaid merchant names have prefixes: `TST*` (Toast), `SQ*` (Square), `SP*` (Stripe), `DD*` (DoorDash)
- Transactions lag 1-3 days behind bank UI — this is normal