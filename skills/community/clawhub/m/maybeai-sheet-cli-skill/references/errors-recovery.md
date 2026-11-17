# Errors and Recovery Reference

## Contents

1. When to use this
2. Auth failures
3. Wrote to the wrong worksheet
4. Styles did not apply
5. SQL compile failures
6. Formula or spill result shows worksheet errors
7. Upload returned incomplete data
8. Local backend mismatch
9. Raw API body mistakes
10. Dashboard chart write ambiguity
11. Pre-delivery verification
12. Full refresh changed numeric-string precision

## 1. When to use this

Read this document when a task fails, writes to the wrong place, ignores styles, fails SQL compilation, or returns incomplete upload metadata.

## 2. Auth failures

Common symptoms:

- `401`
- `403`
- the file can be previewed but API calls fail

Checks:

1. Confirm `MAYBEAI_API_TOKEN` is set
2. Confirm the command is running in the shell where the token is set
3. Confirm the target workbook is accessible to that account

Recovery:

- reset the token
- use `mbs file list` or `mbs workbook list-worksheets` as a minimal auth test

## 3. Wrote to the wrong worksheet

This is the most common failure.

Causes:

- `worksheet_name` was omitted
- a legacy command needed `--gid` but only a bare workbook target was passed
- the caller assumed the CLI would remember the prior worksheet selection

Recovery:

1. `mbs workbook list-worksheets`
2. confirm the target sheet name and gid
3. rerun with explicit `--worksheet-name` or `--gid`
4. `mbs excel-worksheet range read` to confirm

## 4. Styles did not apply

Common symptoms:

- the request succeeded but nothing changed visually
- the response includes `source_info.styles_ignored=true`

Recovery:

1. do not claim the style change succeeded
2. explicitly tell the user the current engine ignored styles
3. if the task requires strong visual formatting, switch to a workbook or engine that supports it

## 5. SQL compile failures

Common causes:

- misspelled column names
- worksheet names not wrapped in double quotes
- SQL dialect is too exotic or outside the current conservative PG worksheet SQL subset
- `WITH` or a more complex structure is rejected by the backend

Recovery:

1. `mbs excel-table schema` or `mbs db-table schema`
2. optionally use a small `mbs excel-worksheet range read`
3. rewrite the query toward the conservative PG worksheet SQL subset
4. compile first, then write the SQL result

## 6. Formula or spill result shows worksheet errors

Common symptoms:

- `#VALUE!`
- `#REF!`
- `#DIV/0!`
- the formula is present but the readback value is empty or missing

Recovery:

1. `mbs excel-worksheet check-error --doc-id <DOC_ID> --worksheet-name <SHEET>`
2. if the formula text itself may be wrong, inspect it with `mbs formula read`
3. rerun `mbs excel-worksheet calculate` or `mbs workbook calculate` when the workbook should recache results
4. read the affected range with `mbs excel-worksheet read --output table`
5. if the error came from `=SQL(...)`, validate headers with `mbs excel-table schema` or `mbs db-table schema` and simplify the SQL

Do not claim a report or model worksheet is healthy based only on a successful
formula write; verify the result range is free of worksheet errors.

## 7. Upload returned incomplete data

Common symptoms:

- upload succeeded but `document_id` is missing
- only `uri` is returned
- local file path was wrong

Recovery:

1. parse `document_id` from `uri`
2. if the local file is missing, fix the path first
3. retry with `mbs workbook import ./file.xlsx`

## 8. Local backend mismatch

Common symptoms:

- local source changes do not affect `mbs` output
- `excel-worksheet list-table --gid <GID>` returns one whole-sheet range instead of multiple content-backed table ranges
- response looks like production even though a local service is running

Checks:

1. Use local `play-be`, not the chat frontend: `http://localhost:7011`
2. Prefer `mbs --base-url http://localhost:7011 ...` when debugging base-url confusion
3. With current CLI versions, `MAYBEAI_BASE_URL=http://localhost:7011 mbs ...` is equivalent
4. If direct `excelize-mcp` on `http://localhost:8080/api` is correct but `mbs` is not, restart `play-be` and check its `EXCELIZE_MCP_URL`

## 9. Raw API body mistakes

Common symptom:

- `Invalid value for '--body': Path '{...}' does not exist.`

Recovery:

1. Prefer a first-class `mbs` command when one exists.
2. For inline JSON, use `mbs raw post <PATH> --json '{"a":"b"}'`.
3. For file-backed JSON, write a body file and pass `--body body.json`.

Do not pass inline JSON to `--body`.

## 10. Dashboard chart write ambiguity

Common symptoms:

- `Missing option '--cell'`
- payload shows nested `chart.chart`
- dashboard batch refresh/create-config returns a server-side error
- chart ids are returned but the browser canvas is not visually verified

Recovery:

1. Run `mbs excel-worksheet dashboard validate --spec dashboard.json`.
2. Run `mbs excel-worksheet dashboard refresh --doc-id <DOC_ID> --spec dashboard.json --dry-run`.
3. Confirm dashboard operations use `charts: [{cell, chart}]`.
4. For single-chart writes, use `chart create-config --cell <CELL> --spec chart.json`, or put `cell` at spec top level.
5. If batch still fails, split into one chart spec per chart and call `chart create-config` per cell.
6. Treat `chart_id`, `dashboard manifest`, and `chart list` as persistence checks only; use data readback and browser canvas verification when possible.

## 11. Pre-delivery verification

Minimum verification standard:

- `mbs workbook list-worksheets`
- `mbs excel-worksheet range read` or table sample on the key output range
- `mbs excel-worksheet check-error` on formula or report-result worksheets
- optionally `mbs file export`

Do not skip verification after:

- SQL result writes
- formula writes or workbook recalculation
- range/table writes
- legacy `mbs sheet upsert`
- creating or deleting worksheets
- chart, picture, or style adjustments

## 12. Full refresh changed numeric-string precision

Common symptom:

- `sheet update-data-keep-headers` succeeds, but a long numeric-looking string
  such as `"46215.95520833333"` reads back as `"46215.95521"`

Cause:

- the backend parses numeric-looking strings as Excel values during this
  full-refresh operation, and Excel display/readback normalizes precision

Recovery:

1. Compare the source JSON and bounded readback by field, not only HTTP status.
2. If the field is conceptually numeric or an Excel date serial, accept the
   normalized value and document the conversion.
3. If exact text is required, do not use the full-refresh command for that
   field; write an exact bounded range through the RAW range-write path.
4. Re-read the affected cells and confirm no column misalignment occurred.
