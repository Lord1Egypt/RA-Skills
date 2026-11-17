# Async — Event Loop, Promises, Cancellation, Context

## Event Loop

- Phase order per turn: timers → poll (I/O) → check (`setImmediate`) → close. `process.nextTick` and microtasks drain between every phase — so recursive `nextTick` starves I/O forever, recursive `setImmediate` doesn't (one per turn).
- Partition long sync loops with `await setImmediate()` from `node:timers/promises` roughly every ~10 ms of work (budget → SKILL.md rule 1). `nextTick` in a loop does NOT yield to I/O.
- `setTimeout(fn, 0)` vs `setImmediate`: inside an I/O callback, setImmediate always runs first; outside I/O their order is nondeterministic — never depend on it.
- Deferring from a cache hit: use `queueMicrotask`, not `nextTick` — same effect, no starvation footgun, portable.
- Timers are a floor, not a promise: `setTimeout(fn, 100)` means "not before 100 ms". Under a blocked loop it fires late by exactly your blocking time — which makes timer drift a free event-loop-health signal.
- Delays are stored in a 32-bit int: anything above 2147483647 ms (~24.8 days) overflows and fires **immediately**. Far-future work needs a rescheduling chain, not one long timer.
- Any pending timer keeps the process alive; `timer.unref()` for background work that must not block exit (→ `debug.md`).

## Promises

- `Promise.all` fails fast but does NOT cancel the losers: they keep running, and their later rejections become unhandled (process terminates by default on node >=15). Attach a no-op `.catch` to survivors or thread an AbortSignal through.
- Same with `Promise.race` timeouts: the slow branch keeps consuming resources. Use `AbortSignal.timeout(ms)` (node >=17.3) so the operation actually stops.
- Choose the combinator deliberately: `all` (every one must succeed, fail fast) · `allSettled` (need every outcome, never rejects — inspect `.status` per entry) · `any` (first success wins; rejects with `AggregateError` only if all fail) · `race` (first settlement wins, including a rejection).
- Sequential `await` in a loop is a decision, not automatically a bug: keep it when order or rate limits matter; otherwise `Promise.all` over capped batches (cap → SKILL.md rule 4).
- Fixed-size batching is not a concurrency limiter: a batch of 10 waits for its slowest member before the next 10 starts, so one slow item idles nine slots. A pool that refills as each task finishes keeps all N in flight and wins by 2-3× on skewed latency.
- Promises are eager. Building the array of 10k promises has already started 10k operations — the limiter must wrap the *creation* of each promise, not the awaiting.
- `return await` is redundant — except inside try/catch, where dropping the await makes the rejection skip your catch, and in stack traces, where it keeps the frame.
- An `async` function that throws before its first `await` still returns a rejected promise. A plain function that returns a promise but throws first throws synchronously — callers that only `.catch()` miss it. Invisible until it isn't.
- Forgotten `await` inside try/catch: the catch never fires; the rejection surfaces as unhandledRejection long after the stack that caused it is gone. Lint: `no-floating-promises`.
- Top-level `await` in ESM blocks every module that imports yours — acceptable for app entry/config, poison in a library.
- A promise nobody settles is a leak with no error message: it retains its closure, the request that created it, and everything they reference, for the life of the process. Every hand-built promise needs a settlement path on the failure branch too.

## Cancellation

- `AbortController` is the single cancellation currency in core: `fetch`, `fs.promises`, `events.once`, `node:timers/promises`, and most modern libraries take `{ signal }`.
- Compose deadlines: `AbortSignal.any([clientSignal, AbortSignal.timeout(3000)])` (node >=20) gives one signal that fires on either client disconnect or timeout.
- Aborting rejects with `err.name === 'AbortError'` — normal control flow, not an incident. Filter it out of error metrics or every client disconnect pages someone.
- Cancellation is cooperative: a signal stops nothing synchronous and nothing that ignores it. Check `signal.aborted` between stages of a long pipeline you wrote yourself.
- Propagate the signal down every layer. A handler that aborts while its database call keeps running has cancelled nothing — it only stopped waiting for the answer.

## Request Context

- `AsyncLocalStorage` (`node:async_hooks`) carries a request id, tenant, or user through an async call tree without threading a parameter through every function. Set it once at the entry point; read it inside the logger.
- Context survives promises, timers, and callbacks — but not a boundary that leaves the process: worker messages, child processes, and queue jobs need the id serialized explicitly.
- `store.run(ctx, fn)` returns whatever `fn` returns, so async functions compose naturally. `enterWith` mutates the current context and leaks across requests easily — prefer `run`.
- The overhead is small and bounded; the alternative (a module-level "current request" variable) is not a tradeoff, it is a bug that only appears under concurrency.

## Callbacks and Events

- Callback errors don't throw — check `if (err)`; try/catch around the call catches nothing.
- Zalgo: an API that calls back synchronously on cache hits and asynchronously otherwise reorders caller logic unpredictably — always defer (`queueMicrotask`) when answering from cache.
- Wrapping callback APIs by hand loses the error argument sooner or later — `util.promisify` respects the `(err, value)` contract; write custom wrappers only for non-standard signatures. `util.callbackify` covers the reverse direction.
- `events.once(emitter, 'name', { signal })` turns a one-shot event into an awaitable with cancellation; `events.on(emitter, 'name')` gives an async iterator over a stream of events — buffered without bound while you are not iterating, so a fast emitter with a slow consumer is a memory leak.
- Emitters never await async listeners: the rejection of an `async` listener is unhandled and the emitter moves on immediately. Wrap the body in its own try/catch, or construct the emitter with `captureRejections: true`.
