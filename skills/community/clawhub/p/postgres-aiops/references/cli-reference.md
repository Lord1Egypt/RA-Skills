# postgres-aiops CLI reference

> Catalog / `pg_stat_*` queries have been exercised against a live PostgreSQL 16.14 instance
> (see docs/VERIFICATION.md).

## Setup & diagnostics

```bash
postgres-aiops init                      # interactive onboarding wizard
postgres-aiops doctor [--skip-auth]      # config + secret store + connectivity (SELECT version())
postgres-aiops overview [--target <t>]   # one-shot cluster health snapshot
postgres-aiops mcp                       # start the MCP server (stdio transport)
```

## Secrets (encrypted store ~/.postgres-aiops/secrets.enc)

```bash
postgres-aiops secret set <target> [--value <pw>]    # store password (hidden prompt if no --value)
postgres-aiops secret list                            # names only — values never shown
postgres-aiops secret rm <target>
postgres-aiops secret migrate                         # import legacy plaintext .env (PG_<T>_PASSWORD)
postgres-aiops secret rotate-password                 # re-encrypt under a new master password
```

## Read commands

```bash
postgres-aiops server version                 # version, uptime, recovery state
postgres-aiops server settings [pattern]      # pg_settings (optional name filter)
postgres-aiops server databases               # databases + sizes
postgres-aiops server roles
postgres-aiops server extensions

postgres-aiops activity list [--state active] # pg_stat_activity + per-state counts
postgres-aiops activity long [--min-seconds 60]
postgres-aiops activity locks

postgres-aiops query top [--order-by total_time] [--limit 20]   # pg_stat_statements
postgres-aiops query explain "<sql>" [--analyze]

postgres-aiops index unused                   # zero-scan indexes
postgres-aiops index missing                  # missing-index hints
postgres-aiops index bloat [--limit 50]
postgres-aiops index invalid                  # invalid + duplicate

postgres-aiops table sizes [--limit 20]
postgres-aiops table bloat [--limit 50]       # dead-tuple bloat proxy
postgres-aiops table autovacuum [--limit 50]

postgres-aiops repl status                    # standby lag
postgres-aiops repl slots
postgres-aiops repl wal

postgres-aiops analyze slow-query [--explain "<sql>"] [--limit 20]   # flagship RCA
postgres-aiops analyze bloat-vacuum [--limit 50]
postgres-aiops analyze blocking
```

## Write commands (governed; risk tier in parentheses)

```bash
postgres-aiops remediate terminate <pid> [--dry-run]                     # (high) no undo; double confirm
postgres-aiops remediate cancel <pid> [--dry-run]                        # (high) no undo; double confirm
postgres-aiops remediate drop-index <name> [--concurrently] [--dry-run]  # (high) reversible; double confirm
postgres-aiops remediate vacuum <table> [--full] [--analyze] [--dry-run] # (medium)
postgres-aiops remediate analyze-table <table> [--dry-run]               # (medium)
postgres-aiops remediate create-index <table> <cols...> [--name N] [--unique] [--concurrently] [--dry-run]  # (medium) reversible
postgres-aiops remediate reindex <name> [--kind INDEX|TABLE|SCHEMA] [--concurrently] [--dry-run]            # (medium)
postgres-aiops remediate set <name> <value> [--dry-run]                  # (medium) ALTER SYSTEM; reversible
```

## Common options

- `--target, -t <name>` — target name from `config.yaml` (omit to use the default/first target)
- `--dry-run` — print the statement that would run, change nothing
- State-changing commands require two confirmations at the CLI layer

## Truncation

Every command that takes `--limit` returns an envelope — `{"...": [...],
"returned": N, "limit": L, "truncated": bool}` — and fetches one row past the
limit so `truncated` is measured, not inferred from the row count. When a read
is cut short the JSON on stdout stays clean and a notice is written to stderr:

```
… truncated at 50 rows (50 returned) — re-run with a higher --limit to see the rest.
```

`analyze slow-query` / `analyze bloat-vacuum` pull a limited read themselves, so
they also report `sourceTruncated` / `sourceLimit` when their input was partial.

## What decides whether a write runs

The tool does not decide whether a write is permitted — that is the agent's
judgement, or the permission of the PostgreSQL role you connect it with:
connect with a role that has no write privileges (a read-only role, or one
without INSERT/UPDATE/DELETE/DDL) and the write fails at the server. Every
call, over MCP and over the CLI alike, is still audited. See
[agent-guardrails.md](agent-guardrails.md).
