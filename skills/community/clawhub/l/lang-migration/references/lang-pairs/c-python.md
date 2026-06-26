# Language Pair: C → Python

**Difficulty tier**: Moderate (memory management dissolves; pointer arithmetic becomes indexing)

**Key differences**:
- Memory: C manual malloc/free → Python GC (ownership structures become irrelevant mechanically but must be documented)
- Pointers: C pointers → Python references or indices (never expose raw pointers)
- Types: C weak static → Python `typing` (strengthen, not weaken)
- Strings: C null-terminated `char*` → Python `str` (encoding must be made explicit)
- Error handling: C return codes + errno → Python exceptions
- Arrays: C fixed/dynamic arrays → Python `list` or `bytes`
- Structs: C structs → Python `dataclass` or class
- Function pointers: C `(*fn)(args)` → Python callable / `Callable`

---

## Pre-Mapped Core Types

| C | Python | Equivalence | Notes |
|---|---|---|---|
| `int8_t` | `int` | behavioral | Document original range: [-128, 127] |
| `int16_t` | `int` | behavioral | [-32768, 32767] |
| `int32_t` | `int` | behavioral | |
| `int64_t` | `int` | structural | Python int covers this range |
| `uint8_t` | `int` | behavioral | [0, 255]; add range assertion |
| `uint16_t` / `uint32_t` / `uint64_t` | `int` | behavioral | Document upper bound |
| `float` | `float` | behavioral | Python float is f64; C float is f32 — document precision widening |
| `double` | `float` | structural | |
| `_Bool` / `bool` | `bool` | structural | |
| `char*` (string) | `str` | behavioral | Must determine encoding; default UTF-8 |
| `char*` (bytes) | `bytes` | structural | When used as raw bytes, not text |
| `uint8_t*` + `size_t` | `bytes` | structural | |
| `void*` | `Any` | behavioral | Document what types it actually points to |
| `NULL` | `None` | structural | |
| `T*` (array) + `size_t n` | `list[T]` | structural | The (pointer, length) pair → single list |
| `T[N]` (fixed array) | `list[T]` | behavioral | Document that N was fixed; add `assert len(arr) == N` |
| `struct T` | `@dataclass` class | structural | |
| `enum` | `enum.IntEnum` or `enum.Enum` | structural | |
| `(*fn)(args) → ret` | `Callable[[args], ret]` | structural | |

---

## Pointer Pairs → Single Object

The most common C pattern — a pointer and its associated length — collapses to one Python object:

```c
// C: two parameters representing one logical unit
void process(const uint8_t *data, size_t len);
int find_max(const int *arr, size_t n);
char *join_strings(const char **strs, size_t count);
```

```python
# Python: one parameter
def process(data: bytes) -> None: ...
def find_max(arr: list[int]) -> int: ...
def join_strings(strs: list[str]) -> str: ...
```

**Rule**: Every `(T*, size_t)` pair in C source → one Python collection parameter.
Document the original C signature in a comment:

```python
def process(data: bytes) -> None:
    # C SOURCE: void process(const uint8_t *data, size_t len)
    ...
```

---

## Error Handling: Return Codes → Exceptions

**C:**
```c
typedef enum {
    ERR_OK = 0,
    ERR_NOT_FOUND = 1,
    ERR_INVALID_ARG = 2,
    ERR_OUT_OF_MEMORY = 3
} ErrorCode;

ErrorCode read_record(const char *key, Record *out);
```

**Python:**
```python
class MigrationError(Exception): pass
class NotFoundError(MigrationError): pass
class InvalidArgError(MigrationError): pass
# ERR_OUT_OF_MEMORY: Python raises MemoryError natively; no custom class needed

def read_record(key: str) -> Record:
    # C SOURCE: ErrorCode read_record(const char *key, Record *out)
    # Output parameter `out` becomes the return value.
    ...
```

**Rules**:
- Each non-zero error code → Python exception class
- Output parameters (`T *out`) → return values
- `errno` checks → catch-and-raise at the call site
- `perror()` / `fprintf(stderr, ...)` → `logging.error()`

---

## struct → dataclass

**C:**
```c
typedef struct {
    char name[64];
    int  age;
    float score;
    struct Node *next;  // linked list pointer
} Person;

Person *person_create(const char *name, int age);
void    person_destroy(Person *p);
void    person_set_score(Person *p, float score);
```

**Python:**
```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class Person:
    # C SOURCE: char name[64] — max 63 chars + null terminator
    # INVARIANT: len(name) <= 63
    name: str
    age: int
    score: float = 0.0
    next: Optional['Person'] = None  # linked list — consider using list[Person] instead

    def set_score(self, score: float) -> None:
        # C SOURCE: void person_set_score(Person *p, float score)
        # Note: C used float (32-bit); Python uses float (64-bit)
        self.score = score

# person_create → __init__ (handled by @dataclass)
# person_destroy → no equivalent needed (GC handles memory)
```

---

## Linked List / Tree → Python Native

C frequently uses manual linked lists and trees. Python should replace these with native collections unless the traversal algorithm is the point of the migration:

| C structure | Python equivalent |
|---|---|
| Singly linked list | `list[T]` (or `collections.deque` if front/back ops) |
| Doubly linked list | `collections.deque` |
| Binary search tree | `sortedcontainers.SortedList` or `list` + `bisect` |
| Hash table (open addressing) | `dict` |
| Stack (via linked list) | `list` (append/pop) |
| Queue (via linked list) | `collections.deque` |
| Heap (manual) | `heapq` |

**Exception**: If the data structure implementation IS the algorithm being migrated
(e.g., migrating a B-tree implementation), translate it structurally as a class.

---

## Pointer Arithmetic → Slice Indexing

**C:**
```c
// Walk through buffer with pointer arithmetic
uint8_t *ptr = buffer;
uint8_t *end = buffer + len;
while (ptr < end) {
    process(*ptr);
    ptr++;
}
```

**Python:**
```python
# Python: index-based or direct iteration
for byte in buffer:
    process(byte)
```

**C:**
```c
// Sliding window via pointer arithmetic
for (int i = 0; i <= len - window; i++) {
    process_window(data + i, window);
}
```

**Python:**
```python
for i in range(len(data) - window + 1):
    process_window(data[i:i + window])
```

---

## Function Pointers → Callable

**C:**
```c
typedef int (*Comparator)(const void *a, const void *b);

void sort_array(int *arr, size_t n, Comparator cmp);
```

**Python:**
```python
from typing import Callable

def sort_array(arr: list[int], cmp: Callable[[int, int], int]) -> None:
    # C SOURCE: qsort-style comparator: returns <0, 0, or >0
    # Python: use key function instead where possible, or functools.cmp_to_key
    import functools
    arr.sort(key=functools.cmp_to_key(cmp))
```

For `qsort`-style comparators, use `functools.cmp_to_key`.
For simpler callbacks (`void (*on_event)(Event *)`), use `Callable[[Event], None]`.

---

## Bit Operations

C bit manipulation is common. Python handles it but with integer semantics:

```c
// C: mask and shift (uint32_t assumed)
uint32_t flags = 0;
flags |= (1 << BIT_READY);
bool is_ready = (flags & (1 << BIT_READY)) != 0;
```

```python
# Python: identical syntax, but no fixed bit width
flags: int = 0
flags |= (1 << BIT_READY)
is_ready: bool = bool(flags & (1 << BIT_READY))
# NOTE: Python int is unbounded; C source assumed uint32_t (32-bit).
# If overflow wrapping matters, apply: flags &= 0xFFFFFFFF
```

For every bit operation, document the original bit width and whether wrapping was relied upon.

---

## Memory Allocation Patterns

| C pattern | Python equivalent | Notes |
|---|---|---|
| `malloc(sizeof(T))` | `T()` constructor | GC allocates |
| `calloc(n, sizeof(T))` | `[T() for _ in range(n)]` | Zero-initialized list |
| `realloc(ptr, new_size)` | `list.extend()` or `list[:]` resize | |
| `free(ptr)` | No equivalent | Document that source freed here |
| `strdup(s)` | `str(s)` or `s[:]` | Python strings are immutable; copies are implicit |
| Buffer pool / arena | No direct equivalent | Use a list as the pool |

---

## String Handling

C strings are particularly dangerous to migrate carelessly:

| C | Python | Notes |
|---|---|---|
| `strlen(s)` | `len(s)` | |
| `strcmp(a, b)` | `a == b` | |
| `strncpy(dst, src, n)` | `src[:n]` | |
| `sprintf(buf, fmt, ...)` | `f"{...}"` or `format(...)` | |
| `strtol(s, &end, 10)` | `int(s)` + `try/except ValueError` | |
| `strtod(s, &end)` | `float(s)` + `try/except ValueError` | |
| `sscanf(s, fmt, ...)` | `re.match(pattern, s)` | Determine regex from format string |
| `strchr(s, c)` | `s.find(c)` | Returns -1 if not found (same as C) |
| Null-terminated `\0` | No equivalent needed | Python strings have no null terminator |

**Encoding**: C `char*` has no encoding. When translating to Python `str`, determine the encoding from context (locale, protocol spec, source comments). Default to UTF-8; document the choice.

---

## Ecosystem Gaps

| C | Gap | Python |
|---|---|---|
| Fixed-width integers | Python int unbounded | Add range comments; use `assert` for critical bounds |
| `float` (32-bit) | Python `float` is 64-bit | Precision widening; document |
| `sizeof(T)` | `sys.getsizeof(T)` (different semantics) | Document for serialization/protocol code |
| `#define` macros | Module-level constants | `CONST_NAME: Final = value` |
| `#include` guards | No equivalent | Python modules are imported once |
| Stack allocation | No distinction | Python heap-allocates everything; no action |
| Volatile variables | No equivalent | Document race condition concerns as comments |

---

## Naming Convention

| C | Python |
|---|---|
| `snake_case` functions | `snake_case` (matches) |
| `UPPER_CASE` macros/constants | `UPPER_CASE` with `Final` annotation |
| `PascalCase` structs/typedefs | `PascalCase` classes |
| `_internal` prefix | `_internal` prefix (convention unchanged) |
| `typename_verb` functions | `ClassName.verb()` methods |

---

## Testing Toolchain

| C | Python | Notes |
|---|---|---|
| `cmocka` / `Unity` / `Check` | `pytest` | |
| `assert(condition)` | `assert condition` | |
| Valgrind (memory check) | No equivalent (GC handles memory) | Run `pytest` with `-v` |
| `gcov` / `lcov` | `pytest --cov` | |
| AddressSanitizer | No equivalent needed | |
| `make test` | `pytest` | |

## Build / CI

```yaml
# C (source):
- run: make test
- run: valgrind --leak-check=full ./test_runner

# Python (target):
- run: pip install -r requirements.txt
- run: pytest
- run: mypy .
- run: ruff check .
```
