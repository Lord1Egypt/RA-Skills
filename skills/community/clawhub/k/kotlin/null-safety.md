# Null Safety — Where Null Still Gets In

The type system stops null inside Kotlin-only code. Every NPE in a Kotlin codebase therefore comes from a boundary or from an escape hatch: Java, reflection, initialization order, or `!!`. Diagnose in that order.

## Symptom → Cause

| Symptom | Cause | Fix |
|---|---|---|
| `NullPointerException` on a non-null property, no `!!` in the stack | Reflection-based JSON, an ORM, or Java put null into it | Validate at the boundary: nullable DTO → mapper → non-null domain type |
| `NullPointerException: … must not be null` at a `!!` | The asserted value was null | Decision order in SKILL.md rule 2 |
| "lateinit property X has not been initialized" | Read before assignment, or assignment happens on only one of several entry paths | Nullable + `?:`, or move initialization into the constructor |
| "Smart cast to 'String' is impossible" | `var`, `open val`, custom getter, or a property from another module | Copy into a local `val` first |
| NPE inside a superclass constructor | An open member ran during base construction, before the subclass fields existed | Never call open members from a constructor or an initializer |
| Java method returned null though its signature said `String` | Platform type `String!` — no check was inserted | Annotate the Java side, or receive it as `String?` |
| NPE on a generated view binding after navigation | The binding outlived the view | Null the binding field in the destroy callback |

## Platform Types

- A Java type with no nullability annotation arrives as `String!`: Kotlin inserts no check, so the NPE fires at the first *use*, often far from the call that produced it.
- `-Xjsr305=strict` promotes JSR-305 annotations (`javax.annotation.Nonnull` and friends) on Java dependencies into real Kotlin types — and only those. JSpecify is a separate switch: type-enhancement strict mode via `-Xjspecify-annotations=strict`, and strict by default from Kotlin >=2.1. Set both for new code; on legacy code expect a wave of errors that are all genuine, because annotated libraries then fail to compile exactly where you were silently unsafe.
- Annotating your own Java sources (`@Nullable`/`@NonNull`, or JSpecify `@NullMarked` at package level) is the highest-leverage migration step: it turns runtime NPEs into compile errors for every Kotlin caller, with no Kotlin written.
- Rule of thumb for unannotated third-party Java: every returned reference is nullable, every parameter is non-null-required, until the source says otherwise.
- Framework callbacks that hand you `Bundle?`, `Intent?` or `View?` are stating real nullability, not being defensive — the null case happens on recreation paths you cannot reproduce by hand.

## lateinit, lazy, Nullable

| | `lateinit var` | `by lazy` | `T?` |
|---|---|---|---|
| Init timing | Any time before first read | First read | Any |
| Thread safety | None | SYNCHRONIZED by default | N/A |
| Primitives | Not supported | Supported | Supported |
| Null as a value | Not supported | Supported | Yes |
| Failure mode | `UninitializedPropertyAccessException`, names the property | The initializer's exception, re-thrown on later reads | None; the caller decides |
| Guard | `this::prop.isInitialized` | Not needed | `!= null` |

- `by lazy(LazyThreadSafetyMode.NONE)` drops the synchronization for single-thread confinement — worth it only in a measured hot path.
- `isInitialized` appearing outside the declaring class means `lateinit` was the wrong model: the value is optional, so declare it nullable and let callers see that.

## Operators, Precisely

- `?.` short-circuits the whole chain: `a?.b?.c` is one check per link, and the result is nullable even when `c` is not.
- `?:` takes the right side whenever the left is null — including when the left is a `let` block that itself returned null. That is the most common false-fallback bug (SKILL.md Traps).
- `?.let {}` runs only for non-null, but its result is nullable; a trailing `?: default` is only safe when the block cannot return null.
- `a!!.b!!.c` reports a line, not which link was null. Split it, or use `requireNotNull(x) { "…" }` per link so the message names the field.
- `as?` is the safe cast — null instead of `ClassCastException`. `val f = x as? Foo ?: return` is the idiomatic guard.
- `?.also {}` for a null-tolerant side effect; `?.run {}` when you want the receiver implicit and a result back.

## Standard-Library Helpers That Remove `!!`

| Instead of | Write |
|---|---|
| `if (s != null && s.isNotEmpty())` | `if (!s.isNullOrEmpty())` |
| `list.filter { it != null }.map { it!! }` | `list.filterNotNull()` |
| `list.map { transform(it) }.filterNotNull()` | `list.mapNotNull { transform(it) }` |
| `map[key]!!` | `map.getValue(key)` — throws with the key in the message — or `map[key] ?: default` |
| `s?.let { it } ?: ""` | `s.orEmpty()` (also on `List?`, `Map?`, `Array?`) |
| `if (x != null) f(x)` guard chains | `x?.let(::f)`, or an early `?: return` |
| A nullable accumulated in a `var` | `buildList` / `buildMap` with conditional `add`/`put` |

## Initialization Order

Execution order is: primary-constructor property initializers and `init` blocks interleaved top to bottom, then the secondary constructor body.

- A property whose initializer reads a property declared *below* it sees the default (null / 0) even though both are non-null types. The compiler catches the direct reference; it does not catch it through a function call.
- An `open` member invoked from a constructor or initializer runs the *subclass* override while the subclass's own properties are still unset, so a non-null `val` reads as null there. Use an explicit `initialize()` called after construction.
- A `by lazy` property read from an `init` block defeats the point: it forces the computation during construction, in whatever thread built the object.

## Nullability And Generics

- Unbounded `T` includes nullable types: in `fun <T> id(x: T): T`, `T` can be `String?`. Constrain with `<T : Any>` to reject null at the call site.
- `T?` where `T` is already nullable is still a single level of nullability — there is no double null.
- `Map<K, V>[key]` returns `V?`; with a nullable `V` you cannot tell "absent" from "present and null" — use `containsKey`, or `getOrElse` with a sentinel.
- Overriding a Java method with a platform-typed parameter lets you *choose* the nullability. Choosing non-null makes the compiler insert a check that throws on the Java caller's null — correct when null is a bug, a new crash when the Java side treated null as "not provided".

## Review Checklist

- Every `!!` names the invariant in a comment, or is replaced per SKILL.md rule 2.
- Types crossing a network or database boundary declare nullable fields unless the format guarantees presence.
- No `open` member invoked from a constructor or an initializer.
- `lateinit` only where exactly one code path sets the value before any read.
- Public library functions reject null with `require`, not with the platform check's anonymous message.
