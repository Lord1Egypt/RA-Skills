# Read/Write Reference

## 1. Select the model from the runtime CLI and target metadata

```bash
mbs --help
mbs workbook inspect --target "$WORKBOOK"
mbs worksheet list --target "$WORKBOOK" --output json
```

Use Sheet targets for A1 ranges, worksheet layout, and cell formulas. Use Base
table targets (`?tid=...`) for typed records and Base fields. A worksheet name
or `gid` is a locator, not proof that an operation is supported.

## 2. Read before writing

```bash
mbs range inspect --target "$SHEET" --range A1:Z100
mbs range read --target "$SHEET" --range A1:D20 --output table
mbs table inspect --target "$BASE_TABLE"
mbs table schema --target "$BASE_TABLE"
mbs table sample --target "$BASE_TABLE" --limit 20 --output table
```

For an unfamiliar task, also run the relevant parent and command help. Do not
use a compatibility command merely because a remembered example contains it.

For a complete table export, use `table read --all --frame-out`; a plain
`table read` is a single bounded page and currently defaults to 1000 records.
The CLI follows cursors or `has_more` offset pages, and refuses a full page
without continuation metadata rather than silently truncate. See
[cli-commands.md](cli-commands.md) for the export command and failure rules.

## 3. Write a Sheet safely

```bash
mbs range write --target "$SHEET" --range A1:C3 --values values.json --verify
mbs range clear --target "$SHEET" --range A2:C100 --verify
mbs range merge --target "$SHEET" --range A1:C1 --verify
mbs range unmerge --target "$SHEET" --range A1:C1 --verify
mbs range style --target "$SHEET" --range A1:C3 --spec range-style.json --verify
mbs formula set --target "$SHEET" --range E2:E100 --expression '=SUM(B2:D2)' --verify
mbs range note set --target "$SHEET" --range B2 --text "Reviewed" --verify
```

Use `range note read|set|clear` for Sheet notes. `set` and `clear` currently
require a single A1 cell. Reconcile Sheet key-based data locally before a range
write; the public CLI does not expose a generic Sheet key-merge operation.

## 4. Write Base records safely

```bash
mbs table insert --target "$BASE_TABLE" --frame-in rows.json --verify
mbs table update --target "$BASE_TABLE" --frame-in corrected_rows.json --key order_id --verify
mbs row insert --target "$BASE_TABLE" --records records.json --verify
mbs row delete --target "$BASE_TABLE" --record-id <RECORD_ID> --verify
```

Do not claim that public insert/update commands preserve whole-table replacement
semantics. If the request requires an atomic replace, deletion of missing
records, or identity preservation, pause and report the public capability gap.

Use `column insert` and `column rename` for individual exposed Base schema
changes. Treat `column config --spec` as a style operation. For an in-place
batch update of existing Base field metadata, use public `column batch-update
--updates` after checking its runtime help; it does not provide whole-schema
replacement, deletion, or migration semantics.

When converting a current Base Formula field to an ordinary type, include the
explicit per-field conversion instruction in the updates file:

```json
[
  {
    "field_id": "col_formula",
    "logical_type": "text",
    "formula_conversion": "materialize"
  }
]
```

Run the public command with `--dry-run` first, then execute with `--verify`:

```bash
mbs column batch-update --target "$BASE_TABLE" \
  --updates formula-to-text.json --dry-run
mbs column batch-update --target "$BASE_TABLE" \
  --updates formula-to-text.json --verify
```

`formula_conversion` is an operation instruction, not a field property that
should be inferred or expected in readback. Use it only for an intentional
Formula-to-ordinary-type conversion; verify the resulting type and values.

## 5. SQL Config and Base materialization

```bash
mbs sql preview --target "$WORKBOOK?table=Sheet6" --sql-file result.sql --output table
mbs sql materialize \
  --target "$WORKBOOK?table=S_orders" \
  --sql-file result.sql \
  --mode create \
  --schema schema.json \
  --verify
```

Use `sql materialize` for a public Base-table result. For a Worksheet SQL Config
result, check `mbs sql --help` and selected command help before using `sql
config` or `sql overwrite`.

`sql query` and `sql preview` may select a worksheet through
`--target "$WORKBOOK?table=<WORKSHEET_NAME>"`; the CLI resolves the selector and
still performs a workbook SQL request. These operations do not accept a
Base-table `tid` target.

The response operation for every public `table create` source is
`table.create`, including frame, SQL-query, and worksheet-range creation.

## 6. Verification

- Use `--dry-run` before a destructive or unfamiliar mutation.
- Preserve `--expected-revision` and `--idempotency-key` when supplied.
- Use `--verify` where available.
- Read back the exact range, rows, table schema, Formula state, or materialized
  result that the task changed.
- Treat `written_unverified` as incomplete until the relevant readback matches.
