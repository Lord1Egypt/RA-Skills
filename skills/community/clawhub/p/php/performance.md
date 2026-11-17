# Performance — Measure, Then Fix the Top Line

Order of operations that holds for almost every PHP application: OPcache on and sized correctly, then the database, then the algorithm, then the runtime. Skipping to the runtime is how teams enable JIT and change nothing.

## OPcache

Without OPcache, every request re-parses and re-compiles every included file. It is the largest single win available, and it is off in some default builds.

```ini
opcache.enable = 1
opcache.enable_cli = 0            ; 1 only for long-running CLI workers
opcache.memory_consumption = 256  ; MB; raise if the status page shows restarts
opcache.interned_strings_buffer = 16   ; MB; frameworks need more than the small default
opcache.max_accelerated_files = 20000  ; must exceed your real file count
opcache.validate_timestamps = 1   ; 0 in production, with an FPM reload on deploy
opcache.revalidate_freq = 2       ; seconds, when validation is on
```

- Size `max_accelerated_files` from reality: `find . -name '*.php' | wc -l` including `vendor/`, then round up. The value is rounded to a prime internally; exceeding it evicts constantly.
- Verify with `opcache_get_status()`: `memory_usage.free_memory` near zero, or a non-zero `opcache_statistics.oom_restarts` / `hash_restarts`, means the cache is thrashing and you are paying compile cost anyway.
- `validate_timestamps = 0` removes a stat call per file per request, at the price that a file swap does nothing until FPM reloads. Make `kill -USR2` the last step of the deploy, or you ship code that never runs (`fpm.md`, `debugging.md`).
- Preloading (`opcache.preload` with a script that `opcache_compile_file`s your framework, `php >=7.4`) links classes once at startup. It helps framework-heavy applications, cannot be changed without a restart, and files it preloads are frozen for the life of the master process.

## JIT — Read This Before Enabling It

- The tracing JIT (`php >=8.0`) compiles hot bytecode to machine code. For CPU-bound numeric loops the improvement is large; benchmarks showing multiples are Mandelbrot-class workloads.
- For a typical web request — I/O to a database, string and array work, framework indirection — the gain is close to nothing, and JIT adds memory (`opcache.jit_buffer_size`) plus a class of crashes that plain OPcache does not have.
- Decision rule: enable JIT only when a profile shows PHP CPU time dominating a hot numeric or parsing loop, and only after measuring the same workload with it off. Otherwise leave `opcache.jit_buffer_size = 0`.

## Profile Before Optimizing

- Xdebug profiler: `php -d xdebug.mode=profile -d xdebug.output_dir=/tmp script.php`, then read the cachegrind file in KCachegrind. Heavy but exact.
- pcov for coverage only; it does not profile.
- Production-grade samplers (SPX, Blackfire, Tideways, XHProf-family) sample live traffic at low overhead — the only way to catch a problem that appears at real concurrency.
- Cheap and always available: `hrtime(true)` around suspect blocks, `memory_get_peak_usage(true)` at checkpoints, and the DB layer's query log.
- Measure p95, not the mean. A mean hides the 5% of requests that generate the complaints.

## Database Is Usually the Answer

- N+1 queries: one query for the list plus one per row. Look for a query count that scales with the row count; every ORM has an eager-loading form (`database.md`).
- `fetchAll()` on a large result set holds every row in memory; `while ($row = $stmt->fetch())` holds one.
- A missing index turns a fast query into a table scan that only shows up at production data volume. `EXPLAIN` the slow queries — the `mysql` skill covers reading the plan.
- Round trips cost more than they look: 200 tiny queries at 1 ms of network latency each is 200 ms of wall clock with zero CPU. Batch them.
- Connect once per request; `PDO::ATTR_PERSISTENT` avoids the handshake but leaks session state between requests (`database.md`).

## PHP-Level Costs Worth Knowing

- `in_array`/`array_search` inside a loop is O(n²). Flip to a keyed lookup once (`arrays.md`) — the highest-yield array change in real code.
- `array_shift` in a loop reindexes the whole array each time; `SplQueue` or an index pointer is O(1).
- Copy-on-write means passing large arrays is free until written. A function that takes `array $rows` and modifies it duplicates the whole structure; take a generator or pass by reference deliberately.
- Generators (`yield`) convert "build a 500k-row array then loop it" into constant memory. `yield from` composes them without buffering.
- Magic methods (`__get`, `__call`) bypass the engine's member caches and are measurably slower than declared members — fine at the edges, wrong on a hot path (`oop.md`).
- Reflection and attribute scanning are startup-cost tools: resolve once and cache the result, never per request (`modern.md`).
- String concatenation in a loop is fine — PHP grows the buffer in place. Micro-optimizing `.=` is a distraction; the real string cost is building megabytes you then hold in memory.

## Caching Layers

| Layer | Scope | Use for |
|---|---|---|
| OPcache | Per FPM pool, per host | Compiled bytecode — not your data |
| APCu | Per FPM pool, per host, cleared on reload | Hot config, resolved metadata, per-node counters |
| Redis / Memcached | Shared across hosts | Sessions, query results, rate limits, locks (`concurrency.md`) |
| HTTP cache (nginx, CDN) | Everything upstream of PHP | Anonymous pages — the cheapest request is the one PHP never sees |

- Every cache entry needs a TTL and an invalidation story you can state in one sentence. "It expires eventually" is how stale prices reach customers.
- Cache stampede: when a hot key expires, every worker recomputes it simultaneously. Use a short lock around the recompute, or serve the stale value while one worker refreshes.
- APCu is per-process-pool, so a two-node cluster has two independent caches — never use it for anything that must agree across hosts.

## Autoloader and Startup

- `composer install --no-dev --optimize-autoloader` in production; `--classmap-authoritative` when nothing generates classes at runtime (`composer.md`).
- Every `files` autoload entry is `require`d on every request; keep that list to one or two files.
- `realpath_cache_size` (default is small) is consulted for every include; on a large `vendor/` tree, raising it to `4096k` with `realpath_cache_ttl = 600` removes a measurable share of syscalls.

## Related

- Worker sizing, and where request time actually goes: `fpm.md`
- Streaming file and result handling: `files.md`, `database.md`
- Long-running runtimes as the next step after this list is exhausted: `concurrency.md`
