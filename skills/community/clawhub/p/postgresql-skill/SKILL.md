---
name: postgre_sql_skill
description: Execute PostgreSQL database operations using psycopg2. List tables, describe schema, execute SQL queries.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - python3
    envVars:
      - name: DB_HOST
        required: false
        description: Optional override for database host (defaults to config.yaml)
      - name: DB_PORT
        required: false
        description: Optional override for database port (defaults to config.yaml)
      - name: DB_NAME
        required: false
        description: Optional override for database name (defaults to config.yaml)
      - name: DB_USER
        required: false
        description: Optional override for database user (defaults to config.yaml)
      - name: DB_PASSWORD
        required: false
        description: Optional override for database password (defaults to config.yaml)
    install:
      - kind: uv
        package: psycopg2-binary
      - kind: uv
        package: pyyaml
    emoji: "🐘"
    homepage: https://gitee.com/tengshengbo/postgre_sql_skill
---

# PostgreSQL Database Operations

Pure Python PostgreSQL skill using psycopg2 (no psql client needed).

## When to Use

Use this skill when the user needs to:
- **List database tables**: "What tables are in the database?", "show tables"
- **View table structure**: "What columns does the users table have?", "describe users"
- **Execute SQL queries**: "Get all users", "SELECT * FROM users"
- **Get schema summary**: "What's the database structure?", "schema overview"
- **Modify data**: Insert, update, or delete records

## When NOT to Use

- User asks conceptual questions (e.g., "What is PostgreSQL?")
- User needs data analysis or business insights (requires LLM reasoning)
- User wants natural language to SQL conversion (should be handled by upper-layer Agent)
- Database is not PostgreSQL

## Usage Guidelines for AI Agents

### Step 1: Check Prerequisites

Before using this skill, ensure:
1. Python 3 is installed
2. Dependencies are installed: `pip install psycopg2-binary pyyaml`
3. `config.yaml` exists with valid database connection details

If config.yaml is missing, instruct the user to:
```bash
cp config.example.yaml config.yaml
# Then edit config.yaml with real database credentials
```

### Step 2: Choose the Right Command

| User Intent | Command | Example |
|------------|---------|---------|
| List tables | `python scripts/pgsql_skill.py list-tables` | Get all table names |
| Describe table | `python scripts/pgsql_skill.py describe-table <table>` | `describe-table users` |
| Query data | `python scripts/pgsql_skill.py execute-sql "<SQL>"` | `execute-sql "SELECT * FROM users LIMIT 10"` |
| Schema overview | `python scripts/pgsql_skill.py schema-summary` | Full database structure |

### Step 3: Parse Results

All commands return JSON (except schema-summary):

**list-tables output:**
```json
{"tables": ["users", "orders", "products"]}
```

**describe-table output:**
```json
{
  "table": "users",
  "columns": [
    {"name": "id", "type": "integer", "nullable": false, "default": null},
    {"name": "username", "type": "varchar", "nullable": false, "default": null}
  ]
}
```

**execute-sql SELECT output:**
```json
{
  "columns": ["id", "username", "email"],
  "rows": [
    {"values": ["1", "alice", "alice@example.com"]},
    {"values": ["2", "bob", "bob@example.com"]}
  ]
}
```

**execute-sql INSERT/UPDATE/DELETE output:**
```json
{"affected_rows": 1}
```

### Step 4: Handle Errors

If a command fails, check the error message:
- `"error": "config.yaml not found"` → Guide user to create config
- `"error": "psycopg2 not installed"` → Run `pip install psycopg2-binary`
- `"error": "connection failed"` → Verify database credentials
- `"error": "Forbidden operation"` → SQL violates safety rules

## Safety Rules

This skill enforces strict SQL safety:

✅ **Allowed:**
- SELECT queries
- INSERT (single row only)
- UPDATE (must have WHERE clause)
- DELETE (must have WHERE clause)

❌ **Blocked:**
- DROP TABLE/DATABASE
- TRUNCATE TABLE
- ALTER TABLE
- Batch INSERT (multiple rows)
- UPDATE/DELETE without WHERE

Example of blocked query:
```bash
python scripts/pgsql_skill.py execute-sql "DROP TABLE users"
# Output: {"error": "Forbidden operation: DROP"}
```

## Programmatic Integration

For advanced usage, import directly in Python:

```python
import sys
from pathlib import Path
sys.path.insert(0, 'scripts')

from pgsql_skill import Database, load_config

# Initialize database connection
config = load_config()
db = Database(
    host=config['host'],
    port=config['port'],
    dbname=config['dbname'],
    user=config['user'],
    password=config.get('password', '')
)

# Use database methods
tables = db.list_tables()
structure = db.describe_table("users")
result = db.execute_sql("SELECT count(*) FROM users")

# Always close connection
db.close()
```

## Troubleshooting

- **ModuleNotFoundError: psycopg2**: Run `pip install psycopg2-binary`
  - On macOS with managed Python: `pip install psycopg2-binary --no-binary :all:`
- **config.yaml not found**: Copy from config.example.yaml
- **Connection failed**: Verify host/port/user/password in config.yaml
- **Permission denied**: Check database user permissions

## Best Practices

1. **Add LIMIT** to SELECT queries to avoid large result sets
2. **Always check errors** before proceeding
3. **Close connections** when using programmatic API
4. **Warn users before data modifications** (INSERT/UPDATE/DELETE) and confirm intent
