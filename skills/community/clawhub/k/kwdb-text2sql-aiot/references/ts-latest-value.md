# Time Series Latest Value

Retrieve the most recent or oldest data points from time-series tables.

## When to Use

Use for: "最新温度", "最近一条记录", "当前状态", "每个设备的最新读数"

## Functions

```sql
first(column)      -- value at minimum timestamp (excludes NULL)
last(column)       -- value at maximum timestamp (excludes NULL)
last_row(column)   -- value at maximum timestamp (includes NULL)
first_row(column)  -- value at minimum timestamp (includes NULL)
```

**Note**: `last()` ignores NULLs; use `last_row()` to include NULLs.

## Examples

**Latest Value per Device:**
```sql
SELECT device_id,
       last(temperature) AS latest_temp,
       last(ts) AS timestamp
FROM sensor_data
GROUP BY device_id;
```

**Latest Values with Time Range:**
```sql
SELECT device_id,
       last(temperature) AS temp,
       last(humidity) AS humidity
FROM sensor_data
WHERE ts >= NOW() - INTERVAL '1 hour'
GROUP BY device_id;
```

**Latest Row with NULLs:**
```sql
SELECT device_id,
       last_row(temperature) AS latest_temp
FROM sensor_data
GROUP BY device_id;
```

**Multiple Metrics:**
```sql
SELECT device_id,
       last(temperature) AS latest_temp,
       last(humidity) AS latest_humidity,
       last(ts) AS last_update
FROM sensor_data
GROUP BY device_id;
```

## Template

```sql
SELECT
    <entity_column>,
    last(<metric>) AS latest_<metric>,
    last(ts) AS timestamp
FROM <table_name>
[WHERE ts >= '<time>']
GROUP BY <entity_column>;
```

## Common NL Patterns

| NL Pattern | SQL Pattern |
|------------|-------------|
| 最新温度 | `last(temperature)` |
| 最近一条记录 | `ORDER BY ts DESC LIMIT 1` |
| 每个设备的最新读数 | `last(col) GROUP BY device_id` |

## Notes

1. `last()` / `first()` exclude NULL values
2. `last_row()` / `first_row()` include NULL values
3. Combine with `last(ts)` to get the timestamp of the latest value
4. Often used with `GROUP BY` entity columns (device_id, location, etc.)
