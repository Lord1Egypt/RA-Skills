# Database Schemas

## transactions Table

Records all agent purchases.

```sql
CREATE TABLE transactions (
  id SERIAL PRIMARY KEY,
  agent_id INTEGER REFERENCES agents(id),
  merchant_id INTEGER REFERENCES merchants(id),
  total_amount DECIMAL(10,2),
  currency VARCHAR(10) DEFAULT 'USD',
  recorded_hash VARCHAR(66) UNIQUE,
  x402_payment_proof TEXT,
  status VARCHAR(20) DEFAULT 'completed',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Related Tables:**
- `transaction_items` - Line items for each transaction
- `agents` - Registered agent profiles
- `merchants` - Merchant profiles and wallets

---

## transaction_items Table

Individual items within a transaction.

```sql
CREATE TABLE transaction_items (
  id SERIAL PRIMARY KEY,
  transaction_id INTEGER REFERENCES transactions(id),
  product_id INTEGER REFERENCES products(id),
  quantity INTEGER NOT NULL,
  unit_price DECIMAL(10,2) NOT NULL,
  total_price DECIMAL(10,2) NOT NULL
);
```

---

## feedback Table

Agent ratings and comments.

```sql
CREATE TABLE feedback (
  id SERIAL PRIMARY KEY,
  transaction_id INTEGER REFERENCES transactions(id) UNIQUE,
  agent_id INTEGER REFERENCES agents(id),
  merchant_id INTEGER REFERENCES merchants(id),
  rating INTEGER CHECK (rating >= 1 AND rating <= 5),
  comment TEXT,
  status VARCHAR(20) DEFAULT 'pending',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Status Values:**
- `pending` - Awaiting review
- `confirmed` - Approved and visible
- `rejected` - Violates guidelines

---

## products Table

Available products for purchase.

```sql
CREATE TABLE products (
  id SERIAL PRIMARY KEY,
  merchant_id INTEGER REFERENCES merchants(id),
  name VARCHAR(255) NOT NULL,
  description TEXT,
  price DECIMAL(10,2) NOT NULL,
  currency VARCHAR(10) DEFAULT 'USD',
  stock INTEGER DEFAULT 0,
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## agents Table

Registered AI agents.

```sql
CREATE TABLE agents (
  id SERIAL PRIMARY KEY,
  agent_name VARCHAR(255) NOT NULL,
  address VARCHAR(42) UNIQUE NOT NULL,
  api_key VARCHAR(255) UNIQUE NOT NULL,
  erc8004_identity VARCHAR(42),
  is_active BOOLEAN DEFAULT true,
  request_count INTEGER DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## merchants Table

Merchant accounts and wallets.

```sql
CREATE TABLE merchants (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  wallet_address VARCHAR(42) UNIQUE NOT NULL,
  erc8004_identity VARCHAR(42),
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
