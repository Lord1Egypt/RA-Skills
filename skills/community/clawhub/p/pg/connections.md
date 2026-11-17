# Connections and Pooling — Before You Raise max_connections

Every Postgres connection is a full OS process: roughly 5-10MB of private memory before it does any work, plus `work_mem` per sort or hash node (formula in SKILL.md Core Rules 5). Idle connections still cost process slots, snapshot bookkeeping, and context switches.

## Sizing

- `max_connections` default 100. Raising it to 1000 does not buy throughput: past roughly `2 × cores + effective_spindles` *active* queries, more concurrency means more contention and less work done.
- The math to state out loud: peak concurrent *queries* is what the database serves; peak *connections* is what the application holds open. A pool converts the second into the first.
- A serverless or short-lived-worker fleet has connection churn, not connection count, as its problem: each new backend costs a fork plus catalog load, measured in single-digit milliseconds — thousands per second is a CPU line item.
- `superuser_reserved_connections` (default 3) is what keeps you able to log in during a connection storm. Never spend it.

## Diagnosing "FATAL: sorry, too many clients already" (53300)

```sql
SELECT state, count(*), max(now() - state_change) AS oldest
FROM pg_stat_activity GROUP BY state ORDER BY count DESC;

SELECT usename, application_name, client_addr, count(*)
FROM pg_stat_activity GROUP BY 1,2,3 ORDER BY count DESC LIMIT 10;
```

Read the state breakdown before touching anything:

| Dominant state | Meaning | Fix |
|---|---|---|
| `idle` | The pool is oversized, or many pools point at one database | Shrink pools, or put a pooler in front |
| `idle in transaction` | Application opens a transaction and then does non-database work | `idle_in_transaction_session_timeout`, and fix the code path |
| `active`, short queries | Genuine load | Pool, then scale reads or hardware |
| `active`, one long query | A runaway is holding slots behind it | Cancel it; add `statement_timeout` |
| Anything else | Unknown client | Group by `application_name` — nameless connections are the ones nobody owns |

Set `application_name` in every connection string. Without it, an incident becomes archaeology.

## PgBouncer Modes

| Mode | Connection returned to the pool | Safe for |
|---|---|---|
| session | On client disconnect | Everything, including session state; pools very little |
| transaction | At each COMMIT/ROLLBACK | The default in practice; the mode with the caveats below |
| statement | After each statement | Autocommit-only workloads; breaks multi-statement transactions |

Transaction mode breaks anything that outlives a transaction:

- `SET` / `SET LOCAL`: session `SET` leaks to the next client. Use `SET LOCAL` inside the transaction.
- Session advisory locks (SKILL.md Query Patterns) — use the `_xact_` variants.
- `LISTEN`/`NOTIFY`: the listener needs a dedicated session-mode connection.
- Temporary tables and `WITH HOLD` cursors.
- Protocol-level prepared statements: supported from PgBouncer >=1.21 with `max_prepared_statements` set; below that, drivers must disable server-side prepares.

Sizing PgBouncer: `default_pool_size` is per user/database pair, not global. Start at `2 × cores` server-side, `max_client_conn` at whatever the fleet opens, and watch `SHOW POOLS` for `cl_waiting` — clients waiting is the signal to grow the pool or the box, and nothing else is.

## Choosing Where the Pool Lives

- **App-side pool only** (HikariCP, pgx, SQLAlchemy, node-postgres): correct for one or two long-lived services. Total pool size across all instances must stay below `max_connections`; the failure mode is a deploy that doubles instance count during a rollout and exhausts the server.
- **PgBouncer / pgcat / Supavisor**: correct once services or instances multiply, or connections churn. Adds a hop (sub-millisecond) and the session-state limits above.
- **Both**: small app pool (5-10) pointing at the pooler is the standard production shape — the app pool amortizes TCP/TLS setup, the pooler amortizes backends.
- Run the pooler close to the application, not next to the database, when latency matters; next to the database when connection count is the problem. Two layers, two purposes.

## Timeouts That Belong on Every Role

```sql
ALTER ROLE app SET statement_timeout = '30s';
ALTER ROLE app SET idle_in_transaction_session_timeout = '5min';
ALTER ROLE app SET lock_timeout = '2s';
ALTER ROLE analytics SET statement_timeout = '10min';
```

Per role, not globally: the migration runner, the analytics user, and the web app need different ceilings (defaults and rationale in SKILL.md Core Rules 4). `idle_session_timeout` (PostgreSQL >=14) also closes idle non-transaction sessions — safe for interactive users, harmful for pooled application connections, which look idle by design.

## Connection Failures Worth Recognizing

- `connection refused` — the server is not listening on that address (`listen_addresses`) or the port is wrong.
- `no pg_hba.conf entry for host ...` — the server is reachable and rejecting you on policy, not on credentials.
- `SSL SYSCALL error: EOF detected` / `server closed the connection unexpectedly` — the backend died (OOM killer, crash) or a middlebox cut an idle TCP session. Distinguish with the server log: a crash writes a log line, a cut connection does not.
- `remaining connection slots are reserved for non-replication superuser connections` — you have hit `max_connections` minus the reserve; the reserve worked.
- TCP keepalives (`tcp_keepalives_idle`) matter behind NAT gateways and cloud load balancers that silently drop idle connections after a few minutes; the symptom is the first query after an idle period failing, always.
