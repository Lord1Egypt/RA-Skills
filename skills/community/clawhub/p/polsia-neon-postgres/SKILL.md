---
name: neon-postgres
description: 'Use Neon PostgreSQL conventions for Polsia apps, including migration patterns and DATABASE_URL usage.'
---

# Neon PostgreSQL

Polsia apps use Neon PostgreSQL. DATABASE_URL is automatically provided.

## Connection
```javascript
const { Pool } = require('pg');
const pool = new Pool({ connectionString: process.env.DATABASE_URL });
```

## Migrations
Create files in migrations/ with timestamp prefix: 1704067200000_add_products_table.js

## Migration Format
```javascript
module.exports = {
  up: async (pool) => {
    await pool.query(`CREATE TABLE products (...)`);
  },
  down: async (pool) => {
    await pool.query(`DROP TABLE products`);
  }
};
```

## Key Rules
- DATABASE_URL is NOT available at build time on Render
- Run migrations in startCommand, not buildCommand
- Always use parameterized queries ($1, $2) for user input
