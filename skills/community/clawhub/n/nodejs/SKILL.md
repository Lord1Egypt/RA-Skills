---
name: nodejs
slug: nodejs
version: 1.0.4
description: >-
  Builds, debugs, and hardens Node.js servers, CLIs, and npm packages: async, modules, streams, memory, and process lifecycle.
  Use when writing or reviewing code that runs on Node, when a process hangs or refuses to exit, leaks memory, gets OOM-killed,
  pins one CPU core at 100%, or dies on an unhandled rejection; when the error reads EADDRINUSE, EMFILE, ECONNRESET,
  ERR_MODULE_NOT_FOUND, ERR_REQUIRE_ESM, or "__dirname is not defined"; when import and require interop breaks, streams
  buffer everything in RAM, a server returns intermittent 502s behind a load balancer, or SIGTERM drops in-flight requests;
  when npm install, lockfiles, peer dependencies, workspaces, native module builds, or publishing misbehave; when a suite
  passes locally and fails in CI; or when containerizing, profiling, and shutting down a service cleanly. Not for browser-only
  JavaScript, TypeScript type-system design, or the Bun and Deno runtimes.
homepage: https://clawic.com/skills/nodejs
changelog: "Full coverage pass: deeper guides, situation-named files, and per-user configuration"
metadata:
  clawdbot:
    emoji: 💚
    requires:
      bins:
      - node
    os:
    - linux
    - darwin
    - win32
    displayName: NodeJS
    configPaths:
    - ~/Clawic/data/nodejs/
---

User preferences and memory live in `~/Clawic/data/nodejs/` (see `setup.md` on first use, `memory-template.md` for the file format). If you have data at an old location (`~/nodejs/` or `~/clawic/nodejs/`), move it to `~/Clawic/data/nodejs/`.

## When To Use

- Writing or reviewing Node services, CLIs, libraries, workers, or release scripts
- Debugging a live process: hangs, crash loops, growing RSS, slow endpoints, import failures, unclean shutdown
- Deciding the runtime shape of a package: ESM vs CJS, exports map, lockfile policy, native dependencies, publish surface
- Production incidents: intermittent 502s behind a proxy, EMFILE, event loop stalls, containers OOMKilled overnight
- Running TypeScript, tests, or child processes on Node — the runtime side, not the type system
- Not for browser-only JavaScript, TypeScript type design, or the Bun/Deno runtimes (each has its own skill)

## Quick Reference

| Situation | Play |
|---|---|
| One core pinned, every request slows at once | Event loop blocked. Record `node --cpu-prof`, read widest self-time frames, not deepest stacks → `performance.md` |
| Process finishes its work but never exits | An open handle: server, socket, `setInterval`, worker, or pool. `process.getActiveResourcesInfo()` names it → `debug.md` |
| RSS climbs while `heapUsed` stays flat | Buffers/native memory, not a JS leak — heap snapshots will show nothing → `performance.md` |
| Intermittent 502/504 behind ALB or nginx | `keepAliveTimeout` below the proxy's idle timeout (rule 5) → `http.md` |
| `ERR_REQUIRE_ESM`, `ERR_MODULE_NOT_FOUND`, `__dirname is not defined` | Module-format mismatch or a missing file extension → `modules.md` |
| `EADDRINUSE` on restart | Old process still holding the port, or two workers binding it; in tests, bind port 0 → `debug.md` |
| `EMFILE` / `ENFILE` | Unbounded concurrency or leaked descriptors (rule 4) → `filesystem.md` |
| Exit 134 with `FATAL ERROR: ... heap out of memory` | V8's heap ceiling, not the container's limit (rule 8) → `performance.md` |
| Memory grows during a copy, upload, or export | Backpressure ignored: `write()` returned false and nobody waited → `streams.md` |
| `npm install` works, `npm ci` fails | Lockfile out of sync with package.json (rule 6) → `packages.md` |
| Native module fails to build or load after an upgrade | ABI mismatch, missing toolchain, or musl vs glibc → `runtime.md` |
| Child process hangs, or its output is truncated | `maxBuffer` exceeded, or nobody drains the stdio pipe → `concurrency.md` |
| A `.ts` file won't run, or imports resolve at build but not at runtime | Type-stripping limits or `moduleResolution` mismatch → `typescript.md` |
| CLI crashes with EPIPE when piped into `head` | stdout closed early; handle the error instead of letting it throw → `cli.md` |
| Suite green locally, red in CI | Port collisions, fake timers, shared module state, file ordering → `testing.md` |
| Untrusted input reaching `exec`, a path join, or a regex | Injection, traversal, ReDoS — the exact checks → `security.md` |
| SIGTERM drops in-flight requests on deploy | No drain sequence, or node is PID 1 with no signal handler → `production.md` |
| Anything else | Reproduce with the smallest script that still fails, then re-add flags, env vars, and imports one at a time |

Depth on demand: `debug.md` symptom→cause chains · `commands.md` diagnostic toolkit · `async.md` event loop and promises · `modules.md` ESM/CJS · `errors.md` failure handling and shutdown · `streams.md` backpressure · `http.md` servers, clients, timeouts · `performance.md` profiling and leaks · `concurrency.md` workers, cluster, child processes · `filesystem.md` files, paths, descriptors · `security.md` hardening · `testing.md` suites and mocks · `packages.md` npm, lockfiles, publishing · `typescript.md` running TS on Node · `runtime.md` versions, flags, native modules · `production.md` deploy, config, logging, observability · `cli.md` command-line tools.

## Core Rules

1. **Budget sync work at ~10 ms per slice.** Max throughput per process ≈ 1000 ms ÷ block_ms: a 50 ms sync `JSON.parse` in a request handler caps that process near 20 req/s, and every concurrent request inherits the stall. Repeatedly over budget → `worker_threads`; one-off → partition with `setImmediate` (→ `async.md`).
2. **Handle operational errors, crash on programmer errors** (Joyent doctrine). ECONNRESET, ENOENT, bad user input → handle at the call site. TypeError, undefined property → let it crash; the supervisor restarts a clean process. Catch-all recovery keeps corrupted state serving traffic.
3. **"Async" fs, dns.lookup, crypto, and zlib share 4 libuv threads** (default `UV_THREADPOOL_SIZE`; max 1024). The 5th concurrent `fs.promises.readFile` queues behind the first 4. Slow "async" crypto/fs under load → raise the pool to roughly the number of concurrent slow calls, or move the work off the process.
4. **Cap concurrency explicitly.** `Promise.all(items.map(fetch))` over 10k items opens 10k sockets — EMFILE at the common 1024 fd soft limit. Batch or use a limiter; 8-32 concurrent per upstream host is a sane starting cap, raised on evidence: throughput climbing with flat latency = raise it; latency climbing = you found the ceiling.
5. **`keepAliveTimeout` must exceed the proxy's idle timeout.** Node's default is 5 s; ALB's default idle is 60 s, so Node closes sockets the balancer just reused → intermittent 502s. Formula: `keepAliveTimeout = proxy_idle + 5 s` and `headersTimeout = keepAliveTimeout + 1 s` (ALB 60 s → 65 s / 66 s; nginx upstream `keepalive_timeout 75s` → 80 s / 81 s).
6. **Exact versions for apps, ranges for libraries; `npm ci` in anything automated.** `npm install` rewrites the lockfile whenever package.json allows it — in CI that means testing an install nobody reviewed (→ `packages.md`).
7. **One process per container.** Let the orchestrator scale replicas; `cluster` only on bare metal or VMs you own entirely — two schedulers fighting over the same cores obscures both.
8. **Set the heap ceiling below the memory limit.** RSS = heap + buffers + stacks + native, so a default-sized heap under a container limit invites an OOMKill instead of a catchable heap error. Formula: `--max-old-space-size = floor(0.75 × container_limit_MB)` — 512 MB limit → 384; 2 GB → 1536. Exit 134 with `FATAL ERROR: ... heap out of memory` means you hit V8's ceiling; exit 137 means the kernel hit yours first.

## Exit and Error Codes

Exit codes above 128 mean killed by signal `code − 128`; Node's own fatal codes sit below 10.

| Code | Meaning | First move |
|---|---|---|
| 1 | Uncaught fatal exception | Read the stack; an empty one means a non-Error was thrown (→ Traps) |
| 3 / 5 | Internal JS parse failure / fatal V8 error | Almost always a bad `--flag` or a corrupt install, not your code |
| 7 | Exception inside an exception handler | Your `uncaughtException` hook itself threw |
| 9 | Invalid argument to the node binary | Flag typo, or a flag this major doesn't support (→ `runtime.md`) |
| 130 | SIGINT (128+2) | Ctrl-C; clean unless a handler swallowed it |
| 134 | SIGABRT (128+6) | V8 fatal — usually heap OOM (rule 8) or a failed native assertion |
| 137 | SIGKILL (128+9) | Kernel or orchestrator OOM kill, or a stop timeout expiring (rule 8) |
| 143 | SIGTERM (128+15) | Normal stop; if requests were dropped, the drain sequence is missing (→ `production.md`) |

Error codes worth recognizing on sight: `EADDRINUSE` (port held), `EMFILE`/`ENFILE` (descriptor limit, rule 4), `ECONNRESET` (peer closed mid-flight — operational, rule 2), `EPIPE` (downstream closed a pipe), `ERR_REQUIRE_ESM` and `ERR_MODULE_NOT_FOUND` (format or extension), `ERR_UNHANDLED_REJECTION` (rule 2), `ERR_STRING_TOO_LONG` (V8 caps string length in the hundreds of MB — stream instead of `JSON.stringify`), `ERR_CHILD_PROCESS_STDIO_MAXBUFFER` (child output over the buffer cap).

## Timeout Ladder

Every timeout in the path must be ordered, or one layer kills a connection another layer still believes in. Each line reads strictly larger left to right:

```
client abort  <  upstream call timeout  <  inbound requestTimeout
proxy idle    <  keepAliveTimeout       <  headersTimeout
force-exit backstop  <  orchestrator kill window
```

- Node HTTP server defaults (node >=18): `keepAliveTimeout` 5 s, `headersTimeout` 60 s, `requestTimeout` 300 s, `server.timeout` 0 (disabled). Only the first is short enough to bite by accident (rule 5).
- Outbound calls need their own deadline — an upstream that never answers holds a socket, a descriptor, and a request slot. `AbortSignal.timeout(ms)`, with retries × per-try timeout still under `requestTimeout`.
- Shutdown backstop = orchestrator grace window − 5 s (Kubernetes `terminationGracePeriodSeconds` defaults to 30 s → force-exit at 25 s), so you exit on your own terms with logs flushed instead of by SIGKILL.

## Version Gates

The canonical minimums this skill's guidance assumes. Check `node -v` before recommending anything above the user's line, and name the fallback when the target is older.

| Feature | Minimum |
|---|---|
| Unhandled rejection terminates the process (default) | 15 |
| `new Error(msg, { cause })` | 16.9 |
| `AbortSignal.timeout()`, `process.getActiveResourcesInfo()` | 17.3 |
| Global `fetch`/undici (stable from 21) | 18 |
| `node:test` runner stable | 20 |
| `--env-file=.env` built in | 20.6 |
| `import.meta.dirname` / `import.meta.filename` | 20.11 |
| `node --run <script>`, `--watch` stable | 22 |
| `require()` of a synchronous ESM graph | 22.12 |
| Running `.ts` by type stripping, unflagged | 24 (backported to 22.18) |

Release cadence, so "supported" stays checkable instead of remembered: one new major every April and October; even majors enter LTS that October and get ~3 years total (6 months Current, 12 Active LTS, 18 Maintenance); odd majors die after ~6 months and never belong in production. Which majors are live today: `runtime.md` (dated).

## Output Gates

Before shipping Node code, verify:

- Any `*Sync` call, unbounded `JSON.parse`, or whole-array loop reachable from a request handler? (rule 1)
- Every `Promise.all` bounded by something other than user input? (rule 4)
- Every stream wired through `pipeline()` or carrying its own `error` handler — an unhandled stream `error` is a process crash?
- Every outbound call carrying a timeout or AbortSignal, and every server timeout ordered per the ladder?
- All `process.env` reads parsed and validated once at startup — they are strings or undefined, never numbers or booleans?
- Shutdown path present: SIGTERM → fail readiness → stop accepting → drain → close pools → exit, in that order (→ `errors.md`)?
- Heap ceiling set against the container limit (rule 8), and one process per container (rule 7)?

## Configuration

User-dependent variables. Defaults apply until the user states a preference; store them in `~/Clawic/data/nodejs/config.yaml`.

| Variable | Type | Default | Effect |
|---|---|---|---|
| package_manager | npm \| pnpm \| yarn \| bun | npm | Every install, lockfile, workspace, and CI command; which `npm ci` equivalent rule 6 names |
| module_system | esm \| cjs | esm | Import syntax and extensions in all examples, `type` field guidance, which half of `modules.md` leads |
| node_target | number (major, >=20) | 24 | Which APIs the guidance may use without a fallback — read against the Version Gates table |
| test_runner | node \| jest \| vitest | node | Test, mock, and fake-timer idioms; the coverage and watch flags quoted in `testing.md` |
| deploy_target | container \| vm \| serverless \| paas | container | Signal and PID-1 handling, cluster vs replicas (rule 7), heap sizing (rule 8), shutdown window |
| ts_runner | none \| strip \| tsx \| tsc | none | Whether `.ts` guidance assumes type stripping, a loader, or a build step (`typescript.md`) |

Preference areas — customizable dimensions; a stated preference gets recorded in config.yaml and applied:

- **Tooling** — script runner (`node --run` vs package-manager scripts), linter/formatter stack, profiler of choice — affects the shape of every command example
- **Conventions** — extensions (`.mjs`/`.cjs` vs a `type` field), error-class taxonomy, script names, folder layout, log field names
- **Platform** — OS (Windows path and `spawn` caveats), architecture (arm64 prebuilds), base image (musl vs glibc), registry mirror
- **Thresholds** — concurrency cap per upstream (rule 4), heap fraction (rule 8), timeout values, stream `highWaterMark`
- **Risk posture** — crash-vs-catch aggressiveness (rule 2), `--ignore-scripts` on install, automatic major bumps, permission model
- **Output format** — log shape (JSON vs pretty), verbosity, how much error detail reaches clients
- **Work order** — test-first vs code-first, profile-before-optimize, review gates before publish
- **Integrations** — registry, observability vendor, CI provider, process supervisor
- **Constraints** — banned dependencies, license policy, no-native-modules, offline or air-gapped installs
- **Cadence** — dependency update rhythm, Node upgrade rhythm against the April/October cadence

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Unhandled promise rejection | Terminates the process by default (node >=15) | `.catch()` or try/catch on every await chain |
| `.pipe()` without error wiring | Errors don't cross pipes; the source leaks, then crashes | `stream.pipeline()` |
| Forgotten `await` inside try/catch | The rejection skips the catch and surfaces later, or never | Lint with `no-floating-promises` |
| `exports = x` in CJS | Rebinds a local alias; `module.exports` is unchanged | `module.exports = x` |
| `__dirname` in ESM | Doesn't exist there | `import.meta.dirname`, else `fileURLToPath(import.meta.url)` |
| Mutating a `require()`d object | Module cache: every consumer sees the mutation | Export factories, or freeze exports |
| `process.env.PORT` used as a number | Env values are strings (`"3000"`) or undefined | Parse and validate the whole env once at startup |
| Listeners added per request | Accumulate to MaxListenersExceededWarning — a leak signal, not a limit | `once()`, or remove on completion |
| Raising the max-listeners limit to silence that warning | Hides the leak that produced it; memory keeps climbing | Find who adds a listener per event and remove it |
| Throwing non-Error values | No stack; `instanceof Error` checks fail; exit 1 with an empty trace | `throw new Error(msg, { cause })` |
| `node:vm` as a sandbox | Not a security boundary — its own docs say so | Isolate untrusted code at process or container level |
| `npm audit fix --force` on a red report | Applies major bumps that break the app to silence findings in code that may never run | Triage by reachability, pin with `overrides` (→ `packages.md`) |
| `node index.js` as PID 1 in a container | PID 1 gets no default signal handlers: SIGTERM is ignored and every stop burns the full grace window | Register a SIGTERM handler, or run an init (→ `production.md`) |

## Where Experts Disagree

- **Crash-and-restart vs catch-and-continue.** Crash when a supervisor restarts you and in-process state may be corrupt; continue only for operational errors scoped to a single request. The boundary question: can you name exactly what stayed consistent?
- **Dual CJS+ESM packages vs ESM-only.** Dual carries the two-instance hazard (`instanceof` fails across copies, module state duplicates); ESM-only is viable once consumers are ESM or run node >=22.12, where `require()` of a sync ESM graph works.
- **`node:test` vs Jest vs Vitest.** `node:test` for new libraries — no transform layer, native ESM, no hoisting magic; Jest for existing suites with heavy matcher and snapshot use; Vitest where the project already runs a Vite pipeline. Migrating a green suite for aesthetics is a net loss.
- **TypeScript at runtime vs a build step.** Type stripping deletes the toolchain for apps deployed from source; a `tsc` build stays correct for published libraries that must ship `.d.ts` and support older consumers.

## Related Skills
More Clawic skills, get them at https://clawic.com/skills/nodejs (install if the user confirms):
- `javascript` — language-level semantics: coercion, closures, dates, regex
- `typescript` — type-system design, tsconfig strictness, declaration files
- `docker` — containerizing the service, image layers, resource limits
- `api` — HTTP API design, versioning, and contracts above the runtime

## Feedback

- If useful, star it: https://clawic.com/skills/nodejs
- Latest version: https://clawic.com/skills/nodejs

Part of [Clawic](https://clawic.com), the verified skill library. Get this skill: https://clawic.com/skills/nodejs.
