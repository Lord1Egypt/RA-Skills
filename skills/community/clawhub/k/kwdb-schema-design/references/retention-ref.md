---
title: Time-Series Retention Reference
tier: 3
tags: [ddl, retention, time-series, data-lifecycle, retentions, auto-delete, storage-management, retention-units]
---

# Retention Reference

Quick reference for KWDB time-series retention policies. Read when designing time-series tables.

## Syntax

```sql
-- At creation
CREATE TABLE t (...) RETENTIONS 30d;

-- At modification
ALTER TABLE t SET RETENTIONS = 90d;

-- Viewing
SHOW RETENTIONS ON TABLE t;
```

## Time Units

| Unit | Abbreviation | Example |
|------|--------------|---------|
| Seconds | s, second | 3600s = 1 hour |
| Minutes | m, minute | 60m = 1 hour |
| Hours | h, hour | 24h = 1 day |
| Days | d, day | 7d = 1 week |
| Weeks | w, week | 4w = 1 month |
| Months | mon, month | 6mon = 6 months |
| Years | y, year | 1y = 1 year |

**Max**: 1000 years

## Default

- `0s` or `0` = **Permanent** (no auto-deletion)
- **Assumption if not specified**: `180d` (半年)

## Retention Selection

| Use Case | Retention |
|----------|-----------|
| Real-time monitoring | 7d - 30d |
| Daily aggregations | 90d - 1y |
| Compliance/logs | 1y - 7y |
| Historical analysis | 0s (permanent) |
| Sensor data (typical) | 180d (半年) - 1y |

## Key Rules

1. **Table level > Database level**
2. **Data exceeding retention is silently dropped**
3. **Always use explicit unit** (30d not 30)

## Common Mistakes

| Wrong | Right |
|--------|--------|
| RETENTIONS 30 | RETENTIONS 30d |
| RETENTIONS 1h for historical data | RETENTIONS 90d |
| No retention on high-volume IoT | RETENTIONS 30d |

## Storage Estimation

```
Storage ≈ bytes_per_record × records_per_second × seconds_in_retention
```

## Best Practice

Always include time filter in queries:

```sql
-- WRONG: May scan entire table
SELECT * FROM sensors;

-- RIGHT: Time-bound query
SELECT * FROM sensors
WHERE k_timestamp >= NOW() - INTERVAL '7 days';
```

## Design Checklist

- [ ] Business retention requirement is known
- [ ] Storage impact estimated
- [ ] Time unit explicitly specified
- [ ] Query patterns align with retention
