---
name: pscale-metrics
description: Query PlanetScale historical and current branch metrics or produce engine-aware performance reports with pscale. Use when investigating workload, latency, errors, traffic control, query efficiency, query/table/tablet/tag time series, network, storage, CPU, memory, IOPS, replication, WAL, PgBouncer, pod health, or backup activity over time. Triggers on pscale metrics, PlanetScale metrics, performance report, historical metrics, current metrics, specialized metrics, query metrics, table metrics, tablet metrics, tag metrics, latency trend, storage utilization, CPU utilization, replication lag, WAL metrics, PgBouncer metrics.
---

# pscale metrics

Use PlanetScale's branch metrics service for read-only time-series, current-value, and curated performance reporting. Prefer `--format json` for structured automation or `--format csv` when every historical sample is needed for external analysis.

## Prerequisites

- Authenticate with `pscale auth check --format json`.
- Identify the exact organization, database, and branch.
- Pass `--org` explicitly rather than relying on the configured default organization.
- Confirm the time window before comparing or reporting values.

## Start with a curated report

```bash
# Engine-aware report for the last day
pscale metrics report <database> <branch> \
  --org <org> \
  --period 1d \
  --format json

# Explicit UTC range instead of a named period
pscale metrics report <database> <branch> \
  --org <org> \
  --from 2026-08-18T00:00:00Z \
  --to 2026-08-19T00:00:00Z \
  --format json
```

`report` detects the database engine and requests curated sections for MySQL, PostgreSQL, or Neki. Neki reports combine query workload/latency with shard and router resource series, storage, WAL/replication, locks, pod health, current capacity, and backup activity. PostgreSQL and Neki reports also include selected current-value sections such as connection and storage capacity. JSON returns one composite `MetricsReport` with target, engine, range, and section results. CSV emits one row per historical sample or current value, with the section and kind preserved.

Named report periods are `15m`, `1h`, `3h`, `6h`, `12h`, `1d`, `2d`, `7d`, and `8d`; the default is `1d`. Use `--steps <positive-count>` to request a particular historical resolution. Do not combine `--period` with `--from`/`--to`, and always pass both range endpoints together.

## Query selected historical metrics

```bash
# Workload and tail latency over the last hour
pscale metrics show <database> <branch> \
  --org <org> \
  --metric queries \
  --metric latency_p99 \
  --period 1h \
  --format json

# Export all returned samples for analysis
pscale metrics show <database> <branch> \
  --org <org> \
  --metric queries \
  --period 1h \
  --format csv
```

At least one `--metric` is required; repeat it or pass comma-separated names. When `--period` is omitted, `show` defaults to `12h`. Human output summarizes each series with latest/minimum/average/maximum values and a compact trend. JSON preserves the complete API response. CSV preserves each timestamped sample and its series labels.

Use optional filters only when the target is known: `--tablet-type`, `--keyspace`, `--shard`, `--role`, `--container`, `--pod`/`--pods`, `--query-id`, `--fingerprint`, `--budget-id`, `--rule-id`, or `--search`. Narrowing filters can legitimately produce an empty result; verify scope before interpreting emptiness as healthy behavior.

## Specialized metrics

Use the specialized commands when the investigation starts from an Insights query, table, tablet, or tag scope. They forward opaque selectors to the API, so use IDs exactly as returned by `pscale insights`, `pscale metrics`, or branch/tablet discovery commands.

```bash
# Query-pattern metrics; query IDs are fingerprint-keyspace selectors
pscale metrics queries <database> <branch> --org <org> \
  --metric latency_p99 \
  --query-id <fingerprint-keyspace> \
  --period 1h \
  --format json

# Table storage metrics (no filter flags; JSON preserves the untyped storage-metrics API response)
pscale metrics tables <database> <branch> --org <org> --format json

# Tablet metrics, including workflow-scoped VReplication lag
pscale metrics tablets <database> <branch> --org <org> \
  --metric vreplication_lag \
  --workflow <workflow-name> \
  --period 1h \
  --format json

# Query-tag metrics; repeat --tag-set for independent series
pscale metrics tags <database> <branch> --org <org> \
  --metric latency_p99 \
  --tag-set Busername=alice,Senv=production \
  --period 1h \
  --format json
```

For `queries`, `tablets`, and `tags`, at least one `--metric` is required; `tables` and `keyspace-tables` accept no local filter flags and preserve the untyped storage-metrics API response. `metrics queries` requires a query selector such as `--query-id`, or `--fingerprint` with `--keyspace`; query selectors are forwarded opaquely, so use exact IDs from current command output rather than short display IDs. `metrics tags` requires at least one `--tag-set`. Traffic Control filters such as `--budget-id` and `--rule-id` should come from the current branch. Workflow filtering is intended for VReplication lag and should use the workflow name visible on the branch.

## Query current values

```bash
pscale metrics instant <database> <branch> \
  --org <org> \
  --metric planetscale_volume_usage_percentage \
  --format json
```

Use `instant` for current metric values rather than a trend. It supports `--role`, `--shard`, `--container`, and `--pod` filters. JSON preserves the API response; CSV emits metric, label, dimensions, and raw value rows.

## Investigation workflow

1. Confirm organization, database, branch, engine, and incident window.
2. Run `metrics report` for an engine-aware baseline.
3. Use `metrics show` for the specific historical series and dimensions related to the symptom.
4. Use `metrics instant` only when current capacity or state matters.
5. Keep units, time range, sample interval, dimensions, and engine attached to every conclusion.
6. Correlate rather than infer causation from one metric: compare workload, latency, errors, resource utilization, and relevant traffic-control or replication signals.
7. Use `pscale insights` for query-fingerprint aggregates and samples, or `pscale inspect` for live connection-level diagnostics.

Metric labels and dimensions can include operational identifiers such as pod, shard, role, query pattern, budget, or rule IDs. Review before pasting raw output into public logs or issues.

## Output interpretation

- Human historical output converts recognized bytes, rates, percentages, durations, and seconds to readable units and summarizes the returned points.
- JSON is the authoritative structured response for automation and retains raw series data.
- CSV is best for charting or calculations because it emits individual samples/current values instead of the human summary.
- An empty series or current-value result is not proof that the database is healthy; verify metric name, engine applicability, dimensions, feature availability, and time range.
- Metrics commands are read-only. They do not resize resources, change traffic rules, or alter database configuration.

## Related skills

- **pscale-insights** — server-side query fingerprints, execution samples, errors, anomalies, tags, and schema recommendations
- **pscale-inspect** — point-in-time MySQL/Vitess, PostgreSQL, and Neki connection-target diagnostics
- **pscale-database** — database settings, throttler defaults, keyspaces, IP restrictions, and dumps
- **pscale-pgbouncer** — dedicated PostgreSQL PgBouncer lifecycle and sizing

See [references/commands.md](references/commands.md) for checksum-verified command help.
