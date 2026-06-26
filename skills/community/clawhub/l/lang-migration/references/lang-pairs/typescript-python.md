# Language Pair: TypeScript → Python

**Difficulty tier**: Low (type systems are structurally similar; most patterns map 1:1)

**Key advantage**: TypeScript's rich type annotations are a goldmine — they provide the
type information that Python's `typing` module needs. Unlike migrating from plain JS,
TypeScript gives you interface definitions, generics, union types, and optional types
that translate almost directly.

**Key differences**:
- Types: TS structural typing → Python `Protocol` (same philosophy, different syntax)
- Async: TS Promise/async → Python asyncio (same model)
- Decorators: TS decorators (experimental) → Python decorators (stable, same concept)
- `undefined` vs `null`: TS has both → Python has only `None`
- Numbers: TS `number` (float64) + `bigint` → Python `int` / `float`
- `readonly`: TS compile-time → Python convention + `Final`

---

## Pre-Mapped Core Types

| TypeScript | Python | Equivalence | Notes |
|---|---|---|---|
| `number` (integer) | `int` | behavioral | Determine from usage context |
| `number` (float) | `float` | structural | |
| `bigint` | `int` | structural | |
| `boolean` | `bool` | structural | |
| `string` | `str` | structural | |
| `null` | `None` | structural | |
| `undefined` | `None` | behavioral | Document distinction where relevant |
| `void` | `None` | structural | |
| `never` | `NoReturn` | structural | `from typing import NoReturn` |
| `unknown` | `object` or `Any` | behavioral | `unknown` is safer than `any`; use `object` |
| `any` | `Any` | structural | Both are escape hatches |
| `T[]` / `Array<T>` | `list[T]` | structural | |
| `readonly T[]` | `tuple[T, ...]` or `Sequence[T]` | behavioral | Document immutability intent |
| `[A, B]` tuple | `tuple[A, B]` | structural | |
| `Map<K,V>` | `dict[K,V]` | structural | |
| `Set<T>` | `set[T]` | structural | |
| `Record<K,V>` | `dict[K,V]` | structural | |
| `T \| null` | `Optional[T]` | structural | |
| `T \| undefined` | `Optional[T]` | behavioral | |
| `A \| B \| C` | `Union[A, B, C]` | structural | |
| `A & B` (intersection) | Multiple inheritance / Protocol | structural | |
| `Promise<T>` | `Awaitable[T]` | structural | |
| `Uint8Array` | `bytes` | structural | |

---

## Interface → Protocol / ABC

TypeScript interfaces (structural typing) → Python `Protocol`:

**TypeScript:**
```typescript
interface Comparable<T> {
    compareTo(other: T): number;
    equals(other: T): boolean;
}

interface Serializable {
    serialize(): Uint8Array;
    readonly version: number;
}
```

**Python:**
```python
from typing import Protocol, TypeVar
T = TypeVar('T')

class Comparable(Protocol[T]):
    def compare_to(self, other: T) -> int: ...
    def equals(self, other: T) -> bool: ...

class Serializable(Protocol):
    def serialize(self) -> bytes: ...
    @property
    def version(self) -> int: ...
```

**Rule**: TS `interface` → Python `Protocol` (structural). TS `abstract class` → Python `ABC`.

---

## Generic Types → TypeVar

**TypeScript:**
```typescript
function zip<A, B>(as: A[], bs: B[]): [A, B][] {
    return as.map((a, i) => [a, bs[i]]);
}

class Repository<T extends { id: string }> {
    private items = new Map<string, T>();
    add(item: T): void { this.items.set(item.id, item); }
    get(id: string): T | undefined { return this.items.get(id); }
}
```

**Python:**
```python
from typing import TypeVar, Generic, Protocol

A = TypeVar('A')
B = TypeVar('B')

def zip_lists(as_: list[A], bs: list[B]) -> list[tuple[A, B]]:
    return [(a, b) for a, b in zip(as_, bs)]

class HasId(Protocol):
    id: str

T = TypeVar('T', bound=HasId)

class Repository(Generic[T]):
    def __init__(self) -> None:
        self._items: dict[str, T] = {}

    def add(self, item: T) -> None:
        self._items[item.id] = item

    def get(self, id: str) -> Optional[T]:
        return self._items.get(id)
```

`T extends Constraint` → `TypeVar('T', bound=ConstraintProtocol)`.

---

## Union Types → Union / Discriminated Unions

**TypeScript:**
```typescript
type Shape =
  | { kind: 'circle'; radius: number }
  | { kind: 'rectangle'; width: number; height: number };

function area(shape: Shape): number {
    switch (shape.kind) {
        case 'circle': return Math.PI * shape.radius ** 2;
        case 'rectangle': return shape.width * shape.height;
    }
}
```

**Python:**
```python
from dataclasses import dataclass
import math

@dataclass
class Circle:
    radius: float

@dataclass  
class Rectangle:
    width: float
    height: float

Shape = Union[Circle, Rectangle]

def area(shape: Shape) -> float:
    # TS SOURCE: discriminated union on shape.kind
    if isinstance(shape, Circle):
        return math.pi * shape.radius ** 2
    elif isinstance(shape, Rectangle):
        return shape.width * shape.height
    else:
        raise ValueError(f"unknown shape: {type(shape)}")
```

---

## Utility Types → Python Equivalents

| TypeScript | Python | Notes |
|---|---|---|
| `Partial<T>` | All fields `Optional[T]` | Use `@dataclass` with `Optional` defaults |
| `Required<T>` | All fields non-optional | Remove `Optional` annotations |
| `Readonly<T>` | `@dataclass(frozen=True)` | Or use `Final` fields |
| `Pick<T, 'a'\|'b'>` | New `@dataclass` with selected fields | No runtime equivalent |
| `Omit<T, 'a'>` | New `@dataclass` without the field | |
| `Record<K,V>` | `dict[K,V]` | |
| `ReturnType<typeof fn>` | `-> type` annotation on fn | Determine from source |
| `Parameters<typeof fn>` | Type annotations on parameters | Determine from source |
| `NonNullable<T>` | Remove `Optional` | |
| `Awaited<T>` | The inner type of `Awaitable[T]` | |

---

## Decorators

TypeScript decorators → Python decorators (Python's are more stable and expressive):

**TypeScript:**
```typescript
function log(target: any, key: string, descriptor: PropertyDescriptor) {
    const original = descriptor.value;
    descriptor.value = function(...args: any[]) {
        console.log(`Calling ${key}`);
        return original.apply(this, args);
    };
    return descriptor;
}

class Service {
    @log
    processOrder(order: Order): void { ... }
}
```

**Python:**
```python
import functools
import logging
from typing import Callable, TypeVar, ParamSpec

P = ParamSpec('P')
R = TypeVar('R')

def log(fn: Callable[P, R]) -> Callable[P, R]:
    @functools.wraps(fn)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        logging.info(f"Calling {fn.__name__}")
        return fn(*args, **kwargs)
    return wrapper

class Service:
    @log
    def process_order(self, order: Order) -> None: ...
```

---

## `readonly` → `Final` / `frozen=True`

```typescript
// TS: compile-time readonly
class Config {
    readonly maxRetries: number = 3;
    readonly endpoint: string;
    constructor(endpoint: string) { this.endpoint = endpoint; }
}
```

```python
from dataclasses import dataclass
from typing import Final

@dataclass(frozen=True)  # makes all fields immutable at runtime
class Config:
    endpoint: str
    max_retries: int = 3
    # TS SOURCE: readonly fields — Python enforces with frozen=True
```

For module-level `const`: use `Final`.

---

## Enum → Python Enum

**TypeScript:**
```typescript
enum Direction { Up = 'UP', Down = 'DOWN', Left = 'LEFT', Right = 'RIGHT' }
enum Status { Active = 1, Inactive = 2, Pending = 3 }
```

**Python:**
```python
from enum import Enum, IntEnum

class Direction(Enum):
    UP = 'UP'
    DOWN = 'DOWN'
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'

class Status(IntEnum):
    ACTIVE = 1
    INACTIVE = 2
    PENDING = 3
```

Use `IntEnum` when TS enum values are numbers (preserves arithmetic compatibility).
Use `Enum` for string enums.

---

## async/await → asyncio

Identical to `bun-python.md` — see that file for the full mapping.
Key addition for TypeScript: `AsyncGenerator<T>` → `AsyncGenerator[T, None]` in Python.

```typescript
async function* generateItems(): AsyncGenerator<number> {
    for (let i = 0; i < 10; i++) yield i;
}
```

```python
from typing import AsyncGenerator

async def generate_items() -> AsyncGenerator[int, None]:
    for i in range(10):
        yield i
```

---

## Naming Convention

| TypeScript | Python |
|---|---|
| `camelCase` functions | `snake_case` |
| `PascalCase` classes/interfaces | `PascalCase` |
| `SCREAMING_SNAKE_CASE` constants | `SCREAMING_SNAKE_CASE` + `Final` |
| `_private` (no enforcement) | `_private` (convention) |
| `#trulyPrivate` (ES2022) | `__mangled` (name mangling) |
| `I` prefix interfaces (`IStorage`) | Remove `I` prefix in Python |

---

## Ecosystem Gaps

| TypeScript | Gap | Python |
|---|---|---|
| `undefined` | Python has no undefined | Map to `None`; document |
| Structural typing at compile time | Python `Protocol` checked by mypy only | Enforce with mypy in CI |
| `const enum` (inlined) | No equivalent | Regular `Enum` |
| Template literal types | No equivalent | Document as string format comments |
| `infer` keyword | No equivalent | Determine type manually |
| `satisfies` keyword | No equivalent | Use `isinstance` assertions |
| Mapped types | No equivalent | Manual `@dataclass` |

---

## Testing Toolchain

| TypeScript | Python | Notes |
|---|---|---|
| `vitest` / `jest` / `bun test` | `pytest` | |
| `expect(val).toBe(x)` | `assert val == x` | |
| `expect(fn).toThrow(ErrClass)` | `pytest.raises(ErrClass)` | |
| `mock()` / `jest.fn()` | PROHIBITED | Real implementations only |
| `tsc --noEmit` (type check) | `mypy .` | |
| `prettier` | `black .` | |
| `eslint` | `ruff check .` | |
| `vitest --coverage` | `pytest --cov` | |

## Build / CI

```yaml
# TypeScript (source):
- run: bun install && bun tsc --noEmit && bun test

# Python (target):
- run: pip install -r requirements.txt
- run: pytest
- run: mypy .
- run: ruff check .
- run: black --check .
```
