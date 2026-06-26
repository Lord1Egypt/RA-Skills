# Output Template

Output format for kwdb-text2sql-aiot skill.

## Response Structure

Every generated SQL response should follow this structure:

```
## Intent
Brief description of what the SQL does

## Assumptions
- Table/column names (verified via MCP or assumed)
- Time range if applicable
- Business context

## Generated SQL
```sql
<SQL statement>
```

## Field Mapping (if MCP was used)
| NL Field | Database Column |
|----------|-----------------|
| 设备ID   | device_id (TAG) |
| 温度     | temperature    |
| 时间     | ts             |

## Validation Checklist
- [ ] SQL syntax verified
- [ ] Table exists (MCP verified / user confirmed)
- [ ] Column names correct
- [ ] Time range makes sense
- [ ] LIMIT clause added for large result sets
```

## Query Type Specific Templates

### 1. Downsampling Query

```
## Intent
Calculate [aggregation] per [entity] at [interval] intervals

## Assumptions
- Table: [table_name] (verified via MCP)
- Entity column: [column] (TAG)
- Timestamp column: ts
- Aggregation: [avg/sum/count/etc.]
- Interval: [1h/1d/etc.]
- Time range: [specified or default 24h]

## Generated SQL
```sql
SELECT
    time_bucket(ts, '[interval]') AS period,
    [entity_column],
    [aggregation]([metric_column]) AS [alias]
FROM [table_name]
WHERE ts >= NOW() - INTERVAL '[duration]'
GROUP BY period, [entity_column]
ORDER BY period, [entity_column];
```
```

### 2. Interpolation Query

```
## Intent
Fill missing values in [column] using [method] interpolation

## Assumptions
- Table: [table_name]
- Timestamp column: ts
- Metric column: [column]
- Interpolation method: [linear/prev/next]
- Time range: [specified]

## Generated SQL
```sql
SELECT
    time_bucket_gapfill(ts, '[interval]') AS bucket,
    interpolate([aggregation]([column]), '[method]') AS [column]_filled
FROM [table_name]
WHERE ts >= '[start_time]' AND ts < '[end_time]'
GROUP BY bucket
ORDER BY bucket;
```
```

### 3. Latest Value Query

```
## Intent
Get the most recent [metric] reading for each [entity]

## Assumptions
- Table: [table_name]
- Entity column: [entity] (TAG)
- Metric column: [metric]
- Timestamp column: ts

## Generated SQL
```sql
SELECT
    [entity_column],
    last([metric_column]) AS latest_[metric],
    last(ts) AS timestamp
FROM [table_name]
GROUP BY [entity_column];
```

### 4. Cross-Model Query (JOIN)

```
## Intent
Get [relational info] with their [time-series metric]

## Assumptions
- Relational table: [rel_table] (verified via MCP)
- Time-series table: [ts_table]
- Join key: [rel_column] = [ts_column]
- Time range: [if applicable]

## Generated SQL
```sql
SELECT
    r.[rel_column],
    r.[rel_field],
    t.[metric_summary]
FROM [rel_table] r
[LEFT/INNER] JOIN (
    SELECT
        [ts_column],
        [aggregation]([metric]) AS [metric_summary]
    FROM [ts_table]
    [WHERE ts >= ...]
    GROUP BY [ts_column]
) t ON r.[rel_column] = t.[ts_column]
[WHERE ...]
[ORDER BY ...];
```
```

### 5. Event Window Query

```
## Intent
Detect events where [condition]

## Assumptions
- Table: [table_name]
- Start condition: [condition]
- End condition: [condition]
- Timestamp column: ts

## Generated SQL
```sql
SELECT
    EVENT_WINDOW([start_cond], [end_cond]) AS event,
    [aggregation_functions]
FROM [table_name]
GROUP BY event
ORDER BY event;
```
```

### 6. Session Window Query

```
## Intent
Group readings into sessions where gaps are less than [interval]

## Assumptions
- Table: [table_name]
- Timestamp column: ts
- Gap threshold: [interval]

## Generated SQL
```sql
SELECT
    SESSION_WINDOW(ts, '[interval]') AS session,
    [entity_column],
    [aggregation]
FROM [table_name]
GROUP BY session, [entity_column]
ORDER BY session;
```
```

### 7. Time-Weighted Average

```
## Intent
Calculate time-weighted average of [metric]

## Assumptions
- Table: [table_name]
- Timestamp column: ts
- Metric column: [metric]
- Time window: [interval]

## Generated SQL
```sql
SELECT
    time_bucket(ts, '[interval]') AS period,
    TWA(ts, [metric]) AS twa_[metric]
FROM [table_name]
WHERE ts >= '[start]' AND ts < '[end]'
GROUP BY period
ORDER BY period;
```
```

## MCP-Verified Output Example

When MCP is used, include verification details:

```
## Intent
Query average temperature per device in the last 24 hours

## Schema Source
- Database: iot_db (verified via kwdb://db_info/iot_db)
- Table: sensor_data (verified via kwdb://table/sensor_data)
- Table type: TIME SERIES

## Generated SQL
```sql
SELECT
    device_id,
    AVG(temperature) AS avg_temp
FROM sensor_data
WHERE ts >= NOW() - INTERVAL '24 hour'
GROUP BY device_id
ORDER BY device_id;
```

## Field Mapping
| NL Term | Column | Type |
|---------|--------|------|
| 设备 | device_id | TAG (INT) |
| 温度 | temperature | DOUBLE |
| 时间 | ts | TIMESTAMP |

## Validation
- [x] Table exists and is TIME SERIES type (MCP verified)
- [x] Columns exist with correct types (MCP verified)
- [x] time_bucket syntax correct
- [x] WHERE clause uses correct time filter
```

## Fallback Output (No MCP)

When MCP is unavailable and user didn't provide schema:

```
## Intent
Query average temperature per device (ASSUMED SCHEMA)

## Assumptions
- Table name: sensor_data (user mentioned "传感器数据")
- Entity column: device_id (assumed standard naming)
- Temperature column: temperature (assumed standard naming)
- Timestamp column: ts (assumed standard for time-series)

## ⚠️ Schema Not Verified
MCP is not available. Please verify the column names are correct.

## Generated SQL
```sql
SELECT
    device_id,
    AVG(temperature) AS avg_temp
FROM sensor_data
WHERE ts >= NOW() - INTERVAL '24 hour'
GROUP BY device_id;
```

## Verification Needed
Please confirm:
- [ ] Table name is correct
- [ ] Column names match actual schema
- [ ] Time range is appropriate
```
