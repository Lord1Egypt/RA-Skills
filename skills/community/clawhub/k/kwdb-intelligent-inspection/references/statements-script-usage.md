## Slow Statements Script Usage

Use `scripts/get_kwdb_statements.py` to collect slow SQL statement statistics from KaiwuDB.

### Full Collection (all statements)

```bash
python3 scripts/get_kwdb_statements.py --host <host> [--port <port>]
```

### Filter by Minimum Latency

```bash
python3 scripts/get_kwdb_statements.py --host <host> --min-latency-ms <ms>
```

Example - get statements with service latency > 100ms:
```bash
python3 scripts/get_kwdb_statements.py --host 10.110.10.146 --min-latency-ms 100
```

### Sort by Different Metrics

```bash
python3 scripts/get_kwdb_statements.py --host <host> --sort-by <field>
```

Available sort fields:
- `service_lat` (default) - total service latency
- `run_lat` - execution latency
- `plan_lat` - planning latency
- `count` - number of executions

### Limit Results

```bash
python3 scripts/get_kwdb_statements.py --host <host> --limit <N>
```

### Options

| Option | Default | Description |
|--------|---------|-------------|
| `--host` | localhost | KaiwuDB admin host |
| `--port` | 8080 | KaiwuDB admin port |
| `--limit` | 10 | Number of statements to display |
| `--min-latency-ms` | 0 | Minimum service latency filter (ms) |
| `--sort-by` | service_lat | Sort field |
| `--json` | false | Output raw JSON |

### Output Format

The script outputs a formatted table with:
- **Query** - SQL statement text (truncated at 200 chars)
- **App** - Application name
- **User** - Database user
- **Database** - Database name
- **Count** - Execution count
- **Service/Run/Plan/Parse** - Latencies in ms
- **DistSQL** - Whether distributed SQL was used
- **Failed** - Whether any executions failed
- **Last Error** - Error message if failed

### Examples

```bash
# Get top 10 slowest statements (by service latency)
python3 scripts/get_kwdb_statements.py --host localhost --port 8080

# Filter statements with latency > 100ms
python3 scripts/get_kwdb_statements.py --host localhost --min-latency-ms 100

# Sort by run latency instead of service latency
python3 scripts/get_kwdb_statements.py --host localhost --sort-by run_lat

# Output raw JSON
python3 scripts/get_kwdb_statements.py --host localhost --json

# Limit to top 5
python3 scripts/get_kwdb_statements.py --host localhost --limit 5
```

### Underlying API

This script wraps the KaiwuDB Statements API at `http://<host>:8080/_status/statements`.

**Note:** TLS mode is not supported because the AdminUI login requires captcha verification that cannot be solved in non-interactive mode.
