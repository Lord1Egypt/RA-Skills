# KDTS Migration Skill User Input Examples

This document shows natural language user requests and how the Skill processes them.

## Language Versions

- **English Version**: This file (`prompt-examples.md`)
- **Chinese Version**: [prompt-examples.zh.md](./prompt-examples.zh.md)

**ALWAYS respond in the same language the user uses.** Both versions contain real user input examples that the AI Agent should handle appropriately.

---

## 1. Complete Migration Request

### User Input 1 (English)

> I want to migrate the users table from MySQL to KaiwuDB. The source is "test_db" on 192.168.1.100:3306, username root with password 123456. The target KaiwuDB is on localhost at port 9092.

### Processing Flow

1. **Intent Recognition**: Complete migration (schema + data)
2. **Missing Parameter Collection**:
   - Target KaiwuDB username/password → Ask
   - Target database name → Ask or suggest same name
   - Migration mode → Full database or specific tables
3. **After Parameter Confirmation**:
   - Test source/target connections
   - List source database tables
   - Preview DDL
   - Execute DDL
   - Build migration script
   - Execute migration and monitor progress

---

### User Input 2 (English)

> Need to migrate Oracle 19c ERP system to KaiwuDB, including structure and data. Oracle is at 10.0.0.5, port 1521, service name ORCL, username erp_user.

### Processing Flow

1. **Intent Recognition**: Complete migration, Oracle source
2. **Missing Parameter Collection**:
   - Oracle password → Ask
   - Source database/Schema → Can be obtained from connection or ask
   - Target KaiwuDB connection details → Collect fully
3. **Capability Check**: Oracle supports complete migration → Can proceed
4. **Performance Suggestion**: Oracle large tables recommended to enable splitPk parallelism

---

## 2. Schema-Only Migration

### User Input (English)

> Help me sync PostgreSQL table structure to KaiwuDB. I only need to create tables; I'll import data later myself. PostgreSQL is at pg.example.com:5432, database analytics.

### Processing Flow

1. **Intent Recognition**: DDL-only migration (schema-only)
2. **Execution Flow**:
   - Test source/target connections
   - Read source metadata
   - Preview DDL
   - Display generated DDL for user confirmation
   - Execute DDL
   - Done (skip data migration)

---

## 3. Data-Only Migration

### User Input (English)

> Target table is already created. I just need to import data from SQL Server 2019 orders table. SQL Server is at 192.168.1.50, database sales, target is kaiwudb_target.

### Processing Flow

1. **Intent Recognition**: Data-only migration
2. **Capability Check**: SQL Server does NOT support complete migration → Need explicit table mapping
3. **Execution Flow**:
   - Test connections
   - Ask target table name (default: same name "orders")
   - Build migration script (with tables field)
   - Execute migration
   - Monitor progress

---

## 4. Multi-Source Migration

### User Input (English)

> We have three databases to migrate: MySQL users DB, Oracle orders DB, PostgreSQL logs DB, all to the same KaiwuDB cluster.

### Processing Flow

1. **Intent Recognition**: Batch multi-source migration
2. **Interaction Flow**:
   - Confirm target cluster info (once only)
   - Collect connection details for each source one by one
   - Recommend sequential execution (to avoid concurrency conflicts)
3. **Generate Migration Plan**:
   ```
   1. MySQL users -> KWDB users_db
   2. Oracle orders -> KWDB orders_db
   3. PostgreSQL logs -> KWDB logs_db
   ```
4. **Execute Sequentially**: Complete each source before the next

---

## 5. Time Series Migration

### User Input (English)

> Need to migrate sensor data from TDengine 3.x to KaiwuDB time series DB. TDengine is at 172.16.0.10:6030, database sensor_monitor, target is kwdb_iot, time range is full year 2024.

### Processing Flow

1. **Intent Recognition**: Time series migration
2. **Capability Check**: TDengine 3.x supports complete time series migration
3. **Special Handling**:
   - Need to set time range (beginDateTime, endDateTime)
   - Confirm target engine is TIMESERIES
   - Handle TDengine super table/sub table structure
4. **Execution Flow**:
   - Connection test
   - Read TDengine metadata
   - Preview time series DDL
   - Convert to KaiwuDB time series table structure
   - Execute migration

---

## 6. InfluxDB Migration (Two-Step Method)

### User Input (English)

> I need to migrate InfluxDB 2.x metrics bucket to KaiwuDB time series DB. InfluxDB is at influx.local:8086, org is myorg, token is xxxxxxx, bucket is metrics.

### Processing Flow

1. **Intent Recognition**: InfluxDB 2.x -> KaiwuDB (TIMESERIES)
2. **Capability Note**: InfluxDB supports metadata + data (META_AND_DATA), but NOT full migration
3. **Two-Step Reminder**:
   - Step 1: Migrate Schema (DDL)
   - Step 2: Migrate Data
4. **Interaction Flow**:
   - Confirm two-step method
   - Collect InfluxDB 2.x specific parameters: org, token, bucket
   - List measurements
   - Preview DDL for each measurement
   - Execute Schema migration
   - Execute Data migration
   - Verify results

**Note**: InfluxDB 1.x and 2.x both use HTTP protocol, not JDBC.

---

## 7. MongoDB Migration

### User Input (English)

> Need to migrate MongoDB logs collection, DB is app_logs, collection is error_logs. Only migrate records where status = 'error'.

### Processing Flow

1. **Intent Recognition**: MongoDB -> KWDB
2. **Capability Check**: MongoDB does NOT support metadata or complete migration
3. **Interaction Flow**:
   - Explain need for manual field mapping
   - Ask about target table structure (skip if exists)
   - Set MongoDB query filter: `{"status": "error"}`
4. **Execution Flow**:
   - Connection test
   - Confirm target table exists
   - Build migration script with query
   - Execute migration

---

## 8. Migration Status Query

### User Input (English)

> How's that MySQL migration task I started earlier? Is it done yet?

### Processing Flow

1. **Intent Recognition**: Task status query
2. **Information Collection**:
   - If user provided task ID/script name -> Query directly
   - If not -> Ask for task identifier or recent tasks
3. **Return Information**:
   - Current status: SUBMITTED / RUNNING / SUCCEEDED / FAILED
   - Progress percentage (if RUNNING)
   - Start time, elapsed time
   - Completion statistics (if SUCCEEDED)

---

## 9. Migration Troubleshooting

### User Input 1 (English)

> Migration failed with error code 3004, saying tag limit exceeded. How to fix this?

### Processing Flow

1. **Intent Recognition**: Error troubleshooting
2. **Error Analysis**:
   - Error code 3004 = METADATA_TAG_LIMIT_EXCEEDED
   - Meaning: KaiwuDB time series table tags exceed 128 or primary tags exceed 4
3. **Provide Solutions**:
   - Check source table tag count
   - Recommend keeping essential tags, converting others to value columns
   - Or split into multiple target tables
   - Give specific modification examples

---

### User Input 2 (English)

> Connection test keeps failing, source database is MySQL at remote.server.com.

### Processing Flow

1. **Intent Recognition**: Connection issue troubleshooting
2. **Diagnostic Steps**:
   - Ask for specific error code/message
   - Check host resolution (DNS)
   - Check port reachability
   - Check account permissions
   - Check KDTS server network configuration
3. **Provide Diagnostic Commands**:
   ```bash
   nslookup remote.server.com
   telnet remote.server.com 3306
   mysql -h remote.server.com -u test -p
   ```

---

## 10. Migration Config Save/Load

### User Input (English)

> Save the migration config we just used; I'll need it again later. Also, I want to load this config next time without re-entering everything.

### Processing Flow

1. **Intent Recognition**: Config management
2. **Handling**:
   - Export current migration config as JSON file
   - Suggest save path (or let user specify)
   - Explain how to load next time
3. **Config Example**:
   ```json
   {
     "source": {
       "engine": "RELATIONAL",
       "type": "MYSQL",
       "host": "source-host",
       "port": 3306,
       "username": "user",
       "password": "pass",
       "dbName": "source_db"
     },
     "target": {
       "engine": "TIMESERIES",
       "type": "KAIWUDB",
       "host": "target-host",
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

---

## 11. Dangerous Operation Intercept

### User Input (English)

> Kill that running migration task.

### Processing Flow

1. **Intent Recognition**: Task termination (dangerous operation)
2. **Safety Check**:
   - [WARNING]: Terminating running migration may cause data inconsistency
   - Show current task status and progress
   - **Require user confirmation**: "Please type YES to confirm termination"
3. **After Confirmation**:
   - Call /datax/control (action=KILL)
   - Report termination result
   - Suggest data recovery steps

---

## Interaction Design Principles

### Parameter Collection Order

1. KDTS server address (default: localhost:8989)
2. Operation type (migrate/query/troubleshoot)
3. Source config (type, connection, database)
4. Target config (connection, database, engine)
5. Migration scope (full database/specific tables)
6. Migration mode (schema/data/all)

### Missing Parameter Handling

- **Required parameter missing**: Ask directly, list all missing items
- **Optional parameter missing**: Use default value and inform user
- **Ambiguous parameter**: Provide options for user to choose

### Error Feedback

- **Before operation**: Clearly state what will happen and impact
- **During operation**: Real-time progress feedback
- **After operation**: Result summary + next step suggestions

### Safety Protection

- **High-risk operation**: Require double confirmation + impact explanation
- **Data loss risk**: Remind backup
- **Network-sensitive operation**: Test connection first before execution

---

## Skill Trigger Keywords

The following keywords trigger the migration Skill:

### Core Verbs
- migrate, sync, import, export, transfer

### Database Types
- MySQL, Oracle, PostgreSQL, SQL Server, SQLServer
- TDengine, InfluxDB, OpenTSDB
- MongoDB, KaiwuDB, KWDB
- time series, relational, document

### Function Operations
- create table, DDL, schema migration
- data migration, full, incremental
- connection test, connectivity
- migration task, progress, status
- error, failed, error code

### Scenario Descriptions
- heterogeneous, cross-database, different databases
- cloud migration, relocation, upgrade

---

**Document Version:** v1.0.0  
**Last Updated:** 2026-08-03  
**Applicable Skill Version:** kwdb-data-migration v1.0.0
