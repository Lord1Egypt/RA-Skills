---
name: error-handling
description: Error codes and recovery actions for the anomaly detection workflow.
---

## Error Handling Reference

### Precondition Errors

| Error | Cause | Recovery |
|-------|-------|----------|
| `SCRIPT_NOT_FOUND` | `scripts/kwdb_sql_execute.py` not available in skill directory | Stop permanently; inform user that the SQL execution script is missing. |
| `CONNECTION_FAILED` | Database connection test failed (host unreachable, port incorrect, authentication error, etc.) | Stop permanently; inform user of the exact failure reason. Do **NOT** retry with alternative parameters or attempt other connection methods. |
| `CONNECTION_PARAMS_MISSING` | User did not provide one or more required connection parameters (host, port, username, password) | Ask the user to supply all missing values. Do **NOT** guess or use default values. |
| `MISSING_TABLE_COLUMN` | User did not specify target | Query metadata → present options → wait for input. |
| `DB_NOT_FOUND` / `TABLE_NOT_FOUND` / `COLUMN_NOT_FOUND` | Invalid name given | Stop permanently; list closest matches if available. |

### Validation Errors

| Error | Cause | Recovery |
|-------|-------|----------|
| `NOT_TS_DATABASE` | Target database is not TIME SERIES | Stop permanently; suggest using a TS database. |
| `NO_NUMERIC_COLUMNS` | All filtered columns are non-numeric | Stop permanently; show numeric columns from metadata. |
| `EMPTY_RESULT_SET` | Single Tag: SQL returned zero rows | Stop permanently; suggest widening time range. |
| `EMPTY_PRIMARY_TAG_LIST` | All Tags: `SELECT DISTINCT <primary_tag>` returned zero values | Stop permanently; table may have no primary tags configured. |
| `ALL_TAGS_EMPTY_RESULT` | All Tags: every primary tag value yields an empty result set | Stop permanently; suggest checking table data or time filter. |

### Detection Errors

| Error | Cause | Recovery |
|-------|-------|----------|
| `INSUFFICIENT_DATA` | Fewer than `2*period+1` points for STL | Report to user; suggest lowering period or collecting more data. |
| `JSON_PARSE_ERROR` | Script input is malformed | Check `/tmp/sql-result*` or `/tmp/sql-result-<tag>*` file encoding and schema. |
| `PERIOD_INFERENCE_FAILED` | Timestamps are irregular or missing | Fall back to `period=7` and warn user in report. |

### Report Generation Errors

| Error | Cause | Recovery |
|-------|-------|----------|
| `PDF_GENERATION_FAILED` | Missing `wkhtmltopdf` or similar | Fall back to Markdown output. |
| `HTML_TEMPLATE_MISSING` | `references/report-template-html.md` unreadable | Fall back to Markdown output. |