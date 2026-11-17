# Concurrency — Parallel Work, Locks, and Long-Running Runtimes

PHP's default model is share-nothing: one request, one process, no shared memory, everything discarded at the end. That model is why PHP is hard to leak and why every form of concurrency below has to be built deliberately.

## Parallel I/O Inside One Request

- Five sequential 200 ms API calls cost 1 second of the user's time and one FPM worker for that whole second. Run them together:

```php
$mh = curl_multi_init();
foreach ($urls as $k => $u) {
    $ch[$k] = curl_init($u);
    curl_setopt_array($ch[$k], [CURLOPT_RETURNTRANSFER => true, CURLOPT_TIMEOUT => 5]);
    curl_multi_add_handle($mh, $ch[$k]);
}
do { $status = curl_multi_exec($mh, $active); curl_multi_select($mh, 1.0); }
while ($active && $status === CURLM_OK);
```

- HTTP client pools (Guzzle's `Pool`, Symfony HttpClient's lazy responses) wrap this with concurrency limits and per-request error handling; prefer them over hand-rolled multi handles.
- Cap the concurrency. Twenty parallel calls to one upstream is a small denial-of-service you aimed at a partner.
- Every parallel call still needs its own timeout — one hung handle holds the whole batch until it expires (`http.md`).

## Subprocesses

- `proc_open` with an argument ARRAY (`php >=7.4`) avoids the shell entirely, which removes the quoting class of bugs and the injection class with it.
- The deadlock: a child writing more than the pipe buffer (commonly 64 KB on Linux) to stderr blocks forever while you sit reading stdout. Read BOTH pipes — `stream_select`, or set both non-blocking — or redirect stderr to a file.
- Always `fclose` the pipes before `proc_close`, and read `proc_close`'s return as the exit status.
- `exec`/`shell_exec` run through a shell; if you use them, every interpolated value goes through `escapeshellarg` (`security.md`). `passthru` streams output directly and cannot be captured.
- `pcntl_fork` is CLI-only and forks the whole process, including open database connections and file handles. The child MUST reconnect — two processes writing on one MySQL socket corrupts the protocol for both (`database.md`).

## Queues

- The default answer for anything slower than a few hundred milliseconds: enqueue, return, let a worker do it. It converts a user-facing timeout into a background retry.
- Assume at-least-once delivery. Every job must be idempotent — a payment job runs twice eventually, and the only defense is a unique key on the effect, not a check at the start of the handler.
- A visibility timeout shorter than the job's runtime means a second worker picks up a job still running. Set it above your p99 job duration and extend it explicitly for long jobs.
- Poison messages: bound retries and move the job to a dead-letter queue. A job that fails forever occupies a worker forever.
- Log the job identifier BEFORE the work, not after — the last line before silence names the job that killed the worker (`cli.md`, `debugging.md`).

## Locks Across Processes

| Scope | Mechanism | Caveat |
|---|---|---|
| One host, one file | `flock($fh, LOCK_EX \| LOCK_NB)` | Advisory only; unreliable on NFS |
| One host, cron overlap | `flock -n /var/lock/x.lock <command>` | The one-line fix for stacking cron jobs (`cli.md`) |
| Many hosts | Redis `SET key token NX PX 30000` | Release must be a Lua compare-and-delete on the token |
| Many hosts, transactional | Database advisory lock (`GET_LOCK`, `pg_advisory_lock`) | Tied to the connection; a dropped connection releases it |

- Releasing a Redis lock with a plain `DEL` deletes whoever holds it NOW, which after your TTL expired is someone else. Store a random token as the value and delete only if it matches, atomically.
- Every lock needs a TTL. A holder that crashes without a TTL blocks the system until a human intervenes.
- A lock long enough to matter is a design smell: prefer making the operation idempotent so a duplicate run is harmless.

## Races You Will Actually Hit

- Check-then-act: `SELECT` to see whether a row exists, then `INSERT`. Two workers pass the check in the same millisecond. Use a unique index and catch the duplicate-key error, or `INSERT … ON CONFLICT` / `ON DUPLICATE KEY UPDATE` (`database.md`).
- Read-modify-write on a counter: `SELECT balance`, compute, `UPDATE`. Do the arithmetic in SQL (`UPDATE … SET n = n + 1`), or take a row lock with `SELECT … FOR UPDATE` inside a transaction.
- Lost update on a form: two users load a record and both save. Optimistic locking — a `version` column in the `WHERE` clause, and zero affected rows means "someone else saved first".
- File written by two workers: the temp-file-plus-rename pattern makes the loser's write disappear cleanly instead of interleaving (`files.md`).
- Cache stampede: a hot key expires and every worker recomputes simultaneously. Lock the recompute, or serve stale while one worker refreshes (`performance.md`).

## Fibers and Async Runtimes

- `Fiber` (`php >=8.1`) is cooperative suspension on ONE thread — a coroutine primitive, not parallelism. It exists so libraries can offer async I/O without turning every caller's signature into promises.
- ReactPHP, Amp, and similar event loops give real concurrent I/O in a single process. The cost is total: a blocking call anywhere in the stack (a synchronous PDO query, `file_get_contents`, `sleep`) stalls the entire loop, so the whole dependency tree must be async-aware.
- `ext-parallel` provides real threads on ZTS builds; the ecosystem support is thin. `pthreads` is dead — do not start there.

## Long-Running Runtimes

Swoole, RoadRunner, FrankenPHP, and framework layers built on them keep the application booted between requests.

- The win is removing bootstrap from every request; measure what bootstrap actually costs at p95 before assuming it is the problem (`performance.md`).
- The cost is that share-nothing is gone. Everything static persists: singletons, container instances, `date_default_timezone_set`, `setlocale`, accumulated arrays, and the previous request's `$_SERVER` if the framework does not reset it.
- Auditable checklist before adopting: no static mutable state in application code · no per-request data cached on a service instance · every connection reconnects after an idle failure · a memory ceiling that recycles the worker · the deploy restarts workers, because code changes have no other way in.
- Debugging shifts too: a leak now compounds across thousands of requests instead of vanishing at the end of one. `memory_get_usage(true)` per request with an alert threshold is the standard instrument (`cli.md`).

## Related

- Worker lifecycle, signals, and supervision: `cli.md`
- Transactions, deadlocks, and retry codes: `database.md`
- Timeouts on the calls you are parallelizing: `http.md`
