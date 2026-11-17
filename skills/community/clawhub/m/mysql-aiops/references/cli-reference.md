# mysql-aiops CLI reference

> The `information_schema` / `performance_schema` queries are modelled from documented
> MySQL 8.x / MariaDB 10.6+ shapes and are mock-validated; see `docs/VERIFICATION.md`
> for the live-run checklist.

## Setup & diagnostics

```bash
mysql-aiops init                      # interactive onboarding wizard
mysql-aiops doctor [--skip-auth]      # config + secrets + connectivity + flavor + perf-schema + replica role
mysql-aiops overview [--target <t>]   # one-shot server health snapshot
mysql-aiops mcp                       # start the MCP server (stdio transport)
```

## Secrets (encrypted store ~/.mysql-aiops/secrets.enc)

```bash
mysql-aiops secret set <target> [--value <pw>]    # store password (hidden prompt if no --value)
mysql-aiops secret list                            # names only — values never shown
mysql-aiops secret rm <target>
mysql-aiops secret migrate                         # import legacy plaintext .env (MYSQL_<T>_PASSWORD)
mysql-aiops secret rotate-password                 # re-encrypt under a new master password
```

## Read commands

```bash
mysql-aiops server version                 # version, flavor (mysql/mariadb), uptime, read_only
mysql-aiops server variables [pattern]     # SHOW GLOBAL VARIABLES (optional name filter)
mysql-aiops server status [pattern]        # SHOW GLOBAL STATUS (optional name filter)
mysql-aiops server databases               # schemas + sizes
mysql-aiops server engines                 # storage engines
mysql-aiops server connections             # headroom vs max_connections

mysql-aiops activity sessions [--no-sleeping]  # processlist + per-command counts
mysql-aiops activity long [--min-seconds 60]
mysql-aiops activity transactions          # open InnoDB transactions
mysql-aiops activity lock-waits            # wait-for edges (flavor-branched)

mysql-aiops query top [--order-by total_time] [--limit 20]   # statement digests
mysql-aiops query explain "<sql>"          # EXPLAIN FORMAT=JSON (planned, not executed)

mysql-aiops index unused                   # zero-I/O indexes since restart
mysql-aiops index redundant                # prefix-covered / duplicate indexes
mysql-aiops index stats                    # columns + cardinality

mysql-aiops table sizes
mysql-aiops table fragmentation            # data_free per table
mysql-aiops table status                   # engine / row format / update time

mysql-aiops repl status                    # replica threads + lag (flavor-branched)
mysql-aiops repl binlog                    # binlog/GTID + downstream replicas

mysql-aiops analyze slow-query [--explain "<sql>"]   # flagship RCA
mysql-aiops analyze lock-waits             # chain + last deadlock
mysql-aiops analyze replication            # lag/thread-state RCA
mysql-aiops analyze fragmentation          # OPTIMIZE candidates
```

## Write commands (governed; risk tier in parentheses)

```bash
mysql-aiops remediate kill <id> [--dry-run]                    # (high) KILL CONNECTION; no undo; double confirm
mysql-aiops remediate kill-query <id> [--dry-run]              # (high) KILL QUERY; no undo; double confirm
mysql-aiops remediate drop-index <table> <name> [--dry-run]    # (high) reversible; double confirm
mysql-aiops remediate optimize <table> [--dry-run]             # (medium) OPTIMIZE TABLE
mysql-aiops remediate analyze-table <table> [--dry-run]        # (medium) ANALYZE TABLE
mysql-aiops remediate create-index <table> <cols...> [--name N] [--unique] [--dry-run]  # (medium) reversible
mysql-aiops remediate set <name> <value> [--dry-run]           # (medium) SET GLOBAL; reversible
mysql-aiops query reset [--dry-run]                            # (medium) truncate digest stats
```

## Common options

- `--target, -t <name>` — target name from `config.yaml` (omit to use the default/first target)
- `--dry-run` — print the statement that would run, change nothing
- State-changing commands require two confirmations at the CLI layer
