# Language Pair: Bun (JavaScript) → Python

**Difficulty tier**: Low-Moderate (both dynamic; async models differ; number precision is a trap)

**Key differences**:
- Types: JS dynamic → Python `typing` annotations (ADD types; JS may have none)
- Async: JS Promise/async-await → Python `asyncio` (structurally similar)
- Numbers: JS `number` (float64) → Python `int` / `float` (must determine which)
- `undefined` vs `null`: JS has both → Python has only `None`
- Prototypal OOP: JS classes → Python classes (both ES6 class and Python class are similar)
- Modules: JS ESM → Python modules

---

## Pre-Mapped Core Types

| Bun (JS) | Python | Equivalence | Notes |
|---|---|---|---|
| `number` (integer use) | `int` | behavioral | JS uses float64 for all numbers; Python distinguishes |
| `number` (float use) | `float` | structural | |
| `bigint` | `int` | structural | Python int is natively arbitrary precision |
| `boolean` | `bool` | structural | |
| `string` | `str` | structural | JS is UTF-16 internally; Python str is abstract Unicode |
| `null` | `None` | structural | |
| `undefined` | `None` | behavioral | JS `undefined` (unset) → Python `None`; document |
| `Array<T>` | `list[T]` | structural | |
| `[A, B]` tuple | `tuple[A, B]` | structural | |
| `Map<K,V>` | `dict[K,V]` | structural | Both preserve insertion order |
| `Set<T>` | `set[T]` | structural | |
| `Uint8Array` | `bytes` | structural | |
| `ArrayBuffer` | `bytes` | structural | |
| `Promise<T>` | `Awaitable[T]` / coroutine | structural | |
| `null \| T` | `Optional[T]` | structural | |
| `A \| B` | `Union[A, B]` | structural | |

---

## Number Type Disambiguation

JS uses `number` for both integers and floats. When migrating, determine the correct Python type from context:

```javascript
// JS: all are `number`
const count = 42;           // → Python int
const ratio = 3.14;         // → Python float
const index = arr.length;   // → Python int
const price = 9.99;         // → Python float
```

**Decision rule** (apply per variable/parameter):
- Used with integer arithmetic, indices, or counts → `int`
- Used with decimal values, ratios, measurements → `float`
- Unclear → `float` (safer; Python float is wider than JS number)
- Was `bigint` in JS → always `int`

---

## `undefined` vs `null` → `None`

```javascript
// JS: different semantics
function find(key) {
    if (!map.has(key)) return undefined;  // not found
    const val = map.get(key);
    if (val === null) return null;         // explicitly absent
    return val;
}
```

```python
# Python: both → None; document the distinction as comment
def find(key: str) -> Optional[str]:
    # JS SOURCE: returned undefined when not found, null when explicitly absent.
    # Python: both map to None. Callers must not distinguish.
    if key not in self._map:
        return None   # was: undefined (not found)
    return self._map[key]   # may be None (was: null — explicitly absent)
```

If the caller distinguished `undefined` from `null`, use a sentinel or `Optional[Optional[T]]` pattern and document thoroughly.

---

## async/await → asyncio

**JS:**
```javascript
async function fetchData(url) {
    const response = await fetch(url);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return await response.json();
}
```

**Python:**
```python
import aiohttp

async def fetch_data(url: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if not response.ok:
                raise RuntimeError(f"HTTP {response.status}")
            return await response.json()
```

| JS | Python | Notes |
|---|---|---|
| `async function` | `async def` | |
| `await expr` | `await expr` | |
| `Promise.all([...])` | `asyncio.gather(...)` | |
| `Promise.race([...])` | `asyncio.wait(..., return_when=FIRST_COMPLETED)` | |
| `Promise.allSettled([...])` | `asyncio.gather(..., return_exceptions=True)` | |
| `new Promise((res, rej) => ...)` | `asyncio.get_event_loop().create_future()` | Rare; prefer async def |
| `.then(fn)` chaining | `await` in sequence | Flatten chains to sequential awaits |

---

## Error Handling

JS and Python exceptions are structurally similar:

**JS:**
```javascript
class DatabaseError extends Error {
    constructor(message, code) {
        super(message);
        this.name = 'DatabaseError';
        this.code = code;
    }
}

function query(sql) {
    try {
        return db.execute(sql);
    } catch (e) {
        if (e instanceof ConnectionError) {
            throw new DatabaseError(`connection failed: ${e.message}`, 'CONN_ERROR');
        }
        throw e;
    }
}
```

**Python:**
```python
class DatabaseError(Exception):
    def __init__(self, message: str, code: str) -> None:
        super().__init__(message)
        self.code = code

def query(sql: str) -> Any:
    try:
        return db.execute(sql)
    except ConnectionError as e:
        raise DatabaseError(f"connection failed: {e}", 'CONN_ERROR') from e
```

**Rule**: Use `raise X from e` (Python) to preserve the exception chain — mirrors JS's implicit cause.

---

## Class Migration

ES6 classes and Python classes are nearly identical:

**JS:**
```javascript
class EventEmitter {
    #listeners = new Map();

    on(event, handler) {
        if (!this.#listeners.has(event)) {
            this.#listeners.set(event, []);
        }
        this.#listeners.get(event).push(handler);
    }

    emit(event, ...args) {
        (this.#listeners.get(event) ?? []).forEach(h => h(...args));
    }
}
```

**Python:**
```python
from typing import Callable, Any

class EventEmitter:
    def __init__(self) -> None:
        self._listeners: dict[str, list[Callable[..., Any]]] = {}

    def on(self, event: str, handler: Callable[..., Any]) -> None:
        if event not in self._listeners:
            self._listeners[event] = []
        self._listeners[event].append(handler)

    def emit(self, event: str, *args: Any) -> None:
        for handler in self._listeners.get(event, []):
            handler(*args)
```

| JS | Python |
|---|---|
| `#privateField` | `self._private_field` (convention) |
| `static method()` | `@staticmethod` or `@classmethod` |
| `get prop()` | `@property` |
| `set prop(v)` | `@prop.setter` |
| `constructor` | `__init__` |
| `toString()` | `__str__` |
| `[Symbol.iterator]()` | `__iter__` |
| `[Symbol.asyncIterator]()` | `__aiter__` |

---

## Bun-Specific APIs → Python Equivalents

| Bun API | Python equivalent | Notes |
|---|---|---|
| `Bun.file(path).text()` | `open(path).read()` | |
| `Bun.file(path).arrayBuffer()` | `open(path, 'rb').read()` | |
| `Bun.write(path, data)` | `open(path, 'w').write(data)` | |
| `Bun.spawn(cmd)` | `subprocess.run(cmd)` | |
| `Bun.serve({...})` | `aiohttp.web.Application()` or FastAPI | |
| `Bun.env.KEY` | `os.environ.get('KEY')` | |
| `Bun.CryptoHasher('sha256')` | `hashlib.sha256()` | |
| `Bun.sleep(ms)` | `await asyncio.sleep(ms / 1000)` | |

---

## Spread / Rest → `*args` / Unpacking

```javascript
function sum(...numbers) { return numbers.reduce((a, b) => a + b, 0); }
const merged = { ...obj1, ...obj2 };
const combined = [...arr1, ...arr2];
```

```python
def sum(*numbers: float) -> float:
    return sum(numbers)

merged = {**obj1, **obj2}
combined = [*arr1, *arr2]
```

---

## Ecosystem Gaps

| JS/Bun | Gap | Python |
|---|---|---|
| `undefined` | Python has no undefined | Map to `None`; document |
| `NaN` | `float('nan')` | `math.isnan(x)` |
| Prototype chain | No equivalent | Python uses class MRO |
| `Symbol` | No equivalent | Use `enum` or sentinel objects |
| Generator functions `function*` | `def gen(): yield` | Very similar |
| `WeakMap` / `WeakRef` | `weakref.WeakValueDictionary` | |
| `Proxy` / `Reflect` | `__getattr__`, `__setattr__` | |
| `structuredClone` | `copy.deepcopy` | |
| `JSON.stringify` circular ref detection | `json.dumps` raises; use `jsonpickle` | |

---

## Testing Toolchain

| Bun/JS | Python | Notes |
|---|---|---|
| `bun test` | `pytest` | |
| `test("name", () => {})` | `def test_name(): ...` | |
| `expect(val).toBe(x)` | `assert val == x` | |
| `expect(fn).toThrow(Err)` | `pytest.raises(ErrClass)` | |
| `mock()` / `jest.fn()` | PROHIBITED | Real implementations only |
| TypeScript type check | `mypy .` | |
| `prettier` | `black .` | |
| `eslint` | `ruff check .` | |

## Build / CI

```yaml
# Bun (source):
- run: bun install && bun test

# Python (target):
- run: pip install -r requirements.txt
- run: pytest
- run: mypy .
- run: ruff check .
- run: black --check .
```
