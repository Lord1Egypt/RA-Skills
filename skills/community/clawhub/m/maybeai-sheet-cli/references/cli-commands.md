# CLI Command Reference

Use this as the primary execution catalog. Prefer these commands over raw HTTP.

Install: `pip install maybeai-sheet-cli`

Required env: `MAYBEAI_API_TOKEN`

## Contents

- Shared options
- Workbook commands
- Sheet read commands
- Sheet write commands
- Raw escape hatch
- Output modes
- Help discovery

## Shared options

These flags work at the root, on `workbook` / `sheet`, or on the leaf command:

| Flag | Purpose |
|------|---------|
| `--token` | API token (defaults to `MAYBEAI_API_TOKEN`) |
| `--base-url` | API base (default `https://play-be.omnimcp.ai`) |
| `--doc-id` | Workbook document ID |
| `--url` | MaybeAI workbook URL (parses doc id + gid when possible) |
| `--uri` | Fully resolved workbook URI |
| `--gid` | Worksheet gid |
| `--worksheet-name` | Worksheet name |
| `--output` | `json` (default), `table`, or `yaml` |
| `--verbose` | Extra resolution details |
| `--timeout` | HTTP timeout in seconds |

Always pass a leaf subcommand. `maybeai-sheet sheet --doc-id <id>` alone is invalid.

## Workbook commands

```bash
# Create empty workbook
maybeai-sheet workbook create --title "Board Pack"

# Upload local .xlsx
maybeai-sheet workbook create-from-file ./report.xlsx

# Inspect workbook structure and capabilities
maybeai-sheet workbook manifest --doc-id <DOC_ID>
maybeai-sheet workbook capabilities --doc-id <DOC_ID>
```

## Sheet read commands

```bash
# Full sheet (table view for humans)
maybeai-sheet sheet read --doc-id <DOC_ID> --gid <GID> --output table

# Full sheet (JSON for automation)
maybeai-sheet sheet read --doc-id <DOC_ID> --worksheet-name <SHEET>

# Range
maybeai-sheet sheet read-range --doc-id <DOC_ID> --gid <GID> --range A1:G20 --output table

# Multiple ranges (JSON file: [{worksheet_name?, range_address}, ...])
maybeai-sheet sheet read-many --doc-id <DOC_ID> --targets targets.json

# Named range
maybeai-sheet sheet named-range --doc-id <DOC_ID> --name RevenueBlock

# Headers only
maybeai-sheet sheet headers --doc-id <DOC_ID> --gid <GID> --output table

# Worksheet list
maybeai-sheet sheet worksheets --doc-id <DOC_ID> --output table

# Formulas in a range
maybeai-sheet sheet formulas --doc-id <DOC_ID> --worksheet-name <SHEET> --range A1:E20
```

## Sheet write commands

```bash
# Write a range (values.json: 2D array or row objects)
maybeai-sheet sheet write-range --doc-id <DOC_ID> --worksheet-name <SHEET> \
  --range A1:C3 --values values.json --verify

# Clear a range
maybeai-sheet sheet clear-range --doc-id <DOC_ID> --gid <GID> --range D1:F10

# Append rows (rows.json: list of row objects)
maybeai-sheet sheet append --doc-id <DOC_ID> --gid <GID> --rows rows.json --verify

# Upsert by key column
maybeai-sheet sheet upsert --doc-id <DOC_ID> --gid <GID> --key order_id --rows rows.json --verify

# Create worksheet
maybeai-sheet sheet create-worksheet --doc-id <DOC_ID> --name Summary

# Set one formula
maybeai-sheet sheet formula-set --doc-id <DOC_ID> --worksheet-name <SHEET> \
  --cell E2 --formula '=SUM(B2:D2)'

# Batch formulas (ops.json)
maybeai-sheet sheet formula-batch-set --doc-id <DOC_ID> --operations ops.json \
  --recalculate-mode worksheet

# Recalculate
maybeai-sheet sheet recalculate --doc-id <DOC_ID> --worksheet-name <SHEET>
```

## Raw escape hatch

For endpoints not yet wrapped as first-class commands (workbook profile, lineage trace, SQL, charts, formatting, file search/export, sharing):

```bash
maybeai-sheet raw post /api/v3/excel/formula/lineage_trace --body body.json
maybeai-sheet raw post /api/v1/excel/workbook_profile --body body.json
maybeai-sheet raw post /api/v1/excel/sql/compile --body body.json
```

Write the smallest possible JSON body file, call once, verify with a read command.

## Output modes

- `--output table` — aligned grid from tabular reads (like pandas/polars); omits styles/formulas metadata
- `--output json` — full CLI envelope with `success`, `endpoint`, `target`, `result`
- `--output yaml` — same payload as JSON in YAML form

## Help discovery

```bash
maybeai-sheet --help
maybeai-sheet sheet --help
maybeai-sheet sheet read --help
```
