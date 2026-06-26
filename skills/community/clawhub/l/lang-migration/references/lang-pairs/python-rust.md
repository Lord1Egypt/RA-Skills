# Language Pair: Python → Rust

**Difficulty tier**: High (paradigm leap — GC+dynamic vs ownership+static)

**Key differences**:
- Memory model: Python uses GC + reference counting / Rust uses ownership + borrow checker
- Type system: Python is dynamically typed / Rust is statically typed with generics + traits
- Error handling: Python raises exceptions / Rust uses `Result<T, E>` and `Option<T>`
- Concurrency: Python has GIL / Rust has fearless concurrency with Send+Sync
- Nullability: Python uses `None` / Rust uses `Option<T>`

---

## Pre-Mapped Core Types

| Python Type | Rust Type | Equivalence | Notes |
|---|---|---|---|
| `int` (small) | `i64` | behavioral | Python int is unbounded; audit for values > i64::MAX |
| `int` (big) | `num_bigint::BigInt` | structural | `num-bigint` crate |
| `float` | `f64` | structural | Both IEEE 754 double |
| `bool` | `bool` | structural | |
| `str` | `String` / `&str` | structural | Rust distinguishes owned vs borrowed |
| `bytes` | `Vec<u8>` / `&[u8]` | structural | |
| `None` | `Option<T>::None` | structural | |
| `list[T]` | `Vec<T>` | structural | |
| `tuple[A, B]` | `(A, B)` | structural | |
| `dict[K, V]` | `HashMap<K, V>` | behavioral | HashMap order is random; use `IndexMap` if order matters |
| `set[T]` | `HashSet<T>` | structural | |
| `collections.OrderedDict` | `IndexMap<K, V>` | structural | `indexmap` crate |
| `collections.deque` | `VecDeque<T>` | structural | |
| `collections.Counter` | `HashMap<T, usize>` | structural | |
| `typing.Optional[T]` | `Option<T>` | structural | |
| `typing.Union[A, B]` | `enum` with variants | structural | |

## Numeric Precision — Critical

| Python | Rust | Delta | Action |
|---|---|---|---|
| `int` division `//` | integer `/` | none | Both truncate toward zero |
| `int` division `/` | `as f64` then `/` | none | Python `/` on ints returns float |
| `float` | `f64` | none | Identical IEEE 754 |
| `float('inf')` | `f64::INFINITY` | none | |
| `float('nan')` | `f64::NAN` | none | |
| Integer overflow | `i64` panics in debug, wraps in release | CRITICAL | Use `checked_add`, `saturating_add`, or `wrapping_add` explicitly |

---

## Standard Library Mapping

| Python | Rust | Package | Equivalence | Notes |
|---|---|---|---|---|
| `os.path.join` | `std::path::Path::join` | std | structural | |
| `os.listdir` | `std::fs::read_dir` | std | structural | Returns iterator |
| `os.environ.get` | `std::env::var` | std | structural | Returns `Result` not `Option` |
| `open(f, 'rb')` | `std::fs::File::open` | std | structural | |
| `json.dumps` | `serde_json::to_string` | serde_json | structural | |
| `json.loads` | `serde_json::from_str` | serde_json | structural | |
| `re.compile` | `regex::Regex::new` | regex | structural | |
| `hashlib.sha256` | `sha2::Sha256` | sha2 | structural | |
| `time.time()` | `std::time::SystemTime::now()` | std | structural | |
| `random.random()` | `rand::random::<f64>()` | rand | behavioral | Different RNG algorithm |
| `random.seed(n)` | `StdRng::seed_from_u64(n)` | rand | behavioral | Different RNG algorithm; output sequence differs |
| `threading.Thread` | `std::thread::spawn` | std | structural | No GIL; true parallelism |
| `asyncio` | `tokio` | tokio | structural | Different runtime; async/await syntax identical |
| `subprocess.run` | `std::process::Command` | std | structural | |
| `sys.argv` | `std::env::args()` | std | structural | |
| `logging` | `tracing` or `log` + `env_logger` | tracing | structural | |
| `argparse` | `clap` | clap | structural | |

---

## Common Third-Party Library Mapping

| Python Package | Rust Crate | Equivalence | Notes |
|---|---|---|---|
| `numpy` | `ndarray` | behavioral | Broadcasting semantics differ; see numpy section below |
| `pandas` | `polars` | behavioral | API differs significantly; structural only at algorithm level |
| `scipy` | (various) | partial | No single equivalent; map function by function |
| `requests` | `reqwest` | structural | Async version: `reqwest::Client` |
| `sqlalchemy` | `sqlx` or `diesel` | structural | |
| `pydantic` | `serde` + struct | structural | |
| `click` | `clap` | structural | |
| `pytest` | `cargo test` | structural | Built-in; no crate needed |
| `PIL/Pillow` | `image` | structural | |
| `matplotlib` | `plotters` | behavioral | API differs |
| `cryptography` | `ring` or `rustls` | structural | |
| `yaml` | `serde_yaml` | structural | |

### NumPy → ndarray Specifics (HIGH RISK)

NumPy has many implicit behaviors that must be explicitly handled:

| NumPy operation | ndarray equivalent | Gap |
|---|---|---|
| `arr[arr > 0]` boolean indexing | `.iter().filter()` + collect | API differs; same semantics |
| `np.sum(arr, axis=0)` | `.sum_axis(Axis(0))` | structural |
| Broadcasting `(3,) + (3,1)` | requires explicit `.broadcast()` | behavioral; always explicit in ndarray |
| `arr.reshape(3, -1)` | `.into_shape((3, n))` | must compute n explicitly |
| `np.linalg.inv` | `ndarray-linalg` crate | structural |
| `np.random.default_rng(seed)` | `SmallRng::seed_from_u64(seed)` | behavioral; different algorithm |
| `arr.dtype` (float32 vs float64) | Compile-time generic `Array<f32, _>` | structural; dtype is type parameter |

---

## Translation Patterns

### Pattern 1: Exception handling → Result

**Python:**
```python
def parse_config(path: str) -> dict:
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError:
        raise ConfigError(f"Config not found: {path}")
    except json.JSONDecodeError as e:
        raise ConfigError(f"Invalid JSON: {e}")
```

**Rust:**
```rust
fn parse_config(path: &str) -> Result<serde_json::Value, ConfigError> {
    let content = std::fs::read_to_string(path)
        .map_err(|_| ConfigError::NotFound(path.to_string()))?;
    serde_json::from_str(&content)
        .map_err(|e| ConfigError::InvalidJson(e.to_string()))
}
```

**Structural note**: Each `except` clause maps to one `map_err` call. Maintain 1:1 correspondence.

---

### Pattern 2: List comprehension → iterator chain

**Python:**
```python
filtered = [x * 2 for x in values if x > threshold]
```

**Rust:**
```rust
let filtered: Vec<f64> = values.iter()
    .filter(|&&x| x > threshold)   // step 1: filter (mirrors the `if`)
    .map(|&x| x * 2.0)             // step 2: transform (mirrors the expression)
    .collect();                      // step 3: materialize
```

**Structural note**: The filter before the map mirrors the Python `if` before the expression. Never swap order.

---

### Pattern 3: Class with state → struct + impl

**Python:**
```python
class RingBuffer:
    def __init__(self, capacity: int):
        self.data = [None] * capacity
        self.head = 0
        self.size = 0
    
    def push(self, item):
        self.data[self.head] = item
        self.head = (self.head + 1) % len(self.data)
        self.size = min(self.size + 1, len(self.data))
```

**Rust:**
```rust
struct RingBuffer<T> {
    data: Vec<Option<T>>,
    head: usize,
    size: usize,
}

impl<T> RingBuffer<T> {
    fn new(capacity: usize) -> Self {
        Self {
            data: (0..capacity).map(|_| None).collect(),
            head: 0,
            size: 0,
        }
    }
    
    fn push(&mut self, item: T) {
        self.data[self.head] = Some(item);
        self.head = (self.head + 1) % self.data.len();
        self.size = (self.size + 1).min(self.data.len());
    }
}
```

---

### Pattern 4: Generator → Iterator trait

**Python:**
```python
def sliding_window(data: list, size: int):
    for i in range(len(data) - size + 1):
        yield data[i:i + size]
```

**Rust:**
```rust
struct SlidingWindow<'a, T> {
    data: &'a [T],
    size: usize,
    pos: usize,
}

impl<'a, T> Iterator for SlidingWindow<'a, T> {
    type Item = &'a [T];
    fn next(&mut self) -> Option<Self::Item> {
        if self.pos + self.size > self.data.len() { return None; }
        let window = &self.data[self.pos..self.pos + self.size];
        self.pos += 1;
        Some(window)
    }
}
```

**Or** use `windows()` if the pattern matches exactly: `data.windows(size)` — structural, stdlib.

---

## Anti-Patterns

| Wrong | Why wrong | Correct |
|---|---|---|
| `Box<dyn Any>` for every collection | Abandons type safety; not structural | Use generics or enums |
| `unwrap()` everywhere | Hides error handling structure | Match the Python exception pattern with `?` or `match` |
| `unsafe` for dict-like mutation | Not required; use `HashMap` properly | Use entry API |
| `Arc<Mutex<T>>` when Python had no locks | Adds concurrency structure not in source | Use `Mutex` only if source used locks; otherwise single-threaded |
| `clone()` proliferation | Hides ownership model mismatch | Restructure lifetime annotations instead |

---

## Ecosystem Gaps

| Python feature | Gap | Compensation |
|---|---|---|
| `int` is unbounded | `i64` overflows | Audit all arithmetic; use `num-bigint` where source values exceed i64::MAX |
| `dict` preserves insertion order (Python 3.7+) | `HashMap` does not | Use `indexmap::IndexMap` |
| `float` division always returns float | Rust integer `/` truncates | Track type of operands; cast when needed |
| `**kwargs` / dynamic dispatch | Rust has no runtime dynamic dispatch for free | Use trait objects `Box<dyn Trait>` or enum dispatch |
| Decorator pattern | No direct equivalent | Implement with wrapper structs or macros |
| `__getattr__` / dynamic attribute | Not possible in safe Rust | Redesign as explicit method; document in translation_notes |
| `isinstance()` at runtime | Rust uses compile-time types | Use `enum` with pattern matching instead |
| Negative list indices `arr[-1]` | Rust panics on out-of-bounds | Use `arr.last()` / `arr[arr.len()-1]` |
| `None` in typed collections | Rust requires `Vec<Option<T>>` | Always explicit |

---

## Testing Toolchain

| Python | Rust | Notes |
|---|---|---|
| `pytest` | `cargo test` | Built-in; `#[test]` attribute |
| `pytest.raises` | `#[should_panic]` or `Result` testing | |
| `unittest.mock` | NO EQUIVALENT — mocks prohibited | Use real implementations |
| `mypy` | `cargo check` | Type checking built into compiler |
| `ruff` / `flake8` | `cargo clippy` | |
| `black` | `rustfmt` | |
| `pytest-benchmark` | `criterion` crate | |

---

## Build System

| Python | Rust | Notes |
|---|---|---|
| `pyproject.toml` / `setup.py` | `Cargo.toml` | |
| `requirements.txt` | `Cargo.lock` (generated) | Do not manually write; generated by cargo |
| `pip install` | `cargo add` | |
| `python -m module` | `cargo run --bin name` | |
| `python setup.py build_ext` | `build.rs` | |

## CI Adaptation

```yaml
# Python (source):
- run: pip install -r requirements.txt && pytest

# Rust (target):
- run: cargo test
- run: cargo clippy -- -D warnings
- run: cargo fmt --check
```
