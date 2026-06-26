# Time Series DDL Reference

KWDB time series database and table creation patterns.

## Create Time Series Database

```sql
CREATE TS DATABASE database_name;
```

## Create Time Series Table

```sql
CREATE TABLE database_name.table_name (
    ts TIMESTAMP NOT NULL,           -- Timestamp column (required, must be first)
    column1 data_type,               -- Data column
    column2 data_type
) TAGS (
    tag1 data_type NOT NULL,        -- Tag column (device identifier)
    tag2 data_type
) PRIMARY TAGS (tag1);
```

### Example: Sensor Table

```sql
CREATE TABLE ts_db.sensors (
    ts TIMESTAMP NOT NULL,
    temperature DOUBLE,
    humidity DOUBLE,
    voltage DOUBLE
) TAGS (
    device_id INT NOT NULL,
    location VARCHAR(100),
    device_type VARCHAR(50)
) PRIMARY TAGS (device_id);
```

## Key Concepts

### Timestamp Column
- Must be `TIMESTAMP NOT NULL`
- Must be the first column
- Represents the time when data was recorded

### Tag Columns
- Device identifiers (device_id, location, etc.)
- Used for partitioning and filtering
- Can be indexed for fast lookups

### Data Columns
- Actual measurement values (temperature, humidity, etc.)
- Stored as columns in the table

### Primary Tags
- Used for data partitioning across nodes
- Should be the most frequently queried tag
- One primary tag per table

## Common Data Types

| Type | Default Width | Max Width | Range / Description |
|------|--------------|-----------|---------------------|
| `TIMESTAMP` | - | - | 时间类型，支持精度 3(毫秒)/6(微秒)/9(纳秒)，默认3 |
| `TIMESTAMPTZ` | - | - | 带时区的时间戳，存储时不包含时区数据，默认UTC |
| `INT2` / `SMALLINT` | 2 字节 | - | -32768 ~ +32767 |
| `INT4` / `INT` / `INTEGER` | 4 字节 | - | -2147483648 ~ +2147483647 |
| `INT8` / `INT64` / `BIGINT` | 8 字节 | - | -9223372036854775808 ~ +9223372036854775807 |
| `FLOAT4` / `REAL` | 4 字节 | - | 最大精度 17 位十进制小数 |
| `FLOAT8` / `DOUBLE` / `DOUBLE PRECISION` | 8 字节 | - | 最大精度 17 位十进制小数 |
| `BOOL` / `BOOLEAN` | 1 字节 | - | true / false |
| `CHAR(n)` | 1 字节 | 1023 字节 | 定长字符，不足补空格，超长报错 |
| `VARCHAR(n)` | 254 字节 | 65534 字节 | 变长字符，不足不补，超长报错 |
| `NCHAR(n)` | 1 字符 | 254 字符 | 定长Unicode字符，不足补空格，超长报错 |
| `NVARCHAR(n)` | 63 字符 | 16383 字符 | 变长Unicode字符，超长报错。**标签不支持该类型** |
| `VARBYTES(n)` | 254 字节 | 65534 字节 | 变长二进制字符 |
| `GEOMETRY` | - | - | 空间数据类型，支持 POINT/LINESTRING/POLYGON |

### 数据类型转换

| 原类型 | 支持转换的目标类型 |
|--------|-------------------|
| `INT2` | INT4, INT8, VARCHAR (最小宽度6) |
| `INT4` | INT8, VARCHAR (最小宽度11) |
| `INT8` | VARCHAR (最小宽度20) |
| `FLOAT4` | FLOAT8, VARCHAR (最小宽度30) |
| `FLOAT8` | VARCHAR (最小宽度30) |
| `TIMESTAMP` | TIMESTAMPTZ, INT8, FLOAT4, FLOAT8 |
| `TIMESTAMPTZ` | TIMESTAMP, INT8, FLOAT4, FLOAT8 |

::: warning 说明
- 转换后的数据类型宽度必须大于原数据类型。例如 INT4 可转 INT8，不可转 INT2。
- 字符类型（CHAR/VARCHAR/NCHAR/NVARCHAR）支持同类型宽度转换，只能增加不能减少。
- 标签列不支持 TIMESTAMP、TIMESTAMPTZ、NVARCHAR 类型。
:::

## Natural Language Mapping

| NL Pattern | SQL Pattern |
|------------|-------------|
| 创建时序数据库 | `CREATE TS DATABASE name` |
| 创建设备表 | `CREATE TABLE ... TAGS (device_id ...)` |
| 创建传感器表 | `CREATE TABLE ... (ts, temperature, humidity)` |
| 添加标签 | `TAGS (tag_name type)` |
| 设置主标签 | `PRIMARY TAGS (tag_name)` |