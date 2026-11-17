
## How to Typical MaybeSheet Worksheet Creation

For this skill, the accepted `cost_monthly` Gold output is a PG/db-table created
through `stage-03-silver2gold.md`. An Excelize worksheet may be created later as
an optional workbook-facing presentation pivot, but it does not replace the
required Gold db-table.

Reference the MaybeSheet CLI skill docs before changing command shapes:

- `../../../mcp/maybeai-sheet-cli-skill/references/read-write.md`
- `../../../mcp/maybeai-sheet-cli-skill/references/formulas-sql.md`
- `../../../mcp/maybeai-sheet-cli-skill/references/file-management.md`

### PG/db-table engine

Use this path for accepted Gold tables and other SQL-backed handoff tables:

```bash
mbs db-table create-from-query --doc-id <DOC_ID> --name cost_monthly --sql-file <GOLD_SQL_FILE> --if-exists adopt --verify --output json
mbs db-table range set-formula --doc-id <DOC_ID> --name cost_monthly --cell A1 --formula '=SQL("<GOLD_SQL_ESCAPED>")' --output json
mbs formula read --doc-id <DOC_ID> --worksheet-name cost_monthly --range A1 --output json
mbs db-table schema --doc-id <DOC_ID> --name cost_monthly --output json
mbs db-table sample --doc-id <DOC_ID> --name cost_monthly --limit 20 --output json
mbs db-table read --doc-id <DOC_ID> --name cost_monthly --limit 100 --output json
```

### Excelize/excel engine

Use this path only for optional workbook-facing presentation worksheets,
reports, charts, images, merged cells, styles, or visible cell formulas after
the required Gold db-table exists:

```bash
mbs excel-worksheet create --doc-id <DOC_ID> --name <REPORT_WORKSHEET> --output json
mbs excel-worksheet range write --doc-id <DOC_ID> --worksheet-name <REPORT_WORKSHEET> --range A1:D20 --values <VALUES_JSON> --verify --output json
mbs excel-worksheet range set-formula --doc-id <DOC_ID> --worksheet-name <REPORT_WORKSHEET> --cell E2 --formula '=<FORMULA>' --output json
mbs excel-worksheet calculate --doc-id <DOC_ID> --worksheet-name <REPORT_WORKSHEET> --output json
mbs formula read --doc-id <DOC_ID> --worksheet-name <REPORT_WORKSHEET> --range E2 --output json
mbs excel-worksheet check-error --doc-id <DOC_ID> --worksheet-name <REPORT_WORKSHEET> --output json
```


