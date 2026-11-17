# Concurrency — Goroutines, Channels, and the Leaks They Cause

Concurrency is Go's advertised feature and its main source of production incidents. Almost every bug is one of three shapes: a goroutine with no exit path, shared state with no synchronization, or a channel whose ownership nobody decided.

## Ownership Rules (decide these before writing the code)

- **One owner closes.** The goroutine that sends is the only one allowed to `close`. Receivers never close — that is how `send on closed channel` happens. Multiple senders → nobody closes; signal completion with a separate `done` channel or a `sync.WaitGroup` followed by a single closer.
- **Closing is a broadcast, not a delete.** Receiving from a closed channel returns the zero value immediately and forever; `v, ok := <-ch` with `ok == false` is the only way to tell "closed" from "someone sent the zero value".
- **A nil channel blocks forever** on send and receive — and is *skipped* in `select`. Setting a case's channel to nil is the idiomatic way to disable that case in a loop without restructuring the select.
- **Buffer size is a design statement, not a speed knob.** Unbuffered = a rendezvous, the sender learns the receiver arrived. Buffer of 1 = one unit of slack, the standard shape for "signal without blocking". Anything larger needs a reason you can say out loud (batching, a known burst size); otherwise it only delays the backpressure you wanted.
- **There is no way to kill a goroutine from outside.** Every stop is cooperative: a closed channel, a cancelled context, or a returned loop condition.

## Leak Patterns and Their Fixes

| Leak | What it looks like | Fix |
|---|---|---|
| Send with no receiver | Caller returned early (timeout, error) and the worker is stuck on `ch <- result` | Buffer of 1 on the result channel, or `select { case ch <- r: case <-ctx.Done(): }` |
| Receive with no sender | `for v := range ch` where the producer died before closing | Producer closes in a `defer`; consumer also watches `ctx.Done()` |
| Forgotten `cancel()` | `ctx, cancel := context.WithCancel(...)` in a helper that returns before calling it | `defer cancel()` on the next line (`context.md`) |
| Ticker never stopped | `time.NewTicker` in a function that returns | `defer t.Stop()` (`time.md`) |
| Worker pool with no shutdown | Workers `range` over a job channel that is never closed | Close the job channel once all sends are done — after `wg.Wait()` on the producers |
| Goroutine per request with no ctx | Fire-and-forget background work started in a handler | Derive `context.WithoutCancel(r.Context())` and give it its own timeout (`context.md`) |

Detect them instead of reasoning about them: compare `runtime.NumGoroutine()` before and after in a test, or install a leak checker in `TestMain` that fails the package when the count does not return to baseline (`testing.md`). On a live process a goroutine dump shows the blocked line directly (`debugging.md`).

## select

- Multiple ready cases are chosen **uniformly at random**, not in source order. Code that relies on "the ctx case is listed first so it wins" is wrong: when both a job and cancellation are ready, the job runs roughly half the time. If cancellation must win, also check `ctx.Err()` at the top of the loop body.
- `default` makes the select non-blocking. Inside a `for` loop with no other blocking call that is a spin loop burning a core — a very common accidental CPU pin.
- An empty `select{}` blocks forever with no allocation; useful only to park `main` in a process whose work happens elsewhere.
- Timeouts in a loop: build one `timer := time.NewTimer(d)` outside and `Reset` it, rather than `case <-time.After(d)` inside (`time.md`).

## Mutexes and Atomics

- `sync.Mutex` zero value is ready to use; never copy the struct that holds it. Put `defer mu.Unlock()` on the line after `Lock()` — anything between them is a path where a panic leaves the lock held forever.
- The critical section holds only what needs protection. Doing I/O, logging, or a channel send under a lock converts a fast mutex into a queue; if that call blocks on something that needs the same lock, it is a self-deadlock.
- `sync.RWMutex` helps when readers vastly outnumber writers *and* hold the lock long enough to matter. For microsecond critical sections the extra bookkeeping and cross-core cache traffic often make it slower than a plain `Mutex` — benchmark both before choosing (`performance.md`).
- Typed atomics (`atomic.Int64`, `atomic.Bool`, `atomic.Pointer[T]`, `go >=1.19`) over the old `atomic.AddInt64(&x, 1)` functions: the function form requires the variable to be 64-bit aligned, which is not guaranteed for a struct field on 32-bit platforms and panics there at runtime. The typed structs carry their own alignment.
- Atomic load plus atomic store is **not** an atomic read-modify-write. Two goroutines running `x.Store(x.Load() + 1)` lose increments. Use `Add`, or `CompareAndSwap` in a retry loop.
- `atomic.Value` panics if a later `Store` has a different concrete type than the first. Store one struct type, or use `atomic.Pointer[T]`.
- `sync.Map` is not "the concurrent map". Its own documentation limits it to two cases: a key written once and read many times, or disjoint key sets per goroutine. Anything else — a plain map behind a `Mutex` is simpler and usually faster.

## sync.WaitGroup

```go
var wg sync.WaitGroup
for _, job := range jobs {
    wg.Add(1)                 // before the go statement, never inside it
    go func(j Job) {
        defer wg.Done()       // defer, so a panic still decrements
        process(j)
    }(job)
}
wg.Wait()
```

- `Add` inside the goroutine races with `Wait`: the main goroutine can reach `Wait` before any `Add` runs and return having waited for nothing.
- Reusing a WaitGroup for a second round is legal only after `Wait` returns; overlapping rounds produce `sync: negative WaitGroup counter`.
- With `go >=1.22` the `(job)` parameter is unnecessary — the loop variable is per-iteration. Keep it while the module's `go` directive is lower (`versions.md`).

## errgroup (golang.org/x/sync/errgroup)

The default for "run N things, stop on the first failure":

```go
g, ctx := errgroup.WithContext(ctx)
g.SetLimit(8)                      // bounded parallelism; Go() blocks when full
for _, u := range urls {
    g.Go(func() error { return fetch(ctx, u) })
}
err := g.Wait()                    // first non-nil error; ctx already cancelled
```

- `WithContext` cancels the derived ctx as soon as any function returns non-nil. Functions that ignore `ctx` keep running, so the leak survives `Wait`.
- `Wait` returns only the **first** error. When every failure matters, collect them into a mutex-guarded slice and `errors.Join` at the end (`errors.md`).
- `SetLimit` replaces a hand-rolled semaphore for the common case; the channel form is still right when the limit differs per item class.

## Worker Pools and Backpressure

- Unbounded `go` per item is not a pool: a million items give a million goroutines competing for memory and the scheduler. Bound with `SetLimit`, a buffered semaphore channel (`sem <- struct{}{}` before, `<-sem` after), or N workers ranging over a job channel.
- Pool size: CPU-bound → `runtime.GOMAXPROCS(0)`; I/O-bound → whatever keeps the downstream busy, capped by what the downstream tolerates (database pool size, remote rate limit). More workers than the bottleneck accepts converts a queue into timeouts (`database.md`).
- Backpressure has to reach the producer. A pool that silently drops or buffers turns overload into data loss or unbounded memory; a blocking send is how the producer learns to slow down.
- Fan-in: N producers into one channel, closed by a single goroutine after `wg.Wait()` on the producers. Never `close` from inside a producer.

## Once, Pools, and Singletons

- `sync.Once` for lazy initialization; `once.Do(f)` returns only after `f` completes, so all callers see the finished value. A panic inside `f` still counts as done — the next caller reads an uninitialized value with no error.
- `sync.OnceValue`/`OnceValues` (`go >=1.21`) express "compute once, return it" without a package-level variable.
- `sync.Pool` reduces allocation churn for short-lived objects (buffers), and is not a connection pool or anything with a lifecycle. Entries can disappear at any GC, so a Pool never holds state you need. Always reset what you get: `buf := pool.Get().(*bytes.Buffer); buf.Reset()`.

## Race Detector Discipline

- `go test -race ./...` in CI, on the full suite. It reports only races that actually executed, so test coverage is the limit; a race in a rarely taken branch stays invisible until production.
- A report names two stacks: the current access and the previous conflicting one. The previous stack is usually where the missing lock belongs.
- Fixing a race with `time.Sleep` is not a fix, and neither is adding an atomic to only one of the two accesses — both sides must synchronize.
- Cost of `-race` and how to read the full report: `debugging.md`.

## Back To SKILL.md

Panic messages and their first move: SKILL.md "Panics And Fatal Errors". Cancellation and deadlines: `context.md`. Memory consequences of goroutine growth: `memory.md`.
