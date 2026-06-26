# KWDB MCP Server Integration

This guide describes how to use kwdb-mcp-server to automatically discover database schema and generate accurate SQL from natural language.

## MCP Tools

### read-query

Executes read-only SQL queries (SELECT, SHOW, EXPLAIN).

**Parameters:**
- `sql` (required) - The SQL query to execute

**Returns:**
```json
{
  "status": "success",
  "type": "query_result",
  "data": {
    "result_type": "table",
    "columns": ["col1", "col2"],
    "rows": [{"col1": "val1", "col2": "val2"}],
    "metadata": {
      "row_count": 1,
      "query": "SELECT ...",
      "auto_limited": false
    }
  }
}
```

**Note:** SELECT queries without LIMIT automatically get `LIMIT 20` added to prevent large result sets. Check `metadata.auto_limited` to detect this.

## Schema Discovery via SHOW Commands

Use `read-query` tool to execute SHOW commands for schema discovery:

| SQL Command | Purpose |
|-------------|---------|
| `SHOW DATABASES` | List all databases |
| `SHOW TABLES FROM {database_name}` | List all tables in a database |
| `SHOW CREATE TABLE {database_name}.{table_name}` | Get complete table structure |



## Workflow: Schema-Aware SQL Generation

### Step 1: Detect MCP Availability

Call `read-query` with `SELECT 1` to verify MCP is available.

### Step 2: Get Database Name (if not provided)

Ask user which database to query, or execute `SHOW DATABASES` to list all databases.

### Step 3: Discover Tables

Execute `SHOW TABLES FROM {database_name}` to get all tables in the database.

### Step 4: Match Candidate Tables

Based on natural language keywords, identify candidate tables:
- "设备" / "device" / "传感器" / "sensor" → tables with device/sensor in name
- "温度" / "temperature" → tables with temperature-related columns
- "历史" / "history" → time-series tables

If multiple tables match, ask the user to confirm.

### Step 5: Get Table Schema

For each candidate table, execute `SHOW CREATE TABLE {database_name}.{table_name}` to get column definitions.

### Step 6: Map NL to Schema

Map natural language field references to actual column names:
- "时间" / "timestamp" → ts column
- "设备ID" / "device_id" → tag columns
- "温度" / "temperature" → measurement columns

### Step 7: Generate SQL

Use the schema information to construct accurate SQL.

## Example

**User query:** "查询最近24小时每台设备的平均温度"

**MCP-assisted workflow:**

1. Ask user for database name → "iot_db"

2. Execute `SHOW DATABASES` to verify database exists

3. Execute `SHOW TABLES FROM iot_db` → returns: ["devices", "sensor_data", "alarms"]

4. Identify candidate tables: "sensor_data" likely contains temperature readings

5. Execute `SHOW CREATE TABLE iot_db.sensor_data`:
```sql
CREATE TABLE iot_db.sensor_data (
    ts TIMESTAMPTZ NOT NULL,
    temperature DOUBLE,
    humidity DOUBLE,
    device_id INT4
) TAGS (
    device_id INT4 NOT NULL,
    location VARCHAR(100)
) PRIMARY TAGS (device_id)
```

6. Execute `SHOW CREATE TABLE iot_db.devices`:
```sql
CREATE TABLE iot_db.devices (
    device_id INT4 NOT NULL,
    device_name VARCHAR(100),
    location VARCHAR(100),
    PRIMARY KEY (device_id)
)
```

7. Generate SQL:
```sql
SELECT d.device_name,
       d.location,
       AVG(s.temperature) AS avg_temp
FROM devices d
INNER JOIN (
    SELECT device_id,
           AVG(temperature) AS temperature
    FROM sensor_data
    WHERE ts >= NOW() - INTERVAL '24 hour'
    GROUP BY device_id
) s ON d.device_id = s.device_id
GROUP BY d.device_name, d.location
ORDER BY d.device_name;
```

## Fallback: No MCP Available

When kwdb-mcp-server is not available:

1. Ask user to manually provide table structure
2. Or generate SQL with placeholder column names and mark as "assumed schema"
3. User should verify and adjust the generated SQL

## MCP Detection Pattern

To check if MCP is available, execute:

```sql
SELECT 1
```

If this fails or returns an error, MCP is unavailable.
