# Errors, Exceptions, and Making Failures Visible

PHP has two failure channels — the diagnostic system (`E_*` levels) and the exception system — and they only partly overlap. Most "PHP gives no error" reports are a message that went to a channel nobody is reading.

## The Throwable Hierarchy

```
Throwable
├── Error            engine failures: TypeError, ValueError, ArgumentCountError,
│                    ArithmeticError/DivisionByZeroError, AssertionError, UnhandledMatchError
└── Exception        your code and the SPL tree: RuntimeException, LogicException,
                     InvalidArgumentException, JsonException, PDOException
```

- `catch (Exception $e)` does NOT catch `Error`. In a framework boundary or a worker loop, catch `\Throwable`.
- `Error` means a bug in the program (wrong type, missing method); `Exception` means an expected failure mode (file missing, API down). Throw `LogicException` subclasses for the first, `RuntimeException` subclasses for the second.
- PHP 8 converted many former warnings into `Error`s: calling a method on null, an undefined function, invalid argument counts. Legacy code that "used to keep going" now stops — which is the point.
- Always chain: `throw new ImportFailed("row {$i}", previous: $e);` — an unchained rethrow deletes the original stack trace, the one fact that would have solved it.

## Diagnostics That Are Not Exceptions

| Level | Typical cause | Fatal? |
|---|---|---|
| `E_WARNING` | Undefined array key, undefined variable, `fopen` failure, division warnings | No — execution continues with a wrong value |
| `E_NOTICE` | Mostly promoted to warnings on `php >=8.0` | No |
| `E_DEPRECATED` | A feature scheduled for removal | No |
| `E_ERROR` | Memory exhausted, max execution time, stack overflow, fatal engine failure | Yes, and NOT catchable |
| `E_USER_*` | `trigger_error()` from your own code | Only `E_USER_ERROR` |

- Turning warnings into exceptions is the single highest-value error-handling change in a PHP codebase, because a warning leaves the wrong value in flight:

```php
set_error_handler(static function (int $no, string $msg, string $file, int $line): bool {
    if (!(error_reporting() & $no)) { return false; }   // respects @ and error_reporting
    throw new ErrorException($msg, 0, $no, $file, $line);
});
```

- `set_error_handler` never sees `E_ERROR`, `E_PARSE`, `E_CORE_*`, or `E_COMPILE_*`. Returning `false` from your handler lets PHP's internal handler run as well; returning `true` suppresses it, and also suppresses `error_get_last()`.
- Catch the uncatchable with a shutdown hook:

```php
register_shutdown_function(static function (): void {
    $e = error_get_last();
    if ($e !== null && ($e['type'] & (E_ERROR | E_PARSE | E_CORE_ERROR | E_COMPILE_ERROR))) {
        error_log("FATAL {$e['message']} at {$e['file']}:{$e['line']}");
    }
});
```

- `set_exception_handler` catches what nothing else did; it runs, then the script terminates — you cannot resume.

## The @ Operator

- `@` sets `error_reporting` to a reduced mask for one expression. On `php >=8.0` it no longer silences fatal errors, so a suppressed line can still kill the request.
- It hides the diagnosis and leaves the failed value in play: `$data = @file_get_contents($url);` gives you `false` with no idea whether the host was down or the path was wrong.
- The only defensible uses are the handful of functions with no non-warning form (some `fopen`-family calls on optional paths), and even there, checking the return and logging the reason beats suppression.

## try / catch / finally

- `finally` runs on normal completion, on `return`, and on exception. If `finally` itself contains a `return`, it OVERRIDES the value from `try` and swallows an in-flight exception — never `return` from `finally`.
- `exit()`/`die()` skip `finally` and skip destructors of objects still in scope. A worker that calls `exit()` mid-transaction leaves it open until the connection drops (`database.md`).
- Multi-catch: `catch (JsonException | PDOException $e)`. Catching without binding (`catch (SomeException)`, `php >=8.0`) is fine when the instance is unused.
- An empty `catch` is a decision to produce a wrong answer silently. If a failure genuinely is expected, write the reason as a comment AND log at debug level.
- Catch narrowly and rethrow at the boundary: one `catch (\Throwable)` at the top of the request, everything below catches only what it can handle.

## Logging That Survives Production

- Fatal messages go to `error_log` (php.ini). Under FPM they only reach the FPM log if the pool sets `catch_workers_output = yes` (`fpm.md`); under CLI they go to stderr.
- `display_errors = Off` and `log_errors = On` in production; the reverse in development. A blank white page is almost always `display_errors=Off` plus a fatal (`debugging.md`).
- `error_log(print_r($x, true))` for a quick structured dump; `var_export($x, true)` when you want valid PHP back (it fails on `NAN`/`INF` and on objects without `__set_state`).
- Structured logging (PSR-3, Monolog): pass context as the second argument, never interpolated. `$log->error('import failed', ['row' => $i, 'file' => $f])` groups in the aggregator; a message with the row number inline creates one unique message per row.
- Never log secrets, full request bodies, or `$_SERVER` wholesale — the log becomes the breach (`security.md`).

## Assertions

- `assert()` is compiled OUT when `zend.assertions = -1`, which is the production setting; it is fully active at `1`. Because the switch is compile-time, it cannot be turned on at runtime with `ini_set`.
- Therefore: never put a security check or a side effect inside `assert()`. Assertions state invariants you believe are already true; validation raises exceptions.
- `zend.assertions = 1` in dev and CI, `-1` in production, set in php.ini rather than per-script (`php-ini.md`).

## Domain Exceptions Worth Defining

- One package-level base interface (`interface BillingError extends \Throwable`) lets consumers catch everything from your module without depending on class names.
- Carry data, not just a message: `final class RateLimited extends \RuntimeException { public function __construct(public readonly int $retryAfter) { … } }`. A caller that has to parse the message is a caller you broke.
- Do not use exceptions for control flow across normal paths — a `tryFrom` returning `null` or a result object beats an exception thrown thousands of times per request (`performance.md`).

## Related

- Finding the error when nothing is printed: `debugging.md`
- Which ini settings control visibility, and per-SAPI differences: `php-ini.md`
- Worker loops that must not die on one bad job: `cli.md`, `concurrency.md`
