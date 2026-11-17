# mysql-aiops setup & security guide

> Mock-validated; not yet run against a live MySQL / MariaDB server. `mysql-aiops doctor`
> is the fastest live check — see `docs/VERIFICATION.md`.

## 1. Install

```bash
uv tool install mysql-aiops
```

## 2. Prepare an account

mysql-aiops connects with PyMySQL and reads `information_schema` /
`performance_schema`. A least-privilege monitoring account works for the reads:

```sql
CREATE USER 'aiops'@'%' IDENTIFIED BY 'change-me';
GRANT PROCESS, REPLICATION CLIENT ON *.* TO 'aiops'@'%';
GRANT SELECT ON performance_schema.* TO 'aiops'@'%';
-- performance_schema must be ON (default on MySQL 8.x) for query stats
```

Maintenance writes need more: `OPTIMIZE`/`ANALYZE`/`CREATE INDEX`/`DROP INDEX`
require `ALTER` + `INDEX` (and `INSERT` for OPTIMIZE) on the target schema;
`KILL` requires `CONNECTION_ADMIN` (or `SUPER`); `SET GLOBAL` requires
`SYSTEM_VARIABLES_ADMIN` (or `SUPER`).

## 3. Onboard

```bash
mysql-aiops init
```

The wizard collects (non-secret) connection details into
`~/.mysql-aiops/config.yaml` and stores the password **encrypted** into
`~/.mysql-aiops/secrets.enc`. Example config:

```yaml
targets:
  - name: primary
    host: 10.0.0.30
    port: 3306
    database: appdb
    user: aiops
    ssl_mode: verify_ca       # disabled/preferred/required/verify_ca/verify_identity
    ssl_ca: /etc/ssl/mysql-ca.pem
```

## 4. Non-interactive use (MCP server / CI / cron)

Export the master password so the encrypted store can be unlocked without a
prompt:

```bash
export MYSQL_AIOPS_MASTER_PASSWORD='your-master-password'
```

## Credential security

- The password is **never** written to disk in plaintext. It lives only in
  `~/.mysql-aiops/secrets.enc`, encrypted with Fernet (AES-128-CBC + HMAC),
  the key derived from your master password via scrypt. Only a per-store random
  salt and the ciphertext are on disk (chmod 600); the master password itself is
  never stored.
- A legacy plaintext env var `MYSQL_<TARGET_NAME_UPPER>_PASSWORD` is still
  honoured as a fallback with a deprecation warning — migrate with
  `mysql-aiops secret migrate` (it imports then renames the old `.env`).
- The password is passed to `pymysql.connect` at connect time and held only in
  memory; it is never logged or echoed. Exception text and tracebacks are
  scrubbed of secret-shaped strings before being written to the audit log.

## TLS

`ssl_mode` follows MySQL client semantics and maps to PyMySQL TLS kwargs:

| ssl_mode | Behaviour |
|----------|-----------|
| `disabled` | TLS off — isolated labs only |
| `preferred` (default) | negotiate TLS when the server supports it |
| `required` | force TLS, no certificate verification |
| `verify_ca` | force TLS + verify the server cert against `ssl_ca` |
| `verify_identity` | `verify_ca` + hostname check (recommended in production) |

## SQL safety

- All values (session ids, thresholds, limits, variable values) are **bound
  query parameters** — never string-formatted into SQL.
- The few identifiers that cannot be parameterised (schema/table/index/column
  names, global variable names, `ORDER BY` columns) are validated against a
  strict identifier charset / allow-lists and backtick-quoted before
  interpolation; anything that is not a plain identifier is rejected.
- `EXPLAIN` rejects multi-statement input (an embedded `;` is refused); the
  `drop_index` undo replay is shape-gated to `CREATE [UNIQUE] INDEX` statements.

## Governance harness state

State lives under `~/.mysql-aiops/` (relocate with `MYSQL_AIOPS_HOME`):

- `audit.db` — every tool call (SQLite), with risk tier and an optional approver/rationale
  annotation (`MYSQL_AUDIT_APPROVED_BY` / `MYSQL_AUDIT_RATIONALE`) if you set one — never
  required, never blocking
- `undo.db` — inverse descriptors for reversible writes (e.g. `drop_index`)
- budget / runaway guard — caps cumulative tool calls and wall-time; trips on
  tight poll/retry loops

## Verify

```bash
mysql-aiops doctor
```

`doctor` checks the config file, the encrypted store and its permissions, that a
password is present per target, and (unless `--skip-auth`) connectivity — then
probes `version()` (reporting the mysql/mariadb flavor), whether
`performance_schema` is ON, and the replica role (`SHOW REPLICA STATUS`, or
`SHOW SLAVE STATUS` on MariaDB).
