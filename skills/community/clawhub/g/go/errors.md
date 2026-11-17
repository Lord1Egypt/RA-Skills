# Errors — Wrapping, Identity, Panics, and Retries

Errors are values. The whole design question is what a caller can *do* with the value: compare it, extract fields from it, or only print it. Pick one deliberately per exported function — that choice is API surface you cannot retract later.

## The Three Error Shapes

| Shape | Declaration | Caller checks with | Use when |
|---|---|---|---|
| Sentinel | `var ErrNotFound = errors.New("not found")` | `errors.Is(err, ErrNotFound)` | The caller branches on one well-known condition |
| Typed | `type ValidationError struct{ Field string }` with `Error() string` | `errors.As(err, &ve)` then read fields | The caller needs data out of the failure |
| Opaque | `fmt.Errorf("open config: %w", err)` | Nothing but logging | Everything else — the default |

Default to opaque. Every exported sentinel and error type is a compatibility promise; a codebase that exports fifteen of them cannot change how it fails.

## Wrapping

- `fmt.Errorf("read %s: %w", path, err)` keeps the chain. `%v` flattens it, and every `errors.Is` above you starts returning false with no compile error — the single most common Go regression during refactors.
- Add context the caller does not already have: the file name, the ID, the operation. `fmt.Errorf("failed: %w", err)` adds a word and no information.
- Do not put the word "error" or "failed" in the message and then wrap it three times: `error: failed to: error opening: EOF` is what that produces. Message style is lowercase, no trailing punctuation, no capital letter (`idioms.md`).
- How much to wrap is the `error_wrapping` variable in Configuration, default `always`: `always` wraps every hop, `boundaries` wraps only where the error crosses a package, `never` returns opaque errors from the package edge. Follow the configured policy, not a habit — under `boundaries`, wrapping once per function is noise; under `always`, skipping a hop loses the frame the caller needed.
- Multiple `%w` verbs in one `fmt.Errorf` are legal from `go >=1.20` and produce a tree; `errors.Is` walks all branches.
- `errors.Join(err1, err2)` (`go >=1.20`) for "N things failed" — a nil argument is skipped, and joining only nils returns nil, which makes it safe as an accumulator in a loop.

## Identity Checks

```go
if errors.Is(err, sql.ErrNoRows) { ... }          // sentinel, anywhere in the chain

var pe *fs.PathError
if errors.As(err, &pe) { log.Print(pe.Path) }     // typed, extracts the value
```

- `err == ErrNotFound` breaks the moment anyone wraps. Use `errors.Is` even when you "know" nothing wraps it today.
- `errors.As` takes a **pointer to the target variable** — `&pe` where `pe` is already a `*fs.PathError`. Passing `pe` panics with "errors: target must be a non-nil pointer".
- A custom type joins the chain by implementing `Unwrap() error`. Forget it and `errors.Is` stops at your type; a wrapper without `Unwrap` is a chain terminator.
- For custom equality (an error that should match a family), implement `Is(target error) bool` on the type; `errors.Is` calls it.

## Typed Errors and the Nil Trap

```go
type MyErr struct{ Code int }
func (e *MyErr) Error() string { return fmt.Sprintf("code %d", e.Code) }

func bad() error  { var e *MyErr; return e }   // returns a NON-nil error holding a nil pointer
func good() error { return nil }               // returns a nil error
```

Declare the return type as `error` and return the literal `nil` on the success path — never a typed nil variable. `go vet`'s `nilness` analyzer and `staticcheck` catch some of these; the reliable defense is the rule (`interfaces.md`).

Give the method a **pointer receiver** (`func (e *MyErr) Error()`). With a value receiver both `MyErr` and `*MyErr` satisfy `error`, so `errors.As(err, &target)` matches only whichever form the producer happened to return.

## Panic and Recover

- `panic` is for programmer bugs — an impossible state, a violated invariant, a nil that a constructor guarantees is non-nil. Library code does not panic on bad user input; it returns an error.
- `recover()` works only when called **directly** by a deferred function of the panicking frame. `defer func() { helper() }()` where `helper` calls `recover` returns nil.
- A panic in any goroutine that nobody recovers kills the **whole process**. Recovery does not cross goroutine boundaries, so every long-lived worker you spawn needs its own deferred recover if a crash there must not take the process down (`concurrency.md`).
- `net/http` recovers panics inside handlers per connection: the process survives, the client gets a dropped connection. `http.ErrAbortHandler` is the one panic value the server treats as intentional and does not log (`http.md`).
- After recovering, re-panic or log with the stack: `debug.Stack()` inside the deferred function, because the stack is gone once you return normally.
- Converting panic to error at a package boundary is legitimate for parser-style code that panics internally to unwind. Name the pattern and keep it inside one package.

```go
func Parse(b []byte) (v Value, err error) {
    defer func() {
        if r := recover(); r != nil {
            err = fmt.Errorf("parse: %v", r)   // named return, assigned in the defer
        }
    }()
    return mustParse(b), nil
}
```

Named return values are the mechanism — a plain `return` cannot be rewritten from a defer without them.

## os.Exit, log.Fatal, and Defers

`os.Exit` terminates immediately: no defers, no buffered writer flushes, no trace export. `log.Fatal` and `log.Panic` call it too. Below `main` this silently drops cleanup — return the error upward and exit once, in `main` (`cli.md`).

## Retries

- Retry only what is retriable: timeouts, 5xx, connection resets, `context.DeadlineExceeded` from an inner call. Never retry a 4xx, a validation error, or `context.Canceled` — the caller already left.
- Exponential backoff with **jitter**. Without jitter, a thousand clients that failed together retry together and re-create the outage; full jitter is `sleep = rand(0, base * 2^attempt)`.
- Cap total attempts *and* total elapsed time, and derive each attempt's deadline from a parent context that bounds the whole operation (`context.md`).
- Retrying a non-idempotent write duplicates it. Either make the operation idempotent with a client-supplied key, or do not retry it.

## Common Mistakes

| Mistake | Consequence | Fix |
|---|---|---|
| `if err != nil { return err }` everywhere | Top-level log says "EOF" with no idea which file | Wrap with the operation and its identifier |
| Ignoring the value when `err != nil` — or using it | Some APIs return a partial value *and* an error (`io.Reader` returns n>0 with `io.EOF`) | Read the doc for that function; for `Read`, process `n` bytes first, then handle the error |
| `errors.New` inside a function used as a sentinel | New instance per call, so `errors.Is` never matches | Package-level `var Err… = errors.New(...)` |
| Logging *and* returning the same error | Every layer logs it; one failure becomes six lines that look like six failures | Log where you handle it, return where you do not |
| `errors.Is` on a wrapped `*MyErr` looking for a field | `Is` compares identity, not shape | `errors.As` |
| `defer f.Close()` on a file you wrote | Close reports the flush error and you dropped it — silent truncated file | Named return + `defer func(){ err = errors.Join(err, f.Close()) }()` (`io.md`) |
| `panic` in a request handler for a bad parameter | 500 with a dropped connection instead of a 400 | Return a typed error the middleware maps to a status |

## Back To SKILL.md

Core Rule 2 fixes the wrap policy; Core Rule 3 fixes the typed-nil rule. Cancellation errors: `context.md`. Error contracts across an exported API: `idioms.md`.
