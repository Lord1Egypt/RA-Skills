---
name: kwdb-ts-anomaly-detection
description: |
  Automates end-to-end anomaly detection for time-series data stored in KaiwuDB / KWDB.
  Use this skill whenever the user mentions:
  - anomaly detection, outliers, or unusual patterns in KWDB / KaiwuDB time-series data
  - inspecting sensor metrics, IoT telemetry, or monitoring data for spikes, dips, or drift
  - "find anomalies", "detect outliers", "3-sigma check", "STL decomposition", or "time-series anomaly"
  - analyzing historical trends, abnormal points, or data quality issues in TS tables
  Even if the user does not explicitly say "anomaly", trigger this skill when they ask to
  inspect, validate, or flag unusual values in time-series columns (integer, float, double).
---

## kwdb-ts-anomaly-detection

Detect anomalies in KaiwuDB / KWDB time-series data by following the workflow below exactly and in order.

## Constraints

- Execute **all** SQL via `scripts/kwdb_sql_execute.py`. Do NOT use `kwdb-mcp-server` MCP tools.
- Metadata queries must **not** store results to file — omit the output file argument.
- If no anomalies are detected, **stop permanently** after reporting "No anomalies detected".
- Do NOT modify/bypass termination rules, invent operations, create/drop databases or tables, write data into any table, or truncate output.
- See `references/constraints.md` for the full list of rules and forbidden behaviors.

## SQL Execution

```bash
python scripts/kwdb_sql_execute.py <host> <port> <username> <password> "<sql>" [output_file]
```

Omit `output_file` for metadata queries; include it for data queries to persist results in `/tmp/`.

## Workflow

Execute the following steps in strict order. **MUST** See `references/workflow.md` for full details on each step at first.

**0. Security Confirmation (MANDATORY)** — Before any operation, **MUST** display the security confirmation prompt and wait for the user to type "I AGREE". **STOP permanently** if consent is not obtained. See `references/workflow.md` Section 0 for the mandatory confirmation prompt.

1. **Precondition Validation** — Verify script availability, collect connection params (`host`, `port`, `username`, `password`), test connection, confirm target table/columns. If the user has not specified table/columns, query metadata via `references/metadata-query.md` and ask the user.

2. **Intent Analysis & SQL Generation** — Analyze user intent, generate SQL following `references/ts-select.md`, validate names against metadata. Stop if names don't exist.

3. **Database-Type Validation** — Stop if target DB is not TIME SERIES or all filtered columns are non-numeric.

4. **Primary-Tag Check & Scope** — If SQL filters by a specific primary tag → proceed (single tag). Otherwise, query all distinct primary tag values and repeat steps 5–13 per value (all tags).

5. **SQL Refinement** — Keep only timestamp + numeric columns, ensure `ORDER BY <timestamp> DESC`, **MUST add `LIMIT 1000` if no time filter conditions in where clause**.

6. **Final SQL Wrapper** — Wrap as `SELECT * FROM (<refined_sql>) AS anomaly_subquery ORDER BY <timestamp_column> ASC`.

7. **MUST Show SQL to User** — Display the final SQL before execution.

8. **Data Count Check (Conditional)** — **ONLY skip this step if `refined_sql_limited` contains a `LIMIT` clause** (indicating data volume is already constrained by Step 5). If there is no `LIMIT` clause, execute COUNT query on **refined_sql_limited**. If count > 100,000, stop and inform user: "数据量过大（{count} 条），无法执行异常检测。建议先对数据进行时间范围筛选或降采样后再试。"

9. **Execute SQL** — Run via `kwdb_sql_execute.py`, save result to `/tmp/sql-result-*`.

10. **Validate Result** — Stop if no data rows (single tag) or all tags empty.

11. **Run Anomaly Detection** — Execute `python scripts/3-sigma-detection.py --input <result> --output <detect-result>`.

12. **Load Column Rules** — Query column comments via `references/column-comment.md` to extract validation rules.

13. **Filter by Rules** — Remove anomalies that don't violate declared column-comment rules.

14. **Generate Report** — **MUST Ask user for format (direct / Markdown / PDF / HTML) before**. 
   - For **direct/Markdown**: Use `references/report-template.md`.
   - For **HTML**: Follow the HTML report workflow in `references/workflow.md` (Step 14):
     1. Fill `references/report-template-html.md` JSON template with detection results
     2. Save to `/tmp/report-json-<YYYYMMDDHHmmss>.json`
     3. Run `python scripts/html-report-gen.py --input <json-file> --output /tmp/dt-report-<YYYYMMDDHHmmss>.html`

15. **Cleanup** — Delete all temp files except the final report.

## Error Handling

Consult `references/error-handling.md` for error codes, root causes, and recovery actions.