# Test Command Details

Detailed parameters and usage for each OBD test tool.

## MySQL Test

```bash
obd test mysqltest <deploy_name> --test-set <test_set> [options]
```

Runs mysqltest **functional** test cases against the cluster (not a performance benchmark).

### Common Options
- `--test-set <test_set>`: Test suite name (e.g., `basic`)
- `--test-dir <dir>`: Custom test directory

## Sysbench

```bash
obd test sysbench <deploy_name> --tenant=<tenant> --script-name=<script> [options]
```

OBD auto-installs `ob-sysbench` when online. Do NOT install via yum.

### Common Options
- `--tenant=<tenant>`: Target tenant name
- `--script-name=<script>`: Sysbench script (e.g., `oltp_read_write.lua`, `oltp_point_select.lua`, `oltp_insert.lua`)
- `--threads=<n>`: Number of threads
- `--time=<seconds>`: Test duration
- `--table-size=<n>`: Rows per table
- `--tables=<n>`: Number of tables

### Example
```bash
obd test sysbench test-cluster \
  --tenant=mysql \
  --script-name=oltp_read_write.lua \
  --threads=32 \
  --time=60
```

## TPC-H

```bash
obd test tpch <deploy_name> --tenant=<tenant> --remote-tbl-dir=<server_dir> [options]
```

OBD auto-installs `obtpch` when online. Do NOT install via yum.

### Common Options
- `--tenant=<tenant>`: Target tenant name
- `--remote-tbl-dir=<server_dir>`: **Required.** Directory on the server for TPC-H table files
- `--scale-factor=<n>`: Data scale factor (default 1)

### Example
```bash
obd test tpch test-cluster \
  --tenant=mysql \
  --remote-tbl-dir=/tmp/tpch \
  --scale-factor=1
```

## TPC-C

```bash
obd test tpcc <deploy_name> --tenant=<tenant> --warehouses=<n> --run-mins=<minutes> [options]
```

OBD auto-installs `obtpcc` when online. Do NOT install via yum. Java may need separate installation.

### Common Options
- `--tenant=<tenant>`: Target tenant name
- `--warehouses=<n>`: Number of warehouses
- `--run-mins=<minutes>`: Test duration in minutes (use `--run-mins`, NOT `--running-minutes`)
- `--threads=<n>`: Number of threads

### Example
```bash
obd test tpcc test-cluster \
  --tenant=mysql \
  --warehouses=10 \
  --run-mins=5
```

## Non-Interactive Execution

For CI/scripts, set auto-confirm before running tests:

```bash
obd env set IO_DEFAULT_CONFIRM 1
```

## Full Test Suite Guidance

When running a full test suite, do NOT abort on first failure. Run all test cases to completion, then produce a single test report with:
- Pass / Fail / Skip status for each test
- Brief notes on failures
- Performance metrics where applicable
