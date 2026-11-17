# Context — Cancellation, Deadlines, and Propagation

`context.Context` is Go's only standard mechanism for saying "stop" across goroutine boundaries. It is a signal, not a killer: nothing stops until the receiving code checks it.

## The Four Constructors

| Constructor | Use | Trap |
|---|---|---|
| `context.Background()` | Root in `main`, `init`, tests, and top-level workers | Never as a parameter default deep in a call chain — it silently discards the caller's deadline |
| `context.TODO()` | Marker while migrating code that has no ctx yet | Grep for it before shipping: in production it means "no cancellation ever" |
| `context.WithCancel(parent)` | Manual stop | Leaks parent bookkeeping and any child timer until `cancel()` runs — `defer cancel()` on the next line |
| `context.WithTimeout(parent, d)` / `WithDeadline(parent, t)` | Every network, database, and subprocess call | Timeout is relative to now, deadline is absolute; a retry loop that reuses the same ctx gets less budget on each attempt, which is usually what you want |

`go vet`'s `lostcancel` analyzer catches the common missing-`cancel()` shape. It does not catch a `cancel` stored in a struct and forgotten.

## Propagation Rules

- `ctx` is the **first parameter**, named `ctx`, of every function that can block. Not a struct field, not the second argument, not optional.
- Cancellation flows down only. Cancelling a child never touches the parent; cancelling the parent cancels every descendant.
- The earliest deadline in the chain wins. `WithTimeout(ctx, time.Hour)` on a ctx that expires in 2s expires in 2s — deriving a longer timeout from a shorter parent does nothing.
- **Never store a Context in a struct.** It freezes one call's deadline into a long-lived object; two callers with different deadlines then share whichever one constructed the struct. The documented exception is a struct that *is* one request's parameters, created and discarded per call.
- Background work that must outlive the request: `context.WithoutCancel(ctx)` (`go >=1.21`) keeps the values and drops the cancellation, then wrap it in its own `WithTimeout`. Without the timeout you have replaced a leak signal with an unbounded goroutine (`concurrency.md`).

## Checking Cancellation

```go
select {
case <-ctx.Done():
    return ctx.Err()          // context.Canceled or context.DeadlineExceeded
case v := <-work:
    return use(v)
}
```

- In a CPU-bound loop with nothing to select on, poll: `if err := ctx.Err(); err != nil { return err }` at the top of each iteration or each batch. Polling every iteration of a tight numeric loop costs more than the work; poll per chunk.
- `ctx.Done()` on a `Background` context returns nil, which blocks forever in a select — that is correct behavior, not a bug, and it is why a `select` with only `ctx.Done()` and no other case can hang.
- Distinguish the two errors: `errors.Is(err, context.DeadlineExceeded)` means "we were too slow, maybe retry with a longer budget"; `context.Canceled` means "the caller went away, do not retry" (`errors.md`).
- `context.Cause(ctx)` (`go >=1.20`) returns the error passed to `WithCancelCause`, which is how you tell *which* of several racing conditions cancelled the tree. `ctx.Err()` still returns the generic `Canceled`.
- `context.AfterFunc(ctx, f)` (`go >=1.21`) runs `f` in its own goroutine when ctx finishes — the clean way to attach cleanup to a cancellation without a watchdog goroutine you wrote yourself.

## Server and Client Wiring

- `r.Context()` is cancelled when the client disconnects or the server closes the connection. Handlers that ignore it keep computing for a caller that already left — under a retry storm that is how a service melts (`http.md`).
- Pass `r.Context()` into every database query, outbound request, and worker the handler starts. `db.QueryContext(ctx, ...)`, `http.NewRequestWithContext(ctx, ...)`.
- A per-handler timeout belongs in middleware (`http.TimeoutHandler` or your own `WithTimeout`), so the deadline exists even when a handler forgets.
- Outbound: the ctx deadline and the `http.Client.Timeout` are separate ceilings and the tighter one wins. Set both — the client timeout is the backstop for code paths that pass `Background`.
- Graceful shutdown is a context handoff: signal → cancel the root ctx → `srv.Shutdown(shutdownCtx)` with its own bounded timeout so a stuck handler cannot block exit forever (`deployment.md`).

## Context Values

`context.WithValue` is for request-scoped data that crosses API boundaries and belongs to no parameter: request ID, trace span, authenticated principal. It is not a way to avoid function arguments.

```go
type ctxKey struct{}                      // unexported type, zero size

func WithUser(ctx context.Context, u *User) context.Context {
    return context.WithValue(ctx, ctxKey{}, u)
}
func UserFrom(ctx context.Context) (*User, bool) {
    u, ok := ctx.Value(ctxKey{}).(*User)  // comma-ok: a miss returns nil, not a panic
    return u, ok
}
```

- The key must be an unexported named type, never a string or an int: two packages using `"user"` overwrite each other with no compile error and no runtime signal.
- Always return through comma-ok accessors. A bare `ctx.Value(k).(*User)` panics with `interface conversion` when the middleware that sets it is not installed on that route (`interfaces.md`).
- Lookup walks the chain from newest to oldest, so a value is O(depth) to read. Deep chains in a hot path are measurable; hoist the value into a local once per request.
- Values are immutable by construction — `WithValue` returns a new ctx. Mutating a pointer you stored inside is a data race shared by every goroutine holding that ctx (`concurrency.md`).

## Common Mistakes

| Mistake | Consequence | Fix |
|---|---|---|
| `context.Background()` inside a library function | The caller's timeout is ignored; the call can hang past every SLA | Take `ctx` as the first parameter |
| `cancel` returned to the caller but never called | Timer and child contexts stay alive until the parent ends | `defer cancel()`, or document the handoff loudly |
| One ctx reused across retries | Second attempt starts with whatever budget is left, third with none | Derive a fresh `WithTimeout` per attempt from a parent that bounds the whole operation |
| Deadline set on a slow batch job at request time | Job dies mid-write when the HTTP request ends | `WithoutCancel` + a job-sized timeout |
| Passing ctx to a function that never checks it | Cancellation is a no-op; the goroutine outlives the request | Check `ctx.Done()` in the loop, or use an API that takes ctx |
| `ctx.Value` for optional configuration | Untyped, invisible in signatures, breaks when middleware order changes | Explicit parameters or a struct field |

## Back To SKILL.md

Core Rule 4 states the parameter and `defer cancel()` requirement. Goroutine exit paths: `concurrency.md`. Timeout values for HTTP: `http.md`.
