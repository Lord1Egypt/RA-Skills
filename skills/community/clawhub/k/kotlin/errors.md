# Errors — Throwing, Typing, And Where Exceptions Disappear

Kotlin has no checked exceptions, so nothing in the compiler tells you a call can fail. That puts the entire burden on design: decide per operation whether failure is expected (return it) or exceptional (throw it), and know exactly how coroutines route the throw.

## Expected Failure vs Exception

| Situation | Shape |
|---|---|
| Validation, not-found, offline, "already exists" | Typed result: `sealed interface LoginResult { data class Ok(…) ; data object WrongPassword ; data class Locked(val until: Instant) }` |
| Caller cannot proceed and cannot fix it (broken invariant, corrupt state) | `throw IllegalStateException` / `error("…")` |
| Caller passed something impossible | `require(...)` → `IllegalArgumentException` |
| I/O that the layer above can retry or surface generically | Throw, and translate at the layer that has UI or policy context |
| Parsing untrusted input | Typed result; a parser that throws forces every caller into `try/catch` |

The decisive test: if every caller wraps the call in `try/catch`, the failure was never exceptional — return it as a value. If no caller can do anything but crash or log, do not make them pattern-match on it.

## kotlin.Result vs A Sealed Hierarchy

- `kotlin.Result` is a value class holding either a value or a `Throwable`: fine for a local `runCatching`, weak as a public API. It cannot be matched exhaustively, it says nothing about which failures exist, it boxes when it crosses a generic boundary, and it invites `getOrNull()!!`.
- A sealed hierarchy names the failures, gets exhaustiveness checking (SKILL.md rule 9), and carries per-case data (`Locked(until)`), which the UI needs anyway.
- `Either`-style types from a functional library are a third option; they buy composition operators at the cost of a dependency and a vocabulary the whole team must share.
- Whatever the shape: one error model per module boundary, translated at the boundary. Leaking `SQLException` into a UI layer means the UI decides what a constraint violation means.

## Exception Basics That Bite

- `require`, `check`, `error`, `assert`: `require` → `IllegalArgumentException` (the caller's fault), `check` → `IllegalStateException` (our state), `error(msg)` → always throws `IllegalStateException`, `assert` → disabled on the JVM unless the process runs with `-ea`, so it is not validation.
- The message lambda in `require(x) { "…" }` is only evaluated on failure — cheap, so always include a message with the offending value.
- `Nothing` is the return type of a function that always throws, which lets `?: error("missing")` type-check as the non-null branch.
- `try` is an expression: `val n = try { s.toInt() } catch (e: NumberFormatException) { 0 }`.
- `s.toIntOrNull()` and friends exist precisely to avoid exception-driven parsing in a loop; throwing costs a stack trace fill, which is orders of magnitude more expensive than a null check.
- Chain causes: `throw RepositoryException("loading user $id", cause = e)`. A rethrow that drops the cause deletes the only useful part of the report.
- Custom exceptions: extend `Exception` (or a domain base class), keep them few, and never use exceptions for control flow across layers.
- `finally` runs on every path, including cancellation; a `return` inside `finally` swallows the pending exception — never return from `finally`.

## Coroutine Exception Routing

- `launch` propagates a failure to its parent immediately; the parent cancels its other children and fails in turn, unless it is a supervisor.
- `async` stores the failure in the `Deferred` and rethrows it at `await()`. An `async` whose result is never awaited inside a `supervisorScope` swallows the failure completely.
- `coroutineScope { }` rethrows the first child failure to its caller after cancelling the siblings — this is the shape that makes `try/catch` around a parallel block work.
- `supervisorScope { }` isolates children, which means the failure has nowhere to go: each child needs its own handler.
- `CoroutineExceptionHandler` is consulted only for uncaught failures of a *root* coroutine in a scope. Installed on a child, it is ignored. It cannot be used with `async` at all.
- `CancellationException` is invisible to all of the above: it is normal termination, not a failure, and it must be rethrown if caught (SKILL.md rule 5).
- `runCatching` catches `Throwable`, which means `CancellationException`, `OutOfMemoryError` and `StackOverflowError` too. Inside coroutines use it only with an immediate rethrow of cancellation, or write the explicit `catch`.

```kotlin
// Safe wrapper when the codebase insists on runCatching in suspend code
suspend inline fun <T> catching(block: () -> T): Result<T> =
    try { Result.success(block()) }
    catch (e: CancellationException) { throw e }
    catch (e: Exception) { Result.failure(e) }
```

## Flow Error Handling

- Exception transparency: a `flow { }` builder must not catch exceptions of its own downstream. Wrapping `collect` in `try/catch` catches both upstream and collector failures and hides which one happened.
- `catch { }` handles failures from *upstream* only, and can emit a fallback value (`catch { emit(Cached) }`).
- Ordering matters: `.catch { }` placed before `.map { }` does not see the map's failure. Put the operator where the failure boundary is.
- `retryWhen { cause, attempt -> attempt < 3 && cause is IOException }` with a backoff `delay` gives bounded retry; a bare `retry()` loops forever on a deterministic bug.
- `onCompletion { cause -> }` sees normal completion (`cause == null`), failures, and cancellation — check the cause before logging "finished".
- A failure inside `collect { }` is the collector's, not the flow's: it propagates to the collecting coroutine, and the flow is cancelled.

## Logging And Reporting

- Log at the boundary that decides — once. An exception logged at every layer produces four reports of one incident and hides the actual handler.
- Never log a caught exception and continue as if it succeeded: either handle it (return a typed failure) or rethrow it wrapped.
- Redact before logging: `toString()` on a data class prints every field, including tokens and passwords — override it on anything that reaches a log.
- Crash reporting on a coroutine-heavy app needs an explicit handler at each scope root, or failures die inside cancelled scopes with no report.

## Review Checklist

- Every `catch` in suspend code rethrows `CancellationException` first.
- No `catch (e: Exception) { }` with an empty or log-only body on a path that then continues.
- Every `async` result is awaited, or the failure is deliberately dropped with a comment.
- Public API failures are typed where the caller can act on them, thrown where they cannot.
- `catch` operators sit at the right position in each flow chain, and no `try/catch` wraps a `collect`.
- Every rethrow carries `cause`.
