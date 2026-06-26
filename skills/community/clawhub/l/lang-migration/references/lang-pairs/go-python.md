# Language Pair: Go → Python

**Difficulty tier**: Low-Moderate (both GC; error model is the main structural shift)

**Key differences**:
- Memory: Both GC — no ownership to translate
- Errors: Go multi-return `(T, error)` → Python exceptions
- Types: Go static → Python `typing` (maintain all annotations)
- Goroutines: Go goroutines → Python `asyncio` or `threading`
- Interfaces: Go implicit interfaces → Python `Protocol`
- Zero values: Go zero-initializes everything → Python has no zero values (use `None` or defaults)
- Nil: Go `nil` → Python `None`
- Multiple return values: Go `(A, B)` → Python `tuple[A, B]`

---

## Pre-Mapped Core Types

| Go | Python | Equivalence | Notes |
|---|---|---|---|
| `int` / `int64` | `int` | behavioral | Python int is unbounded; document original width |
| `int32` / `int16` / `int8` | `int` | behavioral | Add range comment |
| `uint64` etc. | `int` | behavioral | Python has no unsigned; add `assert n >= 0` |
| `float64` | `float` | structural | |
| `float32` | `float` | behavioral | Python float is f64; precision widening |
| `bool` | `bool` | structural | |
| `string` | `str` | structural | |
| `[]byte` | `bytes` | structural | |
| `nil` | `None` | structural | |
| `[]T` (slice) | `list[T]` | structural | |
| `[N]T` (array) | `list[T]` or `tuple` | behavioral | Fixed-size; document N as invariant |
| `map[K]V` | `dict[K, V]` | behavioral | Python preserves insertion order; Go map order is random |
| `struct{}` (empty) | None / sentinel | structural | Used as set values in Go: `map[K]struct{}` → `set[K]` |
| `map[K]struct{}` | `set[K]` | structural | |
| `chan T` | `queue.Queue` | structural | |
| `interface{}` / `any` | `Any` | structural | |

---

## Multiple Return Values → Tuple or Exception

Go's most distinctive pattern: functions return `(value, error)`.

**Go:**
```go
func divide(a, b float64) (float64, error) {
    if b == 0 {
        return 0, fmt.Errorf("division by zero")
    }
    return a / b, nil
}
```

**Python:**
```python
def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("division by zero")
    return a / b
```

**Rule for `(T, error)` returns**:
- When `error != nil`, the Go function signals failure → raise an exception in Python
- When `error == nil`, the Go function succeeds → return the value (not a tuple)
- NEVER translate `(T, error)` to `tuple[T, Optional[Exception]]` — that is not Pythonic and loses the exception flow

**Rule for genuine multi-returns** (not error tuples):
```go
func minMax(data []int) (int, int) { ... }  // returns two values, no error
```
```python
def min_max(data: list[int]) -> tuple[int, int]: ...  # Python tuple return
```

---

## Error Types → Exception Classes

**Go:**
```go
var ErrNotFound = errors.New("not found")

type ValidationError struct {
    Field   string
    Message string
}
func (e *ValidationError) Error() string {
    return fmt.Sprintf("validation error on %s: %s", e.Field, e.Message)
}
```

**Python:**
```python
class NotFoundError(Exception): pass

class ValidationError(Exception):
    def __init__(self, field: str, message: str) -> None:
        self.field = field
        self.message = message
        super().__init__(f"validation error on {field}: {message}")
```

**Rule**: Each Go `var Err* = errors.New(...)` → Python exception class.
Each Go error struct with `Error() string` → Python exception class with matching `__init__`.

---

## Interface → Protocol

**Go:**
```go
type Reader interface {
    Read(p []byte) (n int, err error)
}
type Writer interface {
    Write(p []byte) (n int, err error)
}
type ReadWriter interface {
    Reader
    Writer
}
```

**Python:**
```python
from typing import Protocol

class Reader(Protocol):
    def read(self, n: int) -> bytes: ...

class Writer(Protocol):
    def write(self, data: bytes) -> int: ...

class ReadWriter(Reader, Writer, Protocol): ...
```

Go's implicit interface satisfaction → Python's structural `Protocol` (any class with matching methods satisfies it automatically).

---

## Struct → Class / Dataclass

**Go:**
```go
type Person struct {
    Name string
    Age  int
    Tags []string
}

func NewPerson(name string, age int) *Person {
    return &Person{Name: name, Age: age, Tags: []string{}}
}

func (p *Person) AddTag(tag string) {
    p.Tags = append(p.Tags, tag)
}
```

**Python:**
```python
from dataclasses import dataclass, field

@dataclass
class Person:
    name: str
    age: int
    tags: list[str] = field(default_factory=list)

    def add_tag(self, tag: str) -> None:
        self.tags.append(tag)
```

Use `@dataclass` when the Go struct is a plain data container.
Use a regular class when the struct has significant behavior.

---

## Zero Value Convention

Go zero-initializes all variables (`0`, `""`, `false`, `nil`, etc.).
Python does not — explicitly set defaults in `__init__` or dataclass `field(default=...)`:

```go
// Go: declared but not initialized — has zero value
var count int      // 0
var name string    // ""
var active bool    // false
var items []int    // nil (but not the same as empty slice)
```

```python
# Python: must be explicit
count: int = 0
name: str = ""
active: bool = False
items: list[int] = []   # Note: [] != nil; Go's nil slice is distinct from empty
# ZERO-VALUE NOTE: Go nil slice and empty slice behave identically for append/len/range.
# Python list is equivalent to Go empty slice. No None needed.
```

---

## Goroutines → asyncio / threading

| Go pattern | Python equivalent | Notes |
|---|---|---|
| `go func(){}()` (fire and forget) | `asyncio.create_task(coro())` | Requires async context |
| `go func(){}()` (CPU work) | `threading.Thread(target=fn).start()` | For CPU-bound parallel work |
| `sync.WaitGroup` | `asyncio.gather()` or `threading.Barrier` | |
| `chan T` (unbuffered) | `asyncio.Queue(maxsize=1)` | |
| `chan T` (buffered, n) | `queue.Queue(maxsize=n)` | |
| `select` statement | `asyncio.wait` with `FIRST_COMPLETED` | |
| `sync.Mutex` | `threading.Lock()` | |
| `sync.RWMutex` | `threading.RLock()` | |
| `sync.Once` | `threading.Event()` | |
| `context.Context` | pass cancellation flag or use `asyncio.CancelledError` | |

---

## Goroutine + Channel Pattern

**Go:**
```go
func producer(ch chan<- int, max int) {
    for i := 0; i < max; i++ {
        ch <- i
    }
    close(ch)
}
```

**Python (asyncio):**
```python
async def producer(queue: asyncio.Queue[int], max_val: int) -> None:
    for i in range(max_val):
        await queue.put(i)
    await queue.put(None)  # sentinel instead of close()
```

---

## `defer` → Context Manager / `try/finally`

**Go:**
```go
func processFile(path string) error {
    f, err := os.Open(path)
    if err != nil { return err }
    defer f.Close()
    // ... use f
    return nil
}
```

**Python:**
```python
def process_file(path: str) -> None:
    with open(path, 'r') as f:
        # ... use f
        pass  # f.close() called automatically by context manager
```

Multiple `defer`s (LIFO order) → nested `with` statements or `try/finally`:
```python
try:
    resource1 = acquire1()
    try:
        resource2 = acquire2()
        # work
    finally:
        resource2.release()
finally:
    resource1.release()
```

---

## Ecosystem Gaps

| Go | Gap | Python |
|---|---|---|
| `map` random iteration order | Python dict is ordered (3.7+) | No action needed; Python is stricter |
| `[N]T` fixed-size array | Python list is dynamic | Use `list` with size invariant comment |
| Method sets (pointer vs value receiver) | No distinction in Python | All methods are on the class |
| `iota` in const blocks | No equivalent | Use `enum.auto()` or explicit values |
| Build tags (`//go:build`) | No direct equivalent | Use environment variables or conditional imports |
| `init()` functions | Module-level code in Python | Top-level statements in the module |
| `go generate` | Custom scripts or `makefile` | |

---

## Naming Convention Conversion

| Go | Python |
|---|---|
| `CamelCase` (exported) | `snake_case` |
| `camelCase` (unexported) | `_snake_case` (private by convention) |
| `MixedCaps` for acronyms (`HTTPServer`) | `http_server` |
| Receiver name (`func (s *Server)`) | `self` |
| Error variable `err` | Exception (no variable needed usually) |

---

## Testing Toolchain

| Go | Python | Notes |
|---|---|---|
| `go test ./...` | `pytest` | |
| `t.Errorf(...)` | `assert ...` or `pytest.fail(...)` | |
| `t.Fatal(...)` | `pytest.fail(...)` or raise | |
| Table-driven tests | `@pytest.mark.parametrize` | Very common Go pattern; direct equivalent |
| Benchmark `b.N` | `pytest-benchmark` | |
| `testing/mock` | PROHIBITED — real implementations only | |
| `go vet` | `mypy .` | |
| `gofmt` | `black .` | |
| `golangci-lint` | `ruff check .` | |

## Build / CI

```yaml
# Go (source):
- run: go test ./...
- run: go vet ./...

# Python (target):
- run: pip install -r requirements.txt
- run: pytest
- run: mypy .
- run: ruff check .
- run: black --check .
```
