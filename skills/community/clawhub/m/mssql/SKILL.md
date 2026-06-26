---
name: mssql
version: 1.0.2
description: Execute SQL Server queries and export results as delimiter-separated text. Use when the user asks to fetch, insert, update, or manage data in Microsoft SQL Server, validate BI/reporting numbers, or prepare datasets for charts.
metadata: { "openclaw": { "emoji": "DB", "requires": { "bins": ["sqlcmd"], "env": ["MSSQL_HOST", "MSSQL_DB", "MSSQL_USER", "MSSQL_PASSWORD"] } } }
---

# MSSQL

Run SQL Server queries using `scripts/mssql_query.sh`.

## Quick start

1. Ensure credentials exist at:
   `~/.openclaw/credentials/mssql.env`
2. Run a query:
   `bash skills/mssql/scripts/mssql_query.sh --query "SELECT TOP 20 name FROM sys.tables"`
3. Save to file:
   `bash skills/mssql/scripts/mssql_query.sh --query "SELECT TOP 100 * FROM dbo.MyTable" --out /tmp/mytable.dsv`

## Credentials format

Expected env vars in `~/.openclaw/credentials/mssql.env`:

- `MSSQL_HOST`
- `MSSQL_DB`
- `MSSQL_USER`
- `MSSQL_PASSWORD`
- Optional: `MSSQL_PORT` (default `1433`), `MSSQL_ENCRYPT` (`yes`/`no`, default `yes`), `MSSQL_TRUST_CERT` (`yes`/`no`, default `no`), `SQLCMD_BIN`

The credential file path can be overridden with the `MSSQL_ENV_FILE` environment variable.

## Permissions

Query permissions are controlled entirely at the SQL Server user level. The script does not impose any restrictions on query type — the database user's grants determine what is allowed.

## Database reference map

Place your database map at `references/DB_MAP.md` inside this skill folder. This file tells the agent which databases, schemas, and tables to use and how they relate to each other.

See `references/DB_MAP.example.md` for the expected format.

## Useful patterns

- Run long query from file:
  `bash skills/mssql/scripts/mssql_query.sh --file /path/query.sql --out /tmp/out.dsv`
- Override database:
  `bash skills/mssql/scripts/mssql_query.sh --db OtherDB --query "SELECT TOP 10 * FROM dbo.Users"`
- Change delimiter:
  `bash skills/mssql/scripts/mssql_query.sh --query "SELECT ..." --delim ","`
- Increase timeout:
  `bash skills/mssql/scripts/mssql_query.sh --query "SELECT ..." --timeout 180`

## Output format

Output is **delimiter-separated text**, not RFC 4180 CSV. Fields are not quoted or escaped. This works well for structured numeric and short-text data. If your columns contain embedded delimiters, quotes, or newlines, the output may be malformed — choose a delimiter that does not appear in the data, or post-process the output.

## Best practices

- Prefer explicit columns over `SELECT *`.
- Use `TOP` for exploratory samples.
- Keep queries scoped to the user request.
- Answer in business language by default; provide SQL details when requested.
- Never print or expose credentials in responses.

## Troubleshooting

- `sqlcmd not found` -> install sqlcmd v18+ or set `SQLCMD_BIN`.
- TLS/certificate issues on internal networks -> set `MSSQL_TRUST_CERT=yes` in your credentials file. The default is `no` (certificate validation enabled).
