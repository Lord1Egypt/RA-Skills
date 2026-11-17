---
name: ib-dividend-income
description: Read-only Interactive Brokers dividend income from Activity Flex Query data. Use when the user asks for paid or expected dividends over an inclusive date range, withholding and net income, currency or listing-country attribution, leading contributors, annual dividend-income estimates, or portfolio dividend yield. Reads the Flex Web Service only; never uses Gateway, market data, or orders.
metadata:
  openclaw:
    requires:
      bins: [python3]
    os: [darwin, linux]
---

# ib-dividend-income

Use `/ib-dividend-income` to retrieve one read-only Activity Flex report and
present dividend income for an inclusive date range. This is Flex-only: do not
start IB Gateway, do not request market data, do not place, modify, or cancel
orders, and do not persist account data. Never display the Flex token, Query ID,
account ID, raw XML, or service URL.

## Resolve the date range

Resolve both endpoints to inclusive `YYYY-MM-DD` dates in the user's local
timezone:

- “today” means today for both endpoints.
- “this month” / “month to date” means the first calendar day of this month
  through today; “this year” / “year to date” means January 1 through today.
- “last month” means the complete previous calendar month.
- “last N days” includes today and begins `N - 1` calendar days earlier.
- Keep explicit future end dates when the user wants expected dividends.
- Ask one clarifying question if no range is supplied or a phrase such as
  “recently” is ambiguous. Do not silently choose a range.

Reject a resolved start later than the end. Do not reinterpret the requested
range to fit a configured Flex window.

For a future range, expected rows extend through the requested future end date
when IBKR provides open accruals in that range. The annual trailing history is
capped at today, even when `--end-date` is later. Future calendar days do not
count toward `history_days_covered` or make a 365-day annual estimate complete.

## Run the command

Run exactly one command with both resolved dates:

```bash
{baseDir}/../.venv/bin/python {baseDir}/scripts/dividend_income.py \
  --config .ib-suite/config.yaml \
  --start-date 2026-01-01 \
  --end-date 2026-07-19
```

Parse the single JSON object from stdout. Treat stderr as operational logs; do
not copy it into the financial result. Do not reproduce or reimplement the
Python reconciliation, conversion, attribution, or estimation rules.

## Handle setup states

For `setup_required`, `coverage_required`, or `query_update_required`, stop
financial presentation, link the standalone guide at
`{baseDir}/flex-query-setup.md`, and show only the returned `missing` schema
names. Ask for one item at a time, and only when it is needed:

- If `flex.dividend_query_ids` is missing, ask which numeric window the user
  wants to register, then ask for that saved Activity Flex Query's Query ID.
- For `coverage_required`, use the numeric window named in `missing` and ask for
  its Query ID; do not ask the user to choose a different key silently.
- If `flex.token` is missing, ask for the Flex Web Service token after any
  needed window and Query ID have been collected. Do not ask for a configured
  item again.

Use the shared configurator. Pass a token through stdin with `--token-stdin`,
never as `--token` and never interpolated into the command line. Use
`--target dividend` so the window lands in `flex.dividend_query_ids`; the
dividend target needs a query carrying the six dividend sections (the full
7-section query also works):

```bash
{baseDir}/../.venv/bin/python {baseDir}/../ib-trade-history/scripts/configure_flex.py \
  --config .ib-suite/config.yaml \
  --token-stdin \
  --target dividend \
  --window '365=<query-id>'
```

When the token is already configured, omit `--token-stdin` and register only
the new `--window` (still passing `--target dividend`). If the configurator
refuses because a token or window key already exists, ask for
explicit confirmation to replace that exact item.
Append `--force` only after the user confirms; never treat an earlier general
setup request as overwrite approval. Then rerun `/ib-dividend-income` and report
the actual remote result. A successful local save validates configuration
persistence only, not the remote query.

For `query_update_required`, have the user edit the existing query to add every
returned missing section or field before rerunning. Do not register a new ID
unless the user created a new query. For other `status: error` responses, give
the safe message and guide link; do not infer the redacted service detail.

## Present a successful report

Follow the user's language. If the user asks in Chinese, present every table
heading, column label, summary, limitation, and setup question in Chinese. Keep
currency codes, symbols, dates, and the exact `REALIZED` / `EXPECTED` status
values unchanged.

Present these sections in this order.

### Realized dividends

Render `realized_dividends` first. These are confirmed paid cash events.

### Expected dividends

Render `expected_dividends` second and separately. These are open accruals, not
cash already received. Never combine them with realized rows or totals.

Use this exact column order for both tables:

`Symbol | Payment date | Status | Gross | Withholding tax | Fee | Net | Currency | FX rate to base | Base-currency amount | Quantity | Country`

Map “Base-currency amount” to `base_net`. Show an empty section explicitly when
its list is empty. Render a JSON `null` as “unavailable” (or the equivalent in
the user's language), never as zero. Do not guess missing tax, fee, FX, country,
quantity, or income values.

### Summaries and limitations

After the two tables, present all supplied summaries without recomputation:

1. separate realized totals and expected totals;
2. currency attribution, using the supplied separate realized and expected attribution
   buckets and keeping native currencies separate;
3. country attribution, also using separate realized and expected attribution
   buckets in base currency, including `UNKNOWN` as unresolved
   listing market rather than issuer domicile or tax residence;
4. highest-contributing holdings ranked by realized base-currency net;
5. annual estimate, its history coverage, and portfolio dividend yield.

Finish with `coverage_note` and every `data_limitations` item. Explain an
incomplete annual estimate as a history-based lower bound when the result says
history is shorter than 365 days. Never annualize it yourself, substitute live
prices or FX, or imply that expected income is guaranteed.
