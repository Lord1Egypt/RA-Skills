# Locks — Blocked Queries, Deadlocks, and Lock Queues

Symptom that sends you here: a query is slow but burning no CPU, or an ALTER never returns, or the app throws 40P01 under load.

## Find the Blocker in One Query

```sql
SELECT a.pid, a.state, now() - a.xact_start AS xact_age,
       a.wait_event_type, a.wait_event, pg_blocking_pids(a.pid) AS blocked_by,
       left(a.query, 120) AS query
FROM pg_stat_activity a
WHERE a.backend_type = 'client backend' AND a.state <> 'idle'
ORDER BY xact_age DESC NULLS LAST;
```

- `pg_blocking_pids(pid)` (PostgreSQL >=9.6) returns the PIDs actually holding what this one waits for. Follow the chain to the root — the last PID in the chain is often `idle in transaction`, a connection nobody is watching.
- `wait_event_type = 'Lock'` is a heavyweight lock wait. `LWLock`, `IO`, and `BufferPin` are internal contention and mean something else entirely.
- Resolve: `SELECT pg_cancel_backend(pid)` first (polite, cancels the statement), then `pg_terminate_backend(pid)` (kills the connection, rolls back). Never `kill -9` a backend — the postmaster treats it as a crash and restarts the whole cluster into recovery (SKILL.md Traps).

## Lock Modes and What Takes Them

| Mode | Taken by | Conflicts with |
|---|---|---|
| ACCESS SHARE | `SELECT` | ACCESS EXCLUSIVE only |
| ROW SHARE | `SELECT ... FOR UPDATE/SHARE` | EXCLUSIVE, ACCESS EXCLUSIVE |
| ROW EXCLUSIVE | `INSERT`, `UPDATE`, `DELETE`, `MERGE` | SHARE and stronger |
| SHARE UPDATE EXCLUSIVE | `VACUUM` (non-full), `ANALYZE`, `CREATE INDEX CONCURRENTLY`, most `ALTER TABLE SET (...)` | Itself and stronger — two of these serialize |
| SHARE | `CREATE INDEX` (no CONCURRENTLY) | Writes (not reads) |
| SHARE ROW EXCLUSIVE | `CREATE TRIGGER`, some `ALTER TABLE` | Writes and itself |
| EXCLUSIVE | `REFRESH MATERIALIZED VIEW CONCURRENTLY` | Everything but ACCESS SHARE |
| ACCESS EXCLUSIVE | `ALTER TABLE`, `DROP`, `TRUNCATE`, `REINDEX`, `VACUUM FULL`, `CLUSTER` | Everything, including plain `SELECT` |

Two consequences worth memorizing: `VACUUM` never blocks reads or writes, and `TRUNCATE` — unlike in some other engines — is transactional here, fully rollbackable, and takes ACCESS EXCLUSIVE.

## The Lock Queue Is the Outage

Postgres grants locks roughly in arrival order. A pending ACCESS EXCLUSIVE request does not politely wait aside: every later request that conflicts with *it* also waits. So one `ALTER TABLE` stuck behind one long analytics query freezes all new traffic on that table, while `pg_stat_activity` shows a mostly idle server.

Defences, in order:
1. `SET lock_timeout = '2s'` before every DDL (SKILL.md Core Rules 4) — your statement gives up instead of building a queue.
2. Kill long transactions before scheduled DDL: check `xact_age` above.
3. `idle_in_transaction_session_timeout = '5min'` so an abandoned `BEGIN` cannot become an outage at midnight.
4. For unavoidable hot-table DDL, cancel the identified blocker deliberately rather than waiting and hoping.

## Row Locks

`UPDATE`/`DELETE` lock the rows they touch until commit; readers are never blocked (MVCC), but a second writer to the same row waits.

| Clause | Strength | Use |
|---|---|---|
| `FOR UPDATE` | Strongest row lock | Read-modify-write on a row another transaction may also change |
| `FOR NO KEY UPDATE` | What a plain `UPDATE` of non-key columns takes | Rarely written by hand |
| `FOR SHARE` | Blocks writers, allows readers | "This row must still exist and be unchanged when I commit" |
| `FOR KEY SHARE` | Weakest; what a foreign key check takes | Rarely written by hand |
| `+ NOWAIT` | Error 55P03 instead of waiting | Interactive paths that must fail fast |
| `+ SKIP LOCKED` | Skip contended rows | Job queues (SKILL.md Query Patterns) |

Row locks are stored in the tuple header and an on-disk multixact structure, not in shared memory, so there is no "too many row locks" limit — but heavy `SELECT FOR SHARE` on the same rows creates multixact pressure and its own vacuum work.

## Deadlocks

Postgres detects them after `deadlock_timeout` (default 1s) and aborts one victim with 40P01. A deadlock is never fixed by retrying alone — retries hide the frequency, they do not remove the cycle.

The three common cycles:

- **Opposite update order.** Transaction A updates row 1 then 2, B updates 2 then 1. Fix: sort the keys before updating (`ORDER BY id` in the batch, or sort in the application).
- **Foreign key contention.** Two transactions insert children of the same parent while something updates the parent: the inserts take `FOR KEY SHARE` on the parent, the update wants `FOR NO KEY UPDATE`. Fix: do not update the parent row in the same transaction as bulk child inserts (counter caches are the usual culprit).
- **Upsert races.** Two concurrent `INSERT ... ON CONFLICT DO UPDATE` on overlapping key sets, in different orders. Fix: sort the batch by conflict key.

Diagnose from the log: with `log_lock_waits = on` Postgres logs every wait longer than `deadlock_timeout`, and deadlock reports always include both statements and the relations involved. Turn it on before you need it.

## Advisory Locks

Application-level mutexes that Postgres tracks but never enforces on data.

- `pg_advisory_xact_lock(key)` releases at commit — the default choice.
- `pg_advisory_lock(key)` is session-scoped and survives commit. Behind a transaction-mode pooler the session is not yours after commit, so the lock leaks to a random future client. Only use it with a dedicated connection.
- `pg_try_advisory_lock(key)` returns false instead of waiting: the correct primitive for "only one worker runs this cron job".
- Keys are `bigint`, or two `int`s to namespace them (`pg_advisory_lock(42, user_id)`). Hashing a string with `hashtext()` works but collides — collisions look like a mysterious mutual exclusion between unrelated jobs.
- Held advisory locks are visible: `SELECT * FROM pg_locks WHERE locktype = 'advisory'`.

## Recurring Lock Waits Nobody Expects

- **Autovacuum versus DDL**: autovacuum holds SHARE UPDATE EXCLUSIVE; your `ALTER TABLE` queues behind it. Autovacuum yields automatically when it blocks a stronger request — except in anti-wraparound mode, where it does not. That is the case where DDL appears to hang for hours.
- **A replica's queries do not lock the primary**, but `hot_standby_feedback = on` makes them delay vacuum on the primary, which shows up as bloat rather than as a lock.
- **Extension and catalog operations** (`CREATE EXTENSION`, `ALTER TYPE ... ADD VALUE` before 12) take strong catalog locks that ripple into unrelated sessions.
- **`REFRESH MATERIALIZED VIEW`** without `CONCURRENTLY` blocks all readers of the view for the whole rebuild.
