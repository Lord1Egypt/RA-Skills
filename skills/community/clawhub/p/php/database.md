# Databases from PHP — PDO, Transactions, and Connection Reality

## The Connection

```php
$pdo = new PDO(
    'mysql:host=127.0.0.1;port=3306;dbname=app;charset=utf8mb4',
    $user, $pass,
    [
        PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,  // default on php >=8.0
        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
        PDO::ATTR_EMULATE_PREPARES   => false,
        PDO::ATTR_STRINGIFY_FETCHES  => false,
        PDO::ATTR_TIMEOUT            => 5,
    ],
);
```

- `charset=utf8mb4` belongs in the DSN, not in a `SET NAMES` query. The DSN sets the client charset the DRIVER uses for escaping; a later `SET NAMES` changes the server's view only, which is precisely the gap that made emulated prepares injectable on multibyte charsets (`security.md`).
- `utf8` in MySQL is a three-byte subset that cannot store emoji or many CJK characters; `utf8mb4` is real UTF-8. Column collation must match, or a four-byte character is rejected or truncated at insert.
- `EMULATE_PREPARES => false` sends the statement and the values separately. It also changes behavior you must know about: named placeholders cannot be reused twice in one statement, and `LIMIT ?` requires an integer bind (`bindValue(':n', $n, PDO::PARAM_INT)`) because the driver no longer quotes it into place.
- On `php >=8.1` PDO_MySQL returns native integers and floats instead of strings. Code comparing `$row['id'] === '5'` breaks on upgrade; this is one of the most common 8.1 migration surprises (`versions.md`).
- `127.0.0.1` and `localhost` are not the same for MySQL: `localhost` uses a unix socket, the IP uses TCP. Permissions and TLS settings can differ between them.

## Binding

- Values bind; identifiers do not. Table names, column names, and `ORDER BY` directions come from an allowlist you wrote (`security.md`).
- `IN (?)` cannot take a list: `$in = implode(',', array_fill(0, count($ids), '?')); $stmt = $pdo->prepare("… IN ($in)");` then pass `$ids` to `execute()`.
- `execute([$a, $b])` binds everything as strings, which is usually fine; when the column type matters (booleans on PostgreSQL, `LIMIT` on MySQL), use `bindValue` with an explicit `PDO::PARAM_*`.
- `PDO::PARAM_BOOL` sends an integer on MySQL, which has no boolean type, and a real boolean on PostgreSQL. Storing `'false'` as a string into a Postgres boolean column is truthy — the bug appears months later.
- `NULL` binds correctly, but `WHERE col = ?` with a null parameter never matches: SQL requires `IS NULL`. Build the clause conditionally.

## Transactions

- `beginTransaction()` throws if a transaction is already active — PDO has no nesting. Emulate with a depth counter plus `SAVEPOINT`, or use a framework's transaction manager.
- DDL (`CREATE`, `ALTER`, `DROP`, `TRUNCATE`) causes an implicit commit on MySQL: a migration that mixes schema and data changes inside one transaction is not atomic, whatever the code looks like. PostgreSQL has transactional DDL and does not have this problem.
- Always roll back in `finally`, or an exception leaves the transaction open until the connection dies — and under persistent connections, into the NEXT request:

```php
$pdo->beginTransaction();
try { … ; $pdo->commit(); }
catch (\Throwable $e) { $pdo->rollBack(); throw $e; }
```

- Deadlocks are normal under concurrency, not a bug to design away. Detect (MySQL error 1213, SQLSTATE 40001) and retry the WHOLE transaction with backoff, up to a small fixed number of attempts. Retrying a single statement inside a dead transaction does nothing.
- Keep transactions short and do no I/O inside them. An HTTP call inside a transaction holds row locks for the remote service's latency.
- Isolation level is a real decision: MySQL's default REPEATABLE READ makes a long-running report see a snapshot; READ COMMITTED reduces lock contention for write-heavy work. Set it deliberately and once.

## Reading Results

- `fetchAll()` materializes every row. `while ($row = $stmt->fetch())` holds one — the difference between a working export and "Allowed memory size exhausted" (`performance.md`).
- MySQL buffers the whole result set client-side by default. True streaming needs `PDO::MYSQL_ATTR_USE_BUFFERED_QUERY => false`, and while an unbuffered result is open, that connection cannot run another query.
- `rowCount()` is reliable for `INSERT`/`UPDATE`/`DELETE`, not for `SELECT` on every driver. Count with `SELECT COUNT(*)` when you need a count.
- `lastInsertId()` is per-connection and returns the last id THIS connection generated, so it is safe under concurrency. On PostgreSQL it needs the sequence name, and a trigger that inserts elsewhere can make it point at the wrong table — `RETURNING id` is unambiguous.
- `FETCH_ASSOC` as the default avoids the duplicated numeric-and-named columns of `FETCH_BOTH`; `FETCH_CLASS` hydrates objects but sets properties BEFORE the constructor unless you pass `FETCH_PROPS_LATE`.

## Long-Lived Connections

- `MySQL server has gone away` in a worker means the server closed an idle connection past `wait_timeout`. Reconnect on the error rather than pinging on a timer (`cli.md`).
- `PDO::ATTR_PERSISTENT => true` reuses a connection across requests in the same worker. It inherits everything the previous request left: an open transaction, temporary tables, session variables, `LAST_INSERT_ID`. Use it only with an explicit reset on checkout, or not at all.
- Connection count is `pm.max_children × pools × hosts` against the server's `max_connections`. Persistent connections make this the steady state rather than the peak (`fpm.md`).

## Errors Worth Recognizing

| Code | Meaning | Response |
|---|---|---|
| MySQL 1062 / SQLSTATE 23000 | Duplicate key | Expected under concurrency — catch it instead of SELECT-then-INSERT (`concurrency.md`) |
| MySQL 1213 / SQLSTATE 40001 | Deadlock | Retry the whole transaction with backoff |
| MySQL 1205 | Lock wait timeout | Another transaction is holding a lock too long; find the long transaction |
| MySQL 2006 | Server has gone away | Idle timeout or a packet larger than `max_allowed_packet` |
| MySQL 1452 | Foreign key constraint fails | The parent row does not exist, or the insert order is wrong |
| SQLSTATE HY093 | Invalid parameter number | Placeholder count mismatch, or a reused named placeholder with emulation off |

`$e->errorInfo[1]` holds the driver-specific code; `$e->getCode()` holds the SQLSTATE. Branch on the driver code for the retry decisions above.

## Migrations and Schema

- Migrations are code: reviewed, versioned, and applied by the same pipeline as the deploy. Ad-hoc `ALTER` on production is how environments diverge.
- Every migration needs a rollback path, even if the rollback is "restore from backup" written down explicitly.
- Additive first: add the column, deploy code that writes both, backfill, then switch reads, then drop the old column. A single migration that renames a column breaks every worker still running the previous release.
- Large `ALTER TABLE` locks the table on older MySQL versions; check the online-DDL support for your version before running it in business hours.

## Choosing a Layer

- PDO directly for a handful of queries; a query builder when you assemble filters dynamically; an ORM when you have a domain model with relations and lifecycle rules.
- The recurring failure of every layer is the same: N+1 queries. Instrument the query COUNT per request in development and alert above a threshold — it is the one metric that catches the whole class (`performance.md`).
- `db_layer` in `config.yaml` selects which idiom examples use (SKILL.md Configuration).

## Related

- Injection and charset interaction: `security.md`
- Memory when result sets are large: `performance.md`
- Retries, locks, and idempotency across processes: `concurrency.md`
- Schema, indexing, and query plans: the `mysql` skill
