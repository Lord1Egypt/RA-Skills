# Time Series Interpolation

Fill missing values in time-series data using `time_bucket_gapfill()` and `interpolate()`.

## When to Use

Use for: "填充缺失值", "线性插值", "前值填充", "补全数据"

## time_bucket_gapfill + interpolate

```sql
time_bucket_gapfill(timestamp_column, 'interval')
interpolate(aggregate_function, mode)
```

## Interpolation Modes

| Mode | Description |
|------|-------------|
| `PREV` | Use previous value |
| `NEXT` | Use next value |
| `'linear'` | Linear interpolation |
| `'constant'` | Use a constant value |
| `NULL` | Fill with NULL (no fill) |

## Examples

**Linear Interpolation:**
```sql
SELECT time_bucket_gapfill(ts, '1h') AS hour,
       interpolate(avg(temperature), 'linear') AS temp
FROM sensor_data
WHERE ts >= NOW() - INTERVAL '1 day'
GROUP BY hour
ORDER BY hour;
```

**Previous Value Fill:**
```sql
SELECT time_bucket_gapfill(ts, '30m') AS bucket,
       interpolate(avg(pressure), PREV) AS pressure
FROM readings
WHERE ts >= '2024-01-15' AND ts < '2024-01-16'
GROUP BY bucket
ORDER BY bucket;
```

**Constant Fill:**
```sql
SELECT time_bucket_gapfill(ts, '1h') AS hour,
       interpolate(avg(value), '0') AS value
FROM metrics
WHERE ts >= NOW() - INTERVAL '7 days'
GROUP BY hour
ORDER BY hour;
```

## Template

```sql
SELECT
    time_bucket_gapfill(ts, '<interval>') AS bucket,
    interpolate(<aggregation>(<column>), '<mode>') AS <column>_filled
FROM <table_name>
WHERE ts >= '<start_time>' AND ts < '<end_time>'
GROUP BY bucket
ORDER BY bucket;
```

## Notes

1. Must be used with `GROUP BY` and aggregate functions
2. `interpolate()` requires an aggregate function as first parameter
3. `time_bucket_gapfill()` creates buckets even where no data exists
4. Choose mode based on data characteristics:
   - `linear` — continuous data (temperature, pressure)
   - `PREV` — step-like data (on/off states)
   - `'constant'` — fill with known default value
