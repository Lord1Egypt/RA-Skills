# Objects, Classes, and Inheritance

## Binding: self vs static vs $this

- `self::` resolves to the class where the code is WRITTEN, at compile time. `static::` resolves to the class the call was made ON, at runtime — late static binding.
- `new self()` in a parent factory returns the parent even when called on a child; `new static()` returns the child. Every fluent/factory base class wants `static`.
- `static` is also a return type (`php >=8.0`), which is what makes `withX(): static` type-check on subclasses.
- `parent::method()` calls the parent implementation; inside it, `static::` still points at the original object.
- `$this` exists in static context never — a static method calling `$this->x` is a fatal `Error`, and closures bound to a class keep the binding they were created with (`Closure::bind` changes it).

## Properties

- Typed properties (`php >=7.4`) with no default are UNINITIALIZED, which is different from `null`: reading one throws `Error: Typed property must not be accessed before initialization`. Give a default or assign in the constructor.
- `readonly` (`php >=8.1`): writable once, and only from inside the declaring class's scope. A `readonly` property cannot have a default value, cannot be `unset()`, and cannot be modified in `__clone` — until `php >=8.3`, which allows reinitializing readonly properties during cloning. `readonly` classes: `php >=8.2`.
- Constructor promotion collapses declaration, parameter, and assignment: `public function __construct(private readonly Logger $log) {}`.
- Dynamic properties (assigning to an undeclared property) are deprecated on `php >=8.2`. Add the property, use `#[\AllowDynamicProperties]` deliberately, or extend `stdClass`.
- Asymmetric visibility (`php >=8.4`): `public private(set) string $name;` gives a public reader and a private writer without a getter.
- Property hooks (`php >=8.4`) put `get`/`set` logic on the property itself, which removes the getter-that-only-returns boilerplate — and removes `__get` from most of its remaining use cases.
- Static properties are shared with subclasses unless the subclass redeclares them. `Parent::$count` and `Child::$count` are the same storage; this is the "why did the other tenant's counter move" bug.

## Objects Are Handles

- `$b = $a;` copies the handle, not the object: mutating `$b` mutates `$a`. Arrays are the opposite (`arrays.md`).
- `clone` is shallow — nested objects stay shared. Implement `__clone()` to deep-copy the parts that must not be shared: `$this->meta = clone $this->meta;`.
- `clone` does not call the constructor, so invariants enforced there are not re-checked.
- `==` on objects compares class plus property values recursively; `===` is identity. A cyclic object graph can make `==` recurse until it fatals.
- Objects in a session or cache are serialized: the class must be autoloadable on the next request or you get `__PHP_Incomplete_Class` (`sessions.md`).

## Traits

- A trait is compile-time copy-paste, not inheritance: `instanceof` never sees a trait. Pair every trait with an interface if callers need to type against it.
- Conflicts between two traits with the same method name are a fatal error; resolve with `insteadof` and optionally alias the loser with `as`: `use A, B { A::run insteadof B; B::run as runB; }`.
- Precedence: the using class's own method beats the trait, and the trait beats the inherited parent method. A trait can therefore silently override a parent implementation.
- A trait's static property is separate per USING class, not shared across them — the opposite of static inheritance above.
- Abstract methods in a trait are a contract on the using class; that is how a trait declares its dependencies without an interface.
- `__CLASS__` inside a trait is the using class; `__TRAIT__` is the trait.

## Interfaces and Abstract Classes

- Interfaces can declare constants, and on `php >=8.1` an implementing class or interface may override them (before that it was a fatal error). Typed class constants: `php >=8.3`.
- An abstract class cannot be instantiated but can have a constructor, state, and concrete methods; a class with one abstract method must itself be abstract.
- `#[\Override]` (`php >=8.3`) makes the engine verify that the method really overrides a parent — it catches the renamed-parent-method bug that silently turns an override into a new method.
- Return types are covariant and parameter types contravariant (`php >=7.4`), so a child may narrow the return and widen the parameter, not the reverse.
- `instanceof` accepts a string or a variable holding a class name: `$obj instanceof $className` works and does not autoload if the class is absent (it just returns false).

## Enums (`php >=8.1`)

- Pure enums have cases only; backed enums (`enum S: string`) attach a scalar. Cases are singletons, so `===` is the correct comparison and `match` works naturally.
- `S::from('x')` throws `ValueError` for unknown input; `S::tryFrom('x')` returns `null`. Parse external input with `tryFrom` and decide the error explicitly.
- Enums may implement interfaces and have methods and constants, but cannot have state — no properties, and `$this` in a method refers to the case.
- Backed enums JSON-encode to their value automatically; a pure enum throws unless it implements `JsonSerializable` (`json.md`).
- `S::cases()` returns every case in declaration order — the source of truth for a dropdown or a validation allowlist.
- Enums cannot extend anything; to share behavior use a trait plus an interface.

## Magic Methods (use sparingly, know the rules)

| Method | Fires when | Trap |
|---|---|---|
| `__get`/`__set` | The property is INACCESSIBLE or undefined | Never fires for an accessible declared property; `unset()`-ing one makes them start firing |
| `__isset`/`__unset` | `isset()`/`unset()` on the same | Omit them and `isset($obj->virtual)` is always false |
| `__call`/`__callStatic` | Undefined method | Kills IDE completion and analyzer coverage; document with `@method` |
| `__toString` | String context | May throw on `php >=7.4`; implement `Stringable` for the type |
| `__invoke` | The object is called | Useful for single-method services and middleware |
| `__destruct` | Refcount hits zero, or at shutdown | Shutdown ORDER is not guaranteed; never flush critical data here |
| `__serialize`/`__unserialize` | `serialize()` | Replaces `__sleep`/`__wakeup`; controls exactly which state travels |

Magic methods bypass the engine's property/method caches and are measurably slower than real members — keep them off hot paths (`performance.md`).

## Construction and Failure

- An exception thrown in a constructor leaves no object behind, which is good, but any resource already acquired in that constructor leaks. Acquire nothing before validation completes.
- Named constructors (`public static function fromArray(array $r): self`) let you have several construction paths with distinct validation, which one constructor with optional parameters cannot.
- `new` in initializers (`php >=8.1`) allows `public function __construct(private Logger $l = new NullLogger()) {}` — a real default instead of a nullable parameter.
- First-class callables (`php >=8.1`): `$fn = $this->handle(...);` produces a `Closure` with the correct binding, replacing `[$this, 'handle']` strings that no analyzer could check.
- Lazy objects (`php >=8.4`) give the engine-level proxy pattern that ORMs previously hand-rolled with `__get`.

## Related

- Type declarations and variance rules: `types.md`
- PHP 8 syntax that touches class design: `modern.md`
- Making the analyzer verify overrides, generics, and property types: `static-analysis.md`
