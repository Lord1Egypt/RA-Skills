# Errors and Recovery Reference

## Contents

1. When to use this
2. Auth failures
3. Wrote to the wrong worksheet
4. Styles did not apply
5. SQL compile failures
6. Sheet table insert verifies values but reports a revision gap
7. Formula or spill result shows worksheet errors
8. Upload returned incomplete data
9. Local backend mismatch
10. Raw API body mistakes
11. Dashboard chart write ambiguity
12. Pre-delivery verification
13. Full refresh changed numeric-string precision
14. Full refresh returned `written_unverified`
15. Required worksheet identity changed

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
- use `mbs file list`, `mbs workbook inspect`, or `mbs worksheet list` as a minimal auth test

## 3. Wrote to the wrong worksheet

This is the most common failure.

Causes:

- `worksheet_name` was omitted
- a legacy command needed `--gid` but only a bare workbook target was passed
- the caller assumed the CLI would remember the prior worksheet selection

Recovery:

1. `mbs workbook inspect` and `mbs worksheet list`
2. confirm the target sheet name and gid
3. rerun with explicit `--worksheet-name` or `--gid`
4. `mbs range read` to confirm

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
- SQL dialect is too exotic or outside the current conservative Base worksheet SQL subset
- `WITH` or a more complex structure is rejected by the backend

Recovery:

1. `mbs table schema` or `mbs table schema --table-id <TABLE_ID>`
2. optionally use a small `mbs range read`
3. rewrite the query toward the conservative Base worksheet SQL subset
4. compile first, then write the SQL result

## 6. Sheet table insert verifies values but reports a revision gap

Common symptoms:

- `mbs table insert --target ...?gid=<GID>&tid=<TABLE_ID> --verify` writes rows
  that are visible on a subsequent range/table read.
- The command still exits nonzero because persistent table metadata did not
  advance the expected version (`revision_advanced` or a related verification
  error).

Recovery:

1. Do not immediately retry; a retry can duplicate the inserted rows.
2. Read the bounded inserted range or `mbs table read` and compare every
   submitted row.
3. Re-run `mbs table list --doc-id <DOC_ID> --gid <GID>` or persistent metadata
   only to observe table identity/range, not as the sole proof of the write.
4. If values match, report the mutation as applied with a verification warning;
   if they do not, reconcile from the readback before retrying.

## 7. Formula or spill result shows worksheet errors

Common symptoms:

- `#VALUE!`
- `#REF!`
- `#DIV/0!`
- the formula is present but the readback value is empty or missing

Recovery:

1. `mbs range inspect --doc-id <DOC_ID> --worksheet-name <SHEET>`
2. if the formula text itself may be wrong, inspect it with `mbs formula read`
3. rerun `mbs formula recalculate` or `mbs workbook calculate` when the workbook should recache results
4. read the affected range with `mbs range read --output table`
5. if the error came from a legacy `=SQL(...)` cell, validate headers with `mbs table schema` or `mbs table schema --table-id <TABLE_ID>` and simplify the SQL

Do not claim a report or model worksheet is healthy based only on a successful
formula write; verify the result range is free of worksheet errors.

## 8. Upload returned incomplete data

Common symptoms:

- upload succeeded but `document_id` is missing
- only `uri` is returned
- local file path was wrong

Recovery:

1. parse `document_id` from `uri`
2. if the local file is missing, fix the path first
3. retry with `mbs workbook import ./file.xlsx`

## 9. Local backend mismatch

Common symptoms:

- local source changes do not affect `mbs` output
- `table list --gid <GID>` returns one whole-sheet range instead of multiple content-backed table ranges
- response looks like production even though a local service is running

Checks:

1. Use local `play-be`, not the chat frontend: `http://localhost:7011`
2. Prefer `mbs --base-url http://localhost:7011 ...` when debugging base-url confusion
3. With current CLI versions, `MAYBEAI_BASE_URL=http://localhost:7011 mbs ...` is equivalent
4. If direct `excelize-mcp` on `http://localhost:8080/api` is correct but `mbs` is not, restart `play-be` and check its `EXCELIZE_MCP_URL`

## 10. Raw API body mistakes

Common symptom:

- `Invalid value for '--body': Path '{...}' does not exist.`

Recovery:

1. Prefer a first-class `mbs` command when one exists.
2. For inline JSON, use `mbs raw post <PATH> --json '{"a":"b"}'`.
3. For file-backed JSON, write a body file and pass `--body body.json`.

Do not pass inline JSON to `--body`.

## 11. Dashboard chart write ambiguity

Common symptoms:

- `Missing option '--cell'`
- payload shows nested `chart.chart`
- dashboard batch refresh/create-config returns a server-side error
- chart ids are returned but the browser canvas is not visually verified

Recovery:

1. Run `mbs dashboard validate --spec dashboard.json`.
2. Run `mbs dashboard refresh --doc-id <DOC_ID> --spec dashboard.json --dry-run`.
3. Confirm dashboard operations use `charts: [{cell, chart}]`.
4. For single-chart writes, use `chart create-config --cell <CELL> --spec chart.json`, or put `cell` at spec top level.
5. If batch still fails, split into one chart spec per chart and call `chart create-config` per cell.
6. Treat `chart_id`, `dashboard manifest`, and `chart list` as persistence checks only; use data readback and browser canvas verification when possible.

## 12. Pre-delivery verification

Minimum verification standard:

- `mbs workbook inspect` and `mbs worksheet list`
- `mbs range read` or table sample on the key output range
- `mbs range inspect` on formula or report-result worksheets
- optionally `mbs workbook export --doc-id <DOC_ID> --out workbook.xlsx`

Do not skip verification after:

- SQL result writes
- formula writes or workbook recalculation
- range/table writes
- `mbs table update`
- creating or deleting worksheets
- chart, picture, or style adjustments

## 13. Full refresh changed numeric-string precision

Common symptom:

- a full refresh succeeds, but a long numeric-looking string
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

## 14. Full refresh returned `written_unverified`

Common symptoms:

- `mbs worksheet import ... --strategy replace --verify` exits nonzero
- stdout includes `written_unverified` or `verify failed`
- the response has `error: null`

This is an indeterminate verification result, not proof that the write failed.
Do not say the online sheet remains unchanged, set the task to `BLOCKED`, or
ask the user to select a recovery path until live values have been compared.

Recovery:

1. Read the refreshed footprint or, for a large sheet, header row plus known
   changed sentinels and the previous last row. Do not inspect only an unrelated
   prefix such as `A1:F5` when the claimed change is elsewhere.
2. Compare live cells with source JSON by header. Use exact comparison for text
   and a documented tolerance for Excel-normalized numeric/date values.
3. A changed entity/service set does not by itself change the JSON key set when
   keys are date-column headers; do not use that as a failure explanation.
4. If values match, report success with the CLI verification warning. If they
   differ, automatically use range clear + range write when it preserves the
   required worksheet behavior. When the user required the original worksheet,
   snapshot the latest history entry and formula cells first, then re-read that
   history entry immediately before fallback. Stop the automatic fallback when
   it changed, collaborators are actively editing, or a schema change alters
   formula semantics; the CLI has no lock/revision precondition and must not
   overwrite those changes. Otherwise pass
   `--gid <RECORDED_GID>` to every range mutation, calculate, and error check;
   do not delete, recreate, copy, import, or rename-swap worksheets. Exclude
   formula cells from raw clear/write. For a changed header/schema, clear and
   write the owned value/header ranges from `A1`, including the new header row;
   use `A2` only when headers are unchanged. Recalculate and scan formula
   results for errors before reporting success.

## 15. Required worksheet identity changed

Common symptoms:

- the target worksheet has the same name after a refresh, but a different `gid`
- a recovery deleted, recreated, copied, imported, or rename-swapped a sheet
- a user asked to overwrite the original data or not to create another sheet

This is a failed outcome even when the visible data looks correct. A worksheet
name is not its identity.

Recovery:

1. Before a write, record the target name and `gid` with `mbs workbook inspect` and `mbs worksheet list`.
2. For full refreshes, prefer `worksheet import --strategy replace`; when that
   is unsuitable, use `range clear` and `range write` on the
   same recorded worksheet. Before each range mutation, confirm the target name
   still maps to the recorded `gid` and pass `--gid <RECORDED_GID>`; for a
   header/schema change, cover the owned value/header range beginning at `A1`.
3. Run `workbook inspect` and `worksheet list` after the write. Report success
   only when the original name still maps to the recorded `gid`.
