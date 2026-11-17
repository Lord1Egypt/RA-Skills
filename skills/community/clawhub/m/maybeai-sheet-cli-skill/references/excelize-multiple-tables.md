# Excelize Worksheets With Multiple Tables

Use this reference when one Excelize worksheet contains two or more separate
content-backed tables. A worksheet name identifies the sheet, not an individual
table block. Table identity comes from the table metadata and `table_id`.

## Discovery

List the table blocks before reading or importing the worksheet:

```bash
mbs excel-worksheet list-table \
  --doc-id <DOC_ID> \
  --worksheet-name '<WORKSHEET_NAME>' \
  --output json
```

The response provides one entry per table, including:

- `table_id`: stable target for `excel-table` commands during the current run
- `range` / `range_address`: the worksheet block to preserve and inspect
- `header_row`: the worksheet row containing that table's header
- `row_count` and `column_count`: coarse shape evidence
- `gid`, `worksheet_name`, and `source`: source lineage
- `engine`: confirm that the table is backed by `excelize`

Do not infer table boundaries from blank rows, visual spacing, or a worksheet-
wide sample when table metadata is available. The metadata range is the
boundary to use for the next readback or raw-surface mapping.

## Per-Table Inspection

For every table returned by `list-table`, inspect metadata and sample/read the
same `table_id` independently:

```bash
mbs excel-table metadata \
  --doc-id <DOC_ID> \
  --worksheet-name '<WORKSHEET_NAME>' \
  --table-id <TABLE_ID> \
  --output json

mbs excel-table sample \
  --doc-id <DOC_ID> \
  --worksheet-name '<WORKSHEET_NAME>' \
  --table-id <TABLE_ID> \
  --limit 20 \
  --output json
```

If a raw surface is required, use the metadata `range_address` for that table
only. Retain the source worksheet, `gid`, `table_id`, table name, range, header
row, and imported source document id in the import manifest. Create separate
raw surfaces when the downstream contract treats the blocks as separate
datasets; never concatenate unrelated table blocks solely because they share a
worksheet.

## Worked Shape

For a worksheet named `T14_财务规划引导`, a table inventory can identify two
independent blocks:

| table_id | range_address | header_row | data shape |
| --- | --- | ---: | --- |
| `46` | `A4:H11` | `4` | 8 columns, 7 reported rows |
| `47` | `A13:H18` | `13` | 8 columns, 5 reported rows |

The corresponding metadata lookup for the first block is:

```bash
mbs excel-table metadata \
  --doc-id <DOC_ID> \
  --worksheet-name 'T14_财务规划引导' \
  --table-id 46 \
  --output json
```

The second block must be looked up with `--table-id 47`; do not reuse `46` or
assume that the first table's range extends through the second block. Table ids
and ranges are runtime values, so always use the current `list-table` response
for the source workbook.

## Evidence Requirements

Store the following readbacks for each discovered table:

1. The complete `excel-worksheet list-table` response.
2. One `excel-table metadata` response per `table_id`.
3. One bounded `excel-table sample` or range read per table.
4. The raw-surface mapping showing the source range and table identity.

The multi-table case passes intake only when every selected table is either
mapped to a raw surface or explicitly recorded as skipped with an owner,
reason, and impact. A successful worksheet import by itself is insufficient
evidence that every table block was captured.
