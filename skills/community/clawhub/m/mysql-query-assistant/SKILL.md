---
name: mysql-query-assistant
description: translate natural-language analytics requests into mysql queries, connect to a live mysql database, inspect schema and column comments, execute read-only sql, and validate query correctness against real results. use when chatgpt needs to work with mysql through direct connection details provided by environment variables, especially for ad hoc analysis, sql generation, schema discovery, query debugging, or cautious database workflows that must verify results before presenting them. also use for restricted write workflows that first generate a preview select and never auto-execute the write statement.
---

# Mysql Query Assistant

Use this skill to turn a user's request into safe MySQL work against a live database.

## Core workflow

For every request, follow this sequence:

1. Inspect connection prerequisites from `references/connection-and-safety.md`.
2. Discover relevant schema first. Prefer column comments when available.
3. Draft the SQL.
4. Execute only read-only SQL with `scripts/run_read_query.py`.
5. Perform double validation:
   - structural validation: tables, columns, joins, filters, grouping, and syntax match the request.
   - result validation: returned rows and aggregates look semantically consistent with the user's intent.
6. If validation fails, revise the SQL and run it again.
7. Present the final answer using the output template below.

## Default behavior

- Prefer `SELECT` queries only.
- Never auto-execute `INSERT`, `UPDATE`, `DELETE`, `REPLACE`, `ALTER`, `DROP`, `TRUNCATE`, `CREATE`, `GRANT`, or `REVOKE`.
- Keep result samples small by default.
- When the request is ambiguous, use schema inspection to narrow candidate tables before writing SQL.
- Prefer explicit column lists over `SELECT *` unless schema exploration is the user's goal.
- Prefer bounded queries. Add `LIMIT` when the user did not ask for a full extract.

## Schema discovery workflow

Before generating SQL, inspect schema with `scripts/introspect_schema.py`.

Use this order:

1. List candidate tables.
2. Inspect columns, data types, keys, and column comments for the most relevant tables.
3. Infer business meaning from comments and names.
4. Only then draft SQL.

If comments are missing, fall back to table names, column names, keys, and a few small probing queries.

## Read-only execution workflow

Use `scripts/run_read_query.py` to execute the SQL.

The script rejects non-read-only statements. It also blocks multi-statement execution.

When verifying a query:

1. Run the first candidate SQL.
2. Review row count, sample rows, and whether the columns answer the request.
3. If the result is empty or suspicious, explain why and try a corrected query when appropriate.
4. If multiple interpretations are plausible, prefer the query best supported by schema and results, and say what assumption you made.

## Restricted write workflow

When the user asks for a write operation:

1. Do not execute the write statement.
2. First produce a preview `SELECT` that shows exactly which rows would be affected.
3. Then produce the write SQL separately.
4. Clearly label the write SQL as not executed.
5. Call out any missing safety condition such as a weak or absent `WHERE` clause.

## Output template

Use this structure unless the user asks for a different format.

### Final SQL

```sql
[final sql]
```

### Validation

- Structural check: [why the sql shape matches the request]
- Result check: [why the returned data seems correct, or why confidence is limited]

### Sample results

Show 5 to 20 rows when available and useful. Keep wide tables compact.

### Result summary

Provide a brief natural-language summary of what the query shows.

### Notes

Include assumptions, caveats, and any schema uncertainties.

## Execution details

- Use environment variables described in `references/connection-and-safety.md`.
- Use `scripts/introspect_schema.py` for schema discovery.
- Use `scripts/run_read_query.py` for executing read-only SQL.
- If the python mysql driver is missing, install one of the documented options before running the scripts.

## Examples

### Example: analytics request

User request: `统计最近 7 天每天新增用户数`

Expected approach:

1. Inspect likely user table and created-at column.
2. Confirm time column semantics from comments or names.
3. Generate grouped date query.
4. Run it.
5. Verify the date buckets and counts look plausible.

### Example: restricted write request

User request: `把 status = 'pending' 且 30 天前创建的订单改成 expired`

Expected approach:

1. Generate preview `SELECT` for the target rows.
2. Generate `UPDATE` SQL separately.
3. Do not execute the `UPDATE`.
4. Warn if the table lacks a reliable key or if the filter looks too broad.
