# Window Functions and Event Detection

Sliding windows, session windows, event windows, and advanced time-series analysis.

## When to Use

| Scenario | Function |
|----------|----------|
| Sliding window (overlapping) | `TIME_WINDOW()` |
| Session-based grouping (time gaps) | `SESSION_WINDOW()` |
| Event-based grouping (conditions) | `EVENT_WINDOW()` |
| Count-based grouping | `COUNT_WINDOW()` |
| State-change grouping | `STATE_WINDOW()` |

**Do NOT use `TIME_WINDOW()` for fixed-interval downsampling** — use `time_bucket()` instead (see ts-downsampling.md).

## TIME_WINDOW (Sliding)

```sql
TIME_WINDOW(timestamp_column, 'interval')
TIME_WINDOW(timestamp_column, 'interval', 'sliding_interval')
```

Sliding windows with overlapping time intervals.

**Example:**
```sql
SELECT TIME_WINDOW(ts, '1h', '15m') AS window,
       device_id,
       avg(temperature) AS avg_temp
FROM sensor_data
WHERE ts >= NOW() - INTERVAL '24 hours'
GROUP BY window, device_id
ORDER BY window;
```

## SESSION_WINDOW

Groups data by time gaps between records.

```sql
SESSION_WINDOW(timestamp_column, 'interval')
```

**Example:**
```sql
SELECT SESSION_WINDOW(ts, '5m') AS session,
       device_id,
       avg(temperature) AS avg_temp
FROM sensor_data
GROUP BY session, device_id
ORDER BY session;
```

## EVENT_WINDOW

Groups data based on start and end conditions.

```sql
EVENT_WINDOW(start_condition, end_condition)
```

**Example:**
```sql
SELECT EVENT_WINDOW(temperature > 100, temperature <= 100) AS event,
       count(*) AS records_in_event,
       max(temperature) AS peak_temp
FROM sensor_data
GROUP BY event;
```

**Detect temperature anomaly events:**
```sql
SELECT EVENT_WINDOW(temp > 80, temp <= 80) AS anomaly,
       device_id,
       count(*) AS duration,
       max(temp) AS max_temp
FROM sensor_data
GROUP BY anomaly, device_id
HAVING max(temp) > 80;
```

## COUNT_WINDOW

Groups data by fixed number of rows.

```sql
COUNT_WINDOW(row_limit)
COUNT_WINDOW(row_limit, sliding_rows)
```

**Example:**
```sql
SELECT COUNT_WINDOW(10) AS window,
       avg(value) AS avg_value,
       count(*) AS record_count
FROM sensor_data
GROUP BY window;
```

## STATE_WINDOW

Groups data by state changes.

```sql
STATE_WINDOW(column)
```

**Example:**
```sql
SELECT STATE_WINDOW(status) AS status_segment,
       count(*) AS duration,
       avg(value) AS avg_value
FROM device_data
GROUP BY status_segment
ORDER BY status_segment;
```

## TWA (Time Weighted Average)

Calculates time-weighted average considering data intervals.

```sql
TWA(timestamp_column, expression)
```

**Example:**
```sql
SELECT time_bucket(ts, '1h') AS hour,
       TWA(ts, temperature) AS twa_temp
FROM sensor_data
GROUP BY hour
ORDER BY hour;
```

## diff() Function

Calculates difference from previous row.

```sql
diff(column) OVER (PARTITION BY column_list ORDER BY timestamp_column)
```

**Example:**
```sql
SELECT ts,
       temperature,
       diff(temperature) OVER (PARTITION BY device_id ORDER BY ts) AS temp_change
FROM sensor_data
WHERE device_id = 1;
```

## ELAPSED Function

Returns time coverage in specified units.

```sql
ELAPSED(timestamp_column [, time_unit])
```

**Example:**
```sql
SELECT time_bucket(ts, '1h') AS hour,
       ELAPSED(ts, 's') / 3600.0 AS coverage_ratio
FROM sensor_data
GROUP BY hour
ORDER BY hour;
```

## Quick Reference

| Function | Use Case | Syntax |
|----------|----------|--------|
| `TIME_WINDOW` | Sliding windows | `TIME_WINDOW(ts, '1h', '15m')` |
| `SESSION_WINDOW` | Session by time gaps | `SESSION_WINDOW(ts, '5m')` |
| `EVENT_WINDOW` | Event detection | `EVENT_WINDOW(cond, cond)` |
| `COUNT_WINDOW` | Fixed row count | `COUNT_WINDOW(10)` |
| `STATE_WINDOW` | State changes | `STATE_WINDOW(status)` |
| `TWA` | Time-weighted avg | `TWA(ts, col)` |
| `diff` | Difference | `diff(col) OVER (...)` |
| `ELAPSED` | Time coverage | `ELAPSED(ts, 's')` |

## Notes

1. Window functions require `GROUP BY`
2. Use `time_bucket()` for fixed-interval downsampling (not sliding)
3. `TWA()` is ideal for irregularly-spaced time-series data
4. `EVENT_WINDOW` is useful for anomaly or threshold detection
