# SQL Injection Fix Patterns — Quick Reference for Reviewers

## Vulnerable Patterns (R1 Blockers)

| Pattern | Why It's Vulnerable | Fix |
|---------|---------------------|-----|
| `f"SELECT * FROM t WHERE x = '{input}'"` | String interpolation allows injection | `"SELECT * FROM t WHERE x = ?", (input,)` |
| `cursor.execute("SELECT * FROM t WHERE x = '%s'" % input)` | Python % formatting | `"SELECT * FROM t WHERE x = ?", (input,)` |
| `cursor.execute("SELECT * FROM t WHERE x = {}".format(input))` | .format() interpolation | `"SELECT * FROM t WHERE x = ?", (input,)` |
| `cursor.execute(query)` where `query` built via f-string | Indirect interpolation | Always use parameter placeholders |

## Safe Patterns (All Databases)

### SQLite / Python sqlite3
```python
# GOOD
cursor.execute("SELECT * FROM users WHERE name = ?", (name,))
cursor.execute("SELECT * FROM users WHERE name = ? AND age > ?", (name, age))

# GOOD with named params (sqlite3 supports :name)
cursor.execute("SELECT * FROM users WHERE name = :name", {"name": name})
```

### PostgreSQL / psycopg2
```python
cursor.execute("SELECT * FROM users WHERE name = %s", (name,))
cursor.execute("SELECT * FROM users WHERE name = %(name)s", {"name": name})
```

### MySQL / mysql-connector
```python
cursor.execute("SELECT * FROM users WHERE name = %s", (name,))
```

### General Rule
- **Never** concatenate user input into SQL strings
- **Always** use parameter placeholders (`?`, `%s`, `:name`, `%(name)s`)
- Parameters are passed as separate tuple/dict argument to `execute()`

## Test Cases for Verification

| Input | Expected Behavior |
|-------|-------------------|
| `"O'Reilly"` | Returns row (quote handled as literal) |
| `"Test; DROP TABLE users"` | Returns row if exists, **no table drop** |
| `"admin' --"` | Returns row if exists, **no comment injection** |
| `"' OR '1'='1"` | Returns row if exists, **no tautology** |
| `""` (empty string) | Returns empty list or matching rows |
| `None` | TypeError or returns empty (validate before query) |
| `"日本語"` / `"Иван"` / `"José"` | Works correctly (Unicode safe) |

## Red Flags in Code Review

- [ ] Any `f"SELECT..."` or `f"INSERT..."` with variables
- [ ] Any `.format()` or `%` in SQL string construction
- [ ] Dynamic table/column names from user input (validate against allowlist)
- [ ] `cursor.execute(query)` where `query` is a variable built elsewhere
- [ ] String concatenation: `"SELECT * FROM " + table_name`

## Semgrep Rules (Auto-catch)

```yaml
# Custom rule for sqlite3 f-string SQL
rules:
  - id: python-sqlite-fstring-injection
    pattern-either:
      - pattern: cursor.execute(f"...")
      - pattern: cursor.execute("..." % ...)
      - pattern: cursor.execute("...".format(...))
    message: "Possible SQL injection - use parameterized queries"
    languages: [python]
    severity: ERROR
```