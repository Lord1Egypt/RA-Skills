# Supported Source Types

Complete reference of all source types supported by KDTS, their capabilities, and configuration requirements.

## Capability Legend

| Symbol         | Meaning                                                  |
|----------------|----------------------------------------------------------|
| [YES]          | Supported                                                |
| [NO]           | Not Supported                                            |
| Full Migration | Can migrate entire database (all tables auto-discovered) |
| Metadata       | Supports reading table structure for DDL generation      |
| Table-Level    | Can migrate specific tables (without auto-discovery)     |
| Time Series    | Special handling for time-series data                    |

---

## Source Type Matrix

> **Based on KDTS SourceTypes.java implementation**:
> - Full Migration = `checkSourceForAllData()`: Supports auto-discovery of all tables
> - Metadata = `checkSourceForMetadata()`: Supports reading table structure for DDL generation
> - Data Only = `checkSourceForData()`: Supports data migration only

| Source Type    | Full Migration | Metadata | Engine     | Notes                                        |
|----------------|----------------|----------|------------|----------------------------------------------|
| **MYSQL**      | [YES]          | [YES]    | RELATIONAL | Most common source                           |
| **ORACLE**     | [YES]          | [YES]    | RELATIONAL | Enterprise DB                                |
| **POSTGRESQL** | [YES]          | [YES]    | RELATIONAL | Open-source alternative                      |
| **SQLSERVER**  | [NO]           | [YES]    | RELATIONAL | Metadata + Data, no full migration           |
| **CLICKHOUSE** | [YES]          | [NO]     | RELATIONAL | Analytics DB, auto-discovery, no metadata    |
| **KAIWUDB**    | [YES]          | [NO]     | *REQUIRED* | Auto-discovery, no metadata, engine required |
| **TDENGINE3X** | [YES]          | [YES]    | TIMESERIES | Recommended TDengine version                 |
| **TDENGINE2X** | [NO]           | [NO]     | TIMESERIES | Legacy version                               |
| **INFLUXDB1X** | [NO]           | [YES]    | TIMESERIES | Metadata + Data, no full migration           |
| **INFLUXDB2X** | [NO]           | [YES]    | TIMESERIES | Metadata + Data, no full migration           |
| **OPENTSDB**   | [NO]           | [NO]     | TIMESERIES | Time-series DB                               |
| **MONGODB**    | [NO]           | [NO]     | TIMESERIES | Document DB                                  |
| **FTP**        | [NO]           | [NO]     | TIMESERIES | File transfer                                |
| **HDFS**       | [NO]           | [NO]     | TIMESERIES | Hadoop filesystem                            |

**Notes:**
- All source configurations require explicit `engine` field
- For KAIWUDB as source, engine must be explicitly specified based on data type (RELATIONAL or TIMESERIES)
- SQLSERVER, INFLUXDB1X/2X support metadata + data migration, but NOT full migration (no auto-discovery)
- Full migration (auto-discovery) is supported for: MYSQL, ORACLE, POSTGRESQL, CLICKHOUSE, KAIWUDB, TDENGINE3X
- CLICKHOUSE and KAIWUDB support Full Migration (auto-discovery) but NOT Metadata reading (DDL generation)

**Source-specific requirements:**

| Source           | Requirements                                                                                                                                                              |
|------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| MYSQL            | `where` filters, SQL expression columns (e.g. `1 as t1`), `target_columns` separation                                                                                     |
| ORACLE           | dbName MUST be the owner name (UPPERCASE, e.g. `ORACLE_KWDB`); names are UPPERCASE; new columns need exact NUMBER mappings (`NUMBER(10,0)`→INT4, NOT `NUMBER(1,0)`→FLOAT) |
| POSTGRESQL       | auto-discovery filters by `schema == dbName` — tables in `public` schema need explicit mappings                                                                           |
| SQLSERVER        | JDBC URL needs `encrypt=true;trustServerCertificate=true`; metadata schemaName may be the DB name → fix to `public`; two-step migration                                   |
| CLICKHOUSE       | no metadata — build the Database object manually from USER-provided table structure (`build_manual_metadata`)                                                             |
| KAIWUDB (source) | time range (beginDateTime/endDateTime) + `tsColumn` REQUIRED                                                                                                              |
| TDENGINE3X       | full migration; explicit table mappings for TIMESERIES targets                                                                                                            |
| TDENGINE2X       | data-only; manual metadata for DDL (user-provided structure)                                                                                                              |
| INFLUXDB1X/2X    | mapping uses `measurement`; time column `_time`; data time range REQUIRED (no defaults; too-wide range → memory overflow)                                                 |
| OPENTSDB         | `column` = FULL METRIC names (`table.metric`); time range REQUIRED; usually no auth                                                                                       |
| MONGODB          | `collectionName`; column JSON array (name/type); `query` filter optional; table creation LIMITED (pre-create or SKILL-generated DDL — KDTS has no MongoDB type mapping)   |
| FTP              | `path` MUST start with `/` (FtpReader validates); path is SFTP SERVER-side; `skipHeader: true` for CSV headers                                                            |
| HDFS             | `path` is HDFS SERVER-side absolute (JSON array); `fileType` REQUIRED (text/orc/parquet/rcfile); Kerberos for secured clusters                                            |

---

## Source-Target Engine Compatibility (STRICT)

**CRITICAL**: The following compatibility rules are ENFORCED by KDTS. Violating these rules will cause migration failure.

| Source Type                                      | Source Engine            | Allowed Target Engines   | Notes                                            |
|--------------------------------------------------|--------------------------|--------------------------|--------------------------------------------------|
| MYSQL, ORACLE, POSTGRESQL, SQLSERVER, CLICKHOUSE | RELATIONAL               | RELATIONAL, TIMESERIES   | Relational sources can migrate to either engine  |
| KAIWUDB (source)                                 | RELATIONAL or TIMESERIES | RELATIONAL or TIMESERIES | KaiwuDB can be migrated between engines          |
| TDENGINE2X, TDENGINE3X                           | TIMESERIES               | **ONLY TIMESERIES**      | Time series sources CANNOT migrate to RELATIONAL |
| INFLUXDB1X, INFLUXDB2X                           | TIMESERIES               | **ONLY TIMESERIES**      | Time series sources CANNOT migrate to RELATIONAL |
| OPENTSDB                                         | TIMESERIES               | **ONLY TIMESERIES**      | Time series sources CANNOT migrate to RELATIONAL |
| MONGODB, FTP, HDFS                               | TIMESERIES               | TIMESERIES               | File/NoSQL sources are time series oriented      |

**If Time Series Source → Relational Target is requested:**
1. The migration will FAIL at the KDTS API level
2. Recommend using native tools: Export data from source, transform as needed, import to KaiwuDB RELATIONAL
3. For InfluxDB/TDengine: Use their built-in export (CSV, Line Protocol) then bulk load to KaiwuDB

---

## Target Configuration

**IMPORTANT**: Target is **ALWAYS** KaiwuDB with type = `KAIWUDB`.

| Target           | Engine     | Required |
|------------------|------------|----------|
| Relational KWDB  | RELATIONAL | [YES]    |
| Time Series KWDB | TIMESERIES | [YES]    |

Cannot migrate to other database types. For other targets, use native database tools or ETL solutions.

---

## sourceType Mapping

When building migration scripts, use the correct `sourceType` based on KDTS source type:

| KDTS Source Type | sourceType Value | Description                |
|------------------|------------------|----------------------------|
| MYSQL            | `RDBMS`          | Relational DB (MySQL)      |
| ORACLE           | `RDBMS`          | Relational DB (Oracle)     |
| POSTGRESQL       | `RDBMS`          | Relational DB (PostgreSQL) |
| SQLSERVER        | `RDBMS`          | Relational DB (SQL Server) |
| CLICKHOUSE       | `RDBMS`          | Relational DB (ClickHouse) |
| KAIWUDB          | `KAIWUDB`        | KaiwuDB (source or target) |
| TDENGINE2X       | `TDENGINE`       | TDengine time-series       |
| TDENGINE3X       | `TDENGINE`       | TDengine time-series       |
| INFLUXDB1X       | `INFLUXDB`       | InfluxDB time-series       |
| INFLUXDB2X       | `INFLUXDB`       | InfluxDB time-series       |
| OPENTSDB         | `OPENTSDB`       | OpenTSDB time-series       |
| MONGODB          | `MONGODB`        | MongoDB document           |
| FTP              | `FTP`            | File transfer              |
| HDFS             | `HDFS`           | Hadoop filesystem          |

---

## Per-Source Configuration Templates

**IMPORTANT**: For ALL source configurations, the `engine` field is **REQUIRED**:
- Use `RELATIONAL` for: MYSQL, ORACLE, POSTGRESQL, SQLSERVER, CLICKHOUSE
- Use `TIMESERIES` for: KAIWUDB, TDENGINE2X, TDENGINE3X, INFLUXDB1X, INFLUXDB2X, OPENTSDB, MONGODB, FTP, HDFS

### Relational Sources (MYSQL, ORACLE, POSTGRESQL, SQLSERVER, CLICKHOUSE)

**Engine**: `RELATIONAL`

**sourceType for migration**: `RDBMS`

```json
{
  "engine": "RELATIONAL",
  "type": "MYSQL",
  "host": "127.0.0.1",
  "port": 3306,
  "username": "root",
  "password": "secret",
  "dbName": "source_database"
}
```

**Table-Level Mapping** (for build API):

```json
{
  "source": {
    "sourceType": "RDBMS",
    "table": "users",
    "column": "*"
  },
  "target": {
    "sourceType": "KAIWUDB",
    "table": "users",
    "column": "*",
    "writeMode": "insert"
  }
}
```

**RDBMS-specific options** (in source config):

- `splitPk`: Primary key column for splitting (enables parallel reads)
- `where`: SQL WHERE clause for filtering source data
- `querySql`: Custom SQL query (overrides table + column)

### KaiwuDB Source

**Engine**: Depends on data type - must be explicitly specified (RELATIONAL or TIMESERIES)

**sourceType for migration**: `KAIWUDB`

```json
{
  "engine": "TIMESERIES",
  "type": "KAIWUDB",
  "host": "127.0.0.1",
  "port": 26257,
  "username": "root",
  "password": "secret",
  "dbName": "source_kwdb"
}
```

**Note**: KAIWUDB as source only supports data migration (no metadata reading).

**Table-Level Mapping**:

```json
{
  "source": {
    "sourceType": "KAIWUDB",
    "table": "source_table",
    "column": "*",
    "writeMode": "read"
  },
  "target": {
    "sourceType": "KAIWUDB",
    "table": "target_table",
    "column": "*",
    "writeMode": "insert"
  }
}
```

**KAIWUDB-specific options**:

- `writeMode`: "read" for source, "insert" for target
- `preSql`: SQL to execute before migration
- `postSql`: SQL to execute after migration

### Time Series Sources (TDENGINE, INFLUXDB, OPENTSDB)

**Engine**: `TIMESERIES`

**sourceType for migration**: `TDENGINE`, `INFLUXDB`, or `OPENTSDB`

```json
{
  "engine": "TIMESERIES",
  "type": "TDENGINE3X",
  "host": "127.0.0.1",
  "port": 6030,
  "username": "root",
  "password": "secret",
  "dbName": "source_ts"
}
```

**InfluxDB 1.x/2.x Notes**:

- Supports metadata reading and data migration, but NOT full migration
- Use two-step approach: Schema migration first, then data migration
- Target KaiwuDB will have TIMESERIES engine automatically

**InfluxDB Configuration Example**:

```json
{
  "engine": "TIMESERIES",
  "type": "INFLUXDB2X",
  "host": "127.0.0.1",
  "port": 8086,
  "username": "admin",
  "password": "secret",
  "dbName": "source_bucket"
}
```

**Table-Level Mapping**:

```json
{
  "source": {
    "sourceType": "TDENGINE",
    "table": "sensor_data",
    "column": "*",
    "beginDateTime": "2024-01-01 00:00:00",
    "endDateTime": "2024-12-31 23:59:59"
  },
  "target": {
    "sourceType": "KAIWUDB",
    "table": "sensor_data",
    "column": "*",
    "writeMode": "insert"
  }
}
```

**Time Series-specific options**:

- `beginDateTime`: Start of time range (ISO format)
- `endDateTime`: End of time range (ISO format)

### MongoDB Source

**Engine**: `TIMESERIES`

**sourceType for migration**: `MONGODB`

```json
{
  "engine": "TIMESERIES",
  "type": "MONGODB",
  "host": "127.0.0.1",
  "port": 27017,
  "username": "root",
  "password": "secret",
  "dbName": "source_mongo"
}
```

**Table-Level Mapping**:

```json
{
  "source": {
    "sourceType": "MONGODB",
    "collectionName": "users",
    "column": "*",
    "query": "{\"status\": \"active\"}"
  },
  "target": {
    "sourceType": "KAIWUDB",
    "table": "users",
    "column": "*",
    "writeMode": "insert"
  }
}
```

**MongoDB-specific options**:

- `collectionName`: MongoDB collection name
- `query`: JSON query filter
- `column`: Field selection (comma-separated or "*")

### File Sources (FTP, HDFS)

**Engine**: `TIMESERIES`

**sourceType for migration**: `FTP` or `HDFS`

```json
{
  "engine": "TIMESERIES",
  "type": "FTP",
  "host": "ftp.example.com",
  "port": 21,
  "username": "anonymous",
  "password": "user@example.com"
}
```

**Table-Level Mapping**:

```json
{
  "source": {
    "sourceType": "FTP",
    "path": "/data/export.csv",
    "fieldDelimiter": ",",
    "connectPattern": "",
    "column": "id,name,value"
  },
  "target": {
    "sourceType": "KAIWUDB",
    "table": "import_data",
    "column": "id,name,value",
    "writeMode": "insert"
  }
}
```

**FTP-specific options**:

- `path`: File path on FTP server
- `fieldDelimiter`: Field separator character
- `connectPattern`: FTP connection pattern

**HDFS-specific options**:

- `defaultFS`: Hadoop NameNode URI (e.g., hdfs://namenode:8020)
- `path`: HDFS file path
- `fileType`: File format (csv, json, etc.)

---

## Target Configuration (KaiwuDB)

**IMPORTANT**: Target is **ALWAYS** KaiwuDB and requires `engine` field to specify the storage type.

### KaiwuDB Target - Relational Engine

```json
{
  "type": "KAIWUDB",
  "engine": "RELATIONAL",
  "host": "127.0.0.1",
  "port": 26257,
  "username": "root",
  "password": "kwdb_password",
  "dbName": "target_db",
  "isTarget": true
}
```

### KaiwuDB Target - Time Series Engine

```json
{
  "type": "KAIWUDB",
  "engine": "TIMESERIES",
  "host": "127.0.0.1",
  "port": 26257,
  "username": "root",
  "password": "kwdb_password",
  "dbName": "target_ts_db",
  "isTarget": true
}
```

**Target Configuration Notes**:

- `engine`: **REQUIRED** - Must be "RELATIONAL" or "TIMESERIES"
- `isTarget`: Set to `true` for target configuration
- Use RELATIONAL engine for: MySQL, Oracle, PostgreSQL, SQL Server, ClickHouse sources
- Use TIMESERIES engine for: TDengine, InfluxDB, OpenTSDB sources

---

## Common Issues

### 1. Port Numbers

| Source Type | Default Port |
|-------------|--------------|
| MySQL       | 3306         |
| Oracle      | 1521         |
| PostgreSQL  | 5432         |
| SQL Server  | 1433         |
| ClickHouse  | 9000         |
| KaiwuDB     | 26257        |
| TDengine    | 6030         |
| InfluxDB    | 8086         |
| MongoDB     | 27017        |
| FTP         | 21           |
| HDFS        | 8020         |

### 2. Authentication

- Some sources (MongoDB, InfluxDB) may require authentication even with empty username/password
- Ensure database user has SELECT on source and CREATE/INSERT on target
- For FTP: anonymous access may not require credentials

### 3. Schema Requirements

- Target KaiwuDB must have the correct engine (RELATIONAL or TIMESERIES)
- Table structure must match between source and target
- Time-series tables in KWDB require primary tag(s)

### 4. KaiwuDB Time-Series Table Constraints

When migrating to KaiwuDB with TIMESERIES engine, the following constraints apply:

| Constraint                       | Limit     | Error Code | Description                       |
|----------------------------------|-----------|------------|-----------------------------------|
| Maximum columns per table        | 128       | 3004       | Total of Tag + Value columns      |
| Maximum primary tags             | 4         | 3004       | Cannot exceed 4 primary tags      |
| Maximum tag/column name length   | 128 bytes | 3005       | Each name must be within limit    |
| Must have at least 1 primary tag | 1         | 3006       | Required for time-series indexing |

**Solutions for exceeding constraints:**

1. Reduce columns to meet the limit
2. Split data into multiple tables or migrations
3. Convert some primary tags to secondary tags
4. Shorten column names if too long

**Example Time-Series Table Design:**

```sql
CREATE TABLE sensor_data
(
    ts         TIMESTAMP,
    device_id  INT,          -- Primary tag
    metric     VARCHAR(32),  -- Primary tag
    value      DOUBLE,       -- Value field
    quality    INT           -- Secondary tag
) TAGS(quality);
```

**KaiwuDB Time-Series Migration Tips:**

- Identify columns suitable for primary tags (unique identifiers like device_id, sensor_id)
- Keep primary tags to a minimum (1-4 is ideal)
- Use secondary tags for categorical data (status, type, etc.)
- Value columns should be numeric (DOUBLE, FLOAT, INT) or string
- Timestamp column is mandatory for time-series tables

---

## Reference

- KDTS API: `references/api-reference.md`
- Type Mapping: `references/type-mapping.md`
- Error Codes: `references/error-codes.md`
- Source Code: `kw-datax-utils/.../constant/SourceTypes.java`
