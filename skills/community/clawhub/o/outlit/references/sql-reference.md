# SQL Reference

Use this when writing or debugging `outlit_query` / `outlit sql` queries.

Always inspect schema first with `outlit_get_schema` (`topic`: `views`, `view`, `event_types`, `examples`) or `outlit schema`. The earlier name `outlit_schema` works as an alias until 2026-12-11.

## Tables

Use the public analytics views exposed by `outlit schema`, not backend table names:

- `activity`: product, communication, support, CRM, and other customer activity
- `customers`: customer/account attributes, billing status, and revenue fields (`arr_amount`, `arr_currency`, `arr_decimals`; `arr_cents`, `mrr_cents` and `mrr_status` are deprecated until 2026-12-11, use `arr_amount`)
- `users`: user/contact attributes and journey-stage fields
- `revenue`: ARR per customer per UTC day since 2026-11-06: `snapshot_date`, `arr_amount`, `arr_currency`, `arr_decimals`, `arr_estimated`, `revenue_lifecycle`, and the customer's `customer_id`, `customer_name`, `customer_domain` and `customer_status`. No row for a day means it was not computed; today's row is approximate until the day's last sync. There are no MRR columns and no `arr_history` view.

## ClickHouse patterns

```sql
now()
today()
toStartOfMonth(occurred_at)
dateDiff('day', first_seen_at, now())
occurred_at >= now() - INTERVAL 30 DAY
countIf(billing_status = 'PAYING')
sumIf(arr_amount, billing_status = 'PAYING' AND arr_currency = 'USD')
JSONExtractString(properties, 'path')
```

Use ClickHouse syntax, not MySQL or Postgres helpers like `DATE_SUB()`.

## Rules

- Only `SELECT` queries are allowed.
- Add time filters for event queries.
- Use `LIMIT`.
- Prefer specific columns over `SELECT *`.
- Money is in minor units: divide `arr_amount` by `10^arr_decimals` for display, and keep currencies apart (filter or group by `arr_currency`).

## Use SQL when

- You need aggregates, cohorts, joins, or time-series analysis.
- You need cross-customer reporting.

Use customer tools or commands instead for single-account lookups.
