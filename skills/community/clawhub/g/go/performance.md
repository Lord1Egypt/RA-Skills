# Performance — Measure, Profile, Then Optimize

Go makes it easy to write code that is fast enough and easy to guess wrong about why it is not. The discipline is fixed: reproduce with a benchmark, profile, fix the top line, re-measure. Anything else is decoration.

## The Loop

1. **Define the number.** p99 latency, throughput, allocations per request, or wall time for a batch. "It feels slow" cannot be optimized.
2. **Reproduce in a benchmark** with realistic input size. A benchmark over 10 items answers nothing about 10 million (`testing.md`).
3. **Profile.** CPU for "it pegs a core", heap for "it eats RAM", block/mutex for "wall time far exceeds CPU time".
4. **Fix the top entry only.** Two changes at once and you cannot attribute the win — or the regression.
5. **Re-measure with `benchstat`.** `-count=10` on both sides; a single pair of numbers on a laptop is noise.

## Benchmarking Honestly

```bash
go test -bench=Encode -benchmem -count=10 ./pkg > old.txt
# change the code
go test -bench=Encode -benchmem -count=10 ./pkg > new.txt
benchstat old.txt new.txt
```

- `benchstat` (golang.org/x/perf) reports the delta with a confidence interval and marks results that are statistically indistinguishable. Reporting a "12% win" from one run before/after is the most common false claim in Go performance work.
- Machine noise dominates small deltas: close other work, disable turbo-variable CPU scaling if you can, and treat anything under a few percent as unproven.
- The compiler deletes calls whose results are unused. `for b.Loop()` (`go >=1.24`) prevents that; below it, assign to a package-level sink (`testing.md`).
- `-benchmem` gives B/op and allocs/op. **allocs/op is the most portable optimization signal in Go** — it barely moves between machines and it maps directly to GC pressure.
- Benchmark the input distribution you actually have. Sorted data, all-cache-hit data, and one-element maps produce numbers that do not survive contact with production.

## CPU Profiling

```bash
go test -bench=. -cpuprofile=cpu.out ./pkg
go tool pprof -http=:8080 cpu.out          # flame graph in a browser
```

- In pprof: `top` for the ranked list, `top -cum` for cumulative cost including callees, `list Func` for line-by-line attribution inside a function, `web` for the call graph.
- **Flat vs cumulative**: flat is time in the function itself, cumulative includes everything it calls. A function with high cumulative and near-zero flat is a router, not a cost — keep descending.
- Sampling profilers miss what does not run on CPU. A service whose wall time exceeds its CPU time is blocked, and the CPU profile will show an idle-looking process — that is the block/mutex profile's job.
- Live service: `go tool pprof http://localhost:6060/debug/pprof/profile?seconds=30` (`debugging.md` for mounting it safely).

## Allocation Profiling

```bash
go test -bench=. -memprofile=mem.out ./pkg
go tool pprof -sample_index=alloc_objects mem.out   # count, not bytes
go build -gcflags='-m' ./...                        # why something escaped
```

- Heap profiles have four sample types: `alloc_objects`, `alloc_space` (everything ever allocated), `inuse_objects`, `inuse_space` (live at the sample). Optimization uses the `alloc_*` views; leak hunting uses `inuse_*` (`memory.md`).
- `-gcflags='-m'` prints "escapes to heap" per line, and `-m -m` explains why. The usual causes: the value is stored in an interface, captured by a closure that outlives the frame, returned by pointer, or too large for the stack.
- Escape analysis is per-function and defeated by indirection: passing a pointer to a function the compiler cannot inline forces the heap.

## The Optimizations That Actually Pay

Ordered by how often they matter:

1. **Do less work.** A better algorithm, an index instead of a scan, one query instead of N. No micro-optimization beats deleting the work (`database.md` for the N+1 case).
2. **Preallocate.** `make([]T, 0, n)` and `make(map[K]V, n)` when the size is known: O(log n) reallocations and copies collapse to one (`collections.md`).
3. **Stop allocating in the hot loop.** Hoist buffers out, reuse them, or pool them. `strings.Builder` instead of `+=` (`strings.md`).
4. **Avoid the interface boxing.** Passing a value as `any` allocates when it does not fit in a word. `fmt.Sprintf` boxes every argument; `strconv` does not.
5. **Batch syscalls.** `bufio.Writer` around a file or socket turns a million write syscalls into a few thousand (`io.md`).
6. **`sync.Pool` for large, short-lived buffers** — after a profile shows the allocation, not before. Entries vanish at GC, so it only helps churn (`concurrency.md`).
7. **Reduce pointers in hot data structures.** `[]Item` is one allocation the GC scans as a block; `[]*Item` is N objects to trace (`structs.md`, `memory.md`).
8. **Parallelize** — last, and only for genuinely independent work. Adding goroutines to a memory-bound loop makes it slower (`concurrency.md`).

## Concurrency Performance

- `GOMAXPROCS` bounds simultaneously running goroutines. In a container it must reflect the CPU quota, not the host's core count — `go >=1.25` derives it from the cgroup limit automatically; below that floor, set it or use an automaxprocs library (`deployment.md`).
- Contention shows up as wall time far above CPU time. Enable the profiles explicitly: `runtime.SetBlockProfileRate(n)` and `runtime.SetMutexProfileFraction(n)` — both sample, and both cost something when enabled.
- Sharding a hot mutex (N locks keyed by hash) is usually a bigger win than switching `Mutex` to `RWMutex`. Measure both (`concurrency.md`).
- False sharing: two atomics on the same 64-byte cache line serialize despite being independent variables. Pad with `_ [64]byte` between them only after the mutex profile points there.
- Channels are not free. A channel used to pass one integer between two goroutines costs far more than a function call; batch items per send when the profile says the channel is the cost.

## Compiler Behavior Worth Knowing

- Inlining is budget-based and gated on function complexity; `-gcflags='-m'` reports "can inline" and "cannot inline: function too complex". A function with a `defer` or a loop was historically much harder to inline — check rather than assume.
- Bounds-check elimination happens when the compiler can prove the index is in range; `_ = s[n-1]` before a loop over `s[:n]` is the classic hint. Verify with `-gcflags='-d=ssa/check_bce/debug=1'` — and only bother in a profiled hot loop.
- `//go:noinline` and `//go:nosplit` exist and are almost never the right answer in application code.
- PGO (profile-guided optimization, `go >=1.21`): drop a CPU profile at `default.pgo` next to `main` and the build uses it for inlining decisions. Reported single-digit-percent gains on real services — cheap to try, not a substitute for fixing the top of the profile.

## Common Mistakes

| Mistake | Consequence | Fix |
|---|---|---|
| Optimizing before profiling | Effort spent where the time is not | Profile first, always |
| One before/after run as evidence | Machine noise reported as a win | `-count=10` + `benchstat` |
| Micro-benchmark with tiny input | Everything fits in L1; conclusions invert at scale | Realistic sizes |
| Reading only `top`, never `top -cum` | The expensive caller is invisible | Read both views |
| `sync.Pool` for everything | Complexity plus a source of stale state | Only after an allocation profile |
| Adding goroutines to a memory-bound loop | Cache thrash makes it slower | Parallelize compute, not memory traffic |
| Chasing bounds checks and inlining first | Days of work for a fraction of one percent | Algorithm and allocations first |

## Back To SKILL.md

GC tuning and retained memory: `memory.md`. Profile endpoints in a live service: `debugging.md`. Benchmark mechanics: `testing.md`.
