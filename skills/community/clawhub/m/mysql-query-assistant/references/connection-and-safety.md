# Connection and safety

## Environment variables

This skill expects these environment variables:

- `DB_URL`: mysql connection target in url form, for example `mysql://db.example.com:3306/app_db`
- `DB_USER`: mysql username
- `DB_PASSWORD`: mysql password

Optional:

- `DB_SSL_MODE`: mysql ssl mode when supported by the driver
- `DB_CHARSET`: default `utf8mb4`

The scripts parse host, port, and database name from `DB_URL`.

## Driver support

The bundled scripts try these python drivers in order:

1. `mysql.connector`
2. `pymysql`

Install one if needed:

```bash
pip install mysql-connector-python
```

or

```bash
pip install pymysql
```

## Read-only policy

`run_read_query.py` only allows a single read-only statement.

Blocked examples:

- multiple statements separated by semicolons
- `insert`, `update`, `delete`, `replace`
- `create`, `alter`, `drop`, `truncate`
- `grant`, `revoke`, `lock`, `unlock`, `set`

Allowed examples:

- `select ...`
- `with ... select ...`
- `show tables`
- `show columns from ...`
- `describe table_name`
- read-only queries against `information_schema`

## Validation guidance

Double validation means both of these must be checked before presenting the answer:

### Structural validation

Confirm that:

- the chosen tables match the business question
- join keys are plausible
- filters match the requested scope
- time columns reflect the intended business event
- grouping and aggregation match the requested metric

### Result validation

Confirm that:

- sample rows look semantically correct
- nulls, duplicates, or unexpectedly empty results are explained
- magnitudes and trends are plausible for the request
- the output columns are enough to support the final summary

If confidence is low, say so explicitly and explain what remains uncertain.
