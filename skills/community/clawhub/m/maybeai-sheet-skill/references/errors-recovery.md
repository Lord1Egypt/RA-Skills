# Errors and Recovery Reference

## Contents

1. When to use this
2. Auth failures
3. Wrote to the wrong worksheet
4. Styles did not apply
5. SQL compile failures
6. Upload returned incomplete data
7. Pre-delivery verification

## 1. When to use this

Read this document when a task fails, writes to the wrong place, ignores styles, fails SQL compilation, or returns incomplete upload metadata.

## 2. Auth failures

Common symptoms:

- `401`
- `403`
- the file can be previewed but API calls fail

Checks:

1. Confirm `MAYBEAI_API_TOKEN` is set
2. Confirm the request includes `Authorization: Bearer <token>`
3. Confirm the endpoint actually requires auth

Recovery:

- reset the token
- use `list_files` or `list_worksheets` as a minimal auth test

## 3. Wrote to the wrong worksheet

This is the most common failure.

Causes:

- `worksheet_name` was omitted
- the endpoint required `?gid=` but only a bare `uri` was passed
- the caller assumed the backend would remember the prior worksheet selection

Recovery:

1. `list_worksheets`
2. confirm the target sheet name and gid
3. rewrite the request with explicit `worksheet_name` or `uri?gid=N`
4. `read_sheet` to confirm

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

1. `read_headers`
2. optionally use a small `read_sheet`
3. rewrite the query toward the conservative PG worksheet SQL subset
4. `sql/compile` first, then `sql/write_result`

## 6. Upload returned incomplete data

Common symptoms:

- upload succeeded but `document_id` is missing
- only `uri` is returned
- local file path was wrong

Recovery:

1. parse `document_id` from `uri`
2. if the local file is missing, fix `EXCEL_FILE_PATH` first
3. reproduce with the upload flow from `scripts/01-file-management.sh`

## 7. Pre-delivery verification

Minimum verification standard:

- `list_worksheets`
- `read_sheet` on the key output range
- optionally `export`

Do not skip verification after:

- `sql/write_result`
- `update_data_keep_headers`
- `update_range_by_lookup`
- creating or deleting worksheets
- chart, picture, or style adjustments
