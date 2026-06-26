---
name: high-performance-coding
description: Use when writing or optimizing performance-critical code — batch processing, concurrent/parallel systems, async pipelines, GPU computing, scientific computing, or any code where throughput, latency, or resource efficiency matters. Also trigger when the user mentions "performance", "optimize", "scale", "concurrency", "make it faster", "speed up", "throughput", "latency", "GPU", "memory bound", "CPU bound", "checkpoint", "resume", "断点续传", "中断恢复", "idempotent", or asks about resource usage or making long-running tasks resumable. This skill encodes universal performance principles distilled from real systems — resource-aware parallelism, async pipeline design, GPU acceleration, interruption-tolerant computation, lock-free data structures, and progressive validation.
---

# High-Performance Coding

Universal principles for writing fast, resource-efficient code. These patterns apply across languages and domains — systems programming, scientific computing, data pipelines, and web services.

## Universal Principles

### 0. Identify the Bottleneck First

Before optimizing, answer one question: **is the program compute-bound or bandwidth-bound?**

- **Compute-bound**: the ALUs are the bottleneck. All cores at 100%, instructions are being issued as fast as the hardware can consume them. Solution: reduce instruction count, use SIMD, improve ILP.
- **Bandwidth-bound**: the memory subsystem is the bottleneck. Cores stall waiting for data. Solution: improve data layout, reduce data movement, increase reuse from caches.

A useful mental model is the **roofline**: every operation has an *arithmetic intensity* (FLOPs per byte loaded). Plot that against your hardware's peak compute and peak bandwidth. If your intensity is below the ridge point, you're bandwidth-bound — optimizing compute won't help. If above, you're compute-bound — better caching won't help.

In practice:
- If `perf stat` shows high IPC (> 2) and low cache miss rate, you're likely compute-bound.
- If IPC is low (< 1) and `cache-misses` or `cache-references` are high, you're bandwidth-bound.
- On GPU: high SM utilization + low memory throughput → compute-bound. Low SM utilization → likely bandwidth-bound or launch-overhead-bound.

**Amdahl's Law sets the theoretical ceiling on parallelism.** If a fraction *S* of your program is serial, the maximum speedup with *N* cores is `1 / (S + (1-S)/N)`. For *S* = 10%, infinite cores give at most 10× speedup. This is why finding and shrinking the serial fraction matters more than adding cores — and why the bottleneck (compute, bandwidth, or serial code) dictates the optimization strategy.

**Little's Law connects concurrency to throughput.** `concurrency = throughput × latency`. If each task takes 1 second and you need 100 tasks/s, you need ≥ 100 concurrent workers. Use this to pick `max_workers` from requirements, not guesswork. Combined with Amdahl: the serial fraction limits how much concurrency can actually help.

**This determines everything that follows.** Memory-bound optimizations applied to a compute-bound program add overhead with no benefit. Compute optimizations applied to a bandwidth-bound program don't move the needle. Adding parallelism beyond Amdahl's limit wastes resources. Answer the bottleneck question first.

### 1. Resource-Aware Parallelism

**Before anything: check what the server actually has available right now.** `cpu_count` tells you total cores, not free cores. `total_ram` tells you installed memory, not available memory. Other users, background services, and yesterday's forgotten processes all consume resources. Use `htop` / `free -h` / `nvidia-smi` to see current state, not theoretical capacity. Then pick a strategy:

**CPU-bound workloads:**
- Start conservative: a few workers below the number of *free* cores, not total cores. Watch CPU usage, then increase gradually.
- Python: `ProcessPoolExecutor` for CPU work (the GIL serializes threads on CPU tasks), `ThreadPoolExecutor` for IO waits.
- C++: `std::thread::hardware_concurrency()` returns available cores. `std::execution::par_unseq` (C++17) or OpenMP `#pragma omp parallel for` for loop parallelism.
- Rust: `rayon` with `par_iter()` automatically sizes the thread pool. Use `par_bridge()` for sequential iterators.

**Memory-bound workloads:**
- Check *available* memory (`free -h`, not `total`). Estimate per-worker memory: a worker that loads 2 GB means you can't run 16 of them on 32 GB.
- Stream/iterate instead of materializing. Generators, `Iterator` traits, and lazy pipelines keep memory constant regardless of dataset size.
- GPU memory profiling has its own methodology — see §3.

**IO-bound workloads:**
- Async/await is usually the right answer. But watch for hidden sync calls that block the event loop.
- Connection pools set the real ceiling. A pool of 5 DB connections can't serve 50 concurrent tasks, no matter how many coroutines you spawn.
- Use a `Semaphore(max_concurrent)` gate rather than spawning unlimited tasks. Tune the limit by observing actual resource pressure.

**GPU-bound workloads:**
- Batch size is capped by VRAM. Use gradient accumulation to simulate larger batches: `loss / n_accumulate` then `backward()`, then `optimizer.step()` after every N micro-batches.
- Sparse representation matters enormously. A dense adjacency for N nodes costs O(N²) memory. At N=50K, that's 2.5B entries — even zeros consume memory. Use COO/CSR edge lists.
- Data transfer is async. `tensor.to(device, non_blocking=True)` overlaps CPU→GPU copy with kernel execution when data is pinned.

**Container-bound workloads (Docker/batch evaluation):**
Each container is a resource consumer — memory, disk, CPU. Parallelism strategies:

- **Reuse containers, don't rebuild.** Building a Docker image per task is expensive. Build once, then reset state between runs (`docker exec git checkout HEAD && git clean -fd`). An agent task that shares one container across N modes is N× faster than rebuilding each time.
- **Stale container cleanup before launching.** Previous crashed runs leave `sweb.eval.*` containers sitting around consuming memory. Always run `docker ps -a --filter | xargs docker rm -f` before starting a new batch.
- **Two-level parallelism.** Run instance-level and eval-level as separate pools with different `max_workers`. Instance workers generate predictions (CPU/network-bound), eval workers run Docker containers (memory/IO-bound). They have different bottleneck profiles — tuning them independently avoids contention.
- **ThreadPoolExecutor, not ProcessPoolExecutor.** Docker SDK calls are IO-bound (waiting for `docker exec` or `docker build` to complete). Threads work fine here — the GIL doesn't block waiting on subprocess output.
- **Cap workers to actual tasks.** `max_workers = min(cpu_count, len(tasks))` — spawning 32 workers for 5 tasks wastes thread creation overhead.
- **Pre-compute shared work.** If multiple modes share analysis results, compute them once in a batch before the main parallel phase. Reduces per-container work and avoids redundant API calls.

### 2. Async Pipeline Design

Cross-cutting patterns for async code that apply regardless of framework:

**The event loop must not block:**
Synchronous SDKs (database drivers, HTTP clients, file I/O) stall the entire event loop. Offload them: `asyncio.to_thread()` in Python, `tokio::task::spawn_blocking()` in Rust. One blocked coroutine starves all others.

**Know your framework's concurrency model:**
Not all async primitives are concurrency-safe. Before spawning concurrent tasks, understand what your framework actually supports:
- SQLAlchemy's `AsyncSession` rejects concurrent queries — `asyncio.gather()` on the same session errors. Use separate sessions or serialize.
- `tokio::spawn()` is cheap but spawning 100K tasks holding connections exhausts file descriptors.
- Database connection pools have finite capacity — set `pool_size` and `max_overflow` based on your measured concurrency, not guesswork.

**Test the failure paths:**
What happens when the database is unreachable? When the external API times out? When the semaphore is at capacity? Async error handling often silently swallows exceptions — explicitly test these paths.

**Decouple stages with bounded queues:**
Producer-consumer patterns with `asyncio.Queue(maxsize=N)` or `tokio::sync::mpsc::channel(N)` let stages run at different speeds. Backpressure is automatic — the producer blocks when the queue is full.

**LLM API and embedding throughput:**
When the pipeline calls external AI APIs, throughput is gated by rate limits, latency, and token cost:

- **Batch embeddings, never one-at-a-time.** Every embedding API (OpenAI, Cohere, ChromaDB) supports batched input. Calling `embed(["text1", "text2", ...])` instead of N separate calls can reduce wall time by 10-50×. Test your provider's max batch size — some cap at 96, others at 2048.
- **Prompt caching is the cheapest optimization.** Anthropic's prompt cache has a 5-minute TTL — put the system prompt and long-lived context in `cache_control` blocks. When cache hits, those tokens cost 90% less and skip the model's prefill phase entirely. Structure prompts so the cached prefix stays identical across calls.
- **Parallel API calls with rate-limit awareness.** APIs enforce RPM/TPM limits. Use `asyncio.Semaphore(max_concurrent)` to stay under the limit, and catch 429 responses with exponential backoff. Many SDKs have built-in retry — make sure it's enabled.
- **Pre-compute and cache LLM outputs.** If multiple downstream tasks share an analysis step (e.g., code analysis, paper classification), run it once, cache the result, and reuse. This avoids redundant API cost and latency — the AnalysisAgent pattern from SWE-bench agent eval saves one LLM call per instance per mode.

### 3. GPU Acceleration

Universal GPU programming patterns, applicable whether you use PyTorch, CUDA C++, or JAX:

**Benchmark methodology is not optional:**
1. Warmup: run 5+ iterations before timing. First kernel launch incurs JIT/context init overhead.
2. Synchronize: `cudaDeviceSynchronize()` (CUDA C++) / `torch.cuda.synchronize()` (PyTorch). CUDA ops are asynchronous — without sync you measure launch overhead, not compute time.
3. Profile peak: `cudaMemGetInfo()` (CUDA C++) / `reset_peak_memory_stats()` → `max_memory_allocated()` (PyTorch). Subtract baseline memory.
4. Structure results: record config + metrics + device info as structured data, not printf.

**Memory allocation patterns (CUDA C++):**
- Prefer `cudaMalloc` once, reuse buffers. Runtime allocation inside hot loops is expensive.
- Use pinned (page-locked) host memory (`cudaMallocHost`) for DMA transfers. Enables overlap with `cudaMemcpyAsync` on different streams.
- CUDA streams for concurrency: `cudaStream_t stream; cudaStreamCreate(&stream); kernel<<<grid, block, 0, stream>>>();` — multiple streams can overlap kernel execution with data transfer.

**Reproducibility vs speed:**
- Debugging/tuning: `cudnn.deterministic = True`, `cudnn.benchmark = False`, `manual_seed(seed)`, `cuda.manual_seed_all(seed)`. Slower but outputs are identical run-to-run.
- Production: `cudnn.benchmark = True` (cuDNN auto-tuner picks fastest algorithm). Only works when input shapes are consistent.

**Sparse vs dense is a data property:**
The crossover point where sparse beats dense depends on density, hardware, and operation. Don't guess — benchmark a grid of sizes × densities. For graphs, `edge_index` (sparse) is almost always right when average degree << total nodes.

**Gradient accumulation is the universal solution to "batch doesn't fit":**
Zero gradients once → loop over micro-batches → `loss = loss / n_batches` → `backward()` each → `optimizer.step()` once at the end. The effective batch size is the sum of micro-batches, but peak memory is that of a single micro-batch.

### 4. Validate Before Scaling

The most reliable way to avoid wasting resources:

- **Estimate runtime before committing.** Before `timeout 10m`, run 1-2 iterations of the heavy loop, measure the time, and extrapolate. If one slice takes 150ms and you have 119 slices per epoch × 2000 epochs, that's ~10 hours — not 10 minutes. A 5-second dry run can prevent a multi-hour timeout.
- **Gate everything with a subset parameter.** `max_items=5` before `max_items=5000`. Catch code bugs, config errors, and logic issues on a tiny, fast run. Also catches "this will take all night" before it starts.
- **Maintain a fast test** that exercises the critical path end-to-end in a few seconds. Run it after every change. If it breaks, don't proceed to full scale.
- **Scale progressively.** 5 items → verify output + measure time → 50 items → extrapolate total → full dataset. Each stage gates the next on both correctness AND feasibility.

### 5. Fast Paths for Common Cases

When profiling shows a specific code path dominates, handle it without the general-case overhead:

**Check before locking.**
An atomic counter can tell you "no work to do" without ever touching the lock:
```c
// Wait queue wake: check atomic flag before acquiring the spinlock.
// If num_wakers == 0, there's nothing to wake — skip the lock entirely.
if (atomic_load(&wq->num_wakers, relaxed) == 0)
    return;
spin_lock(&wq->lock);
// ... actual wake logic
```

**Single-owner skip.**
When a reference count is 1, you own the data exclusively:
```rust
// RwArc::get() — if we're the only handle, return &T without any atomic ops.
if self.num_rw.load(Ordering::Relaxed) == 1 {
    return unsafe { &*self.ptr };  // no other thread can observe
}
// Otherwise, fall back to the general (slower) path...
```

**Power-of-two capacities.**
Ring buffer size = 2^n turns modulo into a bitmask:
```c
// idx % capacity   →   idx & (capacity - 1)
// Compiles to a single AND instruction instead of DIV.
buf[tail & (buf->capacity - 1)] = item;
```

**Relaxed memory ordering when safe.**
If your context already provides ordering (preemption disabled, lock held, single-threaded phase), `Ordering::Relaxed` is cheaper than `SeqCst`:
```rust
// Inside a spinlock — lock acquire/release already provides ordering.
// Relaxed is sufficient and generates plain MOV instead of LOCK XADD.
self.counter.fetch_add(1, Ordering::Relaxed);
```

### 6. Memory Access Patterns

Data layout often matters more than instruction count. The gap between CPU speed and DRAM latency has been growing for 40 years — a main memory access costs ~100ns, during which a modern core could execute ~400 instructions.

**Cache lines and false sharing:**
A cache line is 64 bytes on x86/ARM. When any core writes to a cache line, every other core's copy is invalidated. If two threads write to different variables that happen to share a cache line, they destroy each other's cache despite never touching the same data:
```c
// BAD: two ints on the same cache line — threads fight invisibly.
struct {
    int counter_a;  // thread A writes here
    int counter_b;  // thread B writes here — SAME cache line
} __attribute__((packed));

// GOOD: pad to cache line boundaries.
struct {
    alignas(64) int counter_a;
    alignas(64) int counter_b;
};
```
In Rust: `#[repr(align(64))]`. Symptoms: high cache-miss rate on writes, poor scaling beyond 2 threads despite no obvious contention.

**AoS vs SoA:**
When iterating over one field of many objects, Structure-of-Arrays keeps the accessed data contiguous:
```c
// AoS: iterating all x coordinates loads x,y,z into cache for every element.
struct Particle { float x, y, z; } particles[N];

// SoA: three separate arrays. Walking all x touches only x — 3× fewer cache lines.
struct Particles { float *x, *y, *z; };
```
Rule of thumb: if you access all fields together, use AoS (good locality). If you access one field across many objects, SoA wins. GPUs especially punish AoS — coalesced access requires threads in a warp to hit consecutive addresses, and AoS interleaves unused data.

**NUMA awareness:**
On multi-socket machines, memory is attached to specific CPUs. Accessing "remote" memory costs 1.3-2× more latency than "local". When allocating large buffers, allocate them on the NUMA node where they'll be used. In Linux, `numactl --cpunodebind=N --membind=N` pins both. In code, `libnuma` or `numa_alloc_onnode()`.

**Practical rules:**
- Pad shared counters to cache-line boundaries when written by different threads.
- Prefer SoA for hot loops that touch one field across many elements.
- On multi-socket machines, pin threads and allocate memory on the same NUMA node.
- `perf stat -e cache-misses,cache-references` tells you if layout optimization is worth doing at all.

### 7. Error Resilience

Don't let one failure cascade:

- **Timeout every external call.** API, database, subprocess, network — everything needs a deadline. Infinite wait = silent hang.
- **Graceful degradation over crash.** If the premium model errors, fall back to the simple baseline. If semantic search fails, fall back to keyword match. The user gets a result instead of nothing.
- **Retry transient failures, not logic errors.** Network blips and rate limits deserve 2-3 retries with exponential backoff. Validation errors, schema mismatches, and permission denials should fail fast.
- **Catch regressions instantly.** A 2-second fast test that catches a regression saves hours of debugging a full-scale run that silently produces wrong results.

### 8. Design for Interruption

Long-running work should survive crashes, restarts, and partial failures. Five levels of investment, from trivial to production-grade:

**Level 1 — Skip if output exists.** `if os.path.exists(out): return`. One line, makes any script idempotent.

**Level 2 — Track processed IDs.** Save a `processed.json` set, updated after each item. Re-run skips already-done work. For batch processing that takes minutes to hours.

**Level 3 — Structured checkpoints at boundaries.** After each pipeline stage, before external jobs (API calls, Docker, GPU epochs), and before human gates. A JSON row recording: current step, produced artifacts, pending jobs, how to continue.

**Level 4 — Automatic recovery strategy.** Escalate by failure count and type: auto-retry (transient, < 3 attempts) → checkpoint-resume (persistent, roll back) → skip-and-continue (non-critical, log and move on) → manual intervention (critical, pause for human).

**Level 5 — Survive process death.** DB-backed queue (not in-memory) + lease per work item (expired lease = another worker claims it) + graceful shutdown (catch SIGTERM, finish current item, save checkpoint, release locks).

**Core principle:** make the unit of work small enough that restarting from the last checkpoint is cheap. If recomputing from scratch costs 3 hours, create checkpoints more often than every 3 hours. The overhead of saving state is negligible compared to the cost of redoing work.

### 9. Compile-Time Optimization

For compiled languages:

- **Rust**: `lto = true` + `codegen-units = 1` enables cross-crate inlining. `lto = "thin"` for dev builds (most of the benefit, much faster). `panic = "abort"` removes landing pads for smaller binaries and better inlining. Typical: 2-10% speed gain, 2-3× compile time.
- **C++**: `-flto -fwhole-program -fuse-linker-plugin` for GCC/Clang. `-ffast-math` when IEEE compliance isn't needed. `-march=native` to enable instruction sets available on the build machine (AVX2, etc.).
- **Go**: `-ldflags="-s -w"` strips debug info and symbol table. `CGO_ENABLED=0` produces static binaries and avoids cgo overhead. Build with the target's GOARCH for best results — cross-compilation is cheap in Go.

### 10. Data Structures Are Leverage

The right data structure often beats micro-optimization by orders of magnitude:

- **Read-mostly, concurrent**: RCU (Read-Copy-Update) — readers never block, writers clone. Ideal when reads >> writes. ⚠️ *Hard to implement correctly — requires grace period tracking, safe memory reclamation, and preemption control. Use a battle-tested library unless you're writing an OS kernel.*
- **Producer-consumer, bounded**: Lock-free SPSC ring buffer — producer and consumer never contend on the same cache line. ⚠️ *Power-of-two capacity required for bitmask indexing. Validate with TSan before trusting correctness.*
- **Write-heavy storage**: LSM-tree — buffer writes in memory, flush and compact in background. Turns random writes into sequential I/O.
- **Sparse indexing**: Radix tree / XArray — fixed fanout, O(log N) lookup. Good for sparse key spaces. RCU-compatible variants exist for concurrent read access.
- **Large graphs on GPU**: Neighbor sampling (not full adjacency) — sample a fixed number of neighbors per node per layer to keep memory bounded.

The ⚠️ structures are correct only under specific invariants. Without those invariants, they produce silently wrong results — worse than a slow lock.

## When NOT to Optimize

- **Profile before you touch anything.** Without a profiler, you're guessing what's slow. The bottleneck is rarely where you think it is. Run a profiler (perf, py-spy, flamegraph, cProfile, nvprof) and optimize only the functions that actually dominate runtime.
- **If it's already fast enough, stop.** "Acceptable" means within the user's latency expectation or time budget. Don't spend 2 hours optimizing something that runs in 0.1 seconds.
- **One-off scripts don't need infrastructure.** A single-user CLI, a data exploration notebook, a throwaway analysis — these don't need async frameworks, thread pools, or GPU acceleration. The engineering cost outweighs any speed gain.
- **Lock-free code is more dangerous than slow code.** Every lock-free data structure has subtle correctness hazards. Only reach for RCU, SPSC rings, or custom atomics when a lock-based version is measurably too slow AND you've verified the lock-free version under thread sanitizer (TSan).
- **Parallelism without measurement is just complexity.** Don't add threads, async, or multiprocessing without first measuring what the bottleneck actually is. CPU-bound? IO-bound? Memory-bound? The answer determines the fix — guess wrong and you add overhead with no benefit.
- **Last resort, not first instinct.** Algorithmic improvements (better data structure, caching, batching) usually beat micro-optimizations (inlining, loop unrolling, bit tricks) by orders of magnitude. Try the big wins first.

