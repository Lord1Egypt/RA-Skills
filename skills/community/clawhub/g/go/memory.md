# Memory — GC Tuning, Escape Analysis, and Retention

Go's collector is concurrent, non-generational, and non-compacting, with one tuning knob for pace (`GOGC`) and one for a ceiling (`GOMEMLIMIT`). "The GC is slow" is almost always "the program allocates too much" or "the program retains too much" — those are different problems with different fixes.

## How The Pacer Decides

- `GOGC=100` (the default) means: start the next cycle when the heap reaches **2× the live heap** after the previous cycle. The formula is `target = live × (1 + GOGC/100)`. A 200 MB live heap collects again at 400 MB.
- Raising `GOGC` trades memory for CPU: `GOGC=400` collects at 5× live, so fewer cycles and a much larger footprint. Lowering it does the reverse. It is a **ratio**, so a program whose live heap grows also grows its trigger point — which is exactly how a container gets OOM-killed with a "healthy" GC.
- `GOMEMLIMIT` (`go >=1.19`) is a **soft** ceiling on total runtime memory. As the total approaches it, the GC runs more often, and it will not stop the program to enforce it — it is not a hard cap, and it is the right way to say "you have 1 GiB".
- The GC targets about **25% of GOMAXPROCS** for background marking, and a CPU limiter (`go >=1.19`) caps GC at roughly 50% so a program near its memory limit degrades rather than entering an unbounded GC death spiral.
- STW pauses are short by design — sub-millisecond in normal operation — because marking is concurrent. The visible cost of the GC is CPU share and allocation-path assists, not pauses.

## Container Settings

```
GOMEMLIMIT = ~90% of the container memory limit     # leaves room for stacks, the runtime, and non-heap
GOMAXPROCS = the cgroup CPU quota                   # automatic from go >=1.25
```

- Without `GOMEMLIMIT`, a spike in live heap moves the GC trigger above the cgroup ceiling and the kernel kills the process — a `SIGKILL` with no Go-side error, no stack, and no log line (`deployment.md`).
- Do **not** set `GOGC=off` with only `GOMEMLIMIT` unless the live heap is well below the limit and stable. With GOGC off, the limit becomes the sole trigger; if live heap approaches it, the GC runs continuously and the CPU limiter is all that stands between you and a stall.
- On `go <1.25` the runtime read the host's CPU count, so a 0.5-CPU container on a 64-core node ran with `GOMAXPROCS=64`: excessive parallelism, more GC workers than the quota allows, and CPU throttling. Set it explicitly or use an automaxprocs library (`versions.md`).

## Watching The GC

```
GODEBUG=gctrace=1 ./app
gc 12 @3.204s 1%: 0.018+2.1+0.004 ms clock, 0.14+0.5/1.9/0+0.03 ms cpu, 42->43->21 MB, 45 MB goal, 8 P
```

- `42->43->21 MB` is heap-at-start → heap-at-end → **live heap after marking**. The live number is the one to watch: rising steadily = a leak; flat with high churn = an allocation-rate problem.
- `1%` is the cumulative share of CPU spent in GC. Under ~5% the GC is not your problem; sustained double digits means allocation rate or a heap near the limit.
- `45 MB goal` is the pacer's next trigger; compare it with the container limit.
- `runtime.ReadMemStats` gives the same data programmatically but stops the world briefly — sample it at low frequency, or use `runtime/metrics` (`go >=1.16`), which does not.

## Stack vs Heap

- Goroutine stacks start at **2 KB** and grow by copying, up to a default 1 GB limit on 64-bit. That small start is what makes a hundred thousand goroutines viable; unbounded recursion still hits the limit with `stack overflow`.
- Stack allocation is free (bump and pop) and never touches the GC. Heap allocation costs the allocation, the eventual collection, and the pointer scanning in between.
- `go build -gcflags='-m'` reports every escape; `-m -m` explains why. Typical causes: stored in an interface, captured by a closure that outlives the frame, returned as a pointer, too large for the stack, or a size the compiler cannot prove at compile time (`make([]byte, n)` with a variable n).
- Escape analysis is intraprocedural plus inlining. A pointer passed to a function the compiler cannot inline is assumed to escape.

## Retention: Why Memory Does Not Come Back

| Pattern | What is retained | Fix |
|---|---|---|
| Sub-slice of a big buffer | The **entire** backing array | `slices.Clone`, or copy the piece out (`collections.md`) |
| Substring of a big string | The whole string's bytes | `strings.Clone` (`strings.md`) |
| Removing from a `[]*T` by reslicing | The tail pointers still reference the objects | Zero the freed tail, or `slices.Delete` |
| Map that peaked huge | Bucket array never shrinks | Rebuild into a fresh map |
| Long-lived cache with no eviction | Everything ever inserted | Bounded size or TTL; a `map` is not a cache |
| Goroutine blocked forever | Every variable it captured | Give it an exit path (`concurrency.md`) |
| Global slice used as a queue | Grows monotonically | Bounded channel or ring buffer |
| `time.Ticker`/`Timer` never stopped | The timer and its closure | `defer t.Stop()` (`time.md`) |

Diagnose with the **inuse** views of a heap profile: `go tool pprof -sample_index=inuse_space http://…/debug/pprof/heap`. Take two snapshots minutes apart and compare — pprof's `-base` flag diffs them, and the growing entry is the leak (`debugging.md`).

## Reducing Allocation

- Preallocate with a known size: `make([]T, 0, n)`, `make(map[K]V, n)`. One allocation instead of O(log n) grow-and-copy rounds (`collections.md`).
- Reuse buffers across iterations; `sync.Pool` for large short-lived ones, after a profile (`concurrency.md`).
- Value types over pointer types in hot collections: `[]Item` is one GC object; `[]*Item` is N objects to trace. The GC's cost scales with the number of pointers it must follow, not with bytes (`structs.md`).
- A struct with no pointer fields at all is allocated in a pointer-free span the collector never scans — replacing a `string` field with a fixed `[16]byte` in a hot struct can remove it from scanning entirely.
- Avoid boxing: passing a value as `any` allocates unless it fits the optimized cases. `fmt.Sprintf` boxes every argument (`strings.md`).
- Interning repeated strings (a map, or the `unique` package in `go >=1.23`) collapses millions of duplicate keys into one copy each.

## Returning Memory To The OS

- Freed heap is not immediately returned; the runtime keeps it for reuse and hands it back gradually. **RSS stays high after a spike, and that is normal** — the process is not leaking just because the resident size does not drop.
- `GODEBUG=madvdontneed=1` makes the runtime release pages more eagerly on Linux, so RSS tracks the heap more closely at a small cost. Useful when an orchestrator judges you by RSS.
- `debug.FreeOSMemory()` forces a collection and a return. Legitimate after a known one-off spike (a batch import); as a periodic job it is a symptom that `GOMEMLIMIT` was never set.
- Weak pointers (`weak` package, `go >=1.24`) allow caches that do not retain their entries — a real answer to the unbounded-cache pattern, and still niche.

## Common Mistakes

| Mistake | Consequence | Fix |
|---|---|---|
| No `GOMEMLIMIT` in a container | OOM-killed with no Go-side error | Set it to ~90% of the limit |
| `GOGC=off` with only a memory limit | Continuous GC when live heap approaches the ceiling | Keep GOGC on unless measured |
| Reading RSS as heap usage | "Leak" hunts for memory the runtime is holding for reuse | `gctrace` live heap, or `inuse_space` |
| Holding a sub-slice of a huge read | Megabytes retained per small item | Clone the piece |
| `sync.Pool` as a cache | Entries vanish at GC; state disappears | Pool is for churn, not storage |
| Tuning `GOGC` before reducing allocation | Buys memory to hide a fixable allocation rate | Profile allocations first (`performance.md`) |
| Periodic `debug.FreeOSMemory()` | Hides the missing limit and adds pauses | `GOMEMLIMIT` |

## Back To SKILL.md

Allocation-rate optimization: `performance.md`. Goroutine leaks: `concurrency.md`. Container resource wiring: `deployment.md`.
