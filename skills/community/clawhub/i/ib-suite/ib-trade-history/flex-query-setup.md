# IBKR Activity Flex Query setup for trade history

This standalone guide configures the saved Activity Flex Queries used by
`ib-trade-history` and shared with `ib-dividend-income`. It is a read-only
reporting path: do not start IB Gateway, do not request market data, do not
place, modify, or cancel orders, and do not persist trade data to the lake. The
only local write is the Flex token and Query ID window map in the ignored
`.ib-suite/config.yaml`; never paste either value into logs, reports, source
files, or version control.

Official IBKR references: [create an Activity Flex Query](https://www.ibkrguides.com/clientportal/performanceandstatements/activityflex.htm),
[enable Flex Web Service](https://www.ibkrguides.com/brokerportal/performanceandstatements/flex-web-service.htm),
and [Flex Web Service API](https://www.interactivebrokers.com/campus/ibkr-api-page/flex-web-service/).

## 1. Create the Activity Flex Query in Client Portal

1. Sign in to IBKR Client Portal with the same username that will own the query.
2. Open **Performance & Reports → Flex Queries**. The alternate navigation is
   **Menu → Reporting → Flex Queries**. If the Account Selector appears, select
   the account or account set the report must cover.
3. In **Activity Flex Query**, select the **+** icon, enter a descriptive name
   such as `ib-suite-trades-7`, and add every section and field in §2. Select
   each section, select its fields in the pop-up, then select **Save**.
4. Under **Delivery Configuration**, select the intended account(s), choose
   **Format: XML**, and choose the window profile from §3.
5. Under **General Configuration**, set **Date Format: yyyy-MM-dd**,
   **Time Format: HH:mm:ss**, and **Date/Time Separator: ; (semicolon)**. These
   settings produce timestamps such as `2026-07-19;13:45:00` that the trade
   parser expects.
6. Select **Continue**, review the `Trades` section (plus any optional
   compatibility sections), fields, accounts, XML output, and period, then
   select **Create**.

## 2. Select the Trades section (and optional compatibility sections)

The names before parentheses are the Client Portal labels; the backticked names
are the XML attributes the command reads. `Trades` is the only section
`ib-trade-history` parses, so it must be complete and exact. `ib-trade-history`
now keeps its own Query ID map (`flex.trade_history_query_ids`), so a
trade-history query may be a `Trades`-only query. Add the other six sections only
if you want to reuse the same saved query for `/ib-dividend-income` by also
registering it under the dividend target.

### Trades

This is the core section for `ib-trade-history`. Select Date/Time (`dateTime`),
Trade ID (`tradeID`), Symbol (`symbol`), Buy/Sell (`buySell`), Quantity
(`quantity`), Trade Price (`tradePrice`), IB Commission (`ibCommission`),
Currency (`currency`), IB Commission Currency (`ibCommissionCurrency`),
Multiplier (`multiplier`), Order Type (`orderType`), Exchange (`exchange`),
Open/Close Indicator (`openCloseIndicator`), FIFO P&L Realized
(`fifoPnlRealized`), and FX Rate to Base (`fxRateToBase`). Every field is
required; a missing attribute makes the command reject the report and name the
field to enable. An empty Open/Close Indicator is valid for CASH or IDEALFX
fills. FX Rate to Base is what converts a foreign-currency fill and its
commission into the account base currency, so do not omit it.

### Account Information

Select Account ID (`accountId`) and Base Currency / Currency (`currency`).

### Cash Transactions

Select Account ID (`accountId`), Currency (`currency`), Asset Class
(`assetCategory`), FX Rate to Base (`fxRateToBase`), Symbol (`symbol`),
Description (`description`), Conid (`conid`), Underlying Conid
(`underlyingConid`), Underlying Symbol (`underlyingSymbol`), Date/Time
(`dateTime`), Amount (`amount`), Type (`type`), Trade ID (`tradeID`),
871(m) Withholding (`withholdingTax`), and Code (`code`).

### Change in Dividend Accruals

Select Account ID (`accountId`), Currency (`currency`), Asset Class
(`assetCategory`), FX Rate to Base (`fxRateToBase`), Symbol (`symbol`),
Description (`description`), Conid (`conid`), Date (`date`), Ex Date
(`exDate`), Pay Date (`payDate`), Quantity (`quantity`), Tax (`tax`), Fee
(`fee`), Gross Rate (`grossRate`), Gross Amount (`grossAmount`), Net Amount
(`netAmount`), Code (`code`), and Report Date (`reportDate`).

### Open Dividend Accruals

Select Account ID (`accountId`), Currency (`currency`), Asset Class
(`assetCategory`), FX Rate to Base (`fxRateToBase`), Symbol (`symbol`), Conid
(`conid`), Ex Date (`exDate`), Pay Date (`payDate`), Quantity (`quantity`), Tax
(`tax`), Fee (`fee`), Gross Rate (`grossRate`), Gross Amount (`grossAmount`),
Net Amount (`netAmount`), and Code (`code`).

### Open Positions

Select **Level of Detail: Summary**, not lot detail. Select Account ID
(`accountId`), Currency (`currency`), Asset Class (`assetCategory`), FX Rate to
Base (`fxRateToBase`), Symbol (`symbol`), Conid (`conid`), Report Date
(`reportDate`), Quantity (`quantity`), Multiplier (`multiplier`), Mark Price
(`markPrice`), Position Value (`positionValue`), Side (`side`), and Level of
Detail (`levelOfDetail`). Summary rows prevent lots from being double counted.

### Financial Instrument Information

Select Asset Class (`assetCategory`), Symbol (`symbol`), Currency (`currency`),
Listing Exchange (`listingExchange`), Description (`description`), Conid
(`conid`), ISIN (`isin`), Multiplier (`multiplier`), and Security Subtype / Sub
Category (`subCategory`) when available.

## 3. Create coverage windows

Create one saved query per coverage profile you need, with identical sections
and formatting. `ib-trade-history` is the primary user of every profile below,
including the `mtd` and `ytd` logical periods:

| Config key | Client Portal Period | Purpose |
|---|---|---|
| `7` | Last N Calendar Days: 7 | default request when no date range is stated |
| `30` | Last N Calendar Days: 30 | month-scale lookbacks |
| `90` | Last N Calendar Days: 90 | quarter-scale lookbacks |
| `365` | Last 365 Calendar Days (or Last N Calendar Days: 365) | year-scale lookbacks and older ranges |
| `mtd` | Month to Date | `/ib-trade-history --period mtd` ("this month") |
| `ytd` | Year to Date | `/ib-trade-history --period ytd` ("this year") |

For a date range, the command picks the smallest configured **numeric** window
whose day count (counting today) reaches the requested start date. A request
older than the largest numeric window still uses it and adds a `coverage_note`
instead of failing, so register a longer numeric window when you need complete
history for older ranges.

For `--period mtd`/`ytd`, the command prefers the registered `mtd`/`ytd` query
and uses it with no note. When that logical key is absent, it falls back to the
numeric pool for the period's start date and carries a `coverage_note` through.
Register the `mtd` and `ytd` queries to get IBKR's native month/year period and
avoid that fallback. The `7` profile is what a bare `/ib-trade-history` with no
date range uses, so register at least `7`.

## 4. Retrieve each Query ID and the Flex Web Service token

For each saved query, return to **Performance & Reports → Flex Queries** and
select the **Info** icon beside that query. Copy the Query ID shown at the top of
the information pop-over. Keep a private mapping from the exact window (`7`, `30`,
`90`, `365`, `mtd`, `ytd`) to its Query ID; the displayed query name is not the
ID.

On the same Flex Queries page, open **Flex Web Service Configuration**, select
the configure gear, enable **Flex Web Service Status**, and save. Copy the
generated **Current Token**. If the account is in a linked structure, the token
may be visible only from the master account; query visibility also depends on
selecting the same account set used when the query was created.

Treat the token as a credential. A Query ID is also private configuration. Do
not send either through screenshots, command arguments containing the token,
shell history, logs, or source control.

## 5. Register credentials conversationally

First ensure the ib-suite onboarding flow has created
`.ib-suite/config.yaml`. In a conversation, collect one item at a time: desired
window, matching Query ID, then the token only if it is absent. Do not ask the
user to repeat a token that is already configured.

`ib-trade-history` and `ib-dividend-income` now register independent Query IDs
while sharing one Flex token. Pass `--target trade_history` so windows land in
`flex.trade_history_query_ids` (a `Trades`-only query is fine here); a query
carrying the six dividend sections belongs under the dividend target instead.

For the first token and window, run the configurator with `--token-stdin`:

```bash
{baseDir}/../.venv/bin/python {baseDir}/scripts/configure_flex.py \
  --config .ib-suite/config.yaml \
  --token-stdin \
  --target trade_history \
  --window '7=<query-id>'
```

Send the token followed by one newline to the running process's stdin; do not
substitute it into the command. The process never echoes it. When a token is
already stored, add new windows without reading or rewriting that token; repeat
`--window` to register several keys in one confirmed operation:

```bash
{baseDir}/../.venv/bin/python {baseDir}/scripts/configure_flex.py \
  --config .ib-suite/config.yaml \
  --target trade_history \
  --window '30=<query-id>' --window '90=<query-id>' \
  --window 'mtd=<query-id>' --window 'ytd=<query-id>'
```

The configurator refuses to replace an existing token or window key. If
replacement is intended, name the exact key and obtain explicit confirmation
from the user; only then rerun the command with `--force`. Never add `--force`
preemptively or infer overwrite approval from a general request to configure
Flex.

To rotate an expired or exposed token, select **Generate A New Token** in Client
Portal (this invalidates the prior token), choose its expiration and optional IP
restriction, then—with explicit confirmation to replace the local token—run
(token-only, so no `--target` is needed):

```bash
{baseDir}/../.venv/bin/python {baseDir}/scripts/configure_flex.py \
  --config .ib-suite/config.yaml \
  --token-stdin \
  --force
```

## 6. Validate and troubleshoot

A successful configurator response such as
`{"config":".ib-suite/config.yaml","ready":true}` proves only that the ignored
local file was written atomically and reloads under the local schema. Saving
local credentials does not prove the remote query is correct. Validate remotely
by rerunning `/ib-trade-history` for an explicit date range or `--period`; a
successful report is the end-to-end check.

### Troubleshooting

- Flex Trade field missing: the command names the exact `Trades` attribute to
  enable (for example `orderType` or `fxRateToBase`). Edit the saved query, add
  that field from §2, save, and rerun. Saving a local Query ID cannot repair its
  remote template.
- Base currency unresolved: set `data.base_currency` in `.ib-suite/config.yaml`;
  it is required to convert foreign-currency fills and commissions.
- Third-currency commission rejected: a fill whose commission currency differs
  from both the asset currency and the base currency has no independent Flex rate
  in this report. The command rejects it rather than inventing a total; there is
  no field to add for this case.
- Missing window / coverage: register the numeric key whose Client Portal period
  covers the requested day count, retrieve its Query ID, and add that key. If the
  requested range exceeds the longest numeric period Client Portal makes
  available, expect a `coverage_note`; do not label a shorter query as a larger
  key.
- `--period mtd`/`ytd` falls back with a note: register the `mtd` or `ytd`
  query and add that logical key to get IBKR's native period.
- Token expired / Flex error 1012: generate a new token, then follow the
  explicit token-rotation confirmation flow above.
- Query not visible: sign in with the username that created it and select the
  same account set. Linked accounts may require the master account.
- Invalid report or missing section after an edit: confirm **Activity** Flex
  Query (not Trade Confirmation), **XML**, the `Trades` section (plus any
  optional compatibility sections you added), the exact fields,
  and the date/time settings, then run the saved query once in Client Portal.
- Statement temporarily unavailable: wait and retry once later; Activity Flex
  data updates on IBKR's reporting schedule and is not real-time. Do not poll it
  as a market-data source.
