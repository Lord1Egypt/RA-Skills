# postgres-aiops setup & security guide

> Reads, a governed write, and its undo have been exercised against a live PostgreSQL 16.14 instance (see docs/VERIFICATION.md).

## 1. Install

```bash
uv tool install postgres-aiops
```

## 2. Prepare a role

postgres-aiops connects with psycopg 3 and reads the system catalogs and
`pg_stat_*` views. A least-privilege monitoring role works for the reads:

```sql
CREATE ROLE aiops LOGIN PASSWORD 'change-me';
GRANT pg_monitor TO aiops;                 -- read visibility into pg_stat_*
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;  -- for top_queries / slow_query_rca
```

Maintenance writes (VACUUM, CREATE/DROP INDEX, REINDEX) require ownership of the
target objects; `ALTER SYSTEM` requires a superuser or `pg_read_all_settings` +
the appropriate privilege.

## 3. Onboard

```bash
postgres-aiops init
```

The wizard collects (non-secret) connection details into
`~/.postgres-aiops/config.yaml` and stores the password **encrypted** into
`~/.postgres-aiops/secrets.enc`. Example config:

```yaml
targets:
  - name: primary
    host: 10.0.0.30
    port: 5432
    dbname: appdb
    user: aiops
    sslmode: require          # disable/allow/prefer/require/verify-ca/verify-full
```

## 4. Non-interactive use (MCP server / CI / cron)

Export the master password so the encrypted store can be unlocked without a
prompt:

```bash
export POSTGRES_AIOPS_MASTER_PASSWORD='your-master-password'
```

## Credential security

- The password is **never** written to disk in plaintext. It lives only in
  `~/.postgres-aiops/secrets.enc`, encrypted with Fernet (AES-128-CBC + HMAC),
  the key derived from your master password via scrypt. Only a per-store random
  salt and the ciphertext are on disk (chmod 600); the master password itself is
  never stored.
- A legacy plaintext env var `PG_<TARGET_NAME_UPPER>_PASSWORD` is still honoured
  as a fallback with a deprecation warning — migrate with `postgres-aiops secret
  migrate` (it imports then renames the old `.env`).
- The password is passed to `psycopg.connect` at connect time and held only in
  memory; it is never logged or echoed. Exception text and tracebacks are
  scrubbed of secret-shaped strings before being written to the audit log.

## SQL safety

- All values (pids, thresholds, limits, setting values) are **bound query
  parameters** — never string-formatted into SQL.
- The few identifiers that cannot be parameterised (table/index/GUC names,
  `ORDER BY` columns, index methods, `REINDEX` kinds) are validated against
  strict allow-lists and double-quoted before interpolation; anything that is not
  a plain identifier is rejected.
- `EXPLAIN` rejects multi-statement input (an embedded `;` is refused).

## Governance harness state

State lives under `~/.postgres-aiops/` (relocate with `POSTGRES_AIOPS_HOME`):

- `audit.db` — every tool call (SQLite), with risk tier and an optional
  approver/rationale annotation (`POSTGRES_AUDIT_APPROVED_BY` /
  `POSTGRES_AUDIT_RATIONALE` — never required, never blocking)
- `undo.db` — inverse descriptors for reversible writes (e.g. `drop_index`)
- budget / runaway guard — caps cumulative tool calls and wall-time; trips on
  tight poll/retry loops

## Verify

```bash
postgres-aiops doctor
```

`doctor` checks the config file, the encrypted store and its permissions, that a
password is present per target, and (unless `--skip-auth`) connectivity by
running `SELECT version()`.
