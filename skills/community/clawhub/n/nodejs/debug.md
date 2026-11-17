# Debugging — Symptom to Cause in Minutes

Work symptom-first. Each chain is ordered by probability, and every step is a check that returns an answer, not a guess. Node hides its state well: the process is alive, the logs are quiet, and the truth is in the handle table.

## The Universal First Three

1. `node -v` and `node -p "process.execArgv"` — half of "impossible" bugs are a different major or a stray `NODE_OPTIONS` in the shell (`echo $NODE_OPTIONS`).
2. `process.memoryUsage()` and `process.getActiveResourcesInfo()` (node >=17.3) sampled twice, 30 s apart — the first pair separates leak from stall, the second names what is keeping the loop alive.
3. `node --stack-trace-limit=50 --trace-uncaught app.js` — Node truncates stacks at 10 frames by default and reports uncaught throws of non-Errors with no location at all.

## Process Won't Exit

The event loop stays alive while one referenced handle remains. Nothing prints; the shell just hangs.

1. Name the handles: `console.log(process.getActiveResourcesInfo())` in an `exit`-adjacent hook or on a timer — output like `['TCPSERVERWRAP','Timeout']` points straight at the offender.
2. Usual owners, in frequency order: an HTTP server never `close()`d, a database/Redis pool never ended, `setInterval` never cleared, a `readline` interface still open on stdin, a worker or child process still running.
3. Legitimate background timers: `timer.unref()` lets the loop exit while the timer still fires if the process lives (the right fix for metrics flushes and keep-alive pings).
4. Keep-alive sockets hold the server open even after `server.close()`: track sockets and destroy idle ones, or use `server.closeIdleConnections()` (node >=18.2).
5. Last resort to identify, never to fix: `process.exit()` masks the leak and truncates pending writes (→ `errors.md`).

## Process Exits Immediately, Silently, Code 0

- The loop had nothing to do: an `async main()` whose promise was never awaited, or a top-level `await` that resolved before the server bound.
- A `require`/`import` threw inside a `try` that swallowed it, so the setup never ran. Log at the end of bootstrap, not the start.
- `process.exit()` somewhere in a dependency's shutdown path — grep it: `grep -rn "process.exit" node_modules/<pkg>` when a library is suspected.

## Crash Loop Under a Supervisor

1. Get the real exit code (`echo $?`, `docker inspect -f '{{.State.ExitCode}}'`, or the supervisor's log) and decode it against the table in SKILL.md.
2. Code 1 with a stack → application bug. Code 134 with `FATAL ERROR: ... heap out of memory` → heap ceiling (SKILL.md rule 8). Code 137 → the kernel or orchestrator killed it; RSS, not heap.
3. Restart storms hide the first failure: freeze one iteration (supervisor set to no-restart) and read the whole boot log, not the tail.
4. Config drift is the top cause in a container that works locally: `node -p "JSON.stringify(process.env,null,1)"` inside the failing environment, diffed against the working one. Validate env at boot so this fails loudly at second 0 instead of at 3am (→ `production.md`).

## Growing Memory

1. Sample `process.memoryUsage()` every 30 s for 10 minutes under load. `heapUsed` climbing across GC cycles = JS-object leak → heap snapshots. `rss` climbing while `heapUsed` is flat = Buffers, native addons, or fragmentation → snapshots will show nothing.
2. Confirm GC is actually running before calling it a leak: `node --trace-gc` — a sawtooth that returns near its old baseline is normal churn, a staircase is a leak.
3. Heap path: two snapshots minutes apart (`node --inspect` → DevTools Memory, or `--heapsnapshot-signal=SIGUSR2` then `kill -USR2 <pid>`), compare by retained-size delta per constructor.
4. Native path: check Buffer allocation sites, native addons, and `zlib` streams left unclosed — every zlib stream holds native memory until destroyed.
5. Full leak taxonomy and fixes: `performance.md`.

## Everything Is Slow At Once

1. One core at 100% while others idle = the loop is blocked, not overloaded. Confirm with `perf_hooks.monitorEventLoopDelay()`: sustained delay above the 10 ms budget (SKILL.md rule 1) is blocking; flat delay with slow responses means the bottleneck is downstream.
2. Blocked: `node --cpu-prof` for 30 s under load, then read the widest self-time frames — the offender is nearly always a `*Sync` call, a large `JSON.parse`, a regex with nested quantifiers, or a loop over a whole table.
3. Not blocked, still slow: measure the upstream. Add per-call timing around DB and HTTP calls; a slow dependency with no timeout looks exactly like a slow app (→ `http.md`).
4. Neither: check whether "async" work is queuing on the 4 libuv threads (SKILL.md rule 3) — parallel `fs`, `dns.lookup`, `crypto`, and `zlib` serialize past the pool size.

## Works Locally, Fails in CI or Production

Check in this order; each is a one-minute test:

| Difference | Check |
|---|---|
| Node major differs | `node -v` on both sides; compare against the Version Gates table in SKILL.md |
| Case-sensitive filesystem (Linux) vs insensitive (macOS/Windows) | An import whose path differs only in case — resolves locally, `ERR_MODULE_NOT_FOUND` in CI |
| Dev dependency used in production code | `npm ci --omit=dev` locally, then run — the failure appears instantly |
| Env var present locally, absent in CI | Validate the whole env at boot and print the missing names |
| Lockfile not respected | `npm ci`, never `npm install`, in any automated context (SKILL.md rule 6) |
| Native module built for another OS/arch/libc | Rebuild inside the target image; never copy `node_modules` from the host (→ `runtime.md`) |
| Test isolation | Hardcoded ports, shared temp paths, fake timers, file ordering (→ `testing.md`) |
| Locale/timezone | CI runs UTC; assertions on formatted dates flip. Pin `TZ` in both places |

## Port and Connection Failures

- `EADDRINUSE` on restart: the old process still owns it (`lsof -iTCP:3000 -sTCP:LISTEN -n -P` on macOS/Linux, `netstat -ano | findstr :3000` on Windows). In tests, bind port 0 and read `server.address().port`.
- `ECONNREFUSED ::1:3000` while the server "is running": the server bound IPv4 only and the client resolved `localhost` to IPv6 first. Bind `0.0.0.0` or connect to `127.0.0.1` explicitly.
- `ETIMEDOUT` on outbound calls only in the container: DNS or egress rules, not code. Test resolution and reachability from inside that container before touching the app.
- `ECONNRESET` bursts under load: the peer's keep-alive is shorter than yours (SKILL.md rule 5) or you exceeded its connection cap.

## Import and Resolution Failures

- `ERR_REQUIRE_ESM`: a CJS file is requiring an ESM-only package. Dynamic `import()`, or move the caller to ESM (node >=22.12 can `require()` a sync ESM graph).
- `ERR_MODULE_NOT_FOUND` on a relative path: ESM requires the file extension. On a package path: the package's `exports` map blocks that subpath.
- `X is not a function` right after an interop change: the default export arrived as `{ default: fn }`. Print the namespace: `node -p "Object.keys(await import('pkg'))"`.
- Two copies of the same package: `npm ls <pkg>` shows every path; two copies mean two module instances and `instanceof` failing across them (→ `modules.md`).

## Errors With No Stack

- The thrown value was not an Error (a string, an object, a rejected promise carrying a plain value) — `--trace-uncaught` gives the throw site.
- The stack was truncated at Node's 10-frame default: raise `--stack-trace-limit`.
- The async boundary erased the caller: wrap with `new Error('context', { cause: err })` at each layer rather than rethrowing bare (→ `errors.md`).
- The error was swallowed by an empty `catch {}` — grep for them before assuming the failure is silent.

## When You Are Truly Stuck

Cut the surface until it works: run the entry file with an empty handler, no framework, no env file, no TypeScript layer. Then add back one dependency, one route, one flag at a time. The step that reopens the bug names the subsystem, and the subsystem names the file to open next.
