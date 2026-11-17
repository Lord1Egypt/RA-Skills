# Styx Query API

Other skills read from Styx using these patterns. Connect with:
`sqlite3.connect('{agent_root}/data/styx.db')`

## Get enriched transactions for a category

Returns all transactions in a given category with resolved merchant names.

```python
import sqlite3
conn = sqlite3.connect('{agent_root}/data/styx.db')
rows = conn.execute('''
    SELECT t.name as raw_name, t.amount, t.date,
           m.name as merchant_name, m.category, m.city,
           tm.confidence, tm.match_method
    FROM transaction_merchants tm
    JOIN merchants m ON tm.merchant_id = m.id
    JOIN transactions t ON tm.transaction_id = t.transaction_id
    WHERE m.category = 'restaurant'
    ORDER BY t.date DESC
''').fetchall()
```

## Get spending by merchant

Aggregates total spend and visit count per merchant.

```python
rows = conn.execute('''
    SELECT m.name, SUM(t.amount) as total, COUNT(*) as visits
    FROM transaction_merchants tm
    JOIN merchants m ON tm.merchant_id = m.id
    JOIN transactions t ON tm.transaction_id = t.transaction_id
    WHERE tm.is_primary = 1
    GROUP BY m.id
    ORDER BY total DESC
''').fetchall()
```

## Get unresolved transactions (for enrichment)

Returns transactions with no merchant link — candidates for enrichment.

```python
rows = conn.execute('''
    SELECT t.transaction_id, t.name, t.merchant_name, t.amount,
           t.date, t.personal_finance_category
    FROM transactions t
    LEFT JOIN transaction_merchants tm ON t.transaction_id = tm.transaction_id
    WHERE tm.id IS NULL
    ORDER BY t.date DESC
''').fetchall()
```