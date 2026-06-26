# Language Pair: Rust → Python

**Difficulty tier**: Moderate (ownership/types dissolve into GC; explicit becomes implicit)

**Direction note**: Migrating FROM a systems language TO a high-level language.
The target (Python) is more expressive but less explicit. The primary challenge is
NOT losing semantic information during the "simplification" — ownership semantics,
error types, and precision constraints must be preserved as documentation even when
the target language doesn't enforce them.

**Key differences**:
- Memory: Rust explicit ownership → Python GC (no action needed; document original intent)
- Types: Rust static → Python `typing` annotations (maintain all annotations; don't drop them)
- Errors: Rust `Result<T, E>` → Python exceptions
- Traits: Rust traits → Python `Protocol` or ABC
- Generics: Rust `<T: Trait>` → Python `TypeVar` + `Generic`
- Lifetimes: Rust `'a` → no equivalent; document as invariant comment
- `unsafe`: Rust unsafe blocks → Python has no concept; document what invariant was being upheld

---

## Pre-Mapped Core Types

| Rust | Python | Equivalence | Notes |
|---|---|---|---|
| `i8/i16/i32/i64` | `int` | behavioral | Python int is unbounded; document original bit width as comment |
| `u8/u16/u32/u64` | `int` | behavioral | Python has no unsigned; add range assertion if source checks overflow |
| `i128/u128` | `int` | structural | Python int natively handles |
| `f32` | `float` | behavioral | Python float is f64; document precision widening |
| `f64` | `float` | structural | Identical IEEE 754 |
| `bool` | `bool` | structural | |
| `String` / `&str` | `str` | structural | |
| `Vec<u8>` / `&[u8]` | `bytes` | structural | |
| `Option<T>` | `Optional[T]` | structural | `None` maps to `None` |
| `Result<T, E>` | return value or exception | structural | See error handling section |
| `Vec<T>` | `list[T]` | structural | |
| `HashMap<K,V>` | `dict[K,V]` | behavioral | Python dict preserves insertion order; HashMap does not |
| `BTreeMap<K,V>` | `dict[K,V]` (sorted) | structural | Python dict + `sorted()` on access, or `SortedDict` (sortedcontainers) |
| `HashSet<T>` | `set[T]` | structural | |
| `BTreeSet<T>` | `set` (sorted) | structural | Use `sortedcontainers.SortedSet` |
| `(A, B)` tuple | `tuple[A, B]` | structural | |
| `VecDeque<T>` | `collections.deque` | structural | |
| `Arc<T>` | T directly | behavioral | Python GC handles sharing; no Arc needed; document that source was shared |
| `Mutex<T>` | `threading.Lock()` | structural | Wrap shared state in a Lock |
| `Box<T>` | T directly | behavioral | Python heap-allocates everything |
| `Pin<T>` | No equivalent | behavioral | Document the self-referential invariant as a comment |

---

## Ownership → Comment Convention

Rust's ownership semantics carry semantic information that Python's GC erases.
Preserve this information as structured comments:

```python
# OWNERSHIP NOTE: In Rust source, this function took ownership of `data` (Vec<u8>).
# Callers must not use `data` after this call. Python does not enforce this.
# INVARIANT: data must not be aliased after passing to this function.
def process_data(data: bytes) -> Result:
    ...
```

For every function that in Rust took ownership (not `&` or `&mut`), add the comment.
For every `&mut` parameter, note it was mutated:

```python
# MUTATION NOTE: In Rust source, this parameter was `&mut` (mutated in place).
# Python equivalent mutates self or the passed object directly.
```

---

## Lifetime Annotations → Invariant Comments

Rust lifetimes express "this reference must not outlive X".
Python has no lifetimes but the invariant still matters for correctness:

```rust
// Rust:
fn get_name<'a>(person: &'a Person) -> &'a str { &person.name }
```

```python
# Python:
def get_name(person: Person) -> str:
    # LIFETIME NOTE: In Rust source, the returned &str was tied to person's lifetime.
    # Do not store the result beyond person's validity scope.
    return person.name
```

---

## Error Handling: Result → Exceptions

**Rust:**
```rust
#[derive(Debug)]
enum ParseError { InvalidInt(String), Overflow }

fn parse_value(s: &str) -> Result<i64, ParseError> {
    let n = s.parse::<i64>().map_err(|_| ParseError::InvalidInt(s.to_string()))?;
    if n > MAX { return Err(ParseError::Overflow); }
    Ok(n)
}
```

**Python:**
```python
class ParseError(Exception): pass
class InvalidIntError(ParseError):
    def __init__(self, s: str): super().__init__(f"invalid int: {s}")
class OverflowError_(ParseError): pass   # avoid shadowing builtin

def parse_value(s: str) -> int:
    try:
        n = int(s)
    except ValueError:
        raise InvalidIntError(s)
    if n > MAX:
        raise OverflowError_()
    return n
```

**Rule**: Each Rust enum variant of an error type → one Python exception class.
`?` operator → function call (let the exception propagate). `map_err` → except+raise.

---

## Traits → Protocol / ABC

**Rust:**
```rust
trait Serialize {
    fn serialize(&self) -> Vec<u8>;
    fn name(&self) -> &str;
}
```

**Python:**
```python
from typing import Protocol

class Serialize(Protocol):
    def serialize(self) -> bytes: ...
    def name(self) -> str: ...
```

Use `Protocol` for structural typing (matches Rust's trait-as-interface model).
Use `ABC` only when default method implementations need to be inherited.

---

## Generics → TypeVar

**Rust:**
```rust
fn max_of<T: PartialOrd>(a: T, b: T) -> T {
    if a > b { a } else { b }
}
```

**Python:**
```python
from typing import TypeVar
T = TypeVar('T')

def max_of(a: T, b: T) -> T:
    # GENERIC NOTE: Rust source constrained T: PartialOrd.
    # Python has no compile-time constraint; caller must ensure comparable types.
    return a if a > b else b
```

For complex trait bounds (`T: Debug + Clone + Send`), document them:
```python
# TYPE CONSTRAINTS (from Rust source):
#   T must support: comparison (PartialOrd), copying (Clone), repr (Debug)
```

---

## Iterators → Generator / Comprehension

**Rust:**
```rust
fn evens_doubled(data: &[i64]) -> Vec<i64> {
    data.iter()
        .filter(|&&x| x % 2 == 0)
        .map(|&x| x * 2)
        .collect()
}
```

**Python:**
```python
def evens_doubled(data: list[int]) -> list[int]:
    return [x * 2 for x in data if x % 2 == 0]
```

Rust iterator chains map cleanly to list comprehensions. Maintain the same filter-before-map order.

For lazy iterators (no `.collect()`), use Python generators:
```rust
// Rust: returns impl Iterator<Item=i64>
fn evens(data: &[i64]) -> impl Iterator<Item=&i64> { data.iter().filter(|&&x| x % 2 == 0) }
```
```python
from typing import Iterator
def evens(data: list[int]) -> Iterator[int]:
    return (x for x in data if x % 2 == 0)
```

---

## Struct + impl → Class

**Rust:**
```rust
struct Counter { count: u64, max: u64 }

impl Counter {
    fn new(max: u64) -> Self { Self { count: 0, max } }
    fn increment(&mut self) -> Option<u64> {
        if self.count >= self.max { return None; }
        self.count += 1;
        Some(self.count)
    }
}
```

**Python:**
```python
class Counter:
    # TYPE NOTE: count and max were u64 in Rust source (non-negative, max 2^64-1)
    def __init__(self, max_val: int) -> None:
        self._count: int = 0
        self._max: int = max_val

    def increment(self) -> Optional[int]:
        if self._count >= self._max:
            return None
        self._count += 1
        return self._count
```

---

## `unsafe` Blocks → Document and Validate

Rust `unsafe` blocks bypass memory safety guarantees. In Python, these constraints
must become runtime assertions or documented invariants:

```rust
// Rust:
unsafe fn read_raw(ptr: *const u8, len: usize) -> &[u8] {
    std::slice::from_raw_parts(ptr, len)
}
```

```python
def read_raw(data: bytes, offset: int, length: int) -> bytes:
    # UNSAFE NOTE: Rust source used raw pointer arithmetic.
    # Python equivalent uses slice indexing. The following assertion
    # replaces the memory safety guarantee that Rust's borrow checker provided:
    assert 0 <= offset and offset + length <= len(data), \
        f"out-of-bounds read: offset={offset}, len={length}, data_len={len(data)}"
    return data[offset:offset + length]
```

---

## Concurrency Migration

| Rust | Python | Notes |
|---|---|---|
| `std::thread::spawn` | `threading.Thread` | Python has GIL; true parallelism via `multiprocessing` |
| `Arc<Mutex<T>>` | shared object + `threading.Lock()` | |
| `tokio::spawn` (async) | `asyncio.create_task` | |
| `async fn` / `.await` | `async def` / `await` | Same syntax |
| `mpsc::channel` | `queue.Queue` | |
| `RwLock<T>` | `threading.RLock()` | |
| `AtomicUsize` | `threading.Lock()` + int | Python has no atomic primitives in stdlib |
| `Send` + `Sync` | No equivalent | Document which types were marked Send/Sync |

---

## Ecosystem Gaps

| Rust | Gap | Python equivalent |
|---|---|---|
| Integer overflow detection | Python int never overflows | Add range assertions where Rust used checked arithmetic |
| `#[derive(Debug, Clone, PartialEq)]` | Manual in Python | Implement `__repr__`, `__copy__`, `__eq__` |
| `serde` (serialize/deserialize) | `dataclasses` + `json` or `pydantic` | |
| `criterion` (benchmarks) | `pytest-benchmark` | |
| `cargo test` | `pytest` | |
| `cargo clippy` | `ruff` + `mypy` | |
| `rustfmt` | `black` | |
| `log` + `env_logger` | `logging` stdlib | |

---

## Type Annotation Policy

All Python output MUST have full type annotations (PEP 484).
Rust's static types are the source of truth — do not drop them during migration.

```python
# WRONG: dropping Rust's type information
def process(items, threshold):
    return [x for x in items if x > threshold]

# CORRECT: preserving Rust's type information
def process(items: list[float], threshold: float) -> list[float]:
    return [x for x in items if x > threshold]
```

---

## Testing Toolchain

| Rust | Python | Notes |
|---|---|---|
| `cargo test` / `#[test]` | `pytest` | |
| `#[should_panic]` | `pytest.raises(Exception)` | Match the specific exception type from error mapping |
| `assert_eq!` | `assert a == b` | |
| `proptest` | `hypothesis` | Property-based testing |
| `criterion` | `pytest-benchmark` | |
| `cargo clippy` | `ruff check .` | |
| `rustfmt` | `black .` | |
| `cargo check` | `mypy .` | |

## Build / CI

```yaml
# Rust (source):
- run: cargo test
- run: cargo clippy -- -D warnings

# Python (target):
- run: pip install -r requirements.txt
- run: pytest
- run: mypy .
- run: ruff check .
```
