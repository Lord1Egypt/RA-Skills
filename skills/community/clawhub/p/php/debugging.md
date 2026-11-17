# Debugging — Symptom to Cause

PHP hides failures by design in production configurations. Every chain below starts by making the message visible, then narrows. Work symptom-first; each step is a check, not a guess.

## The Universal First Three

1. `php --ini` — which ini files are actually loaded for THIS SAPI. The single most common wasted hour is editing an ini the running process never reads (`php-ini.md`).
2. `php -d error_reporting=E_ALL -d display_errors=1 <script>` for CLI, or the error log for web: `tail -f` the path in `error_log`, the FPM pool log, and the web server's error log together — the message is in exactly one of the three.
3. `php -l <file>` for a parse error, then `php -r 'var_dump(extension_loaded("opcache"));'` to know whether you are even running the code you just edited.

## Blank White Page

1. A fatal error with `display_errors = Off`. Reproduce with `php -d display_errors=1 -d error_reporting=E_ALL public/index.php` from the CLI — most bootstrap fatals surface immediately.
2. If nothing appears, it was fatal before your handler loaded: check the FPM/web error log for the parse or "Allowed memory size" line.
3. Output buffering swallowing the message: an `ob_start()` with no matching flush discards everything on fatal. Grep for `ob_start` in the bootstrap.
4. Still blank with a 200 status: the response was produced and is empty — a template returned nothing, or an early `exit` ran. Check `http_response_code()` and the access log's byte count.
5. Silent 500 with an empty log file: the log path is not writable by the FPM user, or `log_errors = Off`. Both fail silently by nature.

## "It Worked Yesterday" / Stale Code

1. `opcache.validate_timestamps=0` with a deploy that swapped files in place — the workers still hold the old bytecode. Reload FPM (`kill -USR2 <master>`) and re-test (`fpm.md`).
2. `opcache.revalidate_freq` (default 2 seconds) means an edit can take a couple of seconds to appear even with validation on.
3. `--classmap-authoritative` autoloader plus a new class: not in the map, so it "does not exist". `composer dump-autoload` (`composer.md`).
4. A caching layer above PHP (nginx fastcgi_cache, a CDN, the application's own cache) serving the previous render.
5. You are editing a different file than the one running: `var_dump(__FILE__)` at the top of the suspect file settles it in five seconds.

## Wrong Value, No Error

1. `var_dump()` at input, at the midpoint, and at output; the first wrong one is the bug. Use `var_dump`, not `print_r` — `print_r` shows `1` for both `true` and `"1"`, which is the very distinction you are hunting.
2. Suspect the juggling first: `==` where types differ, `in_array` without `true`, `empty()` on `"0"`, a numeric string key collapsing (`types.md`, `arrays.md`).
3. Suspect a reference second: a leftover `foreach ($a as &$v)`, or an object assigned expecting a copy (`arrays.md`, `oop.md`).
4. Suppressed diagnostics third: install the `set_error_handler` that converts warnings to exceptions and re-run — a warning you never saw is a wrong value in flight (`errors.md`).
5. Wrong only in production: config difference. Diff `php -i` output between the environments and look at `precision`, `date.timezone`, `default_charset`, and the loaded extensions.

## Memory Exhausted

1. Read the message: it names the file and line of the allocation that crossed the limit — usually a symptom, not the cause.
2. `memory_get_peak_usage(true)` at a few checkpoints localizes the growth to one phase in minutes.
3. Usual causes, in frequency order: `file_get_contents`/`fetchAll` on something large; an accumulating array inside a loop (log lines, entity map, ORM identity map); an unbounded result set; a recursive structure; image processing, where GD allocates roughly `width × height × 4` bytes regardless of how small the compressed file is — a 4000×3000 JPEG is about 48 MB per open image, and a resize holds two.
4. Fixes: stream (`fgetcsv`, `fetch()` in a loop, generators), `unset()` the previous chunk inside the loop, and for long workers `gc_collect_cycles()` after each job — cycles are only reclaimed by the collector (`performance.md`, `cli.md`).
5. Raising `memory_limit` is the last step and only with a number you justified. In a worker, the true limit is `memory_limit × pm.max_children` against host RAM (`fpm.md`).

## Timeouts and Hangs

| Which limit fired | Signature | Fix |
|---|---|---|
| `max_execution_time` | "Maximum execution time of N seconds exceeded", with a PHP stack trace | The CPU-bound loop that ran long; CLI has no limit by default |
| FPM `request_terminate_timeout` | Worker killed, 504 from the web server, no PHP trace | Time spent inside a system call — a socket or DB read with no timeout (`fpm.md`) |
| Web server timeout | 504 with a fastcgi read-timeout line in the nginx error log | Raise the server timeout only after fixing the slow work |
| Deadlock | No timeout at all; the process sits forever | Almost always a DB lock or a full pipe in `proc_open` (`concurrency.md`) |

- Find where a running process is stuck: `strace -p <pid>` (Linux) shows the syscall it is blocked in; a socket read against your database is a DB problem, `futex` is a lock, `poll` on nothing is a hung upstream.
- `request_slowlog_timeout` plus `slowlog` in the FPM pool prints a PHP backtrace for any request over the threshold. It is the single best FPM diagnostic and it is off by default (`fpm.md`).

## Xdebug 3

Xdebug 3 renamed every setting from Xdebug 2 and changed the default port; almost all outdated guides on the internet are Xdebug 2.

```ini
xdebug.mode = debug,develop     ; develop gives readable var_dump and stack traces
xdebug.start_with_request = yes ; or "trigger" plus XDEBUG_TRIGGER in the request
xdebug.client_host = host.docker.internal   ; the IDE's host as seen FROM the container
xdebug.client_port = 9003       ; 9000 was Xdebug 2
xdebug.discover_client_host = false
```

- Breakpoints never hit: the IDE is not listening, the port is blocked, or path mappings are wrong (the container path must map to the host project root).
- `xdebug.mode` is the master switch. `off` is the production value; loading the extension at all costs measurable time on every request, and coverage or profile mode costs far more (`performance.md`).
- Coverage in CI: `pcov` is dramatically faster than Xdebug for line coverage; use Xdebug when you need branch/path coverage or a debugger (`testing.md`).
- `xdebug.mode=profile` writes cachegrind files; open them in KCachegrind or Qcachegrind and read the inclusive cost column first.

## Without a Debugger

- `error_log(print_r($x, true))` writes to the same log as fatals, so it survives a request that produces no output. `var_export($x, true)` when you want to paste the value back into code.
- `debug_print_backtrace(DEBUG_BACKTRACE_IGNORE_ARGS)` — the call path with no argument dump; `(new \Exception())->getTraceAsString()` when you want it as a string.
- `assert()` is compiled out in production, so it cannot be the check that matters (`errors.md`).
- Long-running workers: log a heartbeat with the job id BEFORE the work, not after — the last line before silence names the poison job (`cli.md`).
- Segfault or "Allowed memory size" with no PHP-level cause: disable Xdebug first, then check for deep recursion. `php >=8.3` detects stack overflow via `zend.max_allowed_stack_size` and reports it instead of crashing.

## Works Locally, Fails on the Server

| Difference | Check |
|---|---|
| Case-sensitive filesystem on Linux vs insensitive on macOS | A class file or `include` path differing only in case |
| Different PHP version | `php -v` on both; then the semantic changes in `versions.md` |
| Different ini per SAPI | `php --ini` vs a `phpinfo()` page — CLI and FPM load different files |
| Missing extension | `php -m` on the server (`ext-intl`, `ext-mbstring`, `ext-pcntl` are the usual absentees) |
| `date.timezone` unset or different | `date_default_timezone_get()` in both (`datetime.md`) |
| File permissions and the FPM user | `ls -l` on cache, log, and upload directories |
| `open_basedir` or `disable_functions` set by the host | `php -i \| grep -E 'open_basedir\|disable_functions'` |

## When You Are Truly Stuck

Reduce to the smallest reproduction: `php -d error_reporting=E_ALL -d display_errors=1 -r '<five suspect lines>'`, no framework, no autoloader. Then add one thing back at a time — the addition that breaks it names the subsystem and the guide to open next.

## Related

- Which ini file wins, and per-SAPI differences: `php-ini.md`
- Making warnings loud in the first place: `errors.md`
- Profiling once the bug is a performance problem: `performance.md`
