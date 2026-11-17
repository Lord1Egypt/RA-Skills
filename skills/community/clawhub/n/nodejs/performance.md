# Performance — Blocking, Memory, and Measurement

## Measure Before You Change Anything

- Decide which of three problems you have before touching code: the loop is blocked (one core pinned, everything slow at once), the process is waiting (loop idle, responses slow — the bottleneck is downstream), or memory is growing (throughput fine until it isn't). The fixes have nothing in common.
- Load-test with a fixed arrival rate, not a fixed concurrency: closed-loop tools slow their own request rate when the server slows, hiding the saturation point you are looking for.
- Report p50 *and* p99. A mean latency that improves while p99 doubles means you moved work into a queue, and the queue is where users live.
- Microbenchmarks lie about JIT warmup, GC timing, and cache effects. Trust an end-to-end measurement of the real path; use a microbenchmark only to compare two implementations of the same hot function you already proved matters.
- Record the number before and after in the same run conditions. "It feels faster" has never survived a second measurement.

## Blocked Event Loop

- Symptom signature: everything slows at once and one core pins at 100%. Confirm with `perf_hooks.monitorEventLoopDelay()` — sustained delay above the 10 ms budget (→ SKILL.md rule 1) means the loop is blocked; flat delay with slow responses means the bottleneck is downstream.
- Usual blockers, in the order they show up in profiles: `*Sync` fs/crypto calls · large `JSON.parse`/`stringify` (tens of MB → hundreds of ms on the loop) · catastrophic regex backtracking (`/(a+)+$/` on `"aaaa…X"` hangs) · tight loops over big arrays · synchronous template rendering of huge collections · `zlib` sync variants.
- Locate it: `node --cpu-prof` (or `--inspect` + DevTools) under real load, then read the widest self-time frames — not the deepest stacks (→ `commands.md`).
- `console.log` to a terminal or file is synchronous on POSIX — hot-path logging blocks the loop; use an async structured logger in request paths (→ `production.md`).
- Parallel-looking fs, `dns.lookup`, zlib, and crypto work serializes on 4 libuv threads (→ SKILL.md rule 3) — "async" is not "concurrent" past the pool size.
- The three fixes, in order of preference: do less work (paginate, index, precompute), yield between slices (`await setImmediate()` every ~10 ms), or move it off the process (→ `concurrency.md`). Rewriting the algorithm beats all three when the loop is blocked by an O(n²) join in JavaScript.

## Memory Leaks — Diagnosis Order

1. Sample `process.memoryUsage()` over time. `heapUsed` climbing across GC cycles = JS-object leak. `rss` climbing while `heapUsed` stays flat = Buffers, native memory, or fragmentation — a different hunt; heap snapshots won't show it.
2. Confirm GC is running: `node --trace-gc`. A sawtooth returning near its old baseline is normal churn; a staircase is a leak. Memory that plateaus high is a cache doing its job, not a leak.
3. Two heap snapshots minutes apart under load (`--inspect` → DevTools Memory, or `--heapsnapshot-signal=SIGUSR2`), compared by retained-size delta per constructor. Retained size, not shallow size, names the owner.
4. Usual JS suspects: module-level Map/array caches (bound them — LRU with a max) · listener arrays (EventEmitter warns past 10 listeners on one event; raising the limit hides the leak, never fixes it) · `setInterval` closures never cleared · promises that never settle · closures captured by a long-lived object · `AsyncLocalStorage` contexts held by an unbounded queue.
5. Usual native suspects: Buffers held in a cache, zlib streams never destroyed, native addon handles, and streams that errored without `destroy()` — descriptors and native buffers both (→ `filesystem.md`).

Containers: set `--max-old-space-size` to ~75% of the container limit (formula and worked numbers → SKILL.md rule 8). Heap equal to the limit guarantees an OOMKill, because RSS = heap + buffers + stacks + native.

## GC Behavior Worth Knowing

- Young-generation collections are frequent and sub-millisecond; old-generation work is what shows up as latency. Objects that survive a couple of young collections get promoted, so a cache of short-lived objects promotes garbage into the expensive space.
- Allocation rate matters more than allocation size: creating a million small objects per second costs more in collection than holding a large buffer.
- Do not tune GC flags before fixing allocation behavior. `--max-semi-space-size` and friends are for measured, reproduced cases; as a first move they usually make throughput worse while looking like they helped.
- `global.gc()` (needs `--expose-gc`) is a diagnostic — call it between two snapshots to distinguish "not collected yet" from "cannot be collected". It is not a memory management strategy.

## Common Wins, Ranked

1. Remove the work: caching a computed result, paginating a query, or fetching two fields instead of an entire row beats any micro-optimization by an order of magnitude.
2. Fix concurrency: batch N+1 upstream calls, reuse keep-alive connections, cap parallelism so latency stays flat (SKILL.md rules 4 and 5, → `http.md`).
3. Stream instead of buffering: constant memory instead of proportional, and time-to-first-byte instead of time-to-last (→ `streams.md`).
4. Move CPU work off the loop only after the profile proves it is CPU work (→ `concurrency.md`).
5. Micro-optimize last, and only inside the frame the profiler named.

## Startup Time

- Matters for CLIs, serverless, and any autoscaling group that adds instances during a spike. Measure with `node --cpu-prof` on a single run: module loading dominates.
- The cost is the module graph, not your code: lazy-load heavy subsystems with dynamic `import()` and keep the entry file thin (→ `cli.md`).
- Bundling into one file removes hundreds of resolution and read syscalls per start — the one case where bundling a server-side application reliably pays.
- A cold serverless start pays module loading plus first-request JIT: keep the handler's hot path free of first-use initialization (build the client at module scope, not inside the handler).
