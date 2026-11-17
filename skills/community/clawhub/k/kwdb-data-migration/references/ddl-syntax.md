# KaiwuDB DDL Syntax Reference

This document provides the complete and authoritative DDL syntax for creating KaiwuDB databases and tables, including real implementation details from the KDTS source code.

---

## 1. Database Creation

### 1.1 Time Series Database

**Syntax**:

```sql
CREATE TS DATABASE <database_name> [RETENTIONS <keep_duration>] [PARTITION INTERVAL <interval>];
```

**Parameters**:

| Parameter          | Required | Description             | Format                                            |
|--------------------|----------|-------------------------|---------------------------------------------------|
| database_name      | Yes      | Database name           | Max 128 bytes                                     |
| RETENTIONS         | No       | Data retention period   | `0d` (default, never expire), or specify duration |
| PARTITION INTERVAL | No       | Time partition interval | e.g., `1d`, `7d`, `1h`                            |

**Time Units for RETENTIONS and PARTITION INTERVAL**:

| Unit   | Keyword      | Example |
|--------|--------------|---------|
| Second | S or SECOND  | `3600S` |
| Minute | M or MINUTE  | `60M`   |
| Hour   | H or HOUR    | `24H`   |
| Day    | D or DAY     | `7D`    |
| Week   | W or WEEK    | `4W`    |
| Month  | MON or MONTH | `12MON` |
| Year   | Y or YEAR    | `1Y`    |

**Maximum value**: 1000 years, value must be integer.

**Examples**:

```sql
CREATE TS DATABASE sensor_data;

CREATE TS DATABASE sensor_data RETENTIONS 1Y;

CREATE TS DATABASE metrics RETENTIONS 30D PARTITION INTERVAL 1D;
```

### 1.2 Relational Database

**Syntax**:

```sql
CREATE DATABASE <database_name>;
```

**Example**:

```sql
CREATE DATABASE orders_db;
```

---

## 2. Time Series Table Syntax

### 2.1 Complete Syntax

```sql
CREATE TABLE <table_name> (
    <column_1> <data_type> [DEFAULT <value>],
    <column_2> <data_type> [DEFAULT <value>],
    ...
)
[TAGS | ATTRIBUTES] (
    <tag_1> <data_type> [NOT NULL],
    <tag_2> <data_type> [NOT NULL],
    ...
)
PRIMARY [TAGS | ATTRIBUTES] (<primary_tag_1>, <primary_tag_2>, ...)
[RETENTIONS <keep_duration>]
[ACTIVETIME <active_duration>]
[PARTITION INTERVAL <interval>]
[DICT ENCODING];
```

### 2.2 Parameter Descriptions

#### Table Name

- Max 128 bytes
- Must be unique within the database
- Follows identifier naming conventions

#### Column List (Data Columns)

- **Minimum**: 2 columns
- **Maximum**: 4096 columns
- **First column requirement**: MUST be `TIMESTAMP` or `TIMESTAMPTZ` with `NOT NULL`
- Column name: Max 128 bytes
- Default value rules:
  - Non-time columns: Only constant defaults allowed
  - Time columns (TIMESTAMP/TIMESTAMPTZ): Can use `now()` function or constant
- Time precision support: Milliseconds (default), Microseconds, Nanoseconds

#### Tag List (TAGS or ATTRIBUTES)

- **Minimum**: 1 tag (at least 1 PRIMARY TAG required)
- **Maximum**: 128 tags per table (source) + 4 primary tags = 132 total from source
- Tag name: Max 128 bytes (UTF-8, 128 bytes max)
- Can specify `NOT NULL`, defaults to nullable

**Forbidden Ordinary Tag Types** (from KDTS source):

- TIMESTAMP, TIMESTAMPTZ
- NVARCHAR
- GEOMETRY

**Auto-conversion**: If source tag type is forbidden, KDTS automatically converts it to VARCHAR.

#### Primary Tag List (PRIMARY TAGS or PRIMARY ATTRIBUTES)

- **Minimum**: 1 PRIMARY TAG (required, error 3006 if missing)
- **Maximum**: 4 PRIMARY TAGS per table (error 3004 if exceeded)
- PRIMARY TAGS MUST be defined in the tag list
- PRIMARY TAGS MUST specify `NOT NULL`
- PRIMARY TAGS CANNOT be modified after table creation

**Forbidden Primary Tag Types** (from KDTS source - TypeMapping.FLOAT_TYPE_NAMES + NON_VARCHAR_VARIABLE_LENGTH_TYPES):

- Floating point types: FLOAT, FLOAT4, FLOAT8, DOUBLE, REAL, BINARY_FLOAT, BINARY_DOUBLE
- **Note**: DECIMAL and NUMERIC are ALSO classified as float types by KDTS and forbidden as primary tags
- Non-VARCHAR variable-length types: NVARCHAR, NCHAR, TEXT, CLOB, BLOB, BYTES, VARBYTES, JSON, ARRAY, MAP, INET, INTERVAL, UUID

**Auto-conversion for Primary Tags**:

- If primary tag source type is forbidden (e.g., NVARCHAR, NCHAR, TEXT), KDTS automatically converts to VARCHAR(128)
- If primary tag VARCHAR length > 128, KDTS truncates to VARCHAR(128)
- If primary tag VARCHAR has no explicit length, KDTS defaults to VARCHAR(64)

#### Optional Table Parameters

| Parameter          | Default             | Description                                       | Format                           |
|--------------------|---------------------|---------------------------------------------------|----------------------------------|
| RETENTIONS         | `0d` (never expire) | Data retention period                             | Same units as database           |
| ACTIVETIME         | `1d`                | Time before data compression                      | Same units, `0` = no compression |
| PARTITION INTERVAL | System default      | Time partition interval                           | e.g., `1h`, `1d`                 |
| DICT ENCODING      | Disabled            | Enable dictionary encoding for better compression | Keyword only                     |

### 2.3 Tag Type Compatibility Table

| Data Type       | Ordinary Tag | Primary Tag | Auto-conversion Rule                                  |
|-----------------|:------------:|:-----------:|-------------------------------------------------------|
| BOOLEAN         |     Yes      |     Yes     | No conversion                                         |
| SMALLINT        |     Yes      |     Yes     | No conversion                                         |
| INT / INTEGER   |     Yes      |     Yes     | No conversion                                         |
| BIGINT          |     Yes      |     Yes     | No conversion                                         |
| REAL / FLOAT4   |     Yes      |   **No**    | Demoted to ordinary tag                               |
| DOUBLE / FLOAT8 |     Yes      |   **No**    | Demoted to ordinary tag                               |
| BINARY_FLOAT    |     Yes      |   **No**    | Demoted to ordinary tag                               |
| BINARY_DOUBLE   |     Yes      |   **No**    | Demoted to ordinary tag                               |
| DECIMAL(p,s)    |     Yes      |   **No**    | Demoted to ordinary tag (classified as float by KDTS) |
| NUMERIC(p,s)    |     Yes      |   **No**    | Demoted to ordinary tag (classified as float by KDTS) |
| CHAR(n)         |     Yes      |     Yes     | No conversion                                         |
| VARCHAR(n)      |     Yes      |     Yes     | Primary: defaults to 64B, max 128B                    |
| TEXT            |    **No**    |   **No**    | Converted to VARCHAR(128) if primary                  |
| TIMESTAMP       |    **No**    |   **No**    | Forbidden; converted to VARCHAR                       |
| TIMESTAMPTZ     |    **No**    |   **No**    | Forbidden; converted to VARCHAR                       |
| DATE            |    **No**    |   **No**    | Forbidden; converted to VARCHAR                       |
| TIME            |    **No**    |   **No**    | Forbidden; converted to VARCHAR                       |
| NVARCHAR        |    **No**    |   **No**    | Converted to VARCHAR(128) if primary                  |
| NCHAR           |     Yes      |   **No**    | Converted to VARCHAR(128) if primary                  |
| GEOMETRY        |    **No**    |   **No**    | Forbidden; converted to VARCHAR                       |
| JSON            |    **No**    |   **No**    | Converted to VARCHAR(128) if primary                  |
| JSONB           |     Yes      |   **No**    | Converted to VARCHAR(128) if primary                  |
| BYTES           |     Yes      |   **No**    | Converted to VARCHAR(128) if primary                  |
| VARBYTES        |     Yes      |   **No**    | Converted to VARCHAR(128) if primary                  |
| BLOB            |     Yes      |   **No**    | Converted to VARCHAR(128) if primary                  |
| ARRAY           |     Yes      |   **No**    | Converted to VARCHAR(128) if primary                  |
| MAP             |     Yes      |   **No**    | Converted to VARCHAR(128) if primary                  |
| UUID            |     Yes      |   **No**    | Converted to VARCHAR(128) if primary                  |
| INET            |     Yes      |   **No**    | Converted to VARCHAR(128) if primary                  |

### 2.4 Examples

#### Example 1: Basic Sensor Data Table

```sql
CREATE TABLE sensor_readings (
    ts TIMESTAMPTZ NOT NULL,
    temperature DOUBLE,
    humidity DOUBLE,
    pressure DOUBLE
)
TAGS (
    sensor_id BIGINT NOT NULL,
    location VARCHAR(100),
    device_type VARCHAR(50)
)
PRIMARY TAGS (sensor_id);
```

#### Example 2: Table with Multiple Primary Tags

```sql
CREATE TABLE order_metrics (
    ts TIMESTAMPTZ NOT NULL,
    order_count INT,
    total_amount DECIMAL(15,2),
    avg_processing_time DOUBLE
)
TAGS (
    tenant_id BIGINT NOT NULL,
    service_id BIGINT NOT NULL,
    region VARCHAR(50) NOT NULL,
    status VARCHAR(20)
)
PRIMARY TAGS (tenant_id, service_id, region);
```

#### Example 3: Table with Retention and Compression Settings

```sql
CREATE TABLE system_logs (
    ts TIMESTAMPTZ NOT NULL,
    log_level VARCHAR(20),
    message TEXT,
    duration_ms INT
)
TAGS (
    service_name VARCHAR(100) NOT NULL,
    host VARCHAR(100),
    cluster VARCHAR(50)
)
PRIMARY TAGS (service_name)
RETENTIONS '30d'
ACTIVETIME '7d'
PARTITION INTERVAL '1d';
```

#### Example 4: Table with Dictionary Encoding

```sql
CREATE TABLE network_metrics (
    ts TIMESTAMPTZ NOT NULL,
    bandwidth_usage DOUBLE,
    packet_loss DOUBLE,
    latency_ms INT
)
TAGS (
    network_id BIGINT NOT NULL,
    interface VARCHAR(30) NOT NULL,
    vlan VARCHAR(10)
)
PRIMARY TAGS (network_id, interface)
RETENTIONS '90d'
ACTIVETIME '1d'
DICT ENCODING;
```

---

## 3. KDTS Auto-Mapping Implementation Details (from Source Code)

### 3.1 Primary Tag Selection Algorithm

Based on KDTS source code (`KaiwuDBStrategy.java`), the primary tag selection follows these steps:

```
Step 1: Collect all source tags (isTag() = true)
Step 2: Validate total count <= 132 (128 tags + 4 primary tags)
Step 3: Sort tags by column order (preserve source order)
Step 4: Demote invalid primary tags in order:
        - FLOAT/FLOAT4/FLOAT8/DOUBLE/REAL types -> demote to ordinary tag
        - NULL/NULLABLE tags -> demote to ordinary tag
Step 5: Identify eligible primary tags (isEligibleForPrimaryTag):
        - NOT NULL
        - NOT FLOAT type
        - NOT over-length (VARCHAR > 128 bytes)
Step 6: If eligible count = 0 -> ERROR 3006 (no primary tag)
Step 7: Select min(eligible_count, 4) primary tags
Step 8: Promote eligible tags in order until target count reached
Step 9: If primary count > 4 -> demote from last to first until 4
```

### 3.2 Auto-Conversion Rules

| Scenario                           | Source Type                         | Target Type  | Action                               |
|------------------------------------|-------------------------------------|--------------|--------------------------------------|
| Primary tag is FLOAT/DOUBLE/REAL   | FLOAT, FLOAT4, FLOAT8, DOUBLE, REAL | Ordinary tag | Demote                               |
| Primary tag is BINARY_FLOAT/DOUBLE | BINARY_FLOAT, BINARY_DOUBLE         | Ordinary tag | Demote                               |
| Primary tag is DECIMAL/NUMERIC     | DECIMAL, NUMERIC                    | Ordinary tag | Demote (classified as float by KDTS) |
| Primary tag is NULL                | NULL                                | Ordinary tag | Demote with warning                  |
| Primary tag is NVARCHAR/NCHAR      | NVARCHAR, NCHAR                     | VARCHAR(128) | Convert with warning                 |
| Primary tag is TEXT/CLOB           | TEXT, CLOB                          | VARCHAR(128) | Convert with warning                 |
| Primary tag is JSON                | JSON, JSONB                         | VARCHAR(128) | Convert with warning                 |
| Primary tag VARCHAR > 128          | VARCHAR(200)                        | VARCHAR(128) | Truncate with warning                |
| Primary tag VARCHAR no length      | VARCHAR                             | VARCHAR(64)  | Default to 64                        |
| Ordinary tag is TIMESTAMP          | TIMESTAMP                           | VARCHAR      | Convert with warning                 |
| Ordinary tag is NVARCHAR           | NVARCHAR                            | VARCHAR      | Convert with warning                 |
| Ordinary tag is GEOMETRY           | GEOMETRY                            | VARCHAR      | Convert with warning                 |
| Primary count > 4                  | Multiple                            | Ordinary tag | Demote from last                     |

### 3.3 Error Handling

| Error Code | Description        | KDTS Behavior                    |
|------------|--------------------|----------------------------------|
| 3004       | Tag limit exceeded | ERROR if source tags > 132       |
| 3005       | Tag name too long  | ERROR if tag name > 128 bytes    |
| 3006       | No primary tag     | ERROR if no eligible primary tag |

### 3.4 Complete Flow Example

**Source (InfluxDB)**:
```
Measurement: cpu_usage
Tags (5): host, region, datacenter, service (FLOAT), priority (NVARCHAR)
Fields: usage, temperature, load_average
```

**KDTS Processing**:
```
Step 1: Collect tags -> [host, region, datacenter, service (FLOAT), priority (NVARCHAR)]

Step 2: Validate count -> 5 <= 132 ✓

Step 3: Sort by order -> Same as above

Step 4: Demote invalid primary tags:
        - service is FLOAT -> demote to ordinary tag
        - priority is NVARCHAR -> demote to ordinary tag (if originally primary)

Step 5: Identify eligible primary tags -> [host, region, datacenter] (all NOT NULL, NOT FLOAT, NOT over-length)

Step 6: Eligible count = 3 -> OK (>= 1)

Step 7: Primary target = min(3, 4) = 3

Step 8: Promote first 3 eligible tags -> host, region, datacenter as PRIMARY TAGS

Step 9: Ordinary tags = [service, priority]
        - service is FLOAT -> kept as ordinary tag (FLOAT is allowed for ordinary tags)
        - priority is NVARCHAR -> convert to VARCHAR (NVARCHAR is forbidden for ordinary tags)

Final DDL:
CREATE TABLE cpu_usage (
    time TIMESTAMPTZ NOT NULL,
    usage FLOAT8,
    temperature FLOAT8,
    load_average FLOAT8
)
TAGS (
    host VARCHAR(100) NOT NULL,
    region VARCHAR(50) NOT NULL,
    datacenter VARCHAR(50) NOT NULL,
    service FLOAT8,
    priority VARCHAR(128)
)
PRIMARY TAGS (host, region, datacenter);
```

---

## 4. Tag Management (ALTER TABLE)

### 4.1 Adding a New Tag

```sql
ALTER TABLE <table_name> ADD TAG <tag_name> <data_type> [NOT NULL];
```

**Example**:

```sql
ALTER TABLE sensor_readings ADD TAG firmware_version VARCHAR(20);
```

### 4.2 Modifying a Tag Type

```sql
ALTER TABLE <table_name> ALTER TAG <tag_name> TYPE <new_data_type>;
```

**Example**:

```sql
ALTER TABLE sensor_readings ALTER TAG firmware_version TYPE VARCHAR(50);
```

### 4.3 Renaming a Tag

```sql
ALTER TABLE <table_name> RENAME TAG <old_tag_name> TO <new_tag_name>;
```

**Example**:

```sql
ALTER TABLE sensor_readings RENAME TAG location TO deployment_location;
```

### 4.4 Dropping a Tag

```sql
ALTER TABLE <table_name> DROP TAG <tag_name>;
```

**Example**:

```sql
ALTER TABLE sensor_readings DROP TAG firmware_version;
```

**Note**: PRIMARY TAGS cannot be modified or dropped after table creation.

---

## 5. Index Management

### 5.1 Auto-created Indexes

KaiwuDB automatically creates **Hash indexes** for all PRIMARY TAGS:
- Supports O(1) time complexity for exact match queries
- Example: `SELECT * FROM sensor_readings WHERE sensor_id = 1005;`

### 5.2 Creating Indexes on Ordinary Tags

```sql
CREATE INDEX <index_name> ON <table_name> (<tag_name>);
```

**Example**:

```sql
CREATE INDEX idx_sensor_location ON sensor_readings (location);
```

### 5.3 Composite Indexes

- Maximum 4 columns per composite index
- Order columns by selectivity (most selective first)

```sql
CREATE INDEX idx_composite ON <table_name> (<tag_1>, <tag_2>, ...);
```

**Example**:

```sql
CREATE INDEX idx_tenant_service ON order_metrics (tenant_id, service_id);
```

---

## 6. Time Series Data Insertion Rules

### 6.1 Timestamp Format

Supported timestamp formats for data insertion:
```sql
-- Format 1: With dash and space
'2023-01-25 10:10:10.123'

-- Format 2: With dash only
'2023-01-25T10:10:10.123'

-- Format 3: With slash
'2023/01/25 10:10:10.123'

-- Precision: Milliseconds, Microseconds, Nanoseconds
'2023-01-25 10:10:10.123456'  -- Microseconds
'2023-01-25 10:10:10.123456789'  -- Nanoseconds
```

### 6.2 Duplicate Timestamp Handling

When inserting data with the same timestamp and primary tags:
- **Default behavior**: New data OVERWRITES existing data
- Can configure dedup rule: `SET CLUSTER SETTING ts.dedup.rule = 'merge' | 'override' | 'discard';`

### 6.3 Null Value Handling

- Tags without values: Auto-filled with NULL (if nullable)
- Tags with NOT NULL constraint: Insert fails with error
- Data columns without values: Auto-filled with default or NULL

---

## 7. Relational Table Syntax

### 7.1 Basic Syntax

```sql
CREATE TABLE <table_name> (
    <column_1> <data_type> [column_constraints],
    <column_2> <data_type> [column_constraints],
    ...
    [table_constraints]
);
```

### 7.2 Data Types

| Category      | Type            | Description                             |
|---------------|-----------------|-----------------------------------------|
| **Integer**   | SMALLINT        | 2-byte signed integer                   |
|               | INT / INTEGER   | 4-byte signed integer                   |
|               | BIGINT          | 8-byte signed integer                   |
|               | SERIAL          | Auto-increment INT                      |
|               | BIGSERIAL       | Auto-increment BIGINT                   |
|               | TINYINT         | 1-byte signed integer                   |
| **Float**     | REAL / FLOAT4   | 4-byte floating point                   |
|               | DOUBLE / FLOAT8 | 8-byte floating point                   |
| **Decimal**   | DECIMAL(p,s)    | Fixed precision decimal                 |
|               | NUMERIC(p,s)    | Same as DECIMAL                         |
| **String**    | CHAR(n)         | Fixed-length string                     |
|               | VARCHAR(n)      | Variable-length string, max 65535 bytes |
|               | TEXT            | Unlimited-length text                   |
| **Date/Time** | DATE            | Date only (YYYY-MM-DD)                  |
|               | TIME            | Time only (HH:MM:SS)                    |
|               | TIMESTAMP       | Date and time                           |
|               | TIMESTAMPTZ     | Date and time with timezone             |
|               | INTERVAL        | Time interval                           |
| **Boolean**   | BOOLEAN         | True/False                              |
| **Binary**    | BINARY(n)       | Fixed-length binary                     |
|               | VARBINARY(n)    | Variable-length binary                  |
|               | BLOB            | Binary large object, max 1GB            |
| **JSON**      | JSON            | JSON data                               |
|               | JSONB           | Binary JSON data                        |

### 7.3 Column Constraints

| Constraint  | Syntax                                      | Description                            |
|-------------|---------------------------------------------|----------------------------------------|
| NOT NULL    | `column_name type NOT NULL`                 | Column cannot be null                  |
| NULL        | `column_name type NULL`                     | Column allows null (default)           |
| DEFAULT     | `column_name type DEFAULT value`            | Default value                          |
| UNIQUE      | `column_name type UNIQUE`                   | All values must be distinct            |
| PRIMARY KEY | `column_name type PRIMARY KEY`              | Primary key (implies NOT NULL, UNIQUE) |
| REFERENCES  | `column_name type REFERENCES table(column)` | Foreign key reference                  |
| CHECK       | `column_name type CHECK (condition)`        | Value constraint                       |

### 7.4 Table Constraints

| Constraint  | Syntax                                    | Description                 |
|-------------|-------------------------------------------|-----------------------------|
| PRIMARY KEY | `PRIMARY KEY (col_1, col_2, ...)`         | Composite primary key       |
| UNIQUE      | `UNIQUE (col_1, col_2, ...)`              | Composite unique constraint |
| FOREIGN KEY | `FOREIGN KEY (col) REFERENCES table(col)` | Foreign key                 |
| CHECK       | `CHECK (condition)`                       | Table-level check           |

### 7.5 Examples

#### Example 1: Simple User Table

```sql
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) NOT NULL,
    full_name VARCHAR(200),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

#### Example 2: Table with Foreign Keys

```sql
CREATE TABLE orders (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    product_id BIGINT NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    unit_price DECIMAL(10,2) NOT NULL,
    total_price DECIMAL(15,2) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);
```

#### Example 3: Table with Check Constraint

```sql
CREATE TABLE products (
    id BIGSERIAL PRIMARY KEY,
    sku VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL CHECK (price > 0),
    stock INT DEFAULT 0 CHECK (stock >= 0),
    category VARCHAR(100),
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

### 7.6 Creating Indexes

```sql
CREATE INDEX <index_name> ON <table_name> (<column>);
CREATE UNIQUE INDEX <index_name> ON <table_name> (<column>);
```

**Example**:
```sql
CREATE INDEX idx_orders_user ON orders (user_id);
CREATE INDEX idx_orders_status ON orders (status);
CREATE INDEX idx_products_category ON products (category);
```

---

## 8. Cross-Engine Table Creation Rules

### 8.1 When Creating Time Series Table

**MUST follow these rules**:

1. First column MUST be `TIMESTAMPTZ` or `TIMESTAMP` with `NOT NULL`
2. At least 1 PRIMARY TAG required (error 3006 if missing)
3. Max 4 PRIMARY TAGS per table (error 3004 if exceeded)
4. PRIMARY TAGS MUST be in TAGS list with `NOT NULL`
5. PRIMARY TAGS cannot be: FLOAT, FLOAT4, FLOAT8, DOUBLE, REAL, BINARY_FLOAT, BINARY_DOUBLE, DECIMAL, NUMERIC, NVARCHAR, NCHAR, TEXT, CLOB, BLOB, BYTES, VARBYTES, JSON, ARRAY, MAP, INET, INTERVAL, UUID
6. Ordinary TAGS cannot be: TIMESTAMP, TIMESTAMPTZ, NVARCHAR, GEOMETRY
7. Table name max 128 bytes, column/tag names max 128 bytes

### 8.2 When Creating Relational Table

**MUST follow these rules**:

1. Supports standard PostgreSQL syntax
2. Primary key can be single or composite
3. Foreign keys must reference existing tables
4. Data types follow PostgreSQL compatibility
5. Supports SERIAL/BIGSERIAL for auto-increment

### 8.3 Error Code Reference (from KDTS source)

| Error Code | Description              | KDTS Behavior                  |
|------------|--------------------------|--------------------------------|
| 3004       | Tag limit exceeded       | ERROR: source tags > 132       |
| 3005       | Tag/column name too long | ERROR: name > 128 bytes        |
| 3006       | No primary tag           | ERROR: no eligible primary tag |

**Note**: Codes 3007, 3008, 3009 (previously documented) are NOT found in KDTS source. Actual KDTS behavior is auto-conversion/demotion with warnings, not hard errors.

---

## 9. Comparison with Other Databases

| Feature             | KaiwuDB                   | InfluxDB     | TDengine    | PostgreSQL      | MySQL           |
|---------------------|---------------------------|--------------|-------------|-----------------|-----------------|
| Primary Key         | Optional                  | None         | None        | Required        | Optional        |
| Time Column         | Required (first col)      | _time (auto) | ts (auto)   | Optional        | Optional        |
| Tags                | TAGS clause               | tags         | TAGS clause | N/A             | N/A             |
| Primary Tags        | Max 4                     | N/A          | N/A         | N/A             | N/A             |
| Secondary Tags      | Yes                       | tags         | TAGS        | N/A             | N/A             |
| Tag Types           | Limited with auto-convert | Flexible     | Flexible    | N/A             | N/A             |
| Data Retention      | Yes                       | Yes          | Yes         | Yes (partition) | Yes (partition) |
| Compression         | Auto                      | Auto         | Auto        | Yes             | Yes             |
| Dictionary Encoding | Yes                       | N/A          | N/A         | N/A             | N/A             |
| Tag Modification    | Yes (ALTER)               | Yes          | Limited     | N/A             | N/A             |
| Index on Tags       | Hash (auto)               | Index        | Yes         | B-tree          | B-tree          |

---

## 10. Migration-Specific DDL Generation Guidelines

### 10.1 For Relational to Time Series Migration

When generating DDL to convert relational tables to time series:

1. **Identify time column**: Find the timestamp/datetime column, make it first column with `TIMESTAMPTZ NOT NULL`
2. **Select PRIMARY TAGS**: Ask user to choose 1-4 columns as PRIMARY TAGS (e.g., device_id, sensor_id)
3. **Select ordinary TAGS**: Ask user to choose additional columns as TAGS (e.g., location, status)
4. **Remaining columns**: These become value/data columns
5. **Apply type constraints**: KDTS will auto-convert/demote invalid tag types

**Example Conversion** (MySQL to KaiwuDB Time Series):

```sql
CREATE TABLE sensor_data (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    device_id BIGINT NOT NULL,
    location VARCHAR(100),
    reading_time DATETIME NOT NULL,
    temperature DECIMAL(10,2),
    humidity DECIMAL(10,2),
    status VARCHAR(20)
);

CREATE TABLE sensor_data (
    reading_time TIMESTAMPTZ NOT NULL,
    id BIGINT,
    temperature DECIMAL(10,2),
    humidity DECIMAL(10,2)
)
TAGS (
    device_id BIGINT NOT NULL,
    location VARCHAR(100),
    status VARCHAR(20)
)
PRIMARY TAGS (device_id);
```

### 10.2 For Time Series to Time Series Migration

When migrating between time series databases, KDTS auto-generates DDL:

1. **Read source tags**: All source tags from measurement/super table
2. **Auto-map tags**: 
   - First N eligible tags -> PRIMARY TAGS (up to 4)
   - Remaining tags -> ordinary TAGS (up to 128)
3. **Auto-convert types**: Invalid types converted per rules in Section 3.3
4. **Auto-demote**: FLOAT/NULL/over-length primary tags demoted to ordinary
5. **Auto-map fields**: Source fields -> data columns
6. **Adjust time column**: Ensure first column is `TIMESTAMPTZ NOT NULL`
7. **Validate**: If no eligible primary tag -> ERROR 3006

**Example Conversion** (InfluxDB to KaiwuDB):

```
-- InfluxDB Source
Measurement: cpu_usage
Tags: host (VARCHAR), region (VARCHAR), datacenter (VARCHAR), service (FLOAT), priority (NVARCHAR)
Fields: usage (FLOAT), temperature (FLOAT), load_average (FLOAT)
Time: _time

-- KDTS Auto-Mapped KaiwuDB Table
CREATE TABLE cpu_usage (
    time TIMESTAMPTZ NOT NULL,
    usage FLOAT8,
    temperature FLOAT8,
    load_average FLOAT8
)
TAGS (
    host VARCHAR(100) NOT NULL,
    region VARCHAR(50) NOT NULL,
    datacenter VARCHAR(50) NOT NULL,
    service FLOAT8,
    priority VARCHAR(128)
)
PRIMARY TAGS (host, region, datacenter);

-- KDTS Notes:
-- - service is FLOAT -> kept as ordinary tag (FLOAT allowed for ordinary)
-- - priority is NVARCHAR -> converted to VARCHAR(128) (NVARCHAR forbidden for ordinary)
-- - host, region, datacenter are eligible -> promoted to PRIMARY TAGS (first 3, <= 4)
```

### 10.3 Auto-Mapping Summary

| Source Type | Total Tags      | PRIMARY TAGS     | Ordinary TAGS         | Notes                                  |
|-------------|-----------------|------------------|-----------------------|----------------------------------------|
| TDengine    | All TAG columns | First 4 eligible | Remaining (up to 128) | Demote FLOAT/NULL/long                 |
| InfluxDB    | All tags        | First 4 eligible | Remaining (up to 128) | Convert NVARCHAR/TEXT/etc.             |
| OpenTSDB    | All tags        | First 4 eligible | Remaining (up to 128) | Same as InfluxDB                       |
| MySQL       | User-selected   | User-selected    | User-selected         | No auto-mapping for relational sources |

### 10.4 Edge Cases

| Scenario                                  | KDTS Behavior                                     |
|-------------------------------------------|---------------------------------------------------|
| 0 eligible primary tags                   | ERROR 3006 (no primary tag)                       |
| All tags are FLOAT/DOUBLE/DECIMAL/NUMERIC | ERROR 3006 (all demoted, no eligible)             |
| Tag name > 128 bytes                      | ERROR 3005                                        |
| Total tags > 132                          | ERROR 3004                                        |
| Primary tag VARCHAR > 128                 | Auto-truncate to VARCHAR(128)                     |
| Primary tag has no length                 | Default to VARCHAR(64)                            |
| Ordinary tag is TIMESTAMP                 | Auto-convert to VARCHAR                           |
| Primary count > 4                         | Demote from last until 4                          |
| Primary tag is DECIMAL/NUMERIC            | Auto-demote to ordinary tag (classified as float) |

---

## 11. References

- [KaiwuDB Official Documentation](https://www.kaiwudb.com/docs/)
- [KaiwuDB Time Series Table DDL](https://www.kaiwudb.com/docs/#/sql-reference/ddl/ts-db/ts-table.html)
- [KaiwuDB Relational Table DDL](https://www.kaiwudb.com/docs/#/sql-reference/ddl/relational-db/relational-table.html)
- [KDTS Source Code - KaiwuDBStrategy.java](file:///D:/workspace/inspur/kw-datax-utils/kdts-server/src/main/java/com/kaiwudb/migration/strategy/KaiwuDBStrategy.java)
- [KDTS Source Code - TypeMapping.java](file:///D:/workspace/inspur/kw-datax-utils/kdts-server/src/main/java/com/kaiwudb/migration/util/TypeMapping.java)
