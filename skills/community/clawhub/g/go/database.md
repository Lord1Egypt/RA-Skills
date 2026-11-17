# Database — database/sql, Pools, Rows, and Transactions

`database/sql` is a connection pool with a query API attached. Most production incidents attributed to "the database" are the pool: unclosed rows, an unbounded pool, or a transaction that never ended.

## Pool Configuration (the four settings)

| Setting | Default | Set it to |
|---|---|---|
| `SetMaxOpenConns(n)` | **0 — unlimited** | A number the server can actually serve; the app-side limit must be below the server's own connection cap divided by the number of instances |
| `SetMaxIdleConns(n)` | **2** | Equal to `MaxOpenConns` for a busy service — the default causes constant connect/disconnect churn above two concurrent queries |
| `SetConnMaxLifetime(d)` | 0 — forever | Minutes, not hours: it lets load balancers rebalance and lets failed-over servers drop out |
| `SetConnMaxIdleTime(d)` | 0 — forever | Releases idle capacity back to the server |

- `sql.Open` does **not** connect; it validates the driver name and returns a pool. The first real connection happens on the first query. Call `db.PingContext(ctx)` at startup if you want to fail fast on bad credentials.
- `*sql.DB` is safe for concurrent use and is meant to be a **long-lived singleton**. Opening one per request is the single most damaging mistake in this package: no pooling, a connection storm, and the server's connection limit hit under trivial load.
- With `MaxOpenConns` set, a query beyond the limit blocks until a connection frees or the context expires — which is correct backpressure, and why every query needs a context (`context.md`).
- `db.Stats()` exposes `InUse`, `Idle`, `WaitCount`, and `WaitDuration`. Rising `WaitCount` means the pool is the bottleneck; rising `InUse` that never falls means leaked rows or transactions.

## Rows Must Close on Every Path

```go
rows, err := db.QueryContext(ctx, q, args...)
if err != nil { return err }
defer rows.Close()                 // idempotent; safe alongside the drain below

for rows.Next() {
    var u User
    if err := rows.Scan(&u.ID, &u.Name); err != nil { return err }
    out = append(out, u)
}
return rows.Err()                  // the error that ended the loop
```

- An open `*sql.Rows` holds a connection out of the pool. A `return` inside the loop without `defer rows.Close()` leaks it permanently; enough of those and every request blocks waiting for a connection that will never come back.
- `rows.Next()` returning false means "done **or** failed". Skipping `rows.Err()` turns a mid-iteration network error into a silently short result set — this is the quiet data-loss bug of this package.
- `defer rows.Close()` inside a loop defers to function return, not iteration end (SKILL.md Core Rule 5). Extract the body into a function.
- `QueryRowContext(...).Scan(...)` releases the connection itself; it returns `sql.ErrNoRows` when nothing matched, which is a normal outcome to check with `errors.Is`, not an error to propagate blindly (`errors.md`).
- Use `ExecContext` for statements with no rows; it returns `RowsAffected()`, which several drivers do not support — check the error rather than trusting the number.

## NULL and Scanning

- Scanning SQL NULL into a `string` or `int` fails with "converting NULL to string is unsupported". Use `sql.NullString`, `sql.NullInt64`, `sql.NullTime`, or a pointer (`*string`) — pointers read better and encode to JSON as `null` naturally (`json.md`).
- `sql.Null[T]` (`go >=1.22`) is the generic version and removes the per-type zoo.
- `Scan` needs a pointer per column, in the exact order and count of the SELECT. `SELECT *` plus a fixed `Scan` list breaks the day someone adds a column — always list the columns.
- Time columns depend on the driver: MySQL needs `parseTime=true` in the DSN or it returns `[]byte`; Postgres drivers return `time.Time` with the session's zone. Store UTC and be explicit (`time.md`).
- `[]byte` scanned from a column is only valid until the next `Next()` call; copy it if you keep it.

## Transactions

```go
tx, err := db.BeginTx(ctx, &sql.TxOptions{Isolation: sql.LevelReadCommitted})
if err != nil { return err }
defer tx.Rollback()                // no-op after a successful Commit
if _, err := tx.ExecContext(ctx, ...); err != nil { return err }
return tx.Commit()
```

- `defer tx.Rollback()` on the line after `BeginTx` is the pattern: it makes every early return safe, and `Rollback` after `Commit` returns `sql.ErrTxDone`, which you ignore here deliberately.
- A `*sql.Tx` **pins one connection** for its whole life. A transaction that waits on an HTTP call, a lock, or user input holds both a pool slot and database-side locks. Keep transactions to database work only, and short.
- Never mix `db.Query` and `tx.Query` inside a transaction: the `db` call takes a *different* connection and cannot see the uncommitted state, which produces "the row I just inserted does not exist".
- Nested transactions do not exist in `database/sql`. Emulate with savepoints via raw statements, or restructure so one function owns the transaction and takes an interface satisfied by both `*sql.DB` and `*sql.Tx`.
- Retry on serialization failures (Postgres 40001, MySQL deadlock 1213) is a normal part of using higher isolation levels — the retry must re-run the whole transaction body, not just the failing statement.

## Placeholders and Injection

- Always use placeholders: `?` for MySQL and SQLite, `$1..$n` for Postgres, `:name` for Oracle. They are not portable, which is why an application that must support two engines needs a builder rather than string constants.
- Placeholders bind **values**, never identifiers. Dynamic table or column names cannot be parameterized: validate them against a fixed allowlist before interpolating (`security.md`).
- `IN (?)` with a slice does not work. Build the placeholder list to match the argument count, or use the driver's array support (`= ANY($1)` with `pq.Array` on Postgres).
- `db.Prepare` returns a statement bound to the pool that re-prepares itself on new connections; for a query run a handful of times, the round trips cost more than they save. Prepare when a statement runs in a tight loop, and `defer stmt.Close()`.

## Migrations and Schema

- Migrations are versioned, forward-only files applied by a tool that records what ran, never DDL executed from application startup by several instances at once.
- Every migration needs a plan for the running old version: add a nullable column, backfill, then make it NOT NULL in a later release. A single migration that renames a column takes the old deployment down during the rollout.
- Long-lived DDL takes locks. On a large table, check what the engine actually locks before shipping the migration at peak.

## Observability

- Log the query name and duration, never the interpolated statement with values in it — that is how PII reaches logs (`logging.md`).
- Instrument `db.Stats()`; pool saturation looks like application slowness with an idle database.
- A query that is fast in a client and slow in Go is usually the pool waiting, not the query. Check `WaitDuration` before rewriting SQL (`performance.md`).

## Back To SKILL.md

Resource-closing discipline: SKILL.md Core Rule 5 and Output Gates. Contexts and deadlines: `context.md`. Pool sizing against worker counts: `concurrency.md`.
