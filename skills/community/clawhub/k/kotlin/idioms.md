# Idioms — Scope Functions, Sealed Types, Delegation, DSLs

The idioms are cheap to learn and easy to overuse. The value here is in the selection rules and in the traps that survive code review because the code reads well.

## Scope Functions

| Function | Receiver | Returns | Use for |
|---|---|---|---|
| `let` | `it` | Lambda result | Null-scoped work, converting a value into another type |
| `run` | `this` | Lambda result | A block of computation over a receiver, or grouping statements into an expression |
| `apply` | `this` | The receiver | Configuring an object before handing it on |
| `also` | `it` | The receiver | Side effects in a chain: logging, validation, registration |
| `with` | `this` | Lambda result | Several calls on one non-null object, without a chain |

Selection rule: pick by *what you need back*. Need the object → `apply`/`also`; need the computed value → `run`/`let`/`with`. Pick `it` over `this` whenever the block also touches the outer scope, because `this` shadows silently and `it` does not.

- Nesting two scope functions makes `this` and `it` ambiguous to the reader before it is ambiguous to the compiler. Extract a named function at the first nesting.
- `apply` on a builder that returns `this` anyway is noise; use the builder's chain.
- `takeIf { }` / `takeUnless { }` turn a condition into a nullable value: `text.takeIf { it.isNotBlank() } ?: return`. They allocate a lambda in a hot path — plain `if` there.
- `also { require(…) }` is a clean validation point in a construction chain because it keeps the value flowing.

## Extension Functions

- Extensions are resolved *statically* on the declared type: an extension on `Base` and one on `Derived` are chosen by the reference's static type, not by the runtime object. Extensions are not polymorphic — if you need dispatch, use a member function.
- A member function always wins over an extension with the same signature. Adding a member to a class silently redirects every call site that used your extension.
- Extensions on nullable receivers are legal and useful: `fun String?.orEmpty()` runs with `this == null` inside.
- Scoping: declare an extension `private` in the file that needs it, or in the module that owns the receiver's domain. A public extension on `String` in a shared module pollutes autocomplete for the whole codebase.
- Extension properties cannot have backing fields — they compile to a getter. Storing state "on" a class you do not own means a map keyed by instances, which is a leak unless the map is weak.
- Extensions compile to static methods with the receiver as the first parameter, which is exactly how Java callers see them (`StringUtilsKt.isEmail(s)`).

## Sealed Types And State Modelling

- `sealed interface` over `sealed class` unless you need shared state: an interface allows a type to belong to several hierarchies and keeps `object` subclasses free of construction cost.
- Subclasses must live in the same package and module (same *file* only for Kotlin <1.5) — the restriction is what lets the compiler prove exhaustiveness.
- Use `data object` for stateless variants (Kotlin >=1.9) so `toString` and `equals` behave like the data classes next to them.
- Model states as one hierarchy, not as a bag of booleans: `Loading | Content(data) | Empty | Error(cause)` makes "loading and error at once" unrepresentable, which is the whole point.
- `when` over a sealed type must be an expression to be checked (SKILL.md rule 9). An `else` branch is the mechanism that turns a compile error into a runtime surprise when someone adds a variant.
- Enum vs sealed: enum when the variants carry no data and you need `values()`/`valueOf`; sealed when variants carry different payloads.

## Delegation

- Class delegation: `class Repo(db: Db) : Db by db` forwards every interface member. The catch: forwarded calls go to the *delegate's* implementation, so overriding a method in `Repo` does not affect calls the delegate makes internally.
- `by lazy` — thread-safe by default (SYNCHRONIZED); `LazyThreadSafetyMode.NONE` when confined to one thread; `PUBLICATION` when several threads may compute but any result is acceptable.
- `Delegates.observable(initial) { _, old, new -> }` fires after every set; `Delegates.vetoable` runs before and returns false to reject the new value.
- `Delegates.notNull<Int>()` is `lateinit` for primitives.
- `by map` (`val name: String by properties`) reads from a map — the shape for config objects and JSON-backed models.
- A custom delegate implements `getValue`/`setValue` operators and allocates one delegate object *per property per instance*: cheap for a handful of properties, measurable when a class with 30 delegated properties is created in a loop.

## Functions And Arguments

- Default arguments plus named arguments replace overload sets — except for Java callers, who see neither (`@JvmOverloads` generates the overloads).
- A boolean parameter at a call site is unreadable: `render(true)`. Either name it (`render(animate = true)`) or take an enum.
- `vararg` copies the array at every call; `vararg` plus spread (`*array`) copies again.
- Single-expression functions (`fun area() = w * h`) with an inferred return type are fine internally and a hazard on public API: a change in the expression silently changes the published type. Declare return types on anything public (`explicit_api` enforces this).
- `infix` is for a genuine two-operand vocabulary (`1 to "a"`, `x shl 2`), not for making prose out of code.
- `operator fun invoke` turns an object into a callable — legitimate for a single-method use case, confusing for anything with several behaviours.
- Local functions capture their enclosing scope and keep a long function readable without exporting helpers; a local function nested three deep should be a class.

## Objects, Companions, Constants

- `object` is a lazily-initialized singleton, thread-safe on first access.
- `companion object` members are not static: they live on a synthetic `Companion` instance, so every access from Java goes through `Foo.Companion` unless annotated (`@JvmStatic`, `@JvmField`).
- `const val` is inlined at the call site at compile time — only for primitives and `String`, and changing one requires recompiling every consumer (relevant for libraries, not for app modules).
- Anonymous `object : Listener { }` expressions capture the enclosing instance. Registered and never unregistered, that capture is the classic leak.

## Strings And Control Flow

- Templates over concatenation: `"$count items"`, `"${user.name}'s"`. Escape a literal dollar with `${'$'}`.
- Raw strings with `trimIndent()` for JSON, SQL and multi-line text; `trimMargin("|")` when the content itself starts with whitespace that matters.
- `buildString { }` when a string is assembled in a loop: `+=` allocates a new string per iteration.
- `require` (IllegalArgumentException) for caller mistakes, `check` (IllegalStateException) for internal invariants, `error("…")` for the unreachable branch, `TODO()` for the not-yet-written one — it throws, so it never ships silently.
- `assert` on the JVM is disabled unless the process runs with `-ea`. It is not a validation mechanism.
- `use { }` on any `Closeable` closes it on every path, including exceptions: `file.bufferedReader().use { it.readText() }`.
- `repeat(n) { }`, `for (i in 0 until n)`, `for (i in n downTo 1 step 2)`, `until`/`..<` for exclusive ranges — an index `var` with manual increment is a bug waiting for a refactor.
- Labelled returns (`loop@`, `return@forEach`) escape nested lambdas; more than one label in a function usually means the function should be split.

## Type-Safe Builders (DSLs)

- The pattern is a lambda with receiver: `fun html(block: Html.() -> Unit): Html = Html().apply(block)`.
- `@DslMarker` on an annotation applied to the builder types stops the inner block from silently calling the outer receiver's methods — without it, a nested DSL compiles into the wrong place.
- Keep DSL scope classes `@PublishedApi internal` or explicitly public with documented members; a half-public builder API is impossible to evolve.
- The cost of a DSL is discoverability: an unfamiliar reader cannot autocomplete their way through it. Worth it for structures written many times (UI trees, test fixtures, build config), not for a single call site.
