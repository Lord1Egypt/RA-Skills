# Formulas and SQL Reference

## 1. Discover the supported operation at runtime

```bash
mbs formula --help
mbs formula set --help
mbs sql --help
```

Generate only commands listed by their parent help. Formula syntax and target
identity differ between Sheet and Base; do not translate expressions between
engines.

## 2. Sheet formulas

```bash
mbs formula validate --target "$SHEET" --cell E2 --expression '=SUM(B2:D2)'
mbs formula set --target "$SHEET" --cell E2 --expression '=SUM(B2:D2)' --verify
mbs formula set --target "$SHEET" --range E2:E100 --expression '=SUM(B2:D2)' --verify
mbs formula calculate --target "$SHEET" --cell E2 --save-result --verify
mbs formula recalculate --target "$SHEET" --verify
mbs formula lineage --target "$SHEET" --cell E2 --format tree --output yaml
```

Use `formula set` for public formula writes. Use `formula calculate` for a
selected expression/cell calculation and `formula recalculate` for worksheet or
workbook recalculation when the runtime help supports the chosen target.

## 3. Base Formula fields

```bash
mbs formula validate --target "$BASE_TABLE" --field gross_margin --expression 'revenue - cost'
mbs formula set --target "$BASE_TABLE" --field gross_margin --expression 'revenue - cost' --verify
mbs formula recalculate --target "$BASE_TABLE" --field gross_margin --verify
mbs formula lineage --target "$BASE_TABLE" --field gross_margin --format tree --output yaml
```

A Base Formula uses a field selector and the Base expression language. If the
public CLI cannot expose the requested normalization, compilation evidence, or
schema behavior, report the capability gap rather than invoking a hidden
compatibility command.

## 4. Worksheet SQL Config and materialization

```bash
mbs sql preview --target "$WORKBOOK?table=Sheet6" --sql-file result.sql --output table
mbs sql query --target "$WORKBOOK?table=Sheet6" --sql-file result.sql --limit 100 --output table
mbs sql materialize \
  --target "$WORKBOOK?table=S_orders" \
  --sql-file result.sql \
  --mode create \
  --schema schema.json \
  --verify
```

`sql materialize` is the public workflow for writing a SQL result into a Base
table. Its `--mode` changes semantics: use `create` for a new target and review
replacement behavior explicitly before any replacement mode. Use `--dry-run`,
`--verify`, and a readback of the materialized result.

For SQL query and preview, `?table=<WORKSHEET_NAME>` is a worksheet selector on
the workbook target. The CLI resolves it before making the workbook SQL
request; a Base-table `tid` target is not valid for these operations.

All public table-creation sources return the canonical operation
`table.create`. This includes creation from a local frame, SQL query, or
worksheet range; do not branch on source-specific operation names.

Use `sql config` and `sql overwrite` only for a Worksheet SQL Config target
when the installed command help supports the requested flow. Raw SQL remains a
separate computation model from Sheet and Base Formula expressions.

## 5. Formula and SQL safety

- Validate before persisting an unfamiliar formula.
- Keep Sheet formulas in Excel syntax and Base fields in the Base expression
  language.
- Preserve explicit revision/idempotency controls on writes.
- Do not generate removed nested cell-note commands or hidden formula aliases.
