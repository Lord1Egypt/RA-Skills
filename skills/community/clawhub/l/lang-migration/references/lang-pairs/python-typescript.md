# Language Pair: Python → TypeScript

**Difficulty tier**: Moderate (dynamic→static with escape hatches; number precision gap)

**Runtime context**: TypeScript compiles to JavaScript. Specify the runtime:
- Node.js: use `node:` prefixed imports
- Bun: prefer Bun native APIs (see `python-bun.md` for Bun-specific APIs)
- Deno: use Deno APIs

**Key advantages over plain JS**: TypeScript's type system is rich enough to express most Python type annotations directly. `typing.Optional`, `Union`, `Generic` all have TS equivalents.

**Key differences**:
- Type system: Python `typing` / TypeScript types (structural, not nominal)
- Number precision: Same gap as JS — `number` is float64, no unbounded int
- Errors: Python exceptions / TS exceptions (throw/catch)
- Async: Python asyncio / TS async/await (Promise-based)

---

## Pre-Mapped Core Types

| Python Type | TypeScript Type | Equivalence | Notes |
|---|---|---|---|
| `int` (< 2^53) | `number` | structural | |
| `int` (>= 2^53) | `bigint` | structural | |
| `float` | `number` | behavioral | No separate int/float in TS |
| `bool` | `boolean` | structural | |
| `str` | `string` | structural | |
| `bytes` | `Uint8Array` | structural | |
| `None` | `null` | structural | |
| `list[T]` | `T[]` or `Array<T>` | structural | |
| `tuple[A, B]` | `[A, B]` | structural | TS has real tuple types |
| `dict[K, V]` | `Map<K, V>` | structural | Use `Map` not `{}` for typed dicts |
| `set[T]` | `Set<T>` | structural | |
| `Optional[T]` | `T \| null` | structural | |
| `Union[A, B]` | `A \| B` | structural | |
| `Any` | `unknown` | structural | Prefer `unknown` over `any`; `any` bypasses type system |
| `TypeVar('T')` | `<T>` generic | structural | |
| `Literal['a', 'b']` | `'a' \| 'b'` | structural | |
| `TypedDict` | `interface` or `type` | structural | |
| `dataclass` | `interface` + class | structural | |
| `Enum` | `enum` or `const` object | structural | TS `const enum` is more efficient |
| `Protocol` | `interface` | structural | TS uses structural typing — interfaces are protocols |
| `Callable[[A], B]` | `(a: A) => B` | structural | |

## Standard Library Mapping

| Python | TypeScript (Node.js) | Equivalence | Notes |
|---|---|---|---|
| `os.path.join` | `path.join()` from `'node:path'` | structural | |
| `os.listdir` | `fs.readdirSync()` from `'node:fs'` | structural | |
| `os.environ.get('KEY', default)` | `process.env.KEY ?? default` | structural | |
| `open(f, 'r').read()` | `fs.readFileSync(f, 'utf8')` | structural | |
| `json.dumps(obj, indent=2)` | `JSON.stringify(obj, null, 2)` | structural | |
| `json.loads(s)` | `JSON.parse(s)` | structural | Returns `any`; type-assert the result |
| `re.compile(pattern)` | `new RegExp(pattern)` | structural | |
| `time.time()` | `Date.now() / 1000` | structural | |
| `random.random()` | `Math.random()` | behavioral | Not seedable |
| `hashlib.sha256` | `crypto.createHash('sha256')` from `'node:crypto'` | structural | |
| `subprocess.run` | `child_process.spawnSync` or `execSync` | structural | |
| `logging` | `console.log/warn/error` or `pino`/`winston` | structural | |
| `argparse` | `yargs` or `commander` | structural | |
| `dataclasses.dataclass` | `class` with typed properties | structural | |
| `abc.ABC` + `@abstractmethod` | `abstract class` | structural | |

## Type Annotation Migration

Python typing maps almost 1:1 to TypeScript:

```typescript
// Python: def process(data: list[tuple[str, int]], 
//                      callback: Callable[[str], bool]) -> Optional[dict[str, Any]]
// TypeScript:
function process(
    data: Array<[string, number]>,
    callback: (s: string) => boolean
): Map<string, unknown> | null { ... }
```

**Rules**:
- `Optional[T]` → `T | null`
- `Union[A, B, C]` → `A | B | C`
- `Dict[K, V]` → `Map<K, V>` (or `Record<K, V>` for string-keyed objects)
- `Any` → `unknown` (safer) or `any` (escape hatch; document why)
- `TypedDict` → `interface`
- `Protocol` → `interface`
- `Generic[T]` → `<T>` on class/function

## Error Handling

Identical to `python-bun.md` — JS exceptions mirror Python exceptions:

```typescript
class ParseError extends Error {
    constructor(message: string) {
        super(message);
        this.name = 'ParseError';
    }
}

function parseValue(s: string): number {
    const n = Number(s);
    if (!Number.isFinite(n)) {
        throw new ParseError(`invalid number: ${s}`);
    }
    return n;
}
```

## Class Migration

TypeScript classes are a superset of Python classes in expressivity:

| Python | TypeScript |
|---|---|
| `def __init__(self, x: int):` | `constructor(private x: number) {}` |
| `self.x` | `this.x` |
| `@property` | `get x()` / `set x(v)` |
| `@classmethod` | `static` method |
| `@staticmethod` | `static` method |
| `__str__` | `toString()` |
| `__eq__` | Override `equals()` (no operator overload in TS) |
| `__len__` | `get length()` or explicit method |

## Abstract Base Classes / Protocols

**Python:**
```python
class Storage(Protocol):
    def read(self, key: str) -> bytes: ...
    def write(self, key: str, data: bytes) -> None: ...
```

**TypeScript:**
```typescript
interface Storage {
    read(key: string): Uint8Array;
    write(key: string, data: Uint8Array): void;
}
```

TS uses structural typing — any class with matching methods satisfies the interface automatically, just like Python Protocols.

## Decorator Migration

Python decorators → TypeScript decorators (experimental, needs `experimentalDecorators: true`) or higher-order functions:

```typescript
// Python: @retry(max_attempts=3)
// TypeScript (higher-order function, no decorator):
function withRetry<T>(fn: () => Promise<T>, maxAttempts: number): () => Promise<T> {
    return async () => {
        for (let i = 0; i < maxAttempts; i++) {
            try { return await fn(); } catch (e) {
                if (i === maxAttempts - 1) throw e;
            }
        }
        throw new Error('unreachable');
    };
}
```

## Anti-Patterns

| Wrong | Why | Correct |
|---|---|---|
| Using `any` everywhere | Defeats type system; not structural | Use specific types; `unknown` if truly dynamic |
| `{}` for typed dictionaries | No type safety on keys | Use `Map<K, V>` or `interface` |
| `==` for equality | Type coercion | Always `===` |
| `parseInt(s)` builtin | Ignores trailing non-digits | `Number(s)` + `Number.isInteger` check |
| Not explicitly handling `undefined` | TS optional chaining hides bugs | Check `!== undefined` explicitly |

## Ecosystem Gaps

| Python | Gap | Compensation |
|---|---|---|
| Seedable RNG | `Math.random()` not seedable | `npm install seedrandom`; type: `@types/seedrandom` |
| `int` unbounded | `number` loses precision >2^53 | Use `bigint` where needed |
| `@dataclass` equality | TS classes don't auto-implement structural equality | Implement explicit `equals()` method |
| `functools.lru_cache` | No stdlib equivalent | Use `npm install lru-cache` or `Map` with manual eviction |
| `itertools` | Limited stdlib equivalent | Implement generators manually or use `itertools-ts` |

## Testing Toolchain

| Python | TypeScript | Notes |
|---|---|---|
| `pytest` | `vitest` or `jest` or `bun test` | |
| `pytest.raises` | `expect(() => fn()).toThrow(ErrorClass)` | |
| `unittest.mock` | PROHIBITED | Real implementations only |
| `mypy` | TypeScript compiler (`tsc --noEmit`) | |
| `black` | `prettier` | |
| `ruff` / `flake8` | `eslint` | |

## tsconfig.json Baseline

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "noImplicitAny": true,
    "strictNullChecks": true
  }
}
```

Enable all strict options. Do not disable `strictNullChecks` to work around translation difficulties.

## Build / CI

```yaml
# Python:
- run: pip install -r requirements.txt && pytest

# TypeScript (Bun):
- run: bun install
- run: bun tsc --noEmit
- run: bun test
```
