# Error Code Reference

Complete error code reference for KDTS migration. Includes causes, symptoms, and fix suggestions.

## Error Code Ranges

| Range     | Category   | Description                                |
|-----------|------------|--------------------------------------------|
| 1001-1005 | Parameter  | Invalid or missing request parameters      |
| 2001      | Connection | Database connection failures               |
| 3001-3006 | Metadata   | Source metadata reading and DDL generation |
| 4001-4003 | DataX      | Migration script building and execution    |
| 5001-5002 | Resource   | System resource availability               |
| 9999      | System     | Unexpected internal errors                 |

---

## Parameter Errors (1xxx)

### 1001 - PARAM_INVALID

**Title**: Invalid Request Parameters

**Symptoms**: API returns with `code: 1001`

**Common Causes**:

- Missing required field (`engine`, `type`, `host`, `port`, `username`, `password`)
- Incorrect field type (string vs number)
- Invalid enum value for `engine` (must be `RELATIONAL` or `TIMESERIES`)
- Invalid enum value for `type`

**Required Fields**:

For ALL DataSource configurations (source and target):

1. `engine`: **REQUIRED** - Must be `RELATIONAL` or `TIMESERIES`
   - Use `RELATIONAL` for: MYSQL, ORACLE, POSTGRESQL, SQLSERVER, CLICKHOUSE
   - Use `TIMESERIES` for: KAIWUDB, TDENGINE2X/3X, INFLUXDB1X/2X, OPENTSDB, MONGODB, FTP, HDFS
2. `type`: **REQUIRED** - One of 14 supported types
3. `host`: **REQUIRED** - Database hostname or IP
4. `port`: **REQUIRED** - Database port number (integer)
5. `username`: **REQUIRED** - Database username
6. `password`: **REQUIRED** - Database password
7. `dbName`: **CONDITIONAL** - Required for most source types

**Checks**:

1. Verify all required fields present: `engine`, `type`, `host`, `port`, `username`, `password`
2. Check `port` is an integer, not string
3. Ensure `type` is uppercase: `MYSQL` not `mysql`
4. Verify `engine` is `RELATIONAL` or `TIMESERIES`

**Correct Example**:

```json
{
  "engine": "RELATIONAL",
  "type": "MYSQL",
  "host": "127.0.0.1",
  "port": 3306,
  "username": "root",
  "password": "secret",
  "dbName": "source_db"
}
```

**Incorrect Example** (missing engine):

```json
{
  "type": "MYSQL",
  "host": "127.0.0.1",
  "port": 3306,
  "username": "root",
  "password": "secret"
}
```

**Fix**: Add the missing `engine` field with correct value.

---

### 1002 - PARAM_SOURCE_TYPE_INVALID

**Title**: Unsupported Source Type

**Symptoms**: API rejects source type with code 1002

**Common Causes**:

- Typo in source type name
- Using non-existent source type
- Copy-paste error from documentation

**Supported Types** (exact match required):

```
MYSQL, ORACLE, POSTGRESQL, SQLSERVER, CLICKHOUSE, 
KAIWUDB, TDENGINE2X, TDENGINE3X, INFLUXDB1X, INFLUXDB2X, 
OPENTSDB, MONGODB, FTP, HDFS
```

**Fix**: Correct the `type` field to one of the supported types.

---

### 1003 - PARAM_TARGET_TYPE_INVALID

**Title**: Invalid Target Type

**Symptoms**: API rejects target configuration

**Cause**: Target `type` is not `KAIWUDB`

**Fix**:

```json
{
  "target": {
    "type": "KAIWUDB",
    "engine": "RELATIONAL"
  }
}
```

---

### 1004 - PARAM_TABLE_MAPPING_MISMATCH

**Title**: Table Mapping Error

**Symptoms**: Build API rejects with mapping error

**Common Causes**:

- `tables` array has items without both `source` and `target`
- `source.sourceType` not specified
- `target.sourceType` not `KAIWUDB`

**Correct Format**:

```json
{
  "tables": [
    {
      "source": {
        "sourceType": "RDBMS",
        "table": "t1",
        "column": "*"
      },
      "target": {
        "sourceType": "KAIWUDB",
        "table": "t1",
        "column": "*",
        "writeMode": "insert"
      }
    }
  ]
}
```

---

### 1005 - JSON_PARSE_ERROR

**Title**: JSON Parse Error

**Symptoms**: Request cannot be parsed as JSON

**Common Causes**:

- Trailing comma in JSON
- Single quotes instead of double quotes
- Control characters in strings
- Comments in JSON

**JSON Validation Tips**:

1. Use JSON validator: `jsonlint file.json` or online tool
2. No trailing commas
3. All keys and strings use double quotes
4. No comments

---

## Connection Errors (2xxx)

### 2001 - CONNECTION_FAILED

**Title**: Database Connection Failed

**Symptoms**: API returns code 2001 with message containing connection details

**Diagnostic Steps**:

1. **Check database service**:
   - MySQL: `mysqladmin ping -h host -P port -u user -p`
   - PostgreSQL: `pg_isready -h host -p port`
   - Generic TCP: `telnet host port` / `nc -zv host port`

2. **Verify credentials**:
   - Try connecting manually: `mysql -h host -P port -u user -p`

3. **Check network/firewall**:

   - KDTS server can reach database host?
   - Port not blocked by firewall/security group?
   - VPN required for remote databases?

4. **Database-specific checks**:

   - MySQL: user permission, host allow list
   - Oracle: TNS listener running, service name correct
   - PostgreSQL: `pg_hba.conf` allows connections

**Common Connection String Patterns**:

```
MySQL:      jdbc:mysql://host:3306/dbname
Oracle:     jdbc:oracle:thin:@host:1521:ORCL
PostgreSQL: jdbc:postgresql://host:5432/dbname
KaiwuDB:    jdbc:mysql://host:9092/dbname (MySQL protocol compatibility)
```

---

## Metadata Errors (3xxx)

### 3001 - METADATA_PARSE_FAILED

**Title**: Metadata Reading Failed

**Symptoms**: `/datasource/metadata` returns code 3001

**Common Causes**:

- Source does not support metadata (e.g., TDENGINE2X, OPENTSDB, MONGODB, FTP, HDFS)
- Database user lacks metadata privileges
- Source is corrupted or incompatible version

**Note**: INFLUXDB 1.x and 2.x support metadata reading (META_AND_DATA capability), but not full migration.

**Check**:

1. Verify source supports metadata: See `references/source-types.md`
2. Check user has privileges: SELECT on INFORMATION_SCHEMA / system tables
3. Test with simpler tables first

---

### 3002 - METADATA_DDL_BUILD_FAILED

**Title**: DDL Generation Failed

**Symptoms**: `/metadata/preview` returns code 3002

**Common Causes**:

- Unsupported column type in source
- Complex constraint (check constraint, trigger)
- Type mapping not available

**Workaround**:

1. Manually create DDL in KaiwuDB
2. Use data-only migration (skip DDL)
3. Filter problematic columns with `column` field

---

### 3003 - METADATA_EXECUTE_FAILED

**Title**: DDL Execution Failed

**Symptoms**: `/metadata/execute` returns code 3003

**Common Causes**:

- Table already exists with different structure
- Insufficient privileges on target
- Invalid KaiwuDB syntax (version mismatch)

**Check**:

1. `SHOW TABLES` on target - drop conflicting tables if safe
2. Verify user has CREATE, ALTER privileges
3. Check KaiwuDB version compatibility

---

### 3004 - METADATA_TAG_LIMIT_EXCEEDED

**Title**: Tag Column Limit Exceeded

**Symptoms**: Time-series migration fails with tag limit error

**Rule**: KaiwuDB time-series tables have:

- Max 128 columns total (Tag + Value)
- Max 4 primary tags

**Solutions**:

1. Reduce columns to ≤ 128
2. Split into multiple migrations
3. Convert primary tags to secondary tags if possible

---

### 3005 - METADATA_TAG_NAME_TOO_LONG

**Title**: Tag/Column Name Too Long

**Rule**: KaiwuDB column names ≤ 128 bytes

**Solutions**:

1. Shorten source column names
2. Use column alias mapping in migration config
3. Consider ASCII-only names for multi-byte characters

---

### 3006 - METADATA_NO_PRIMARY_TAG

**Title**: No Valid Primary Tag

**Symptoms**: Time-series migration cannot identify primary tag

**Cause**: No column suitable for primary key in source. Common reasons:
- All candidate columns are FLOAT/DOUBLE/DECIMAL/NUMERIC (classified as float, demoted)
- Selected primary tag columns are **nullable in the column definition** — KDTS demotes
  nullable primary tags to ordinary tags (3006 if none remain). Fix: set `nullAble=false`
  on the primary tag columns in the metadata (`mark_time_series_columns()` does this
  automatically), after confirming the source DATA has no NULL values

**Solutions**:

1. Identify unique, non-null column (device ID, sensor ID)
2. Add a primary key column to source
3. If source has auto-increment ID, use that
4. For nullable source columns: verify no NULLs in the data, then set `nullAble=false`
   (or pick a NOT NULL column / demote to ordinary tag)

**KaiwuDB Time Series Design**:

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

---

## DataX Errors (4xxx)

### 4001 - DATAX_BUILD_SCRIPT_FAILED

**Title**: Migration Script Build Failed

**Symptoms**: `/datax/build` returns code 4001

**Checklist**:

1. `target.sourceType` must be `KAIWUDB`
2. `source.sourceType` correct for source type
3. Table mapping has both `source` and `target` sections
4. Empty `tables` array is valid (auto-discovery)

**Debug**:

- Print the exact request body
- Check if DataX templates exist on KDTS server
- Try with single simple table first

---

### 4002 - DATAX_PROCESS_LAUNCH_FAILED

**Title**: DataX Process Cannot Start

**Symptoms**: `/datax/execute` returns code 4002

**Checklist**:

1. **Python 3 available?**
   - `which python3` / `python3 --version`

2. **DataX installed?**
   - `ls /opt/kdts/datax/` (or configured path); `cat /opt/kdts/datax/version.txt` (if exists)

3. **Permissions?**
   - Can the KDTS user execute DataX? `sudo -u kdts /opt/kdts/datax/bin/datax.py --help`

4. **KDTS config check**:
   - In `application.yml`: `datax.home.path` (e.g. `/opt/kdts/datax`) and
     `datax.python.path` (e.g. `/usr/bin/python3` if not default)

---

### 4003 - DATAX_PROCESS_TIMEOUT

**Title**: Migration Process Timeout

**Symptoms**: Migration killed after timeout; also returned when an HTTP request
(e.g. submitting MANY scripts in one `execute_migration`) exceeds the client read
timeout — the request may still have reached the server, which keeps processing.

**Default Timeout**: 3600 seconds (1 hour); client read timeout default 300s (KDTS_TIMEOUT)

**Solutions**:

1. **Use batch script execution** (common cause: submitting dozens of scripts at once):
   Use `workflow.execute_migration_batches(script_names, batch_size=10)` — submit 10 scripts
   per batch, wait for the batch to reach final states, then submit the next.
   A 4003 on submission means the request reached the server (it keeps processing) — still monitor.
   (Full code example: SKILL.md Workflow 1 step 11)

2. **Increase timeout**:
   - Server: `datax.timeout: 7200` in `application.yml` (2 hours)
   - Client: `KDTS_TIMEOUT=300` env var or `KDTSClient(timeout=...)`

3. **Optimize migration**:
   - Increase `data.fetchSize`/`data.batchSize` (e.g. 5000) and `setting.speed.channel` for more concurrency

4. **Reduce data volume**:

   - Add `where` clause to filter source
   - Migrate in batches by time range
   - Skip large tables initially

5. **Check performance**:

   - Source: slow queries? locks?
   - Network: bandwidth between source and target
   - Target: disk I/O, index overhead

---

## Resource Errors (5xxx)

### 5001 - RESOURCE_THREAD_POOL_FULL

**Title**: Service Thread Pool Exhausted

**HTTP Status**: 503 (with Retry-After header)

**Symptoms**: KDTS returns 503, cannot accept new requests

**Cause**: Too many concurrent migrations, thread pool saturated

**Actions**:

1. Wait for Retry-After seconds (typically 60)
2. Kill unnecessary running migrations
3. Reduce concurrent migration requests
4. Increase thread pool size in KDTS config

**Configuration**:

```yaml
# application.yml
server:
  tomcat:
    threads:
      max: 200  # Increase from default
```

---

### 5002 - RESOURCE_PYTHON_NOT_FOUND

**Title**: Python 3 Not Available

**Symptoms**: Any migration returns 5002

**Check and Fix**:

```bash
# Check if Python 3 installed
python3 --version  # Should show 3.x

# If not installed (Ubuntu/Debian)
sudo apt-get update && sudo apt-get install python3

# If not installed (CentOS/RHEL)
sudo yum install python3

# Install dependencies (optional)
pip3 install requests pymysql psycopg2
```

**Configure KDTS**:

```yaml
# application.yml
datax:
  python.path: /usr/bin/python3  # Full path
```

**Restart KDTS**:

```bash
# After any configuration change
sudo systemctl restart kdts  # or however KDTS is managed
```

---

## System Error (9xxx)

### 9999 - SYSTEM_INTERNAL_ERROR

**Title**: Unexpected Internal Error

**Symptoms**: Any operation returns code 9999

**Diagnostic Steps**:

1. **Check KDTS logs**:
   - `tail -f /var/log/kdts/app.log`;`grep "ERROR\|Exception" /var/log/kdts/app.log`

2. **Check KDTS version**:
   - `curl http://localhost:8989/kdts/info/version`

3. **Check system resources**:
   - `free -m` (memory) / `df -h` (disk space) / `top` (CPU)

4. **Restart KDTS** (if possible):
   - `sudo systemctl restart kdts`; or `sudo kill -9 $(pgrep -f kdts) && java -jar kdts-server.jar`

5. **Report issue** with:
    - KDTS version
    - Operating system
    - Full stack trace from logs
    - Steps to reproduce

---

## Error Resolution Flowchart

```
API Call Returns Error
        │
        ▼
   Is code = 0? ──── YES ────► Success!
        │
        NO
        │
        ▼
   Get error info from this doc
        │
        ▼
   Code category?
   ├── 1xxx (Parameter)
   │   → Check all required fields, types, enum values
   │
   ├── 2xxx (Connection)
   │   → Test connection manually, check network/firewall
   │
   ├── 3xxx (Metadata)
   │   → Check source support, privileges, schema compatibility
   │
   ├── 4xxx (DataX)
   │   → Check Python/DataX installation, optimize migration params
   │
   ├── 5xxx (Resource)
   │   → Wait, reduce concurrency, install dependencies
   │
   └── 9xxx (System)
       → Check logs, restart KDTS, report bug
        │
        ▼
   Apply fix suggestion
        │
        ▼
   Retry API call
        │
        ▼
   Still failing?
   ├── Try simpler case (single table, no DDL)
   ├── Contact KDTS support
   └── Use alternative migration method
```

---

## Common Error Scenarios

### Scenario 1: MySQL to KaiwuDB fails at build

**Error**: 4001 (BUILD_FAILED)

**Check**:

1. Is target `type: KAIWUDB`?
2. Is `sourceType` `RDBMS`?
3. Is the table accessible?

### Scenario 2: Oracle connection fails

**Error**: 2001 (CONNECTION_FAILED)

**Check**:

1. Is Oracle TNS listener running?
2. Correct service name (not SID)?
3. Username has CONNECT privilege?

### Scenario 3: Large table timeout

**Error**: 4003 (TIMEOUT)

**Fix**:

1. Increase `fetchSize` and `batchSize`
2. Add `where` clause to filter
3. Split into multiple migrations

### Scenario 4: Time-series tag limit

**Error**: 3004 (TAG_LIMIT_EXCEEDED)

**Fix**:

1. Identify which columns are truly tags vs values
2. Move tag data to value columns where possible
3. Use multiple target tables

---

## Get Help

If unable to resolve:

1. Collect full error details: code, message, stack trace
2. Collect KDTS version and configuration
3. Collect source/target database versions
4. Document exact steps to reproduce
5. Contact KDTS team or file issue in kw-datax-utils repo
