# Styx Database Schema

Styx maintains its own SQLite database at `<hermes-home>/data/styx.db`.

**Path note:** Hardcode this path. Do NOT use `{agent_root}` — under the `indigo` Hermes profile it resolves to `<hermes-home>/profiles/indigo/home/.hermes/` which does NOT contain Styx data. The active DBs are:
- `<hermes-home>/data/transactions.db` — raw Plaid transaction data
- `<hermes-home>/data/styx.db` — enriched merchant data

A second copy at `<hermes-home>/commons/data/ocas-styx/styx.db` is a stale 0-byte stub — ignore it.

## Tables

### merchants

Canonical business/merchant entities.

```sql
CREATE TABLE merchants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,              -- canonical business name
    normalized_name TEXT NOT NULL,   -- lowercase, stripped for matching
    category TEXT,                   -- business category (restaurant, grocery, etc.)
    subcategory TEXT,                -- finer classification
    address TEXT,
    city TEXT,
    state TEXT,
    zip TEXT,
    phone TEXT,
    website TEXT,
    source TEXT,                     -- how this merchant was identified
    confidence REAL,                 -- 0.0-1.0 confidence in this entity
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(normalized_name)
);
```

### transaction_merchants

Links transactions to merchants (many-to-many).

```sql
CREATE TABLE transaction_merchants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    transaction_id TEXT NOT NULL,    -- from transactions.db
    merchant_id INTEGER NOT NULL,
    raw_name TEXT NOT NULL,          -- original transaction name
    match_method TEXT,               -- 'exact', 'fuzzy', 'search', 'llm'
    confidence REAL,                 -- 0.0-1.0
    is_primary INTEGER DEFAULT 1,    -- best match for this transaction
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (merchant_id) REFERENCES merchants(id),
    UNIQUE(transaction_id, merchant_id)
);
```

### enrichment_runs

Tracks enrichment pipeline execution.

```sql
CREATE TABLE enrichment_runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    transactions_processed INTEGER DEFAULT 0,
    merchants_found INTEGER DEFAULT 0,
    merchants_created INTEGER DEFAULT 0,
    status TEXT DEFAULT 'running',   -- 'running', 'completed', 'failed'
    error TEXT
);
```

### receipt_line_items

Stores parsed email receipt line items (e.g., Rainbow Grocery eReceipts).
23 columns; `id` auto-increments, so INSERT supplies 22 values.

```sql
CREATE TABLE IF NOT EXISTS receipt_line_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    transaction_id TEXT,              -- matched Styx transaction ID
    message_id TEXT,                  -- Gmail message ID
    receipt_number TEXT,              -- receipt number from email
    plu_upc TEXT,                     -- PLU or UPC code
    product_name TEXT,                -- product name as printed on receipt
    brand TEXT,                       -- brand (from Open Food Facts lookup)
    category TEXT,                    -- product category
    subcategory TEXT,                 -- product subcategory
    department TEXT,                  -- store department (BULK, PRODUCE, etc.)
    price REAL,                       -- line item price
    tax_code TEXT,                    -- 'T' = taxable, 'E' = exempt
    quantity REAL,                    -- item count (NULL if weighted)
    unit_price REAL,                  -- price per unit (for qty items)
    weight_lb REAL,                   -- weight in pounds (for bulk/produce)
    price_per_lb REAL,                -- price per pound
    is_bulk INTEGER DEFAULT 0,        -- 1 if sold by weight
    is_organic INTEGER DEFAULT 0,     -- 1 if organic
    source_receipt_date TEXT,         -- date from receipt email
    match_method TEXT,                -- how transaction was matched
    match_confidence REAL,            -- 0.0-1.0 confidence in match
    merchant_name TEXT NOT NULL,      -- 'Rainbow Grocery Cooperative'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Initialization note**: This table must be created before running the receipt parsing pipeline. If `styx.db` exists but has no tables, run the CREATE TABLE statements above first. The `seed.py` script may also handle initialization — check `references/scripts.md`.