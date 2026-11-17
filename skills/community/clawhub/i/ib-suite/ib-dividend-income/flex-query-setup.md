# IBKR Activity Flex Query setup for dividend income

This standalone guide configures the saved Activity Flex Queries shared by
`ib-dividend-income` and `ib-trade-history`. It is a read-only reporting path:
do not start IB Gateway, do not request market data, do not place, modify, or
cancel orders, and do not persist account data. The only local write is the
Flex token and Query ID window map in the ignored
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
   such as `ib-suite-dividends-365`, and add every section and field in §2.
   Select each section, select its fields in the pop-up, then select **Save**.
4. Under **Delivery Configuration**, select the intended account(s), choose
   **Format: XML**, and choose the window profile from §3.
5. Under **General Configuration**, set **Date Format: yyyy-MM-dd**,
   **Time Format: HH:mm:ss**, and **Date/Time Separator: ; (semicolon)**. These
   settings produce timestamps such as `2026-07-19;13:45:00`.
6. Select **Continue**, review the six dividend sections (plus the optional
   `Trades` section), fields, accounts, XML output,
   and period, then select **Create**.

## 2. Select the six dividend sections (and optional Trades) and fields

The names before parentheses are the Client Portal labels; the backticked names
are the XML attributes validated by the command. Include the section even when
the current account has no rows for it. The six dividend sections below are
required by `ib-dividend-income`. `ib-trade-history` now keeps its own Query ID
map, so a dividend-only query needs just these six sections; adding the seventh
`Trades` section lets the same saved query double as a trade-history query when
you also register it under the trade-history target.

### Account Information

Select Account ID (`accountId`) and Base Currency / Currency (`currency`).

This section is mandatory even though it holds no dividend rows: its `currency`
is the single source of the report's base currency, which every base-value
conversion depends on. If the section is missing the command returns
`query_update_required`; if its `currency` differs across rows the parse fails
with an inconsistent-currency error. Client Portal can silently drop this
section when you edit the query, so re-confirm both fields are still checked
after any change and save again.

### Cash Transactions

Select Account ID (`accountId`), Currency (`currency`), Asset Class
(`assetCategory`), FX Rate to Base (`fxRateToBase`), Symbol (`symbol`),
Description (`description`), Conid (`conid`), Underlying Conid
(`underlyingConid`), Underlying Symbol (`underlyingSymbol`), Date/Time
(`dateTime`), Amount (`amount`), Type (`type`), Trade ID (`tradeID`),
and Code (`code`).

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
(`reportDate`), Quantity (`position`), Multiplier (`multiplier`), Mark Price
(`markPrice`), Position Value (`positionValue`), Side (`side`), and Level of
Detail (`levelOfDetail`). Summary rows prevent lots from being double counted.

### Financial Instrument Information

Select Asset Class (`assetCategory`), Symbol (`symbol`), Currency (`currency`),
Listing Exchange (`listingExchange`), Description (`description`), Conid
(`conid`), ISIN (`isin`), Multiplier (`multiplier`), and Security Subtype / Sub
Category (`subCategory`) when available.

### Trades

Select Date/Time (`dateTime`), Trade ID (`tradeID`), Symbol (`symbol`), Buy/Sell
(`buySell`), Quantity (`quantity`), Trade Price (`tradePrice`), IB Commission
(`ibCommission`), Currency (`currency`), IB Commission Currency
(`ibCommissionCurrency`), Multiplier (`multiplier`), Order Type (`orderType`),
Exchange (`exchange`), Open/Close Indicator (`openCloseIndicator`), FIFO P&L
Realized (`fifoPnlRealized`), and FX Rate to Base (`fxRateToBase`). This section
is not used to calculate dividend income; include it only if you want to reuse
this saved query for `/ib-trade-history` by also registering it under the
trade-history target.

## 3. Create coverage windows

Create one saved query per numeric coverage profile you need, with identical
sections and formatting:

| Config key | Client Portal Period | Purpose |
|---|---|---|
| `7` | Last N Calendar Days: 7 | short-range dividend requests |
| `30` | Last N Calendar Days: 30 | month-scale dividend requests |
| `90` | Last N Calendar Days: 90 | quarter-scale dividend requests |
| `365` | Last 365 Calendar Days (or Last N Calendar Days: 365) | annual-history estimate and most dividend requests |

The `7/30/90` profiles serve short-range dividend requests. Dividend income
generally requires a `365` profile because its annual estimate needs up to 365
days of trailing history capped at today. The dividend command chooses the
smallest configured **numeric** window that covers both the requested dates and
that trailing-history requirement. Older historical requested ranges may need a
longer registered numeric window and return `coverage_required` until one is
available. Do not label a shorter query as `365` or claim future requested days
make trailing history complete.

Optional Month to Date and Year to Date queries may be registered as `mtd` and
`ytd` under the trade-history target. The current dividend command uses numeric
keys only, so `mtd` or `ytd` alone does not satisfy dividend coverage.

## 4. Retrieve each Query ID and the Flex Web Service token

For each saved query, return to **Performance & Reports → Flex Queries** and
select the **Info** icon beside that query. Copy the Query ID shown at the top of
the information pop-over. Keep a private mapping from the exact numeric window
to its Query ID; the displayed query name is not the ID.

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

`ib-dividend-income` and `ib-trade-history` now register independent Query IDs
while sharing one Flex token. Pass `--target dividend` so windows land in
`flex.dividend_query_ids` (the dividend map needs a query carrying the six
dividend sections); a `Trades`-only query belongs under the trade-history
target instead.

For the first token and window, run the configurator with `--token-stdin`:

```bash
{baseDir}/../.venv/bin/python {baseDir}/../ib-trade-history/scripts/configure_flex.py \
  --config .ib-suite/config.yaml \
  --token-stdin \
  --target dividend \
  --window '365=<query-id>'
```

Send the token followed by one newline to the running process's stdin; do not
substitute it into the command. The process never echoes it. When a token is
already stored, add a new window without reading or rewriting that token:

```bash
{baseDir}/../.venv/bin/python {baseDir}/../ib-trade-history/scripts/configure_flex.py \
  --config .ib-suite/config.yaml \
  --target dividend \
  --window '90=<query-id>'
```

Repeat `--window` to add multiple new keys in one confirmed operation. The
configurator refuses to replace an existing token or window key. If replacement
is intended, name the exact key and obtain explicit confirmation from the user;
only then rerun the command with `--force`. Never add `--force` preemptively.

To rotate an expired or exposed token, select **Generate A New Token** in Client
Portal (this invalidates the prior token), choose its expiration and optional IP
restriction, then—with explicit confirmation to replace the local token—run
(token-only, so no `--target` is needed):

```bash
{baseDir}/../.venv/bin/python {baseDir}/../ib-trade-history/scripts/configure_flex.py \
  --config .ib-suite/config.yaml \
  --token-stdin \
  --force
```

## 6. Validate and troubleshoot

A successful configurator response such as
`{"config":".ib-suite/config.yaml","ready":true}` proves only that the ignored
local file was written atomically and reloads under the local schema. Saving
local credentials does not prove the remote query is correct. Validate remotely
by rerunning `/ib-dividend-income` for an explicit date range; a successful
report is the end-to-end check.

### Troubleshooting

- `setup_required`: register the returned missing `flex.token` or numeric
  `flex.dividend_query_ids` item. Never print existing values while checking.
- `coverage_required`: create a numeric query whose Client Portal period covers
  the returned day count, retrieve its Query ID, and register that numeric key.
  If the requested count exceeds the longest numeric period Client Portal makes
  available, explain that the current workflow cannot cover that range and ask
  the user to shorten it; never register a misleading larger key.
- `query_update_required`: edit the selected saved query and add every returned
  section or field from §2. Saving a local ID cannot repair its remote template.
- Token expired / Flex error 1012: generate a new token, then follow the explicit
  token-rotation confirmation flow above.
- Query not visible: sign in with the username that created it and select the
  same account set. Linked accounts may require the master account.
- Invalid report or missing section after an edit: confirm **Activity** Flex
  Query (not Trade Confirmation), **XML**, the six dividend sections (plus the
  optional `Trades` section), the exact fields,
  and the date/time settings, then run the saved query once in Client Portal.
- Statement temporarily unavailable: wait and retry once later; Activity Flex
  data updates on IBKR's reporting schedule and is not real-time. Do not poll it
  as a market-data source.
