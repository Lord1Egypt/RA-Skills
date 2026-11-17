# PHP 8 Features — What to Reach For, and What It Costs

Each entry: what it replaces, and the edge that bites. Version floors are in SKILL.md; the upgrade procedure is in `versions.md`.

## match

- Compares with `===`, returns a value, has no fall-through, and throws `UnhandledMatchError` when nothing matches. That last property is a feature: a new enum case surfaces as an exception instead of a silently skipped branch.
- Multiple conditions per arm: `1, 2 => 'low',`. A `default` arm turns exhaustiveness off — omit it when you want the analyzer and the runtime to force you to handle every case.
- `match(true)` with boolean arms replaces an if/elseif ladder and stays an expression: `match(true) { $n < 10 => 'low', $n < 100 => 'mid', default => 'high' }`.
- Arms are expressions only. A branch needing three statements calls a method; that pressure toward small named operations is usually an improvement.

## Enums

- Replace class constants and magic strings. `enum Status: string { case Draft = 'draft'; … }` gives type-safe parameters, exhaustive `match`, and `Status::cases()` as the single source for dropdowns and validation.
- `from()` throws, `tryFrom()` returns null — parse external input with `tryFrom` (`oop.md`).
- Backed enums JSON-encode to their value; pure enums throw unless they implement `JsonSerializable` (`json.md`).
- Cannot hold state and cannot extend. Behavior goes in methods or a trait; a case-to-data mapping goes in a `match` inside a method, not in a property.

## Named Arguments

- `createUser(email: $e, admin: true)` removes boolean-parameter guessing and lets you skip optional parameters in the middle.
- The cost is real: parameter NAMES become part of your public API. Renaming a parameter is a breaking change for every named-argument caller, and no analyzer level catches it in a consumer's code. Interfaces are the worst case — an implementation is free to rename, so named arguments against an interface are unsafe.
- Practical line: use them freely at call sites inside your own codebase and in library code you own; treat parameter names in published interfaces as frozen.

## Constructor Promotion, readonly, and Property Hooks

- `public function __construct(private readonly Clock $clock) {}` collapses three lines into one. Promoted parameters cannot be `callable`-typed and cannot be used in a `variadic`.
- `readonly` properties (`php >=8.1`) and `readonly` classes (`php >=8.2`) give value objects for free; the `withX(): static` pattern replaces setters. Reinitializing a readonly property inside `__clone` needs `php >=8.3`.
- Property hooks (`php >=8.4`) attach `get`/`set` to the property itself, deleting getter-only boilerplate and most remaining uses of `__get`.
- Asymmetric visibility (`php >=8.4`): `public private(set) int $count;` is a public reader with a private writer.

## Nullsafe Operator

- `$user?->address?->city` short-circuits the ENTIRE chain to the right when any link is null, including method arguments that would have been evaluated.
- It does not extend past the chain: `$a?->b + 1` still evaluates `null + 1`. It cannot appear on the left of an assignment.
- Overusing it hides missing-data bugs. A null that should be impossible deserves an exception, not a silent chain of nulls.

## Attributes

- Structured metadata the engine parses (`#[Route('/users')]`), read through `ReflectionClass::getAttributes()` and materialized with `newInstance()`. They replace docblock annotations, which were strings that no tool could type-check.
- Reflection is not free: cache the resolved metadata (compiled container, cached route table), never scan attributes per request (`performance.md`).
- An attribute class is an ordinary class marked `#[Attribute]`; its constructor signature is the attribute's syntax.

## Types

- Union types (`int|string`), intersection types (`Countable&Traversable`, `php >=8.1`), and DNF combinations (`(A&B)|null`, `php >=8.2`).
- `never` (`php >=8.1`) on a function that always throws or exits lets the analyzer know the following code is unreachable.
- `static` as a return type is what makes fluent base classes type-check on subclasses; `self` would pin them to the parent (`oop.md`).
- Standalone `null`, `false`, and `true` types (`php >=8.2`) let you type the legacy `false`-on-failure functions honestly.
- Typed class constants (`php >=8.3`) stop a subclass from redefining a constant with an incompatible type.

## Everyday Additions

| Feature | Replaces | Floor |
|---|---|---|
| `str_contains`, `str_starts_with`, `str_ends_with` | `strpos(...) !== false` and its offset-0 trap | php >=8.0 |
| `array_is_list()` | `$a === array_values($a)` | php >=8.1 |
| First-class callables `$obj->m(...)` | `[$obj, 'm']` and `'strlen'` strings | php >=8.1 |
| `new` in initializers | Nullable parameter plus a null check in the body | php >=8.1 |
| `#[\Override]` | A comment hoping the parent method still exists | php >=8.3 |
| `json_validate()` | `json_decode` purely to test validity, allocating the whole tree | php >=8.3 |
| `array_find`, `array_any`, `array_all` | `foreach` with a flag variable | php >=8.4 |
| `mb_trim`, `mb_str_pad` | Byte-based trimming and padding on human text | php >=8.4 / 8.3 |
| Pipe operator `\|>` | Nested calls read inside-out | php >=8.5 |
| `#[\NoDiscard]` | A comment saying "you must use this return value" | php >=8.5 |

## Fibers

- `Fiber` (`php >=8.1`) is cooperative single-threaded suspension, not parallelism: it lets a library suspend a call stack and resume it later.
- You almost never write `Fiber` directly. Its value is that ReactPHP, Amp, and similar runtimes can now offer async I/O without infecting every caller's signature with promises (`concurrency.md`).

## Behavior Changes That Break Old Code

- String-to-number comparison changed on `php >=8.0`: `0 == "foo"` is now `false`. Validation code that leaned on the old truth silently changes meaning (`types.md`).
- Many warnings became `Error`s: method calls on null, undefined functions, wrong argument counts. Code that "used to keep going" now stops.
- `htmlspecialchars` escapes single quotes by default on `php >=8.1`; output compared byte-for-byte in tests will differ.
- Dynamic properties deprecated on `php >=8.2`; `${var}` interpolation deprecated on the same release.
- Implicit nullable parameters (`Foo $x = null`) deprecated on `php >=8.4` — a mechanical fix Rector applies across a codebase in one pass (`static-analysis.md`).

## Related

- Choosing a floor and surviving the deprecation wall: `versions.md`
- Class-design consequences of readonly, enums, and hooks: `oop.md`
- Type semantics underneath the new syntax: `types.md`
