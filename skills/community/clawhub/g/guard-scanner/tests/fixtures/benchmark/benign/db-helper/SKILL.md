# Database Query Helper

Helps users construct and execute safe SQL queries.

## Instructions

When the user asks to query a database, generate parameterized queries only.

```javascript
const sqlite3 = require('better-sqlite3');

function query(db, sql, params = []) {
  const stmt = db.prepare(sql);
  return stmt.all(...params);
}

function insert(db, table, data) {
  const keys = Object.keys(data);
  const placeholders = keys.map(() => '?').join(', ');
  const sql = `INSERT INTO ${table} (${keys.join(', ')}) VALUES (${placeholders})`;
  return db.prepare(sql).run(...Object.values(data));
}

module.exports = { query, insert };
```
