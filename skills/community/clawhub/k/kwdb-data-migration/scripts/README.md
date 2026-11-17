# KWDB Data Migration Scripts

Complete Python implementation for KaiwuDB heterogeneous database migration via KDTS REST API.

## Architecture Overview

```
scripts/
├── __init__.py          # Package init
├── api_client.py        # Unified KDTS API client (10 endpoints + mapping helpers)
├── data_source.py       # Data source management (14 types)
├── migration_task.py    # Migration workflow orchestration
├── config_validator.py  # Configuration validation
├── error_handler.py     # Error code handling (18 error codes)
├── config.py            # Multi-layer configuration (env > param > file > default)
└── README.md            # This file
```

## Module Details

### 1. api_client.py - Unified KDTS API Client

Full implementation of all 10 KDTS REST API endpoints.

**Classes:**

- `KDTSClient`: Main API client with methods for all endpoints
- `build_source_config()`: Helper to create source configurations
- `build_table_mapping()`: Helper to create table mappings (uses the correct source
  identifier field per type: `table`/`measurement`/`collectionName`; FTP/HDFS rejected).
  Supports `where` (source filter), `pre_sql`/`post_sql` (target SQL) and
  `target_columns` — REQUIRED when source `columns` contain SQL expressions
  (e.g. source `"...,1 as t1"` → target `"...,t1"`), otherwise DataX cannot find the target column
- `build_influxdb_mapping()`: Helper for InfluxDB measurement mappings — source column
  names use `sourceColumnName` (`_time` for the time column, NOT `ts`), and the data
  time range (begin/end datetime) is REQUIRED (no defaults; too-wide range causes
  reader memory overflow)
- `build_added_column()`: Helper to build a NEW column definition for sources lacking
  it (ALL source types: RDBMS/TDengine/InfluxDB/KaiwuDB) — type derived from the
  default value (int→INT4 or INT8 for InfluxDB, str→VARCHAR, bool→BOOL eligible for
  PRIMARY TAG; float→FLOAT4/FLOAT8 ordinary TAG ONLY, never a primary tag);
  sourceColumnType picked per source for an exact KDTS mapping
- `build_manual_metadata()`: Helper to build a Database object for sources WITHOUT
  KDTS metadata support. The table structure MUST come from the USER (CREATE TABLE DDL or column list) — never guess
- `mark_time_series_columns()`: Helper to mark column roles (isTs/isTag/isPrimaryTag,
  auto-sets primary tags to NOT NULL) on a source Database for time-series DDL generation

**Supported Endpoints:**

| Method | Path                    | Purpose                |
|--------|-------------------------|------------------------|
| GET    | `/health`               | Health check           |
| POST   | `/datasource/validate`  | Test connection        |
| POST   | `/datasource/databases` | List databases         |
| POST   | `/datasource/metadata`  | Read metadata          |
| POST   | `/metadata/preview`     | Preview DDL            |
| POST   | `/metadata/execute`     | Execute DDL            |
| POST   | `/datax/build`          | Build migration script |
| POST   | `/datax/execute`        | Execute migration      |
| GET    | `/datax/status`         | Query task status      |
| POST   | `/datax/control`        | Kill/control task      |

**Key Features:**

- Automatic error handling with standardized response format
- **Connection normalization**: KDTS returns code=0 even for FAILED validation (failure 
  text in `data`) — `test_connection()` normalizes such responses to code=2001, so `code == 0` always means success
- **`DEFAULT_DATAX_CONFIG`**: `build_migration()` uses a complete DataX config
  (core + setting REQUIRED for successful migration; missing them causes failures)
- Connection and read timeout management (default read timeout 300s via KDTS_TIMEOUT)
- HTTP 503 detection (returns code 5001 with Retry-After hint; no automatic retry)
- Request/response logging

### 2. data_source.py - Complete Data Source Management

Comprehensive data source configuration for all 14 KDTS supported types.

**Classes:**

- `Engine`: Enum for KaiwuDB target engine types (RELATIONAL, TIMESERIES)
- `SourceType`: Enum for all 14 source types
- `SourceCapability`: Enum for capability levels
- `DataSourceManager`: Main manager class

**Supported Source Types:**

| Type       | Engine     | Default Port | Capability                         |
|------------|------------|--------------|------------------------------------|
| MYSQL      | RELATIONAL | 3306         | Full Migration                     |
| ORACLE     | RELATIONAL | 1521         | Full Migration                     |
| POSTGRESQL | RELATIONAL | 5432         | Full Migration                     |
| SQLSERVER  | RELATIONAL | 1433         | Metadata + Data, No Full Migration |
| CLICKHOUSE | RELATIONAL | 9000         | Full Migration (No Metadata)       |
| KAIWUDB    | *REQUIRED* | 26257        | Data Migration Only                |
| TDENGINE3X | TIMESERIES | 6030         | Full Migration                     |
| TDENGINE2X | TIMESERIES | 6030         | Data Migration Only                |
| INFLUXDB1X | TIMESERIES | 8086         | Metadata + Data, No Full Migration |
| INFLUXDB2X | TIMESERIES | 8086         | Metadata + Data, No Full Migration |
| OPENTSDB   | TIMESERIES | 4242         | Data Migration Only                |
| MONGODB    | TIMESERIES | 27017        | Data Migration Only                |
| FTP        | TIMESERIES | 21           | Data Migration Only                |
| HDFS       | TIMESERIES | 8020         | Data Migration Only                |

**Note:** 

- Engine must be explicitly specified for KAIWUDB (RELATIONAL or TIMESERIES)
- Engine is required for all source configurations per KDTS API

**Key Features:**

- Auto-detect engine type from source type
- JDBC URL construction for relational databases
- Source-specific configuration builders (FTP, HDFS, MongoDB)
- Connection test integration with api_client
- Configuration template generation

### 3. migration_task.py - Migration Workflow Orchestration

End-to-end migration workflow management by composing KDTS API calls.

**Classes:**

- `MigrationWorkflow`: Enum for workflow types
- `MigrationStep`: Enum for workflow steps
- `MigrationStatus`: Enum for task statuses (SUBMITTED, RUNNING, SUCCEEDED, FAILED, KILLED)
- `MigrationWorkflowManager`: Main workflow manager

**Supported Workflows:**

1. `FULL_MIGRATION`: Schema + Data (full migration)
2. `SCHEMA_ONLY`: DDL only (no data)
3. `DATA_ONLY`: Data only (tables must exist)
4. `TABLE_LEVEL`: Specific tables (for restricted sources)

**Key Features:**

- Complete workflow orchestration (test → metadata → DDL → build → execute → monitor)
- Step-by-step result tracking
- Progress monitoring with polling
- Batch migration support for large datasets
- Safe task termination with confirmation

**Batch Script Execution (`execute_migration_batches`):**

- When `build_migration()` returns MANY scripts (one per table), submitting them all in
  one `execute_migration()` call exceeds the HTTP read timeout.
- Use `workflow.execute_migration_batches(script_names, batch_size=10)` to submit
  10 scripts per batch, wait for the batch to reach final states, then submit the next.
- A 4003 on submission means the request reached the server (it keeps processing) —
  the batch is still monitored to completion.

**Important:** KDTS API only supports KILL and QUERY actions. No pause/resume.

### 4. config_validator.py - Configuration Validation

Validates all migration parameters before API calls.

**Classes:**

- `ConfigValidator`: Static validation methods

**Validations:**

- Source type against 14 supported types
- Source capability against requested operation
- Required field presence
- Target must be KAIWUDB
- Table mapping structure

### 5. error_handler.py - Error Code Handling

Maps all KDTS error codes to human-readable messages and fix suggestions.

**Classes:**

- `ErrorHandler`: Error lookup and formatting

**Error Categories:**

| Category   | Code Range | Examples                                         |
|------------|------------|--------------------------------------------------|
| Parameter  | 1xxx       | 1001 (invalid params), 1002 (unsupported type)   |
| Connection | 2xxx       | 2001 (connection failed)                         |
| Metadata   | 3xxx       | 3001 (metadata error), 3004 (tag limit)          |
| DataX      | 4xxx       | 4001 (build failed), 4002 (launch failed)        |
| Resource   | 5xxx       | 5001 (thread pool full), 5002 (Python not found) |
| System     | 9xxx       | 9999 (internal error)                            |

## Usage Examples

### Quick Start - Full Migration

```python
from scripts.api_client import KDTSClient
from scripts.data_source import DataSourceManager
from scripts.migration_task import MigrationWorkflowManager

client = KDTSClient(base_url="http://localhost:8989")
ds_manager = DataSourceManager(api_client=client)
workflow = MigrationWorkflowManager(api_client=client)

source_config = ds_manager.build_relational_config(
    source_type="MYSQL",
    host="192.168.1.100",
    username="root",
    password="secret",
    db_name="source_db",
)

target_config = ds_manager.build_target_config(
    engine="RELATIONAL",
    host="127.0.0.1",
    username="root",
    password="kwdb_secret",
    db_name="target_db",
)

result = workflow.run_full_migration(
    source_config=source_config,
    target_config=target_config,
)

print(f"Migration {'succeeded' if result['success'] else 'failed'}")
```

### Manual API Calls

```python
from scripts.api_client import KDTSClient, build_source_config

client = KDTSClient(base_url="http://localhost:8989")

source = build_source_config(
    source_type="MYSQL",
    host="127.0.0.1",
    port=3306,
    username="root",
    password="123456",
    db_name="test_db",
    engine="RELATIONAL"
)
result = client.test_connection(source)
print(f"Connection: {result}")

metadata = client.read_metadata(source)
print(f"Tables found: {len(metadata.get('data', {}).get('tableMap', {}))}")
```

### Error Handling

```python
from scripts.error_handler import ErrorHandler

response = client.build_migration(source, target)
if response.get("code") != 0:
    hint = ErrorHandler.get_error_hint(response["code"])
    print(f"Error: {response['message']}")
    print(f"Hint: {hint}")
```

### Batch Migration

```python
batches = [
    [{"source": {...}, "target": {...}} for table in batch1],
    [{"source": {...}, "target": {...}} for table in batch2],
]

result = workflow.run_batch_migration(
    source_config=source_config,
    target_config=target_config,
    table_batches=batches,
)

print(f"Completed: {result['completed_batches']}/{result['total_batches']}")
```

### Batch Script Execution

```python
result = workflow.execute_migration_batches(
    script_names=script_names,
    batch_size=10,
)
```

### Time-Series Mapping Helpers

```python
from scripts.api_client import (mark_time_series_columns, build_added_column,
                                build_influxdb_mapping, build_manual_metadata)

mark_time_series_columns(source_db, "orders", time_column="order_time",
                         primary_tags=["customer_id"], tags=["status"])

table["columns"].append(
    build_added_column("t1", 1, source_type="ORACLE", is_tag=True, is_primary_tag=True))

mapping = build_influxdb_mapping(
    source_db, "test_tb",
    begin_datetime="2025-10-22 00:00:00",
    end_datetime="2025-10-26 00:00:00",
)

db = build_manual_metadata("CLICKHOUSE", "clickhouse_kwdb", "test_tb", user_columns)
```

## Requirements

- Python 3.8+
- requests library (`pip install requests`)
- KDTS Server running and accessible

### Other Dependencies

All other modules use Python standard library only:
- typing, enum, json, os, re, time, sys, logging, pathlib

## Dependencies Between Modules

```
api_client.py ──────────────────────────┐
    │                                    │
    ▼                                    ▼
data_source.py ──► migration_task.py ──► config_validator.py
                                        │
                                        ▼
                                    error_handler.py
```

## Response Format

All API responses follow:

```json
{
  "code": 0,
  "message": "success",
  "timestamp": 1719290000000,
  "data": {}
}
```

## Important Notes

1. KDTS Server is the backend; these scripts are the client library
2. All operations are stateless per call; manage state at the workflow level
3. Migration can be time-consuming; use `wait_for_completion()` for long-running tasks
4. Always test connections before migration
5. For large migrations (>1M rows), use batch migration or parallel channels
6. KDTS API only supports KILL operation; NO pause/resume
7. MetaData fields: `primaryKey`, `constraint`, `comment`, `index`, `view` (NOT includePK, etc.)
8. DDL uses Database object for `sourceDb` parameter (NOT string)
9. **TIMESERIES targets MUST use explicit table mappings** (`tables` required, never
   empty — KDTS rejects whole-database migration into the time-series engine)
10. **InfluxDB mappings REQUIRE a data time range** (begin/end datetime, no defaults;
    too-wide ranges cause reader memory overflow)
11. **MongoDB table creation is limited**: KDTS does NOT support MongoDB type mapping —
    either pre-create the target table, or let the SKILL generate the DDL from
    user-provided table info (int→INT4, long→INT8, double→FLOAT8, string→VARCHAR,
    bytes→VARBYTES, date→TIMESTAMP, bool→BOOL)

## References

- KDTS API: `references/api-reference.md`
- DDL Syntax: `references/ddl-syntax.md`
- Source Types: `references/source-types.md`
- Error Codes: `references/error-codes.md`
- Type Mapping: `references/type-mapping.md`
- Config Templates: `references/config-templates.md`

## Testing

Test utilities are located in `internal/tests/kwdb-data-migration/scripts/`:

- `mock_server.py`: Mock KDTS server for local testing
- `test_migration_flow.py`: End-to-end migration flow test
- `agent_dialogue_simulator.py`: AI Agent dialogue simulation

Refer to the internal test directory for usage instructions.