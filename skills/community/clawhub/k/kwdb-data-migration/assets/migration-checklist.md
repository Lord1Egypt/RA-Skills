# KDTS Heterogeneous Database Migration Checklist

Complete migration workflow checklist to ensure every step is executed correctly.

## Language Versions

- **English Version**: This file (`migration-checklist.md`)
- **Chinese Version**: [migration-checklist.zh.md](./migration-checklist.zh.md)

The AI Agent will respond in the same language the user uses.

---

## Phase 1: Pre-Migration Preparation

### 1.1 Environment Check

- [ ] KDTS Server is running and accessible
    - Access `http://{kdts_host}:{port}/kdts/api/v1/health` to confirm status
    - Default port: 8989
- [ ] Source database is network-accessible from KDTS Server
    - Test connectivity: `ping {source_host}` or `telnet {source_host} {port}`
- [ ] Target KaiwuDB is installed and running
    - Test connection: `mysql -h {kwdb_host} -P {port} -u root -p`
- [ ] Python 3 is installed (on KDTS Server)
    - Run: `python3 --version`

### 1.2 Account Permissions

- [ ] Source database account has sufficient permissions
    - MySQL: SELECT on target database
    - Oracle: SELECT_CATALOG_ROLE or DBA
    - PostgreSQL: USAGE on schema
    - Other databases: refer to their documentation
- [ ] Target KaiwuDB account has sufficient permissions
    - CREATE, DROP, ALTER (for DDL)
    - INSERT, SELECT (for data migration)
    - Target database exists or auto-creation is allowed
- [ ] Network firewall/security group has required ports open

### 1.3 Backup Reminder

- [ ] Critical source data is backed up
- [ ] Existing target data is backed up (if any)
- [ ] Rollback plan is prepared for migration failure

---

## Phase 2: Connection and Metadata

### 2.1 Connection Test

- [ ] Source database connection test passed

  POST /kdts/api/v1/datasource/validate
  ```json
  {
    "engine": "RELATIONAL",
    "type": "MYSQL",
    "host": "127.0.0.1",
    "port": 3306,
    "username": "user",
    "password": "pass",
    "dbName": "example_db",
    "isTarget": false
  }
  ```
    - Expected response: `{"code": 0, "data": "SUCCEED"}`
    - NOTE: KDTS may return code=0 even for FAILED validation, with the failure
      text in `data` — success requires `data == "SUCCEED"`
- [ ] Target KaiwuDB connection test passed
    - Set `isTarget: true`

### 2.2 Source-side Metadata

- [ ] List source databases

  POST /kdts/api/v1/datasource/databases

  ```json
  {
    "engine": "RELATIONAL",
    "type": "MYSQL",
    "host": "127.0.0.1",
    "port": 3306,
    "username": "user",
    "password": "pass",
    "dbName": null
  }
  ```

- [ ] Read source table metadata

  POST /kdts/api/v1/datasource/metadata
  ```json
  {
    "source": {
      "engine": "RELATIONAL",
      "type": "MYSQL",
      "host": "127.0.0.1",
      "port": 3306,
      "username": "user",
      "password": "pass",
      "dbName": "example_db"
    },
    "metadata": {
      "enable": true,
      "autoDdl": false,
      "primaryKey": true,
      "constraint": true,
      "comment": true,
      "index": true,
      "view": false
    }
  }
  ```
- [ ] Verify metadata completeness
    - Correct table count
    - Correct column count and types
    - Correct primary keys/constraints
    - (Optional) Comments and indexes included

### 2.3 Sources Without Metadata Support

**If source does NOT support metadata (ClickHouse, TDengine 2.x, OpenTSDB, MongoDB,
FTP, HDFS; read_metadata returns 3001):**

- [ ] **Check whether the target DB/table already exists**
    - Target table exists and matches → skip DDL, go directly to data migration
    - Not exists → continue with the table-creation flow below
- [ ] **Collect the table structure from the USER** (source CREATE TABLE DDL or a
      column list with names and types)
    - NEVER guess the structure
- [ ] Build the Database object via `build_manual_metadata(source_type, db_name, table_name, columns)`
- [ ] Mark time-series columns/tags (`mark_time_series_columns`) or add columns (`build_added_column`) as needed
- [ ] `preview_ddl` → user confirmation → `execute_ddl` creates the target table
- [ ] After the table is created, run the data migration (explicit table mappings, `tables` REQUIRED)
- [ ] File sources (FTP/HDFS) have no table structure: pre-create target tables or migrate per file configuration
- [ ] **OpenTSDB source**: `column` is a list of FULL METRIC names in
      `table.metric` format (e.g. `test_tb.c1,test_tb.c2,...`); time range REQUIRED
      (beginDateTime/endDateTime); usually NO authentication (username/password empty)
- [ ] **SQL Server source**: JDBC URL MUST include `encrypt=true;trustServerCertificate=true`
      (`jdbc:sqlserver://host:1433;databaseName=db;encrypt=true;trustServerCertificate=true`);
      supports `where` filters and expression columns; two-step migration (schema + data)
    - **schemaName fix**: the metadata table schemaName may come back as the DATABASE 
      name → DDL becomes `"db"."db"."table"` (duplicated); set it to `public` → `"db"."public"."table"`
- [ ] **KaiwuDB source** (KaiwuDB→KaiwuDB): the time-series engine source
      REQUIRES time range (beginDateTime/endDateTime) + `tsColumn` (time column
      name); collect the time range from the user
- [ ] **MongoDB source**: identifier is `collectionName`; `column` is a
      JSON array (name/type: date/int/long/double/bool/string/bytes); `query` optional
      (MongoDB JSON query syntax filter, e.g. `{"t1":{"$gte":1,"$lt":8}}`)
    - **Table creation is LIMITED to two options** (KDTS does NOT support MongoDB→KaiwuDB type mapping):
      ① User pre-creates the target table (skip DDL, migrate data directly);
      ② **SKILL generates DDL from the user-provided table info** (mapping: int→INT4, long→INT8,
      double→FLOAT8, string→VARCHAR, bytes→VARBYTES, date→TIMESTAMP, bool→BOOL), user confirms, then execute
    - **DDL execution FAILED → inform the user the table was NOT created, END migration**
- [ ] **FTP path requirements**: MUST start with `/`; path is the SFTP SERVER-side path; 
      Set `skipHeader: true` when the CSV has a header row
- [ ] **HDFS path requirements**: path is the HDFS SERVER-side absolute path
      (JSON array, e.g. `/user/hive/warehouse/hdfs_test.db/test_tb`); `fileType`
      REQUIRED (text/orc/parquet/rcfile); text supports fieldDelimiter/encoding/
      compress/csvReaderConfig; connect to NameNode (host:9000)

**Note:** SQL Server, InfluxDB 1.x and 2.x support metadata reading (META_AND_DATA capability), but do NOT support full migration. Use two-step migration approach for these sources.

---

## Phase 3: DDL and Schema Migration

### 3.1 DDL Preview

- [ ] Preview target DDL

  POST /kdts/api/v1/metadata/preview
  ```json
  {
    "target": {
      "engine": "RELATIONAL",
      "type": "KAIWUDB",
      "host": "127.0.0.1",
      "port": 26257,
      "username": "root",
      "password": "pass",
      "dbName": "target_db",
      "isTarget": true
    },
    "sourceDb": {
      "type": "MYSQL",
      "name": "source_db",
      "encoding": "UTF-8",
      "tableMap": {
        "example_table": {
          "tableName": "example_table",
          "columns": [
            {
              "columnName": "id",
              "columnType": "INT",
              "nullAble": false,
              "finalConvertDataType": "INT",
              "isChecked": true
            }
          ],
          "primaryKey": {
            "tableName": "example_table",
            "columns": [{"columnName": "id", "asc": true}]
          },
          "constraint": [],
          "indexes": []
        }
      },
      "viewMap": {}
    },
    "metadata": {
      "enable": true,
      "autoDdl": false,
      "primaryKey": true,
      "constraint": true,
      "comment": true,
      "index": true,
      "view": false
    },
    "isTimeSeries": false
  }
  ```

  **Note**: The `sourceDb` field must be a complete `Database` object returned from `/datasource/metadata` API.
  Do NOT pass a simplified structure - use the full response object.
- [ ] Review generated DDL
    - Table names match
    - Column names and types map correctly
    - Primary keys/constraints preserved
    - Special types converted correctly

- [ ] Verify KaiwuDB Time-Series Table Constraints (for TIMESERIES engine)
    - Total columns (Tags + Values) <= 128
    - Primary Tags count <= 4
    - Tag/Column names <= 128 bytes
    - At least 1 Primary Tag defined
    - If exceeded, consider splitting into multiple tables or migrations

### 3.2 DDL Execution

- [ ] (If needed) Drop existing target tables
    - Confirm target table data is backed up or can be discarded
    - Use KaiwuDB DROP TABLE command
- [ ] Execute DDL

  POST /kdts/api/v1/metadata/execute
  ```json
  {
    "target": {
      "engine": "RELATIONAL",
      "type": "KAIWUDB",
      "host": "127.0.0.1",
      "port": 26257,
      "username": "root",
      "password": "pass",
      "dbName": "target_db",
      "isTarget": true
    },
    "ddlScript": {
      "dbName": "SOURCE_DB",
      "createDb": "CREATE DATABASE SOURCE_DB ENGINE=TIMESERIES",
      "table": {
        "example_table": "CREATE TABLE example_table (id INT PRIMARY KEY, name VARCHAR(100))"
      },
      "view": {}
    },
    "autoDdl": false
  }
  ```

  **Note**: The `ddlScript` must be a complete `DdlScript` object returned from `/metadata/preview` API.
  Do NOT pass a simple array of SQL statements.

- [ ] Verify DDL execution result
    - Check table creation success
    - Check column type correctness

### 3.3 Data-Only Migration Scenario

**If target tables already exist and schema matches:**

- [ ] Skip DDL phase
- [ ] Confirm target table schema matches source
- [ ] Execute `TRUNCATE TABLE` if data needs clearing

### 3.4 Relational Source → Time-Series Target Scenario (RELATIONAL → TIMESERIES)

**IMPORTANT**: KDTS `preview_ddl` fully supports time-series DDL generation — the request
field is `"isTimeSeries": true`, and the `sourceDb` columns carry tag marks.

- [ ] Guide user to select PRIMARY TAGS (1-4, REQUIRED)
    - Exclude float types (FLOAT/DOUBLE/DECIMAL/NUMERIC etc. cannot be primary tags)
    - Recommend unique identifier columns (e.g., device_id, sensor_id)
- [ ] Guide user to select ordinary TAGS (optional)
- [ ] Apply marks to the `sourceDb` columns (use the `mark_time_series_columns()` helper):
    - Time column: `"isTs": true` (KDTS renders first column `TIMESTAMPTZ NOT NULL`)
    - Primary tag: `"isTag": true` + `"isPrimaryTag": true` + `"nullAble": false`
      (primary tags must be NOT NULL in the column definition, otherwise KDTS demotes
      the tag and may fail with 3006; the helper handles this automatically)
    - Ordinary tag: `"isTag": true`
- [ ] Check source data for NULL values in selected PRIMARY TAG columns
    - Run `SELECT COUNT(*) FROM <table> WHERE <primary_tag_col> IS NULL;`
    - PRIMARY TAGS must be NOT NULL; NULLs in source data will fail the migration
- [ ] Call `preview_ddl(target, source_db, metadata, is_time_series=True)` to generate TS DDL
    - Verify `CREATE TS DATABASE` and `TAGS (...)` / `PRIMARY TAGS (...)` clauses
    - Tables WITHOUT any tag-marked column are SKIPPED by KDTS (no DDL) — warn the user
    - Watch for auto-demotion/conversion (FLOAT/nullable primary tags demoted, NVARCHAR→VARCHAR)
- [ ] Execute via `execute_ddl` API (createDb is auto-generated by KDTS from the target engine)
- [ ] Use explicit table mappings (`tables` REQUIRED) for the data migration phase

### 3.5 InfluxDB Source Scenario (INFLUXDB1X/2X → TIMESERIES)

**InfluxDB mapping requirements:**

- [ ] Use the `measurement` field in the mapping (NOT `table`) — use the
      `build_influxdb_mapping()` helper
- [ ] Source column names use `sourceColumnName`: the time column MUST be `_time`
      (not the target column name `ts`)
- [ ] **Data time range is REQUIRED (no defaults)**: collect begin/end from the user
    - Format: `Begin time (YYYY-MM-DD HH:MM:SS)` and `End time (YYYY-MM-DD HH:MM:SS)`
    - No time range → migration fails
    - Too-wide range (e.g. 1970-2099) → reader memory overflow
    - Use the actual data range; `splitIntervalS` defaults to 86400 (1-day windows)
- [ ] Build the mapping via:
    `build_influxdb_mapping(source_db, 'test_tb', begin_datetime='2025-10-22 00:00:00', end_datetime='2025-10-26 00:00:00')`

### 3.6 Oracle Source Notes

- [ ] **Source dbName must be the owner name, usually UPPERCASE**: KDTS reads Oracle
      metadata via `owner = dbName`; a lowercase dbName returns zero tables
      (e.g. `ORACLE_KWDB`, not `oracle_kwdb`)
- [ ] **Table/column names are UPPERCASE**: mapping columns must match the metadata
      exactly (e.g. `TS,C1,...`)
- [ ] **Expression columns need separated target columns**: source `1 as t1` requires
      `target_columns="...,t1"` (target must use real column names, else DataX fails
      to find the target column)

### 3.7 Added-Column Type Rules (ALL source types → KaiwuDB)

When adding a column the source lacks (e.g. a tag column), derive the type from the
DEFAULT VALUE (use `build_added_column()`; applies to RDBMS/TDengine/InfluxDB/KaiwuDB):
- int default → `INT4` (`INT8` for InfluxDB); str default → `VARCHAR`; bool default →
  `BOOL` (eligible for PRIMARY TAG)
- **float default → `FLOAT4/FLOAT8` — ordinary TAG ONLY, NEVER a primary tag**
  (float types are demoted by KDTS; 3006 if no eligible primary tag remains)
- sourceColumnType per source for an exact mapping: MySQL/SQLServer/TDengine `INT`,
  Oracle `NUMBER(10,0)`, PostgreSQL `INTEGER`, ClickHouse `INT32`, InfluxDB `INTEGER`,
  KaiwuDB `INT4`
- SELECT-based sources use a SQL expression matching the default (e.g. default 1 →
  `1 as t1`); InfluxDB uses `build_influxdb_mapping()` (no SQL-expression support)

---

## Phase 4: Data Migration

### 4.1 Configure DataX Parameters (REQUIRED)

**IMPORTANT**: DataX configuration with `core` and `setting` fields is REQUIRED for successful data migration. Missing these fields will cause migration failures!

**Three Configuration Methods (Mutually Exclusive):**
- Method 1: Fixed channel count (simple, recommended for most cases)
- Method 2: By byte limit (precise bandwidth control)
- Method 3: By record limit (precise QPS control)

- [ ] Review default DataX configuration (Method 1: Fixed channel count)

  Default DataX Configuration:
  ```json
  {
    "batchSize": 1000,
    "core": {
      "transport": {
        "channel": {
          "speed": {
            "byte": 1048576,
            "record": 1000
          }
        }
      }
    },
    "enable": true,
    "fetchSize": 1000,
    "setting": {
      "errorLimit": {
        "percentage": 0.02
      },
      "speed": {
        "channel": 4
      }
    }
  }
  ```

- [ ] Confirm or customize DataX parameters:
  
  **Common parameters (for all methods):**
  - `fetchSize`: Records fetched per request from source (default: 1000)
  - `batchSize`: Records per batch written to target (default: 1000)
  - `setting.errorLimit.percentage`: Acceptable error percentage (default: 0.02 = 2%)
  
  **Method 1: Fixed channel count**
  - `setting.speed.channel`: Number of parallel channels (default: 4)
  - `core.transport.channel.speed.byte`: Optional byte limit per channel (default: 1048576 = 1MB/s)
  - `core.transport.channel.speed.record`: Optional record limit per channel (default: 1000 records/s)
  
  **Method 2: By byte limit**
  - `setting.speed.byte`: Global byte limit (e.g., 52428800 = 50MB/s)
  - `core.transport.channel.speed.byte`: REQUIRED byte limit per channel (e.g., 10485760 = 10MB/s)
  - Channel count auto-calculated: global byte / per-channel byte
  
  **Method 3: By record limit**
  - `setting.speed.record`: Global record limit (e.g., 40000 = 40000 records/s)
  - `core.transport.channel.speed.record`: REQUIRED record limit per channel (e.g., 1000 = 1000 records/s)
  - Channel count auto-calculated: global record / per-channel record

- [ ] Verify configuration constraints:
  - Method 1 and Method 2/3 are MUTUALLY EXCLUSIVE (cannot mix)
  - If using Method 2, `core.transport.channel.speed.byte` MUST be configured
  - If using Method 3, `core.transport.channel.speed.record` MUST be configured
  - Do NOT configure `channel` in `core.transport.channel.speed` (only in `setting.speed`)

### 4.2 Build Migration Script

- [ ] Build DataX migration script

  POST /kdts/api/v1/datax/build
  ```json
  {
    "source": {
      "engine": "RELATIONAL",
      "type": "MYSQL",
      "host": "127.0.0.1",
      "port": 3306,
      "username": "user",
      "password": "pass",
      "dbName": "source_db"
    },
    "target": {
      "engine": "RELATIONAL",
      "type": "KAIWUDB",
      "host": "127.0.0.1",
      "port": 26257,
      "username": "root",
      "password": "pass",
      "dbName": "target_db",
      "isTarget": true
    },
    "tables": [],
    "data": {
      "batchSize": 1000,
      "core": {
        "transport": {
          "channel": {
            "speed": {
              "byte": 1048576,
              "record": 1000
            }
          }
        }
      },
      "enable": true,
      "fetchSize": 1000,
      "setting": {
        "errorLimit": {
          "percentage": 0.02
        },
        "speed": {
          "channel": 4
        }
      }
    }
  }
  ```

  **Note**: 
  - Empty `tables` array means auto-discover all tables (for sources that support full migration,
    and RELATIONAL targets ONLY).
  - **TIMESERIES targets MUST use explicit table mappings**: empty `tables` fails with 4001
    "No datax contents generated from config".
  - **PostgreSQL source limitation**: auto-discovery filters tables by `schema == dbName`.
    Tables in the `public` schema (the common case) are filtered out → 4001 even for RELATIONAL targets.
    Use explicit table mappings for PostgreSQL unless tables live in a schema named after the database.
  - For table-level migration, specify tables explicitly.
  - **CRITICAL**: Both `core` and `setting` fields in `data` are REQUIRED for successful DataX execution.

- [ ] Record returned script filename
    - Format: `{SOURCE}2KAIWUDB_{timestamp}.json`
    - Note filename for later queries

### 4.3 Execute Migration

- [ ] Start migration

  POST /kdts/api/v1/datax/execute
  ```json
  ["MYSQL2KAIWUDB_1719290000.json"]
  ```
- [ ] **Use batch execution when scripts > 10** (`execute_migration_batches(script_names, batch_size=10)`)
    - Submitting dozens of scripts in one request triggers HTTP 4003 timeouts
    - Submit 10 scripts per batch, wait for the batch to reach final states, then next
    - A 4003 on submission only means the response timed out — the request reached the
      server (it keeps processing), so still monitor the batch
- [ ] Record returned log file path

### 4.4 Monitor Progress

- [ ] Periodically query task status
  ```
  GET /kdts/api/v1/datax/status?scriptName=MYSQL2KAIWUDB_1719290000.json
  ```
- [ ] Status definitions
    - `SUBMITTED`: Submitted, waiting to execute
    - `RUNNING`: In progress
    - `SUCCEEDED`: Completed successfully
    - `FAILED`: Execution failed
    - `KILLED`: Terminated
- [ ] If failed, view detailed logs

### 4.5 Large Dataset Migration Tips

- [ ] Set `splitPk` on large tables to enable parallelism
- [ ] Adjust `fetchSize` and `batchSize`
- [ ] Set `speed.channel` to increase concurrency
- [ ] Execute migration in time-based batches

---

## Phase 5: Migration Verification

### 5.1 Row Count Verification

- [ ] Verify row count per table
  ```sql
  -- Source
  SELECT COUNT(*) FROM table_name;
  
  -- Target
  SELECT COUNT(*) FROM table_name;
  ```
- [ ] Verify counts match (or match expected difference)

### 5.2 Data Sampling Verification

- [ ] Randomly sample records for comparison
  ```sql
  -- Compare key fields
  SELECT * FROM table_name ORDER BY pk LIMIT 100;
  ```
- [ ] Verify special values (NULL, empty strings, special characters)

### 5.3 Business Verification

- [ ] Core business scenarios pass verification
- [ ] Application functionality works normally
- [ ] No noticeable performance degradation

---

## Troubleshooting Common Issues

### Q1: Connection Test Failed

**Checklist:**

- [ ] Database service is running
- [ ] Correct host/port
- [ ] Network connectivity (firewall)
- [ ] Correct username/password
- [ ] Database exists
- [ ] KDTS Server has access permissions

### Q2: DDL Preview Error

**Checklist:**

- [ ] Source type supports metadata
- [ ] No unsupported column types
- [ ] KaiwuDB version compatibility

### Q3: Migration Timeout

**Checklist:**

- [ ] Source table too large
- [ ] Batch migration needed
- [ ] Sufficient network bandwidth
- [ ] KDTS Server has sufficient resources

**Solutions:**

- Increase timeout
- Reduce migration scope
- Enable parallelism (splitPk)
- Optimize query (WHERE clause)

### Q4: Migration FAILED but Status Query Shows No Details

**Checklist:**

- [ ] Check KDTS server log files (`/opt/kdts/data/log/`)
- [ ] Time-series migration: does source data contain NULL in PRIMARY TAG columns?
    - PRIMARY TAGS must be NOT NULL; NULL source values fail the write
    - Solutions: fix source data / choose different primary tags / demote to ordinary tags
- [ ] Time-series target: was an explicit table mapping used? (empty `tables` fails with 4001)

### Q5: Partial Data Loss

**Checklist:**

- [ ] Any error logs
- [ ] Any data filtered out
- [ ] Any write failures

**Solutions:**

- Check error logs
- Increase errorLimit percentage
- Retry failed tables

---

## Rollback Scenarios

### Scenario 1: DDL Execution Failed

1. Check target table status
2. Drop created tables (if any)
3. Fix source-side issue
4. Re-execute DDL

### Scenario 2: Data Migration Failed (Incomplete)

1. Query task status: `GET /datax/status?scriptName=...`
2. If resumable: check resume support (limited scenarios)
3. If not resumable:
    - Clear target table (TRUNCATE)
    - Rebuild and re-execute migration

### Scenario 3: Migration Completed But Data Has Issues

1. Assess impact scope
2. Fix problematic data
3. Re-migrate affected tables (needs clearing)
4. Or manually fix target data

---

## Performance Optimization

### Before Migration

- [ ] Source: Ensure statistics are up to date (ANALYZE TABLE)
- [ ] Source: Avoid peak hours
- [ ] Target: Create sufficient tablespace
- [ ] Target: Disable unnecessary triggers/constraints

### During Migration

- [ ] Use `splitPk` for parallel reads
- [ ] Adjust `speed.channel` for parallel writes
- [ ] Set appropriate `fetchSize` and `batchSize`
- [ ] Monitor system resources (CPU, memory, disk I/O)

### After Migration

- [ ] Rebuild target indexes (if disabled)
- [ ] Update statistics
- [ ] Verify data integrity

---

## Success Criteria

[OK] All tables migrated successfully  
[OK] Row counts match  
[OK] Data sampling shows no differences  
[OK] Business functionality normal  
[OK] Performance meets expectations

---

**Document Version:** v1.0.0  
**Last Updated:** 2026-08-03  
**Maintainer:** KDTS Development Team
