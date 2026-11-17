---
name: ib-trade-history
description: Read-only Interactive Brokers trade history from Flex Query. Use when the user asks to list executions or fills for a date range, inspect buy and sell activity, commissions, order type, exchange, open/close status, realized FIFO P&L, win rate, average win/loss, or profit/loss ratio. Reads Flex records only - never places, modifies, or cancels an order.
metadata:
  openclaw:
    requires:
      bins: [python3]
      config: [config.yaml]
    os: [darwin, linux]
---

# ib-trade-history

Read only the requested IBKR Flex Query trade history. Do not place, modify, or
cancel orders; do not start IB Gateway; do not write trade data to the lake.

## Prerequisites

Build one Flex Query per lookback window you need in IBKR. For the complete
Client Portal walkthrough — creating the Activity Flex Query, selecting every
section and field, creating coverage windows, and registering credentials —
follow the standalone guide at `{baseDir}/flex-query-setup.md`. The field
requirements are unchanged: every query's `Trades` section must include
`dateTime`, `tradeID`, `symbol`, `buySell`, `quantity`, `tradePrice`,
`ibCommission`, `currency`, `ibCommissionCurrency`, `multiplier`, `orderType`,
`exchange`, `openCloseIndicator`, `fifoPnlRealized`, and `fxRateToBase`. Each
query's history window must cover the days it is registered for.

Set `data.base_currency` in `.ib-suite/config.yaml`. Credentials come only from
`flex.token` and the `flex.trade_history_query_ids` map (days -> Query ID) in
that local config; there is no environment-variable fallback. Before running
`/ib-trade-history`, check those fields without exposing any value. To register
a window, ask for the matching Query ID and ask for the Flex token only when it
is not already configured. Invoke the configurator with `--token-stdin` through
the execution tool (repeat `--window` for each window you register):

```bash
{baseDir}/../.venv/bin/python {baseDir}/scripts/configure_flex.py \
  --config .ib-suite/config.yaml --token-stdin \
  --target trade_history \
  --window '7=<query-id>'
```

After starting the process, send the provided token followed by one newline on
stdin through the execution tool. Never place the token in argv or command text,
and do not use `printf`, `echo`, an environment variable, or a shell pipeline to
feed it. The configurator never echoes the value.

When the token is already stored, register month-to-date and year-to-date
windows without reading or resupplying it, using `mtd`/`ytd` in place of a day
count:

```bash
{baseDir}/../.venv/bin/python {baseDir}/scripts/configure_flex.py \
  --config .ib-suite/config.yaml \
  --target trade_history \
  --window 'mtd=<query-id>' --window 'ytd=<query-id>'
```

Adding a brand-new window does not need `--force`. Overwriting an existing
`flex.token` or replacing a window whose days-key is already present requires
`--force`; without it the tool refuses and leaves the config untouched. Name
the exact item and obtain explicit confirmation before rerunning with `--force`.
Never add `--force` to an initial setup command or infer overwrite approval from
a general request to configure Flex.

This setup persists plaintext credentials only in the ignored local config,
validates only local persistence, does not validate against the Flex Web Service,
and never echoes values.

The runtime picks the smallest configured window whose day count is greater
than or equal to the requested lookback (counting today); requests older than
the largest configured window use it and add a `coverage_note`.

## Command

For a date range, resolve the user's dates to inclusive `YYYY-MM-DD` values and run:

```bash
{baseDir}/../.venv/bin/python {baseDir}/scripts/trade_history.py \
  --config .ib-suite/config.yaml \
  --start-date 2026-07-01 \
  --end-date 2026-07-17
```

With no stated time range, omit both date arguments to query the latest seven
calendar days:

```bash
{baseDir}/../.venv/bin/python {baseDir}/scripts/trade_history.py \
  --config .ib-suite/config.yaml
```

For month-to-date or year-to-date, use `--period` (mutually exclusive with the
date arguments):

```bash
{baseDir}/../.venv/bin/python {baseDir}/scripts/trade_history.py \
  --config .ib-suite/config.yaml --period mtd
```

Interpret "this month" / "month to date" as `--period mtd`, and "this year" /
"year to date" as `--period ytd`. If the matching `mtd`/`ytd` window is not
registered, the runtime falls back to the numeric windows and adds a
`coverage_note`. Interpret "last month" as the previous calendar month via
`--start-date`/`--end-date`; ask one clarifying question for ambiguous phrases
such as "recently".

The script prints one JSON object with `trades` and `summary`. Each fill keeps
its original currency; notional includes the Flex contract multiplier. `FIFO
P/L` is IBKR's realized P&L; do not recompute lots. An empty open/close
indicator is valid for CASH or IDEALFX fills. Commission conversion uses the
asset FX rate only when its currency matches the asset currency, or uses 1.0
when the commission is already in the account base currency. A third currency
commission has no independent Flex rate in this report, so the script rejects
it instead of inventing a base-currency total. Zero-P&L fills are excluded from
win rate. `profit_loss_ratio` is null when there are no winning or no losing
realized-P&L fills.
