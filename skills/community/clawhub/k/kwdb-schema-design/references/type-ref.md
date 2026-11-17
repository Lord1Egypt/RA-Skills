---
title: Data Type Reference
tier: 2
tags: [ddl, data-types, numeric, string, timestamp, type-selection, int4, int8, decimal, float4, float8, varchar, jsonb, uuid, bool, geometry]
---

# Data Type Reference

Quick reference for KWDB data types. Read when choosing column types.

## Numeric Types

| Type | Bytes | Range | Use When |
|------|-------|-------|----------|
| INT2 | 2 | ±32K | Small counts, ages |
| INT4 (INT) | 4 | ±2.1B | Default integer |
| INT8 (BIGINT) | 8 | ±9.2E18 | Large IDs, counters |
| DECIMAL(p,s) | Variable | Exact | **Money/currency** (ALWAYS) |
| FLOAT4 | 4 | ~7 digits | Low-precision measurements (temp, humidity) |
| FLOAT8 | 8 | ~17 digits | Measurements (default float) |
| BOOL | 1 | true/false | Flags |

## String Types

| Type | Max Length | Use When |
|------|------------|----------|
| VARCHAR(n) | 65,534 | **Default** for text |
| CHAR(n) | 1,023 | Fixed-length codes only |
| JSONB | - | Structured/semi-structured data |
| ARRAY[T] | 1-D | Simple lists (no index support) |
| BLOB | 64MB | Binary files |
| CLOB | 64MB | Long text |

## Time Types

| Type | Use When |
|------|----------|
| TIMESTAMPTZ | **Time-series tables**, timezone matters |
| TIMESTAMP | Business dates without timezone |
| DATE | Date only (no time) |
| TIME | Time only (rare) |

### Timestamp Precision

| Precision | Syntax | Use When |
|-----------|--------|----------|
| Millisecond | `TIMESTAMPTZ(3)` | **Default** — most IoT sensors, general monitoring |
| Microsecond | `TIMESTAMPTZ(6)` | High-frequency trading, network packet analysis, precision industrial control |
| Nanosecond | `TIMESTAMPTZ(9)` | Scientific instruments, particle physics, ultra-low-latency systems |

**Note**: Higher precision increases storage. Choose the lowest precision that meets your requirements.

## Special Types

| Type | Use When |
|------|----------|
| UUID | Distributed IDs, global uniqueness |
| INET | IP addresses |
| GEOMETRY (TS only) | Spatial data (POINT/LINESTRING/POLYGON) |

## Type Selection Quick Table

| Data | Right | Wrong |
|------|-------|-------|
| User IDs | INT8 or UUID | VARCHAR for ID |
| Money | DECIMAL(10,2) | FLOAT/DOUBLE |
| Sensor readings | FLOAT8 | DECIMAL |
| Names | VARCHAR(100) | CHAR(1000) |
| Status codes | VARCHAR(20) or INT | - |
| JSON payloads | JSONB | VARCHAR |
| Timestamps (TS) | TIMESTAMPTZ | DATE |
| Booleans | BOOL | INT ('1'/'0') |

## Common Mistakes

### Error vs Correct Examples

**Incorrect:**
```sql
CREATE TABLE products (
    id VARCHAR(50) PRIMARY KEY,       -- VARCHAR as ID: bad index performance
    price FLOAT,                       -- FLOAT for money: precision loss
    name CHAR(200),                    -- CHAR wastes space
    description VARCHAR,               -- No length specified
    is_active INT,                     -- INT as boolean
    metadata TEXT                      -- TEXT for JSON
);
```

**Correct:**
```sql
CREATE TABLE products (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,  -- UUID for ID
    price DECIMAL(10,2) NOT NULL,                     -- DECIMAL for money
    name VARCHAR(200) NOT NULL,                       -- VARCHAR for variable text
    description VARCHAR(2000),                        -- Explicit max length
    is_active BOOL NOT NULL DEFAULT true,             -- BOOL for boolean
    metadata JSONB                                    -- JSONB for structured data
);
```

**Incorrect (time-series):**
```sql
CREATE TABLE sensor (
    k_timestamp TIMESTAMP NOT NULL,    -- TIMESTAMP without TZ
    temperature DECIMAL(5,2),          -- DECIMAL not ideal for measurements
    tags JSONB                         -- JSONB not supported in TS
) TAGS (
    sensor_id INT4 NOT NULL
) PRIMARY TAGS (sensor_id);
```

**Correct (time-series):**
```sql
CREATE TABLE sensor (
    k_timestamp TIMESTAMPTZ(3) NOT NULL,  -- TIMESTAMPTZ with precision
    temperature FLOAT4 NOT NULL            -- FLOAT for measurements
) TAGS (
    sensor_id INT4 NOT NULL
) PRIMARY TAGS (sensor_id)
RETENTIONS 180d;
```

### Mistake Summary

| Wrong | Right | Impact |
|-------|-------|--------|
| `price FLOAT` | `price DECIMAL(10,2)` | 精度丢失导致金额错误 |
| `VARCHAR` (no length) | `VARCHAR(100)` | 存储规划不明确 |
| `CHAR(1000)` for variable text | `VARCHAR(1000)` | CHAR 固定长度浪费空间 |
| `id VARCHAR` | `id INT8` or `UUID` | 索引性能下降 3-5x |
| `is_active INT` | `is_active BOOL` | 语义不清，浪费空间 |
| `metadata TEXT` for JSON | `metadata JSONB` | 无法索引和查询 JSON |
| `TIMESTAMP` in TS table | `TIMESTAMPTZ(3)` | 无时区信息 |
| `DECIMAL` in TS data column | `FLOAT4`/`FLOAT8` | DECIMAL 不支持于 TS 表 |

## Time-Series Type Support

**Data Columns**:

| Supported | NOT Supported |
|-----------|---------------|
| TIMESTAMP/TIMESTAMPTZ | - |
| INT, BIGINT, FLOAT | DECIMAL |
| VARCHAR, CHAR, NCHAR | NVARCHAR |
| BOOL, GEOMETRY | JSONB, ARRAY |

**Tag Columns** (TAGS clause):

| Supported | NOT Supported |
|-----------|---------------|
| INT2, INT4, INT8 | UUID |
| FLOAT4, FLOAT8 | DATE |
| CHAR, VARCHAR | TIMESTAMPTZ |
| BOOL | DECIMAL, JSONB, ARRAY |

**Workaround**: Store dates as `VARCHAR(10)` (e.g., `'2024-01-15'`), UUIDs as `INT8` or `VARCHAR(36)`.
