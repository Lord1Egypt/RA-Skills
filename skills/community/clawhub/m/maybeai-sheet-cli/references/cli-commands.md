# CLI Command Reference

## Runtime discovery is the command contract

Do not copy a static command tree from this skill. The installed CLI is the
source of truth for public commands and flags:

```bash
mbs --help
mbs <group> --help
mbs <group> <command> --help
```

Generate only commands listed by their parent `--help`. A directly callable
command that is absent from parent help is a hidden compatibility surface; do
not probe, recommend, or generate it for new work.

## Discover and identify the target

```bash
mbs workbook inspect --target "$WORKBOOK"
mbs worksheet list --target "$WORKBOOK" --output json
mbs table list --doc-id <DOC_ID> --output json
```

Use a Sheet target with `gid` for A1 range/cell work. Use a persistent `tid`
(and field or record IDs when required) for Base work. Do not infer the engine
from a worksheet name or visual appearance.

## Public operational patterns

### Read and inspect

```bash
mbs range inspect --target "$SHEET" --range A1:Z100
mbs range read --target "$SHEET" --range A1:D20 --output table
mbs table schema --target "$BASE_TABLE"
mbs table read --target "$BASE_TABLE" --limit 100 --output table
mbs table read --target "$BASE_TABLE" --all --order-by order_id --frame-out /tmp/orders.parquet
```

#### Complete table exports and pagination

`table read` currently defaults to 1000 records per request and accepts at
most 5000. Without `--all`, it performs exactly one bounded read, even if the
response says more records exist. Use a smaller explicit `--limit` for a
preview; use a frame for a complete result:

```bash
mbs table read \
  --target "$BASE_TABLE" \
  --all \
  --order-by order_id \
  --frame-out /tmp/orders.parquet \
  --output json
```

`--frame-out` requires `--all`. The CLI collects every page, then writes one
complete `.parquet`, `.csv`, or `.json` frame; it does not leave a partial
frame when pagination fails. It follows `next_cursor` / `nextCursor`. When a
backend instead returns `has_more: true` without a cursor, it requests the
next page with `offset += records_returned`. `has_more: false`, a reached
declared total, or an explicit completion marker ends the read.

Never infer completion from the number of returned rows. If a page fills the
requested limit but has no cursor, `has_more`, total, or completion marker,
the CLI exits with `backend.pagination_contract` rather than silently export a
truncated result. Repeated cursors, an empty page with `has_more: true`, and a
declared total larger than the rows received also fail. `--order-by` is a
backend capability: if the target cannot honor it, the CLI returns a capability
error instead of sorting locally. Complete reads do not pin a table snapshot;
avoid concurrent writes when an exact point-in-time export is required.

### Write table records

```bash
mbs table insert --target "$BASE_TABLE" --frame-in rows.json --verify
mbs table update \
  --target "$BASE_TABLE" \
  --frame-in corrected_rows.json \
  --key order_id \
  --expected-revision <REVISION> \
  --verify
```

`table clear` removes all Base records while preserving fields/schema and
requires explicit `--yes` (or `--dry-run`). `table insert` and `table update`
are not an automatic replacement for an atomic whole-table replacement operation. If the request requires deleting
missing records, preserving identities, or atomic replacement semantics, state
the capability gap and obtain an explicit product/API decision before composing
destructive calls.

### Write Sheet ranges, formulas, and notes

```bash
mbs range write --target "$SHEET" --range A1:C3 --values values.json --verify
mbs range style --target "$SHEET" --range B2:D4 --spec range-style.json --verify
mbs formula validate --target "$SHEET" --cell E2 --expression '=SUM(B2:D2)'
mbs formula set --target "$SHEET" --cell E2 --expression '=SUM(B2:D2)' --verify
mbs formula calculate --target "$SHEET" --cell E2 --save-result --verify
mbs range note read --target "$SHEET" --range B2:D4
mbs range note set --target "$SHEET" --range B2 --text "Reviewed" --verify
mbs range note clear --target "$SHEET" --range B2 --verify
```

Use `formula set` for formula writes and `range note read|set|clear` for Sheet
notes. Notes are not Base record notes. `range lineage` uses `--range`, not
`--cell`.

### Worksheet operations and styling

```bash
mbs worksheet calculate --target "$SHEET" --verify
mbs worksheet check-error --target "$SHEET" --range A1:Z100
mbs worksheet config --target "$SHEET" --spec worksheet-config.json --verify
# Default `--layout auto` detects a normal table or a pivot/report.
# Always inspect the plan before an unfamiliar styling mutation.
mbs worksheet beautify --target "$SHEET" --dry-run --output json
mbs worksheet beautify --target "$SHEET" --verify
mbs range merge --target "$SHEET" --range A1:C1 --verify
mbs range unmerge --target "$SHEET" --range A1:C1 --verify
```

`worksheet beautify` uses `--layout auto` when `--layout` is omitted. It
keeps **table** for ordinary column-oriented data, so a field such as `日期`
remains a date column. It selects **pivot** only after finding at least two
concrete horizontal members, such as `1店`/`2店`, `Store A`/`Store B`,
`Q1`/`Q2`, or `2025-01`/`2025-02`. Generic field names (`日期`, `门店`, `月份`,
`年度`) and a lone `合计`/`Total` do not count as pivot evidence. In a detected
pivot, the first column of the target range is the row-label area; it may hold
text labels or numeric codes. Its labels determine value-area formats row by
row: `毛利率` formats `B:E` as percent while `毛利-CNY` and `净利润-CNY` format
`B:E` as currency. The label header `利润项目` remains text; it must not be
classified as a currency value merely because it contains `利润`. Numeric row
labels default to number formatting unless a `rowLabelRules` rule overrides
that classification.

Auto detection currently treats only the **first column of the target range**
as the pivot row-label column. Choose a range with that shape, or use
`--layout pivot` for an intentional pivot whose members do not match the
structural patterns above; use `--layout table` to force field-by-column
formatting.

Before applying beautify to an unfamiliar worksheet, use dry-run and inspect
`result.plan.worksheets[0].layout_detection.selected`,
`layout_detection.reasons`, `row_semantics`, and `value_range` in the JSON
response. Override inference only when required:

```bash
mbs worksheet beautify --target "$SHEET" --layout pivot --verify --output json
mbs worksheet beautify --target "$SHEET" --layout table --verify --output json
```

A pivot label column automatically receives a wider minimum width. Set an
explicit width in the beautify policy when needed:

```json
{
  "columnWidths": {
    "byColumn": {"A": 24},
    "byHeader": {"利润项目": 24}
  }
}
```

Width precedence is `byColumn` > `byHeader` > automatic width. Supply this
policy through `mbs worksheet beautify --config beautify-policy.json`.

Run `mbs worksheet style --help` only when the task needs explicit worksheet
styling operations, then inspect the selected child with `--help`. Do not copy a
nested worksheet-style command list into this skill.

### Base fields and formulas

```bash
mbs column insert --target "$BASE_TABLE" --field new_status --field-type text --verify
mbs column rename --target "$BASE_TABLE" --field status --new-name Status --verify
mbs column config --target "$BASE_TABLE" --field amount --spec column-style.json --verify
mbs column batch-update --target "$BASE_TABLE" --updates base-field-updates.json --verify
mbs formula validate --target "$BASE_TABLE" --field gross_margin --expression 'revenue - cost'
mbs formula set --target "$BASE_TABLE" --field gross_margin --expression 'revenue - cost' --verify
mbs formula recalculate --target "$BASE_TABLE" --field gross_margin --verify
```

`column config` is a resource-style operation. For an in-place batch update of
existing Base field metadata, use public `column batch-update --updates` and
inspect its installed help for the accepted update-object contract. It does not
replace whole-schema migration: adding, deleting, or reordering fields may need
separate public column operations and has different atomicity/data-migration
semantics.

For a Formula-to-ordinary-type conversion, put the explicit conversion mode on
the affected update object:

```json
[
  {
    "field_id": "col_formula",
    "logical_type": "text",
    "formula_conversion": "materialize"
  }
]
```

```bash
mbs column batch-update \
  --target "$BASE_TABLE" \
  --updates formula-to-text.json \
  --dry-run
mbs column batch-update \
  --target "$BASE_TABLE" \
  --updates formula-to-text.json \
  --verify
```

The public command already accepts arbitrary JSON update objects and forwards
`formula_conversion` to the field batch-update API; no separate top-level CLI
flag is required. `materialize` is required only when changing a current
Formula field to an ordinary `logical_type`. It materializes the current
formula results and removes Formula metadata, so do not add it automatically
to rename, style, or ordinary type updates. Verification should assert the
resulting field type and values, not the presence of `formula_conversion` in
readback metadata.

### SQL materialization

```bash
mbs sql query --target "$WORKBOOK?table=Sheet6" --sql-file result.sql --all --frame-out /tmp/query.parquet
mbs sql preview --target "$WORKBOOK?table=Sheet6" --sql-file result.sql --output table
mbs sql materialize \
  --target "$WORKBOOK?table=S_orders" \
  --sql-file result.sql \
  --mode create \
  --schema schema.json \
  --verify
```

Use `sql materialize` for public Base-table materialization. Use `sql config`
and `sql overwrite` only when the current help and selected target show a
Worksheet SQL Config workflow. `sql query --all --frame-out` is read-only and
writes a complete local Parquet, CSV, or JSON frame; it does not modify the
workbook.

`sql query` and `sql preview` accept a workbook target with
`?table=<WORKSHEET_NAME>` to select the worksheet used by the query. The CLI
resolves the worksheet selector before issuing the workbook SQL request. Do
not replace this with a Base-table `?tid=<TABLE_ID>` target; SQL query and
preview require a workbook target.

The canonical response operation for every public `table create` source is
`table.create`, including frame, SQL-query, and worksheet-range sources. The
source-specific implementation path does not change the operation name in
the response envelope.

### Other public groups

For chart, pivot, dashboard, image, media, history, file, share, and raw work,
start with the relevant parent help and then inspect the selected operation's
flags. Use `mbs image`, not a worksheet image compatibility alias.

## Native Sorting

Use `range sort` for Sheet cells and `table sort` for a Base table view:

```bash
# Sort complete rows inside this rectangle, retaining the first row as headers.
mbs range sort --target "$SHEET" --range A1:D100 --by B:asc --by C:desc --dry-run
mbs range sort --target "$SHEET" --range A1:D100 --by B:asc --by C:desc

# Include the first row when the range contains no header.
mbs range sort --target "$SHEET" --range A2:D100 --by B:asc --no-header

# Save sort keys on a Base view while retaining its filters and field settings.
mbs table sort --doc-id "$DOC_ID" --table-id "$TABLE_ID" --by col_amount:desc
mbs table sort --doc-id "$DOC_ID" --table-id "$TABLE_ID" --view-id "$VIEW_ID" --clear
```

Repeat `--by` in priority order. Sheet keys are absolute column letters inside
the selected rectangle; Base keys are stable field IDs. Directions are `asc`
or `desc`. Sheet sorting is stable and places blanks last in either direction.
It runs on the server and preserves cell content and formatting; unsupported
cell structures are rejected before mutation. Base sorting changes the saved
view, not the underlying record order.

Sheet compatibility requires cached values for formula-valued sort keys.
Merged cells, cell comments/hyperlinks, and unsupported formula constructs
are rejected before mutation. Moved formulas retain absolute references and
translate relative ones. Formula result caches are invalidated for recalculation.
`range sort` reports verification as unavailable; `table sort` verifies saved
view settings by reading them back. If that read fails after saving, the command
reports the failure without repeating the write.

These commands require a CLI build containing native sorting. Sheet range
sorting additionally requires the matching SheetTable `sort_range` endpoint
and its API proxy route; older deployed servers do not provide that endpoint.

## Mutation safety

For mutations, use `--dry-run` before unfamiliar or destructive work, preserve
`--expected-revision` and `--idempotency-key` when the workflow needs them, and
verify with a target-appropriate readback. `--output table|yaml` changes
rendering only; it does not alter the command contract.
