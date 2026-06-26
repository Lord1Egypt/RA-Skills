# Time Series Downsampling

Downsampling time-series data by fixed time intervals using `time_bucket()`.

## When to Use

Use for: "每小时的平均值", "每天的统计", "降采样到1分钟"

**Do NOT use `TIME_WINDOW()` here** — use `time_bucket()` for fixed-interval downsampling (performance optimized).

## time_bucket Function

```sql
time_bucket(timestamp_column, 'interval')
```

### Parameters

| Parameter | Description |
|-----------|-------------|
| timestamp_column | The timestamp column (e.g., `ts`) |
| interval | Support `ns`,`us`,`ms`,`s`,`m`,`h`,`day`,`week`,`mon`,`y` (e.g. `20ms`,`60s`) |

## Examples

**Hourly Average:**
```sql
SELECT time_bucket(ts, '1h') AS hour, avg(temperature) AS avg_temp
FROM sensor_data
WHERE ts >= NOW() - INTERVAL '1 day'
GROUP BY hour
ORDER BY hour;
```

**Daily Max/Min:**
```sql
SELECT time_bucket(ts, '1d') AS day,
       max(temperature) AS max_temp,
       min(temperature) AS min_temp
FROM sensor_data
WHERE ts >= NOW() - INTERVAL '7 days'
GROUP BY day
ORDER BY day;
```

**15-Minute Intervals:**
```sql
SELECT time_bucket(ts, '15m') AS bucket,
       device_id,
       avg(humidity) AS avg_humidity
FROM sensor_data
WHERE ts >= NOW() - INTERVAL '24 hours'
GROUP BY bucket, device_id
ORDER BY bucket, device_id;
```

## Template

```sql
SELECT
    time_bucket(ts, '<interval>') AS period,
    <group_column>,
    <aggregation>(<metric>) AS <alias>
FROM <table_name>
WHERE ts >= NOW() - INTERVAL '<duration>'
GROUP BY period, <group_column>
ORDER BY period, <group_column>;
```

## Time Intervals

| Interval | Keyword | Use Case |
|----------|---------|----------|
| 1 second | `'1s'` | High-frequency data |
| 1 minute | `'1m'` | Real-time monitoring |
| 5 minutes | `'5m'` | Standard monitoring |
| 1 hour | `'1h'` | Hourly reports |
| 1 day | `'1d'` | Daily aggregation |
| 1 week | `'1w'` | Weekly reports |
| 1 month | `'1mon'` | Monthly analysis |

## time_bucket vs time_bucket_gapfill

| 场景 | 推荐函数 |
|------|---------|
| 数据无缺失，正常时间对齐 | `time_bucket()` |
| 数据存在缺失时间点，需返回完整时间序列 | `time_bucket_gapfill()` |
| 缺失时间点需要补值（线性插值） | `time_bucket_gapfill()` + `interpolate()` |

### 何时用 time_bucket

`time_bucket` 仅对时间戳进行对齐，**不会填充缺失的时间桶**。适用于数据采集连续、无缺失的场景。

- 查询每小时的平均值（数据完整）
- 每天的统计汇总
- 对数据做固定间隔的降采样

### 何时用 time_bucket_gapfill

`time_bucket_gapfill` 除了对齐时间戳外，**会自动填充缺失的时间桶行**。必须与 `GROUP BY` 配合使用。

典型场景：
- 设备定期上报数据，但某些时间点缺失，需要展示完整时间线
- 绘制时间序列图时，需要保证每个时间间隔都有数据点
- 配合 `interpolate()` 函数对缺失值进行线性补值

```sql
-- 使用 time_bucket_gapfill 填充缺失时间桶，配合 interpolate 补值
SELECT
    time_bucket_gapfill(ts, '1h') AS hour,
    interpolate(temperature) AS temp
FROM sensor_data
WHERE ts >= NOW() - INTERVAL '1 day'
GROUP BY hour
ORDER BY hour;
```

## Notes

1. Use `time_bucket()` for fixed-interval downsampling (not `TIME_WINDOW`)
2. Always include `GROUP BY time_bucket(...)` or `GROUP BY time_bucket_gapfill(...)`
3. Use `ORDER BY` for predictable output ordering
4. Combine with aggregate functions: `avg`, `sum`, `count`, `min`, `max`, `stddev`
5. `time_bucket_gapfill()` 必须与 `GROUP BY` 配合使用
6. `time_bucket_gapfill()` 可与 `interpolate()` 配合填充数据列的空值
