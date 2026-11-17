# Pivot Tables Reference

## Contents

1. When to use this
2. CLI workflow
3. Pivot config shape
4. Common patterns
5. Verification

## 1. When to use this

Read this document when the task involves creating, previewing, overwriting, or
deleting persisted pivot tables in worksheet cells.

Use `mbs pivot` for native pivot-table aggregation. Do not hand-build
`MAYBE_PIVOT(...)`, call pivot APIs through `raw post`, or use ordinary formula
writes unless `mbs pivot --help` proves the first-class command is unavailable.

## 2. CLI workflow

Default flow:

1. `mbs workbook metadata` or `mbs workbook list-worksheets`
2. Identify the source worksheet name and header row
3. Author `pivot-config.json`
4. Run `mbs pivot preview`
5. Run `mbs pivot upsert` with an explicit target worksheet and anchor cell
6. Read the target range or worksheet to verify the result

CLI:

```bash
mbs pivot preview --doc-id <DOC_ID> --worksheet-name SourceData --spec pivot-config.json --output table
mbs pivot upsert --doc-id <DOC_ID> --target-worksheet-name PivotResult --anchor-cell A1 --spec pivot-config.json
mbs excel-worksheet read --doc-id <DOC_ID> --worksheet-name PivotResult --range A1:H30 --output table
```

Use `--dry-run` before mutation when you need to confirm the write request
without changing the workbook:

```bash
mbs pivot upsert --doc-id <DOC_ID> --target-worksheet-name PivotResult --anchor-cell A1 --spec pivot-config.json --dry-run
```

Delete an existing persisted pivot by target worksheet and anchor cell:

```bash
mbs pivot delete --doc-id <DOC_ID> --worksheet-name PivotResult --anchor-cell A1 --dry-run
mbs pivot delete --doc-id <DOC_ID> --worksheet-name PivotResult --anchor-cell A1 --yes
```

## 3. Pivot config shape

Reusable example: [../artifacts/pivot-config.json](../artifacts/pivot-config.json)

`pivot-config.json` for `preview` and the usual `upsert` path is the pivot
config object:

```json
{
  "worksheet_name": "SourceData",
  "range_address": "A1:E1001",
  "row_fields": ["period", "dimension_type"],
  "column_fields": [],
  "metrics": [
    {
      "aggregate": "sum",
      "value_field": "settled_amount_reporting",
      "label": "settled_revenue_reporting"
    }
  ],
  "row_sort": {"by": "label", "order": "asc"},
  "show_row_totals": false,
  "show_column_totals": false,
  "blank_label": "(blank)"
}
```

Important rules:

- `worksheet_name` should identify the source worksheet.
- `range_address` is optional only when the full used range should be inferred.
- `row_fields` and `column_fields` must match source headers.
- `metrics[].aggregate` commonly uses `sum`, `count`, `avg`, `min`, or `max`.
- Use `metrics[].value_field: ""` for count-style pivots that count rows.
- `row_sort.by` and `column_sort.by` support `label` or `value`.
- `row_sort.order` and `column_sort.order` support `asc` or `desc`.
- Always pass `--anchor-cell` to `pivot upsert`; if the user says `A1`, keep `A1`.
- The target worksheet can be created by the backend semantic pivot path; do not pre-create it just to call `pivot upsert`.

`pivot read` uses the older read shape and supports one metric. If the spec
contains a single `metrics[]` item, the CLI converts it to `aggregate` and
`value_field`; for multi-metric output use `pivot preview`.

## 4. Common patterns

Single row dimension with totals:

```json
{
  "worksheet_name": "Orders",
  "range_address": "A1:F5000",
  "row_fields": ["region"],
  "metrics": [
    {
      "aggregate": "sum",
      "value_field": "revenue",
      "label": "total_revenue"
    }
  ],
  "show_row_totals": true,
  "show_column_totals": false
}
```

Rows by columns with sorted labels:

```json
{
  "worksheet_name": "Orders",
  "range_address": "A1:F5000",
  "row_fields": ["region"],
  "column_fields": ["category"],
  "metrics": [
    {
      "aggregate": "sum",
      "value_field": "revenue",
      "label": "total_revenue"
    }
  ],
  "row_sort": {"by": "label", "order": "asc"},
  "column_sort": {"by": "label", "order": "asc"},
  "show_row_totals": true,
  "show_column_totals": true
}
```

Row count:

```json
{
  "worksheet_name": "Orders",
  "range_address": "A1:F5000",
  "row_fields": ["status"],
  "metrics": [
    {
      "aggregate": "count",
      "value_field": "",
      "label": "order_count"
    }
  ]
}
```

For row slice requests such as "2:5 row", include the header row in the range,
for example `A1:C5`, so the pivot can still resolve field names.

## 5. Verification

Use `preview` to inspect the shape before writing:

```bash
mbs pivot preview --doc-id <DOC_ID> --worksheet-name SourceData --spec pivot-config.json --output table
```

After `upsert`, verify the written worksheet:

```bash
mbs excel-worksheet read --doc-id <DOC_ID> --worksheet-name PivotResult --range A1:H30 --output table
mbs workbook list-worksheets --doc-id <DOC_ID> --output table
```

If the target sheet was auto-created, `workbook list-worksheets` should show it
after the write completes.
