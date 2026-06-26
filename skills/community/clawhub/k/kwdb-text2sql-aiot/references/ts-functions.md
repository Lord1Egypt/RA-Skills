# KWDB Functions Quick Reference

Function syntax reference. For query scenarios and routing, see `scenarios.md`.

## Time Functions

| Function | Syntax | Description |
|----------|--------|-------------|
| `time_bucket` | `time_bucket(ts, 'interval')` | Align timestamps to fixed intervals |
| `time_bucket_gapfill` | `time_bucket_gapfill(ts, 'interval')` | Align timestamps and fill gaps |
| `date_trunc` | `date_trunc('precision', ts)` | Truncate timestamp to precision |
| `now` | `now()` | Current timestamp (returns TIMESTAMPTZ) |
| `age` | `age(end, begin)` | Calculate time interval between timestamps |
| `to_timestamp` | `to_timestamp(val)` | Convert Unix epoch to timestamp |
| `experimental_strftime` | `experimental_strftime(ts, format)` | Format timestamp using strftime |

### date_trunc precision values
`millennium`, `century`, `decade`, `year`, `quarter`, `month`, `week`, `day`, `hour`, `minute`, `second`, `millisecond`, `microsecond`

### Additional timestamp functions
| Function | Syntax | Description |
|----------|--------|-------------|
| `current_timestamp` | `current_timestamp()` | Current transaction timestamp |
| `localtimestamp` | `localtimestamp()` | Current transaction timestamp (local) |
| `statement_timestamp` | `statement_timestamp()` | Current statement start time |
| `transaction_timestamp` | `transaction_timestamp()` | Current transaction time |
| `timeofday` | `timeofday()` | Current system time (string) |

## Time Intervals

Used with `time_bucket` and `time_bucket_gapfill`:

| Unit | Keyword | Example |
|------|---------|---------|
| Nanosecond | `ns`, `nsec`, `nanosecond` | `'500ns'` |
| Microsecond | `us`, `usec`, `microsecond` | `'100us'` |
| Millisecond | `ms`, `msec`, `millisecond` | `'500ms'` |
| Second | `s`, `sec`, `second` | `'30s'` |
| Minute | `m`, `min`, `minute` | `'5m'` |
| Hour | `h`, `hr`, `hour` | `'1h'` |
| Day | `d`, `day` | `'7d'` |
| Week | `w`, `week` | `'2w'` |
| Month | `mon`, `month` | `'3mon'` |
| Year | `y`, `yr`, `year` | `'1y'` |

## Aggregation Functions

| Function | Syntax | Description |
|----------|--------|-------------|
| `avg` | `avg(val)` | Average |
| `sum` | `sum(val)` | Sum |
| `count` | `count(*)` or `count(val)` | Count |
| `min` | `min(val)` | Minimum |
| `max` | `max(val)` | Maximum |
| `stddev` | `stddev(val)` | Standard deviation (N denominator for population, N-1 for sample) |
| `variance` | `variance(val)` | Population variance (stddev squared) |

Supported input types: `INT2`, `INT4`, `INT8`, `FLOAT4`, `FLOAT8`, `DECIMAL`

## First/Last Functions

| Function | Syntax | Description |
|----------|--------|-------------|
| `first` | `first(val)` | First non-null value by timestamp |
| `last` | `last(val)` | Last non-null value by timestamp |
| `first_row` | `first_row(val)` | First value including nulls |
| `last_row` | `last_row(val)` | Last value including nulls |

## Interpolation

| Function | Syntax | Description |
|----------|--------|-------------|
| `interpolate` | `interpolate(agg_func, mode)` | Fill missing values. Modes: `PREV`, `NEXT`, `'linear'`, `'constant'`, `NULL` |

Must be used with `time_bucket_gapfill()`. The `method` parameter must be an aggregate function with numeric data type.

## Time-Series Analysis

| Function | Syntax | Description |
|----------|--------|-------------|
| `TWA` | `TWA(ts, expr)` | Time-weighted average |
| `diff` | `diff(col) OVER (...)` | Difference from previous row |
| `ELAPSED` | `ELAPSED(ts [, unit])` | Time coverage in units |

## Window Functions

| Function | Syntax | Description |
|----------|--------|-------------|
| `TIME_WINDOW` | `TIME_WINDOW(ts, 'interval' [, 'slide'])` | Sliding time windows |
| `COUNT_WINDOW` | `COUNT_WINDOW(n [, slide])` | Fixed row count windows |
| `SESSION_WINDOW` | `SESSION_WINDOW(ts, 'interval')` | Session-based windows (time gaps) |
| `EVENT_WINDOW` | `EVENT_WINDOW(start_cond, end_cond)` | Event-based windows |
| `STATE_WINDOW` | `STATE_WINDOW(col)` | State-change windows |

## Date/Time Extraction

| Function | Syntax | Description |
|----------|--------|-------------|
| `extract` | `EXTRACT(field FROM ts)` | Extract timestamp part |
| `date_part` | `date_part('field', ts)` | Alternative extraction |

### extract/date_part fields
`year`, `month`, `day`, `hour`, `minute`, `second`, `epoch`, `millennium`, `century`, `decade`, `quarter`, `week`, `isoyear`, `dayofweek`, `isodow`, `dayofyear`, `julian`, `millisecond`, `microsecond`, `timezone`, `timezone_hour`, `timezone_minute`

## Math Functions

| Function | Syntax | Description |
|----------|--------|-------------|
| `abs` | `abs(val)` | Absolute value |
| `round` | `round(val)` | Round to nearest |
| `floor` | `floor(val)` | Round down |
| `ceil` | `ceil(val)` | Round up (alias: `ceiling`) |
| `sqrt` | `sqrt(val)` | Square root |
| `cbrt` | `cbrt(val)` | Cube root |
| `power` | `power(x, y)` | x to the power of y (alias: `pow`) |
| `exp` | `exp(val)` | e raised to the power of val |
| `log` | `log(val)` or `log(val, base)` | Logarithm (default base 10) |
| `ln` | `ln(val)` | Natural logarithm |
| `mod` | `mod(x, y)` | Modulo (remainder) |
| `div` | `div(x, y)` | Integer division |
| `sign` | `sign(val)` | Sign of value (-1, 0, 1) |
| `trunc` | `trunc(val)` | Truncate decimal |
| `pi` | `pi()` | Pi constant (~3.14159) |
| `random` | `random()` | Random float between 0 and 1 |
| `isnan` | `isnan(val)` | Check if value is NaN |

### Trigonometric Functions

| Function | Syntax | Description |
|----------|--------|-------------|
| `sin` | `sin(val)` | Sine (radians) |
| `cos` | `cos(val)` | Cosine (radians) |
| `tan` | `tan(val)` | Tangent (radians) |
| `cot` | `cot(val)` | Cotangent (radians) |
| `asin` | `asin(val)` | Inverse sine |
| `acos` | `acos(val)` | Inverse cosine |
| `atan` | `atan(val)` | Inverse tangent |
| `atan2` | `atan2(y, x)` | Inverse tangent of y/x |
| `degrees` | `degrees(val)` | Convert radians to degrees |
| `radians` | `radians(val)` | Convert degrees to radians |

### Hash Functions

| Function | Syntax | Description |
|----------|--------|-------------|
| `crc32c` | `crc32c(val)` | CRC32C checksum |
| `crc32ieee` | `crc32ieee(val)` | CRC32 IEEE checksum |
| `fnv32` | `fnv32(val)` | FNV-32 hash |
| `fnv32a` | `fnv32a(val)` | FNV-32a hash |
| `fnv64` | `fnv64(val)` | FNV-64 hash |
| `fnv64a` | `fnv64a(val)` | FNV-64a hash |

### width_bucket

| Function | Syntax | Description |
|----------|--------|-------------|
| `width_bucket` | `width_bucket(operand, b1, b2, count)` | Return bucket number of operand in histogram with count buckets |

## String Functions

| Function | Syntax | Description |
|----------|--------|-------------|
| `lower` | `lower(str)` | Convert to lowercase |
| `upper` | `upper(str)` | Convert to uppercase |
| `substring` | `substring(str, start [, len])` | Extract substring (aliases: `substr`) |
| `length` | `length(str)` | String length |
| `char_length` | `char_length(str)` | Character count (alias: `character_length`) |
| `bit_length` | `bit_length(str)` | Bit length |
| `octet_length` | `octet_length(str)` | Byte length |
| `trim` | `trim(str)` | Remove leading/trailing whitespace |
| `ltrim` | `ltrim(str)` | Remove leading whitespace |
| `rtrim` | `rtrim(str)` | Remove trailing whitespace |
| `concat` | `concat(str1, str2 [, ...])` | Concatenate strings (variadic) |
| `initcap` | `initcap(str)` | Capitalize first letter of each word |
| `left` | `left(str, n)` | First n characters |
| `right` | `right(str, n)` | Last n characters |
| `lpad` | `lpad(str, len [, fill])` | Left pad with spaces or fill |
| `rpad` | `rpad(str, len [, fill])` | Right pad with spaces or fill |
| `chr` | `chr(val)` | Character from ASCII code |
| `strpos` | `strpos(str, substr)` | Position of substring |
| `overlay` | `overlay(str1 PLACING str2 FROM pos FOR len)` | Replace substring |

## Conditional Functions

| Function | Syntax | Description |
|----------|--------|-------------|
| `COALESCE` | `COALESCE(val1, val2 [, ...])` | First non-null value |
| `NULLIF` | `NULLIF(val1, val2)` | NULL if val1 equals val2 |
| `IFNULL` | `IFNULL(val1, val2)` | val1 if not null, else val2 |
| `CASE WHEN` | `CASE WHEN cond THEN val1 ELSE val2 END` | Conditional expression |

## Geographic/Spatial Functions

| Function | Syntax | Description |
|----------|--------|-------------|
| `ST_Distance` | `ST_Distance(a, b)` | Euclidean distance between two points |
| `ST_DWithin` | `ST_DWithin(a, b, d)` | Check if distance between a and b is within d |
| `ST_Contains` | `ST_Contains(a, b)` | Check if geometry a contains geometry b |
| `ST_Intersects` | `ST_Intersects(a, b)` | Check if two geometries intersect |
| `ST_Equals` | `ST_Equals(a, b)` | Check if two geometries are equal |
| `ST_Touches` | `ST_Touches(a, b)` | Check if two geometries touch |
| `ST_Covers` | `ST_Covers(a, b)` | Check if geometry a covers geometry b |
| `ST_Area` | `ST_Area(geom)` | Calculate area of a polygon |

## Type Casting

Use `::type` for casting:

```sql
-- Cast to integer
value::INT
value::INT4
value::INT8

-- Cast to float
value::FLOAT4
value::FLOAT8
value::DOUBLE

-- Cast to string
value::VARCHAR
value::STRING
value::CHAR

-- Cast to timestamp
value::TIMESTAMP
value::TIMESTAMPTZ

-- Cast to boolean
value::BOOL

-- Cast to date
value::DATE
```

**Note on timestamp casting**: When the timestamp column in a time-series table is set to TIMESTAMP type, the system automatically converts it to TIMESTAMPTZ. Casting operations on this column will be processed according to the database timezone setting.

**Common patterns:**
```sql
-- String to timestamp
'2024-01-15'::TIMESTAMP

-- Integer to timestamp (Unix epoch)
1705315200::TIMESTAMP

-- Timestamp to date
ts::DATE

-- Keep only date part
date_trunc('day', ts)
```

## Special SQL Syntax Forms

Compatible SQL standard syntax that KWDB supports:

| Special Form | Equivalent To | Description |
|--------------|---------------|-------------|
| `AT TIME ZONE` | `timezone()` | Timezone conversion |
| `CURRENT_DATE` | `current_date()` | Current date |
| `CURRENT_TIME` | `current_time()` | Current time |
| `CURRENT_TIMESTAMP` | `current_timestamp()` | Current timestamp |
| `CURRENT_ROLE` / `CURRENT_USER` | `current_user()` | Current user |
| `CURRENT_SCHEMA` | `current_schema()` | Current schema |
| `SESSION_USER` | `current_user()` | Session user |
| `USER` | `current_user()` | Current user (abbreviated) |
| `CURRENT_CATALOG` | `current_database()` | Current database |
| `EXTRACT(field FROM ts)` | `extract(field, ts)` | Extract timestamp part |
| `EXTRACT_DURATION(field FROM val)` | `extract_duration(field, val)` | Extract duration part |
| `OVERLAY(str1 PLACING str2 FROM pos FOR len)` | `overlay(str1, str2, pos, len)` | Replace substring |
| `POSITION(substr IN str)` | `strpos(str, substr)` | Position of substring |
| `SUBSTRING(str FOR len)` | `substring(str, 1, len)` | Substring from start |
| `TRIM(chars FROM str)` | `btrim(str, chars)` | Trim characters |
| `TRIM(LEADING chars FROM str)` | `ltrim(str, chars)` | Trim leading characters |
| `TRIM(TRAILING chars FROM str)` | `rtrim(str, chars)` | Trim trailing characters |
| `COLLATION FOR` | `pg_collation_for()` | Collation for expression |

## Common Pitfalls

1. **SUM overflow**: Avoid letting SUM results exceed the maximum supported range
2. **Avoid escape character `+` in SUBSTRING regex**: Use `substr()` or `substring()` without regex patterns containing `+`
3. **time_bucket interval format**: Do NOT use compound interval format like `'1d1h'`
4. **NULL handling**: `last()` ignores NULLs, `last_row()` includes NULLs — choose based on data characteristics
5. **Trig functions use radians**: `sin()`, `cos()`, `tan()` etc. expect values in radians, not degrees
