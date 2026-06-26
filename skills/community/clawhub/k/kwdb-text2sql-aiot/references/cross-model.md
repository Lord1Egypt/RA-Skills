# Cross-Model Query Reference

Queries that join relational and time-series tables in KWDB.

## KWDB Multi-Model Architecture

- **Relational Tables**: Standard SQL tables with primary keys
- **Time-Series Tables**: Tables with timestamp and tag columns
- **Cross-Model Queries**: JOIN between relational and time-series tables

## Join Types Supported

| Join Type | Keyword | Description |
|-----------|---------|-------------|
| Inner Join | `INNER JOIN` or `JOIN` | Only matching rows |
| Left Join | `LEFT JOIN` | All left + matching right |
| Right Join | `RIGHT JOIN` | Matching left + all right |
| Full Join | `FULL JOIN` | All rows from both tables |

### FULL JOIN Constraint

When using `FULL JOIN`, **avoid subqueries in the join condition**:

```sql
-- Avoid (may cause issues):
SELECT * FROM a FULL JOIN (SELECT ... FROM b WHERE ...) AS sub ON a.id = sub.id

-- Prefer:
SELECT * FROM a FULL JOIN b ON a.id = b.id
```

## Unsupported Joins

- Cross Join (Cartesian product)

## Subqueries Supported

KWDB supports the following subquery types in cross-model queries:
- **Correlated subquery**: Inner query depends on outer query results
- **Non-correlated subquery**: Inner query runs independently, executes once
- **Correlated scalar subquery**: Returns a single value based on outer query
- **Non-correlated scalar subquery**: Independent, returns single value
- **FROM subquery**: Full SQL query nested in FROM clause as a temp table

## Common Patterns

### Join on Primary Tag

Time-series tables typically join on their primary tag:

```sql
relational_table.id = timeseries_table.primary_tag
```

### Example: Device Info with Latest Readings

```sql
-- Input: "Get device names with their latest temperature readings"
SELECT
    d.device_name,
    d.location,
    t.latest_temp,
    t.ts AS reading_time
FROM devices d
INNER JOIN (
    SELECT
        device_id,
        last(temperature) AS latest_temp,
        last(ts) AS ts
    FROM sensor_data
    GROUP BY device_id
) t ON d.device_id = t.device_id;
```

### Example: Product Catalog with Sales Statistics

```sql
-- Input: "Show product details with total sales in the last month"
SELECT
    p.product_id,
    p.product_name,
    p.category,
    COALESCE(s.total_quantity, 0) AS total_sold,
    COALESCE(s.total_revenue, 0) AS total_revenue
FROM products p
LEFT JOIN (
    SELECT
        product_id,
        sum(quantity) AS total_quantity,
        sum(quantity * price) AS total_revenue
    FROM sales
    WHERE sale_date >= NOW() - INTERVAL '1 month'
    GROUP BY product_id
) s ON p.product_id = s.product_id
ORDER BY total_revenue DESC;
```

### Example: Location-Based Aggregation

```sql
-- Input: "Calculate average temperature per location"
SELECT
    d.location,
    avg(t.temperature) AS avg_temp,
    count(*) AS reading_count
FROM locations d
INNER JOIN sensor_data t ON d.device_id = t.device_id
WHERE t.ts >= NOW() - INTERVAL '24 hours'
GROUP BY d.location
ORDER BY avg_temp DESC;
```

### Example: Real-Time Monitoring Dashboard

```sql
-- Input: "Create a dashboard view with device status and current readings"
SELECT
    d.device_id,
    d.device_name,
    d.status AS device_status,
    s.temperature,
    s.humidity,
    s.pressure,
    s.ts AS last_update
FROM devices d
LEFT JOIN (
    SELECT
        device_id,
        last(temperature) AS temperature,
        last(humidity) AS humidity,
        last(pressure) AS pressure,
        last(ts) AS ts
    FROM sensor_data
    WHERE ts >= NOW() - INTERVAL '1 hour'
    GROUP BY device_id
) s ON d.device_id = s.device_id
ORDER BY d.device_id;
```

### Example: Time-Series with Relational Filter

```sql
-- Input: "Get temperature trends for active devices only"
SELECT
    time_bucket(t.ts, '1h') AS hour,
    d.device_name,
    avg(t.temperature) AS avg_temp
FROM sensor_data t
INNER JOIN devices d ON t.device_id = d.device_id
WHERE d.status = 'active'
  AND t.ts >= NOW() - INTERVAL '7 days'
GROUP BY hour, d.device_name
ORDER BY hour, d.device_name;
```

## Multi-Model Optimization

KWDB optimizes cross-model queries by:

1. Pushing aggregations to time-series engine
2. Reducing data transfer between engines
3. Using BatchLookupJoin for efficient joins

### Enabling Optimization

```sql
-- Session level (default: enabled)
SET enable_multimodel = true;

-- Cluster level
SET CLUSTER SETTING sql.defaults.multimodel.enabled = true;
```

## Template

```sql
-- Basic cross-model join
SELECT
    r.<relational_column>,
    t.<timeseries_column>,
    t.<measurement>
FROM <relational_table> r
[JOINTYPE] JOIN (
    SELECT
        <primary_tag>,
        <aggregation>(<measurement>) AS <alias>
    FROM <timeseries_table>
    WHERE <timestamp> >= '<start_time>'
    GROUP BY <primary_tag>
) t ON r.<join_column> = t.<primary_tag>
[WHERE <additional_filters>]
[ORDER BY <order_columns>];
```

## Union Queries

KWDB also supports UNION-based set operations in cross-model queries:

| Operation | Description |
|-----------|-------------|
| `UNION` | Combine results, remove duplicates |
| `UNION ALL` | Combine results, keep all rows |
| `INTERSECT` | Return rows in both results, remove duplicates |
| `INTERSECT ALL` | Return rows in both results, keep duplicates |
| `EXCEPT` | Return rows only in the first result, remove duplicates |
| `EXCEPT ALL` | Return rows only in the first result, keep duplicates |

**Example:**
```sql
-- List all devices that are either smart meters or have fault status
SELECT deviceID, deviceName, 'smart_meter' AS category
FROM rdb.Device
WHERE modelID IN (101, 102)
UNION ALL
SELECT d.deviceID, d.deviceName, 'fault_device' AS category
FROM rdb.Device d
INNER JOIN tsdb.MonitoringCenter mc ON d.deviceID = mc.deviceID
WHERE mc.status = -1
ORDER BY deviceID;
```

## Notes

1. Join on Primary Tag columns for best performance
2. Use LEFT JOIN when relational data might not have matching time-series
3. Filter time-series data before joining when possible
4. KWDB automatically optimizes cross-model queries
5. Include appropriate WHERE clauses to limit data scope
6. `FULL JOIN` does not support subqueries in join conditions — use direct table join instead