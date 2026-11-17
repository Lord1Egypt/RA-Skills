# Production — Running a Node Service Someone Depends On

Scope: the process and its host contract — signals, configuration, logging, observability, and the container shape. Request-path timeouts live in `http.md`; the shutdown code path lives in `errors.md`.

## The Process Contract

A production Node process owes its platform four behaviors. Missing any one turns a routine deploy into an incident:

1. **Answers SIGTERM.** As PID 1 in a container there are no default handlers — SIGTERM is ignored and every stop burns the full grace window, then SIGKILL drops in-flight requests. Register a handler, or run an init (`docker run --init`, or an init process in the image) which also reaps zombies from any child you spawn.
2. **Exits non-zero on failure.** Supervisors decide restart-versus-alert on the exit code; `process.exitCode = 1` plus a drained loop, never `process.exit(0)` in an error path.
3. **Reports readiness separately from liveness.** Liveness = the process responds. Readiness = it can serve (migrations done, pools connected, not draining). One endpoint for both means a restarting pod gets traffic, or a healthy one gets killed for being busy.
4. **Logs to stdout/stderr only.** Writing log files inside a container makes the platform's collection, rotation, and retention your problem instead of its.

## Configuration

- Read and validate the entire environment once at startup, then pass a typed config object around. A missing variable discovered mid-request at 3am was checkable at boot: fail fast, print every missing or malformed name at once, exit non-zero.
- Env values are strings or undefined. `process.env.DEBUG` is truthy for `"false"`; `PORT` is `"3000"`, not `3000`.
- `--env-file=.env` is built in on node >=20.6; the file is for local development, never the deploy artifact — real environments inject variables.
- Secrets: environment variables are visible to anything that can read `/proc/<pid>/environ` or run `docker inspect`, and they leak into crash dumps and error reporters. Mounted files with a filesystem-permission boundary are strictly better; either way, never in argv (`ps` shows argv to every user on the box).
- `NODE_ENV=production` changes dependency installs and framework behavior (view caching, verbose errors) — set it explicitly; a missing value quietly gives you development behavior in production.

## Logging

- Structured JSON to stdout, one object per line, with a level, a timestamp, and a request/trace id. Grep-friendly prose stops being greppable the day you have three services.
- `console.log` to a file or terminal is synchronous on POSIX — hot-path logging blocks the event loop (SKILL.md rule 1). Use an async structured logger (pino) inside request handlers, keeping `console` for boot and crash paths.
- Redact at the logger, not at the call site: tokens, `authorization`, cookies, and full request bodies. A redaction list in one place survives the next developer; a careful `logger.info` does not.
- Log level from config, default `info`; `debug` in production is a disk and throughput cost, not a safety net.
- Sampling beats truncation for high-volume paths: log 1% of successful requests in full and 100% of failures, rather than a stub line for everything.

## Observability

- Four numbers tell you whether the process is healthy: event loop delay p99 (SKILL.md rule 1), RSS vs the container limit (rule 8), open descriptors vs `ulimit -n` (rule 4), and in-flight requests. Export them before you buy a vendor; all four are available from `perf_hooks` and `process`.
- Enable diagnostic reports in advance: `--report-on-fatalerror --report-on-signal --report-directory=...`. After an OOM abort, that JSON is the only artifact with stacks and handle state (→ `commands.md`).
- `diagnostics_channel` publishes internal HTTP/DNS events without patching the modules; APM auto-instrumentation uses it. Prefer it over monkey-patching `http.request`.
- Alert on rate of change, not absolutes: RSS at 70% of the limit is fine and stable, or it is five minutes from an OOMKill — only the slope distinguishes them.

## Containers

- Multi-stage: build with dev dependencies, ship `npm ci --omit=dev` plus the built output. Never copy `node_modules` from the host — native modules are compiled for that OS, arch, and libc (→ `runtime.md`).
- Set the heap ceiling relative to the container memory limit (SKILL.md rule 8). The default heap sizing does not read your cgroup limit reliably; a 512 MB container gets `--max-old-space-size=384`.
- One process per container (SKILL.md rule 7): the orchestrator scales replicas, and a supervisor inside the container hides crashes from it.
- Run as a non-root numeric UID and make the filesystem read-only where possible; a Node app that needs to write usually needs one tmpfs mount, not a writable root.
- Alpine ships musl: prebuilt native binaries mostly target glibc, so installs fall back to compiling from source and some binaries segfault. Default to a slim glibc base; move to Alpine only when image size is a measured constraint.
- `.dockerignore` must exclude `node_modules`, `.git`, and build output — otherwise the host's `node_modules` uploads with the build context and can shadow the image's.

## Deploying

- Deploy an immutable artifact identified by digest or commit sha, and record it — rollback is only possible if you know the previous identity.
- Roll one instance at a time with readiness gating; the drain sequence (fail readiness → stop accepting → drain → exit) is what makes a rolling deploy invisible to users (→ `errors.md`).
- Database migrations run as a separate step with its own success criterion, never at process boot: N replicas booting at once means N concurrent migrations racing.
- Backward-compatible schema changes first, then the code that uses them, then the cleanup. A deploy that requires both sides to change at the same instant has no rollback.

## Capacity Sizing

- One Node process saturates roughly one core for JS work. Sizing formula: `replicas ≈ ceil(peak_rps ÷ (1000 ms ÷ mean_handler_ms))`, then add headroom for the p99 handler, not the mean. At 20 ms mean that is ~50 rps per process; at 200 ms it is ~5.
- Memory per process = heap ceiling + native/buffers + a margin; set the container limit above `--max-old-space-size`, not equal to it, or the kernel wins the race and you get exit 137 instead of a readable heap error (rule 8).
- Concurrency limits belong in the app as well as the platform: without a cap, a traffic spike converts into unbounded queueing and every request times out instead of most of them succeeding (rule 4).

## Production Gate

Before calling a Node service deployed:

- SIGTERM handler present, drain sequence ordered, backstop timer under the platform's grace window?
- Env validated at boot, secrets not in argv, `NODE_ENV` set explicitly?
- Heap ceiling set from the container limit, container limit above it?
- Structured logs to stdout, redaction list in the logger, level from config?
- Readiness and liveness distinct, readiness failing first on shutdown?
- Deployed artifact identified by digest/sha and recorded for rollback?
- Diagnostic reports enabled and the report directory writable?
