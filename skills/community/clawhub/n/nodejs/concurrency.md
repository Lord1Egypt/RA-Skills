# Concurrency — Workers, Child Processes, and Cluster

Three mechanisms, three different problems. Picking the wrong one costs either parallelism you never get or complexity you never needed.

| Need | Mechanism | Cost |
|---|---|---|
| CPU-bound work inside this app (hashing, image resize, parsing) | `worker_threads` | ~ms and ~MBs per worker; message copying |
| Run another program, or isolate untrusted/crashy code | `child_process` | Full process: memory, startup, IPC serialization |
| Use N cores for the same server on a machine you own | `cluster` | Shared port, N× memory, N× connection pools |
| I/O concurrency (HTTP, DB, files) | None of the above — the event loop already does it | Adding threads here buys copying, not speed |

## Worker Threads

- Spawning costs milliseconds and megabytes. Pool them (piscina or a hand-rolled fixed pool sized to `os.availableParallelism()`); never spawn per request — under load, spawn cost becomes the bottleneck you were trying to remove.
- `postMessage` structured-clones by default: copying a 100 MB buffer per task erases the parallelism you bought. Pass ArrayBuffers in the transfer list (zero-copy; the sender loses access) or share via `SharedArrayBuffer`.
- Workers do not share the module cache or globals — each one re-executes the module graph, so heavyweight imports multiply memory by worker count. Keep worker entry files thin.
- Each worker has its own heap, and `--max-old-space-size` applies per thread. Under a container limit, budget the sum: main heap + N × worker heap must fit (SKILL.md rule 8), or set `resourceLimits: { maxOldGenerationSizeMb }` per worker.
- An error in a worker with no `'error'` listener is silent from the parent's perspective. Always wire `'error'` and `'exit'`; treat a non-zero exit as a failed task, not a dead pool.
- Workers keep the process alive like any handle: `worker.unref()` or terminate the pool during shutdown, or the process hangs at exit (→ `debug.md`).

## Child Processes

- `execFile(bin, [args])` over `exec(string)`: array arguments never touch a shell, which removes the injection class entirely (→ `security.md`). `spawn` defaults to `shell: false` — keep it.
- `exec`/`execFile` buffer all output with `maxBuffer` at 1 MiB by default; exceeding it kills the child and yields `ERR_CHILD_PROCESS_STDIO_MAXBUFFER` with the output truncated. For anything that can produce real output, use `spawn` and stream.
- The classic hang: `spawn` with `stdio: 'pipe'` and nobody reading. The OS pipe buffer fills (tens of KB), the child blocks on write, your `await` never resolves. Consume both stdout and stderr, or use `stdio: 'ignore'` for the streams you do not want.
- `fork()` is `spawn` for another Node file, with an IPC channel. Messages are JSON-serialized: no functions, no `undefined` values, no cycles, and large payloads cost real CPU on both sides.
- Killing the parent does not kill children. Track them and kill on shutdown; `detached: true` puts the child in its own process group, which is how you kill a whole tree (`process.kill(-child.pid)`) — and how you accidentally orphan one.
- `child.kill()` sends SIGTERM, which a child can ignore. Escalate: SIGTERM, wait a bounded interval, then SIGKILL. Windows has no signal semantics — `kill()` terminates immediately regardless.
- Windows also cannot `spawn` a `.cmd`/`.bat` without `shell: true`; the failure is `EINVAL`. Resolve the real executable, or set `shell: true` only with fully controlled arguments.
- Exit is two events: `'exit'` fires when the process ends, `'close'` when its stdio streams are also finished. Read output on `'close'`, or you read a truncated buffer.

## Cluster

- Only for machines you own entirely (SKILL.md rule 7): under an orchestrator, replicas are the scaling unit and two schedulers hide each other's failures.
- The primary distributes connections round-robin by default on non-Windows; on Windows the OS distributes and can heavily favor one worker.
- Memory multiplies: N workers means N heaps, N connection pools, N caches. A 4-worker cluster with a per-worker DB pool of 10 opens 40 connections — databases have connection limits and each one costs memory server-side.
- In-memory state per worker breaks anything sticky: sessions, rate limit counters, WebSocket subscriptions, and in-process caches all diverge. Move that state out before clustering, not after the bug report.
- The primary must handle worker exits itself: respawn with a backoff, and refuse to respawn if workers keep dying at boot — an unconditional respawn loop is a fork bomb with your own code.
- Zero-downtime reload = restart workers one at a time, each new worker gated on readiness before the next old one is retired.

## Choosing And Sizing

- Default worker count = `os.availableParallelism()` (node >=18.14, cgroup-aware in containers, unlike `os.cpus().length` which reports host cores). One vCPU with 4 workers means 4× memory for the same throughput.
- Measure before parallelizing: if the profile shows the loop is waiting on I/O rather than burning CPU (→ `performance.md`), more threads add copying and scheduling to a problem that is not CPU-bound.
- Cross-cutting rule: any of these mechanisms adds a shutdown obligation. Every worker, child, and cluster worker must be terminated in the drain sequence, or the process refuses to exit and the platform SIGKILLs it (→ `errors.md`).
