# SQL Reference

Use this when writing or debugging `outlit_query` / `outlit sql` queries.

Always inspect schema first with `outlit_schema` or `outlit schema`.

## Tables

Use the public analytics views exposed by `outlit schema`, not backend table names:

- `activity`: product, communication, support, CRM, and other customer activity
- `customers`: customer/account attributes, billing status, and revenue fields
- `users`: user/contact attributes and journey-stage fields
- `revenue`: revenue and MRR reporting fields

## ClickHouse patterns

```sql
now()
today()
toStartOfMonth(occurred_at)
dateDiff('day', first_seen_at, now())
occurred_at >= now() - INTERVAL 30 DAY
countIf(billing_status = 'PAYING')
sumIf(mrr_cents, billing_status = 'PAYING')
JSONExtractString(properties, 'path')
```

Use ClickHouse syntax, not MySQL or Postgres helpers like `DATE_SUB()`.

## Rules

- Only `SELECT` queries are allowed.
- Add time filters for event queries.
- Use `LIMIT`.
- Prefer specific columns over `SELECT *`.
- Divide cents by `100` for display.

## Use SQL when

- You need aggregates, cohorts, joins, or time-series analysis.
- You need cross-customer reporting.

Use customer tools or commands instead for single-account lookups.
