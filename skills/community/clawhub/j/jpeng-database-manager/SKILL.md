---
name: jpeng-database-manager
description: "Database management skill supporting PostgreSQL, MySQL, SQLite, and MongoDB. Query, migrate, backup, and manage databases."
version: "1.0.0"
author: "jpeng"
tags: ["database", "sql", "postgresql", "mysql", "mongodb", "backup"]
---

# Database Manager

Manage databases with support for multiple database systems.

## When to Use

- User wants to query a database
- Create backups and migrations
- Manage database schemas
- Import/export data

## Supported Databases

- PostgreSQL
- MySQL / MariaDB
- SQLite
- MongoDB

## Configuration

```bash
# PostgreSQL
export DB_TYPE="postgresql"
export DB_HOST="localhost"
export DB_PORT="5432"
export DB_NAME="mydb"
export DB_USER="postgres"
export DB_PASS="password"

# MongoDB
export DB_TYPE="mongodb"
export DB_URI="mongodb://localhost:27017/mydb"
```

## Usage

### Execute query

```bash
python3 scripts/db.py query "SELECT * FROM users LIMIT 10"
```

### Execute from file

```bash
python3 scripts/db.py query --file ./query.sql
```

### Create backup

```bash
python3 scripts/db.py backup --output ./backup.sql
```

### Restore backup

```bash
python3 scripts/db.py restore --input ./backup.sql
```

### Run migration

```bash
python3 scripts/db.py migrate --dir ./migrations/
```

### Export to CSV

```bash
python3 scripts/db.py export \
  --table users \
  --format csv \
  --output ./users.csv
```

### Import from CSV

```bash
python3 scripts/db.py import \
  --table users \
  --input ./users.csv
```

## Output

```json
{
  "success": true,
  "rows_affected": 10,
  "rows": [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"}
  ]
}
```
