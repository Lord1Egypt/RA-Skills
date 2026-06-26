---
name: kwdb-text2sql-aiot
description: |
  Convert natural language queries to KWDB SQL for time series data, relational data and cross-model analysis.
  Use this skill whenever users ask to query KWDB databases, write SQL for KWDB,
  or convert natural language to KWDB-specific SQL syntax.
  Supports: CREATE DATABASE/TABLE, downsampling, interpolation, latest value queries,
  aggregation analysis, cross-model queries, window/session/event analysis.
triggers:
  - query KWDB database
  - write SQL for KWDB
  - convert natural language to SQL
  - time series query
  - IoT sensor data query
  - downsampling query
  - interpolation query
  - latest value query
  - cross-model join query
  - 创建库/创建表/CREATE DATABASE/CREATE TABLE
  - 时序/降采样/插值/最新值/跨模
---

# KWDB Text-to-SQL Skill

## Query Type Routing

Based on the user's query, read the appropriate reference file:

| Query Type | Reference File |
|---------|---------------|
| **Query routing (start here)** | `references/scenarios.md` |
| MCP integration | `references/mcp-integration.md` |
| 时序DDL (创建时序库/表) | `references/ts-ddl.md` |
| 聚合操作及降采样 (每小时/每天统计) | `references/ts-downsampling.md` |
| 插值/填充缺失值 | `references/ts-interpolation.md` |
| 最新值查询 | `references/ts-latest-value.md` |
| 滑动窗口/session/event | `references/ts-window-events.md` |
| 关系表查询 | `references/relational.md` |
| 跨模查询（时序表+关系表） | `references/cross-model.md` |
| 时序函数语法速查 | `references/ts-functions.md` |
| 关系函数语法速查 | `references/relational-functions.md` |

## Quick Reference

| NL Pattern | SQL Pattern |
|------------|-------------|
| 最近N分钟/小时/天的数据 | `WHERE ts >= NOW() - INTERVAL 'N hour'` |
| 每小时/每天的平均值 | `time_bucket(ts, '1h/1d')` + `avg(col)` |
| 每N分钟/小时/天降采样 | `time_bucket(ts, 'X')` + aggregation |
| 填充缺失值 | `time_bucket_gapfill()` + `interpolate()` |
| 最新数据 | `last(col)` or `ORDER BY ts DESC LIMIT 1` |
| 滑动窗口 | `TIME_WINDOW(ts, '1h', '15m')` |
| 关联设备信息 | `JOIN devices ON ...` |

## Workflow

### Phase 0: MCP Detection & Schema Discovery (Recommended)

1. **Detect MCP availability**: Call `read-query` with `SELECT 1`
   - If successful → MCP is available
   - If failed → MCP is unavailable, proceed to fallback

2. **Get database name** (if not provided by user):
   - Ask user: "请提供要查询的数据库名称"
   - Or execute `SHOW DATABASES` to list all databases

3. **Discover tables in database**: Execute `SHOW TABLES FROM {database_name}`

4. **Identify candidate tables**:
   - Match NL keywords to table names (e.g., "传感器" → sensor_data)
   - If multiple candidates → ask user: "请确认表名: [A, B, C]?"

5. **Get table schema**: Execute `SHOW CREATE TABLE {database_name}.{table_name}`, do not use `DESCRIBE`
   - Note column names, types, primary key, tags, comments
   - Map NL field names to actual column names

6. **Proceed to Phase 1** with verified schema

### Phase 0 Fallback: No MCP Available

When MCP is unavailable:

1. **Option A - Ask user**: "请提供表结构信息（表名、列名）"
   - Wait for user to describe the schema
   - Proceed to Phase 1

2. **Option B - Use assumed fields**: "我将使用常见字段名生成 SQL，请验证"
   - Use standard field names (ts, device_id, temperature, etc.)
   - Mark output as "ASSUMED SCHEMA - please verify"

3. **Proceed to Phase 1**

### Phase 1: Query Type Routing

1. **Read scenarios.md**: `references/scenarios.md` - single entry point with decision tree
2. **Route to scenario file** based on query type:
   - aggregation/downsampling → `ts-downsampling.md`
   - interpolation → `ts-interpolation.md`
   - latest value → `ts-latest-value.md`
   - window/session/event → `ts-window-events.md`
   - cross-model → `cross-model.md`
   - relational → `relational.md`
3. **Function syntax** → see `ts-functions.md` (time-series) or `relational-functions.md` (relational)

### Phase 2: SQL Generation

1. **Extract entities**: Table name, columns, time range, conditions
2. **Use schema from Phase 0** (if MCP was used)
3. **Generate SQL**: Use patterns from reference to construct SQL
4. **Validate**: Ensure SQL follows KWDB function syntax

### Phase 3: Output

1. **Format output**: Follow `assets/output-template.md`
2. **Include field mapping** if MCP was used
3. **Mark assumptions** if schema was assumed
4. **Add verification checklist**

### Phase 4: KWDB Execute

**Prerequisite:** SQL has been generated in Phase 2 and formatted in Phase 3.

#### Step 1: Check MCP Availability

**Note:** If MCP was successfully used in Phase 0 and schema was discovered, MCP is available. If Phase 0 indicated MCP was unavailable, skip this phase entirely.

If MCP availability is unknown (e.g., Phase 0 was skipped), verify now:
- Call `read-query` with `SELECT 1`
- If successful → MCP is available, proceed to Step 2
- If failed → MCP is unavailable, **skip this phase entirely** and end workflow

#### Step 2: Ask User for Execution Confirmation

Prompt user:
```
生成的 SQL 已准备就绪。是否需要通过 kwdb-mcp-server 执行该 SQL？
- 输入 "是" 或 "执行" → 继续执行
- 输入 "否" 或 "跳过" → 结束，不再执行
```

If user declines → **end workflow**.

#### Step 3: Determine Query Type

Analyze the generated SQL:
- **Read query**: SELECT, SHOW, EXPLAIN → use `read-query`
- **Write query**: INSERT, UPDATE, DELETE, CREATE, DROP, ALTER → use `write-query`

#### Step 4: Execute Query

Call the appropriate MCP tool:

**For read queries (`read-query`):**
```json
{
  "sql": "<generated SQL>"
}
```

**For write queries (`write-query`):**
```json
{
  "sql": "<generated SQL>"
}
```

#### Step 5: Handle Execution Result

**On Success:**
Report to user:
```
## Execution Result
- Status: success
- Query Type: read / write
- Row Count: N
- Auto-Limited: true/false

### Results
[formatted table if applicable]
```

**On Failure:**
1. Parse the error message to identify error type (see Error Type table in Error Handling section below)
2. If error indicates **SQL generation issue** (wrong table name, wrong column, syntax error):
   - Explain to user: "SQL 执行失败，正在分析错误原因..."
   - Report the error and analysis:
     ```
     ## Execution Result
     - Status: failed
     - Error: [error message]
     - Analysis: [cause analysis]
     ```
   - Return to **Phase 1** with error context to regenerate SQL
3. If error indicates **user data issue** (constraint violation, permission issue, etc.):
   - Report the error and suggest fixes, but do not auto-regenerate

## Reference Files

- `references/scenarios.md` - Query routing entry point (decision tree)
- `references/mcp-integration.md` - How to use kwdb-mcp-server for schema discovery
- `references/ts-ddl.md` - Time series DDL (CREATE DATABASE/TABLE with TAGS)
- `references/ts-downsampling.md` - time_bucket for fixed-interval downsampling
- `references/ts-interpolation.md` - time_bucket_gapfill + interpolate for gap filling
- `references/ts-latest-value.md` - first/last/last_row for latest value queries
- `references/ts-window-events.md` - TIME_WINDOW, SESSION_WINDOW, EVENT_WINDOW, TWA, diff
- `references/relational.md` - Standard SQL for relational tables
- `references/cross-model.md` - JOIN between relational and time series
- `references/ts-functions.md` - KWDB time-series function syntax reference
- `references/relational-functions.md` - KWDB relational function syntax reference


## Guardrails

1. **Always verify table existence** when MCP is available
2. **Confirm column names** match actual schema before generating SQL
3. **Ask for time range** if user doesn't specify
4. **Add LIMIT clause** for queries without one (MCP auto-adds LIMIT 20, but you should be explicit)
5. **Mark assumed schema** when MCP is unavailable
6. **Handle ambiguous NL** by asking clarifying questions

## Error Handling (Authoritative Reference)

This Error Type table is used by:
- **Phase 4 Step 5** when SQL execution fails
- **When user reports** that generated SQL failed

When a user reports that generated SQL failed, diagnose and regenerate:

| Error Type | Likely Cause | Fix |
|-----------|-------------|-----|
| `relation "xxx" does not exist` | Wrong table name | Ask user to confirm table name, re-discover via MCP |
| `column "xxx" not found` | Wrong column name | Use MCP to re-read schema, update field mapping |
| `syntax error` | SQL syntax issue | Review KWDB SQL syntax, check function parameter order |
| `invalid interval` | Wrong interval format | Use format like `'1h'`, `'1d'`, `'5m'` — not复合格式 like `'1d1h'` |
| Overflow / out of range | Aggregation result too large | Add filters to reduce result set size |
| `ambiguous column reference` | Column name exists in both joined tables | Use fully-qualified column names (`table.column`) |
| `permission denied` | No write permission | Report to user, do not regenerate |
| `duplicate key` | Constraint violation | Report to user, do not regenerate |

When SQL fails:
1. Read the error message to identify the error type
2. If schema issue → re-run MCP discovery
3. If syntax issue → check `ts-functions.md` or `relational-functions.md` and relevant reference file
4. If data issue → ask user for clarification
5. Regenerate corrected SQL with explanation

## Schema Discovery via MCP

Use `read-query` tool to execute SHOW commands:

| SQL Command | Purpose |
|-------------|---------|
| `SHOW DATABASES` | List all databases |
| `SHOW TABLES FROM {database_name}` | List all tables in a database |
| `SHOW CREATE TABLE {database_name}.{table_name}` | Get table structure (columns, types, tags, comments) |