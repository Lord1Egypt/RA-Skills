# Language Pair: Python → Bun (JavaScript with Bun Runtime)

**Difficulty tier**: Moderate

**Note on target**: "Bun" is a JavaScript/TypeScript runtime, not a language.
This module covers migration to **JavaScript** running on **Bun** (not Node.js).
If the target is TypeScript on Bun, use `python-typescript.md` instead.
Bun-specific APIs replace Node.js equivalents (file I/O, HTTP, subprocess).

**Key differences**:
- Memory model: Python GC / JS GC (similar; both automatic)
- Type system: Python dynamic / JavaScript dynamic (no compile-time checks)
- Error handling: Python exceptions / JS exceptions (throw/catch — very similar)
- Async: Python asyncio / JS Promise + async/await (similar model)
- Numbers: Python int is unbounded / JS uses float64 for all numbers (critical gap)
- Modules: Python imports / JS ESM + CommonJS

---

## Pre-Mapped Core Types

| Python | Bun (JS) | Equivalence | Notes |
|---|---|---|---|
| `int` (< 2^53) | `number` | structural | JS float64 can represent integers exactly up to 2^53 |
| `int` (>= 2^53) | `BigInt` | structural | Use `BigInt(n)` or `n` suffix |
| `float` | `number` | behavioral | Both IEEE 754 double; no separate int type |
| `bool` | `boolean` | structural | |
| `str` | `string` | structural | JS strings are UTF-16 internally; careful with emoji/surrogate pairs |
| `bytes` | `Uint8Array` | structural | |
| `None` | `null` / `undefined` | behavioral | Use `null` for explicit absence; `undefined` for unset |
| `list[T]` | `Array` | structural | Dynamic arrays; no typed generics |
| `dict[K,V]` | `Object` or `Map` | behavioral | Use `Map` when keys are non-string or when order matters |
| `set[T]` | `Set` | structural | |
| `tuple[A,B]` | `[A, B]` (array) or `{first, second}` | structural | Prefer destructured array |
| `Optional[T]` | `T \| null` | structural | |

## Critical: Number Precision Gap

**Python integers are unbounded. JavaScript `number` is IEEE 754 float64.**

Safe integer range: `Number.MIN_SAFE_INTEGER` to `Number.MAX_SAFE_INTEGER` (±2^53 - 1).

For every integer operation in the IPO registry:
1. Can the value exceed 2^53? → Use `BigInt`
2. Is it used in bitwise operations? → JS bitwise ops truncate to 32-bit signed; use `BigInt` or explicit masking
3. Is it used as an array index? → Safe (arrays limited to 2^32 elements)

```js
// Source: Python large int computation
// Target: use BigInt
const result = BigInt(a) * BigInt(b);  // NOT: a * b (may lose precision)
```

## Standard Library / Bun APIs

| Python | Bun | Equivalence | Notes |
|---|---|---|---|
| `os.path.join` | `path.join()` (node:path) | structural | `import { join } from 'node:path'` |
| `os.listdir` | `fs.readdirSync()` or `Bun.readdir()` | structural | Prefer Bun native API |
| `os.environ.get` | `process.env.KEY` | structural | |
| `open(f, 'r')` | `Bun.file(path).text()` | structural | Bun API; returns Promise |
| `open(f, 'rb')` | `Bun.file(path).arrayBuffer()` | structural | |
| `json.dumps` | `JSON.stringify` | structural | |
| `json.loads` | `JSON.parse` | structural | |
| `re.compile` | `new RegExp(pattern)` | structural | |
| `hashlib.sha256` | `new Bun.CryptoHasher('sha256')` | structural | Bun native |
| `time.time()` | `Date.now() / 1000` | structural | Returns float seconds |
| `random.random()` | `Math.random()` | behavioral | Different algorithm; not seedable in standard JS |
| `random.seed` | NO EQUIVALENT in standard JS | GAP | Use `seedrandom` npm package for reproducible RNG |
| `subprocess.run` | `Bun.spawn()` | structural | Bun native subprocess API |
| `logging` | `console.log/warn/error` | structural | Or `pino` for structured logging |
| `argparse` | `Bun.argv` + manual parsing or `yargs` | structural | |

## Error Handling Pattern

Python exceptions map directly to JS throw/catch:

**Python:**
```python
def parse_int(s: str) -> int:
    try:
        return int(s)
    except ValueError:
        raise ParseError(f"invalid int: {s}")
```

**Bun (JS):**
```js
class ParseError extends Error {
    constructor(msg) { super(msg); this.name = 'ParseError'; }
}

function parseInt(s) {
    const n = Number(s);
    if (!Number.isInteger(n) || isNaN(n)) {
        throw new ParseError(`invalid int: ${s}`);
    }
    return n;
}
```

**Rule**: Each Python exception class → JS class extending `Error`. Each `raise ExType(msg)` → `throw new ExType(msg)`. Each `except ExType:` → `catch(e) { if (e instanceof ExType) { ... } }`.

## Async Pattern

**Python:**
```python
async def fetch_data(url: str) -> bytes:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.read()
```

**Bun:**
```js
async function fetchData(url) {
    const response = await fetch(url);  // Bun has native fetch
    return new Uint8Array(await response.arrayBuffer());
}
```

## Class → Class (ES6)

Python classes map directly to ES6 classes:

**Python:**
```python
class Counter:
    def __init__(self, start: int = 0):
        self._count = start
    def increment(self):
        self._count += 1
    def value(self) -> int:
        return self._count
```

**JS:**
```js
class Counter {
    #count;  // private field (ES2022)
    constructor(start = 0) {
        this.#count = start;
    }
    increment() {
        this.#count += 1;
    }
    value() {
        return this.#count;
    }
}
```

## Anti-Patterns

| Wrong | Why | Correct |
|---|---|---|
| `==` for equality | JS `==` coerces types | Always use `===` |
| `parseInt(s)` (JS builtin) | Has different semantics from Python `int()` | Use `Number(s)` + `Number.isInteger` check |
| Treating `0`, `""`, `null` as false uniformly | JS falsy rules differ from Python | Explicit: `value === null`, `value === 0` |
| `for...in` on arrays | Iterates keys (string indices) | Use `for...of` or `.forEach` |
| Not handling Promise rejections | Silent failures | Always `await` or `.catch()` |

## Ecosystem Gaps

| Python | Gap | Compensation |
|---|---|---|
| Seedable RNG | `Math.random()` not seedable | `npm install seedrandom`; `const rng = new seedrandom(seed)` |
| `dict` preserves order | `Object` order is implementation-defined for non-string keys | Use `Map` for reliable insertion order |
| `int` unbounded | `number` loses precision >2^53 | Use `BigInt` where needed |
| `bytes` mutable | `Uint8Array` is mutable; string is immutable | Use `Uint8Array` for mutable byte work |

## Testing Toolchain

| Python | Bun | Notes |
|---|---|---|
| `pytest` | `bun test` | Built-in; `test("name", () => { ... })` |
| `pytest.raises` | `expect(() => fn()).toThrow(ErrorClass)` | |
| `unittest.mock` | PROHIBITED | Real implementations only |
| `mypy` | N/A (dynamic JS) | Use TypeScript for type checking |
| `black` | `bun run prettier --write .` | |

## Build / CI

```yaml
# Python:
- run: pytest

# Bun:
- run: bun install
- run: bun test
```
