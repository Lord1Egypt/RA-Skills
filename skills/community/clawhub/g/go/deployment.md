# Deployment — Containers, Resource Limits, Shutdown, Health

A Go service is a single static binary, which makes packaging trivial and makes three things easy to get wrong: the resource limits the runtime reads, the shutdown path, and everything the scratch image does not contain.

Sections: Container Image · Resource Limits The Runtime Must See · Graceful Shutdown · Health Endpoints · Configuration and Secrets · Observability In Production · Common Mistakes

## Container Image

```dockerfile
FROM golang:1.24 AS build
WORKDIR /src
COPY go.mod go.sum ./
RUN go mod download                      # cached until the manifests change
COPY . .
RUN CGO_ENABLED=0 go build -trimpath -ldflags="-s -w" -o /app ./cmd/server

FROM gcr.io/distroless/static-debian12:nonroot
COPY --from=build /app /app
USER nonroot:nonroot
ENTRYPOINT ["/app"]
```

- Copy `go.mod`/`go.sum` and run `go mod download` **before** copying the source, so a code edit does not invalidate the dependency layer (`docker` skill for layer ordering in general).
- `CGO_ENABLED=0` produces a static binary that runs on `scratch` and `distroless/static`. With cgo on, the runtime image needs the matching libc — that is the Debian-build/Alpine-run failure (`build.md`).
- What a `scratch` or `distroless/static` image does **not** have, in the order they bite:
  - **CA certificates** → every outbound HTTPS call fails with "x509: certificate signed by unknown authority". Copy `/etc/ssl/certs/ca-certificates.crt` from the builder, or use a base that includes them (distroless/static does).
  - **Timezone data** → `time.LoadLocation` fails with "unknown time zone". `import _ "time/tzdata"` embeds it (`time.md`).
  - **`/etc/passwd`** → some libraries calling `os/user` fail. Distroless `:nonroot` variants provide a user.
  - **A shell** → no `docker exec sh` for debugging; plan on logs, pprof, and a debug image variant.
- Run as non-root with a numeric UID, and ship a `.dockerignore` that excludes `.git` and build output.
- Multi-arch: build once per target with `GOARCH`, or let buildx do it — cross-compiling in Go is native and far faster than QEMU emulation.

## Resource Limits The Runtime Must See

| Variable | Set to | Why |
|---|---|---|
| `GOMEMLIMIT` | ~90% of the container memory limit | Without it a heap spike passes the cgroup ceiling and the kernel SIGKILLs the process — no Go error, no stack, no log (`memory.md`) |
| `GOMAXPROCS` | The cgroup CPU quota (automatic from `go >=1.25`) | Below that floor the runtime reads the **host's** core count: a 1-CPU container on a 64-core node runs 64 Ps, causing throttling and GC overhead |

- An OOM kill shows up as exit code 137 and nothing else. If a container dies with no log line and no panic, check the memory limit before reading code.
- Reserve headroom: `GOMEMLIMIT` bounds Go's own accounting, not goroutine stacks beyond the heap, not cgo allocations, and not the OS page cache.
- CPU throttling looks like latency, not like CPU saturation. A service pinned at 100% of a 0.5-CPU quota shows p99 spikes with an idle-looking profile.

## Graceful Shutdown

```go
// shutdown timeout = 2/3 of the platform's grace period, floor 2s — never a copied constant
func shutdownBudget() time.Duration {
    grace := 30 * time.Second                        // Kubernetes default; see the table below
    if s := os.Getenv("GRACE_SECONDS"); s != "" {    // set it from the deployment manifest
        if n, err := strconv.Atoi(s); err == nil { grace = time.Duration(n) * time.Second }
    }
    if d := grace * 2 / 3; d > 2*time.Second { return d }
    return 2 * time.Second
}

ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt, syscall.SIGTERM)
defer stop()

go func() {
    if err := srv.ListenAndServe(); err != nil && !errors.Is(err, http.ErrServerClosed) {
        log.Error("listen", "err", err)
    }
}()

<-ctx.Done()
stop()                                   // restore default handling: a second signal kills
shutdownCtx, cancel := context.WithTimeout(context.Background(), shutdownBudget())
defer cancel()
if err := srv.Shutdown(shutdownCtx); err != nil { /* forced close */ }
```

- Orchestrators send **SIGTERM** and then SIGKILL when the grace period expires, and the default grace period is a different number on every platform:

| Platform | Grace default | Raise it with | Shutdown timeout at 2/3 |
|---|---|---|---|
| Kubernetes | 30s (`terminationGracePeriodSeconds`) | pod spec field | 20s |
| `docker stop` / `docker run --stop-timeout` | **10s** | `docker stop -t N` | 6s |
| Docker Compose | **10s** | `stop_grace_period: 30s` | 6s, or 20s once raised |
| systemd | 90s (`DefaultTimeoutStopSec`) | `TimeoutStopSec=` | 60s |

- Derive the timeout from the grace period that actually applies. A 20s shutdown copied from a Kubernetes example into a Compose service is killed at 10s, mid-drain, losing exactly the in-flight writes this section exists to protect. Two thirds leaves the remaining third for connection close and telemetry flush.
- The order that avoids dropped requests: fail the readiness probe → wait one probe interval so load balancers stop sending traffic → stop accepting → drain in-flight → close database pools and flush telemetry → exit.
- `srv.Shutdown` waits for active handlers but not for hijacked connections or WebSockets; track those yourself (`http.md`).
- Shutdown must be bounded. One stuck handler with an unbounded shutdown context turns a rolling restart into an outage.
- `ListenAndServe` returns `http.ErrServerClosed` on a clean shutdown — treating it as an error produces a spurious non-zero exit and a failed deploy.

## Health Endpoints

- **Liveness**: "is the process wedged?" — a trivial handler returning 200. It must not check dependencies: a database blip then restarts every replica at once and turns a degradation into an outage.
- **Readiness**: "should traffic come here?" — checks the dependencies this instance needs, with short timeouts, and flips to failing during shutdown.
- **Startup**: for a slow boot (migrations, cache warm), so the liveness probe does not kill the process before it is up.
- Cache dependency checks for a few seconds. An uncached readiness probe hitting the database every second from every replica is a self-inflicted load source.

## Configuration and Secrets

- Environment variables for configuration; files (mounted secrets) for anything sensitive. A token on the command line is visible in the process list (`security.md`).
- Validate all configuration at startup and exit non-zero with a clear message. A service that boots with a missing setting and fails on the first request has moved a deploy-time error into an incident.
- Never bake secrets into the image with `ENV` or `COPY` — every layer is readable by anyone who can pull it.
- Stamp the build: `-ldflags "-X main.version=…"`, or read `runtime/debug.ReadBuildInfo()` (`build.md`). Log the version once at startup; it is the first thing you need during an incident.

## Observability In Production

- Logs as JSON on stderr, collected by the platform; no in-process rotation (`logging.md`).
- pprof bound to a **separate internal listener**, never the public mux: `http.ListenAndServe("localhost:6060", nil)` after importing `net/http/pprof`. Exposing it publishes heap dumps and command-line arguments (`debugging.md`).
- `GOTRACEBACK=all` in the container environment so a crash prints every goroutine, not only the panicking one.
- Metrics worth having from day one: request rate and latency histogram, error rate by class, goroutine count, heap live bytes, GC CPU fraction. Goroutine count rising monotonically is a leak; heap live bytes rising monotonically is a retention bug (`memory.md`).

## Common Mistakes

| Mistake | Consequence | Fix |
|---|---|---|
| No `GOMEMLIMIT` | Silent OOM kills at exit 137 | ~90% of the container limit |
| `GOMAXPROCS` from the host on `go <1.25` | Throttling and GC overhead in a small container | Set it, or use an automaxprocs library |
| Shutdown timeout ≥ orchestrator grace period | SIGKILL mid-request | 2/3 of the real grace period (30s in Kubernetes, 10s under `docker stop`), and drain first |
| Liveness probe that checks the database | A dependency blip restarts every replica | Liveness trivial, readiness checks deps |
| `scratch` image making HTTPS calls | x509 unknown authority | Copy the CA bundle |
| cgo binary on a different libc | "no such file or directory" for a file that exists | `CGO_ENABLED=0` |
| pprof on the public listener | Heap dumps and args exposed | Internal-only port |
| Treating `http.ErrServerClosed` as failure | Non-zero exit on every clean deploy | `errors.Is` check |

## Back To SKILL.md

Build flags and static linking: `build.md`. GC and memory ceilings: `memory.md`. Server timeouts and shutdown API: `http.md`.
