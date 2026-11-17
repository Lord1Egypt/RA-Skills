# KDTS API Reference

This document provides a complete reference for all KDTS REST API endpoints, based on the actual source code
implementation in `kw-datax-utils`.

## Base Configuration

- **Base URL**: `http://{host}:{port}` (default port: 8989)
- **API Prefix**: `/kdts/api/v1` (configured in application.yml via `common.request-path-prefix`)
- **Content-Type**: `application/json`
- **Response Format**: All API responses follow the `Result<T>` wrapper:

```json
{
  "code": 0,
  "message": "success",
  "timestamp": 1719290000000,
  "data": {}
}
```

---

## Common Data Structures

### DataSourceRequest

Unified data source connection request DTO, used by all datasource-related APIs.

```json
{
  "engine": "RELATIONAL",
  "type": "MYSQL",
  "url": "jdbc:mysql://127.0.0.1:3306/db",
  "host": "127.0.0.1",
  "port": 3306,
  "username": "root",
  "password": "password",
  "dbName": "test_db",
  "isTarget": false
}
```

| Field    | Type    | Required | Allowed Values                                                                                                                          | Description                         |
|----------|---------|----------|-----------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------|
| engine   | String  | Yes      | RELATIONAL, TIMESERIES                                                                                                                  | Database engine type                |
| type     | String  | Yes      | MYSQL, ORACLE, POSTGRESQL, SQLSERVER, CLICKHOUSE, KAIWUDB, TDENGINE2X, TDENGINE3X, INFLUXDB1X, INFLUXDB2X, OPENTSDB, MONGODB, FTP, HDFS | Database product type               |
| url      | String  | No       | -                                                                                                                                       | Full JDBC URL (overrides host:port) |
| host     | String  | No*      | -                                                                                                                                       | Hostname or IP address              |
| port     | Integer | No*      | -                                                                                                                                       | Port number                         |
| username | String  | Yes      | -                                                                                                                                       | Database username                   |
| password | String  | Yes      | -                                                                                                                                       | Database password                   |
| dbName   | String  | No       | -                                                                                                                                       | Database name                       |
| isTarget | Boolean | No       | true, false                                                                                                                             | Set true for target validation      |

*Required if `url` not provided

### MetaData

Metadata migration configuration, controls which metadata types to read/generate.

```json
{
  "enable": true,
  "autoDdl": true,
  "primaryKey": true,
  "constraint": true,
  "comment": true,
  "index": true,
  "view": false
}
```

### Database (Response Object)

Complete database metadata structure returned by `/datasource/metadata`.

```json
{
  "type": "MYSQL",
  "name": "source_db",
  "encoding": "UTF-8",
  "interval": "10m",
  "retentions": "7d",
  "comment": "Database comment",
  "tableMap": {
    "users": {
      "schemaName": "public",
      "sourceTableName": "users",
      "tableName": "users",
      "tableCollation": "utf8mb4_general_ci",
      "tableComment": "User table",
      "columns": [
        {
          "dbType": "MYSQL",
          "schemaName": "public",
          "tableName": "users",
          "sourceColumnName": "id",
          "columnName": "id",
          "sourceColumnType": "BIGINT",
          "columnType": "BIGINT",
          "columnOrder": 1,
          "strLength": null,
          "precision": null,
          "scale": null,
          "nullAble": false,
          "comment": "Primary key",
          "extra": "auto_increment",
          "columnKey": "PRI",
          "finalConvertDataType": "BIGINT",
          "isChecked": true,
          "isTs": false,
          "isTag": false,
          "isPrimaryTag": false
        }
      ],
      "primaryKey": {
        "schemaName": "public",
        "tableName": "users",
        "pkName": "PRIMARY",
        "columns": [
          {
            "columnName": "id",
            "asc": true
          }
        ]
      },
      "constraint": [],
      "indexes": [],
      "source": null
    }
  },
  "viewMap": {}
}
```

#### Table Object Fields

| Field           | Type   | Description                      |
|-----------------|--------|----------------------------------|
| schemaName      | String | Source database schema name      |
| sourceTableName | String | Original table name in source DB |
| tableName       | String | Target table name in KaiwuDB     |
| tableCollation  | String | Table collation (relational)     |
| tableComment    | String | Table comment                    |
| columns         | Array  | List of Column objects           |
| primaryKey      | Object | PrimaryKey object                |
| constraint      | Array  | List of Constraint objects       |
| indexes         | Array  | List of Index objects            |

#### Column Object Fields

| Field                | Type    | Description                                    |
|----------------------|---------|------------------------------------------------|
| dbType               | String  | Source database type                           |
| schemaName           | String  | Source schema name                             |
| tableName            | String  | Source table name                              |
| sourceColumnName     | String  | Original column name in source                 |
| columnName           | String  | Target column name (KaiwuDB)                   |
| sourceColumnType     | String  | Original data type in source                   |
| columnType           | String  | Target data type (KaiwuDB)                     |
| columnOrder          | Integer | Column order in table                          |
| strLength            | Integer | String/binary column length                    |
| precision            | Integer | Numeric precision (DECIMAL)                    |
| scale                | Integer | Numeric scale (decimal places)                 |
| nullAble             | Boolean | Whether column allows NULL                     |
| comment              | String  | Column comment                                 |
| extra                | String  | Extra attributes (auto_increment, etc.)        |
| columnKey            | String  | Column constraint marker (PRI, UNI, MUL, etc.) |
| finalConvertDataType | String  | Final converted type after mapping             |
| isChecked            | Boolean | Whether included in migration                  |
| isTs                 | Boolean | Whether time-series column                     |
| isTag                | Boolean | Whether time-series Tag                        |
| isPrimaryTag         | Boolean | Whether primary Tag                            |

#### PrimaryKey Object Fields

| Field      | Type   | Description                                    |
|------------|--------|------------------------------------------------|
| schemaName | String | Schema name                                    |
| tableName  | String | Table name                                     |
| pkName     | String | Primary key name (defaults to "pk_{table}")    |
| columns    | Array  | List of {"columnName": String, "asc": Boolean} |

### DdlScript (Response Object)

Generated DDL scripts for KaiwuDB.

```json
{
  "dbName": "SOURCE_DB",
  "createDb": "CREATE DATABASE \"SOURCE_DB\" ENGINE=RELATIONAL",
  "table": {
    "users": "CREATE TABLE \"users\" (\n  \"id\" BIGINT NOT NULL AUTO_INCREMENT,\n  \"username\" VARCHAR(50) NOT NULL,\n  \"email\" VARCHAR(100),\n  PRIMARY KEY (\"id\")\n) ENGINE=RELATIONAL COMMENT='User table'",
    "orders": "CREATE TABLE \"orders\" (\n  ...\n) ENGINE=RELATIONAL"
  },
  "view": {
    "v_user_stats": "CREATE VIEW \"v_user_stats\" AS SELECT ..."
  }
}
```

| Field    | Type   | Description                          |
|----------|--------|--------------------------------------|
| dbName   | String | Target database name                 |
| createDb | String | CREATE DATABASE DDL                  |
| table    | Object | Map of table name → CREATE TABLE DDL |
| view     | Object | Map of view name → CREATE VIEW DDL   |

### Source Polymorphism (DataX Source Configuration)

The `Source` interface uses Jackson `@JsonTypeInfo` for polymorphic serialization. The `sourceType` field determines
which implementation is used.

#### RDBMS Source (for relational databases: MYSQL, ORACLE, POSTGRESQL, SQLSERVER, CLICKHOUSE)

```json
{
  "sourceType": "RDBMS",
  "table": "users",
  "column": "id,username,email",
  "splitPk": "id",
  "where": "id > 1000",
  "querySql": null,
  "columns": null
}
```

| Field      | Type   | Required | Description                             |
|------------|--------|----------|-----------------------------------------|
| sourceType | String | Yes      | Must be "RDBMS"                         |
| table      | String | Yes      | Source table name                       |
| column     | String | No       | Comma-separated column names            |
| splitPk    | String | No       | Split key for parallel extraction       |
| where      | String | No       | WHERE clause condition                  |
| querySql   | Array  | No       | Custom SQL statements (overrides where) |
| columns    | Array  | No       | Structured Column objects               |

#### KaiwuDB Source (for both source and target)

```json
{
  "sourceType": "KAIWUDB",
  "table": "users",
  "column": "id,username,email",
  "where": null,
  "beginDateTime": null,
  "endDateTime": null,
  "splitIntervalS": null,
  "tsColumn": null,
  "querySql": null,
  "writeMode": "insert",
  "preSql": null,
  "postSql": null,
  "columns": null
}
```

| Field          | Type   | Required | Description                             |
|----------------|--------|----------|-----------------------------------------|
| sourceType     | String | Yes      | Must be "KAIWUDB"                       |
| table          | String | Yes      | Table name                              |
| column         | String | Yes      | Column names (comma-separated)          |
| where          | String | No       | Reader: WHERE condition                 |
| beginDateTime  | String | No       | Reader: Time range start                |
| endDateTime    | String | No       | Reader: Time range end                  |
| splitIntervalS | Long   | No       | Reader: Window split interval (seconds) |
| tsColumn       | String | No       | Reader: Time-series column name         |
| querySql       | Array  | No       | Reader: Custom SQL array                |
| writeMode      | String | No       | Writer: "insert" (default) or "upsert"  |
| preSql         | Array  | No       | Writer: SQL before write                |
| postSql        | Array  | No       | Writer: SQL after write                 |

#### InfluxDB Source (for INFLUXDB1X/2X)

```json
{
  "sourceType": "INFLUXDB",
  "measurement": "metrics",
  "column": "time,temperature,humidity",
  "splitIntervalS": 3600,
  "beginDateTime": "2024-01-01T00:00:00Z",
  "endDateTime": "2024-12-31T23:59:59Z",
  "readTimeout": 60,
  "connectTimeout": 10,
  "columns": null
}
```

| Field          | Type   | Required | Description                     |
|----------------|--------|----------|---------------------------------|
| sourceType     | String | Yes      | Must be "INFLUXDB"              |
| measurement    | String | Yes      | InfluxDB measurement name       |
| column         | String | Yes      | Column names (comma-separated)  |
| splitIntervalS | Long   | No       | Window split interval (seconds) |
| beginDateTime  | String | No       | Time range start (ISO 8601)     |
| endDateTime    | String | No       | Time range end (ISO 8601)       |
| readTimeout    | Int    | No       | Read timeout (seconds)          |
| connectTimeout | Int    | No       | Connect timeout (seconds)       |

#### Other Source Types

Similar structure for MongoDB, HDFS, FTP, OpenTSDB, TDengine sources. Each has type-specific fields.

---

## API Endpoints

### 1. Health Check

#### GET /health

Check if KDTS server is running.

**Request**: No parameters

**Response**:

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "status": "UP"
  }
}
```

---

### 2. DataSource APIs

#### POST /datasource/validate

Test connection to data source or target.

**Request Body**: `DataSourceRequest`

```json
{
  "engine": "RELATIONAL",
  "type": "MYSQL",
  "url": null,
  "host": "127.0.0.1",
  "port": 3306,
  "username": "root",
  "password": "password",
  "dbName": "test_db",
  "isTarget": false
}
```

| Field    | Type    | Required | Description                         |
|----------|---------|----------|-------------------------------------|
| engine   | String  | Yes      | RELATIONAL or TIMESERIES            |
| type     | String  | Yes      | Source type (MYSQL, ORACLE, etc.)   |
| url      | String  | No       | Full JDBC URL (overrides host:port) |
| host     | String  | No*      | Hostname or IP                      |
| port     | Integer | No*      | Port number                         |
| username | String  | Yes      | Database username                   |
| password | String  | Yes      | Database password                   |
| dbName   | String  | No       | Default database                    |
| isTarget | Boolean | No       | true for target validation          |

*Required if url not provided

**Response**:

```json
{
  "code": 0,
  "message": "success",
  "data": "SUCCEED"
}
```

> **IMPORTANT**: On FAILED validation, KDTS may still return `code: 0` with the
> failure text in `data`. Success is `data == "SUCCEED"`,
> NOT `code == 0`. The python api_client normalizes non-SUCCEED data to code=2001 automatically.

---

#### POST /datasource/databases

List all databases on source.

**Request Body**: `DataSourceRequest` (same as validate)

```json
{
  "engine": "RELATIONAL",
  "type": "MYSQL",
  "host": "127.0.0.1",
  "port": 3306,
  "username": "root",
  "password": "password",
  "dbName": null,
  "isTarget": false
}
```

**Response**:

```json
{
  "code": 0,
  "message": "success",
  "data": [
    "information_schema",
    "mysql",
    "performance_schema",
    "shop_db",
    "test_db"
  ]
}
```

---

#### POST /datasource/metadata

Read source metadata (tables, columns, PKs, constraints, indexes).

**Request Body**: `MetadataRequest`

```json
{
  "source": {
    "engine": "RELATIONAL",
    "type": "MYSQL",
    "url": null,
    "host": "127.0.0.1",
    "port": 3306,
    "username": "root",
    "password": "password",
    "dbName": "shop_db",
    "isTarget": false
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

| Field               | Type    | Required | Description                                          |
|---------------------|---------|----------|------------------------------------------------------|
| source              | Object  | Yes      | DataSourceRequest with dbName set to source database |
| metadata            | Object  | Yes      | MetaData config controlling what to read             |
| metadata.enable     | Boolean | Yes      | Enable metadata reading                              |
| metadata.primaryKey | Boolean | No       | Read primary keys                                    |
| metadata.constraint | Boolean | No       | Read constraints                                     |
| metadata.comment    | Boolean | No       | Read table/column comments                           |
| metadata.index      | Boolean | No       | Read indexes                                         |
| metadata.view       | Boolean | No       | Read views                                           |

**Response**: `Database` object (see Common Data Structures above)

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "type": "MYSQL",
    "name": "shop_db",
    "encoding": "UTF-8",
    "interval": null,
    "retentions": null,
    "comment": null,
    "tableMap": {
      "users": {
        "schemaName": "shop_db",
        "sourceTableName": "users",
        "tableName": "users",
        "tableCollation": "utf8mb4_general_ci",
        "tableComment": "User information table",
        "columns": [
          {
            "dbType": "MYSQL",
            "schemaName": "shop_db",
            "tableName": "users",
            "sourceColumnName": "id",
            "columnName": "id",
            "sourceColumnType": "BIGINT",
            "columnType": "BIGINT",
            "columnOrder": 1,
            "strLength": null,
            "precision": null,
            "scale": null,
            "nullAble": false,
            "comment": "User ID",
            "extra": "auto_increment",
            "columnKey": "PRI",
            "finalConvertDataType": "BIGINT",
            "isChecked": true,
            "isTs": false,
            "isTag": false,
            "isPrimaryTag": false
          },
          {
            "sourceColumnName": "username",
            "columnName": "username",
            "sourceColumnType": "VARCHAR",
            "columnType": "VARCHAR(100)",
            "columnOrder": 2,
            "strLength": 100,
            "nullAble": false,
            "comment": "Login username",
            "columnKey": "UNI",
            "finalConvertDataType": "VARCHAR(100)",
            "isChecked": true,
            "isTs": false,
            "isTag": false
          }
        ],
        "primaryKey": {
          "schemaName": "shop_db",
          "tableName": "users",
          "pkName": "PRIMARY",
          "columns": [
            {
              "columnName": "id",
              "asc": true
            }
          ]
        },
        "constraint": [],
        "indexes": [
          {
            "schemaName": "shop_db",
            "tableName": "users",
            "indexName": "idx_username",
            "columns": [
              {
                "columnName": "username",
                "asc": true
              }
            ]
          }
        ],
        "source": null
      }
    },
    "viewMap": {}
  }
}
```

---

### 3. Metadata APIs

#### POST /metadata/preview

Preview DDL for target KaiwuDB based on source metadata.

**Request Body**: `PreviewDdlRequest`

```json
{
  "target": {
    "engine": "RELATIONAL",
    "type": "KAIWUDB",
    "url": null,
    "host": "127.0.0.1",
    "port": 26257,
    "username": "root",
    "password": "kwdb_password",
    "dbName": null,
    "isTarget": true
  },
  "sourceDb": {
    "type": "MYSQL",
    "name": "shop_db",
    "encoding": "UTF-8",
    "interval": null,
    "retentions": null,
    "comment": null,
    "tableMap": {
      "users": {
        "tableName": "users",
        "columns": [],
        "primaryKey": {},
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

| Field        | Type    | Required | Description                                             |
|--------------|---------|----------|---------------------------------------------------------|
| target       | Object  | Yes      | DataSourceRequest for target (must be KAIWUDB type)     |
| sourceDb     | Object  | Yes      | Database object from /datasource/metadata response      |
| metadata     | Object  | No       | MetaData config (can override source metadata settings) |
| isTimeSeries | Boolean | No       | true to generate time-series DDL.                       |

**Response**: `DdlScript` object

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "dbName": "SHOP_DB",
    "createDb": "CREATE DATABASE \"SHOP_DB\" ENGINE=RELATIONAL COMMENT='Source: MySQL shop_db'",
    "table": {
      "users": "CREATE TABLE \"users\" (\n  \"id\" BIGINT NOT NULL AUTO_INCREMENT COMMENT 'User ID',\n  \"username\" VARCHAR(100) NOT NULL COMMENT 'Login username',\n  \"email\" VARCHAR(255) COMMENT 'Email address',\n  \"created_at\" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Creation time',\n  PRIMARY KEY (\"id\"),\n  UNIQUE INDEX \"idx_username\" (\"username\")\n) ENGINE=RELATIONAL COMMENT='User information table'",
      "orders": "CREATE TABLE \"orders\" (\n  \"id\" BIGINT NOT NULL AUTO_INCREMENT,\n  \"user_id\" BIGINT NOT NULL,\n  \"total_amount\" DECIMAL(12,2) NOT NULL,\n  \"status\" TINYINT NOT NULL DEFAULT 0,\n  \"created_at\" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,\n  PRIMARY KEY (\"id\")\n) ENGINE=RELATIONAL COMMENT='Order table'"
    },
    "view": {}
  }
}
```

---

#### POST /metadata/execute

Execute DDL on target KaiwuDB.

**Request Body**: `ExecuteDdlRequest`

```json
{
  "target": {
    "engine": "RELATIONAL",
    "type": "KAIWUDB",
    "host": "127.0.0.1",
    "port": 26257,
    "username": "root",
    "password": "kwdb_password",
    "dbName": null,
    "isTarget": true
  },
  "ddlScript": {
    "dbName": "SHOP_DB",
    "createDb": "CREATE DATABASE \"SHOP_DB\" ENGINE=RELATIONAL",
    "table": {
      "users": "CREATE TABLE \"users\" (\"id\" BIGINT NOT NULL, \"username\" VARCHAR(100))",
      "orders": "CREATE TABLE \"orders\" (\"id\" BIGINT NOT NULL, \"user_id\" BIGINT)"
    },
    "view": {}
  },
  "autoDdl": true
}
```

| Field     | Type    | Required | Description                                             |
|-----------|---------|----------|---------------------------------------------------------|
| target    | Object  | Yes      | DataSourceRequest for target (must be KAIWUDB type)     |
| ddlScript | Object  | Yes      | DdlScript from /metadata/preview response               |
| autoDdl   | Boolean | No       | true = execute all DDL, false = return script path only |

**Response**: Script file path

```json
{
  "code": 0,
  "message": "success",
  "data": "/opt/kdts/data/sql/kaiwudb_ddl_1719290000.sql"
}
```

---

### 4. DataX APIs

#### POST /datax/build

Build DataX migration job script.

**Request Body**: `MigrateDataRequest`

```json
{
  "source": {
    "engine": "RELATIONAL",
    "type": "MYSQL",
    "host": "127.0.0.1",
    "port": 3306,
    "username": "root",
    "password": "password",
    "dbName": "shop_db",
    "isTarget": false
  },
  "target": {
    "engine": "RELATIONAL",
    "type": "KAIWUDB",
    "host": "127.0.0.1",
    "port": 26257,
    "username": "root",
    "password": "kwdb_password",
    "dbName": "SHOP_DB",
    "isTarget": true
  },
  "tables": [
    {
      "source": {
        "sourceType": "RDBMS",
        "table": "users",
        "column": "id,username,email,created_at,status",
        "splitPk": "id",
        "where": null,
        "querySql": null
      },
      "target": {
        "sourceType": "KAIWUDB",
        "table": "users",
        "column": "id,username,email,created_at,status",
        "writeMode": "insert",
        "preSql": null,
        "postSql": null
      }
    }
  ],
  "data": {
    "enable": true,
    "fetchSize": 1000,
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
    "setting": {
      "speed": {
        "channel": 4
      },
      "errorLimit": {
        "percentage": 0.02
      }
    }
  }
}
```

| Field                                    | Type    | Required | Description                                                                               |
|------------------------------------------|---------|----------|-------------------------------------------------------------------------------------------|
| source                                   | Object  | Yes      | DataSourceRequest for source database                                                     |
| target                                   | Object  | Yes      | DataSourceRequest for target (must be KAIWUDB type)                                       |
| tables                                   | Array   | No       | TableMapping array (empty = full database auto-migration)                                 |
| tables.source                            | Object  | Yes*     | Source configuration (RDBMS, INFLUXDB, etc.)                                              |
| tables.target                            | Object  | No       | Target configuration (KAIWUDB). Auto-derived if missing                                   |
| data                                     | Object  | **Yes**  | **Data migration settings. Both core and setting are REQUIRED for successful migration!** |
| data.enable                              | Boolean | Yes      | Enable data migration (default: true)                                                     |
| data.fetchSize                           | Integer | Yes      | Records per fetch from source (default: 1000)                                             |
| data.batchSize                           | Integer | Yes      | Records per batch to target (default: 1000)                                               |
| data.core                                | Object  | **Yes**  | **DataX core configuration. REQUIRED for migration!**                                     |
| data.core.transport                      | Object  | Yes      | DataX transport configuration                                                             |
| data.core.transport.channel              | Object  | Yes      | DataX channel configuration                                                               |
| data.core.transport.channel.speed        | Object  | Yes      | Speed configuration with byte and record limits                                           |
| data.core.transport.channel.speed.byte   | Integer | Yes      | Byte-level speed limit in bytes/sec (default: 1048576 = 1MB/s)                            |
| data.core.transport.channel.speed.record | Integer | Yes      | Record-level speed limit in records/sec (default: 1000)                                   |
| data.setting                             | Object  | **Yes**  | **DataX setting configuration. REQUIRED for migration!**                                  |
| data.setting.speed                       | Object  | Yes      | Global speed configuration                                                                |
| data.setting.speed.channel               | Integer | Yes      | Number of parallel channels (default: 4)                                                  |
| data.setting.errorLimit                  | Object  | Yes      | Error tolerance configuration                                                             |
| data.setting.errorLimit.percentage       | Float   | Yes      | Acceptable error percentage (default: 0.02 = 2%)                                          |

**Key Notes**:

- Empty `tables` array = full database migration (auto-discover all tables)
- Non-empty `tables` = table-level migration (only specified tables)
- Target `source.sourceType` must be "KAIWUDB"
- **CRITICAL**: The `data` object with `core` and `setting` fields is REQUIRED. Missing these fields will cause migration failures!

**Response**: List of generated script filenames

```json
{
  "code": 0,
  "message": "success",
  "data": [
    "MYSQL2KAIWUDB_1719290000.json",
    "MYSQL2KAIWUDB_1719290001.json"
  ]
}
```

---

#### POST /datax/execute

Execute built migration scripts.

**Request Body**: Array of script names

```json
[
  "MYSQL2KAIWUDB_1719290000.json"
]
```

**Response**: List of log file paths

```json
{
  "code": 0,
  "message": "success",
  "data": [
    "/opt/kdts/data/log/kaiwudb_migrate_1719290000.log"
  ]
}
```

---

#### GET /datax/status

Query migration task status.

**Query Parameters**:

| Parameter  | Type   | Required | Description      |
|------------|--------|----------|------------------|
| scriptName | String | Yes      | Script file name |

**Response**: Job status object

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "scriptName": "MYSQL2KAIWUDB_1719290000.json",
    "status": "RUNNING",
    "progress": 45.2,
    "message": "Processing batch 452/1000",
    "startTime": 1719290000000,
    "elapsedTime": 125000,
    "endTime": null
  }
}
```

**Status Values**:

| Status    | Description                      |
|-----------|----------------------------------|
| SUBMITTED | Script built, not yet started    |
| RUNNING   | Migration in progress            |
| SUCCEEDED | Migration completed successfully |
| FAILED    | Migration failed                 |
| KILLED    | Migration killed by user         |
| UNKNOWN   | Status cannot be determined      |

---

#### POST /datax/control

Control migration task (kill or query).

**Request Body**: `JobControlRequest`

```json
{
  "scriptName": "MYSQL2KAIWUDB_1719290000.json",
  "action": "KILL"
}
```

| Field      | Type   | Required | Description       |
|------------|--------|----------|-------------------|
| scriptName | String | Yes      | Script file name  |
| action     | String | Yes      | "QUERY" or "KILL" |

| Action | Description                                    |
|--------|------------------------------------------------|
| QUERY  | Get current status (same as GET /datax/status) |
| KILL   | Terminate running migration process            |

**Response**: Job control result

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "status": "KILLED",
    "message": "Process terminated by user"
  }
}
```

---

## 5. Complete Migration Flow Example

### Step 1: Validate Source Connection

```bash
curl -X POST http://localhost:8989/kdts/api/v1/datasource/validate \
  -H "Content-Type: application/json" \
  -d '{
    "engine": "RELATIONAL",
    "type": "MYSQL",
    "host": "192.168.1.50",
    "port": 3306,
    "username": "root",
    "password": "password",
    "dbName": null,
    "isTarget": false
  }'
```

### Step 2: Validate Target Connection

```bash
curl -X POST http://localhost:8989/kdts/api/v1/datasource/validate \
  -d '{
    "engine": "RELATIONAL",
    "type": "KAIWUDB",
    "host": "127.0.0.1",
    "port": 26257,
    "username": "root",
    "password": "kwdb_password",
    "isTarget": true
  }'
```

### Step 3: Read Source Metadata

```bash
curl -X POST http://localhost:8989/kdts/api/v1/datasource/metadata \
  -d '{
    "source": {
      "engine": "RELATIONAL",
      "type": "MYSQL",
      "host": "192.168.1.50",
      "port": 3306,
      "username": "root",
      "password": "password",
      "dbName": "shop_db",
      "isTarget": false
    },
    "metadata": {
      "enable": true,
      "primaryKey": true,
      "constraint": true,
      "comment": true,
      "index": true,
      "view": false
    }
  }'
```

### Step 4: Preview DDL

```bash
curl -X POST http://localhost:8989/kdts/api/v1/metadata/preview \
  -d '{
    "target": {
      "engine": "RELATIONAL",
      "type": "KAIWUDB",
      "host": "127.0.0.1",
      "port": 26257,
      "username": "root",
      "password": "kwdb_password",
      "isTarget": true
    },
    "sourceDb": {},
    "metadata": {},
    "isTimeSeries": false
  }'
```

### Step 5: Execute DDL

```bash
curl -X POST http://localhost:8989/kdts/api/v1/metadata/execute \
  -d '{
    "target": {},
    "ddlScript": {},
    "autoDdl": true
  }'
```

### Step 6: Build Migration Script

```bash
curl -X POST http://localhost:8989/kdts/api/v1/datax/build \
  -d '{
    "source": {},
    "target": {},
    "tables": [],
    "data": {
      "enable": true,
      "fetchSize": 1000,
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
      "setting": {
        "speed": {
          "channel": 4
        },
        "errorLimit": {
          "percentage": 0.02
        }
      }
    }
  }'
```

**Note**: The `data` object with `core` and `setting` fields is REQUIRED for successful DataX execution.
Without these fields, the migration will fail.

### Step 7: Execute Migration

```bash
curl -X POST http://localhost:8989/kdts/api/v1/datax/execute \
  -d '["MYSQL2KAIWUDB_1719290000.json"]'
```

### Step 8: Monitor Progress

```bash
curl -X GET "http://localhost:8989/kdts/api/v1/datax/status?scriptName=MYSQL2KAIWUDB_1719290000.json"
```

---

## 6. Common Response Patterns

### Success (code = 0)

```json
{
  "code": 0,
  "message": "success",
  "timestamp": 1719290000000,
  "data": "result"
}
```

### Business Error (code != 0, HTTP 200)

```json
{
  "code": 2001,
  "message": "Connection failed - check network and credentials",
  "timestamp": 1719290000000,
  "data": null
}
```

### System Error (HTTP 500)

```json
{
  "code": 9999,
  "message": "Internal server error",
  "timestamp": 1719290000000,
  "data": null
}
```

### Resource Unavailable (HTTP 503)

```json
{
  "code": 5001,
  "message": "Thread pool full - retry later",
  "timestamp": 1719290000000,
  "data": null
}
```

---

## 7. Source Type Capabilities

> **Based on KDTS SourceTypes.java implementation**:
> - Full Migration = `checkSourceForAllData()`: Supports auto-discovery of all tables
> - Metadata = `checkSourceForMetadata()`: Supports reading table structure for DDL generation
> - Data Only = `checkSourceForData()`: Supports data migration only
>
> **Note**: CLICKHOUSE and KAIWUDB support Full Migration (auto-discovery) but NOT Metadata reading.

| Source Type | Engine     | Full Migration | Metadata | Data Only | Notes                                       |
|-------------|------------|----------------|----------|-----------|---------------------------------------------|
| MYSQL       | RELATIONAL | Yes            | Yes      | Yes       | Primary relational source                   |
| ORACLE      | RELATIONAL | Yes            | Yes      | Yes       | Supports SID and SERVICE_NAME               |
| POSTGRESQL  | RELATIONAL | Yes            | Yes      | Yes       | Supports PostgreSQL-specific types          |
| SQLSERVER   | RELATIONAL | No             | Yes      | Yes       | Metadata + Data, no full migration          |
| CLICKHOUSE  | RELATIONAL | Yes            | No       | Yes       | Full Migration (auto-discover), no Metadata |
| KAIWUDB     | *          | Yes            | No       | Yes       | Full Migration (auto-discover), no Metadata |
| TDENGINE3X  | TIMESERIES | Yes            | Yes      | Yes       | Primary time-series source                  |
| TDENGINE2X  | TIMESERIES | No             | No       | Yes       | Data-only migration                         |
| INFLUXDB1X  | TIMESERIES | No             | Yes      | Yes       | Metadata + Data (two-step)                  |
| INFLUXDB2X  | TIMESERIES | No             | Yes      | Yes       | Metadata + Data (two-step), needs Token/Org |
| OPENTSDB    | TIMESERIES | No             | No       | Yes       | Data-only migration                         |
| MONGODB     | TIMESERIES | No             | No       | Yes       | Data-only migration                         |
| FTP         | TIMESERIES | No             | No       | Yes       | File source (CSV/JSON)                      |
| HDFS        | TIMESERIES | No             | No       | Yes       | File source (Parquet/ORC)                   |

---

## 8. Timeout and Retry

- **Connection Timeout**: 5 seconds (recommended)
- **Read Timeout**: 30 seconds for standard operations, longer for large migrations
- **Retry Logic**:
    - 503 errors: respect Retry-After header
    - 2001 errors: check configuration before retrying
    - Other errors: retry only after fixing root cause

---

## 9. File Paths

- **Script Output**: `/opt/kdts/datax/job/{SCRIPT_NAME}`
- **Log Output**: `/opt/kdts/data/log/{LOG_FILE}`
- **SQL Output**: `/opt/kdts/data/sql/{SQL_FILE}`
- **DataX Home**: Configured in KDTS application.yml

---

## 10. Version Information

This API reference is based on KDTS Server source code in `kw-datax-utils`.
Last updated: 2026-08-03

Source packages:

- Controller: `com.kaiwudb.migration.controller`
- DTO: `com.kaiwudb.migration.dto`
- Service: `com.kaiwudb.migration.service`
- Constants: `com.kaiwudb.migration.constant`

---

## 11. DataX Configuration Reference

This section documents the complete DataX configuration based on KDTS source code and DataX official documentation.

**DataX Three-Tier Rate Limiting Model** (Source: [DataX Parameter Tuning Guide](https://blog.csdn.net/weixin_44893236/article/details/149827940)):
```
Tier 1: setting.speed.channel - Number of channels (fixed channel count)
Tier 2: setting.speed.byte/record - Global rate limit (can be combined with channel)
Tier 3: core.transport.channel.speed.byte/record - Per-channel rate limit
```

**Important: channel, byte, and record can be combined to implement flexible rate limiting strategies!**

Source classes:
- `com.kaiwudb.migration.dto.config.UserData`
- `com.kaiwudb.migration.dto.datax.Core`
- `com.kaiwudb.migration.dto.datax.Setting`

---

### 11.1 UserData Configuration Structure

**Example 1: Fixed Channel Count + Global Rate Limit** (recommended for most scenarios)
```json
{
  "data": {
    "enable": true,
    "fetchSize": 1000,
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
    "setting": {
      "speed": {
        "channel": 4,
        "byte": 52428800,
        "record": 40000
      },
      "errorLimit": {
        "record": 50000,
        "percentage": 0.02
      }
    }
  }
}
```
**Note:** Fixed 4 channels, global rate limit of 50MB/s and 40,000 records/s, per-channel rate limit of 12.5MB/s and 10,000 records/s

**Example 2: Byte-Only and Record-Only Rate Limiting (Auto-Calculate Channel Count)**
```json
{
  "data": {
    "enable": true,
    "fetchSize": 1000,
    "batchSize": 1000,
    "core": {
      "transport": {
        "channel": {
          "speed": {
            "byte": 10485760,
            "record": 5000
          }
        }
      }
    },
    "setting": {
      "speed": {
        "byte": 52428800,
        "record": 40000
      },
      "errorLimit": {
        "record": 50000,
        "percentage": 0.02
      }
    }
  }
}
```
**Note:** Rate limiting by both bytes and records, channel count calculated separately: 52428800 ÷ 10485760 = 5, 40000 ÷ 5000 = 8, take the larger value of 8 channels

---

### 11.2 UserData Field Reference

| Field Name | Type             | Default | Description                                    |
|------------|------------------|---------|------------------------------------------------|
| enable     | boolean          | false   | Whether to enable user data migration          |
| fetchSize  | int              | 1000    | Number of records fetched per pull from source |
| batchSize  | int              | 1000    | Number of records submitted per push to target |
| core       | Core (Object)    | null    | DataX core configuration (per-channel level)   |
| setting    | Setting (Object) | null    | DataX setting configuration (global level)     |

---

### 11.3 Core Configuration Structure (Per-Channel Level)

`core.transport.channel.speed` is a **per-channel level** rate limiting configuration that controls the transmission speed of each independent channel.

```json
{
  "core": {
    "transport": {
      "channel": {
        "speed": {
          "byte": 1048576,
          "record": 1000
        }
      }
    }
  }
}
```

#### Core Field Reference

| Field     | Type               | Default | Description            |
|-----------|--------------------|---------|------------------------|
| transport | Transport (Object) | null    | DataX transport config |

#### Core.Transport Field Reference

| Field   | Type             | Default | Description           |
|---------|------------------|---------|-----------------------|
| channel | Channel (Object) | null    | DataX channel config  |

#### Core.Transport.Channel Field Reference

| Field | Type                  | Default | Description                                                                   |
|-------|-----------------------|---------|-------------------------------------------------------------------------------|
| speed | Map\<String, Object\> | null    | Per-channel rate limit config<br>Example: `{"byte": 1048576, "record": 1000}` |

**Available Keys for speed Map (can be configured simultaneously):**

| Key    | Type | Default | Description                                                                             |
|--------|------|---------|-----------------------------------------------------------------------------------------|
| byte   | Long | null    | Per-channel byte rate limit (bytes/second), e.g., 1048576 means 1MB/s/channel           |
| record | Long | null    | Per-channel record rate limit (records/second), e.g., 1000 means 1000 records/s/channel |

**Notes:**
- `byte` and `record` are **two independent rate limiting dimensions** and can be set simultaneously
- If only one is configured, rate limiting is applied only to that dimension
- If neither is configured, the channel has no rate limit

---

### 11.4 Setting Configuration Structure (Global Level)

`setting.speed` is a **global level** rate limiting configuration that controls the transmission speed of the entire task.

**Configuration Options:**

| Parameter | Type    | Description                                                                                             |
|-----------|---------|---------------------------------------------------------------------------------------------------------|
| channel   | Integer | Fixed channel count. If configured, channel count is fixed and does not participate in auto-calculation |
| byte      | Long    | Global byte rate limit, must be used with core.transport.channel.speed.byte                             |
| record    | Long    | Global record rate limit, must be used with core.transport.channel.speed.record                         |

**Configuration Rules:**
- channel only: Fixed channel count, per-channel rate limit controlled by core.transport.channel.speed
- byte or record only: Auto-calculate channel count = global rate limit / per-channel rate limit
- byte and record together: Calculate required channel count separately, take the larger value
- channel and byte/record together: Channel count fixed, byte/record serve as global rate limits

#### Setting Field Reference

| Field      | Type                  | Default | Description                                                        |
|------------|-----------------------|---------|--------------------------------------------------------------------|
| speed      | Map\<String, Object\> | null    | Global rate limit config, channel/byte/record can be used together |
| errorLimit | Map\<String, Object\> | null    | Error tolerance config                                             |

#### Available Keys for "setting.speed" Map

| Key     | Type    | Default | Description                                                                  |
|---------|---------|---------|------------------------------------------------------------------------------|
| channel | Integer | null    | Fixed channel count, e.g., 4 means 4 parallel channels                       |
| byte    | Long    | null    | Global byte rate limit (bytes/second), total rate limit across all channels  |
| record  | Long    | null    | Global record rate limit (records/second), total records across all channels |

#### Available Keys for setting.errorLimit Map (can be configured simultaneously)

| Key        | Type  | Default | Description                                           |
|------------|-------|---------|-------------------------------------------------------|
| record     | Long  | null    | Maximum allowed number of error records               |
| percentage | Float | 0.02    | Maximum allowed error percentage, e.g., 0.02 means 2% |

---

### 11.5 Configuration Examples

#### 11.5.1 Fixed Channel Count + Global Rate Limit

```json
{
  "setting": {
    "speed": {
      "channel": 4,
      "byte": 52428800,
      "record": 40000
    }
  },
  "core": {
    "transport": {
      "channel": {
        "speed": {
          "byte": 1048576,
          "record": 1000
        }
      }
    }
  }
}
```
- Fixed 4 channels
- Global rate limit of 50MB/s and 40,000 records/s
- Per-channel rate limit of 12.5MB/s and 10,000 records/s

#### 11.5.2 Byte-Only Rate Limiting (Auto-Calculate Channel Count)

```json
{
  "setting": {
    "speed": {
      "byte": 52428800
    }
  },
  "core": {
    "transport": {
      "channel": {
        "speed": {
          "byte": 10485760
        }
      }
    }
  }
}
```
- Channel count auto-calculated: `52428800 ÷ 10485760 = 5` channels

#### 11.5.3 Record-Only Rate Limiting (Auto-Calculate Channel Count)

```json
{
  "setting": {
    "speed": {
      "record": 40000
    }
  },
  "core": {
    "transport": {
      "channel": {
        "speed": {
          "record": 1000
        }
      }
    }
  }
}
```
- Channel count auto-calculated: `40000 ÷ 1000 = 40` channels

#### 11.5.4 Combined Byte and Record Rate Limiting

```json
{
  "setting": {
    "speed": {
      "byte": 52428800,
      "record": 40000
    }
  },
  "core": {
    "transport": {
      "channel": {
        "speed": {
          "byte": 10485760,
          "record": 5000
        }
      }
    }
  }
}
```
- Channel count auto-calculated: max(`52428800 ÷ 10485760`, `40000 ÷ 5000`) = max(5, 8) = 8 channels

#### 11.5.5 Important Constraints

| Constraint                           | Description                                                                                                                                                                           |
|--------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Must be configured in pairs**      | If `setting.speed.byte` is configured, `core.transport.channel.speed.byte` must also be configured                                                                                    |
| **Must be configured in pairs**      | If `setting.speed.record` is configured, `core.transport.channel.speed.record` must also be configured                                                                                |
| **Cannot configure channel in core** | The `channel` parameter can only be configured in `setting.speed`, not in `core.transport.channel.speed`                                                                              |
| **Priority**                         | If both channel and byte/record are configured, channel takes effect and byte/record serve as global rate limits; if only byte/record is configured, channel count is auto-calculated |

---

### 11.6 Configuration Examples

#### Example 1: Recommended Configuration (Auto-Calculate Channel Count)

```json
{
  "data": {
    "enable": true,
    "fetchSize": 1000,
    "batchSize": 1000,
    "core": {
      "transport": {
        "channel": {
          "speed": {
            "byte": 10485760,
            "record": 5000
          }
        }
      }
    },
    "setting": {
      "speed": {
        "byte": 52428800,
        "record": 40000
      },
      "errorLimit": {
        "percentage": 0.02
      }
    }
  }
}
```

**Configuration Note:**
- Each channel: 10MB/s or 5000 records/s
- Global max: 50MB/s or 40,000 records/s
- Channel count auto-calculated as 5 (50MB/s ÷ 10MB/s = 5)
- 2% error tolerance

#### Example 2: Fixed Channel Count Configuration

```json
{
  "data": {
    "enable": true,
    "fetchSize": 1000,
    "batchSize": 1000,
    "core": {
      "transport": {
        "channel": {
          "speed": {
            "byte": 10485760
          }
        }
      }
    },
    "setting": {
      "speed": {
        "channel": 4
      },
      "errorLimit": {
        "percentage": 0.02
      }
    }
  }
}
```

**Configuration Note:**
- Each channel: 10MB/s
- Fixed 4 channels
- Global theoretical rate limit = 10MB/s × 4 = 40MB/s

#### Example 3: High Concurrency Configuration (for 16-core CPU, recommended)

```json
{
  "data": {
    "enable": true,
    "fetchSize": 2000,
    "batchSize": 2000,
    "core": {
      "transport": {
        "channel": {
          "speed": {
            "byte": 5242880,
            "record": 10000
          }
        }
      }
    },
    "setting": {
      "speed": {
        "byte": 78643200,
        "record": 100000
      },
      "errorLimit": {
        "record": 100000
      }
    }
  }
}
```

**Configuration Note:**
- Suitable for 16-core CPU
- Each channel: 5MB/s or 10,000 records/s
- Global: 75MB/s or 100,000 records/s
- Channel count auto-calculated: min(78643200 ÷ 5242880, 100000 ÷ 10000) = min(15, 10) = 10 channels
- Maximum 100,000 errors allowed

---

### 11.7 References

For more detailed information about DataX rate limiting configuration, please refer to:

1. [DataX Parameter Tuning Guide - CSDN](https://blog.csdn.net/weixin_44893236/article/details/149827940)
2. [DataX Job Allocation](https://zhmin.github.io/posts/datax-job/)
3. [DataX Channel Principle](https://zhmin.github.io/posts/datax-channel/)

---

## 12. Source Class Hierarchy

The following class hierarchy is based on KDTS source code:

```
Source (Interface)
├── RDBMS (for MYSQL, ORACLE, POSTGRESQL, SQLSERVER, CLICKHOUSE)
├── KaiwuDB (for KAIWUDB source/target)
├── InfluxDB (for INFLUXDB1X, INFLUXDB2X)
├── TDengine (for TDENGINE2X, TDENGINE3X)
├── OpenTSDB (for OPENTSDB)
├── MongoDB (for MONGODB)
├── Ftp (for FTP)
└── Hdfs (for HDFS)
```

**Source Type Mapping in TableMapping**:

| KDTS Source Type                                 | sourceType Value | Implementation Class |
|--------------------------------------------------|------------------|----------------------|
| MYSQL, ORACLE, POSTGRESQL, SQLSERVER, CLICKHOUSE | RDBMS            | `RDBMS`              |
| KAIWUDB                                          | KAIWUDB          | `KaiwuDB`            |
| TDENGINE2X, TDENGINE3X                           | TDENGINE         | `TDengine`           |
| INFLUXDB1X, INFLUXDB2X                           | INFLUXDB         | `InfluxDB`           |
| MONGODB                                          | MONGODB          | `MongoDB`            |
| OPENTSDB                                         | OPENTSDB         | `OpenTSDB`           |
| FTP                                              | FTP              | `Ftp`                |
| HDFS                                             | HDFS             | `Hdfs`               |

**Note**: The `sourceType` field is used by Jackson polymorphism to deserialize the correct Source implementation.
