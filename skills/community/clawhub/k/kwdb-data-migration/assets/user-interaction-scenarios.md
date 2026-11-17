# KWDB Data Migration Skill - User Interaction Scenarios

This document provides interaction scenarios for validating AI Agent behavior during database migration.

## Language Versions

- **English Version**: This file (`user-interaction-scenarios.md`)
- **Chinese Version**: `user-interaction-scenarios.zh.md`

Both versions contain the same 8 scenarios with dialogue in their respective languages. The AI Agent should respond in the same language the user uses.

## Scenario 1: MySQL to KaiwuDB (Relational) - Full Migration

### User Request
````
Help me migrate MySQL order_system database to KaiwuDB relational database
````

### Expected AI Agent Response

**Step 1: Recognize Migration Intent**
````
[OK] Migration intent recognized: MySQL (order_system) -> KaiwuDB (RELATIONAL)

Please provide the following information to start migration:

1. KDTS server address (default: http://127.0.0.1:8989)
2. MySQL connection info:
   - Host:
   - Port (default 3306):
   - Username:
   - Password:
3. KaiwuDB connection info:
   - Host (default 127.0.0.1):
   - Port (default 26257):
   - Username (default root):
   - Password:
   - Target database name (default order_system):

[IMPORTANT] Security reminder: Please ensure you have backed up both source and target databases before migration!
````

**User Response**
````
KDTS at http://192.168.1.100:8989
MySQL: 192.168.1.50:3306, user=root, password=mysql123
KaiwuDB: 127.0.0.1:26257, user=root, password=kwdb_secret
Target database name: order_system
````

**Step 2: Parameter Validation**
````
[OK] Parameters collected, starting validation...

[System Internal Call]
1. ConfigValidator.validate_source_config()
2. ConfigValidator.validate_target_config()
3. Source capability check: MySQL supports full migration [OK]

[OK] Parameter validation passed
````

**Step 3: Connection Test**
````
[INFO] Testing database connections...

[System Internal Call]
1. KDTSClient.test_connection(source_config)
2. KDTSClient.test_connection(target_config)

[OK] MySQL connection successful (192.168.1.50:3306)
[OK] KaiwuDB connection successful (127.0.0.1:26257)
````

**Step 4: Read Metadata**
````
[INFO] Reading MySQL metadata...

[System Internal Call]
1. KDTSClient.read_metadata(source_config)

[OK] Found 6 tables:
   - orders (15 columns)
   - order_items (8 columns)
   - customers (12 columns)
   - products (10 columns)
   - categories (5 columns)
   - inventory (7 columns)

   Estimated total data volume: ~50,000 rows
````

**Step 5: Preview DDL**
````
[INFO] Generating KaiwuDB DDL...

[System Internal Call]
1. KDTSClient.preview_ddl(target_config, source_db, metadata)

[WARNING] DDL preview (first 3 tables):
```sql
-- orders table
CREATE TABLE orders (
    id INT8 PRIMARY KEY,
    customer_id INT8,
    order_time TIMESTAMP,
    total_amount DECIMAL(15,2),
    status VARCHAR(50)
);

-- order_items table
CREATE TABLE order_items (
    id INT8 PRIMARY KEY,
    order_id INT8,
    product_id INT8,
    quantity INT,
    price DECIMAL(10,2)
);
```

[WARNING] About to execute DDL to create 6 tables in KaiwuDB
[WARNING] Existing target tables will be overwritten

Confirm execution? (yes/no)
````

**User Response**
````
yes
````

**Step 6: Execute DDL**
````
[OK] Executing DDL...

[System Internal Call]
1. KDTSClient.execute_ddl(target_config, ddl_script, auto_ddl=True)

[OK] DDL execution successful!
   SQL file saved to: /opt/kdts/data/sql/order_system_ddl.sql
   Tables created: 6
   Time taken: 0.8 seconds
````

**Step 7: Build & Execute Migration**
````
[INFO] Building migration task...

[System Internal Call]
1. KDTSClient.build_migration(source_config, target_config)

[OK] Migration task built successfully
   Task name: MYSQL2KAIWUDB_1720000000000.json
   
   Starting data migration...

[System Internal Call]
1. KDTSClient.execute_migration(script_names)

[INFO] Migration task started, monitoring progress...
````

**Step 8: Monitor Progress**
````
[INFO] Migration progress:
   |████████████████████████████████████████| 100%
   
   orders:        [████████████████████] 100% (12,345 rows)
   order_items:   [████████████████████] 100% (45,678 rows)
   customers:     [████████████████████] 100% (2,345 rows)
   products:      [████████████████████] 100% (1,234 rows)
   categories:    [████████████████████] 100% (56 rows)
   inventory:     [████████████████████] 100% (3,456 rows)

[OK] Migration completed!
   Total rows migrated: 65,114
   Time taken: 45.2 seconds
   Average speed: 1,440 rows/second

[REPORT] Migration report:
   - Successful tables: 6/6
   - Failed tables: 0/6
   - Error rows: 0

[TIP] Recommendation: Please verify data integrity by comparing row counts between source and target databases
````

---

## Scenario 2: InfluxDB to KaiwuDB (Time Series) - Two-Step Migration

### User Request
````
I want to migrate InfluxDB metrics bucket to KaiwuDB time series database
````

### Expected AI Agent Response

**Step 1: Recognize Migration Intent**
````
[OK] Migration intent recognized: InfluxDB (metrics bucket) -> KaiwuDB (TIMESERIES)

[INFO] InfluxDB Note: Full migration (Schema + Data) requires two steps:
   1. Step 1: Migrate table structure (Schema/DDL)
   2. Step 2: Migrate data (Data)

   I will perform both steps for you.

Please provide the following information:

1. KDTS server address (default: http://127.0.0.1:8989)
2. InfluxDB connection info:
   - Version (1.x or 2.x):
   - Host:
   - Port (default 8086):
   - Username:
   - Password (token required for 2.x):
   - Bucket/Database name (metrics):
3. KaiwuDB connection info:
   - Host (default 127.0.0.1):
   - Port (default 26257):
   - Username (default root):
   - Password:
   - Target database name (default metrics):

[IMPORTANT] Security reminder: Please ensure you have backed up both source data and target database before migration!
````

**User Response**
````
KDTS: http://192.168.1.100:8989
InfluxDB 2.x: 192.168.1.60:8086, token=my-influxdb-token, bucket=metrics
KaiwuDB: 127.0.0.1:26257, user=root, password=kwdb_secret
Target database name: metrics_ts
````

**Step 2: Step 1 - Schema Migration**
````
[INFO] Step 1: Migrating table structure (Schema)

[INFO] Reading InfluxDB metadata...

[System Internal Call]
1. KDTSClient.read_metadata(source_config)

[OK] Found 3 measurements:
   - cpu_usage (tags: host, region; fields: usage, temperature)
   - memory_usage (tags: host, region; fields: used, free)
   - network_io (tags: host, interface; fields: rx_bytes, tx_bytes)

[INFO] Generating KaiwuDB time series table DDL...

[WARNING] DDL preview (cpu_usage example):
```sql
CREATE TABLE cpu_usage (
    time TIMESTAMP,
    host VARCHAR(100) PRIMARY TAG,
    region VARCHAR(50) TAG,
    usage FLOAT8 FIELD,
    temperature FLOAT8 FIELD
);
```

[WARNING] About to execute DDL to create 3 time series tables

Confirm execution? (yes/no)
````

**User Response**
````
yes
````

````
[OK] DDL execution successful!
   Tables created: 3
   Time taken: 0.5 seconds

[INFO] Step 2: Starting data migration...
````

**Step 3: Step 2 - Data Migration**
````
[INFO] Building data migration task...

[System Internal Call]
1. KDTSClient.build_migration(source_config, target_config)

[OK] Data migration task built successfully
   Task name: INFLUXDB2X2KAIWUDB_1720000000000.json

[INFO] Migrating data...
````

**Step 4: Monitor & Complete**
````
[INFO] Migration progress:
   |████████████████████████████████████████| 100%

   cpu_usage:    [████████████████████] 100% (1,234,567 rows)
   memory_usage: [████████████████████] 100% (1,234,567 rows)
   network_io:   [████████████████████] 100% (1,234,567 rows)

[OK] Migration completed!
   Total rows migrated: 3,703,701
   Time taken: 180.5 seconds
   Average speed: 20,520 rows/second

[REPORT] Migration report:
   - Schema migration: [OK] Success (3 tables)
   - Data migration: [OK] Success (3,703,701 rows)
   - Error rows: 0

[TIP] Recommendation: Please verify data integrity, especially timestamps and tags for time series data
````

---

## Scenario 3: Error Handling - Connection Failure

### User Request
````
Help me migrate data
````

### Expected AI Agent Response
````
[OK] Please provide more information so I can help you migrate data:

1. Source database type (MySQL, Oracle, PostgreSQL, InfluxDB, etc.)
2. Target KaiwuDB engine type (RELATIONAL or TIMESERIES)
3. KDTS server address
4. Source database connection info
5. Target KaiwuDB connection info
````

**User Response**
````
Source: MySQL at 192.168.1.50:3306, user=root, password=wrong
Target: KaiwuDB RELATIONAL
KDTS: http://192.168.1.100:8989
````

**Expected AI Agent Response**
````
[INFO] Testing connection...

[ERROR] MySQL connection failed!
   Error message: Access denied for user 'root'@'192.168.1.100'

[TIP] Possible causes:
   1. Incorrect password
   2. User does not have permission to connect from this IP
   3. MySQL service is not running

[SUGGESTION] Recommended actions:
   - Verify username and password
   - Check MySQL user permissions
   - Retry with correct password

Please provide correct MySQL connection information.
````

---

## Scenario 4: Non-Supported Source Type

### User Request
````
Help me migrate Redis data to KaiwuDB
````

### Expected AI Agent Response
````
[WARNING] Sorry, Redis is not currently supported as a source database.

Currently supported source database types:
[OK] Relational databases: MySQL, Oracle, PostgreSQL, SQL Server, ClickHouse
[OK] Time series databases: TDengine 2.x/3.x, InfluxDB 1.x/2.x, OpenTSDB
[OK] Others: KaiwuDB, MongoDB, FTP, HDFS

[ALTERNATIVE] Alternative solutions:
1. If Redis data can be exported to CSV/JSON files, you can import using FTP/HDFS
2. First migrate Redis data to a supported database, then migrate to KaiwuDB

Would you like to know the specific operation method?
````

---

## Scenario 5: Ambiguous Request Clarification

### User Request
````
I want to migrate my data to KaiwuDB
````

### Expected AI Agent Response
````
Okay! Please tell me the following information first:

1. What is the source database type?
   - MySQL / Oracle / PostgreSQL / SQL Server / ClickHouse
   - TDengine / InfluxDB / OpenTSDB (time series databases)
   - MongoDB / FTP / HDFS

2. What engine does the target KaiwuDB use?
   - RELATIONAL (relational)
   - TIMESERIES (time series)

3. What is the KDTS server address? (Default http://127.0.0.1:8989)

After providing this information, I will guide you through the complete migration process.
````

---

## Scenario 6: Configuration Query

### User Request
````
How should I configure the KDTS service address?
````

### Expected AI Agent Response
````
KDTS server address supports multiple configuration methods (in priority order):

### Method 1: Environment Variables (Recommended for CI/CD)
```bash
# Method A: Full address
export KDTS_BASE_URL="http://your-kdts-server.com:8989"

# Method B: Configure host and port separately
export KDTS_HOST="your-kdts-server.com"
export KDTS_PORT="8989"
```

### Method 2: Configuration File (kdts_config.json)
Create a configuration file in the project root:
```json
{
  "base_url": "http://your-kdts-server.com:8989",
  "api_prefix": "/kdts/api/v1",
  "timeout": 30
}
```

### Method 3: Default Value
If not configured, the default address will be used: http://127.0.0.1:8989

### Current Configuration Check
Do you need me to check your current KDTS configuration?

[TIP] Note: When you start migration, if I find the KDTS address is unavailable, I will proactively ask you.
````

---

## Scenario 7: Migration Status Check

### User Request
````
I previously started a migration task, help me check if it's completed?
````

### Expected AI Agent Response
````
Okay, please provide the migration task name, for example:
- MYSQL2KAIWUDB_1720000000000
- INFLUXDB2X2KAIWUDB_1720000000000

If you don't remember the task name, you can provide:
1. KDTS server address
2. Migration time range (e.g., migration at 10 AM today)

I can help you query the recent migration task status.
````

**User Response**
````
Task name is MYSQL2KAIWUDB_1720000000000
KDTS at http://192.168.1.100:8989
````

**Expected AI Agent Response**
````
[INFO] Querying task status...

[System Internal Call]
1. KDTSClient.query_status(script_name)

[INFO] Task status: [OK] Completed
   
   Task name: MYSQL2KAIWUDB_1720000000000
   Status: SUCCEEDED
   Start time: 2024-03-15 10:23:45
   End time: 2024-03-15 10:24:30
   Time taken: 45 seconds

[INFO] Migration details:
   Total tables: 6
   Total rows: 65,114
   Error rows: 0

[OK] Migration task completed successfully!
````

---

## Scenario 8: InfluxDB 2.x Complex Migration with Boundary Conditions

### User Request
````
I have a complex InfluxDB 2.x database migration requirement:
- bucket: production_metrics (contains 50 measurements, over 100 million records)
- Need to preserve original tag and field structure
- Target KaiwuDB time series database name: metrics_archive
- Migration time range: 2024-01-01 to 2024-12-31
````

### Expected AI Agent Response

**Step 1: Recognize Complex Migration Need**
````
[OK] Complex migration requirement recognized: InfluxDB 2.x (production_metrics) -> KaiwuDB (TIMESERIES)

[WARNING] Detected high complexity migration scenario:
  - Number of measurements: 50
  - Estimated data volume: > 100 million records
  - Time span: 1 year
  - Involves multi-tenant/multi-region tags

[INFO] Recommended migration strategy:
  1. Batch migration (by time month or by measurement)
  2. Increase concurrency (recommended 8-16 channels)
  3. Use batch submission mode (batch_size: 10000)

Please confirm the following migration configuration:

KDTS server address (default: http://127.0.0.1:8989):
InfluxDB 2.x connection info:
  - Host/Port:
  - Organization:
  - Token (or Username/Password):
  - Bucket: production_metrics
KaiwuDB connection info (engine: TIMESERIES):
  - Host/Port (default 127.0.0.1:26257):
  - Username/Password:
  - Target Database: metrics_archive
Migration parameters:
  - Time range: 2024-01-01 ~ 2024-12-31
  - Batch strategy (by month/by measurement):
  - Concurrency (default 8):
  - Include all tags/fields (default: Yes):

[IMPORTANT] Security reminders:
  - Please back up the source bucket before migration!
  - Large data migration is recommended during business off-peak hours
  - Migration may take several hours to complete
````

**User Response**
````
KDTS: http://10.0.0.100:8989
InfluxDB: 192.168.1.60:8086, org=myorg, token=secret-token, bucket=production_metrics
KaiwuDB: 127.0.0.1:26257, user=root, password=kwdb, db=metrics_archive
Time range: 2024-01-01 ~ 2024-12-31
Batch strategy: By month
Concurrency: 16
Include all tags/fields: Yes
````

**Step 2: Validate and Plan Migration**
````
[INFO] Validating connection...
  [OK] InfluxDB 2.x connection successful
  [OK] KaiwuDB connection successful

[INFO] Analyzing source bucket structure...
  Measurements (50):
    - cpu_usage: tags(host, region, pod), fields(usage, temperature, load)
    - memory_usage: tags(host, region, pod), fields(used, free, swap)
    - network_io: tags(host, region, interface), fields(rx_bytes, tx_bytes, errors)
    - ... (47 more measurements)
  
  Data statistics:
    - Total records: 127,345,678
    - Average records/second: ~4000 (peak ~15000)
    - Estimated migration time: 3-5 hours

[WARNING] Boundary condition detection:
  [WARNING] Some measurements have dynamic tags (e.g., request_id, trace_id)
  [INFO] Recommendation: Convert dynamic tags to FIELD or create indexes
  [INFO] Auto-handling: Will be kept as TAG but limit unique value count

[INFO] Generating migration plan (batch by month):
  Batch 1: 2024-01 (10,612,140 records)
  Batch 2: 2024-02 (9,318,752 records)
  ...
  Batch 12: 2024-12 (11,234,567 records)

[IMPORTANT] Final confirmation before migration:
  - Skip empty measurements? (default: No)
  - Ignore error records? (default: Yes, error rate < 0.1%)
  - Auto-retry failed batches? (default: Yes, up to 3 times)

Start executing migration plan? (yes/no)
````

**User Response**
````
Confirm to start, skip empty measurements, ignore errors, auto-retry
````

**Step 3: Execute Migration - Schema Phase**
````
[INFO] Step 1/2: Schema Migration (all measurements)...

[INFO] Generating DDL (50 measurements):
  [INFO] cpu_usage -> CREATE TABLE cpu_usage (...)
  [INFO] memory_usage -> CREATE TABLE memory_usage (...)
  [INFO] network_io -> CREATE TABLE network_io (...)
  ...
  
[WARNING] DDL preview (cpu_usage example):
  CREATE TABLE cpu_usage (
    time TIMESTAMP,
    host VARCHAR(255) PRIMARY TAG,
    region VARCHAR(100) TAG,
    pod VARCHAR(255) TAG,
    usage DOUBLE FIELD,
    temperature DOUBLE FIELD,
    load DOUBLE FIELD
  );

[WARNING] About to create 50 time series tables
[WARNING] Estimated storage: 127M records x ~200 bytes = 24 GB

Confirm DDL execution? (yes/no)
````

**User Response**
````
yes
````

**Step 4: Execute Migration - Data Phase**
````
[OK] DDL execution successful! Tables created: 50

[INFO] Step 2/2: Data Migration (12 batches)...

[INFO] Batch 1/12: 2024-01 (10,612,140 records)
  [INFO] Progress: 25% (2,653,035 records) - 180MB/min
  [INFO] Progress: 50% (5,306,070 records) - 185MB/min
  [INFO] Progress: 75% (7,959,105 records) - 190MB/min
  [INFO] Progress: 100% (10,612,140 records) - Completed!
  [OK] Batch 1 successful! Time taken: 55 minutes

[INFO] Batch 2/12: 2024-02 (9,318,752 records)
  ...
  [OK] Batch 2 successful! Time taken: 48 minutes

... (intermediate batches omitted)

[INFO] Batch 12/12: 2024-12 (11,234,567 records)
  ...
  [OK] Batch 12 successful! Time taken: 62 minutes

[OK] All batch migrations completed!
  Total time taken: 7 hours 15 minutes
  Average speed: 250 MB/min

[INFO] Error handling statistics:
  Error records: 12,345 (0.0097%)
  Auto-retry successful: 12,100
  Skipped records: 245 (logged to error.log)

[REPORT] Migration report:
  [OK] Schema migration: Success (50 tables)
  [OK] Data migration: Success (127,333,333 records)
  [INFO] Error records: 245 (logged)

[IMPORTANT] Verification recommendations:
  1. Check if the record count of each measurement matches
  2. Verify data type conversion is correct
  3. Sample check tag/field values
  4. Run key queries to verify performance

Migration successful? It is recommended to run verification script to confirm before deleting source data.
````

---

## Scenario 9: MySQL to KaiwuDB (TIMESERIES) - Tag Selection

### User Request
````
I have a MySQL table sensor_data that stores IoT sensor readings:
- id (BIGINT, PK)
- device_id (VARCHAR(50))
- location (VARCHAR(100))
- sensor_type (VARCHAR(30))
- reading_time (DATETIME)
- temperature (DECIMAL(10,2))
- humidity (DECIMAL(10,2))

I want to migrate this to KaiwuDB as a time series table so I can perform time-series queries.
````

### Expected AI Agent Response

**Step 1: Analyze and Offer Tag Configuration**
````
[OK] MySQL -> KaiwuDB (TIMESERIES) migration recognized

[INFO] Analyzing source table structure...
Table: sensor_data (7 columns)
- id (BIGINT, PK)
- device_id (VARCHAR(50))
- location (VARCHAR(100))
- sensor_type (VARCHAR(30))
- reading_time (DATETIME)
- temperature (DECIMAL(10,2))
- humidity (DECIMAL(10,2))

[INFO] For time series tables, you need to select tags and value fields:

[WARNING] TIMESERIES Table Requirements:
- Must have at least 1 PRIMARY TAG (max 4)
- Can have SECONDARY TAGS (optional)
- Remaining columns become VALUE FIELDS
- reading_time is auto-selected as TIME column (required)

Please configure tags for sensor_data table:

PRIMARY TAG Selection (1-4 required, max 4):
[ ] id (BIGINT)
[ ] device_id (VARCHAR(50))
[ ] location (VARCHAR(100))
[ ] sensor_type (VARCHAR(30))

[INFO] Tip: Primary tags are used for indexing and filtering
[INFO] Recommended: device_id, location, sensor_type (common filter columns)

SECONDARY TAG Selection (optional, max 128 total tags):
[ ] id (BIGINT)
[ ] device_id (VARCHAR(50))
[ ] location (VARCHAR(100))
[ ] sensor_type (VARCHAR(30))
````

**User Response**
````
PRIMARY TAGS: device_id, location, sensor_type (3 selected)
SECONDARY TAGS: (none)
````

**Step 2: Show DDL Preview with Tag Configuration**
````
[INFO] Generating DDL with your tag configuration...

[SUCCESS] Tag configuration saved:
- PRIMARY TAGS (3): device_id, location, sensor_type
- SECONDARY TAGS: None
- VALUE FIELDS: id, temperature, humidity
- TIME COLUMN: reading_time

[WARNING] DDL Preview:
```sql
CREATE TABLE sensor_data
(
    reading_time TIMESTAMPTZ NOT NULL,
    id BIGINT,
    temperature DECIMAL(10,2),
    humidity DECIMAL(10,2)
)
TAGS
(
    device_id VARCHAR(50) NOT NULL,
    location VARCHAR(100) NOT NULL,
    sensor_type VARCHAR(30) NOT NULL
)
PRIMARY TAGS (device_id, location, sensor_type);
```

[INFO] Statistics:
- Total columns: 4 value + 3 tags = 7
- Primary tags: 3 (limit: 4)
- Estimated DDL size: ~1.5KB

Confirm to execute this DDL? (yes/no)
````

**User Response**
````
yes
````

**Step 3: Execute and Show Result**
````
[INFO] Executing DDL...

[System Internal Call]
1. KDTSClient.execute_ddl(target_config, ddl)

[SUCCESS] DDL executed successfully!
  Table created: sensor_data
  Time taken: 0.15 seconds

[INFO] Next step: Configure DataX for data migration
  Would you like to use default or custom configuration?
````

---

## Scenario 10: InfluxDB 1.x to KaiwuDB (TIMESERIES) - Auto Tag Mapping

### User Request
````
I need to migrate an InfluxDB 1.x database to KaiwuDB TIMESERIES:
- Database: metrics
- Has measurements with various tags (some have 5+ tags)
- Want to preserve all data

Check if migration is possible and handle any tag issues.
````

### Expected AI Agent Response

**Step 1: Analyze InfluxDB Structure**
````
[OK] InfluxDB 1.x -> KaiwuDB (TIMESERIES) migration recognized

[INFO] Note: InfluxDB time series sources can ONLY migrate to KaiwuDB TIMESERIES
  (Not compatible with RELATIONAL engine - this is enforced by KDTS)

[INFO] Analyzing source database structure...

[System Internal Call]
1. KDTSClient.read_metadata(source_config)

[INFO] Found 5 measurements:
- cpu_usage: tags(host, region, datacenter, service, priority), fields(usage, temperature)
- memory_usage: tags(host, region), fields(used, free)
- disk_io: tags(host, device, region), fields(read_bytes, write_bytes)
- network: tags(host, interface, region, datacenter), fields(rx, tx)
- request_log: tags(service, endpoint, method, status_code, region, datacenter), fields(latency)

[WARNING] Tag Overflow Detection:
- cpu_usage: 5 tags (exceeds PRIMARY limit of 4)
- request_log: 6 tags (exceeds PRIMARY limit of 4)

[INFO] KDTS Auto-Mapping Rules:
- First 4 tags -> PRIMARY TAGS
- Remaining tags -> SECONDARY TAGS

Example auto-mapping for cpu_usage:
- PRIMARY TAGS: host, region, datacenter, service
- SECONDARY TAGS: priority
- VALUE FIELDS: usage, temperature

Example auto-mapping for request_log:
- PRIMARY TAGS: service, endpoint, method, status_code
- SECONDARY TAGS: region, datacenter
- VALUE FIELDS: latency

Would you like to use this auto-mapping or manually adjust?
````

**User Response**
````
Use auto-mapping, it looks good
````

**Step 2: Preview DDL**
````
[INFO] Generating DDL with auto-mapped tags...

[WARNING] DDL Preview (2 of 5 measurements):

```sql
-- cpu_usage (5 tags -> 4 PRIMARY + 1 secondary)
CREATE TABLE cpu_usage
(
    time TIMESTAMPTZ NOT NULL,
    usage DOUBLE,
    temperature DOUBLE
)
TAGS
(
    host VARCHAR(100) NOT NULL,
    region VARCHAR(50) NOT NULL,
    datacenter VARCHAR(50) NOT NULL,
    service VARCHAR(100) NOT NULL,
    priority VARCHAR(20)
)
PRIMARY TAGS (host, region, datacenter, service);

-- request_log (6 tags -> 4 PRIMARY + 2 secondary)
CREATE TABLE request_log
(
    time TIMESTAMPTZ NOT NULL,
    latency DOUBLE
)
TAGS
(
    service VARCHAR(100) NOT NULL,
    endpoint VARCHAR(200) NOT NULL,
    method VARCHAR(10) NOT NULL,
    status_code INT NOT NULL,
    region VARCHAR(50),
    datacenter VARCHAR(50)
)
PRIMARY TAGS (service, endpoint, method, status_code);
```

[INFO] Total tables to create: 5
- 2 tables with auto-adjusted tags (max 4 PRIMARY TAGS)
- 3 tables with standard PRIMARY TAGS (<= 4 tags)

Confirm to execute DDL for all 5 tables? (yes/no)
````

**User Response**
````
yes
````

**Step 3: Execute and Continue**
````
[INFO] Executing DDL for 5 tables...

[System Internal Call]
1. KDTSClient.execute_ddl(target_config, ddl_batch)

[SUCCESS] All 5 tables created successfully!
  - cpu_usage (with SECONDARY TAG: priority)
  - memory_usage
  - disk_io
  - network (with SECONDARY TAGS: datacenter)
  - request_log (with SECONDARY TAGS: region, datacenter)

[INFO] Ready for data migration...

IMPORTANT: KaiwuDB tables created with:
- PRIMARY TAGS: Used for efficient indexing and filtering
- SECONDARY TAGS: Indexed but less frequently queried
- VALUE FIELDS: Measured data values

Next: Configure DataX parameters for data migration
````

---

## Scenario 11: Oracle to KaiwuDB (TIMESERIES) - Adding a t1 Primary Tag Column

### User Request

```
Migrate the Oracle oracle_kwdb database to a KaiwuDB time-series database
(target database: oracle_kwdb). Oracle has no time-series column — add a new
column t1 as the time-series primary tag with default value 1.
Oracle connection: ORACLE_KWDB/123456 @ 127.0.0.1:1521 (SID: ORCL)
```

### Expected AI Agent Response

````
[INFO] Migration intent recognized: Oracle -> KaiwuDB (TIMESERIES), database oracle_kwdb
[INFO] Oracle note: source dbName must be the owner name (ORACLE_KWDB, UPPERCASE)

[OK] Connection tests passed (Oracle + KaiwuDB)

[INFO] Oracle metadata read: table TEST_TB, 13 columns (TS, C1-C12)
[INFO] Oracle table/column names are UPPERCASE

[INFO] Adding new t1 primary tag column (not present in Oracle):
  Use build_added_column('t1', 1, source_type='ORACLE', is_tag=True, is_primary_tag=True)
  - int default 1 → INT4 (eligible for primary tag, auto NOT NULL)
  - sourceColumnType = NUMBER(10,0) (exact mapping to INT4, avoids FLOAT fallback)

[WARNING] DDL preview:
CREATE TS DATABASE "oracle_kwdb";
CREATE TABLE "oracle_kwdb"."TEST_TB" (
    "TS" TIMESTAMPTZ NOT NULL,
    "C1" INT2, "C2" INT4, "C3" INT8, "C4" FLOAT4, "C5" FLOAT4,
    "C6" VARCHAR(5), "C7" CHAR(1), "C8" NCHAR(10),
    "C9" VARCHAR(10), "C10" NVARCHAR(10), "C11" VARBYTES, "C12" TIMESTAMPTZ
) TAGS ("t1" INT4 NOT NULL) PRIMARY TAGS ("t1");
Execute this DDL? (yes/no)

User: yes

[OK] DDL executed successfully

[INFO] Building migration script (explicit table mapping):
  Source columns: TS,C1,...,C12,1 as t1 (SQL expression generates default 1)
  Target columns: TS,C1,...,C12,t1 (real column names via target_columns)
[OK] Migration launched: ORACLE2KAIWUDB_xxx.json

[REPORT] Migration completed: SUCCEEDED
[TIP] Compare source/target row counts to verify data integrity
````

---

## Scenario 12: MongoDB to KaiwuDB (TIMESERIES) - SKILL-Generated DDL + query Filter

### User Request

```
Migrate the MongoDB mongo_kwdb database to a KaiwuDB time-series database
(target database: mongo_kwdb). collectionName: test_tb; 14 columns
(ts date, c1-c2 int, c3 long, c4-c5 double, c6 bool, c7-c10 string, c11 bytes,
c12 date, t1 int); query filter: {"t1":{"$gte":1,"$lt":8}}.
Address: 127.0.0.1:27017, root/123456
```

### Expected AI Agent Response

````
[INFO] Migration intent recognized: MongoDB -> KaiwuDB (TIMESERIES), database mongo_kwdb
[INFO] MongoDB note: KDTS does NOT support MongoDB type mapping; table creation is
      limited to two options (① pre-create the table, ② SKILL generates DDL from the user-provided table info)

[OK] Connection tests passed (MongoDB + KaiwuDB)

[INFO] Generating DDL from user-provided table info + type mapping
      (int→INT4, long→INT8, double→FLOAT8, string→VARCHAR, bytes→VARBYTES, date→TIMESTAMP, bool→BOOL)

[WARNING] DDL preview:
CREATE TS DATABASE "mongo_kwdb";
CREATE TABLE "mongo_kwdb"."test_tb" (
    "ts" TIMESTAMPTZ NOT NULL, "c1" INT4, "c2" INT4, "c3" INT8,
    "c4" FLOAT8, "c5" FLOAT8, "c6" BOOL,
    "c7" VARCHAR, "c8" VARCHAR, "c9" VARCHAR, "c10" VARCHAR,
    "c11" VARBYTES, "c12" TIMESTAMP
) TAGS ("t1" INT4 NOT NULL) PRIMARY TAGS ("t1");
Execute this DDL? (yes/no)

User: yes

[OK] DDL executed successfully

[INFO] Building migration script: collectionName=test_tb + column JSON +
      query={"t1":{"$gte":1,"$lt":8}}
[OK] Migration launched: MONGODB2KAIWUDB_xxx.json

[REPORT] Migration completed: SUCCEEDED
[TIP] Due to the query filter, the target only contains documents with t1=1~7;
      verify by comparing counts
````

---

## Scenario 13: SQL Server to KaiwuDB (TIMESERIES) - schemaName Fix + t1 Primary Tag

### User Request

```
Migrate the SQL Server sqlserver_kwdb database to a KaiwuDB time-series database
(target database: sqlserver_kwdb). Connection: sa/Password@2024 @ 127.0.0.1:1433
(URL with encrypt=true;trustServerCertificate=true). Add 1 as t1 as the primary tag.
```

### Expected AI Agent Response

````
[INFO] Migration intent recognized: SQL Server -> KaiwuDB (TIMESERIES), database sqlserver_kwdb
[INFO] SQL Server note: URL needs encrypt=true;trustServerCertificate=true; two-step migration

[OK] Connection tests passed (SQL Server + KaiwuDB)

[INFO] Metadata read: table test_tb, 13 columns
[INFO] schemaName fix: metadata schemaName=sqlserver_kwdb (database name) → public
      (avoids duplicated "db"."db"."table" in the DDL)

[INFO] Adding new t1 primary tag column (1 as t1 expression):
  build_added_column('t1', 1, source_type='SQLSERVER', is_tag=True, is_primary_tag=True)
  → INT4, auto NOT NULL

[WARNING] DDL preview:
CREATE TS DATABASE "sqlserver_kwdb";
CREATE TABLE "sqlserver_kwdb"."public"."test_tb" (
    "ts" TIMESTAMPTZ NOT NULL, "c1" INT2, "c2" INT4, "c3" INT8,
    "c4" FLOAT4, "c5" FLOAT4, "c6" BOOL,
    "c7" CHAR(1), "c8" NCHAR(20), "c9" VARCHAR(10), "c10" NVARCHAR(20),
    "c11" VARBYTES, "c12" TIMESTAMPTZ
) TAGS ("t1" INT4 NOT NULL) PRIMARY TAGS ("t1");
Execute this DDL? (yes/no)

User: yes

[OK] DDL executed successfully

[INFO] Building migration script: source columns ts,c1,...,c12,1 as t1; target
      columns ts,c1,...,c12,t1 (target_columns)
[OK] Migration launched: SQLSERVER2KAIWUDB_xxx.json

[REPORT] Migration completed: SUCCEEDED
[TIP] Compare source/target row counts and spot-check the t1 default value
````

---

## Summary

These interaction scenarios validate that the AI Agent:

1. [OK] Correctly identifies migration intent from natural language
2. [OK] Asks for all necessary parameters in a structured way
3. [OK] Provides clear explanations for special cases (e.g., InfluxDB two-step migration)
4. [OK] Validates parameters before proceeding
5. [OK] Handles errors gracefully with helpful suggestions
6. [OK] Provides progress updates in real-time
7. [OK] Generates comprehensive migration reports
8. [OK] Supports status queries for previous migrations
9. [OK] Can clarify ambiguous requests
10. [OK] Handles complex scenarios (batch processing, large datasets)
11. [OK] Provides optimization suggestions for high-volume migrations
12. [OK] Manages boundary conditions and edge cases

These scenarios can be used for:
- Manual testing of the AI Agent
- Training new team members
- Validating SKILL updates
- Creating integration test cases

---

## Key to Tags

| Tag           | Meaning                                                     |
|---------------|-------------------------------------------------------------|
| [OK]          | Operation completed successfully                            |
| [INFO]        | Providing information or progress updates                   |
| [WARNING]     | Requires user attention or has potential risks              |
| [ERROR]       | An error occurred that needs handling                       |
| [TIP]         | Providing suggestions or best practices                     |
| [IMPORTANT]   | Critical security or configuration information              |
| [REPORT]      | Migration results or statistics report                      |
| [ALTERNATIVE] | Alternative solution when the primary option is unavailable |
