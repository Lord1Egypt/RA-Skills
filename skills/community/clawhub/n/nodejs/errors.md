# Errors — Classification, Boundaries, and Shutdown

## Classify First

- Operational errors (ECONNRESET, ENOENT, invalid input, upstream 503) get retry, degrade, or report; programmer errors (TypeError, failed assertion, impossible state) get a crash and a clean restart (→ SKILL.md rule 2). A catch-all that "recovers" from both keeps corrupted state serving traffic.
- The test that settles the argument: after catching this, can you name exactly what is still consistent? If not, it is a programmer error and the honest move is to exit.
- Branch on `err.code` (ENOENT, ECONNRESET, EADDRINUSE), never on `err.message` — messages change between Node versions; codes are the contract.
- `err.cause` chains context without losing the root: `throw new Error('config load failed', { cause: err })` (node >=16.9). Print chains with `console.error(err)` or `util.inspect(err, { depth: null })`; a bare `err.message` shows only the outermost layer.
- `AggregateError` from `Promise.any` and `AbortSignal.any` carries `.errors` — logging `.message` alone throws away every actual failure.

## Error Types You Define

- One base class per boundary, not per error: `AppError` with `code`, `status`, and `expose` covers a whole service. Fifty subclasses is a taxonomy nobody keeps consistent.
- Attach machine-readable fields (`code`, `resource`, `attempt`), never a pre-formatted sentence — the caller decides the wording, the log wants structure.
- `Error.captureStackTrace(this, this.constructor)` in a custom error's constructor removes the constructor frame, so the stack starts where the error was actually raised.
- Throw only Errors. A thrown string has no stack, breaks `instanceof`, and exits 1 with an empty trace (→ `debug.md`).
- `expose: true` marks the messages safe to return to a client; everything else surfaces as a generic message plus a correlation id. Leaking a driver error to an HTTP client leaks your schema.

## Boundaries

- Every entry point needs exactly one error boundary: the HTTP error middleware, the queue consumer's wrapper, the CLI's top-level catch, the worker's `'error'` handler. Between boundaries, let errors propagate — a catch that only re-logs and rethrows adds noise and hides the stack's origin.
- An `'error'` event with no listener throws — every EventEmitter and every stream needs one (or `pipeline()`, which wires all of them).
- Unhandled rejection terminates the process by default (node >=15). Every await chain ends in a catch, a route handler, or a deliberate `.catch(noop)` on a fire-and-forget you have thought about.
- `process.on('uncaughtException' | 'unhandledRejection')`: log, flush, exit. After an uncaught throw, program state is unknown; these hooks are for cleanup, not recovery. A handler that logs and continues converts a crash into a slow corruption.
- Never let the boundary itself throw: an exception inside `uncaughtException` exits with code 7 and no useful output.
- `AbortError` at a boundary is not a failure — it means someone cancelled. Count it separately or your error rate tracks client behavior.

## Retries and Degradation

- Retry only what is idempotent and only on transient causes (connection errors, 5xx, 429). Retrying a 4xx repeats the same failure forever; retrying a non-idempotent POST on timeout can duplicate the effect (→ `http.md`).
- Exponential backoff with jitter, bounded attempts, and a total budget under the caller's own timeout — the ladder in SKILL.md exists so a retry storm cannot outlive the request that started it.
- Degrade explicitly: a cached value, a partial response, or a documented empty result is a decision. An empty array returned from a `catch` block is a bug that reports success.
- Log the final failure once, at the boundary, with the attempt count — logging every attempt at every layer multiplies one incident into thousands of lines.

## Graceful Shutdown (order matters)

1. On SIGTERM: fail the readiness probe first, so the balancer stops sending traffic. Keep serving for a moment — the probe interval, not zero — before step 2, or you drop the requests already in flight toward you.
2. `server.close()` — stop accepting, let in-flight requests finish; close idle keep-alive sockets so pooled clients do not hold the process open (→ `http.md`).
3. Start an unref'd force-exit timer as backstop, shorter than the orchestrator's kill window (Kubernetes `terminationGracePeriodSeconds` defaults to 30 s → force-exit at 25 s, per SKILL.md's Timeout Ladder).
4. Stop consumers before producers: pause queue/cron consumers, await in-flight work, THEN close DB pools and queues — closing pools first makes step 2's surviving requests fail at the finish line.
5. Terminate workers, child processes, and cluster workers (→ `concurrency.md`); a live handle keeps the loop alive and turns a clean exit into a SIGKILL.
6. Flush the logger and any telemetry exporter — buffered logs are lost otherwise, and the shutdown you most need to read is the one that went wrong.
7. Set `process.exitCode = 0` and let the loop drain. `process.exit(1)` truncates pending stdout/log writes; reserve `exit()` for the backstop timer.

Signals worth handling: SIGTERM (orchestrator stop, the main path), SIGINT (Ctrl-C, same path, exit 130), SIGHUP (reload config if you support it). SIGKILL and SIGSTOP cannot be caught. As PID 1 in a container there are no defaults at all — without a handler, SIGTERM is ignored entirely (→ `production.md`).
