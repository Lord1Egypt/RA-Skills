# `pscale inspect` command reference

Behavior was re-verified against the official, checksum-verified PlanetScale CLI v0.337.0 macOS arm64 release binary (archive SHA-256 `4660b4606d0232076b7e54166d15e68e3030d59c2ae22b8b1c47677e506521d7`). The compact fences below are curated usage excerpts, not byte-for-byte help captures.

## Command group

```text
pscale inspect [command]

Available Commands:
  all                  Run every applicable check and print a combined report
  bloat                Wasted space: estimated bloat (PostgreSQL) or fragmentation (MySQL)
  calls                Most frequently called queries (needs pg_stat_statements)
  index-sizes          Indexes by size, largest first
  invalid-indexes      Invalid indexes left over from failed concurrent index builds
  locks                Blocking locks and the sessions stuck behind them
  long-running-queries Queries running longer than 5 minutes
  outliers             Queries by cumulative execution time (needs pg_stat_statements)
  redundant-indexes    Indexes made redundant by another index
  replication-slots    Replication slots: status, WAL retention, and lag
  seq-scans            Tables receiving full-table scans
  subscriptions        Per-table logical replication progress on this subscriber
  table-sizes          Tables by total size, largest first
  unused-indexes       Indexes with little or no use — removal candidates
  vacuum-stats         Autovacuum and autoanalyze health: last runs, dead tuples, thresholds
```

Every subcommand uses:

```text
pscale inspect <check> <database> <branch> [flags]
```

## Persistent target flags

```text
--org string        The organization for the current user
--dbname string     PostgreSQL database to inspect (default "postgres")
--keyspace string   Vitess keyspace, optionally with shard/tablet target
--replica           Run checks against a replica instead of the primary
--shard string      Neki shard ID to inspect
--router string     Neki router group to inspect through
--role string       Ephemeral credential role: reader, writer, readwriter, admin
```

`--keyspace` examples:

```text
commerce
commerce/-80
commerce/-80@replica
```

List Vitess shards before selecting one:

```bash
pscale sql <database> <branch> --org <org> --format json \
  --query "SHOW VITESS_SHARDS"
```

The default role is `reader`. On PostgreSQL or Neki, it may lack `CONNECT` for a non-default `--dbname`; the CLI reports this and suggests `--role admin`.

For Neki, list shard IDs and router names before selecting one:

```bash
pscale branch shard list <database> <branch> --org <org> --format json
pscale branch router list <database> <branch> --org <org> --format json
# Primary-path evidence is the default
pscale inspect all <database> <branch> --org <org> \
  --shard <shard-id> --format json
# Select a router and/or replica only when that target path is intentional
pscale inspect all <database> <branch> --org <org> \
  --shard <shard-id> --router <router-name> --replica --format json
```

`--shard`, `--router`, and `--replica` can be combined on Neki. The first two are rejected for other engines, and Neki `--shard` rejects Vitess-style `keyspace/shard` values.

## Output formats

The root `--format` flag accepts `human`, `json`, or `csv`.

- A single check supports all three formats.
- `inspect all` supports human and JSON.
- `inspect all --format csv` fails because the checks have different result schemas.
- JSON single-check output contains `check`, `database`, `branch`, `columns`, `rows`, `row_count`, and optional `skipped`/`next_steps` fields.
- JSON `all` output contains all check results plus catalog-level `next_steps`.

## Engine applicability

| Check | MySQL/Vitess | PostgreSQL/Neki | Notes |
|---|---:|---:|---|
| `table-sizes` | yes | yes | PostgreSQL/Neki table size excludes separately reported index storage |
| `index-sizes` | yes | yes | Largest first |
| `unused-indexes` | yes | yes | Usage statistics are evidence, not automatic drop approval |
| `redundant-indexes` | yes | no | PostgreSQL/Neki uses `insights recommendations` |
| `invalid-indexes` | no | yes | Failed concurrent index builds |
| `seq-scans` | yes | yes | PostgreSQL/Neki lists only tables with actual sequential scans |
| `long-running-queries` | yes | yes | Threshold is five minutes |
| `locks` | yes | yes | Reports blocking relationships rather than routine granted locks |
| `outliers` | no | yes | Requires `pg_stat_statements`; MySQL uses `insights queries --sort totalTime` |
| `calls` | no | yes | Requires `pg_stat_statements`; MySQL uses `insights queries --sort count` |
| `bloat` | yes | yes | MySQL fragmentation / PostgreSQL/Neki estimated table and index bloat |
| `vacuum-stats` | no | yes | Includes per-table autovacuum settings and thresholds |
| `replication-slots` | no | yes | Slot state, WAL retention/headroom, lag |
| `subscriptions` | no | yes | Subscriber-side per-table logical replication progress |

## Combined report behavior

```bash
pscale inspect all <database> <branch> --org <org> --format json
```

- A single ephemeral SQL session is used for the selected target.
- A Neki run stays pinned to the requested shard/router/replica path and does not fan out; customer-facing results omit the internal `__neki` schema.
- Each diagnostic is one bounded, read-only query with a 30-second timeout.
- An unavailable check is represented as skipped with an explanation.
- A failed check is recorded as skipped and does not abort later checks.
- Targeted and catalog-level `next_steps` point to complementary `pscale insights` commands.
- No check fans out over all Vitess shards; select a keyspace/shard explicitly when shard-specific evidence matters.
