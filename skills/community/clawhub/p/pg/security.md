# Security — Roles, Grants, RLS, and the Connection Perimeter

## Roles: Three Layers, Not One

Postgres has no separate "users" and "groups" — only roles, some with `LOGIN`. The shape that survives a team:

```sql
CREATE ROLE app_owner NOLOGIN;                      -- owns the schema and tables
CREATE ROLE app_rw NOLOGIN;                         -- privilege bundle
CREATE ROLE app_ro NOLOGIN;
CREATE ROLE app_service LOGIN PASSWORD '...' IN ROLE app_rw;   -- what connects

GRANT USAGE ON SCHEMA app TO app_rw, app_ro;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA app TO app_rw;
GRANT SELECT ON ALL TABLES IN SCHEMA app TO app_ro;
ALTER DEFAULT PRIVILEGES FOR ROLE app_owner IN SCHEMA app
  GRANT SELECT ON TABLES TO app_ro;                 -- future tables too
```

- `ALTER DEFAULT PRIVILEGES` applies only to objects created **by the role named in `FOR ROLE`**. Set it for the role that actually runs migrations, or next month's tables will be invisible to the read-only role — the most common grant bug in Postgres.
- Applications never own their tables. If the connecting role owns them, an SQL injection can `DROP` them; if it does not, the same injection cannot.
- Grant on the schema (`USAGE`) *and* the objects. Missing schema usage produces "permission denied for schema", which reads like a table problem and is not.
- Predefined roles instead of superuser: `pg_read_all_data` / `pg_write_all_data` (PostgreSQL >=14), `pg_monitor` for observability tooling, `pg_signal_backend` for an on-call role that must cancel queries. Superuser should be a break-glass account, not a service account.
- Since PostgreSQL 15 the `public` schema is no longer world-writable. Upgrades from 14 or earlier break scripts that assumed every role could create tables in `public`.

## Row-Level Security

```sql
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation ON orders
  USING (tenant_id = current_setting('app.tenant_id')::bigint);
```

- `USING` filters what is visible to `SELECT`/`UPDATE`/`DELETE`; `WITH CHECK` constrains what `INSERT`/`UPDATE` may write. A policy with only `USING` lets a tenant insert rows belonging to another tenant.
- **The table owner and superusers bypass RLS by default.** `ALTER TABLE orders FORCE ROW LEVEL SECURITY` closes the owner hole — required whenever the application role also owns the table.
- With no policy defined but RLS enabled, the table returns zero rows. That is the intended fail-closed behaviour and it looks exactly like data loss the first time.
- Set the tenant with `SET LOCAL app.tenant_id = ...` inside the transaction, never plain `SET`: behind a transaction-mode pooler a session `SET` leaks to the next tenant on that connection (see the pooler caveats in the connections guide). This is the RLS multi-tenancy bug that actually happens.
- Performance: the policy predicate is added to every query. Make sure it is indexable — `tenant_id` first in the composite index (SKILL.md Core Rules 3) — and remember that policies referencing subqueries or functions run per row.
- RLS is a strong second layer, not a substitute for filtering in the application; treat it as the net that catches the forgotten `WHERE`.

## SECURITY DEFINER Functions

A `SECURITY DEFINER` function runs with the privileges of its owner. Without a pinned search path, a caller can create a same-named function or table in a schema earlier in their `search_path` and have the definer's privileges execute it:

```sql
CREATE FUNCTION admin_action() RETURNS void
LANGUAGE plpgsql SECURITY DEFINER
SET search_path = pg_catalog, pg_temp   -- mandatory, not optional
AS $$ ... $$;
```

Also `REVOKE EXECUTE ... FROM PUBLIC` and grant explicitly: functions are executable by PUBLIC by default.

## The Connection Perimeter

`pg_hba.conf` is evaluated **top to bottom, first match wins** — a permissive line above a strict one silently wins. Reload with `SELECT pg_reload_conf()` (no restart) and verify with the `pg_hba_file_rules` view, which shows parse errors before they lock you out.

```
# TYPE    DATABASE  USER        ADDRESS          METHOD
hostssl   app       app_service 10.0.0.0/16      scram-sha-256
host      all       all         0.0.0.0/0        reject
```

- `scram-sha-256`, never `md5` (deprecated, and its hash is offline-crackable). Switching requires `password_encryption = 'scram-sha-256'` **and** every user resetting their password — the old hash is not upgraded in place.
- `trust` in any file reachable from a network is a total compromise; it is the default in some container images.
- `hostssl` plus `ssl = on` forces TLS server-side. Client-side, `sslmode=require` only encrypts; `verify-full` is the one that stops a man in the middle. Managed providers hand you a CA bundle — use it.
- `listen_addresses = 'localhost'` by default. If a database must be reachable, put it behind a private network or a bastion, never on a public IP with an allowlist as the only control.

## Secrets, Auditing, and Data at Rest

- Never put credentials in a SQL file, a migration, or a `postgresql.conf` comment. Passwords set via `CREATE ROLE ... PASSWORD` land in `pg_stat_activity` and in the logs unless `log_statement` excludes DDL — use `\password` in psql, which sends the hash.
- `log_statement = 'ddl'` plus `log_connections`/`log_disconnections` is a reasonable baseline audit trail; `log_statement = 'all'` writes every parameter value, including personal data, to a file with different access controls than the database. That is a compliance decision, not a debugging one.
- `pgaudit` gives per-object, per-class auditing when a regime demands it.
- Encryption at rest is a storage-layer concern (LUKS, provider-managed keys); Postgres has no built-in TDE. Column-level encryption with `pgcrypto` is real but means the key lives near the query — useful for a handful of columns, not for a strategy.
- Encoding user data in the connection string, the `application_name`, or a query comment leaks it into every log and monitoring system downstream.

## Erasure and Retention Requests

A "delete this person's data" request is a schema question before it is a legal one:

- Map the reachability first: `SELECT conrelid::regclass, confrelid::regclass FROM pg_constraint WHERE contype = 'f'` gives the FK graph, which is the only reliable list of where a subject's rows can live. Denormalized copies, audit tables, and jsonb payloads are outside it — enumerate those by hand once and write the list down.
- Prefer anonymization to deletion where a row must survive for accounting: overwrite identifiers with a deterministic pseudonym in the same transaction, keep the aggregate. Deleting a row that a financial report depends on trades one compliance problem for another.
- Deletion is not immediate on disk: the old row version lives until vacuum removes it, and it lives in backups until they expire. State that retention window in the policy rather than claiming instant erasure.
- Scheduled retention (delete everything older than N) is a partition drop when the table is partitioned by time and a batched delete otherwise — never one unbounded `DELETE`.
- Log the erasure itself in a table that contains no personal data: subject id hash, date, scope. That record is what an audit asks for.

## Injection, in the Database's Own Terms

- Parameterized queries end injection for application code. Inside the database, dynamic SQL in plpgsql needs `format()` with `%I` (identifier) and `%L` (literal), or `quote_ident`/`quote_literal`; string concatenation in an `EXECUTE` is the same vulnerability with fewer readers.
- `search_path` is an attack surface for any function, not just definer ones. Pin it on functions that run with elevated rights.
- Grant `EXECUTE` deliberately; `REVOKE ALL ON FUNCTION ... FROM PUBLIC` for anything privileged.
