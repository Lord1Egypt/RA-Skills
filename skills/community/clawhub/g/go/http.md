# HTTP — Servers, Clients, Timeouts, and Leaks

`net/http` is production-grade out of the box in exactly one respect: it works. Every default that concerns time and memory is unbounded, and the package expects you to set the limits yourself.

Sections: Client: The Defaults That Bite · Always Drain and Close the Response Body · Redirects, Status, and Errors · Server: Set Every Timeout · Handlers · Routing · Graceful Shutdown · Testing

## Client: The Defaults That Bite

| Setting | Default | Consequence |
|---|---|---|
| `http.Client.Timeout` | **0 — no timeout** | One unresponsive server pins a goroutine and a connection until the process exits |
| `Transport.MaxIdleConns` | 100 | Total idle connections across all hosts |
| `Transport.MaxIdleConnsPerHost` | **2** | A service hammering one backend opens and discards connections constantly; raise it to match concurrency |
| `Transport.IdleConnTimeout` | 90s | Idle connections close after this |
| `Transport.TLSHandshakeTimeout` | 10s | |
| `Transport.MaxConnsPerHost` | 0 — unlimited | No ceiling on concurrent connections to one host |

```go
var client = &http.Client{
    Timeout: 10 * time.Second,          // = default_timeout; whole request: dial + TLS + headers + body
    Transport: &http.Transport{
        MaxIdleConnsPerHost: 100,
        IdleConnTimeout:     90 * time.Second,
    },
}
```

- **Create one client per process and reuse it.** A new `http.Client` per call means a new `Transport`, a new connection pool, and no connection reuse at all — the pool lives on the Transport, not the Client.
- `http.Get`, `http.Post`, and `http.DefaultClient` all share a zero-timeout client. Acceptable in a script, never in a service.
- `Client.Timeout` covers the entire exchange **including reading the body**. A streaming download needs a zero client timeout plus per-phase timeouts on the Transport and a context deadline.
- Always `http.NewRequestWithContext(ctx, ...)`: the context deadline is per call, the client timeout is the process-wide backstop, and the tighter one wins (`context.md`).
- Every number in this file is the `default_timeout` variable (Configuration, default 10s) or a fixed multiple of it — the client timeout is `default_timeout` itself, the server set is ×0.5/×1.5/×3/×6. A budget the caller states wins over it; a `default_timeout` the user states rescales the whole set, never one field.

## Always Drain and Close the Response Body

```go
resp, err := client.Do(req)
if err != nil { return err }
defer func() {
    io.Copy(io.Discard, resp.Body)   // drain, so the connection is reusable
    resp.Body.Close()
}()
```

- `Close` without draining discards the connection: the pool cannot reuse a stream with unread bytes, so every call opens a new TCP+TLS connection. The symptom is a slow rise in latency and file descriptors under load, with no error anywhere.
- The body must be closed even on non-2xx responses. `err == nil` with a 500 still allocated a body.
- Bound what you read from an untrusted peer: `io.ReadAll(io.LimitReader(resp.Body, 1<<20))`.
- A non-nil error means `resp` is nil — do not `defer resp.Body.Close()` before the error check.

## Redirects, Status, and Errors

- The client **does not** return an error for 4xx or 5xx. Check `resp.StatusCode` explicitly; forgetting this is how error pages get parsed as JSON (`json.md`).
- Redirects are followed automatically up to 10 hops, and by default the `Authorization` header is dropped when the redirect crosses to a different host. Override with `CheckRedirect` when you need different behavior; return `http.ErrUseLastResponse` to stop and inspect the 3xx yourself.
- `url.Values.Encode()` for query strings; manual concatenation of user input into a URL is an injection surface (`security.md`).
- Retry only idempotent requests, on timeouts and 5xx, with jittered backoff, and rebuild the request body each attempt — a consumed `io.Reader` body sends empty on the retry (`errors.md`).

## Server: Set Every Timeout

```go
srv := &http.Server{
    Addr:              ":8080",
    Handler:           mux,
    ReadHeaderTimeout: 5 * time.Second,    // default_timeout ×0.5 — the slowloris defense
    ReadTimeout:       15 * time.Second,   // ×1.5
    WriteTimeout:      30 * time.Second,   // ×3
    IdleTimeout:       60 * time.Second,   // ×6
    MaxHeaderBytes:    1 << 20,
}
```

- Every one of those timeouts is **zero by default**, meaning unlimited. A client that opens a connection and sends one header byte per minute occupies a goroutine forever; `ReadHeaderTimeout` is the cheapest fix and the one most often missing.
- `WriteTimeout` starts when the request headers are read, not when the handler starts writing — a long-polling or streaming endpoint needs it disabled on that route (via a separate server or `http.ResponseController`), not raised globally.
- `http.ListenAndServe(addr, handler)` uses a zero-value server with none of these. Construct the `http.Server` explicitly.
- Never register handlers on `http.DefaultServeMux` in a library or via a side-effecting import: `net/http/pprof` registers itself there, so exposing DefaultServeMux publishes your profiling endpoints (`security.md`, `debugging.md`).

## Handlers

- A handler returns when it returns; there is no "response object" to complete. Once you have written a byte, the status is sent and `WriteHeader` cannot change it. Write the status first, then the body.
- `w.Write` without `WriteHeader` implies 200. A common bug: validate, `w.WriteHeader(400)`, and then fall through to the success path — the second write logs "superfluous WriteHeader call" and the client got a 400 with a success body.
- `r.Context()` is cancelled when the client disconnects. Pass it into every query and outbound call so a hung upstream does not outlive the caller (`context.md`).
- The server closes `r.Body`; you do not have to, though closing early is a way to stop a large upload. Reading the body twice requires buffering it yourself.
- Bound uploads with `http.MaxBytesReader(w, r.Body, n)` before decoding anything.
- `net/http` recovers a panic in a handler: the process survives, that connection dies, and the client sees a truncated response. Add recovery middleware that turns it into a logged 500 (`errors.md`).
- Handler middleware that wraps `http.ResponseWriter` to capture the status loses the optional interfaces (`http.Flusher`, `http.Hijacker`, `io.ReaderFrom`) unless it forwards them. `http.ResponseController` (`go >=1.20`) is the supported way to reach flush and deadline control through wrappers.

## Routing

- `http.ServeMux` supports method and wildcard patterns from `go >=1.22`: `mux.HandleFunc("GET /users/{id}", h)`, read with `r.PathValue("id")`. Below that floor the stdlib mux does prefix matching only, which is why third-party routers existed.
- Patterns ending in `/` match a subtree; the more specific pattern wins, and two patterns that overlap without one being more specific panic at registration — an immediate, loud failure rather than a silent shadow.
- `http_stack` in Configuration selects the router idiom (net/http, chi, gin, echo). Middleware ordering (recover → log → trace → auth → route) is the same in all of them; a recovery middleware registered after the router never sees the panic.

## Graceful Shutdown

```go
ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt, syscall.SIGTERM)
defer stop()
go func() { _ = srv.ListenAndServe() }()
<-ctx.Done()
// 20s = 2/3 of the Kubernetes 30s grace default; derive it from the grace period that applies (`deployment.md`)
shutdownCtx, cancel := context.WithTimeout(context.Background(), 20*time.Second)
defer cancel()
_ = srv.Shutdown(shutdownCtx)
```

- `Shutdown` stops accepting, closes idle connections, and waits for active handlers. Without its own bounded context, one stuck handler blocks exit forever and the orchestrator eventually SIGKILLs the process mid-write.
- The timeout must be shorter than the orchestrator's grace period, and the defaults differ: **30s** in Kubernetes, **10s** for `docker stop` and Compose. Under plain Docker, 20s here is SIGKILLed mid-drain; take 2/3 of the real grace period instead (`deployment.md`).
- `Shutdown` does **not** wait for hijacked connections or WebSockets — track those yourself and close them.
- `ListenAndServe` returns `http.ErrServerClosed` on a normal shutdown; treating that as a failure produces a spurious non-zero exit code (`deployment.md`).

## Testing

- `httptest.NewServer(handler)` gives a real server on a real port with a client that already trusts it; `defer ts.Close()`.
- `httptest.NewRecorder()` plus `handler.ServeHTTP(rec, req)` tests a handler with no network at all — faster, and the default for unit tests.
- Never assert against a live third-party endpoint; stand up an `httptest` server that returns the recorded payload (`testing.md`).

## Back To SKILL.md

Traps for `http.DefaultClient` and undrained bodies are in SKILL.md Traps. Deadlines: `context.md`. TLS and header hardening: `security.md`.
