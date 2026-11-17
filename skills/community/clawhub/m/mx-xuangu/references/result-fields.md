# mx-xuangu Result Fields

Read this only when parsing raw `mx_xuangu_*_raw.json` or explaining CSV columns.

## Status and Counts

- `status`: API global status, usually `0` for success.
- `message`: global message.
- `data.code`: screening parser status. `100` usually means parsed successfully.
- `data.data.result.total`: final number of matched securities.
- `data.data.result.totalRecordCount`: total row count, should align with `total`.

## Column Definition

- `data.data.result.columns[]`: table column metadata.
- `columns[].title`: display title, often includes unit.
- `columns[].key`: row key used in `dataList`.
- `columns[].dateMsg`: date attached to a column.
- `columns[].sortable`: whether front-end sorting is supported.
- `columns[].sortWay`: default sort direction.
- `columns[].unit`: unit such as yuan, percent, shares, or multiple.
- `columns[].dataType`: String, Double, Long, etc.

## Row Data

- `data.data.result.dataList[]`: matched securities.
- Common keys: `SECURITY_CODE`, `SECURITY_SHORT_NAME`, `MARKET_SHORT_NAME`, `NEWEST_PRICE`, `CHG`, `PCHG`.
- Use the generated CSV for user-facing output because the script maps many columns to Chinese labels.

## Condition Echo

- `responseConditionList[]`: per-condition match statistics.
- `responseConditionList[].describe`: parsed condition text.
- `responseConditionList[].stockCount`: count matched by that condition.
- `totalCondition.describe`: combined final condition.
- `parserText`: semicolon-separated parsed conditions.
