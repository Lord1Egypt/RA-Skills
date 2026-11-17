# Configuration Templates

Ready-to-use JSON templates for KDTS migration requests.

---

## Important Configuration Notes

### 1. DataX Configuration Requirements

All data migration requests must include the `data` field, where `core` and `setting` are required configuration items.

Default DataX Configuration (based on KDTS source code):
```json
{
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

### 2. Configuration Field Reference

#### UserData Fields

| Field     | Type    | Default | Description                                    |
|-----------|---------|---------|------------------------------------------------|
| enable    | boolean | false   | Whether to enable user data migration          |
| fetchSize | int     | 1000    | Number of records fetched per pull from source |
| batchSize | int     | 1000    | Number of records submitted per push to target |
| core      | Object  | -       | DataX core config (required)                   |
| setting   | Object  | -       | DataX setting config (required)                |

#### core.transport.channel.speed (Map<String, Object>)
**Note: byte and record can be configured simultaneously (different dimensions of rate limiting), but channel cannot be configured here!**

| Key    | Type    | Description                                                                           |
|--------|---------|---------------------------------------------------------------------------------------|
| byte   | Integer | Per-channel byte-level rate limit (bytes/second), e.g., 1048576 means 1MB/s           |
| record | Integer | Per-channel record-level rate limit (records/second), e.g., 1000 means 1000 records/s |

#### setting.speed (Map<String, Object>)
**Note: The following parameters can be combined to implement flexible rate limiting strategies!**

| Parameter | Type    | Description                                                                                                           |
|-----------|---------|-----------------------------------------------------------------------------------------------------------------------|
| channel   | Integer | Fixed number of parallel channels. If configured, channel count is fixed and does not participate in auto-calculation |
| byte      | Long    | Global byte-level rate limit, must be used with core.transport.channel.speed.byte                                     |
| record    | Long    | Global record-level rate limit, must be used with core.transport.channel.speed.record                                 |

**Configuration Constraints and Calculation Rules:**
- channel only: Fixed channel count, byte/record as global rate limits distributed to each channel
- byte or record only: Auto-calculate channel count = global rate limit / per-channel rate limit
- byte and record together: Calculate required channel count separately, take the larger value
- channel and byte/record together: Channel count fixed, byte/record as global rate limits
- If byte is configured, core.transport.channel.speed.byte must also be configured
- If record is configured, core.transport.channel.speed.record must also be configured

**Example 1: Fixed Channel Count + Global Rate Limit (Recommended)**
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
  },
  "setting": {
    "speed": {
      "channel": 4,
      "byte": 52428800,
      "record": 40000
    }
  }
}
```
**Note:** Fixed 4 channels, global rate limit of 50MB/s and 40,000 records/s, per-channel rate limit of 12.5MB/s and 10,000 records/s

**Example 2: Byte-Only Rate Limiting (Auto-Calculate Channel Count)**
```json
{
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
      "byte": 52428800
    }
  }
}
```
**Note:** Global 50MB/s rate limit, per-channel 10MB/s, channel count auto-calculated as 5

**Example 3: Record-Only Rate Limiting (Auto-Calculate Channel Count)**
```json
{
  "core": {
    "transport": {
      "channel": {
        "speed": {
          "record": 10000
        }
      }
    }
  },
  "setting": {
    "speed": {
      "record": 40000
    }
  }
}
```
**Note:** Global 40,000 records/s rate limit, per-channel 10,000 records/s, channel count auto-calculated as 4

#### setting.errorLimit (Map<String, Object>)
**Note: record and percentage can be configured simultaneously; DataX will apply the stricter limit!**

| Key        | Type    | Description                                           |
|------------|---------|-------------------------------------------------------|
| record     | Integer | Maximum allowed number of error records               |
| percentage | Float   | Maximum allowed error percentage, e.g., 0.02 means 2% |

### 3. Mutually Exclusive Parameters and Notes

The following parameters cannot be used simultaneously:

| Parameter A | Parameter B | Description                          |
|-------------|-------------|--------------------------------------|
| where       | querySql    | Choose WHERE condition or custom SQL |

The following parameters are not recommended to be used simultaneously:

| Parameter A     | Parameter B     | Description                                                           |
|-----------------|-----------------|-----------------------------------------------------------------------|
| splitPk         | querySql        | splitPk requires original table structure, incompatible with querySql |
| column (string) | columns (array) | Choose simple column names or structured definitions                  |

### 4. Combinable Configurations

The following parameters can be used in combination:

| Parameter Combination                      | Description                                                                                                       |
|--------------------------------------------|-------------------------------------------------------------------------------------------------------------------|
| setting.speed.channel + byte + record      | Fixed channel count with global byte and record rate limits                                                       |
| setting.speed.byte + record                | Global byte and record rate limits, DataX calculates required channel count separately and takes the larger value |
| core.transport.channel.speed.byte + record | Per-channel byte and record rate limits (different dimensions)                                                    |
| setting.errorLimit.record + percentage     | Maximum error records and percentage, DataX applies the stricter limit                                            |

### 5. Common Configuration Examples

#### Example 1: Basic Configuration (Recommended)
```json
{
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
**Note:** Basic configuration with 4 parallel channels, per-channel limit of 1MB/s and 1000 records/s

#### Example 2: Auto-Calculate Channel Count by Bytes
```json
{
  "data": {
    "batchSize": 2000,
    "core": {
      "transport": {
        "channel": {
          "speed": {
            "byte": 10485760
          }
        }
      }
    },
    "enable": true,
    "fetchSize": 2000,
    "setting": {
      "errorLimit": {
        "percentage": 0.01
      },
      "speed": {
        "byte": 52428800
      }
    }
  }
}
```
**Note:** Global 50MB/s, per-channel 10MB/s, channel count auto-calculated as 5

#### Example 3: Auto-Calculate Channel Count by Records
```json
{
  "data": {
    "batchSize": 1000,
    "core": {
      "transport": {
        "channel": {
          "speed": {
            "record": 10000
          }
        }
      }
    },
    "enable": true,
    "fetchSize": 1000,
    "setting": {
      "errorLimit": {
        "record": 1000
      },
      "speed": {
        "record": 40000
      }
    }
  }
}
```
**Note:** Global 40,000 records/s, per-channel 10,000 records/s, channel count auto-calculated as 4

---

## 1. DataSource Templates

### 1.1 MySQL Source

```json
{
  "engine": "RELATIONAL",
  "type": "MYSQL",
  "host": "127.0.0.1",
  "port": 3306,
  "username": "root",
  "password": "mysql_password",
  "dbName": "source_database"
}
```

**Alternative with JDBC URL**:

```json
{
  "engine": "RELATIONAL",
  "type": "MYSQL",
  "url": "jdbc:mysql://127.0.0.1:3306/source_database?useSSL=false&serverTimezone=UTC",
  "username": "root",
  "password": "mysql_password",
  "dbName": "source_database"
}
```

### 1.2 Oracle Source

```json
{
  "engine": "RELATIONAL",
  "type": "ORACLE",
  "host": "192.168.1.100",
  "port": 1521,
  "username": "ORACLE_USER",
  "password": "oracle_password",
  "dbName": "ORCL"
}
```

### 1.3 PostgreSQL Source

```json
{
  "engine": "RELATIONAL",
  "type": "POSTGRESQL",
  "host": "192.168.1.101",
  "port": 5432,
  "username": "postgres",
  "password": "pg_password",
  "dbName": "source_db"
}
```

### 1.4 TDengine Source (Time Series)

```json
{
  "engine": "TIMESERIES",
  "type": "TDENGINE3X",
  "host": "192.168.1.103",
  "port": 6030,
  "username": "root",
  "password": "taos_password",
  "dbName": "sensor_db"
}
```

### 1.5 KaiwuDB Target

```json
{
  "engine": "RELATIONAL",
  "type": "KAIWUDB",
  "host": "127.0.0.1",
  "port": 26257,
  "username": "root",
  "password": "kwdb_password",
  "dbName": "target_database"
}
```

**Time Series Target**:

```json
{
  "engine": "TIMESERIES",
  "type": "KAIWUDB",
  "host": "127.0.0.1",
  "port": 26257,
  "username": "root",
  "password": "kwdb_password",
  "dbName": "target_ts"
}
```

---

## 2. Migration Request Templates

### 2.1 Full Database Migration (Relational)

For sources that support full migration (auto-discovery): MySQL, Oracle, PostgreSQL, ClickHouse, KaiwuDB.

```json
{
  "source": {
    "engine": "RELATIONAL",
    "type": "MYSQL",
    "host": "192.168.1.100",
    "port": 3306,
    "username": "root",
    "password": "source_password",
    "dbName": "source_database"
  },
  "target": {
    "engine": "RELATIONAL",
    "type": "KAIWUDB",
    "host": "127.0.0.1",
    "port": 26257,
    "username": "root",
    "password": "kwdb_password",
    "dbName": "target_database",
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

**Key Points**:

- Empty `tables` array = auto-discover all tables
- `setting.speed.channel` = parallel read/write threads
- `setting.errorLimit.percentage` = % of rows that can fail before stopping
- `core.transport.channel.speed.byte` = byte-level speed limit per channel (default: 1048576 = 1MB/s)
- `core.transport.channel.speed.record` = record-level speed limit per channel (default: 1000 records/s)
- **CRITICAL**: Both `core` and `setting` fields are REQUIRED for successful DataX execution

### 2.2 Table-Level Migration

For sources that don't support full migration (no auto-discovery): SQL Server, TDengine 2.x, InfluxDB 1.x/2.x, MongoDB, FTP, HDFS.

```json
{
  "source": {
    "engine": "RELATIONAL",
    "type": "SQLSERVER",
    "host": "192.168.1.102",
    "port": 1433,
    "username": "sa",
    "password": "source_password",
    "dbName": "source_database"
  },
  "target": {
    "engine": "RELATIONAL",
    "type": "KAIWUDB",
    "host": "127.0.0.1",
    "port": 26257,
    "username": "root",
    "password": "kwdb_password",
    "dbName": "target_database",
    "isTarget": true
  },
  "tables": [
    {
      "source": {
        "sourceType": "RDBMS",
        "table": "customers",
        "column": "*"
      },
      "target": {
        "sourceType": "KAIWUDB",
        "table": "customers",
        "column": "*",
        "writeMode": "insert"
      }
    }
  ],
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

### 2.3 Time Series Migration

```json
{
  "source": {
    "engine": "TIMESERIES",
    "type": "TDENGINE3X",
    "host": "192.168.1.103",
    "port": 6030,
    "username": "root",
    "password": "taos_password",
    "dbName": "sensor_db"
  },
  "target": {
    "engine": "TIMESERIES",
    "type": "KAIWUDB",
    "host": "127.0.0.1",
    "port": 26257,
    "username": "root",
    "password": "kwdb_password",
    "dbName": "sensor_target",
    "isTarget": true
  },
  "tables": [
    {
      "source": {
        "sourceType": "TDENGINE",
        "table": "temperature_readings",
        "column": "*",
        "beginDateTime": "2024-01-01 00:00:00",
        "endDateTime": "2024-12-31 23:59:59"
      },
      "target": {
        "sourceType": "KAIWUDB",
        "table": "temperature_readings",
        "column": "*",
        "writeMode": "insert"
      }
    }
  ],
  "data": {
    "batchSize": 5000,
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
    "fetchSize": 5000,
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

### 2.4 Migration with WHERE Filter

```json
{
  "source": {
    "engine": "RELATIONAL",
    "type": "MYSQL",
    "host": "192.168.1.100",
    "port": 3306,
    "username": "root",
    "password": "source_password",
    "dbName": "source_db"
  },
  "target": {
    "engine": "RELATIONAL",
    "type": "KAIWUDB",
    "host": "127.0.0.1",
    "port": 26257,
    "username": "root",
    "password": "kwdb_password",
    "dbName": "target_db",
    "isTarget": true
  },
  "tables": [
    {
      "source": {
        "sourceType": "RDBMS",
        "table": "orders",
        "column": "*",
        "where": "order_date >= '2024-01-01' AND status = 'completed'"
      },
      "target": {
        "sourceType": "KAIWUDB",
        "table": "orders_2024",
        "column": "*",
        "writeMode": "insert"
      }
    }
  ],
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

### 2.5 Parallel Migration with splitPk

```json
{
  "source": {
    "engine": "RELATIONAL",
    "type": "MYSQL",
    "host": "192.168.1.100",
    "port": 3306,
    "username": "root",
    "password": "source_password",
    "dbName": "large_db"
  },
  "target": {
    "engine": "RELATIONAL",
    "type": "KAIWUDB",
    "host": "127.0.0.1",
    "port": 26257,
    "username": "root",
    "password": "kwdb_password",
    "dbName": "target_db",
    "isTarget": true
  },
  "tables": [
    {
      "source": {
        "sourceType": "RDBMS",
        "table": "big_table",
        "column": "*",
        "splitPk": "id"
      },
      "target": {
        "sourceType": "KAIWUDB",
        "table": "big_table",
        "column": "*",
        "writeMode": "insert"
      }
    }
  ],
  "data": {
    "batchSize": 5000,
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
    "fetchSize": 5000,
    "setting": {
      "errorLimit": {
        "percentage": 0.02
      },
      "speed": {
        "channel": 8
      }
    }
  }
}
```

### 2.6 Data-Only Migration (Tables Exist)

Skip DDL steps, go directly to build.

```json
{
  "source": {
    "engine": "RELATIONAL",
    "type": "MYSQL",
    "host": "192.168.1.100",
    "port": 3306,
    "username": "root",
    "password": "source_password",
    "dbName": "source_db"
  },
  "target": {
    "engine": "RELATIONAL",
    "type": "KAIWUDB",
    "host": "127.0.0.1",
    "port": 26257,
    "username": "root",
    "password": "kwdb_password",
    "dbName": "target_db",
    "isTarget": true
  },
  "tables": [
    {
      "source": {
        "sourceType": "RDBMS",
        "table": "existing_table",
        "column": "*"
      },
      "target": {
        "sourceType": "KAIWUDB",
        "table": "existing_table",
        "column": "*",
        "writeMode": "insert"
      }
    }
  ],
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

---

## 3. Metadata Configuration

Metadata config uses `MetaData` fields from KDTS API. Full field reference:

- `enable` (boolean): Enable metadata extraction, default `true`
- `autoDdl` (boolean): Auto-generate DDL statements, default `true`
- `primaryKey` (boolean): Include primary key definitions, default `true`
- `constraint` (boolean): Include constraint definitions, default `true`
- `comment` (boolean): Include table/column comments, default `true`
- `index` (boolean): Include index definitions, default `true`
- `view` (boolean): Include view definitions, default `false`

### Full Metadata (Slower, Complete)

```json
{
  "enable": true,
  "autoDdl": true,
  "primaryKey": true,
  "constraint": true,
  "comment": true,
  "index": true,
  "view": true
}
```

### Minimal Metadata (Faster)

```json
{
  "enable": true,
  "autoDdl": true,
  "primaryKey": true,
  "constraint": false,
  "comment": false,
  "index": false,
  "view": false
}
```

---

## 4. DDL Execution

### Preview DDL Request

The `sourceDb` field must be a complete `Database` object returned from `/datasource/metadata` API.
Do NOT pass a string - use the full object structure.

```json
{
  "target": {
    "engine": "RELATIONAL",
    "type": "KAIWUDB",
    "host": "127.0.0.1",
    "port": 26257,
    "username": "root",
    "password": "kwdb_password",
    "dbName": "target_db",
    "isTarget": true
  },
  "sourceDb": {
    "type": "MYSQL",
    "name": "source_db",
    "encoding": "UTF-8",
    "tableMap": {
      "users": {
        "tableName": "users",
        "columns": {
          "id": {
            "columnName": "id",
            "dataType": "BIGINT",
            "nullable": false,
            "primaryKey": true
          },
          "name": {
            "columnName": "name",
            "dataType": "VARCHAR(100)",
            "nullable": true
          }
        }
      }
    },
    "viewMap": {}
  },
  "metadata": {
    "primaryKey": true,
    "constraint": true,
    "comment": true,
    "index": true,
    "view": false
  },
  "isTimeSeries": false
}
```

### Execute DDL Request

The `ddlScript` must be a `DdlScript` object returned from `/metadata/preview` API.

```json
{
  "target": {
    "engine": "RELATIONAL",
    "type": "KAIWUDB",
    "host": "127.0.0.1",
    "port": 26257,
    "username": "root",
    "password": "kwdb_password",
    "dbName": "target_db",
    "isTarget": true
  },
  "ddlScript": {
    "dbName": "SOURCE_DB",
    "createDb": "CREATE DATABASE \"SOURCE_DB\"",
    "table": {
      "users": "CREATE TABLE \"users\" (\"id\" BIGINT NOT NULL, \"name\" VARCHAR(100), PRIMARY KEY (\"id\"))"
    },
    "view": {}
  },
  "autoDdl": true
}
```

**Response**: Returns absolute path of executed SQL file, e.g., `/data/kwdb/logs/ddl_20240115_143022.sql`

---

## 5. Task Control

### Query Status

```
GET /kdts/api/v1/datax/status?scriptName=MYSQL2KAIWUDB_1719290000.json
```

### Kill Task

POST /kdts/api/v1/datax/control

```json
{
  "scriptName": "MYSQL2KAIWUDB_1719290000.json",
  "action": "KILL"
}
```

---

## 6. Data Source Compatibility Matrix

| Source Type | Full Migration | Metadata | Time Filter | Custom SQL | Notes                                        |
|-------------|----------------|----------|-------------|------------|----------------------------------------------|
| MYSQL       | Yes            | Yes      | No          | Yes        | Full support                                 |
| ORACLE      | Yes            | Yes      | No          | Yes        | Full support                                 |
| POSTGRESQL  | Yes            | Yes      | No          | Yes        | Full support                                 |
| SQLSERVER   | No             | Yes      | No          | Yes        | Metadata + Data, no full migration           |
| CLICKHOUSE  | Yes            | No       | No          | Yes        | Auto-discovery, no metadata                  |
| KAIWUDB     | Yes            | No       | No          | Yes        | Auto-discovery, no metadata, engine required |
| TDENGINE3X  | Yes            | Yes      | Yes         | No         | Full support                                 |
| TDENGINE2X  | No             | No       | Yes         | No         | Data-only migration                          |
| INFLUXDB1X  | No             | Yes      | Yes         | No         | Metadata + Data, no full migration           |
| INFLUXDB2X  | No             | Yes      | Yes         | No         | Metadata + Data, no full migration           |
| OPENTSDB    | No             | No       | Yes         | No         | Data-only migration                          |
| MONGODB     | No             | No       | No          | Yes        | Data-only migration                          |
| FTP         | No             | No       | No          | No         | Data-only migration                          |
| HDFS        | No             | No       | No          | No         | Data-only migration                          |

---

## 7. Source-Target Engine Compatibility (STRICT)

**CRITICAL**: The following compatibility rules are enforced by KDTS:

| Source Type                                      | Source Engine            | Allowed Target Engines   | Restriction                                 |
|--------------------------------------------------|--------------------------|--------------------------|---------------------------------------------|
| MYSQL, ORACLE, POSTGRESQL, SQLSERVER, CLICKHOUSE | RELATIONAL               | RELATIONAL, TIMESERIES   | Relational sources have flexibility         |
| KAIWUDB (source)                                 | RELATIONAL or TIMESERIES | RELATIONAL or TIMESERIES | KaiwuDB can be migrated between engines     |
| TDENGINE2X, TDENGINE3X                           | TIMESERIES               | **ONLY TIMESERIES**      | Cannot migrate to RELATIONAL                |
| INFLUXDB1X, INFLUXDB2X                           | TIMESERIES               | **ONLY TIMESERIES**      | Cannot migrate to RELATIONAL                |
| OPENTSDB                                         | TIMESERIES               | **ONLY TIMESERIES**      | Cannot migrate to RELATIONAL                |
| MONGODB, FTP, HDFS                               | TIMESERIES               | TIMESERIES               | File/NoSQL sources are time series oriented |

**If Time Series Source → Relational Target is requested:**
1. The migration will FAIL at the KDTS API level
2. Alternative: Export data from source, transform as needed, import to KaiwuDB RELATIONAL
3. For InfluxDB/TDengine: Use built-in export (CSV, Line Protocol) then bulk load

---

## 8. KaiwuDB Time-Series Table Constraints

When migrating to KaiwuDB with TIMESERIES engine, the following constraints apply:

| Constraint                       | Limit     | Error Code | Description                       |
|----------------------------------|-----------|------------|-----------------------------------|
| Maximum columns per table        | 128       | 3004       | Total of Tag + Value columns      |
| Maximum primary tags             | 4         | 3004       | Cannot exceed 4 primary tags      |
| Maximum tag/column name length   | 128 bytes | 3005       | Each name must be within limit    |
| Must have at least 1 primary tag | 1         | 3006       | Required for time-series indexing |

### Solutions for Exceeding Constraints

1. Reduce columns to meet the limit
2. Split data into multiple tables or migrations
3. Convert some primary tags to secondary tags
4. Shorten column names if too long

### Example Time-Series Table Design

```sql
CREATE TABLE sensor_data
(
    ts TIMESTAMPTZ NOT NULL,
    value DOUBLE
)
TAGS
(
    device_id INT NOT NULL,
    metric VARCHAR(32) NOT NULL,
    quality INT
)
PRIMARY TAGS (device_id, metric);
```

**Note**: For complete DDL syntax and KDTS auto-mapping details, see `references/ddl-syntax.md`

### Auto-Mapping for Time Series Sources

| Source Type | PRIMARY TAG Source  | Additional Tags | VALUE FIELD Source |
|-------------|---------------------|-----------------|--------------------|
| InfluxDB    | First 4 tags        | Tags 5+         | All fields         |
| TDengine    | First 4 TAG columns | TAG columns 5+  | Regular columns    |
| OpenTSDB    | First 4 tags        | Tags 5+         | Metric value       |

**Note**: For InfluxDB/TDengine with > 4 tags, KDTS auto-assigns first 4 as PRIMARY TAGS, rest as regular tags

---

## 9. Performance Tips

### Large Data Sets

```json
{
  "data": {
    "batchSize": 5000,
    "core": {
      "transport": {
        "channel": {
          "speed": {
            "byte": 10485760,
            "record": 10000
          }
        }
      }
    },
    "enable": true,
    "fetchSize": 5000,
    "setting": {
      "errorLimit": {
        "percentage": 0.01
      },
      "speed": {
        "channel": 4
      }
    }
  }
}
```

### Time Series Optimization

```json
{
  "tables": [
    {
      "source": {
        "sourceType": "TDENGINE",
        "table": "sensor_data",
        "column": "*",
        "beginDateTime": "2024-01-01",
        "endDateTime": "2024-06-30"
      },
      "target": {
        "sourceType": "KAIWUDB",
        "table": "sensor_data_2024h1",
        "column": "*",
        "writeMode": "insert"
      }
    }
  ]
}
```

### Error Tolerant Migration

```json
{
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
        "percentage": 5.0
      },
      "speed": {
        "channel": 1
      }
    }
  }
}
```

## 10. File/NoSQL Source Table Mapping Templates

Table mappings for file-based and NoSQL sources. These CANNOT use `build_table_mapping()` — build them manually.

### 10.1 FTP/SFTP Source Mapping

**Requirements**:
- `path` MUST be an absolute path starting with `/`; it is the SFTP 
   SERVER-side path (resolvable where the SFTP service runs).
- `skipHeader: true` when the CSV has a header row
- `column` is a JSON array string with index/type/format per field

```json
{
  "source": {
    "sourceType": "FTP",
    "protocol": "sftp",
    "timeout": 60000,
    "path": "[\"/data/files/test_tb.csv\"]",
    "fieldDelimiter": ",",
    "compress": null,
    "encoding": "UTF-8",
    "nullFormat": null,
    "connectPattern": null,
    "column": "[{\"index\":0,\"type\":\"date\",\"format\":\"yyyy-MM-dd HH:mm:ss.SSS\"},{\"index\":1,\"type\":\"long\"},{\"index\":2,\"type\":\"double\"},{\"index\":3,\"type\":\"string\"}]",
    "skipHeader": true,
    "maxTraversalLevel": null,
    "csvReaderConfig": "{\"useTextQualifier\":false,\"safetySwitch\":true,\"skipEmptyRecords\":true}"
  },
  "target": {
    "sourceType": "KAIWUDB",
    "table": "test_tb",
    "column": "ts,c1,c2,c3",
    "writeMode": "insert"
  }
}
```

### 10.2 HDFS Source Mapping

**Requirements**:
- `path` is the HDFS SERVER-side path (JSON array string, absolute) — NOT local
- `fileType` REQUIRED: `text` / `orc` / `parquet` / `rcfile`
- `column` is a JSON array string with index/type/format per field
- `compress` (e.g. `gzip`) for text files; Kerberos fields for secured clusters
- DataSource: host = NameNode host, port = 9000 (RPC)
- Target tables must pre-exist

```json
{
  "source": {
    "sourceType": "HDFS",
    "path": "[\"/user/hive/warehouse/hdfs_test.db/test_tb\"]",
    "fileType": "text",
    "column": "[{\"index\":0,\"type\":\"date\",\"format\":\"yyyy-MM-dd HH:mm:ss.SSS\"},{\"index\":1,\"type\":\"long\"},{\"index\":2,\"type\":\"double\"},{\"index\":3,\"type\":\"string\"}]",
    "fieldDelimiter": ","
  },
  "target": {
    "sourceType": "KAIWUDB",
    "table": "test_tb",
    "column": "ts,c1,c2,c3",
    "writeMode": "insert"
  }
}
```

### 10.3 MongoDB Source Mapping

**Requirements**:
- `column` is a JSON array string WITH types (NOT a comma string):
  name/type pairs — types: `date` / `int` / `long` / `double` / `bool` / `string` / `bytes`
- `query` (optional filter): MongoDB JSON query syntax as a string, e.g.
  `{"t1":{"$gte":1,"$lt":8}}` — filters documents before migration
- **Table creation LIMITED to two options** (KDTS does NOT support MongoDB→KaiwuDB
  type mapping — its generic fallback emits invalid types like LONG/STRING):
  1. User pre-creates the target table (skip DDL);
  2. SKILL generates DDL from user-provided table info with the mapping
     int→INT4 / long→INT8 / double→FLOAT8 / string→VARCHAR / bytes→VARBYTES /
     date→TIMESTAMP / bool→BOOL, user confirms, then execute_ddl.
     DDL failure → inform the user the table was NOT created, END migration

```json
{
  "source": {
    "sourceType": "MONGODB",
    "collectionName": "test_tb",
    "column": "[{\"name\":\"ts\",\"type\":\"date\"},{\"name\":\"c1\",\"type\":\"int\"},{\"name\":\"c2\",\"type\":\"long\"},{\"name\":\"c3\",\"type\":\"double\"}]",
    "query": "{\"t1\":{\"$gte\":1,\"$lt\":8}}"
  },
  "target": {
    "sourceType": "KAIWUDB",
    "table": "test_tb",
    "column": "ts,c1,c2,c3",
    "writeMode": "insert"
  }
}
```

### 10.4 Oracle Source Mapping (with expression column)

Oracle requirements: dbName = owner (UPPERCASE), names are UPPERCASE, expression
columns need separated target columns:

```python
mapping = build_table_mapping(
    source_type="ORACLE",
    source_table="TEST_TB",
    target_table="TEST_TB",
    columns="TS,C1,C2,C3,C4,C5,C6,C7,C8,C9,C10,C11,C12,1 as t1",
    target_columns="TS,C1,C2,C3,C4,C5,C6,C7,C8,C9,C10,C11,C12,t1",
    write_mode="insert",
)
```

```json
{
  "source": {
    "sourceType": "RDBMS",
    "table": "TEST_TB",
    "column": "TS,C1,C2,C3,C4,C5,C6,C7,C8,C9,C10,C11,C12,1 as t1"
  },
  "target": {
    "sourceType": "KAIWUDB",
    "table": "TEST_TB",
    "column": "TS,C1,C2,C3,C4,C5,C6,C7,C8,C9,C10,C11,C12,t1",
    "writeMode": "insert"
  }
}
```

New-column type mapping for Oracle (must have exact mappings):
`NUMBER(5,0)→INT2`, `NUMBER(10,0)→INT4`, `NUMBER(19,0)→INT8`;
unmapped values (e.g. `NUMBER(1,0)`) fall back to `NUMBER` → FLOAT (float type).

### 10.5 Added-Column Type Derivation (ALL source types)

Type derived from the DEFAULT VALUE via `build_added_column()` (RDBMS, TDengine,
InfluxDB, KaiwuDB):

| Default value    | KaiwuDB type                 | Primary tag?               | SQL expression in source columns |
|------------------|------------------------------|----------------------------|----------------------------------|
| int (e.g. 1)     | `INT4` (`INT8` for InfluxDB) | Yes                        | `1 as t1`                        |
| str (e.g. 'x')   | `VARCHAR`                    | Yes                        | `'x' as t1`                      |
| bool             | `BOOL`                       | Yes                        | `true as t1`                     |
| float (e.g. 1.5) | `FLOAT4/FLOAT8`              | **No — ordinary tag only** | `1.5 as t1`                      |

sourceColumnType per source (exact KDTS mappings):

| Source type                                 | int sourceColumnType | maps to |
|---------------------------------------------|----------------------|---------|
| MYSQL / SQLSERVER / TDENGINE2X / TDENGINE3X | `INT`                | INT4    |
| ORACLE                                      | `NUMBER(10,0)`       | INT4    |
| POSTGRESQL                                  | `INTEGER`            | INT4    |
| CLICKHOUSE                                  | `INT32`              | INT4    |
| INFLUXDB1X / INFLUXDB2X                     | `INTEGER`            | INT8    |
| KAIWUDB                                     | `INT4`               | INT4    |

```python
from scripts import build_added_column, build_table_mapping

table["columns"].append(build_added_column("t1", 1, source_type="MYSQL", is_tag=True, is_primary_tag=True))

mapping = build_table_mapping(
    source_type="MYSQL", source_table="test_tb", target_table="test_tb",
    columns="ts,c1,...,12,1 as t1",
    target_columns="ts,c1,...,12,t1",
)
```

### 10.6 OpenTSDB / KaiwuDB-Source Mapping

**OpenTSDB source**:
- `column` = FULL METRIC names in `table.metric` format (e.g. `test_tb.c1,test_tb.c2,...`)
- time range REQUIRED: `beginDateTime` / `endDateTime`

```json
{
  "source": {
    "sourceType": "OPENTSDB",
    "table": "test_tb",
    "column": "test_tb.c1,test_tb.c2,test_tb.c3,test_tb.c4,test_tb.c5,test_tb.c6",
    "beginDateTime": "2024-04-09 16:00:00",
    "endDateTime": "2024-04-09 18:00:00"
  },
  "target": {
    "sourceType": "KAIWUDB",
    "table": "test_tb",
    "column": "ts,c1,c2,c3,c4,c5,c6",
    "writeMode": "insert"
  }
}
```

**KaiwuDB source** (KaiwuDB→KaiwuDB):
- time range REQUIRED: `beginDateTime` / `endDateTime`
- `tsColumn`: the time column name (e.g. `ts`)

```json
{
  "source": {
    "sourceType": "KAIWUDB",
    "table": "test_tb",
    "column": "ts,c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,c12,t1",
    "beginDateTime": "2025-04-01 00:00:00",
    "endDateTime": "2025-06-01 00:00:00",
    "tsColumn": "ts"
  },
  "target": {
    "sourceType": "KAIWUDB",
    "table": "test_tb",
    "column": "ts,c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,c12,t1",
    "writeMode": "insert"
  }
}
```
