# SQL Reference

Use this when writing or debugging `outlit_query` / `outlit query` queries.

Always inspect schema first with `outlit_get_schema` (`topic`: `views`, `view`, `event_types`, `examples`) or `outlit schema get`. The schema is the authority for columns, units, coverage, freshness, duplicates, and worked examples. The earlier name `outlit_schema` works as an alias until 2026-12-11.

## Views

Use the public analytics views, not backend table names:

- `activity`: product use, email and Slack, calls and meetings, CRM and billing changes, support tickets, and other customer activity. Count events with `uniqExact(event_id)`, not `count()`.
- `customers`: customer/account attributes, billing status, lifetime revenue, engagement counts, and current ARR (`arr_amount`, `arr_currency`, `arr_decimals`). `arr_cents`, `mrr_cents`, and `mrr_status` are deprecated; use `arr_amount` with its currency and decimals.
- `users`: people at customers, profile traits, journey-stage fields, roles, acquisition, and their own activity.
- `revenue`: ARR per customer per UTC day since 2026-11-06: `snapshot_date`, `arr_amount`, `arr_currency`, `arr_decimals`, `arr_estimated`, `revenue_lifecycle`, and the customer's `customer_id`, `customer_name`, `customer_domain`, and `customer_status`. No row for a day means it was not computed; today's row is approximate until the day's last sync. There are no MRR columns and no `arr_history` view.

Read `outlit_get_schema` for the exact column list and the view rules before relying on a boundary case.

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
custom_properties['key']
```

Use ClickHouse syntax, not MySQL or Postgres helpers like `DATE_SUB()`.

## Rules

- Only one read-only `SELECT` (or `WITH ... SELECT`) is allowed.
- Add time filters for event queries.
- Use `LIMIT`.
- Prefer specific columns over `SELECT *`; avoid selecting large JSON unless needed.
- Money is in minor units: divide `arr_amount` by `10^arr_decimals` for display, and keep currencies apart (filter or group by `arr_currency`). Never add amounts across currencies.
- A JOIN from customers to activity or users multiplies rows. Use `IN`/`EXISTS`, or aggregate the many-row side first.
- Send `page.nextCursor` with the identical SQL to read the next page of the frozen result. On a large export, check `truncation`; if present, partition the export with narrower filters or time windows, or aggregate in SQL instead of trying to read past the retained-result cap.

## Use SQL for

- Counts, sums, ratios, cohorts, time series, and rankings that need aggregation or fields unavailable in the customer tools.
- Cross-customer aggregations or custom reporting.
- Event names, event properties, traits, custom windows, and other fields the curated tools do not carry.
- Per-currency ARR totals. For one customer's lifetime revenue, use `outlit_get_customer` with `include: ["revenue"]`; it returns lifetime revenue with each amount's currency.

For one customer's current ARR, subscriptions, renewal date, credits, meters, or relationship state, `outlit_get_customer` usually carries the answer with its provenance. Choose the tool that directly matches the question rather than applying a fixed ordering.
