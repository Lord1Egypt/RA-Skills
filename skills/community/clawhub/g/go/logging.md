# Logging — slog, Levels, and What Not To Log

`log/slog` (`go >=1.21`) made structured logging standard library. Below that floor, or with `logger` set to zap/zerolog in Configuration, the API differs but every rule here still applies.

## Setup

```go
h := slog.NewJSONHandler(os.Stderr, &slog.HandlerOptions{
    Level:     slog.LevelInfo,
    AddSource: true,          // file:line; costs a stack lookup per record
})
slog.SetDefault(slog.New(h))
```

- `NewJSONHandler` for anything a machine will read; `NewTextHandler` for a terminal. Choose from a flag or env var so the same binary does both.
- `slog.SetDefault` also redirects the old `log` package's default output through slog, so third-party libraries using `log.Printf` land in the same stream.
- Logs go to **stderr**. Stdout is for the program's data output; mixing them makes a CLI unpipeable and a server's output unparseable (`cli.md`).
- Pass a `*slog.Logger` explicitly into components that need one, rather than reaching for the global everywhere. The global is fine in `main` and in small tools; it is untestable in a library.

## Attributes, Not Formatting

```go
slog.Info("request done", "method", r.Method, "path", p, "status", code, "dur_ms", ms)
slog.LogAttrs(ctx, slog.LevelInfo, "request done",   // allocation-free form
    slog.String("method", r.Method), slog.Int("status", code))
```

- Never build the message with `fmt.Sprintf`. `slog.Info(fmt.Sprintf("user %d failed", id))` produces a unique string per user, so the aggregator cannot group them and you cannot filter by user.
- The variadic `key, value` form is convenient and does allocate; `LogAttrs` with typed attrs (`slog.String`, `slog.Int`, `slog.Duration`) avoids the boxing. Use `LogAttrs` on hot paths only — readability wins elsewhere (`performance.md`).
- An odd number of variadic arguments produces a `!BADKEY` entry rather than a compile error. `go vet`'s `slog` analyzer catches the common mistakes; enable it.
- `logger.With("request_id", id)` returns a child logger that carries the attribute on every record — that is how you avoid repeating context on twenty call sites.
- `slog.Group("db", ...)` nests attributes so JSON consumers get `db.query`, `db.duration` instead of a flat namespace collision.

## Levels

| Level | Means | Rule of thumb |
|---|---|---|
| Debug | Detail for a developer reproducing something | Off in production; must be switchable at runtime without a redeploy |
| Info | A thing happened that an operator would want in the record | One per request or per unit of work, not per step |
| Warn | Degraded but handled — retry succeeded, fallback used, quota near | If nobody would act on it, it is Info |
| Error | The operation failed and a human may need to look | Log **once**, where the error is handled |

- Log **or** return, never both. An error logged at every layer becomes six lines that look like six failures (`errors.md`).
- Make the level dynamic: a `slog.LevelVar` in `HandlerOptions.Level` can be flipped by a signal or an admin endpoint, which is how you get debug logs from a production incident without a deploy.
- Sample high-volume repeated lines rather than dropping the level; the tenth identical timeout tells you nothing the first one did not, but you still want the count.

## Context and Request Correlation

- `slog.InfoContext(ctx, ...)` passes the context to the handler, which is how trace/span IDs get attached automatically by an OpenTelemetry-aware handler.
- Put a request ID into the context in middleware, derive `logger.With("request_id", id)`, and carry that logger through the request. Without a correlation ID, logs from concurrent requests interleave into an unreadable stream — this is the single highest-value line item in a service's logging (`http.md`, `context.md`).
- Do not store the logger in a struct that outlives one request when it carries request attributes; that leaks one request's ID into another's lines (`context.md`).

## What Never Goes In A Log

- Passwords, tokens, API keys, session cookies, authorization headers, full card numbers, national IDs.
- Whole request or response bodies "for debugging" — that is where credentials and personal data hide.
- `%+v` on a struct: `fmt` prints unexported fields via reflection, so a `Config` with a secret field logs the secret. Implement `LogValue() slog.Value` on the type to redact it at the source (`strings.md`, `security.md`):

```go
func (c Credentials) LogValue() slog.Value {
    return slog.StringValue("Credentials{redacted}")
}
```

- SQL with interpolated values (`database.md`). Log the statement name and duration.
- The fix belongs on the **type**, not at each call site: any redaction you have to remember is redaction you will forget.

## Errors In Logs

- `slog.Error("save failed", "err", err)` — the attribute renders via `Error()`, so the wrapped chain is preserved as text.
- Include the identifiers needed to act: which user, which file, which request. "database error" is a line that costs storage and gives nothing.
- Stack traces belong at the panic-recovery boundary, not on every error. `debug.Stack()` inside the recover, once (`errors.md`).

## Output and Operations

- One JSON object per line, to stderr, with no rotation logic in the process: the platform (systemd, Docker, the orchestrator) collects and rotates. In-process rotation is a source of lost lines and duplicate writers.
- A log write is a syscall on a shared file descriptor; per-line logging inside a tight loop is a measurable cost and a lock contention point. Aggregate and log the summary.
- Metrics answer "how often / how slow", logs answer "what happened to this one request", traces answer "where did the time go". Reaching for a log to count something is how log volume explodes.

## Common Mistakes

| Mistake | Consequence | Fix |
|---|---|---|
| `fmt.Sprintf` inside the log message | Unbounded distinct messages; no grouping or filtering | Attributes |
| Logging and returning the same error | One failure looks like several | Log where handled |
| `log.Fatal` in a library or handler | Kills the process, skips defers | Return the error (`errors.md`) |
| Debug level fixed at compile time | No way to raise verbosity during an incident | `slog.LevelVar` |
| Logging the request body | Credentials and PII in the log store | Log field names and sizes |
| Odd number of key/value args | Silent `!BADKEY` | `go vet`'s slog analyzer |
| Logging to stdout in a CLI | Breaks piping | stderr |

## Back To SKILL.md

Redaction and secret handling: `security.md`. Structured output for tools: `cli.md`. Correlating logs with traces at the handler boundary: `http.md`.
