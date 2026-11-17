# Generics, Variance, Inline And Reified

Every generic compile error in Kotlin is one of three things: variance (the type is in the wrong position), erasure (the type does not exist at runtime), or inlining rules (`reified` needs `inline`, and `inline` restricts what the lambda may do).

## Error → Meaning

| Compiler says | It means | Fix |
|---|---|---|
| "Type parameter T is declared as 'out' but occurs in 'in' position" | A producer type used as a parameter | Take a supertype parameter, or use a separate type parameter with `<U : T>` |
| "Type mismatch: inferred type is List\<Dog\> but List\<Animal\> was expected" (on a `MutableList`) | `MutableList` is invariant | Accept `List<Animal>` (covariant) or `MutableList<out Animal>` for reading only |
| "Cannot check for instance of erased type: T" | Type erasure | Make the function `inline` with `reified T` |
| "Cannot use 'T' as reified type parameter" | Passing a non-reified `T` into a reified slot | Propagate `reified` up the call chain, or pass a `KClass<T>` |
| "Only type parameters of inline functions can be reified" | `reified` on a normal function | Add `inline` |
| "Non-local returns are not allowed here" | A `return` inside a `crossinline` lambda | `return@label`, or drop `crossinline` if you can inline the call |
| "Platform declaration clash" | Two functions with the same JVM signature after erasure | `@JvmName("…")` on one of them |
| "Star projection prevents writing" | `List<*>` can be read as `Any?`, never written | Recover the real type parameter, or model the API without the star |

## Variance

- Declaration-site: `out T` means the class only *produces* T (safe to treat `Box<Dog>` as `Box<Animal>`); `in T` means it only *consumes* T (`Comparator<Animal>` works wherever `Comparator<Dog>` is needed). No modifier means invariant.
- Mnemonic that survives review: producers are `out`, consumers are `in` — read-only `List<out E>` is covariant, `MutableList<E>` cannot be, because adding a `Cat` to a `MutableList<Dog>` typed as `MutableList<Animal>` would compile.
- Use-site (type projection) when you cannot change the class: `fun copy(from: Array<out Any>, to: Array<Any>)` — `from` is read-only in that function, so any `Array<Something>` is accepted.
- Star projection `Foo<*>` means "some specific but unknown type": reads produce the upper bound (`Any?` unless bounded), writes are forbidden. Use it for `is Foo<*>` checks and for logging, not as an API parameter.
- Java's arrays are covariant and Kotlin's are not: `Array<String>` is not an `Array<Any>`. This is Kotlin fixing a Java hole, and it is why array APIs need `out` projections at the boundary.

## Erasure And What Survives

- Generic *arguments* are erased on the JVM: at runtime `List<String>` and `List<Int>` are the same class. `x is List<String>` does not compile; `x is List<*>` does.
- Two overloads differing only in a generic argument clash after erasure (`fun f(x: List<String>)` and `fun f(x: List<Int>)`) — `@JvmName` on one, or different function names.
- What does survive: the *declaration's* type parameters in metadata (reflection can read them), superclass type arguments (the trick behind `object : TypeToken<List<Foo>>() {}`), and anything `reified` inlined into the call site.
- Serialization libraries need the full type, which is why they take a `TypeToken`/`typeOf<T>()`/`serializer<T>()` rather than a `Class`.

## inline, noinline, crossinline

- `inline` copies the function body *and its lambdas* into the call site: no `Function` object, no virtual call, and non-local `return` becomes legal inside the lambda. That is what makes `forEach`, `let` and `use` free.
- Inline only functions whose main cost is the lambda. A large inline function multiplies its bytecode at every call site: slower compilation, bigger artifacts, worse instruction-cache behaviour — the compiler warns for functions with no lambda parameters for exactly this reason.
- `noinline` on a lambda parameter keeps it as an object so it can be stored, returned, or passed on to a non-inline function.
- `crossinline` keeps the lambda inlined but forbids non-local returns — required when the lambda is invoked from another execution context (a callback, another thread, a nested object).
- Inline functions cannot touch `private` members of their declaring class, because the copied body ends up in the caller. `@PublishedApi internal` is the escape hatch for library code.
- Public inline functions are a binary-compatibility hazard: their body is baked into every consumer, so changing it does nothing until consumers recompile.

## reified

- `inline fun <reified T> Gson.fromJson(json: String): T = fromJson(json, T::class.java)` — the type argument becomes a real class at the call site, so `T::class`, `is T`, and `as T` all work.
- Without `reified` the same code needs an explicit `Class<T>`/`KClass<T>` parameter — a fine API when the function cannot be inline (a virtual method, or a large body).
- `reified` cannot cross a non-inline boundary: an inline function may pass its reified `T` to another inline reified function, never to a normal one.
- Common uses beyond deserialization: filtering (`inline fun <reified R> Iterable<*>.filterIsInstance()`), typed dependency lookup, and building `typeOf<T>()` for kotlinx.serialization.

## Constraints And Bounds

- Single bound inline: `fun <T : Comparable<T>> max(a: T, b: T)`. Several bounds go in a `where` clause: `fun <T> f(x: T) where T : Comparable<T>, T : Serializable`.
- `<T : Any>` is the way to reject nullable arguments; unbounded `T` includes `T?` (SKILL.md Nullability Decision Table).
- Recursive bounds (`T : Node<T>`) model self-referencing hierarchies and builder chains that must return the concrete type.
- `Nothing` is the type with no values: it is a subtype of everything, so `fun fail(): Nothing = throw …` type-checks anywhere, and `List<Nothing>` (what `emptyList()` really is) is assignable to any `List<T>`.
- A generic function whose type parameter appears only in the return type forces the caller to specify it (`val x: Foo = create()` or `create<Foo>()`) — a common source of "not enough information to infer type parameter".

## Contracts

- A contract tells the compiler what a function guarantees, unlocking smart casts across the call: `contract { returns(true) implies (value is String) }` inside `fun isText(value: Any?): Boolean`.
- `callsInPlace(block, InvocationKind.EXACTLY_ONCE)` lets `val x: Int; run { x = 1 }` compile — it is what makes `let`/`run`/`apply` work with `val` initialization inside them.
- Contracts are declared as the first statement of a function body, only on top-level (non-member, non-override) functions, and the compiler does not verify them: a wrong contract turns a smart cast into an unchecked lie.
- The API is still experimental in the stdlib; using the stdlib's own contracts is safe, writing your own means opting in and accepting the churn.

## Reflection Costs

- `T::class` from a reified parameter is free at runtime (the class literal is inlined). `::class.java` on an instance is cheap. `kotlin-reflect` (`memberProperties`, `callBy`, `KType` inspection) is a separate dependency, adds megabytes, and is slow enough that libraries cache every lookup.
- Prefer a compile-time solution — a code generator, a sealed dispatch table, a `reified` factory — over reflection in anything on a hot path or in an Android artifact.
