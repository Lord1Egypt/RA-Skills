---
name: constraints
description: Critical constraints and forbidden behaviors for the anomaly detection skill.
---

## Critical Constraints (non-negotiable)

- Execute **all** SQL queries via `scripts/kwdb_sql_execute.py`. Do NOT use `kwdb-mcp-server` MCP tools (e.g., `read-query`, `write-query`) for any SQL execution.
- Metadata queries (database/table/column discovery, primary tag listing, column comment inspection) must **NOT** store results to file — omit the output file argument so results print to stdout only.
- For all metadata queries， you **MUST ONLY** use the exact SQL statements defined in `references/metadata-query.md`. **Never write or generate any other SQL for metadata purposes**.
- If no abnormal points are detected, **stop the task permanently** after reporting "No anomalies detected".


## Strict Forbidden Behavior

- Do **NOT** modify or bypass predefined termination rules.
- Do **NOT** invent unrequired operations or extend the task arbitrarily.
- Do **NOT** create any database or table.
- Do **NOT** write data into any table.
- Do **NOT** truncate intermediate output.
- Do **NOT** continue with follow-up steps, supplementary explanations, or associative reasoning when the workflow demands termination.

## Termination Rules

The following conditions require **permanent task termination** (stop and inform the user; do not retry or continue):

| Step | Termination Condition |
|------|-----------------------|
| 1.1 | `scripts/kwdb_sql_execute.py` not found in skill directory |
| 1.2 | User fails to provide required connection parameters |
| 1.3 | Database connection test fails |
| 2 | User-specified database/table/column does not exist |
| 3 | Target database is not TIME SERIES, or all filtered columns are non-numeric |
| 4 | `SELECT DISTINCT <primary_tag>` returns empty list (All Tags case) |
| 9 | Result file is empty (Single Tag), or all tags yield empty results (All Tags) |

When termination is triggered, explain the exact reason to the user. Do NOT attempt alternative approaches unless explicitly directed by the user.