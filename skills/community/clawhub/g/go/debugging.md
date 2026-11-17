# Debugging — Panics, Hangs, Races, and Live Processes

Go's runtime is unusually forthcoming: it will hand you every goroutine's stack on request. Most Go debugging is knowing which lever produces that dump and how to read it.

Sections: Read The Panic First · Hangs: Dump The Goroutines · The Race Detector · GODEBUG · pprof For Diagnosis · Delve · Bisecting And Reproducing · Common Mistakes

## Read The Panic First

```
panic: runtime error: index out of range [5] with length 3

goroutine 42 [running]:
main.process(0xc0000140a0, 0x3)
    /app/process.go:88 +0x1f5
main.handle(...)
    /app/handler.go:31
```

- The **first** line names the failure and, for index/slice errors, both numbers involved. Read it before opening any file.
- The stack is newest-first: the top frame panicked, the bottom frame started the goroutine. The interesting line is usually the topmost one inside your own module.
- `goroutine 42 [running]` — the bracketed word is the state. On a full dump the states are the diagnosis: `chan receive`, `chan send`, `select`, `semacquire` (waiting on a mutex), `IO wait`, `sync.WaitGroup.Wait`.
- `created by main.serve in goroutine 7` at the bottom of a goroutine's stack tells you who started it, which is what you need for a leak.
- `GOTRACEBACK=all` prints every goroutine, not just the panicking one; `GOTRACEBACK=system` adds runtime frames. Set it in production containers — the default hides the goroutines you need.
- `fatal error:` instead of `panic:` means the runtime killed the process directly: no defer ran, no `recover` was possible (SKILL.md "Panics And Fatal Errors").

## Hangs: Dump The Goroutines

| Situation | How to get the dump |
|---|---|
| Foreground process | `Ctrl-\` (SIGQUIT) — prints all stacks and exits |
| Background/containerized process | `kill -QUIT <pid>` |
| Service with pprof mounted | `curl localhost:6060/debug/pprof/goroutine?debug=2` — full stacks, process keeps running |
| Test that hangs | Wait for `-timeout` (default 10 minutes) — the panic includes every stack |
| Programmatically | `pprof.Lookup("goroutine").WriteTo(w, 2)` |

Reading a deadlock from the dump: find two or more goroutines in `chan send`/`chan receive`/`semacquire` and trace what each is waiting for. A goroutine blocked on `semacquire` names the mutex's holder indirectly — the holder is the goroutine that is *not* blocked but is doing something slow.

`fatal error: all goroutines are asleep - deadlock!` only fires when **every** goroutine is blocked. A server with a live listener never qualifies, so partial deadlocks in production are silent forever and the dump is the only way to see them (`concurrency.md`).

## The Race Detector

- `go test -race ./...` and, for staging, `go build -race`. It costs roughly **2-20× in CPU time and 5-10× in memory** (the documented range), which is why it runs in CI and staging rather than production.
- It detects only races that **actually executed**. Passing under `-race` proves nothing about untested paths.
- A report has two stacks. The lower one — "Previous write at ... by goroutine N" — is the access that happened first and usually the one missing a lock. The "created by" lines at the bottom of each identify the spawn sites.
- `-race` also detects some misuse the compiler cannot: unsynchronized map access, and races on interface and slice headers that look atomic but are two words.
- Only under `-race`, `GORACE="halt_on_error=1"` stops at the first report, which keeps the output readable in a noisy suite.
- A race that "goes away with a Sleep" is still there. So is one masked by adding an atomic to only one of the two sides (`concurrency.md`).

## GODEBUG

| Setting | Shows |
|---|---|
| `GODEBUG=gctrace=1` | One line per GC: heap before/after, goal, pause, CPU share (`memory.md`) |
| `GODEBUG=schedtrace=1000` | Scheduler state every second: runnable queues, idle Ps, syscall counts |
| `GODEBUG=scheddetail=1` | Per-P and per-goroutine detail alongside schedtrace |
| `GODEBUG=inittrace=1` | Time and allocation of every package `init` — the first stop for slow startup |
| `GODEBUG=http2debug=1` (or `=2`) | HTTP/2 frame-level logging (`http.md`) |
| `GODEBUG=madvdontneed=1` | Return freed memory to the OS sooner, so RSS reflects the heap |

`GODEBUG` also carries **compatibility switches**: a Go upgrade that changes behavior usually ships a `GODEBUG=<name>=<old>` escape hatch so you can bisect a regression across the upgrade before fixing it properly (`versions.md`).

## pprof For Diagnosis

```go
import _ "net/http/pprof"    // registers on http.DefaultServeMux — do NOT expose publicly

go func() { log.Println(http.ListenAndServe("localhost:6060", nil)) }()
```

- Bind it to localhost or an internal-only listener. Importing the package and then serving `http.DefaultServeMux` on your public port publishes heap dumps and command lines to the internet (`security.md`, `http.md`).
- `goroutine?debug=2` for full stacks, `goroutine?debug=1` for the grouped-by-stack summary — the summary is what tells you "4,812 goroutines all blocked on the same line", which is a leak diagnosis in one screen.
- `/debug/pprof/heap` for what is retained, `/debug/pprof/profile?seconds=30` for CPU, `/debug/pprof/block` and `/debug/pprof/mutex` for contention (both need explicit enabling: `runtime.SetBlockProfileRate`, `runtime.SetMutexProfileFraction`).
- Interpreting these profiles: `performance.md` for CPU and allocation, `memory.md` for retention.

## Delve

- `dlv debug ./cmd/app -- --flag=value`, `dlv test ./pkg`, `dlv attach <pid>`, `dlv exec ./binary`.
- Commands worth knowing: `break pkg.Func`, `condition <id> i == 500`, `continue`, `next`, `step`, `stack`, `locals`, `print expr`, `goroutines`, `goroutine <n> stack`.
- `goroutines -t` lists every goroutine with its stack inside the debugger — the interactive equivalent of the SIGQUIT dump.
- Optimizations and inlining make variables read as `<optimized out>`. Build with `-gcflags="all=-N -l"` when stepping matters; delve does this by default for `dlv debug`.
- Debugging a container: the process needs `SYS_PTRACE` and usually a non-stripped binary — so a production image built with `-ldflags "-s -w"` cannot be debugged in place (`build.md`).

## Bisecting And Reproducing

- Reduce before you investigate: a `main.go` under 30 lines that reproduces the behavior answers most questions on its own and is what you attach to a bug report.
- `git bisect run go test ./pkg -run TestX -count=1` automates the search over commits; `-count=1` is required or the test cache returns a stale pass.
- Flaky tests: `go test -race -count=100 -run TestFlaky ./pkg`, and `-shuffle=on` to expose order dependence (`testing.md`).
- A bug that appears only in CI: compare Go version, GOARCH, `GOFLAGS`, and whether the runner enforces a CPU quota — a 2-core runner exposes races and scheduler assumptions a 10-core laptop never will (`deployment.md`).
- `go build -gcflags='-m'` prints escape-analysis and inlining decisions when the question is "why is this allocating" (`memory.md`).

## Common Mistakes

| Mistake | Consequence | Fix |
|---|---|---|
| Reading the bottom of the stack first | You debug `main` instead of the failing frame | Top frame in your module |
| Default `GOTRACEBACK` in production | Only the crashing goroutine is printed; the blocker is invisible | `GOTRACEBACK=all` |
| Running `-race` in production | 2-20× CPU and 5-10× memory | CI and staging |
| Exposing `net/http/pprof` on the public mux | Heap and goroutine dumps to anyone | Localhost or an internal listener |
| `print` debugging a concurrency bug | The added synchronization hides it | `-race`, then the goroutine dump |
| Bisecting without `-count=1` | Cached results give the wrong commit | `-count=1` in the bisect command |

## Back To SKILL.md

Panic message decoder: SKILL.md "Panics And Fatal Errors". Leak patterns: `concurrency.md`. Profiles and what to do with them: `performance.md`, `memory.md`.
