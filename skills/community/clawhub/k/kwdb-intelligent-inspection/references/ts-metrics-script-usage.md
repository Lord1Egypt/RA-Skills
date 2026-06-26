## Time Series Metrics Script Usage

Use `scripts/get_kwdb_ts_metrics.py` to collect time series metrics from KaiwuDB.

### Full Collection (all metrics)

```bash
python3 scripts/get_kwdb_ts_metrics.py --host <host> [--port <port>]
```

### Partial Collection (specific metrics)

```bash
python3 scripts/get_kwdb_ts_metrics.py --host <host> --metric <metric_name> [--metric <metric_name> ...]
```

Example:
```bash
python3 scripts/get_kwdb_ts_metrics.py --host 10.110.10.146 --metric sys.cpu.user.percent --metric sql.insert.count
```

### Options

| Option | Default | Description |
|--------|---------|-------------|
| `--host` | localhost | KaiwuDB admin host |
| `--port` | 8080 | KaiwuDB admin port |
| `--start` | 1 hour ago | Start time (unix timestamp in ns) |
| `--end` | now | End time (unix timestamp in ns) |
| `--sample` | 60 | Sample interval in seconds |
| `--metric` | all | Filter by metric name (can repeat) |
| `--json` | false | Output raw JSON |

### Available Metrics

See `references/metric-types.md` for the complete list of available metrics.
