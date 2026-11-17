# psql — Client Workflow and SQL Scripting

The default client, present wherever Postgres is. `pgcli` adds autocompletion and syntax highlighting over the same protocol; everything below except the meta-commands applies to both.

## Inspection Meta-Commands

| Command | Shows |
|---|---|
| `\d table` / `\d+ table` | Columns, indexes, constraints, triggers; `+` adds sizes, storage, and comments |
| `\dt+` / `\di+` / `\dv` / `\dm` | Tables / indexes / views / materialized views with sizes |
| `\df+ name` / `\sf name` | Function signature and full source |
| `\dn+` / `\du+` / `\dp table` | Schemas / roles / per-object privileges |
| `\dx` | Installed extensions and versions |
| `\l+` | Databases with size, encoding, and collation |
| `\conninfo` | Which host, database, user, and port you are actually on |
| `\errverbose` | The full DETAIL/HINT/constraint of the last error |
| `\watch 5` | Re-run the previous query every 5 seconds — a live dashboard for `pg_stat_activity` |
| Anything else | `\?` for meta-commands, `\h ALTER TABLE` for the syntax of any statement |

`\d` on the wrong environment is the cheapest incident of the day: put the target in the prompt, `\set PROMPT1 '%n@%/%R%# '`, and keep production in a differently coloured terminal.

## Output That Is Readable

- `\x auto` — expanded output when a row is too wide, normal otherwise. The single highest-value setting.
- `\timing on` — execution time after every statement.
- `\pset pager off` for scripted output; `\pset null '∅'` to see NULLs as distinct from empty strings.
- `\gx` runs the current query with expanded output once, without changing the mode.
- Put the durable ones in `~/.psqlrc`; add `\set ON_ERROR_STOP on` there too, and remember that scripts run with `-X` to ignore `.psqlrc` deliberately.

## Scripting Rules

```bash
psql -X -v ON_ERROR_STOP=1 --single-transaction -f migration.sql "$DATABASE_URL"
```

- `-X` ignores `~/.psqlrc` so the script behaves the same on every machine — without it, someone's local `\set AUTOCOMMIT off` changes your deployment.
- `ON_ERROR_STOP=1` is mandatory in automation. Without it, psql reports the error, continues to the next statement, and exits 0: a half-applied migration that CI calls green.
- `--single-transaction` makes the whole file atomic. It is incompatible with statements that cannot run in a transaction block (`CREATE INDEX CONCURRENTLY`, `VACUUM`) — those files run without it.
- Variables: `-v tenant=42` then `:'tenant'` (quoted literal) or `:"tenant"` (quoted identifier). Bare `:tenant` interpolates raw text and is an injection vector in generated scripts.
- `\gexec` executes the result set of a query as SQL — the idiomatic way to generate DDL over many objects:
  ```sql
  SELECT format('REINDEX INDEX CONCURRENTLY %I.%I;', schemaname, indexname)
  FROM pg_indexes WHERE schemaname = 'app' \gexec
  ```
- Exit codes: 0 success, 1 psql-level error (bad flag), 2 connection failure, 3 script error with `ON_ERROR_STOP`. Check them in CI.

## COPY In and Out

- `COPY` (server-side) reads and writes files on the **server**, needs superuser or the `pg_read_server_files`/`pg_write_server_files` role, and does not exist on managed platforms.
- `\copy` (client-side) reads and writes files where psql runs, with your OS permissions. It is the one that works everywhere.

```sql
\copy (SELECT * FROM orders WHERE created_at >= '2026-07-01') TO 'jul.csv' WITH (FORMAT csv, HEADER)
\copy staging_orders FROM 'jul.csv' WITH (FORMAT csv, HEADER)
\copy orders TO PROGRAM 'gzip > orders.csv.gz' WITH (FORMAT csv)
```

- Import failures report the line number and the failing column; import into a staging table with permissive types first, then transform with SQL. The alternative is discovering the bad row at 90% of a two-hour load.
- Nulls: `WITH (FORMAT csv, NULL '')` distinguishes empty string from NULL — CSV cannot express both without saying which is which.
- Encoding mismatches surface as "invalid byte sequence for encoding": `WITH (ENCODING 'LATIN1')` on the copy, not a database-wide change.

## Transaction Discipline for Destructive Work

```
\set AUTOCOMMIT off
DELETE FROM orders WHERE created_at < '2020-01-01';
-- verify the row count, then
COMMIT;   -- or ROLLBACK;
```

With autocommit off, every destructive statement is reviewable before it is real. Pair it with `SELECT count(*)` using the identical WHERE clause first — if the count and the reported rows disagree, something is wrong with your predicate, not with the database. On a shared production console, `SET default_transaction_read_only = on` in the session makes read-only work incapable of writing by accident.

## Connecting Without Leaking Credentials

- `~/.pgpass` (mode 0600, `host:port:db:user:password`) or a `PGPASSWORD` exported by a secret manager — never a password in the command line, which lands in shell history and in `ps`.
- Connection URIs work everywhere: `postgres://user@host:5432/db?sslmode=verify-full&application_name=migrate`.
- `~/.pg_service.conf` names environments (`psql service=prod-ro`), which keeps hostnames out of scripts and makes "which database am I on" answerable.
- Always set `application_name` — it is what makes `pg_stat_activity` legible during an incident (monitoring guide).
- For a long remote session, run psql inside tmux/screen: a dropped SSH session leaves an orphaned backend holding locks until TCP keepalives notice.
