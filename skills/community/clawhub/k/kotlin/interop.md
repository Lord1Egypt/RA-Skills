# Java Interop And Migrating Java To Kotlin

Two directions, two different problems. Kotlin calling Java is about nullability and platform types. Java calling Kotlin is about everything Kotlin generates that Java cannot see: default arguments, properties, companions, top-level functions, no checked exceptions.

## Java Calling Kotlin — What They See

| Kotlin | Java sees | Annotation that fixes it |
|---|---|---|
| `val name: String` | `getName()` | `@JvmField` exposes the field directly (no getter) |
| `var isReady: Boolean` | `isReady()` / `setReady()` | — (the `is` prefix keeps its name) |
| `fun f(a: Int, b: Int = 0)` | `f(int, int)` only | `@JvmOverloads` generates the whole overload set |
| `companion object { fun of() }` | `Foo.Companion.of()` | `@JvmStatic` makes it `Foo.of()` |
| Top-level `fun util()` in `Utils.kt` | `UtilsKt.util()` | `@file:JvmName("Utils")` |
| `internal fun f()` | Public with a mangled name (`f$module_name`) | Nothing — `internal` is not a JVM concept |
| `fun read(): String` that throws `IOException` | No checked exception; `catch (IOException)` fails to compile | `@Throws(IOException::class)` |
| `suspend fun load(): Data` | A method with an extra `Continuation` parameter | Expose a `CompletableFuture` or callback wrapper instead |
| `@JvmInline value class Id(val v: String)` | Mangled function names, the raw type in signatures | Avoid value classes on the Java-facing API surface |
| `fun f(vararg xs: String)` | `f(String...)` | — (works, but a spread from Kotlin copies the array) |
| Sealed hierarchy | Ordinary classes; no exhaustiveness | Document the contract; Java has no equivalent guarantee |

- Named arguments do not exist in Java: an API designed around long default-argument lists is hostile to Java callers. Provide a builder or `@JvmOverloads`.
- Kotlin's `List` is `java.util.List` at runtime, so a Java caller can mutate what Kotlin declared read-only. Return a defensive copy across a public Java-facing boundary.
- `Unit`-returning functions are `void` from Java; a lambda parameter typed `() -> Unit` arrives as `Function0<Unit>` and requires `return Unit.INSTANCE;` unless you declare a Java-friendly SAM interface.
- Generic variance leaks: `List<out T>` shows up as `List<? extends T>` in Java signatures. `@JvmSuppressWildcards` removes the wildcard when it makes the API unusable; `@JvmWildcard` forces it.

## Kotlin Calling Java

- Platform types (`String!`) insert no null check — the crash happens at first use, far from the call. Treat unannotated returns as nullable (SKILL.md rule 1).
- SAM conversion works for Java interfaces (`executor.execute { }`), and for Kotlin interfaces only when declared `fun interface`.
- Java `static` members are called on the class; a Java field is a Kotlin property (`point.x`), including for public mutable fields.
- Java getters/setters become synthetic properties: `calendar.firstDayOfWeek = MONDAY`. This works only for the Java bean pattern, not for `getFoo(int)`.
- Java's checked exceptions vanish: nothing forces you to catch `IOException`. Every Java call that declares one is an unmarked failure point — the compiler will not remind you.
- `Array<String>` maps to `String[]`; `IntArray` to `int[]`, not `Integer[]`. A Java API taking `Integer[]` needs `Array<Int>`.
- `Class` vs `KClass`: `Foo::class.java` for Java APIs, `.kotlin` for the reverse.
- Java's `Optional<T>` should stop at the boundary: convert to `T?` immediately rather than propagating a second null-representation through Kotlin code.
- Synchronization: `@Synchronized` on a function, `synchronized(lock) { }` for a block — but not around suspending code (SKILL.md Concurrency Primitive Selection).

## Semantics That Differ From Java

- `==` is `equals` and `===` is identity — the reverse of the Java reflex (SKILL.md Equality, Copy, And Identity).
- Everything is final by default; `open` is required for inheritance and for most mocking and proxying frameworks (Spring, JPA, Mockito).
- No implicit widening: `int` → `long` needs `toLong()`. And `Int.MAX_VALUE + 1` wraps silently, exactly as in Java.
- Integer division truncates (`5 / 2 == 2`); write `5.0 / 2` or `toDouble()`.
- `String` templates instead of concatenation, and `equals` for comparison — `==` on strings is structural in Kotlin, so the classic Java `==`-on-strings bug does not exist here.
- No ternary: `if (c) a else b` is an expression. No `switch` fallthrough: `when` branches never fall through.
- Static initialization: `object` initializes lazily on first access, unlike a Java `static` block that runs at class load.

## Migrating A Java Codebase

Order the work so that each step is independently shippable:

1. **Annotate first, convert later.** Add `@Nullable`/`@NonNull` (or JSpecify `@NullMarked`) to the Java API surface you are about to consume. Every annotation removes a platform type from the future Kotlin code, before any Kotlin exists.
2. **Convert leaves first.** Model and utility classes with few dependents. Never start with the class everything imports.
3. **One file per commit**, with tests green in between. Mixed Java/Kotlin modules compile fine — there is no big-bang step and no reason to invent one.
4. **Clean up the converter's output.** The IDE converter is a starting point, not a result. Its signature smells: `!!` everywhere, every property `var` and nullable, `lateinit` where the constructor could assign, Java-style loops instead of collection operators, `Companion` clutter for what should be top-level functions.
5. **Re-model, don't transliterate.** Builders become default arguments; a class with getters and setters becomes a `data class`; a `Result` class with `isSuccess`/`getError` becomes a sealed hierarchy; a listener interface becomes a `Flow` or a lambda parameter.
6. **Turn on strictness once the module is Kotlin**: `-Xjsr305=strict`, warnings as errors, and explicit API mode for library modules.
7. **Keep the Java-facing API stable** while callers are still Java: `@JvmOverloads`, `@JvmStatic` and `@Throws` on anything they call, so conversion is invisible from their side.

## Review Checklist For A Mixed Module

- Every Java type consumed by new Kotlin is either annotated or received as nullable.
- Every Kotlin function Java calls has the `@Jvm*` annotations it needs, and `@Throws` where the Java caller must catch.
- No `internal` member relied on from Java (it is reachable, mangled, and unsupported).
- No public API built on default arguments while Java callers remain.
- Converted files re-modelled, not transliterated: no `!!` walls, no all-`var` data holders.
