---
name: kwdb-data-migration
description: |
  Automated heterogeneous database migration skill for KaiwuDB / KWDB via KDTS REST API.
  Use this skill whenever the user mentions:
  - heterogeneous migration, cross-database migration, or data migration to KaiwuDB / KWDB
  - KDTS, migration tool, or data transfer between different databases
  - Specific source databases: MySQL, Oracle, PostgreSQL, SQL Server, ClickHouse, TDengine, InfluxDB, OpenTSDB, MongoDB, FTP, HDFS
  - Migration operations: create migration task, configure data source, test connection, import data, sync schema, batch migration
  - Migration management: query task status, view migration progress, check logs, kill migration, export/import config
  - Data type mapping, table structure sync, DDL generation, schema validation
  Even if the user does not explicitly say "migration", trigger this skill when they ask to transfer or sync data between databases with different engines.
version: 1.0.0
---

# KWDB Data Migration Skill

## IMPORTANT: How to Use This Skill

**This is an AI Agent Skill**, NOT a library for manual coding. Here's how it works:

### Language Support

**ALWAYS respond in the same language the user uses.** This skill fully supports both Chinese and English users:
- If user writes in Chinese, respond in Chinese
- If user writes in English, respond in English
- When displaying technical terms (e.g., JDBC, DDL, TIMESERIES, RELATIONAL), keep them in their original form
- Example Chinese responses are available in `user-interaction-scenarios.zh.md`

### Correct Usage Pattern (Natural Language)

````
User: Help me migrate MySQL database to KaiwuDB

AI Agent:
1. Reads this SKILL.md to understand the migration workflow
2. Guides user step-by-step to collect necessary parameters:
   - KDTS server address (default: http://127.0.0.1:8989)
   - MySQL connection info (host, port, user, password, database)
   - KaiwuDB connection info (host, port, user, password, database, engine type)
   - Migration mode (full/schema-only/data-only)
3. Calls the Python scripts in `scripts/` as backend tools
4. Reports progress and results to user in natural language
````

### What AI Agent Does

The AI Agent acts as an **intelligent assistant** that:

- [STEP] Understands user's migration intent from natural language
- [COLLECT] Collects all necessary parameters through guided questions
- [EXECUTE] Executes migration operations by calling KDTS API
- [VALIDATE] Validates parameters and handles errors automatically
- [REPORT] Reports progress and results in user-friendly format
- [CONFIRM] Asks for confirmation at critical steps (DDL execution, task termination)

### What User Needs to Do

User only needs to:

- [DESCRIBE] Describe migration intent in plain language (e.g., "Migrate MySQL to KaiwuDB")
- [PROVIDE] Provide connection information when asked
- [CONFIRM] Confirm critical operations when prompted

### Example Conversation

````
User: Help me migrate MySQL sales database to KaiwuDB time series

AI Agent:
  [INFO] Migration intent recognized: MySQL -> KaiwuDB (TIMESERIES)
  
  Please provide the following information:
  1. KDTS server address (default: http://127.0.0.1:8989)
  2. MySQL connection info:
     - Host:
     - Port (default 3306):
     - Username:
     - Password:
  3. KaiwuDB connection info (engine: TIMESERIES):
     - Host (default 127.0.0.1):
     - Port (default 26257):
     - Username (default root):
     - Password:
  
  [WARNING] Security reminder: Please ensure you have backed up both source and target databases before migration!

User: KDTS at http://192.168.1.100:8989, MySQL: root/password abc at 192.168.1.50:3306, KaiwuDB at 127.0.0.1:26257

AI Agent:
  [OK] Parameters collected, starting migration process...
  
  Step 1: Testing database connections...
  [OK] MySQL connection successful
  [OK] KaiwuDB connection successful
  
  Step 2: Reading MySQL metadata...
  [INFO] Found 5 tables: orders, customers, products, categories, inventory
  
  Step 3: Configuring time-series tags (TIMESERIES target)...
  For table orders, select the time column and PRIMARY TAGS (1-4):
  - Time column: order_time
  - PRIMARY TAGS: customer_id, product_id
  [WARNING] Verify no NULL values in the primary tag columns
  
  Step 4: Previewing DDL (KaiwuDB time series tables)...
  [Shows DDL content with TAGS / PRIMARY TAGS]
  
  [WARNING] About to execute DDL to create tables. Continue? (yes/no)
````

### Python Scripts Purpose

The Python scripts in `scripts/` are **backend tools** for the AI Agent.
They provide low-level functions that the Agent calls during migration.
Users do NOT need to read or write these scripts directly.

### Python Dependencies

The scripts require minimal dependencies:

| Dependency | Purpose                        | Installation           |
|------------|--------------------------------|------------------------|
| `requests` | HTTP client for KDTS API calls | `pip install requests` |

All other modules use Python standard library only (`typing`, `json`, `re`, `logging`, etc.).

---

## Overview

This skill provides **automated heterogeneous database migration** to KaiwuDB / KWDB through KDTS REST API. Unlike the
old version that only provided manual GUI guidance, this skill directly calls the KDTS API to automate the entire
migration workflow.

### Migration Path: KDTS REST API

- Supports 14 source types: MySQL, Oracle, PostgreSQL, SQL Server, ClickHouse, TDengine 2.x/3.x, InfluxDB 1.x/2.x,
  OpenTSDB, MongoDB, FTP, HDFS, KaiwuDB (KaiwuDB as source = data migration only)
- Full automation: connection test, schema migration (DDL), data migration, progress tracking

## KDTS Server Configuration

Before any migration operations, determine the KDTS Server connection.
Configuration uses multi-layer priority (highest to lowest):

### Configuration Methods

**1. Environment Variables (Recommended for CI/CD)**

```bash
# Option A: Full URL
export KDTS_BASE_URL="http://your-kdts-server.com:8989"

# Option B: Separate host and port
export KDTS_HOST="your-kdts-server.com"
export KDTS_PORT="8989"

# Optional additional settings
export KDTS_API_PREFIX="/kdts/api/v1"  # Default
export KDTS_TIMEOUT="300"               # Default seconds
export KDTS_CONNECT_TIMEOUT="5"         # Default seconds
```

**2. Explicit Parameter**

```python
client = KDTSClient(base_url="http://your-kdts-server.com:8989")
```

**3. Configuration File (kdts_config.json)**
Create `kdts_config.json` in your project directory:

```json
{
  "base_url": "http://your-kdts-server.com:8989",
  "api_prefix": "/kdts/api/v1",
  "timeout": 300,
  "connect_timeout": 5
}
```

**4. Default (Fallback)**

```
Default: http://127.0.0.1:8989
API Prefix: /kdts/api/v1
```

### Configuration Detection

Use `get_environment_info()` to check current configuration:

```python
from scripts import get_environment_info
info = get_environment_info()
print(f"Config source: {info['config_source']}")
print(f"Current config: {info['current_config']}")
```

### Mandatory Step

Ask the user for KDTS server address if:

- No environment variables are set
- No config file exists
- Default is not appropriate for their environment

Example prompt:
> "What is your KDTS server address? (Default: http://127.0.0.1:8989)"

---

## Script Reference

All migration operations use Python scripts in `scripts/`. Read `scripts/README.md` for API details.

### Initialization

```python
from scripts import (
    KDTSClient, DataSourceManager, MigrationWorkflowManager,
    get_environment_info
)

# Check current configuration
print(get_environment_info())

# Initialize client (uses multi-layer config: env > param > file > default)
client = KDTSClient()  # Reads from env or defaults to http://127.0.0.1:8989

# Or specify explicitly
client = KDTSClient(base_url="http://your-kdts-server:8989")

# Initialize managers
ds_manager = DataSourceManager(api_client=client)
workflow = MigrationWorkflowManager(api_client=client)
```

### Config Methods

| Intent                 | Function                                   | Signature                    |
|------------------------|--------------------------------------------|------------------------------|
| Get config info        | `get_environment_info()`                   | No params, returns Dict      |
| Resolve base URL       | `resolve_base_url()`                       | `(explicit_url: str = None)` |
| Create config template | `KDTSConfig.create_config_file_template()` | `(path: str)`                |

### API Client Methods

| Intent            | Method                           | Signature                                                                                     |
|-------------------|----------------------------------|-----------------------------------------------------------------------------------------------|
| Test connection   | `KDTSClient.test_connection()`   | `(config: Dict, is_target: bool = False)`                                                     |
| List databases    | `KDTSClient.list_databases()`    | `(config: Dict, is_target: bool = False)`                                                     |
| Read metadata     | `KDTSClient.read_metadata()`     | `(source_config: Dict, metadata_options: Dict = None)`                                        |
| Preview DDL       | `KDTSClient.preview_ddl()`       | `(target_config: Dict, source_db: Dict, metadata: Dict = None, is_time_series: bool = False)` |
| Execute DDL       | `KDTSClient.execute_ddl()`       | `(target_config: Dict, ddl_script: Dict, auto_ddl: bool = True)`                              |
| Build migration   | `KDTSClient.build_migration()`   | `(source: Dict, target: Dict, tables: List = None, data_config: Dict = None)`                 |
| Execute migration | `KDTSClient.execute_migration()` | `(script_names: List[str])`                                                                   |
| Query status      | `KDTSClient.query_status()`      | `(script_name: str)`                                                                          |
| Kill task         | `KDTSClient.control_task()`      | `(script_name: str, action: str = "KILL")`                                                    |

### Data Source Methods

| Intent                | Method                                    | Signature                                                     |
|-----------------------|-------------------------------------------|---------------------------------------------------------------|
| Build source config   | `DataSourceManager.build_config()`        | `(source_type, host, port, username, password, db_name, ...)` |
| Build target config   | `DataSourceManager.build_target_config()` | `(engine, host, port, username, password, db_name)`           |
| Get source capability | `DataSourceManager.get_capability()`      | `(source_type: str)`                                          |
| Test connection       | `DataSourceManager.test_connection()`     | `(config: Dict)`                                              |

### Workflow Methods

| Intent                 | Method                                                 | Signature                                            |
|------------------------|--------------------------------------------------------|------------------------------------------------------|
| Full migration         | `MigrationWorkflowManager.run_full_migration()`        | `(source_config, target_config, ...)`                |
| Schema-only            | `MigrationWorkflowManager.run_schema_only_migration()` | `(source_config, target_config, ...)`                |
| Data-only              | `MigrationWorkflowManager.run_data_only_migration()`   | `(source_config, target_config, tables, ...)`        |
| Batch migration        | `MigrationWorkflowManager.run_batch_migration()`       | `(source_config, target_config, table_batches, ...)` |
| Batch script execution | `MigrationWorkflowManager.execute_migration_batches()` | `(script_names, batch_size=10, batch_timeout=3600)`  |
| Kill task              | `MigrationWorkflowManager.kill_task()`                 | `(script_name, confirm=False)`                       |

### Utility Methods

| Intent                 | Module                        | Function                                                                                                  |
|------------------------|-------------------------------|-----------------------------------------------------------------------------------------------------------|
| Validate config        | `scripts/config_validator.py` | `ConfigValidator.validate_source_config(config)`                                                          |
| Generate error hint    | `scripts/error_handler.py`    | `ErrorHandler.get_error_hint(code)`                                                                       |
| Build table mapping    | `scripts/api_client.py`       | `build_table_mapping(source_type, source_table, ...)` (auto field: table/measurement/collectionName)      |
| Build InfluxDB mapping | `scripts/api_client.py`       | `build_influxdb_mapping(source_db, measurement, begin_datetime, end_datetime, ...)` (time range REQUIRED) |
| Build manual metadata  | `scripts/api_client.py`       | `build_manual_metadata(source_type, db_name, table_name, columns)`                                        |
| Mark TS columns        | `scripts/api_client.py`       | `mark_time_series_columns(source_db, table_name, time_column, primary_tags, tags)`                        |

---

## Mandatory Rules

### 1. Never Guess Parameters

All migration parameters **must** be collected from the user explicitly:

- KDTS server address (default: http://localhost:8989)
- Source database: engine, type, host, port, username, password, database name
- Target KWDB: engine, host, port, username, password, database name
- Migration scope: full database or specific tables
- Migration mode: schema-only, data-only, or full

### 2. Always Validate Source Type

Before any operation, **must** call `ConfigValidator.validate_source_config()` from `scripts/config_validator.py`:

- Check if source type is in supported list (14 types)
- Check if source type supports the requested operation (metadata, full migration, etc.)
- Refer to `references/source-types.md` for full capability matrix

### 3. Always Test Connection First

Before reading metadata or building migration scripts:

```python
from scripts.api_client import KDTSClient
client = KDTSClient(base_url)

# Test source connection
result = client.test_connection(source_config, is_target=False)
if result['code'] != 0:
    raise Exception("Source connection failed")

# Test target connection  
result = client.test_connection(target_config, is_target=True)
if result['code'] != 0:
    raise Exception("Target connection failed")
```

> **NOTE (KDTS behavior)**: `test_connection()` returns code=0 even for FAILED
> validations — the failure text is in the `data` field.
> The api_client normalizes such responses to code=2001 automatically, so
> `code == 0` always means success. Do NOT bypass this check.

If connection fails, **stop immediately** and show error hint from `error_handler.py`.

### 4. Mandatory Backup Reminder

Before any migration starts:
> **Reminder:** Please ensure you have backed up both source and target databases before proceeding with migration. KDTS
> migration is non-transactional for data operations and cannot be automatically rolled back.

### 5. Never Kill Running Tasks Without Confirmation

**CRITICAL:** Never execute `control_task(action="KILL")` without explicit user confirmation:

1. Show current task status and progress
2. Warn: "Killing a running migration may leave data in inconsistent state"
3. Ask: "Are you absolutely sure you want to kill this task? (type 'YES' to confirm)"
4. Only proceed after explicit confirmation

### 6. Migration Task Naming Convention

When building scripts, inform user of the generated script names:

```
Script naming: <SOURCE>2<TARGET>_<timestamp>.json
Example: MYSQL2KAIWUDB_1719290000000.json
```

### 7. Engine Compatibility Rules (STRICT)

**CRITICAL**: Certain source types are STRICTLY limited to specific target engines. Do NOT attempt to bypass these restrictions.

| Source Category | Source Types                                               | Allowed Target Engines   | Restriction                                             |
|-----------------|------------------------------------------------------------|--------------------------|---------------------------------------------------------|
| **Time Series** | TDengine 2.x/3.x, InfluxDB 1.x/2.x, OpenTSDB               | **ONLY TIMESERIES**      | Time series sources CANNOT migrate to RELATIONAL engine |
| **Relational**  | MySQL, Oracle, PostgreSQL, SQL Server, ClickHouse, KaiwuDB | RELATIONAL or TIMESERIES | Relational sources have flexibility                     |
| **File/NoSQL**  | MongoDB, FTP, HDFS                                         | TIMESERIES               | File-based sources are time series oriented             |

**Violation Handling**: If user requests invalid combination (e.g., TDengine → RELATIONAL):
1. Explain the restriction clearly
2. Suggest alternative: Use native ETL tools or custom scripts for cross-engine migration
3. Show supported alternatives: Migrate TDengine → TIMESERIES, or export data manually then import to RELATIONAL

---

## Supported Data Sources

Refer to `references/source-types.md` for complete capability matrix.

| Category    | Source Type  | Full Migration | Metadata | Notes                              |
|-------------|--------------|----------------|----------|------------------------------------|
| Relational  | MySQL        | Yes            | Yes      |                                    |
| Relational  | Oracle       | Yes            | Yes      |                                    |
| Relational  | PostgreSQL   | Yes            | Yes      |                                    |
| Relational  | SQL Server   | No             | Yes      |                                    |
| Relational  | ClickHouse   | Yes            | No       | Data migration only                |
| Time Series | KaiwuDB      | No             | No       | Data migration only (as source)    |
| Time Series | TDengine 3.x | Yes            | Yes      |                                    |
| Time Series | TDengine 2.x | No             | No       | Data migration only                |
| Time Series | InfluxDB 1.x | No             | Yes      | Metadata + Data, no full migration |
| Time Series | InfluxDB 2.x | No             | Yes      | Metadata + Data, no full migration |
| Time Series | OpenTSDB     | No             | No       | Data migration only                |
| NoSQL       | MongoDB      | No             | No       | Data migration only                |
| File        | FTP/SFTP     | No             | No       | Data migration only                |
| File        | HDFS         | No             | No       | Data migration only                |

> **Note:**
> - Target is **ALWAYS** KaiwuDB with engine specified as RELATIONAL or TIMESERIES
> - Source **MUST** also specify engine field (RELATIONAL for RDBMS, TIMESERIES for others)
> - For SQL Server, InfluxDB 1.x/2.x: Use two-step migration (Schema first, then Data)
> - **Sources without metadata support (e.g. ClickHouse)**: KDTS `preview_ddl` generates DDL
>   from the passed-in Database object, NOT from the source connection — so a table-based
>   source (ClickHouse, TDengine 2.x) can still get DDL. **REQUIRED interaction — the table
>   structure MUST come from the USER** (source CREATE TABLE DDL or a column list); NEVER
>   guess the structure or rely on test code. Build the Database object manually from the
>   user-provided structure (use `build_manual_metadata()`), then call `preview_ddl()` as
>   usual. File sources (FTP/HDFS) have no table structure — pre-create the target tables.

### KaiwuDB Time-Series Table Constraints

When migrating to KaiwuDB with TIMESERIES engine, the following constraints apply:

| Constraint                                | Limit                      | Error Code                | KDTS Behavior            |
|-------------------------------------------|----------------------------|---------------------------|--------------------------|
| Maximum total columns (data + tags)       | 4096                       | -                         | -                        |
| Maximum source tags                       | 132 (128 tags + 4 primary) | 3004 (TAG_LIMIT_EXCEEDED) | ERROR if exceeded        |
| Maximum primary tags                      | 4                          | 3004 (TAG_LIMIT_EXCEEDED) | Auto-demote from last    |
| Maximum tag/column name length            | 128 bytes                  | 3005 (TAG_NAME_TOO_LONG)  | ERROR if exceeded        |
| Must have at least 1 primary tag          | 1                          | 3006 (NO_PRIMARY_TAG)     | ERROR if no eligible     |
| Primary tags must be in tag list          | -                          | -                         | Auto-demote              |
| Primary tags must be NOT NULL             | -                          | -                         | Auto-demote with warning |
| First column must be TIMESTAMPTZ NOT NULL | -                          | -                         | KDTS ensures in DDL      |

**Primary Tag Type Rules (from KDTS source - TypeMapping.FLOAT_TYPE_NAMES)**:
- **NOT eligible (float types)**: FLOAT, FLOAT4, FLOAT8, DOUBLE, REAL, BINARY_FLOAT, BINARY_DOUBLE, DECIMAL, NUMERIC → Auto-demoted to ordinary tags
  - **Note**: DECIMAL and NUMERIC are classified as float types by KDTS and cannot be primary tags
- **NOT eligible**: NULL/Nullable columns → Auto-demoted to ordinary tags
- **Auto-converted**: NVARCHAR, NCHAR, TEXT, CLOB, BLOB, BYTES, VARBYTES, JSON, ARRAY, MAP, INET, INTERVAL, UUID → Converted to VARCHAR(128)
- **VARCHAR handling**: Default 64 bytes, max 128 bytes (auto-truncated if exceeded)

**Tag Type Rules (from KDTS source)**:
- **Auto-converted**: TIMESTAMP, TIMESTAMPTZ, NVARCHAR, GEOMETRY → Converted to VARCHAR

**KDTS Auto-Mapping Algorithm**:
1. Collect all source tags
2. Validate count <= 132
3. Demote invalid primary tags (FLOAT, DOUBLE, DECIMAL, NUMERIC, NULL)
4. Identify eligible primary tags (NOT NULL, NOT FLOAT/DECIMAL/NUMERIC, NOT over-length)
5. If 0 eligible → ERROR 3006
6. Select first N eligible as PRIMARY TAGS (max 4)
7. Auto-convert invalid types to supported types

**Recommendation**: When source has many columns, consider splitting into multiple tables or migrations.

**Note**: For complete DDL syntax and auto-mapping details, see `references/ddl-syntax.md`

---

## API Endpoint Mapping

All endpoints under `{base_url}/kdts/api/v1`:

| Method | Path                    | Purpose                         | Script Function            |
|--------|-------------------------|---------------------------------|----------------------------|
| GET    | `/health`               | Health check                    | `test_connection()`        |
| POST   | `/datasource/validate`  | Test source/target connectivity | `test_connection()`        |
| POST   | `/datasource/databases` | List databases on source        | `list_databases()`         |
| POST   | `/datasource/metadata`  | Read source metadata            | `read_metadata()`          |
| POST   | `/metadata/preview`     | Preview DDL for target          | `preview_ddl()`            |
| POST   | `/metadata/execute`     | Execute DDL on target           | `execute_ddl()`            |
| POST   | `/datax/build`          | Build DataX migration script    | `build_migration_script()` |
| POST   | `/datax/execute`        | Execute migration scripts       | `execute_migration()`      |
| GET    | `/datax/status`         | Query migration status          | `query_task_status()`      |
| POST   | `/datax/control`        | Kill or query task              | `control_task()`           |

---

## Migration Workflows

### Workflow 1: Full Migration (Schema + Data)

**When to use:** Source supports full migration:

- MYSQL, ORACLE, POSTGRESQL, CLICKHOUSE, KAIWUDB, TDENGINE3X

**Note:** 
- KAIWUDB and CLICKHOUSE support auto-discovery (Full Migration) but do NOT support metadata reading (DDL generation). 
  You may need to pre-create target tables or use alternative DDL generation methods.
- SQLSERVER, INFLUXDB1X/2X support metadata + data but NOT auto-discovery (use Workflow 2).
- TDENGINE2X, OPENTSDB, MONGODB, FTP, HDFS only support data migration (use Workflow 3).

````
1. Collect parameters (interactive)
   +-- KDTS base URL
   +-- Source config (engine, type, host, port, user, password, db)
   |   Note: engine MUST be specified (RELATIONAL for RDBMS, TIMESERIES for others)
   +-- Target config (engine: RELATIONAL or TIMESERIES, host, port, user, password, db)
   |   Note: engine MUST be specified for KaiwuDB target
   +-- Metadata options (PK, constraint, comment, index, view)

2. Validate source type → ConfigValidator.validate_source_config()

3. Test connections → test_connection() × 2

4. Check target DB exists → list_databases()
   If not exists, remind user to create or use DDL

5. Read source metadata → read_metadata()
   Show table count, columns per table, PK/constraint info
   
   **Branch for sources WITHOUT metadata support**:
   5a. Check whether the TARGET table already exists (ask the user, or infer from a previous migration). 
   5b. If the target table exists and matches: skip DDL, go directly to data migration.
   5c. If NOT exists: **REQUIRED interaction — collect the table structure from the USER**
       (source CREATE TABLE DDL or a column list with names and types). NEVER guess the structure.
   5d. Build the Database object manually from the user-provided structure:
       ```python
       from scripts import build_manual_metadata, build_added_column, mark_time_series_columns
       db = build_manual_metadata('CLICKHOUSE', 'clickhouse_kwdb', 'test_tb', user_columns)
       mark_time_series_columns(db, 'test_tb', time_column='ts', primary_tags=['t1'], tags=[])
       # add a new column if the user wants one (e.g. t1 default 1)
       db['tableMap']['test_tb']['columns'].append(
           build_added_column('t1', 1, source_type='CLICKHOUSE', is_tag=True, is_primary_tag=True))
       ```
   5e. Continue with DDL preview (step 7) → confirmation → execute → then data migration.
       For file sources (FTP/HDFS, no table structure): pre-create the target tables.

6. **Configure Tags for Time-Series Target** (ONLY for TIMESERIES target with RELATIONAL source)
   
   **Trigger Condition**: Target engine is TIMESERIES AND source type is RELATIONAL (MySQL, Oracle, etc.)
   
   **Interaction Flow**:
   
   6.1 Show all columns for each table:
   ```
   Table: orders
   Columns:
   - id (BIGINT, PK)
   - customer_id (BIGINT)
   - product_id (BIGINT)
   - order_time (TIMESTAMP)
   - status (VARCHAR(50))
   - total_amount (DECIMAL(15,2))
   ```
   
   6.2 Ask user to select primary tags (1-4 columns, REQUIRED):
   ```
   Primary Tag Selection (1-4 required, max 4):
   [ ] id
   [ ] customer_id
   [ ] product_id
   [ ] order_time
   [ ] status
   [ ] total_amount
   
   Note: Primary tags are used for indexing and filtering in time-series queries
   Recommended: Select unique identifiers like device_id, sensor_id, etc.
   ```
   
   6.3 Ask user to select secondary tags (optional):
   ```
   Secondary Tag Selection (optional):
   [ ] id
   [ ] customer_id
   [ ] product_id
   [ ] order_time
   [ ] status
   [ ] total_amount
   
   Note: Secondary tags are additional indexed columns
   Recommended: Select commonly filtered columns like status, type, etc.
   ```
   
   6.4 Show summary and confirm:
   ```
   Tag Configuration Summary for orders table:
   - PRIMARY TAGS: customer_id, product_id
   - SECONDARY TAGS: status
   - VALUE FIELDS: id, order_time, total_amount
   
   Note: This configuration will be shown in the DDL preview.
   KDTS will generate appropriate time-series DDL based on this selection.
   ```
   
   **For Time-Series Sources (InfluxDB, TDengine, OpenTSDB)**:
   - Tags are AUTO-MAPPED from source to KaiwuDB:
     - InfluxDB tags → PRIMARY TAGS (first 4 eligible, rest become SECONDARY)
     - InfluxDB fields → VALUE columns
     - TDengine TAG columns → PRIMARY TAGS
     - TDengine regular columns → VALUE columns
   - No user interaction needed, but show the mapping in DDL preview for confirmation
   
   **Constraints**:
   - Maximum 4 PRIMARY TAGS per table (Error 3004 if exceeded)
   - At least 1 PRIMARY TAG required (Error 3006 if missing)
   - Maximum 4096 columns total (tags + values), max 132 tags from source
   - Column names max 128 bytes
   
   6.5 **Check Tag Column NULL Values (CRITICAL)**
   
   PRIMARY TAGS must be NOT NULL. If the source data contains NULL values in a column
   selected as PRIMARY TAG, the data migration will FAIL on write.
   
   **Required interaction**: After tag selection, check the source data for NULLs in
   all selected PRIMARY TAG columns:
   
   ```
   [WARNING] Primary Tag NULL Check
   ===============================
   Table: orders
   PRIMARY TAGS: customer_id, product_id
   
   Please verify in the source database (e.g., MySQL):
   SELECT COUNT(*) FROM orders WHERE customer_id IS NULL OR product_id IS NULL;
   
   If count > 0, options:
   1. Fix/backfill the NULL values in the source data, then re-run migration
   2. Choose different columns as PRIMARY TAGS (or demote to ordinary TAGS)
   3. Keep as-is — migration will fail on NULL tag values (NOT recommended)
   ```
   
   **Also apply to KDTS auto-mapped primary tags** (time-series sources): KDTS demotes
   NULL columns to ordinary tags with a warning, so the resulting DDL preview must be
   checked before execution.
   
   6.6 **Apply Tag Marks to the Metadata (CRITICAL)**
   
   KDTS generates time-series DDL from the tag marks on the source Database columns.
   After the user selects PRIMARY TAGS / TAGS / time column in steps 6.1-6.3, update the
   `source_db` object from `read_metadata()` — set these JSON fields per column
   (field names are declared explicitly in KDTS via `@JsonProperty`, matching
   `Column.java`; see `KaiwuDBStrategy.java` for the generation logic):
   
   - Time column: `"isTs": true` (KDTS renders it as the FIRST column, `TIMESTAMPTZ NOT NULL`)
   - Primary tag: `"isTag": true` AND `"isPrimaryTag": true` AND **`"nullAble": false`**
   - Ordinary tag: `"isTag": true` only
   - Everything else: leave `"isTs"/"isTag"/"isPrimaryTag"` as `false`
   
   **Primary tags MUST be NOT NULL in the column definition**: 
   KDTS demotes nullable primary tags to ordinary tags; if none remain eligible
   → Error 3006 (NO_PRIMARY_TAG). The helper sets `nullAble=false` automatically for
   primary tags — only use columns whose source DATA is NULL-free (see step 6.5).
   
   Use the provided helper to avoid manual field edits:
   ```python
   from scripts.api_client import mark_time_series_columns
   source_db = mark_time_series_columns(
       source_db=source_db,          # Database object from read_metadata()
       table_name="orders",
       time_column="order_time",
       primary_tags=["customer_id", "product_id"],
       tags=["status"],
   )
   ```
   
   **KDTS behavior when generating (from source code)**:
   - Tables with NO `"isTag": true` column are **SKIPPED** — no DDL is emitted for them
   - Primary tag demotion: FLOAT/DOUBLE/DECIMAL/NUMERIC or nullable columns → demoted to
     ordinary tags automatically (nullable primary tags are demoted with a warning)
   - If no eligible primary tag remains → Error 3006 (NO_PRIMARY_TAG)
   - Type conversion: primary tags of non-VARCHAR variable-length types (NVARCHAR, TEXT,
     CLOB, BLOB, VARBYTES, JSON, etc.) → converted to VARCHAR(128); VARCHAR > 128 truncated;
     VARCHAR without length → VARCHAR(64)
   - Ordinary tags of forbidden types (TIMESTAMP, TIMESTAMPTZ, NVARCHAR, GEOMETRY) → VARCHAR
   - > 132 tag columns → Error 3004; tag name > 128 bytes → Error 3005
   - `CREATE TS DATABASE` is emitted; Database `interval`/`retentions` fields become
     `PARTITION INTERVAL` / `RETENTIONS` clauses when present
   
   **Implementation Note**: 
   - KDTS `preview_ddl` fully supports time-series DDL generation from the tag marks
     described above — NO need for the skill to hand-craft DDL
   - The request field is `"isTimeSeries": true` (explicitly declared via
     `@JsonProperty("isTimeSeries")` in `PreviewDdlRequest.java`)
   - After DDL execution, use **Data-Only Migration** (Workflow 3) for data transfer
   - For TIMESERIES → TIMESERIES: KDTS handles automatic tag mapping internally

7. Preview DDL → preview_ddl()
   Show generated DDL for each table
   
   **For RELATIONAL → TIMESERIES (KDTS-Generated DDL)**:
   - Call `preview_ddl(target_config, source_db, metadata, is_time_series=True)` —
     the source_db object already carries the tag/primaryTag/ts marks from Step 6.6
   - KDTS generates `CREATE TS DATABASE` + time-series tables with TAGS / PRIMARY TAGS
   - Tables without any tag-marked column are SKIPPED in the output (warn the user)
   - Display with clear tag annotations (PRIMARY TAG, SECONDARY TAG, VALUE FIELD)
   - Point out any auto-demotion / type conversions in the DDL
     (FLOAT/nullable primary tags demoted, NVARCHAR→VARCHAR(128), etc.)
   - User confirms before execution
   
   Example DDL for RELATIONAL → TIMESERIES (as generated by KDTS):
   ```sql
   CREATE TABLE orders
   (
       order_time TIMESTAMPTZ NOT NULL,
       id BIGINT,
       total_amount DECIMAL(15,2)
   )
   TAGS
   (
       customer_id BIGINT NOT NULL,
       product_id BIGINT NOT NULL,
       status VARCHAR(50)
   )
   PRIMARY TAGS (customer_id, product_id);
   ```
   
   **Note**: For complete DDL syntax and KDTS auto-mapping details, see `references/ddl-syntax.md`
   - TIMESTAMPTZ is preferred over TIMESTAMP for timezone support
   - First column MUST be TIMESTAMPTZ NOT NULL
   - PRIMARY TAGS must be in the TAGS list and NOT NULL
   - Max 4 PRIMARY TAGS per table
   - KDTS auto-converts/demotes invalid tag types (see Section 3 in ddl-syntax.md)

   **For TIMESERIES → TIMESERIES (KDTS Auto-Generated)**:
   - Call `preview_ddl(target_config, source_db, metadata, is_time_series=True)`
     to get KDTS-generated DDL
   - KDTS auto-selects first 4 ELIGIBLE tags as PRIMARY TAGS (not simply first 4)
   - Ineligible tags (FLOAT, NULL, over-length) are auto-demoted to ordinary tags
   - Invalid types (NVARCHAR, TEXT, etc.) are auto-converted to VARCHAR
   - Show the mapped DDL for user confirmation with warnings about conversions
   
   Example DDL for TIMESERIES → TIMESERIES (InfluxDB auto-mapped):
   ```sql
   CREATE TABLE cpu_usage
   (
       time TIMESTAMPTZ NOT NULL,
       usage DOUBLE,
       temperature DOUBLE
   )
   TAGS
   (
       host VARCHAR(100) NOT NULL,
       region VARCHAR(50) NOT NULL
   )
   PRIMARY TAGS (host, region);
   ```
   
   Ask user to confirm before execution

8. Execute DDL → execute_ddl()
   **For RELATIONAL → TIMESERIES**: Execute the previewed DdlScript via the KDTS `execute_ddl()` API:
   `execute_ddl(target_config, previewed_ddl_script, auto_ddl=true)`.
   Do NOT rely on a direct JDBC/ODBC connection — the agent executes through KDTS.
   Note: the `createDb` field of DdlScript is NOT executed — KDTS generates the 
   CREATE DATABASE / CREATE TS DATABASE statement itself from the target engine and executes it when `auto_ddl=true`.
   **For TIMESERIES → TIMESERIES**: Use KDTS `execute_ddl()` API with the previewed DdlScript
   
   Report success with table count

9. **Switch to Data-Only Migration (RELATIONAL → TIMESERIES only)**
   Since the schema was created by the Skill-generated DDL, continue with **Workflow 3: Data-Only Migration**
   Note: `build_migration()` has NO `dataMode` parameter — data-only migration simply means
   providing **explicit table mappings** (`tables` REQUIRED, never empty) with the target tables already existing
   IMPORTANT: DataX configuration with `core` and `setting` is REQUIRED for successful data migration!
   
   Ask user: "Use default DataX configuration or customize?"
   
   Default DataX Configuration (Fixed Channel Count):
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
   Optional Configuration (Byte and Record Rate Limiting, Auto-Calculate Channel Count):
   ```json
   {
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
   ```
   Note: The above configuration will auto-calculate channel count = min(52428800/10485760, 40000/5000) = min(5, 8) = 5
   
   If user wants to customize, explain the configuration based on KDTS source annotations:
   
   **UserData Top-Level Configuration**:
   
   | Field | Type | Default | Description |
   |---|---|---|---|
   | enable | boolean | false | Whether to enable user data migration |
   | fetchSize | int | 1000 | Number of records fetched per pull from source |
   | batchSize | int | 1000 | Number of records submitted per push to target |
   | core | Object | - | DataX core config (required) |
   | setting | Object | - | DataX setting config (required) |
   
   **core.transport.channel.speed Configuration** (Map<String, Object> - Per-Channel Level):
   `byte` and `record` can be configured simultaneously; they are different dimensions of rate limiting and **NOT mutually exclusive**!
   
   | Key | Type | Description |
   |---|---|---|
   | byte | Long | Per-channel byte rate limit (bytes/second), e.g., 1048576 means 1MB/s/channel |
   | record | Long | Per-channel record rate limit (records/second), e.g., 1000 means 1000 records/s/channel |
   
   **setting.speed Configuration** (Map<String, Object> - Global Level):
   The following parameters can be combined to implement flexible rate limiting strategies:
   
   | Key | Type | Description |
   |---|---|---|
   | channel | Integer | Fixed channel count. If configured, channel count is fixed and does not participate in auto-calculation |
   | byte | Long | Global byte rate limit, must be used with core.transport.channel.speed.byte |
   | record | Long | Global record rate limit, must be used with core.transport.channel.speed.record |
   
   **Configuration Combination Examples**:
   
   | Configuration Method | setting.speed Configuration | core.transport.channel.speed Configuration | Description |
   |---|---|---|---|
   | Fixed Channel Count + Global Rate Limit | channel=4, byte=52428800, record=40000 | byte=1048576, record=1000 | Fixed 4 channels, global rate limit distributed to each channel |
   | Byte-Only Rate Limit | byte=52428800 | byte=1048576 | Channel count auto-calculated = 52428800 ÷ 1048576 = 5 |
   | Record-Only Rate Limit | record=40000 | record=1000 | Channel count auto-calculated = 40000 ÷ 1000 = 40 |
   | Combined Byte and Record Rate Limit | byte=52428800, record=40000 | byte=1048576, record=1000 | Calculate channel count separately, take the larger value max(5, 40) = 40 |
   
   **Configuration Rules**:
   - If `setting.speed.byte` is configured, `core.transport.channel.speed.byte` **must** also be configured
   - If `setting.speed.record` is configured, `core.transport.channel.speed.record` **must** also be configured
   - channel only: Fixed channel count, per-channel rate limit controlled by core.transport.channel.speed
   - byte or record only: Auto-calculate channel count = global rate limit / per-channel rate limit
   - byte and record together: Calculate required channel count separately, take the larger value
   - channel and byte/record together: Channel count fixed, byte/record serve as global rate limits
   
   **setting.errorLimit Configuration** (Map<String, Object>):
   
   | Key | Type | Description |
   |---|---|---|
   | record | Integer | Maximum allowed number of error records |
   | percentage | Float | Maximum allowed error percentage, e.g., 0.02 means 2% |
   
   **Source-Specific Options (When Configuring Table Mapping)**:
   
   *RDBMS Sources (MySQL, Oracle, PostgreSQL, etc.):*
   - splitPk: Split primary key; when enabled, DataX uses concurrent fetching (primary key type must be numeric or string)
   - where: Filter condition, appended to SQL WHERE clause (mutually exclusive with querySql)
   - querySql: Custom query SQL array (mutually exclusive with where)
   
   *KaiwuDB Target:*
   - writeMode: Write mode, insert (default) or upsert
   - preSql/postSql: SQL executed before/after writing
   
   *Time-Series Sources:*
   - beginDateTime/endDateTime: Time range filter
   - splitIntervalS: Time window split (seconds) for concurrent fetching
   - tsColumn: Timestamp column name (required when using time range)
   
   **Configuration Rules**:
   - byte and record in `core.transport.channel.speed` can be configured simultaneously (different dimensions of rate limiting)
   - channel, byte, and record in `setting.speed` can be used in combination
   - If `setting.speed.byte` is configured, `core.transport.channel.speed.byte` must also be configured
   - If `setting.speed.record` is configured, `core.transport.channel.speed.record` must also be configured
   - where and querySql are mutually exclusive and cannot be used simultaneously
   - splitPk and querySql are not recommended to be used simultaneously (splitPk requires original table structure, querySql may have no table)
   
   **CRITICAL**: Do NOT skip this step! Missing core/setting config causes migration failures.
   
   For complete configuration reference, see `references/api-reference.md` Chapter 11.

10. Build migration script → build_migration_script(data_config=user_config)
    Show generated script name(s)
    **IMPORTANT — tables parameter by target engine**:
    - **RELATIONAL target**: `tables` can be empty (auto-discover all tables) for full migration
    - **TIMESERIES target**: `tables` MUST be explicit table mappings — empty tables fails with
      error 4001 "No datax contents generated from config" (KDTS source explicitly rejects 
      whole-database migration into the time-series engine)
    - **PostgreSQL source limitation**: auto-discovery filters tables by `schema == dbName`. 
      Tables in the `public` schema (the common case) are filtered out → auto-discovery 
      fails with 4001 even for RELATIONAL targets. Use explicit table mappings for PostgreSQL,
      unless the tables live in a schema named after the database.
    - **Oracle source requirements**:
      - **dbName must be the owner (schema) name, usually UPPERCASE** — KDTS reads Oracle
        metadata via `all_tab_comments WHERE owner = dbName`; a lowercase dbName returns
        zero tables (e.g. dbName=`ORACLE_KWDB`, not `oracle_kwdb`)
      - **Names are UPPERCASE**: table and column names from the metadata are uppercase
        (e.g. `TEST_TB`, `TS`, `C1`); table-mapping columns must match exactly (uppercase)
      - **New-column type trap**: when adding a column to the metadata, pick a
        sourceColumnType with an exact mapping — `NUMBER(5,0)→INT2`, `NUMBER(10,0)→INT4`,
        `NUMBER(19,0)→INT8`; an unmapped value like `NUMBER(1,0)` falls back to `NUMBER`
        → FLOAT (float type) → demoted primary tag → error 3006
      - **Expression columns need separated target columns**: source `"...,1 as t1"`
        requires `target_columns="...,t1"` (target must use real column names, else
        DataX cannot find the target column)
    - **Added-column type rules (ALL source types → KaiwuDB)**: when adding a
      column that the source lacks (e.g. a tag column), derive its type from the
      DEFAULT VALUE — use `build_added_column(column_name, default_value, source_type)`:
      - int default → INT4 (INT8 for InfluxDB), str default → VARCHAR, bool default →
        BOOL (eligible for PRIMARY TAG)
      - **float default → FLOAT4/FLOAT8 — ordinary TAG ONLY, NEVER a primary tag**
        (float types are demoted by KDTS; 3006 if no eligible primary tag remains)
      - applies to ALL sources: RDBMS (MySQL/Oracle/PostgreSQL/SQL Server/ClickHouse),
        TDengine 2.x/3.x, InfluxDB 1.x/2.x, KaiwuDB
      - the sourceColumnType is picked per source for an EXACT mapping
        (MySQL/SQLServer/TDengine `INT`, Oracle `NUMBER(10,0)`, PostgreSQL `INTEGER`,
        ClickHouse `INT32`, InfluxDB `INTEGER`, KaiwuDB `INT4`)
      - NOTE: KaiwuDB has no type-mapping rules in KDTS — verify the generated DDL
      - for SELECT-based sources the mapping source column uses a SQL expression
        matching the default (e.g. `1 as t1` for default 1); InfluxDB mappings use
        `build_influxdb_mapping()` (no SQL-expression support)
      Build mappings with `build_table_mapping()` per table (source + target columns).
      **Source identifier field per type**:
      `table` for RDBMS/KAIWUDB/TDENGINE/OPENTSDB, `measurement` for INFLUXDB,
      `collectionName` for MONGODB — build_table_mapping handles this automatically.
      FTP/HDFS are file sources (no table) — build their mappings manually (path-based).
      **InfluxDB REQUIRED interaction — data time range**: before building an
      InfluxDB mapping, ask the user for the data time range
      (begin/end "YYYY-MM-DD HH:MM:SS") and pass it to `build_influxdb_mapping()`
      with `split_interval_s` (default 86400 = 1 day). NO defaults for the range:
      a null range fails the migration, and a too-wide range (e.g. 1970~2099)
      causes reader memory overflow.
      Optional: readTimeout/connectTimeout (seconds; KDTS tests use 60).
      **Extended mapping options**: `build_table_mapping()`
      supports `where` (source filter, e.g. time range; RDBMS/KAIWUDB/TDENGINE/OPENTSDB),
      `pre_sql`/`post_sql` (target pre/post SQL, e.g. drop/create table), and SQL
      expression columns for RDBMS (e.g. `"...,1 as t1"`).
      **OpenTSDB mapping requirements**:
      - `column` is a list of FULL METRIC names in `table.metric` format
        (e.g. `"test_tb.c1,test_tb.c2,..."`) — NOT plain column names
      - **time range REQUIRED**: beginDateTime/endDateTime (no splitIntervalS) —
        collect the data time range from the user
      - OpenTSDB usually has NO authentication (username/password may be empty)
      **SQL Server source requirements**:
      - JDBC URL MUST include `encrypt=true;trustServerCertificate=true`
        (modern JDBC drivers require TLS by default):
        `jdbc:sqlserver://host:1433;databaseName=db;encrypt=true;trustServerCertificate=true`
      - supports `where` filters and SQL expression columns (RDBMS mapping, e.g.
        `1 as t1`); two-step migration (schema + data), no full migration
      - **schemaName fix**: the metadata table schemaName may come back as
        the DATABASE name → DDL becomes `"db"."db"."table"` (duplicated). Set the table
        schemaName to `public` so DDL is `"db"."public"."table"`
      **KaiwuDB-source mapping requirements** (KaiwuDB→KaiwuDB): 
      the KaiwuDB source (time-series engine) REQUIRES `beginDateTime`/`endDateTime` (data time range)
      and `tsColumn` (time column name, e.g. "ts") in the mapping — collect the time range from the user.
      **MongoDB mapping requirements**:
      - source identifier is `collectionName` (NOT `table`)
      - `column` is a JSON array string with name/type (e.g.
        `[{"name":"ts","type":"date"},{"name":"c1","type":"int"},...]`), NOT a comma
        string — types: date/int/long/double/bool/string/bytes
      - **`query` (optional filter)**: MongoDB JSON query syntax as a string,
        e.g. `{"t1":{"$gte":1,"$lt":8}}` — filters documents before migration
      - **Table creation is LIMITED to two options** (KDTS does NOT support MongoDB→KaiwuDB 
        type mapping — its generic fallback emits invalid types like LONG/STRING):
        1. **User pre-creates the target table** (skip DDL, migrate data directly);
        2. **SKILL generates the DDL from the USER-provided column info + type
           mapping rules** (int→INT4, long→INT8, double→FLOAT8, string→VARCHAR,
           bytes→VARBYTES, date→TIMESTAMP, bool→BOOL), user confirms, then
           `execute_ddl()`. If DDL execution FAILS: inform the user that the target
           table was NOT created and END the migration.
      **FTP mapping requirements**:
      - **`path` MUST be an absolute path starting with `/`**
      - **`path` is the SFTP SERVER-side path**, NOT the client local path — it must
        be resolvable where the SFTP service runs (Windows host, WSL, or container).
      - **`skipHeader: true`** when the CSV has a header row (otherwise the header is migrated as data)
      - `column` is a JSON array string with index/type/format per field (see `references/config-templates.md` §10.1)
      **HDFS mapping requirements**:
      - `path` is the HDFS SERVER-side path (JSON array string, absolute, e.g.
        `["/user/hive/warehouse/hdfs_test.db/test_tb"]`) — NOT a local path
      - `fileType` REQUIRED: `text` / `orc` / `parquet` / `rcfile` (text supports
        fieldDelimiter/encoding/compress/csvReaderConfig; orc/parquet do not)
      - `column` is a JSON array string with index/type/format per field (same
        structure as FTP, e.g. 14 columns with date/long/double/boolean/string)
      - `compress`: file compression (e.g. `gzip` for text files)
      - Kerberos-secured clusters: `haveKerberos` + `kerberosPrincipal` + `kerberosKeytabFilePath`
      - DataSource: host = NameNode host, port = 9000 (RPC), user/password
      - target tables must pre-exist (file source, no table structure)
      **HDFS mapping example**: see `references/config-templates.md` §10.2
      **View migration**: to migrate views, pass metadata option `view: true` to
      `read_metadata()` / `preview_ddl()` — views are then included in the DDL.

11. Execute migration → execute_migration() or execute_migration_batches()
    Return log file paths
    **BATCH EXECUTION (REQUIRED for many scripts)**: When `build_migration()` returns
    MANY scripts (one per table), DO NOT submit them all in a single
    `execute_migration()` call — the KDTS server starts DataX processes sequentially
    and the request exceeds the client read timeout.
    Instead use the batch workflow manager:
    ```python
    result = workflow.execute_migration_batches(
        script_names=script_names,   # all generated scripts
        batch_size=10,               # 10 scripts per batch
        batch_timeout=3600,          # per-batch wait limit
    )
    # result['all_succeeded'] == True  → every batch reached SUCCEEDED
    ```
    Rule of thumb: batch_size=10 for large table counts (>20 tables); single-shot
    `execute_migration()` is fine for ≤ 10 scripts. Timeout note: a 4003 on submission
    means the request reached the server (it keeps processing) — still monitor.

12. Monitor progress → query_task_status() (polling every 2s)
    Show status: SUBMITTED → RUNNING → SUCCEEDED/FAILED
    Report final status (execute_migration_batches monitors each batch to completion)

13. Verify (manual step for user)
    Remind to compare row counts between source and target
````

### Workflow 2: Schema-Only Migration

**When to use:** Only need table structure, no data transfer

````
Steps 1-8 from Workflow 1, then STOP.
Report DDL execution result.
````

### Workflow 3: Data-Only Migration

**When to use:**

- Target tables already exist, only need data sync
- For InfluxDB 1.x/2.x: Use this after Schema migration (Workflow 1 steps 1-7)

````
1. Collect parameters (interactive)
   +-- KDTS base URL
   +-- Source config
   +-- Target config
   +-- Table mappings (tables MUST be provided)

2. Validate source type

3. Test connections × 2

4. **Configure DataX Parameters** (REQUIRED - see Workflow 1 step 8 for details)
   Show default config and ask user to confirm or customize

5. Build migration script with explicit tables field
   → build_migration(tables=table_mappings, data_config=user_config)
   Note: tables are ALWAYS required for TIMESERIES targets (auto-discovery fails with 4001)

6. Execute migration (use `execute_migration_batches()` when > 10 scripts — see
   Workflow 1 step 11 for batch execution rules)

7. Monitor progress
````

### Workflow 4: Table-Level Migration (Restricted Sources)

**When to use:** Source does NOT support full migration (SQL Server, TDengine 2.x, OpenTSDB, MongoDB, FTP, HDFS)

````
1. Collect ALL table mappings explicitly:
   Source: table name, columns
   Target: table name, columns, write mode (insert/upsert)

2. Validate source type

3. Test connections × 2

4. **Configure DataX Parameters** (REQUIRED - see Workflow 1 step 8 for details)
   Show default config and ask user to confirm or customize

5. Build migration script with explicit tables field
   → build_migration(tables=all_mappings, data_config=user_config)

6. Execute and monitor (use `execute_migration_batches()` when > 10 scripts — see
   Workflow 1 step 11 for batch execution rules)
````

---

## Source Type Configuration Templates

### Source Configuration Examples

**Important**: For ALL source configurations, the `engine` field is **REQUIRED** per KDTS API:
- Use `RELATIONAL` for: MySQL, Oracle, PostgreSQL, SQL Server, ClickHouse
- Use `TIMESERIES` for: KAIWUDB, TDengine 2.x/3.x, InfluxDB 1.x/2.x, OpenTSDB, MongoDB, FTP, HDFS

#### Relational Source (MySQL Example)

```json
{
  "engine": "RELATIONAL",
  "type": "MYSQL",
  "host": "127.0.0.1",
  "port": 3306,
  "username": "root",
  "password": "********",
  "dbName": "source_db"
}
```

#### Time Series Source (InfluxDB Example)

```json
{
  "engine": "TIMESERIES",
  "type": "INFLUXDB1X",
  "host": "127.0.0.1",
  "port": 8086,
  "username": "admin",
  "password": "********",
  "dbName": "source_db"
}
```

### Target Configuration Examples

**Note:** For target (KaiwuDB) configuration, `engine` field is REQUIRED to specify the KaiwuDB storage engine:

- Use `RELATIONAL` for relational database
- Use `TIMESERIES` for time-series database

#### KaiwuDB Target - Relational Engine

```json
{
  "type": "KAIWUDB",
  "engine": "RELATIONAL",
  "host": "127.0.0.1",
  "port": 26257,
  "username": "root",
  "password": "********",
  "dbName": "target_db",
  "isTarget": true
}
```

#### KaiwuDB Target - Time Series Engine

```json
{
  "type": "KAIWUDB",
  "engine": "TIMESERIES",
  "host": "127.0.0.1",
  "port": 26257,
  "username": "root",
  "password": "********",
  "dbName": "target_ts_db",
  "isTarget": true
}
```

### Source Type → sourceType Mapping

When building migration scripts, use the appropriate `sourceType`:

| KDTS Source Type                                 | sourceType value |
|--------------------------------------------------|------------------|
| MYSQL, ORACLE, POSTGRESQL, SQLSERVER, CLICKHOUSE | `RDBMS`          |
| KAIWUDB                                          | `KAIWUDB`        |
| TDENGINE2X, TDENGINE3X                           | `TDENGINE`       |
| INFLUXDB1X, INFLUXDB2X                           | `INFLUXDB`       |
| MONGODB                                          | `MONGODB`        |
| OPENTSDB                                         | `OPENTSDB`       |
| FTP                                              | `FTP`            |
| HDFS                                             | `HDFS`           |

---

## Error Handling

Refer to `references/error-codes.md` for complete error code reference.

When API returns error:

1. Extract `code` and `message` from response
2. Call `get_error_hint(code)` to get user-friendly explanation and fix suggestion
3. Show both original error and hint to user
4. If it's a connection/validation error, **stop and ask for corrected parameters**
5. If it's a data migration error, show partial progress and ask whether to retry or skip

### Common Error Scenarios

| Code | Meaning                 | Action                                                          |
|------|-------------------------|-----------------------------------------------------------------|
| 1001 | Invalid parameters      | Show which field is missing/wrong                               |
| 1002 | Unsupported source type | Show supported types, ask user to choose                        |
| 2001 | Connection failed       | Check host/port/credentials, test network                       |
| 3004 | Tag limit exceeded      | Reduce tag columns or split migration                           |
| 4001 | Build failed            | Check table mapping, ensure both sides match                    |
| 4002 | Launch failed           | Check Python 3 availability on KDTS server                      |
| 4003 | Timeout                 | Batch execution + larger KDTS_TIMEOUT; still monitor after 4003 |
| 5001 | Thread pool full        | Wait and retry (HTTP 503, Retry-After: 10)                      |
| 5002 | Python not found        | Install Python 3 on KDTS server                                 |

---

## Interactive Parameter Collection

When user intent is identified but parameters are missing, collect them step by step:

### Step 1: KDTS Server

````
What is the KDTS server address?
(default: http://localhost:8989)
````

### Step 2: Migration Type

````
Select migration type:
1. Full Migration (schema + data)
2. Schema-Only Migration (DDL only)
3. Data-Only Migration (tables must exist)
````

### Step 3: Source Configuration

````
Source database type?
[MySQL, Oracle, PostgreSQL, SQL Server, ClickHouse, TDengine 2.x/3.x, 
 InfluxDB 1.x/2.x, OpenTSDB, MongoDB, FTP, HDFS, KaiwuDB]

Source connection:
Host: 
Port: (show default based on type, e.g., MySQL=3306)
Username: 
Password: 
Database:
````

### Step 4: Target Configuration

````
Target KaiwuDB connection:
Engine: [RELATIONAL, TIMESERIES]
Host: (default: 127.0.0.1)
Port: (default: 26257)
Username: (default: root)
Password: 
Database:
````

### Step 5: Migration Scope

````
Migration scope:
1. Full database (all tables)
2. Specific tables only

If specific tables:
- Table name(s):
- Columns (optional):
````

### Step 6: Data Configuration (Optional)

````
Data migration settings:
Fetch size (rows per fetch, default 1000): 
Batch size (rows per write, default 1000):
Error tolerance (% allowed, default 0.02):
Concurrency (channels, default 4):
````

---

## Confirmation Gates (Critical Safety Points)

### Gate 1: DDL Execution Confirmation

**Before executing DDL**, you MUST:

1. Show the previewed DDL to the user
2. Explain what will be created (databases, tables, indexes, constraints)
3. Warn about potential issues:
    - Existing tables will be overwritten (if `auto_ddl=true`)
    - Data loss if target already has data
4. Ask for explicit confirmation:
   ````
   [WARNING] DDL Execution Preview
   ===============================
   Database: [db_name]
   Tables to create: [count]
   - table1: [columns, PK, indexes]
   - table2: ...
   
   [WARNING] This will create tables in the target KaiwuDB.
   [WARNING] Existing tables with the same name will be overwritten.
   
   Do you want to proceed? (yes/no)
   ````
5. If user says NO, save the DDL preview and offer to show it later

### Gate 2: KILL Operation Confirmation

**Before killing a running migration**, you MUST:

1. Show current task status and progress
2. Explain the consequence:
   ````
   [WARNING] Task Termination Warning
   ===============================
   Task: [script_name]
   Status: [RUNNING/SUBMITTED]
   Progress: [X%]
   Elapsed: [minutes]
   
   [WARNING] Killing this task will:
   - Stop data transfer immediately
   - Leave partial data in target
   - Require manual cleanup or re-migration
   - Cannot be resumed
   
   Are you absolutely sure you want to kill this task? 
   (Type "YES" to confirm)
   ````
3. Only proceed if user explicitly types "YES"

### Gate 3: Source with Limited Capability

**When source doesn't support full migration**, you MUST:

1. Explain the limitation clearly:
   ````
   [WARNING] Source Type Limitation
   ===============================
   Source type: SQLSERVER
   
   This source does NOT support:
   - Automatic schema discovery
   - Full database migration
   
   Supported operations:
   - Table-level migration (you must specify each table)
   
   Please provide table mappings:
   ````
2. Help user build explicit table mappings

---

## Error Recovery Flow

### Scenario 1: Connection Failure

**Problem**: `test_connection()` returns error

**Recovery Steps**:

1. Show error details: host, port, error code, message
2. Suggest common fixes:
    - Check if database is running
    - Verify host/port accessibility
    - Confirm credentials
    - Check firewall/network
3. Ask user to verify and retry
4. If user provides new values, update config and retry

### Scenario 2: Partial Migration Failure

**Problem**: Migration fails after some data transferred

**Recovery Steps**:

1. Check which tables failed vs succeeded
2. Show summary:
   ````
   Migration Summary
   =================
   Total tables: 10
   Succeeded: 7
   Failed: 3
   
   Failed tables:
   - table_a: [error message]
   - table_b: [error message]
   - table_c: [error message]
   ````
3. Offer options:
    - **Retry failed tables only** (recommended)
    - **Restart entire migration** (cleanup first)
    - **Skip and continue** (accept partial result)
4. If retrying failed tables:
    - Use table-level migration for specific tables
    - Consider increasing error tolerance

### Scenario 3: Metadata Reading Failure

**Problem**: `read_metadata()` fails or returns empty

**Recovery Steps**:

1. Check if source is accessible (retry connection test)
2. Verify database exists and user has permissions
3. For sources without metadata support (ClickHouse, TDengine 2.x, etc.):
    - Inform user: "This source type doesn't support metadata reading"
    - Offer to skip to DDL phase or use table-level migration

### Scenario 4: DDL Execution Failure

**Problem**: `execute_ddl()` fails

**Recovery Steps**:

1. Show the exact DDL that failed
2. Highlight problematic SQL
3. Suggest fixes:
    - Syntax error: Show alternative syntax
    - Type mismatch: Show compatible types
    - Already exists: Suggest `auto_ddl=true` or manual DDL
4. Offer to:
    - Show corrected DDL
    - Skip DDL (if tables exist)
    - Retry with different options

### Scenario 5: Build Failed with 4001 "No datax contents generated from config"

**Problem**: `build_migration()` with empty `tables` fails with 4001

**Recovery Steps**:

1. Check the target engine:
    - **RELATIONAL target**: empty `tables` is valid (auto-discovery) — check source type
      supports full migration instead
    - **TIMESERIES target**: auto-discovery is NOT supported — this is the expected cause
2. Rebuild with **explicit table mappings** for every table:
   ```python
   mapping = build_table_mapping(
       source_type="MYSQL",
       source_table="test_tb",
       target_table="test_tb",
       columns="ts,c1,c2,c3",
       write_mode="insert",
   )
   build_result = client.build_migration(source, target, tables=[mapping], data_config=data_config)
   ```
3. If still failing, check DataX templates on the KDTS server and the request body

### Scenario 6: Migration Failed on Tag Column NULL Values

**Problem**: Migration task FAILED (activeProcessCount=0) with no detail in status query;
KDTS server log shows tag column NULL constraint violations

**Root cause**: PRIMARY TAGS must be NOT NULL, but source data contains NULL values
in the selected primary tag columns

**Recovery Steps**:

1. Ask the user to check the KDTS server log to confirm (e.g., `NULL` constraint error)
2. Check source data for NULLs in primary tag columns:
   ```sql
   SELECT COUNT(*) FROM <table> WHERE <primary_tag_col> IS NULL;
   ```
3. Offer options:
    - **Fix source data**: backfill the NULL values, then re-run the migration (recommended)
    - **Change tag selection**: pick different columns as PRIMARY TAGS (must be NOT NULL, non-float)
    - **Demote to ordinary TAGS**: ordinary tags allow NULL (nullable)
4. Re-run data migration — target schema stays unchanged in options 1 and 3

---

## Edge Case Handling

### Edge Case 1: Large Dataset Migration (1M+ Rows)

**Symptoms**: Migration takes too long, times out, or errors

**Handling**:

1. Recommend batch migration:
   ```python
   # Split into batches of 100K rows
   batch_config = {"splitPk": "id", "channel": 10}
   ```
2. **Execute scripts in batches** (many tables → many scripts): use
   `workflow.execute_migration_batches(script_names, batch_size=10)` — submitting
   dozens of scripts in one `execute_migration()` call causes HTTP 4003 timeouts; 
   batch execution waits per batch to completion
3. Monitor progress frequently (every 30 seconds)
4. Warn user about estimated time
5. Offer to run in background mode (poll only, no waiting)

### Edge Case 2: Concurrent Migration Tasks

**Symptoms**: Multiple migrations running simultaneously

**Handling**:

1. Note: the KDTS API has NO "list all tasks" endpoint — `query_status()` works per
   script name only. Check running tasks by querying the known script names, or ask
   the user whether other migrations are running.
   ```python
   for name in script_names:          # known scripts from build_migration()
       status = client.query_status(name)
   ```
2. If other tasks exist:
    - Show their names, progress, estimated completion
    - Warn about resource contention
    - Ask user to wait or proceed anyway

### Edge Case 3: Schema Drift (Source Changed During Migration)

**Symptoms**: Source table structure changed after DDL but before data migration

**Handling**:

1. Detect schema mismatch when data errors occur
2. Show error: "Schema changed during migration"
3. Offer to:
    - Re-run metadata + DDL (will recreate target tables)
    - Continue with partial data (accept data loss for changed columns)
    - Cancel migration

### Edge Case 4: Timeout During Long Migration

**Symptoms**: `wait_for_completion()` times out

**Handling**:

1. Return current task status
2. Show progress achieved
3. Offer options:
    - **Continue waiting** (extend timeout)
    - **Poll only** (check status without waiting)
    - **Kill and restart** (if stuck)
4. Always show current progress before deciding

### Edge Case 5: Unsupported Data Types

**Symptoms**: Column type not supported in KaiwuDB

**Handling**:

1. Show problematic columns:
   ````
   [WARNING] Unsupported Type Detected
   ===============================
   Table: users
   Column: avatar
   Source type: BLOB
   
   KaiwuDB compatible alternatives:
   - BINARY (max 64KB)
   - VARBINARY (max 64KB)
   - LOB (for large objects)
   
   Please select target type:
   ````
2. Map to the closest compatible type
3. Note: May need to split or convert large objects

---

## Workflow State Management

### State Tracking

Track migration progress with these states:

````
INIT → COLLECTING_PARAMS → VALIDATING → TESTING_CONNECTIONS 
    → READING_METADATA → PREVIEWING_DDL → WAITING_CONFIRMATION 
    → EXECUTING_DDL → BUILDING_SCRIPT → EXECUTING_MIGRATION 
    → MONITORING → COMPLETED | FAILED | KILLED
````

### Resume After Interruption

If conversation is interrupted:

1. When user returns, ask:
   ````
   Welcome back! I found your previous migration session:
   
   Source: MySQL @ 192.168.1.100:3306/users_db
   Target: KaiwuDB @ 127.0.0.1:26257
   Progress: DDL executed, migration in progress (60%)
   
   Would you like to:
   1. Continue monitoring current migration
   2. Check current status
   3. Start a new migration
   ````
2. If continuing, query task status immediately
3. Show latest progress

---

## Cross-Reference

- API Reference: `references/api-reference.md`
- DDL Syntax: `references/ddl-syntax.md`
- Source Types: `references/source-types.md`
- Error Codes: `references/error-codes.md`
- Type Mapping: `references/type-mapping.md`
- Config Templates: `references/config-templates.md`
- Migration Checklist: `assets/migration-checklist.md`
- Prompt Examples: `assets/prompt-examples.md`
- Script README: `scripts/README.md`
- KDTS Docs: `{kw-datax-utils}/docs/api.md`

---

## Notes

- KDTS Server is the backend service; this skill is the AI agent interface
- All operations are stateless — the agent does NOT maintain session
- Task tracking is via `script_name` returned by build endpoint
- Migration scripts are stored on KDTS server at `/opt/kdts/datax/job/`
- Log files are at `/opt/kdts/data/log/`
- For large migrations (>1M rows), recommend monitoring with `query_task_status()` until completion
- **DO NOT** assume migration succeeded — always verify with row count comparison

## Support

If migration fails:

1. Check error codes in `references/error-codes.md`
2. Review KDTS server logs
3. Test connection again
4. Try with smaller batch size or fewer tables
