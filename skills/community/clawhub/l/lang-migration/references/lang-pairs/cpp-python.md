# Language Pair: C++ → Python

**Difficulty tier**: Moderate (RAII dissolves; templates become generics; exceptions survive)

**Key differences**:
- Memory: C++ RAII (`unique_ptr`, `shared_ptr`) → Python GC (RAII destructor logic becomes `__del__` or context managers)
- Templates: C++ templates → Python generics (`TypeVar`, `Generic`) or `overload`
- Multiple inheritance: C++ → Python (both support it; map directly)
- Operator overloading: C++ → Python dunder methods (`__add__`, `__eq__`, etc.)
- Exceptions: C++ → Python (both use try/catch–try/except; very similar)
- `const` correctness: C++ `const` → Python has no enforcement; document as comments
- Namespaces: C++ `namespace` → Python modules / classes
- `constexpr`: C++ compile-time → Python module-level constants

---

## Pre-Mapped Core Types

| C++ | Python | Equivalence | Notes |
|---|---|---|---|
| `int32_t` / `int64_t` | `int` | behavioral | Document original width |
| `uint32_t` / `uint64_t` | `int` | behavioral | Add non-negative invariant |
| `float` | `float` | behavioral | Precision widening (f32→f64) |
| `double` | `float` | structural | |
| `bool` | `bool` | structural | |
| `std::string` | `str` | structural | |
| `std::vector<T>` | `list[T]` | structural | |
| `std::array<T, N>` | `list[T]` | behavioral | Document fixed size N as invariant |
| `std::tuple<A,B>` | `tuple[A, B]` | structural | |
| `std::pair<A, B>` | `tuple[A, B]` | structural | |
| `std::map<K,V>` | `dict[K,V]` | behavioral | `std::map` is sorted; Python dict is insertion-ordered |
| `std::unordered_map<K,V>` | `dict[K,V]` | behavioral | No ordering difference |
| `std::set<T>` | `set[T]` (sorted) | behavioral | `std::set` is sorted; Python `set` is not; use `sortedcontainers.SortedSet` if order matters |
| `std::unordered_set<T>` | `set[T]` | structural | |
| `std::optional<T>` | `Optional[T]` | structural | |
| `std::variant<A,B>` | `Union[A, B]` | structural | |
| `std::deque<T>` | `collections.deque` | structural | |
| `std::priority_queue<T>` | `heapq` | behavioral | C++ default is max-heap; Python `heapq` is min-heap — CRITICAL |
| `std::unique_ptr<T>` | T directly | behavioral | Ownership → GC; document original owner |
| `std::shared_ptr<T>` | T directly | behavioral | Sharing → GC; document |
| `std::weak_ptr<T>` | `weakref.ref(obj)` | structural | `import weakref` |
| `nullptr` | `None` | structural | |
| `void*` | `Any` | behavioral | Document actual types |

---

## RAII → Context Manager / `__del__`

RAII in C++ ensures cleanup on scope exit. Map to Python context managers:

**C++:**
```cpp
class FileHandle {
    FILE* f_;
public:
    explicit FileHandle(const std::string& path) {
        f_ = fopen(path.c_str(), "rb");
        if (!f_) throw std::runtime_error("cannot open: " + path);
    }
    ~FileHandle() { if (f_) fclose(f_); }  // RAII destructor
    // ... read methods
};
```

**Python:**
```python
class FileHandle:
    def __init__(self, path: str) -> None:
        try:
            self._f = open(path, 'rb')
        except OSError:
            raise RuntimeError(f"cannot open: {path}")

    def __enter__(self) -> 'FileHandle':
        return self

    def __exit__(self, *args: object) -> None:
        self._f.close()

    # C++ RAII NOTE: destructor guaranteed close on scope exit.
    # In Python, use `with FileHandle(path) as fh:` to match this guarantee.
    def __del__(self) -> None:
        if hasattr(self, '_f'):
            self._f.close()
```

Document all RAII-dependent classes with: `# RAII NOTE: use as context manager to guarantee cleanup`

---

## Templates → TypeVar / Generic

**C++:**
```cpp
template<typename T>
class Stack {
    std::vector<T> data_;
public:
    void push(T value) { data_.push_back(std::move(value)); }
    T pop() {
        if (data_.empty()) throw std::underflow_error("empty stack");
        T val = data_.back();
        data_.pop_back();
        return val;
    }
    bool empty() const { return data_.empty(); }
};
```

**Python:**
```python
from typing import Generic, TypeVar
T = TypeVar('T')

class Stack(Generic[T]):
    def __init__(self) -> None:
        self._data: list[T] = []

    def push(self, value: T) -> None:
        self._data.append(value)

    def pop(self) -> T:
        if not self._data:
            raise IndexError("empty stack")
        return self._data.pop()

    def empty(self) -> bool:
        return len(self._data) == 0
```

Template specialization (`template<> class Stack<bool>`) → Python `@overload` or subclass.

---

## Operator Overloading → Dunder Methods

| C++ operator | Python dunder | Notes |
|---|---|---|
| `operator==` | `__eq__` | Also define `__hash__` if implementing `__eq__` |
| `operator<` | `__lt__` | Add `@functools.total_ordering` + `__eq__` to get all comparisons |
| `operator+` | `__add__` | |
| `operator+=` | `__iadd__` | |
| `operator[]` | `__getitem__` / `__setitem__` | |
| `operator()` (functor) | `__call__` | |
| `operator<<` (stream) | `__str__` / `__repr__` | |
| `operator bool()` | `__bool__` | |
| `operator size_t()` (hash) | `__hash__` | |

**C++:**
```cpp
struct Vec2 {
    float x, y;
    Vec2 operator+(const Vec2& o) const { return {x + o.x, y + o.y}; }
    bool operator==(const Vec2& o) const { return x == o.x && y == o.y; }
};
```

**Python:**
```python
import math
from dataclasses import dataclass

@dataclass
class Vec2:
    x: float
    y: float

    def __add__(self, other: 'Vec2') -> 'Vec2':
        return Vec2(self.x + other.x, self.y + other.y)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vec2): return NotImplemented
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))
```

---

## Multiple Inheritance → Python Multiple Inheritance

C++ multiple inheritance maps directly (Python supports it with MRO):

**C++:**
```cpp
class Flyable { virtual void fly() = 0; };
class Swimmable { virtual void swim() = 0; };
class Duck : public Flyable, public Swimmable { ... };
```

**Python:**
```python
from abc import ABC, abstractmethod

class Flyable(ABC):
    @abstractmethod
    def fly(self) -> None: ...

class Swimmable(ABC):
    @abstractmethod
    def swim(self) -> None: ...

class Duck(Flyable, Swimmable):
    def fly(self) -> None: ...
    def swim(self) -> None: ...
```

For diamond inheritance: Python MRO (C3 linearization) differs from C++ virtual inheritance. Document differences in `translation_notes`.

---

## `std::priority_queue` Direction (Critical)

`std::priority_queue` is a **max-heap** by default.
Python `heapq` is a **min-heap**.

```cpp
// C++: max-heap
std::priority_queue<int> pq;
pq.push(3); pq.push(1); pq.push(2);
int top = pq.top();  // 3 (maximum)
```

```python
import heapq
# Python min-heap — negate values for max-heap behavior
pq: list[int] = []
for v in [3, 1, 2]:
    heapq.heappush(pq, -v)   # negate for max-heap
top = -pq[0]  # 3 (maximum, negated back)
```

Always check the IPO registry to confirm the heap direction.

---

## `std::map` vs `dict` Ordering

`std::map` is a sorted BST (always sorted by key).
`std::unordered_map` has no order guarantee.
Python `dict` preserves insertion order (not sorted).

When migrating `std::map`:
```python
# If sorted access is needed:
from sortedcontainers import SortedDict
data: SortedDict[str, int] = SortedDict()

# If sorted access is NOT needed (most cases):
data: dict[str, int] = {}
# ORDERING NOTE: C++ source used std::map (sorted). Python dict is insertion-ordered.
# If sorted iteration is required, use: sorted(data.items())
```

---

## `constexpr` → Module Constants

```cpp
constexpr int MAX_RETRIES = 3;
constexpr double PI = 3.14159265358979;
constexpr std::array<int, 4> VALID_PORTS = {80, 443, 8080, 8443};
```

```python
from typing import Final

MAX_RETRIES: Final[int] = 3
PI: Final[float] = 3.14159265358979
VALID_PORTS: Final[tuple[int, ...]] = (80, 443, 8080, 8443)
```

---

## Namespace → Module

```cpp
namespace crypto {
namespace internal {
    void hash_block(const uint8_t* data, size_t len, State* state);
}
}
```

```python
# crypto/internal.py
def hash_block(data: bytes, state: State) -> None:
    ...
```

C++ namespaces → Python module hierarchy. Translate `namespace a::b::c` → `a/b/c.py`.

---

## Ecosystem Gaps

| C++ | Gap | Python |
|---|---|---|
| `std::map` sorted order | Python dict is insertion-ordered | Use `SortedDict` from `sortedcontainers` |
| `std::priority_queue` max-heap | Python `heapq` is min-heap | Negate values for max-heap |
| Template specialization | No direct equivalent | Use `@overload` + isinstance dispatch |
| RAII guarantee | Python GC is non-deterministic | Use context managers; document |
| `const` correctness | Python has no const enforcement | Add `# CONST:` comments; use `Final` for module-level |
| `consteval` / `constexpr` functions | No compile-time execution | Module-level computation at import time |
| `std::thread` with hardware parallelism | Python GIL limits CPU parallelism | Use `multiprocessing` for CPU-bound; `asyncio` for I/O |

---

## Testing Toolchain

| C++ | Python | Notes |
|---|---|---|
| Google Test | `pytest` | |
| `EXPECT_EQ(a, b)` | `assert a == b` | |
| `EXPECT_THROW(fn(), ExType)` | `pytest.raises(ExType)` | |
| `EXPECT_NEAR(a, b, tol)` | `assert abs(a - b) < tol` or `pytest.approx` | |
| Catch2 | `pytest` | |
| `unittest.mock` equivalent | PROHIBITED | Real implementations only |
| AddressSanitizer | No equivalent (GC handles) | |
| `clang-format` | `black` | |
| `clang-tidy` / `cppcheck` | `ruff check .` | |
| `valgrind` | Not needed | |

## Build / CI

```yaml
# C++ (source):
- run: cmake -B build && cmake --build build
- run: ctest --test-dir build

# Python (target):
- run: pip install -r requirements.txt
- run: pytest
- run: mypy .
- run: ruff check .
- run: black --check .
```
