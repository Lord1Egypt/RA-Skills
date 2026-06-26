---
name: go-patterns
description: Go language patterns for 2026 — concurrency with errgroup, error wrapping, HTTP servers, gRPC, database access, testing, and CLI with Cobra
version: 1.0.0
tags:
  - go
  - golang
  - backend
  - concurrency
  - midos
---

# Go Language Patterns & Best Practices

## Description

Production Go patterns for Go 1.24+ covering the full development lifecycle. Includes idiomatic concurrency with errgroup and context cancellation, error wrapping with %w, HTTP servers with Chi router, PostgreSQL with pgx, gRPC services, table-driven testing, CLI tools with Cobra, and performance profiling with pprof. Covers Go 1.18+ generics, Go 1.22+ range-over-integers, and Go 1.23+ iterators.

## Usage

Install this skill to get production-ready Go patterns including:
- context.Context propagation for all I/O operations
- errgroup for managing concurrent goroutines safely
- Error wrapping with %w and errors.Is() / errors.As()
- Standard project layout (cmd/, internal/, pkg/)
- Worker pools, fan-out/fan-in, and select multiplexing

When working on Go projects, this skill provides context for:
- Choosing between pgx, GORM, and sqlc for database access
- Structuring HTTP servers with graceful shutdown
- Building gRPC services with interceptors
- Preventing goroutine leaks and data races
- Profiling with pprof before optimizing

## Key Patterns

### Context for Cancellation — MANDATORY for I/O

```go
// Always pass context as first parameter for I/O functions
func FetchData(ctx context.Context, url string) ([]byte, error) {
    req, err := http.NewRequestWithContext(ctx, "GET", url, nil)
    if err != nil { return nil, err }
    resp, err := http.DefaultClient.Do(req)
    if err != nil { return nil, err }
    defer resp.Body.Close()
    return io.ReadAll(resp.Body)
}

// Caller controls the timeout
ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
defer cancel()
data, err := FetchData(ctx, "https://api.example.com/data")
```

### errgroup for Concurrent Tasks

```go
func ProcessItems(ctx context.Context, items []string) error {
    g, ctx := errgroup.WithContext(ctx)
    g.SetLimit(5)  // cap at 5 concurrent goroutines

    for _, item := range items {
        item := item  // capture loop variable
        g.Go(func() error {
            return processOne(ctx, item)
        })
    }
    return g.Wait()  // returns first error
}
```

### Error Wrapping

```go
// Wrap with %w to preserve the error chain
func ReadConfig(path string) (Config, error) {
    data, err := os.ReadFile(path)
    if err != nil {
        return Config{}, fmt.Errorf("read config at %s: %w", path, err)
    }
    var cfg Config
    if err := json.Unmarshal(data, &cfg); err != nil {
        return Config{}, fmt.Errorf("parse config: %w", err)
    }
    return cfg, nil
}

// errors.Is() works with wrapped errors; == does not
if errors.Is(err, ErrNotFound) { ... }

// errors.As() extracts custom error types from chain
var valErr *ValidationError
if errors.As(err, &valErr) {
    fmt.Printf("Invalid field: %s\n", valErr.Field)
}
```

### Standard Project Layout

```
myapp/
├── cmd/myapp/main.go        # Entry point
├── internal/
│   ├── domain/              # Business logic (unexported)
│   ├── service/             # Application services
│   ├── repository/          # Data access layer
│   └── http/                # HTTP handlers
├── pkg/                     # Public libraries
├── migrations/              # SQL migration files
└── go.mod
```

`internal/` is enforced by the Go compiler. Never create /src.

### Chi Router (Recommended)

```go
r := chi.NewRouter()
r.Use(middleware.Logger)
r.Use(middleware.Recoverer)
r.Use(middleware.RequestID)

r.Get("/", homeHandler)
r.Post("/users", createUserHandler)
r.Route("/api", func(r chi.Router) {
    r.Use(authMiddleware)
    r.Get("/profile", getProfileHandler)
})
http.ListenAndServe(":8080", r)
```

### Graceful Shutdown

```go
server := &http.Server{
    Addr: ":8080", Handler: setupRoutes(),
    ReadTimeout: 5 * time.Second, WriteTimeout: 5 * time.Second,
}
sigChan := make(chan os.Signal, 1)
signal.Notify(sigChan, syscall.SIGINT, syscall.SIGTERM)
go func() {
    <-sigChan
    ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
    defer cancel()
    server.Shutdown(ctx)
}()
if err := server.ListenAndServe(); err != nil && err != http.ErrServerClosed {
    log.Fatalf("server error: %v", err)
}
```

### pgx — Best PostgreSQL Driver

```go
config, _ := pgxpool.ParseConfig("postgres://user:pass@localhost/db")
config.MaxConns = 25
pool, err := pgxpool.NewWithConfig(context.Background(), config)

var id int; var name string
err = pool.QueryRow(ctx, "SELECT id, name FROM users WHERE id = $1", 1).Scan(&id, &name)
if errors.Is(err, pgx.ErrNoRows) { fmt.Println("not found") }
```

Database selection: `pgx` for high performance raw SQL, `GORM` for complex relationships, `sqlc` for type-safe Go from SQL annotations.

### Table-Driven Tests

```go
func TestAdd(t *testing.T) {
    tests := []struct{ name string; a, b, expected int }{
        {"positive", 2, 3, 5},
        {"negative", -2, -3, -5},
        {"zero", 0, 0, 0},
    }
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            if got := Add(tt.a, tt.b); got != tt.expected {
                t.Errorf("Add(%d, %d) = %d, want %d", tt.a, tt.b, got, tt.expected)
            }
        })
    }
}
```

### Mocking with Interfaces

```go
type Database interface {
    GetUser(ctx context.Context, id int) (User, error)
}
// Inject the interface, not the concrete type
type UserService struct { db Database }

// Mock for testing
type MockDB struct{}
func (m *MockDB) GetUser(ctx context.Context, id int) (User, error) {
    return User{ID: id, Name: "Mock"}, nil
}
```

### Cobra CLI

```go
var rootCmd = &cobra.Command{Use: "myapp", Short: "My application"}
var counterCmd = &cobra.Command{
    Use: "count", Args: cobra.ExactArgs(1),
    RunE: func(cmd *cobra.Command, args []string) error {
        max, _ := cmd.Flags().GetInt("max")
        fmt.Printf("counting to %d\n", max)
        return nil
    },
}
func init() {
    rootCmd.AddCommand(counterCmd)
    counterCmd.Flags().IntP("max", "m", 10, "maximum count")
}
```

### Performance Tips

- Pre-allocate slices: `make([]T, 0, capacity)` — avoids repeated allocations
- String concat in loops: use `strings.Builder` not `+` (O(n) vs O(n^2))
- Profile first: `go tool pprof http://localhost:6060/debug/pprof/profile?seconds=30`

### Anti-Patterns

| Problem | Solution |
|---|---|
| Goroutine leak (no exit) | Add `case <-ctx.Done(): return` in goroutine loops |
| `range ch` never exits | Sender must `close(ch)` after done |
| Concurrent map writes | Protect with `sync.RWMutex` or use `sync.Map` |
| `defer f.Close()` in loop | Wrap loop body in a named function |

## Tools & References

- [Effective Go](https://go.dev/doc/effective_go)
- [Context Best Practices](https://go.dev/blog/context)
- [Error Handling in Go 1.13+](https://go.dev/blog/go1.13-errors)
- [Chi Router](https://github.com/go-chi/chi)
- [pgx Documentation](https://github.com/jackc/pgx)
- [gRPC in Go](https://grpc.io/docs/languages/go/)
- [Cobra CLI](https://github.com/spf13/cobra)

---
*Published by [MidOS](https://midos.dev) — MCP Community Library*
