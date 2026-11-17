# Coroutines — Scopes, Cancellation, Dispatchers

A coroutine bug is almost always one of four things: the wrong scope (it leaks), non-cooperative cancellation (it will not stop), the wrong dispatcher (it blocks something), or a swallowed `CancellationException` (it lies about finishing). Stream behaviour, exception routing and coroutine testing each have their own guide — route from the Quick Reference in SKILL.md.

## Symptom → Cause

| Symptom | First check | Cause |
|---|---|---|
| Work continues after the screen/request is gone | Which scope started it | `GlobalScope`, or a scope nobody cancels (SKILL.md rule 3) |
| `cancel()` returns but the job keeps running | Is there a suspension point in the loop | Cancellation is cooperative (SKILL.md rule 4) |
| UI freezes / request thread pinned | Is the blocking call inside `withContext(Dispatchers.IO)` | Blocking call on `Main` or `Default` |
| Parent never completes | Any child in an infinite loop, or a `Job()` created manually and never completed | A child of the scope is still active |
| Exception disappears | Was it `async` without `await`, or a `catch (Exception)` | Deferred failure, or swallowed cancellation |
| Everything runs sequentially despite `async` | Is `await` called inside the loop | `async(...).await()` in the same iteration is just a suspend call |
| Deadlock under load with a fixed pool | `limitedParallelism` value vs pool size | More coroutines waiting than the resource allows (rule 7) |
| Test hangs forever | Which dispatcher the code under test uses | A hard-coded real dispatcher running inside a virtual-time test |

## Scope Ownership

- A scope has one job: to die at a known moment. Every coroutine started inside it dies with it.
- `coroutineScope { }` — suspends until all children finish; a child failure cancels the siblings and rethrows to the caller. The default for parallel decomposition inside a suspend function.
- `supervisorScope { }` — same lifetime, but a child failure is isolated. Use when partial results are acceptable; every child then needs its own `try/catch`, because failures no longer propagate upward.
- `CoroutineScope(SupervisorJob() + Dispatchers.Default)` in a class means you own the cancellation: write the `cancel()` call in the teardown path *first*, then use the scope.
- `withContext(ctx)` is not a new scope's lifetime — it is the same coroutine on another context; it suspends until its body completes and rethrows normally.
- `GlobalScope` is defensible for exactly one thing: process-lifetime work in a `main` that would otherwise exit. In a library or a UI it is a leak.

## Cancellation

- Cancellation propagates down (parent cancels children) and, for a failure, up (a failing child cancels the parent unless a supervisor intervenes).
- Every suspension point in `kotlinx.coroutines` checks for cancellation and throws `CancellationException`. Pure CPU loops check nothing: add `ensureActive()` at the top of the iteration, or `yield()` when you also want to let peers run.
- `isActive` is the polling form for a loop that must exit gracefully rather than throw: `while (isActive) { … }`.
- `CancellationException` is normal control flow: it is not reported to a `CoroutineExceptionHandler`, and it must be rethrown if you catch it (SKILL.md rule 5).
- Cleanup in `finally` runs, but a *suspending* cleanup in a cancelled coroutine throws immediately. Wrap it: `finally { withContext(NonCancellable) { closeSession() } }` — and keep that block short, because it is uncancellable by definition.
- Blocking, uninterruptible calls (a legacy JDBC driver, a native SDK) cannot be cancelled. `withTimeout` around them expires the coroutine while the thread stays busy — bound them with the library's own timeout as well.
- `withTimeout` throws `TimeoutCancellationException`; `withTimeoutOrNull` returns null. Prefer the null form for expected slowness, the throwing form when a timeout is a bug worth a stack trace.

## Dispatchers

| Dispatcher | Parallelism | For |
|---|---|---|
| `Dispatchers.Default` | CPU cores, minimum 2 | Parsing, sorting, image work, anything CPU-bound |
| `Dispatchers.IO` | 64 threads by default (`kotlinx.coroutines.io.parallelism`), and it can grow beyond `Default`'s pool because they share threads | Blocking I/O, JDBC, file access, legacy callbacks |
| `Dispatchers.Main` | 1 | UI state, view access |
| `Dispatchers.Unconfined` | Caller's thread until the first suspension | Tests and operator plumbing only, never business logic |
| `limitedParallelism(n)` view | n | Matching a bounded resource: connection pool, rate-limited API, single-writer file |

- Suspend functions are expected to be main-safe: the *function* moves to the right dispatcher internally (`suspend fun load() = withContext(io) { … }`), so callers never have to know. A suspend function that requires the caller to pick a dispatcher is a leaky API.
- `withContext` on the same dispatcher is nearly free but not free — do not wrap every call; wrap the boundary where the work changes nature.
- `Dispatchers.IO` at 64 threads is a *thread* limit, not a concurrency budget: 200 coroutines hitting a 10-connection pool will occupy 64 threads waiting. `Dispatchers.IO.limitedParallelism(10)` keeps 10 in flight and the rest cheap and suspended.
- Never construct one `Executors.newFixedThreadPool(...).asCoroutineDispatcher()` per call — it allocates threads that nothing closes. Create it once and `close()` it in teardown.

## launch vs async vs withContext

- `launch` returns a `Job`: fire-and-track. An exception propagates to the parent immediately.
- `async` returns a `Deferred`: the exception is stored and rethrown at `await()` — an `async` whose result nobody awaits inside a `supervisorScope` can hide a failure entirely.
- Parallel decomposition, both required: `coroutineScope { val a = async { one() }; val b = async { two() }; a.await() + b.await() }`. Latency = max(one, two), not the sum.
- `async { … }.await()` back to back on one line is a suspend call with extra allocation — write the plain call.
- `awaitAll(listOf(d1, d2))` fails fast on the first failure and cancels the rest; `map { runCatching { … } }` collects per-item outcomes instead (rethrow cancellation inside — SKILL.md rule 5).

## Shared State

- Coroutine confinement beats locking: keep mutable state inside one coroutine, or behind a `StateFlow`'s atomic `update`.
- `Mutex.withLock` is the suspend-aware lock. `synchronized` blocks the thread; a coroutine that suspends while holding a monitor can starve the whole dispatcher.
- `AtomicInteger`/`AtomicReference` remain correct and cheapest for single-variable counters.
- `MutableStateFlow.update { }` retries on conflict and is the only safe read-modify-write; `.value = .value + 1` loses updates under concurrency.
- `CoroutineContext` elements are inherited by children: a `ThreadLocal` is not. To carry request context (MDC, tracing, security), use `ThreadContextElement`-based integrations, added to the context of the scope.

## Bridging Callback And Blocking APIs

- One-shot callback → `suspendCancellableCoroutine { cont -> api.request(cb); cont.invokeOnCancellation { api.cancel() } }`. Missing `invokeOnCancellation` means cancellation frees the coroutine but not the underlying work.
- A callback that fires more than once must become a `Flow` (`callbackFlow`), never a continuation — resuming a continuation twice throws `IllegalStateException`.
- Blocking library → `withContext(Dispatchers.IO) { blockingCall() }`, plus that library's own timeout.
- Exposing coroutines to Java or RxJava callers: `future { }` (kotlinx-coroutines-jdk8) and the `kotlinx-coroutines-rx*` adapters are the supported bridges; hand-rolled bridges lose cancellation.

## Debugging A Running Coroutine

- Default stack traces stop at the dispatcher: the frames above the suspension are gone. Debug mode restores the caller chain — it turns on with `-Dkotlinx.coroutines.debug`, and automatically when the JVM runs with assertions enabled (`-ea`).
- Name your coroutines: `launch(CoroutineName("sync-orders"))` puts the name in thread dumps, debug output and IDE views — the cheapest way to identify one of forty suspended jobs.
- `kotlinx-coroutines-debug` adds `DebugProbes`: `DebugProbes.install()` then `DebugProbes.dumpCoroutines()` prints every live coroutine with its state and creation site. This is the tool for "something is still running and I do not know what".
- "It hangs" is usually a job waiting on a child: walk `job.children` (or dump the coroutines) rather than guessing which `await` is stuck.
- A suspended coroutine consumes no thread, so a thread dump alone shows an idle process while the work is stalled. Absence of busy threads is not evidence that nothing is pending.
- Enable coroutine debugging in test runs too: a leaked coroutine that only shows up under load is usually visible in the dump of a single test.

## Review Checklist

- Every scope in a class has a matching `cancel()` on the teardown path.
- Every CPU loop longer than a few milliseconds calls `ensureActive()` or `yield()`.
- Every blocking call is inside `withContext` with a dispatcher sized for the resource.
- Every `catch` around suspend code rethrows `CancellationException` first.
- No `async` whose `Deferred` is dropped, and no `runBlocking` outside `main` and tests.
- Dispatchers are injected, not hard-coded, in anything that will be tested.
