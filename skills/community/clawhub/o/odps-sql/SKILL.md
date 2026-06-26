---
name: "ODPS (MaxCompute) Data Query"
description: |
  Use this skill when the user wants to query, analyze, or explore data in Alibaba Cloud ODPS (MaxCompute / 阿里云大数据计算服务).
  This skill executes SQL queries, lists tables, and inspects table schemas by running the odps_helper.py command-line script.
  Trigger this skill for requests like: querying ODPS data, listing MaxCompute tables, running SQL on ODPS, checking table structure,
  analyzing business data stored in ODPS, or any data exploration tasks involving Alibaba Cloud MaxCompute / ODPS.
metadata:
  { "openclaw": { "requires": { "bins": ["python"], "env": ["ALIYUN_ACCESS_ID", "ALIYUN_ACCESS_SECRET", "ALIYUN_PROJECT_NAME", "ALIYUN_END_POINT"] } } }
---

## Setup (First-time only)

1. Copy the credential template and fill in your values:
   ```bash
   cd odps-sql/
   cp config.example.env .env
   # Edit .env with your Alibaba Cloud credentials
   ```

2. Activate your Python environment and install dependency:
   ```bash
   # conda users:
   conda activate <your-env>
   # venv users:
   source .venv/bin/activate

   pip install pyodps
   ```

## Executing Commands

Activate your Python environment first, then run all commands from the project root with:

```bash
SCRIPT=odps-sql/scripts/odps_helper.py
```

### List tables

```bash
python $SCRIPT --list-tables
```

Filter by name:
```bash
python $SCRIPT --list-tables --pattern <keyword>
```

### Get table schema

```bash
python $SCRIPT --describe <table_name>
```

### Execute SQL query

```bash
python $SCRIPT --query "<SQL statement>" [--limit <n>]
```

Default limit is 100 rows.

## Workflow for Data Tasks

Follow this pattern when the user asks about ODPS data:

1. **Discover** — If the table name is unknown, run `--list-tables --pattern <keyword>` to find it.
2. **Inspect** — Run `--describe <table>` to understand columns, types, and partition structure.
3. **Query** — Construct the SQL and run `--query`. Always add a partition filter (`WHERE dt = '...'`) for partitioned tables to avoid full scans.
4. **Present** — Summarize the results clearly for the user.

## ODPS SQL Key Differences from Standard SQL

| Feature | Standard SQL | ODPS SQL |
|---------|-------------|----------|
| String concat | `a \|\| b` | `CONCAT(a, b)` |
| Current time | `NOW()` | `GETDATE()` |
| Null coalesce | `IFNULL(x,y)` | `NVL(x, y)` |
| Regex match | `REGEXP` | `RLIKE` |
| Date literal | `'2024-01-01'` | `TO_DATE('2024-01-01','yyyy-mm-dd')` |

Partition filter is **required** for partitioned tables (partition column is usually `dt`):
```sql
SELECT * FROM table_name WHERE dt = '2024-01-01' LIMIT 100
```

See `odps-sql/references/odps_sql_guide.md` for a full SQL reference.

## Error Handling

- **`pyodps` not found** → Run install command in Setup step above
- **Missing credentials** → Check that `odps-sql/.env` exists and all four fields are filled in
- **Table not found** → Use `--list-tables --pattern` to find the correct name
- **SQL syntax error** → Check the ODPS SQL differences table above; avoid MySQL/PostgreSQL-specific syntax
