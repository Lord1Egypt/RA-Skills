---
name: workflow
description: Detailed step-by-step workflow for the anomaly detection skill.
---

## Workflow Detail

## 0. Security Confirmation (MANDATORY)

**Before proceeding, you MUST display the following confirmation prompt to the user.**

```
🔒 Security Confirmation                                                    
Database configuration information is SENSITIVE data, anomaly detection SKILL should be used in insecure mode
Type "I AGREE" to proceed
```

**IMPORTANT:**
- **STOP permanently** if the user does not explicitly type "I AGREE"
- Do NOT proceed to Step 1 until the user provides consent
- Do NOT skip this step for any reason
- Do NOT assume the user has already consented

### 1. Precondition Validation

#### 1.1 Verify Script Availability
- If `scripts/kwdb_sql_execute.py` is **not** available in the skill directory, **stop permanently** and inform the user.

#### 1.2 Collect Connection Parameters
| Parameter | Description | Example |
|-----------|-------------|---------|
| `host` | KWDB server hostname or IP | `127.0.0.1` |
| `port` | KWDB server port | `54321` |
| `username` | Database login username | `root` |
| `password` | Database login password (`""` if none) | `123456` |

If any parameter is missing, **ask the user**. Do NOT guess or use defaults.

#### 1.3 Verify Database Connection

```bash
python scripts/kwdb_sql_execute.py <host> <port> <username> <password> "SELECT 1"
```

- **Succeeds** → connection valid, proceed to 1.4.
- **Fails** → **stop permanently** and report the exact failure reason. Do NOT retry with alternative parameters.

Common failure reasons:
- Host unreachable / port incorrect → report connection refused / timeout
- Username or password incorrect → report authentication failure
- Network unreachable → report network error

#### 1.4 Confirm Target Table and Columns
- If the user has not specified the target **table** and **numeric column(s)**:
  1. **MUST** query table and column metadata (only `INTEGER` / `FLOAT` / `DOUBLE` columns) via `references/metadata-query.md` using `kwdb_sql_execute.py` (no output file).
  2. Present the metadata to the user and ask them to provide the exact table and column names.

### 2. Intent Analysis & SQL Generation
- Analyze the user's intent.
- Generate the SQL query following the rules in `references/ts-select.md`.
- Use the metadata fetched via `references/metadata-query.md` to ensure correct database/table/column names.
- **Rule**: If the user-specified database/table/column does not exist, **stop permanently** and explain exactly what is missing.

### 3. Database-Type Validation
If the SQL statement violates any rule below, **stop permanently** and tell the user the detailed reason:
- The target database is **not** a TIME SERIES database.
- **All** filtered columns are non-numeric (not `INTEGER` / `FLOAT` / `DOUBLE`).

### 4. Primary-Tag Check & Scope Determination

| Case | Condition | Action |
|------|-----------|--------|
| **Single Tag** | SQL contains `WHERE <primary_tag> = '<value>'` | Proceed directly to step 5. |
| **All Tags** | SQL does **not** filter by primary tag | Query `SELECT DISTINCT <primary_tag> FROM <table>` via `kwdb_sql_execute.py` (no output file) to get all values, then repeat steps 5–14 once per value. |

**All Tags — detailed sub-workflow:**
1. Execute `SELECT DISTINCT <primary_tag> FROM <table>` via `kwdb_sql_execute.py` (no output file). Parse stdout to extract distinct values.
2. If the distinct list is empty, **stop permanently**.
3. For each primary tag value:
   - Append `AND <primary_tag> = '<value>'` to the `WHERE` clause (or add `WHERE <primary_tag> = '<value>'` if no `WHERE` exists).
   - Execute steps 5–13 for this value.
   - In step 9, save result to `/tmp/sql-result-<safe_tag_value>.json` where `<safe_tag_value>` has `/` replaced by `_`.
   - In step 11, run detection on that file.
   - Record the per-tag detection result.
4. After all values are processed, proceed to step 14 with aggregated per-tag results.

### 5. SQL Refinement (per primary-tag iteration)

| Rule | Action |
|------|--------|
| Remove irrelevant columns | Keep only the timestamp and numeric columns needed for detection. |
| Remove non-numeric columns | **Drop any filtered column that is not `INTEGER` / `FLOAT` / `DOUBLE` / `DECIMAL` / `NUMERIC` /`TIMESTAMP`**. |
| Ensure timestamp in SELECT | If no timestamp column is in the filtered clause, look it up in table metadata and add it. |
| Limit without time filter | If there is **no time filter condition** in `WHERE`, **MUST add `ORDER BY <timestamp_column> DESC` and `LIMIT 1000`**. |

**Output**: The refined SQL after this step is called `refined_sql_limited`.

### 6. Final SQL Wrapper
**MUST** rewrite the refined SQL as:

```sql
SELECT * FROM (<refined_sql_limited>) AS anomaly_subquery ORDER BY <timestamp_column> ASC
```

### 7. Show SQL to User
**MUST** display the final fixed SQL before execution.
In **All Tags** cases, show the SQL for the current primary tag value and indicate progress (e.g. "Processing device dev_001 of 10...").

### 8. Data Count Check (Conditional)

**ONLY skip this step if `refined_sql_limited` contains a `LIMIT` clause** (indicating data volume is already constrained by Step 5).

| Condition | Action |
|-----------|--------|
| `refined_sql_limited` has `LIMIT` clause | **Skip** this step, proceed directly to step 9 |
| `refined_sql_limited` has **no** `LIMIT` clause | Execute COUNT check |

**Rationale**: In Step 5, `LIMIT 1000` is automatically added when there is no timestamp filter. This already constrains the data volume, so COUNT check is unnecessary. When `LIMIT` is present, the data volume is already bounded and no COUNT check is needed.

**When to execute:**
Execute a COUNT query to check data volume in **refined_sql_limited**:

```bash
python scripts/kwdb_sql_execute.py <host> <port> <username> <password> "SELECT COUNT(*) FROM (<refined_sql_limited>) AS count_subquery"
```

- If the COUNT result is **greater than 1,00,000**, **stop permanently** and inform the user:
  > "数据量过大（{count} 条），无法执行异常检测。建议先对数据进行时间范围筛选或降采样后再试。"
  
- If the COUNT is within the limit, proceed to step 9.

### 9. Execute SQL via Script

```bash
python scripts/kwdb_sql_execute.py <host> <port> <username> <password> "the-fixed-sql" sql_result_file
```

- `sql_result_file`: Result file path in `/tmp/`:
  - **Single Tag**: `/tmp/sql-result-<YYYYMMDDHHmmss>`
  - **All Tags**: `/tmp/sql-result-<safe_tag_value>-<YYYYMMDDHHmmss>` (no `.json` extension in the script argument; the script handles the output format).

Connection parameters from step 1.2 are reused for all SQL executions. Do NOT ask for them again.

### 10. Validate Result File
- Verify the result file was created successfully.
- **Single Tag**: if empty or no data rows, **stop permanently**.
- **All Tags**: if a single primary tag value yields an empty result, skip it and continue with the next value. If **all** values yield empty results, **stop permanently**.

### 11. Run Anomaly Detection

```bash
python scripts/3-sigma-detection.py --input sql-result-file --output detect-result-file
```

- `detect-result-file`:
  - **Single Tag**: `/tmp/detect-result-<YYYYMMDDHHmmss>`
  - **All Tags**: `/tmp/detect-result-<safe_tag_value>-<YYYYMMDDHHmmss>`

In **All Tags** cases, run the script once per saved result file and record each output.

### 12. Load Column Rules
Extract validation rules from column comments:
- Execute `SHOW COLUMNS FROM dbname.tbname WITH COMMENT` via `kwdb_sql_execute.py` (no output file).
- Parse stdout to extract column comment rules.
- See `references/column-comment.md` for the query pattern.

### 13. Filter Anomalies by Rules
If extracted rules are non-empty, apply them to filter detected anomaly points.
- Example rule types: `min > X`, `max < Y`, `range [A, B]`.
- Remove any anomaly that does **not** violate the declared rule.

### 14. Generate Inspection Report
Ask the user which report format they prefer:

| Format | Delivery |
|--------|----------|
| Direct output | Print inline using `references/report-template.md`. |
| Markdown file | Save to `/tmp/dt-report-<YYYYMMDDHHmmss>.md` using `references/report-template.md`. |
| HTML file | **Follow the HTML report generation workflow below**. |

#### HTML Report Generation Workflow
1. **Fill in the JSON template**: Populate `references/report-template-html.md` with the actual detection results:
   - `db_name`: database name
   - `table_name`: table name
   - `detection_time`: current system datetime
   - `time_span`: start and end time from the queried data
   - `detection_method`: "3-Sigma"
   - `tags`: array containing each primary tag value with its column detection results

2. **Save JSON to `/tmp`**: Write the filled JSON to `/tmp/report-json-<YYYYMMDDHHmmss>.json`

3. **Generate HTML report**: Execute the following command:
   ```bash
   python scripts/html-report-gen.py --input /tmp/report-json-<YYYYMMDDHHmmss>.json --output /tmp/dt-report-<YYYYMMDDHHmmss>.html
   ```

4. **Verify output**: Confirm the HTML file was generated successfully at `/tmp/dt-report-<YYYYMMDDHHmmss>.html`

In **All Tags** cases, the report must group results by primary tag value (one section or tab per tag).

### 15. Cleanup
Delete **all** temporary files generated during the task **except** the final report file.
