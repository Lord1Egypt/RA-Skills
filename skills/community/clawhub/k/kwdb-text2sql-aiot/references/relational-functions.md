# KWDB Relational Functions Reference

Relational database functions for KWDB, following CockroachDB SQL dialect.

## Conditional Functions

- `COALESCE(val, ...)` - returns first non-NULL value
- `IF(cond, then, else)` - conditional evaluation
- `IFNULL(val, else)` - alias for COALESCE with two operands
- `NULLIF(val1, val2)` - returns NULL if val1 equals val2, else val1
- `CASE WHEN cond THEN val ... [ELSE val] END` - case expression

## Comparison Functions

- `between(val, low, high)` - val between low and high (inclusive)
- `greatest(val, ...)` - maximum value from list
- `least(val, ...)` - minimum value from list

## Type Casting

- `CAST(val AS type)` - cast value to type
- `type::type` - PostgreSQL-style cast notation (e.g., `col::INT`)

## Math Functions

- `abs(val)` - absolute value
- `avg(val)` - average (aggregate)
- `ceil(val)` / `ceiling(val)` - round up
- `cbrt(val)` - cube root
- `div(val, divisor)` - integer division
- `exp(val)` - e to the power of val
- `floor(val)` - round down
- `ln(val)` - natural logarithm
- `log(val)` / `log(val, base)` - logarithm (base 10 if single arg)
- `log2(val)` - logarithm base 2
- `log10(val)` - logarithm base 10
- `max(val)` - maximum (aggregate)
- `min(val)` - minimum (aggregate)
- `mod(val, divisor)` - modulo remainder
- `pi()` - pi constant (3.14159...)
- `power(val, exp)` / `pow(val, exp)` - val raised to power
- `random()` - random value between 0 and 1
- `round(val)` - round to nearest integer
- `setseed(val)` - set random seed
- `sign(val)` - sign of value (-1, 0, 1)
- `sqrt(val)` - square root
- `sum(val)` - sum (aggregate)
- `trunc(val)` - truncate decimal part

## Trigonometric Functions

- `acos(val)` - arc cosine
- `asin(val)` - arc sine
- `atan(val)` - arc tangent
- `atan2(y, x)` - arc tangent of y/x
- `cos(val)` - cosine
- `cot(val)` - cotangent
- `degrees(val)` - radians to degrees
- `radians(val)` - degrees to radians
- `sin(val)` - sine
- `tan(val)` - tangent

## Hyperbolic Functions

- `sinh(val)` - hyperbolic sine
- `cosh(val)` - hyperbolic cosine
- `tanh(val)` - hyperbolic tangent
- `arcsinh(val)` - inverse hyperbolic sine
- `arccosh(val)` - inverse hyperbolic cosine
- `arctanh(val)` - inverse hyperbolic tangent

## String Functions

- `char_length(val)` / `character_length(val)` - character count
- `concat(val, ...)` - concatenate values
- `concat_ws(sep, val, ...)` - concatenate with separator
- `initcap(string)` - capitalize first letter of each word
- `length(string)` - character length
- `lower(string)` - convert to lowercase
- `lpad(string, length)` / `lpad(string, length, fill)` - pad left
- `octet_length(val)` - byte length
- `bit_length(val)` - bit length
- `replace(string, from, to)` - replace substring
- `reverse(string)` - reverse string
- `rpad(string, length)` / `rpad(string, length, fill)` - pad right
- `left(string, n)` - first n characters
- `right(string, n)` - last n characters
- `rtrim(string)` / `rtrim(string, chars)` - trim right
- `ltrim(string)` / `ltrim(string, chars)` - trim left
- `btrim(string)` / `btrim(string, chars)` - trim both sides
- `split_part(string, delim, n)` - split and return nth part
- `strpos(string, substring)` - position of substring
- `substring(string, start)` / `substring(string, start, len)` - extract substring
- `trim(LEADING|TRAILING|BOTH chars FROM string)` - trim characters
- `upper(string)` - convert to uppercase
- `overlay(string PLACING new FROM start FOR count)` - replace substring
- `format(text, val, ...)` - format string (printf-style)
- `md5(string)` - MD5 hash
- `sha256(string)` - SHA-256 hash
- `chr(val)` - character from ASCII code

## Array Functions

- `array_append(array, elem)` - append element
- `array_prepend(elem, array)` - prepend element
- `array_cat(left, right)` - concatenate arrays
- `array_dims(array)` - dimensions as text
- `array_length(array, dim)` - length of dimension
- `array_lower(array, dim)` - lower bound
- `array_upper(array, dim)` - upper bound
- `array_to_string(array, sep)` - array to string
- `cardinality(array)` - element count
- `string_to_array(string, sep)` / `string_to_array(string, sep, null)` - split to array
- `unnest(array)` - expand array to rows
- `generate_series(start, stop)` / `generate_series(start, stop, step)` - generate series

## Date and Time Functions

- `age(timestamp)` - interval between timestamp and current date
- `current_date` - current date
- `current_time` - current time
- `current_timestamp` - current timestamp
- `localtime` - current local time
- `localtimestamp` - current local timestamp
- `clock_timestamp()` - current timestamp (变化)
- `now()` - current timestamp
- `statement_timestamp()` - statement start time
- `transaction_timestamp()` - transaction start time
- `timeofday()` - current time as text
- `date_part(text, timestamp)` - extract part
- `date_trunc(text, timestamp)` - truncate to precision
- `extract(part FROM timestamp)` - extract field
- `make_date(year, month, day)` - create date
- `make_time(hour, min, sec)` - create time
- `make_timestamp(...)` - create timestamp
- `make_interval(...)` - create interval
- `make_timestamptz(...)` - create timestamptz
- `isfinite_date(date)` / `isfinite_timestamp(timestamp)` - check if finite

## ID Generation Functions

- `gen_random_uuid()` - generate random UUID
- `uuid_generate_v4()` - generate UUID v4

## Network Functions

- `host(inet)` - extract host from inet
- `masklen(inet)` - mask length
- `netmask(inet)` - network mask
- `network(inet)` - network address

## JSONB Functions

- `jsonb_build_array(...)` - build JSON array
- `jsonb_build_object(...)` - build JSON object
- `jsonb_extract_path(jsonb, path)` - extract path
- `jsonb_object_keys(jsonb)` - object keys
- `jsonb_populate_record(record, jsonb)` - populate record
- `jsonb_pretty(jsonb)` - formatted JSON
- `jsonb_set(jsonb, path, value)` - set value
- `jsonb_typeof(jsonb)` - JSON type
- `jsonb_each(jsonb)` - expand object to rows

## System Information Functions

- `current_catalog()` / `current_database()` - current database
- `current_schema()` - current schema
- `current_schemas(boolean)` - visible schemas
- `current_user()` / `session_user()` / `user` - current user
- `version()` - database version
- `current_setting(name)` - get setting
- `set_config(name, value, is_local)` - set configuration
- `pg_column_size(any)` - column size in bytes
- `pg_database_size(oid)` - database size
- `pg_relation_size(relation)` - relation size
- `pg_table_size(relation)` - table size
- `pg_indexes_size(relation)` - indexes size
- `pg_typeof(val)` - type of value
- `pg_encoding_to_char(encoding)` - encoding name
- `quote_ident(val)` - properly quoted identifier
- `quote_literal(val)` - properly quoted literal

## Sequence Functions

- `nextval(regclass)` - next value in sequence
- `currval(regclass)` - last value returned
- `lastval()` - last value returned
- `setval(regclass, count)` / `setval(regclass, count, is_called)` - set sequence value

## Aggregate Functions

- `array_agg(val)` - collect values into array
- `avg(val)` - average
- `bit_and(val)` - bitwise AND
- `bit_or(val)` - bitwise OR
- `bit_xor(val)` - bitwise XOR
- `bool_and(val)` / `every(val)` - boolean AND
- `bool_or(val)` - boolean OR
- `count(*)` - count all rows
- `count(val)` - count non-NULL values
- `jsonb_agg(val)` - aggregate to JSON array
- `jsonb_object_agg(key, value)` - aggregate to JSON object
- `string_agg(val, separator)` - concatenate with separator
- `sum(val)` - sum
- `stddev(val)` / `stddev_pop(val)` / `stddev_samp(val)` - standard deviation
- `variance(val)` / `var_pop(val)` / `var_samp(val)` - variance

## Window Functions

- `row_number()` - sequential row number
- `rank()` - rank with gaps
- `dense_rank()` - rank without gaps
- `percent_rank()` - relative rank (0-1)
- `cume_dist()` - cumulative distribution
- `ntile(n)` - divide into n buckets
- `lag(val)` / `lag(val, n)` / `lag(val, n, default)` - previous row value
- `lead(val)` / `lead(val, n)` / `lead(val, n, default)` - next row value
- `first_value(val)` - first value in window
- `last_value(val)` - last value in window
- `nth_value(val, n)` - nth value in window

## Special SQL Syntax Forms

| Special Form | Equivalent To |
|--------------|---------------|
| `AT TIME ZONE` | `timezone()` |
| `CURRENT_CATALOG` | `current_database()` |
| `CURRENT_DATE` | `current_date()` |
| `CURRENT_ROLE` | `current_user()` |
| `CURRENT_SCHEMA` | `current_schema()` |
| `CURRENT_TIMESTAMP` | `current_timestamp()` |
| `CURRENT_TIME` | `current_time()` |
| `CURRENT_USER` | `current_user()` |
| `EXTRACT(part FROM value)` | `extract(part, value)` |
| `EXTRACT_DURATION(part FROM value)` | `extract_duration(part, value)` |
| `OVERLAY(text1 PLACING text2 FROM int1 FOR int2)` | `overlay(text1, text2, int1, int2)` |
| `SUBSTRING(text FROM start FOR count)` | `substr(text, start, count)` |
| `TRIM(LEADING\|TRAILING\|BOTH chars FROM text)` | `ltrim/rtrim/btrim(text, chars)` |
| `POSITION(text1 IN text2)` | `strpos(text2, text1)` |
| `NEXTVAL(seq)` | `nextval(seq)` |
| `DATE_TRUNC(text, timestamp)` | `date_trunc(text, timestamp)` |
| `TREAT(expr AS type)` | type cast |
| `session_user` | `current_user()` |
| `COLLATION FOR` | `pg_collation_for()` |
