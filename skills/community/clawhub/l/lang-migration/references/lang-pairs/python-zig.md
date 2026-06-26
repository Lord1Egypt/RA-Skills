# Language Pair: Python → Zig

**Difficulty tier**: High (explicit allocators, no hidden control flow, comptime)

**Key differences**:
- Memory model: Python GC / Zig explicit allocators (every allocation uses an `Allocator`)
- Type system: Python dynamic / Zig static + comptime (compile-time generics)
- Error handling: Python exceptions / Zig `error` unions + `try`/`catch`
- OOP: Python classes / Zig structs with methods (no inheritance)
- No hidden allocations: Zig functions cannot allocate without an explicit allocator parameter
- No undefined behavior: Integer overflow is a compile-time configurable error (use `@addWithOverflow` or `std.math.add`)

---

## Pre-Mapped Core Types

| Python | Zig | Equivalence | Notes |
|---|---|---|---|
| `int` | `i64` | behavioral | Zig integers are fixed-width; use `i128` or `std.math.big.int` for big nums |
| `float` | `f64` | structural | |
| `bool` | `bool` | structural | |
| `str` | `[]const u8` | structural | Zig strings are byte slices; UTF-8 by convention |
| `bytes` | `[]u8` | structural | |
| `None` | `null` (optional type) | structural | |
| `list[T]` | `std.ArrayList(T)` | structural | Requires allocator |
| `dict[K,V]` | `std.AutoHashMap(K,V)` | behavioral | No order guarantee |
| `Optional[T]` | `?T` | structural | Zig optional is a language primitive |
| `Union[A,B]` | `union(enum)` | structural | Tagged union |

## Allocator Protocol (Critical)

Every function that allocates MUST accept an `std.mem.Allocator` parameter.
This directly maps to Python's implicit heap allocation.

**Python:**
```python
def build_list(n: int) -> list[int]:
    return [i * 2 for i in range(n)]
```

**Zig:**
```zig
fn buildList(allocator: std.mem.Allocator, n: usize) ![]i64 {
    var list = try std.ArrayList(i64).initCapacity(allocator, n);
    errdefer list.deinit();  // cleanup if subsequent steps fail
    for (0..n) |i| {
        try list.append(@intCast(i * 2));
    }
    return try list.toOwnedSlice();
}
```

**Rule**: Every Python function that creates a collection or string gets an `allocator` parameter in Zig. Document this in the IPO registry under `inputs`.

## Error Handling Pattern

**Python:**
```python
def read_file(path: str) -> str:
    try:
        with open(path) as f:
            return f.read()
    except FileNotFoundError:
        raise IOError(f"not found: {path}")
```

**Zig:**
```zig
const ReadError = error{ NotFound, ReadFailed };

fn readFile(allocator: std.mem.Allocator, path: []const u8) ReadError![]u8 {
    const file = std.fs.cwd().openFile(path, .{}) catch return ReadError.NotFound;
    defer file.close();
    return file.readToEndAlloc(allocator, std.math.maxInt(usize))
        catch return ReadError.ReadFailed;
}
```

**Rule**: Each Python exception type → one Zig error value in an `error` set. `try` propagates errors; `catch` handles them. This mirrors Python's `raise` and `except` structure precisely.

## Class → Struct with Methods

**Python:**
```python
class RingBuffer:
    def __init__(self, allocator, capacity: int):
        self.data = [0] * capacity
        self.head = 0
        self.size = 0
    def push(self, item: int):
        self.data[self.head] = item
        self.head = (self.head + 1) % len(self.data)
        self.size = min(self.size + 1, len(self.data))
    def deinit(self):
        pass  # GC handles it
```

**Zig:**
```zig
pub const RingBuffer = struct {
    data: []i64,
    head: usize,
    size: usize,
    allocator: std.mem.Allocator,

    pub fn init(allocator: std.mem.Allocator, capacity: usize) !RingBuffer {
        const data = try allocator.alloc(i64, capacity);
        @memset(data, 0);
        return .{ .data = data, .head = 0, .size = 0, .allocator = allocator };
    }

    pub fn deinit(self: *RingBuffer) void {
        self.allocator.free(self.data);
    }

    pub fn push(self: *RingBuffer, item: i64) void {
        self.data[self.head] = item;
        self.head = (self.head + 1) % self.data.len;
        self.size = @min(self.size + 1, self.data.len);
    }
};
```

**Rule**: Every Python class constructor → `init`. Every `__del__` or resource cleanup → `deinit`. Always call `defer obj.deinit()` at the allocation site.

## Integer Overflow (Critical — Zig is strict)

Python integers never overflow. Zig integers overflow by default in debug mode (panic).

For every arithmetic operation in the IPO registry, check whether overflow is possible:

```zig
// If source algorithm assumes no overflow (e.g., indices):
const next = head + 1;  // safe: index into bounded array

// If source algorithm works on arbitrary integers:
const result = std.math.add(i64, a, b) catch return error.Overflow;

// If source algorithm intentionally wraps (e.g., checksums):
const hash = a +% b;  // wrapping add
```

Always document which strategy is used in `translation_notes`.

## Comptime Generics

Python generics (typing module) → Zig comptime types:

**Python:**
```python
def max_val(items: list[T]) -> T:
    return max(items)
```

**Zig:**
```zig
fn maxVal(comptime T: type, items: []const T) T {
    var result = items[0];
    for (items[1..]) |item| {
        if (item > result) result = item;
    }
    return result;
}
```

## Ecosystem Gaps

| Python | Gap | Compensation |
|---|---|---|
| `dict` ordering | `AutoHashMap` has no order | Use `std.ArrayHashMap` for insertion order |
| `random.seed` + reproducible | `std.rand` has no seed API equivalent to Python | Use `std.rand.DefaultPrng.init(seed)` |
| `str.split`, `str.join` | No stdlib equivalents | Use `std.mem.split`, manual join loop |
| `logging` | No stdlib equivalent | Use `std.log` (basic) or third-party |
| `json` (complex) | `std.json` is limited | Use `std.json` for simple cases; document limitations |

## Anti-Patterns

| Wrong | Why | Correct |
|---|---|---|
| Ignoring `errdefer` | Memory leak on error path | Always `errdefer deinit()` after every allocation |
| `unreachable` in logic paths | Hides missing translation | Translate the actual logic |
| `@panic` for Python exceptions | Not equivalent | Use `error` union |
| Not passing allocator to sub-functions | Hides allocation | Pass allocator explicitly at every level |

## Testing Toolchain

| Python | Zig | Notes |
|---|---|---|
| `pytest` | `zig test` | Built-in; `test "name" { ... }` blocks |
| `pytest.raises` | `try { ... } catch ...` or `std.testing.expectError` | |
| `unittest.mock` | PROHIBITED | Real implementations only |
| `mypy` | Zig compiler (type-safe by construction) | |
| `black` | `zig fmt` | |

## Build / CI

```yaml
# Python:
- run: pytest

# Zig:
- run: zig build test
- run: zig build -Doptimize=ReleaseSafe  # verify no safety violations
```

```zig
// build.zig test step:
const test_step = b.step("test", "Run unit tests");
const unit_tests = b.addTest(.{ .root_source_file = .{ .path = "src/main.zig" } });
test_step.dependOn(&b.addRunArtifact(unit_tests).step);
```
