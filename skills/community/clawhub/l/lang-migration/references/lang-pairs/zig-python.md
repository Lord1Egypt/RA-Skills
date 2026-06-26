# Language Pair: Zig → Python

**Difficulty tier**: Moderate (explicit allocators dissolve; comptime becomes runtime; error unions become exceptions)

**Key differences**:
- Memory: Zig explicit allocators → Python GC (allocator parameters disappear; `deinit` calls disappear)
- Errors: Zig `error` unions + `try` → Python exceptions (structurally similar)
- Comptime: Zig `comptime` generics → Python `TypeVar` / `Generic` or runtime checks
- Optional: Zig `?T` → Python `Optional[T]`
- Slices: Zig `[]T` (pointer + length) → Python `list[T]` or `bytes`
- Tagged unions: Zig `union(enum)` → Python `Union` + type dispatch or `@dataclass` with variant field
- Integers: Zig `i32`, `u64`, etc. → Python `int` (unbounded; document original width)
- `comptime` constants → Python module-level constants

---

## Pre-Mapped Core Types

| Zig | Python | Equivalence | Notes |
|---|---|---|---|
| `i8/i16/i32/i64` | `int` | behavioral | Document original width as comment |
| `u8/u16/u32/u64` | `int` | behavioral | Add non-negative invariant |
| `i128/u128` | `int` | structural | Python int covers |
| `usize` | `int` | behavioral | Platform-dependent in Zig; use `int` |
| `f32` | `float` | behavioral | Precision widening; document |
| `f64` | `float` | structural | |
| `bool` | `bool` | structural | |
| `[]const u8` (string) | `str` | structural | Zig strings are UTF-8 byte slices |
| `[]u8` (mutable bytes) | `bytearray` | structural | |
| `[]T` (slice) | `list[T]` | structural | The (ptr, len) pair → list |
| `?T` (optional) | `Optional[T]` | structural | |
| `anyerror` | `Exception` | structural | |
| `error{A, B}!T` | function returning T or raising | structural | See error section |
| `void` | `None` | structural | |
| `*T` (pointer) | T directly | behavioral | GC handles memory; document original pointer semantics |
| `std.ArrayList(T)` | `list[T]` | structural | |
| `std.AutoHashMap(K,V)` | `dict[K,V]` | behavioral | No order guarantee |
| `std.ArrayHashMap(K,V)` | `dict[K,V]` | structural | Insertion order preserved |
| `comptime T: type` | `TypeVar('T')` or type annotation | structural | |

---

## Allocator Parameters → Disappear

The most visible Zig pattern: every function that allocates takes an `Allocator` parameter.
In Python, remove the allocator parameter entirely — the GC handles allocation.

**Zig:**
```zig
fn buildList(allocator: std.mem.Allocator, n: usize) ![]i64 {
    var list = try std.ArrayList(i64).initCapacity(allocator, n);
    errdefer list.deinit();
    for (0..n) |i| try list.append(@intCast(i * 2));
    return try list.toOwnedSlice();
}
```

**Python:**
```python
def build_list(n: int) -> list[int]:
    # ZIG SOURCE: fn buildList(allocator: Allocator, n: usize) ![]i64
    # Allocator parameter removed — GC handles memory.
    # errdefer / deinit removed — GC handles cleanup.
    return [i * 2 for i in range(n)]
```

**Rule**: Remove ALL allocator parameters. Remove ALL `deinit()` calls. Remove ALL `errdefer` cleanup for memory. If `errdefer` cleaned up non-memory resources (file handles, network), translate to `try/finally` or context manager.

---

## Error Unions → Exceptions

Zig error unions (`!T`) map structurally to Python exceptions:

**Zig:**
```zig
const FileError = error{ NotFound, PermissionDenied, ReadFailed };

fn readFile(allocator: std.mem.Allocator, path: []const u8) FileError![]u8 {
    const file = std.fs.cwd().openFile(path, .{}) catch return FileError.NotFound;
    defer file.close();
    return file.readToEndAlloc(allocator, std.math.maxInt(usize))
        catch return FileError.ReadFailed;
}
```

**Python:**
```python
class FileError(Exception): pass
class NotFoundError(FileError): pass
class PermissionDeniedError(FileError): pass
class ReadFailedError(FileError): pass

def read_file(path: str) -> bytes:
    # ZIG SOURCE: fn readFile(allocator, path) FileError![]u8
    try:
        with open(path, 'rb') as f:
            return f.read()
    except FileNotFoundError:
        raise NotFoundError(path)
    except PermissionError:
        raise PermissionDeniedError(path)
    except OSError:
        raise ReadFailedError(path)
```

**Rules**:
- Each `error.Variant` → one Python exception class
- `try expr` (Zig) → function call that may raise
- `expr catch return error.X` → `try/except` block raising `XError`
- `errdefer` for non-memory cleanup → `try/finally`
- `anyerror` → base `Exception`

---

## Comptime Generics → TypeVar / Generic

**Zig:**
```zig
fn Stack(comptime T: type) type {
    return struct {
        data: std.ArrayList(T),
        
        pub fn init(allocator: std.mem.Allocator) @This() {
            return .{ .data = std.ArrayList(T).init(allocator) };
        }
        pub fn push(self: *@This(), val: T) !void {
            try self.data.append(val);
        }
        pub fn pop(self: *@This()) ?T {
            if (self.data.items.len == 0) return null;
            return self.data.pop();
        }
    };
}
```

**Python:**
```python
from typing import Generic, TypeVar
T = TypeVar('T')

class Stack(Generic[T]):
    # ZIG SOURCE: fn Stack(comptime T: type) type — comptime generic
    def __init__(self) -> None:
        self._data: list[T] = []

    def push(self, val: T) -> None:
        self._data.append(val)

    def pop(self) -> Optional[T]:
        if not self._data:
            return None
        return self._data.pop()
```

---

## Tagged Union → Union Type + Dispatch

**Zig:**
```zig
const Shape = union(enum) {
    circle: f64,          // radius
    rectangle: struct { w: f64, h: f64 },
    triangle: struct { base: f64, height: f64 },
};

fn area(shape: Shape) f64 {
    return switch (shape) {
        .circle => |r| std.math.pi * r * r,
        .rectangle => |rect| rect.w * rect.h,
        .triangle => |tri| 0.5 * tri.base * tri.height,
    };
}
```

**Python:**
```python
import math
from dataclasses import dataclass
from typing import Union

@dataclass
class Circle:
    radius: float

@dataclass
class Rectangle:
    w: float
    h: float

@dataclass
class Triangle:
    base: float
    height: float

Shape = Union[Circle, Rectangle, Triangle]

def area(shape: Shape) -> float:
    # ZIG SOURCE: switch(shape) on union(enum)
    if isinstance(shape, Circle):
        return math.pi * shape.radius ** 2
    elif isinstance(shape, Rectangle):
        return shape.w * shape.h
    elif isinstance(shape, Triangle):
        return 0.5 * shape.base * shape.height
    else:
        raise ValueError(f"unknown shape: {type(shape)}")
```

---

## Integer Overflow Strategy → Assertions

Zig enforces integer overflow at runtime (debug mode panics).
Python int never overflows. Preserve the original intent as assertions:

```zig
// Zig: wrapping add (explicit)
const result = a +% b;

// Zig: checked add (returns optional)
const result = std.math.add(i32, a, b) catch return error.Overflow;
```

```python
# Python equivalent of wrapping add (i32):
result = (a + b) & 0xFFFFFFFF
if result >= 0x80000000:
    result -= 0x100000000  # sign extend
# ZIG SOURCE: +% wrapping add on i32

# Python equivalent of checked add:
result = a + b
if not (-2**31 <= result <= 2**31 - 1):
    raise OverflowError(f"i32 overflow: {a} + {b} = {result}")
# ZIG SOURCE: std.math.add(i32, a, b) — panics on overflow
```

---

## `defer` → `try/finally` / Context Manager

**Zig:**
```zig
const file = try std.fs.cwd().openFile(path, .{});
defer file.close();
const data = try file.readToEndAlloc(allocator, max_size);
defer allocator.free(data);
```

**Python:**
```python
with open(path, 'rb') as file:
    data = file.read()
    # allocator.free(data) → GC handles; no action needed
```

For non-resource `defer` (e.g., resetting a flag):
```zig
self.lock = true;
defer self.lock = false;
```
```python
self.lock = True
try:
    ...
finally:
    self.lock = False
```

---

## `@This()` → `Self`

```zig
pub fn clone(self: *@This()) @This() { ... }
```

```python
from typing import Self  # Python 3.11+

def clone(self) -> Self: ...
# Or for older Python:
def clone(self) -> 'MyClass': ...
```

---

## Comptime Constants → Module Constants

```zig
const MAX_BUFFER_SIZE: usize = 4096;
const DEFAULT_TIMEOUT_MS: u32 = 5000;
const SUPPORTED_VERSIONS = [_]u8{ 1, 2, 3 };
```

```python
from typing import Final

MAX_BUFFER_SIZE: Final[int] = 4096
DEFAULT_TIMEOUT_MS: Final[int] = 5000
SUPPORTED_VERSIONS: Final[tuple[int, ...]] = (1, 2, 3)
```

---

## Ecosystem Gaps

| Zig | Gap | Python |
|---|---|---|
| Explicit allocator control | No equivalent | Document; GC handles |
| Integer width enforcement | Python int unbounded | Add range comments and assertions |
| `comptime` code execution | Module-level Python executes at import | Module-level constants and `__init_subclass__` |
| `@import("builtin")` | `platform` / `sys` module | |
| `std.testing.expectError` | `pytest.raises(ExcType)` | |
| Sentinel-terminated slices `[:0]u8` | No equivalent; use `bytes` | |
| `packed struct` / bit fields | `struct` module for serialization | |
| `extern struct` / C ABI | `ctypes` | |
| `build.zig` | `pyproject.toml` + `makefile` | |

---

## Testing Toolchain

| Zig | Python | Notes |
|---|---|---|
| `zig test` / `test "name" {}` | `pytest` | |
| `std.testing.expect(cond)` | `assert cond` | |
| `std.testing.expectEqual(a, b)` | `assert a == b` | |
| `std.testing.expectError(err, expr)` | `pytest.raises(ErrClass)` | |
| `zig fmt` | `black .` | |
| Zig compiler (type-safe) | `mypy .` | |

## Build / CI

```yaml
# Zig (source):
- run: zig build test

# Python (target):
- run: pip install -r requirements.txt
- run: pytest
- run: mypy .
- run: black --check .
- run: ruff check .
```
