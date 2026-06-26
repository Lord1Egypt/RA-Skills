# Language Pair: Python → C

**Difficulty tier**: High (manual memory, no stdlib collections, no exceptions)

**Key differences**:
- Memory model: Python GC / C manual malloc/free
- Type system: Python dynamic / C static, weak, implicit coercion
- Error handling: Python exceptions / C return codes + errno
- OOP: Python classes / C structs + function pointers
- Strings: Python str (unicode) / C null-terminated char arrays (encoding is caller's problem)
- Overflow: Python int unbounded / C integer overflow is undefined behavior

---

## Pre-Mapped Core Types

| Python | C | Equivalence | Notes |
|---|---|---|---|
| `int` (small) | `int64_t` | behavioral | Use stdint.h types always; never plain `int` |
| `int` (large) | `__int128` or GMP `mpz_t` | behavioral | GMP library for truly arbitrary precision |
| `float` | `double` | structural | Both IEEE 754 double |
| `bool` | `bool` (stdbool.h) | structural | |
| `str` | `char *` + length | behavioral | ALWAYS carry length separately; never assume null-term is safe |
| `bytes` | `uint8_t *` + size | structural | |
| `None` | `NULL` pointer | structural | Context-dependent |
| `list[T]` | `T *` + length + capacity | structural | Implement as dynamic array struct |
| `dict[K,V]` | hash table struct | structural | Use uthash or implement from scratch |
| `Optional[T]` | pointer (NULL = absent) | structural | |

## Critical: Memory Ownership Protocol

Every function that returns a pointer MUST document who owns it:
```c
// OWNED: caller must free()
char *create_string(const char *src);

// BORROWED: do not free; lifetime tied to container
const char *get_name(const Person *p);
```

Map Python's implicit GC to explicit ownership. For every source object:
1. Where is it created? → `malloc`
2. Where is it consumed/destroyed? → `free`
3. Is it shared? → reference counting struct or copy

## Error Handling Pattern

**Python:**
```python
def parse_int(s: str) -> int:
    try:
        return int(s)
    except ValueError:
        raise ParseError(f"invalid int: {s}")
```

**C:**
```c
typedef enum { PARSE_OK = 0, PARSE_ERROR_INVALID = 1 } ParseResult;

ParseResult parse_int(const char *s, int64_t *out) {
    char *end;
    errno = 0;
    *out = strtoll(s, &end, 10);
    if (errno != 0 || *end != '\0') {
        return PARSE_ERROR_INVALID;
    }
    return PARSE_OK;
}
```

**Rule**: Every Python exception type becomes a C enum value. Every `try` block becomes a caller checking the return code.

## Class → Struct + Function Pointers

**Python:**
```python
class Buffer:
    def __init__(self, capacity: int):
        self.data = bytearray(capacity)
        self.size = 0
    def push(self, byte: int):
        self.data[self.size] = byte
        self.size += 1
```

**C:**
```c
typedef struct {
    uint8_t *data;
    size_t   size;
    size_t   capacity;
} Buffer;

Buffer *buffer_create(size_t capacity) {
    Buffer *b = malloc(sizeof(Buffer));
    b->data = malloc(capacity);
    b->size = 0;
    b->capacity = capacity;
    return b;
}

void buffer_push(Buffer *b, uint8_t byte) {
    b->data[b->size++] = byte;
}

void buffer_destroy(Buffer *b) {
    free(b->data);
    free(b);
}
```

**Rule**: Every Python class becomes a C struct + a set of `typename_verb` functions. Constructor → `_create`. Destructor → `_destroy` (always required).

## Anti-Patterns

| Wrong | Why | Correct |
|---|---|---|
| Plain `int` / `long` | Width is platform-dependent | Use `int32_t`, `int64_t` from stdint.h |
| `gets()`, `strcpy()` without bounds | Buffer overflow | Use `fgets()`, `strncpy()` with explicit sizes |
| Ignoring malloc return value | Null dereference on OOM | Always check: `if (!ptr) { ... }` |
| Global mutable state for "class" state | Not thread-safe, not structural | Pass struct pointer explicitly |
| Signed integer overflow | Undefined behavior in C | Use `__builtin_add_overflow` or cast to unsigned for wrap |

## Ecosystem Gaps

| Python | Gap | Compensation |
|---|---|---|
| Dynamic `list` | No stdlib equivalent | Use dynamic array pattern (data+size+capacity struct) |
| `dict` | No stdlib equivalent | Use `uthash` library or implement open-addressing hash table |
| `str.split/join/format` | No stdlib equivalent | Use `strtok_r`, manual formatting, or `asprintf` |
| Exception traceback | No equivalent | Log error context manually at each return site |
| GC | No equivalent | Explicit malloc/free; document ownership in every function |
| `random` | `rand()` (low quality) | Use `arc4random()` or a seeded PRNG struct |

## Testing Toolchain

| Python | C | Notes |
|---|---|---|
| `pytest` | `cmocka` or `Unity` | |
| `pytest.raises` | Check return code in test | |
| `unittest.mock` | PROHIBITED | Real implementations only |
| `mypy` | `-Wall -Wextra -Wpedantic` | |
| `black` | `clang-format` | `.clang-format` config file |
| Valgrind | memory error detector | Required: run all tests under `valgrind --leak-check=full` |

## Build System

```makefile
# Adapt from Python's build system to:
CC = gcc
CFLAGS = -std=c11 -Wall -Wextra -Wpedantic -O2
LDFLAGS = -lm

all: $(TARGET)
test: $(TEST_TARGET)
    valgrind --leak-check=full ./$(TEST_TARGET)
```

## CI Adaptation

```yaml
# Python:
- run: pytest

# C:
- run: make test
- run: valgrind --leak-check=full --error-exitcode=1 ./test_runner
```
