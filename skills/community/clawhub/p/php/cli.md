# CLI Scripts, Workers, and Cron

The CLI SAPI is a different runtime with different defaults. Code that behaves under FPM can hang, leak, or die silently here.

## What Differs From the Web SAPI

- `max_execution_time` is `0` — no time limit at all. A runaway loop runs until the host notices.
- Output goes straight out; there is no output buffering by default, and `header()` does nothing.
- A separate php.ini (`/etc/php/8.x/cli/php.ini`) with its own extensions and limits. `php --ini` is the answer to "why does it work in the browser" (`php-ini.md`).
- OPcache is usually disabled for CLI (`opcache.enable_cli = 0`), which is correct for short scripts and wrong for long-running workers.
- `$_SERVER['REQUEST_METHOD']` and friends do not exist; `php_sapi_name() === 'cli'` is the guard for code that must not run from the web.

## Script Skeleton

```php
#!/usr/bin/env php
<?php
declare(strict_types=1);
require __DIR__ . '/../vendor/autoload.php';

exit(main($argv));

function main(array $argv): int
{
    if (!isset($argv[1])) {
        fwrite(STDERR, "usage: import <file>\n");
        return 2;                       // 2 = usage error, by convention
    }
    // data to STDOUT, diagnostics to STDERR
    fwrite(STDOUT, "ok\n");
    return 0;
}
```

- Exit codes: `0` success, `1` general failure, `2` usage. Values above 254 are truncated, and `255` is reserved by PHP itself — never return it deliberately.
- `exit()` with a STRING prints it and exits `0`. `exit("error")` is a success exit that looks like a failure; use `fwrite(STDERR, …)` then `exit(1)`.
- Data on STDOUT, everything else on STDERR. That is what makes the script composable in a pipeline, and it keeps log lines out of the JSON your caller parses.
- `exit()` skips `finally` blocks and does not guarantee destructors run in a useful order — close transactions and files explicitly before exiting (`errors.md`).

## Arguments and Input

- `$argv[0]` is the script path; real arguments start at 1. Requires `register_argc_argv` (on by default for CLI).
- `getopt()` handles short and long options but stops at the first non-option argument and cannot express subcommands. Anything with more than two flags is cheaper to write with a console component than to debug.
- Streaming STDIN keeps memory flat: `while (($line = fgets(STDIN)) !== false) { … }`. `file_get_contents('php://stdin')` buffers the entire pipe.
- `posix_isatty(STDOUT)` (needs `ext-posix`) decides whether to emit colors — piping colored output into a log file is how escape codes end up in your alerts.
- `stream_set_blocking(STDIN, false)` before reading when the script must not hang waiting for input that may never arrive.

## Long-Running Workers

A worker is a web request that never ends, so every assumption PHP makes about short-lived processes stops holding.

- Memory grows monotonically: static caches, an ORM identity map, an accumulating log array. Check `memory_get_usage(true)` per job and exit cleanly above a threshold — the supervisor restarts you with a clean heap.
- Bound the loop deliberately: `--max-jobs=1000` or `--max-time=3600`, then exit 0. This is not a workaround; it is the standard PHP worker pattern, and it converts slow leaks into a non-event.
- `gc_collect_cycles()` after each job reclaims reference cycles that refcounting alone never frees.
- Database connections time out while idle (`MySQL server has gone away`): reconnect on failure rather than assuming a connection survives a quiet hour (`database.md`).
- Turn OPcache on for workers (`opcache.enable_cli = 1`) — the compile cost is paid once and every subsequent job benefits.
- Configuration and code are frozen at start: a deploy has no effect until the worker restarts. Make the deploy signal the supervisor.

## Signals and Graceful Shutdown

```php
pcntl_async_signals(true);                       // php >=7.1, no ticks needed
$running = true;
pcntl_signal(SIGTERM, function () use (&$running) { $running = false; });
pcntl_signal(SIGINT,  function () use (&$running) { $running = false; });

while ($running) {
    $job = $queue->reserve();
    if ($job === null) { usleep(200_000); continue; }
    $job->handle();                              // finishes before the loop re-checks
}
```

- `ext-pcntl` is CLI-only and absent on Windows; guard with `function_exists('pcntl_async_signals')` in cross-platform tools.
- Without a SIGTERM handler, a supervisor's stop kills the worker mid-job. With one, the job finishes and the process exits — the difference between an at-least-once queue that works and one that duplicates.
- Supervisors (systemd, supervisord, Docker) send SIGTERM, wait a grace period, then SIGKILL. Make the grace period longer than your slowest job.
- `SIGKILL` and `SIGSTOP` cannot be trapped. Any cleanup that must happen has to survive the process disappearing — design for idempotent retry, not for a clean exit (`concurrency.md`).

## Cron

- Cron runs with a minimal environment and a different `PATH`: use the absolute path to the intended binary (`/usr/bin/php8.3`), and an absolute path to the script.
- Cron does not load your shell profile, so `.env`-style variables set there are absent. Pass them in the crontab line or load them in the script.
- Redirect both streams or you lose the diagnosis: `>> /var/log/app/import.log 2>&1`. Cron's default mail-on-output is silently discarded on most servers.
- Overlap protection: `flock -n /var/lock/import.lock /usr/bin/php8.3 /srv/app/bin/import.php` — a job that runs every minute and sometimes takes ninety seconds will otherwise stack until the host falls over (`concurrency.md`).
- The CLI ini is what cron uses; a `memory_limit` you set in the FPM pool does not apply.
- Timezone: cron uses the system zone, PHP uses `date.timezone`. A job "at midnight" can be two different midnights (`datetime.md`).

## The Built-In Server

- `php -S localhost:8000 -t public` is a development convenience only. It is single-threaded before `php >=7.4`, and even after, concurrency comes from `PHP_CLI_SERVER_WORKERS`, which is not supported everywhere.
- Consequence: a page that makes an HTTP request back to itself deadlocks. Diagnose that before suspecting your code.
- It has no timeouts, no process isolation, and no request limits. Never expose it beyond localhost.

## Related

- Queues, locks, and parallelism across processes: `concurrency.md`
- Streaming file input without buffering: `files.md`
- CLI vs FPM ini differences: `php-ini.md`
