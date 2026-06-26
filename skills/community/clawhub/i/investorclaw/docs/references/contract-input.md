<!--
v4.x adaptation note: this reference contract is carried forward from
v2.6 essentially unchanged — the engine's input/output schema, holdings
field mapping, and consultative-LLM setup are identical in v4.x. The
only surface change is invocation: replace v2.x `/portfolio X` slash
commands with the equivalent v4.x MCP tool (`portfolio_X`) or a
natural-language query through `portfolio_ask`. Paths like
`~/portfolio_reports/` correspond to the bind-mounted `./reports/`
under your compose project; `portfolios/` corresponds to the
bind-mounted `./portfolios/`.
-->

# Input Contract

Supported portfolio file types: CSV, Excel (`.xls`, `.xlsx`). Place files in
`portfolios/` or `$INVESTOR_CLAW_PORTFOLIO_DIR`.

## Auto-detected column names

| Column | Recognized names |
|--------|-----------------|
| Symbol | `SYMBOL`, `TICKER`, `symbol`, `Description` |
| Quantity | `QUANTITY`, `SHARES`, `QTY`, `shares` |
| Price | `PRICE`, `MARKET PRICE`, `current_price` |
| Value | `VALUE`, `MARKET VALUE`, `value` |
| Asset type | `ASSET TYPE`, `TYPE`, `asset_type` |
| Cost basis | `COST BASIS`, `PURCHASE PRICE`, `purchase_price` |
| Purchase date | `PURCHASE DATE`, `purchase_date` |
| Coupon rate | `COUPON`, `COUPON RATE`, `coupon_rate` (bonds) |
| Maturity date | `MATURITY`, `MATURITY DATE`, `maturity_date` (bonds) |

## Bond metadata in description strings

Bond coupon and maturity embedded in description text (e.g.,
`"RATE 05.000% MATURES 11/01/28"`) are extracted automatically during
ingestion. No explicit coupon/maturity columns are required for bonds if the
description carries them.

## Guided mapping

Run `/portfolio setup` for guided column-mapping if your broker uses column
names that don't appear in the recognized-names table above.
