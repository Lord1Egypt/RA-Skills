# Incremental Java to Kotlin migration

Load this when planning or doing a Java-to-Kotlin conversion in an Android codebase. The goal is a
codebase that builds and ships at every step, not a big-bang rewrite.

## Order of work

1. Make the module build Kotlin: the Kotlin Android plugin, or the built-in Kotlin support of newer AGP
   versions. Versions go in `libs.versions.toml`.
2. Move annotation processors that Kotlin classes will need (Room, Hilt, Glide) from `annotationProcessor`
   to KSP. Java-only `annotationProcessor` does not see Kotlin sources.
3. Annotate nullability in the Java code first (`@NullMarked` per package, `@Nullable` where needed).
   The converter then produces correct nullable types instead of guesses.
4. Write or extend tests around the class being converted, if they are missing.
5. Convert in this order:
   - Tests (low risk, fast feedback on Kotlin setup).
   - Leaf classes: models, mappers, utilities with no Android dependencies.
   - Repositories and data sources.
   - ViewModels.
   - Activities, Fragments and adapters last, usually together with a move to Compose or a rewrite of the screen.
6. One class or small cluster per merge request. Conversion commit separate from cleanup and behaviour changes.

Do not convert code that is scheduled for deletion, or a large class nobody can test.

## Converting a file

1. Use the IDE converter ("Convert Java File to Kotlin File" in the Code menu).
2. Build and run tests before touching anything else. Commit.
3. Clean up in a second commit, using the list below.

## Cleanup after the converter

| Converter output | Replace with |
|---|---|
| `!!` everywhere | Correct nullable types, `?.`, `?:`, `requireNotNull(x) { "reason" }` |
| `lateinit var` for constructor-provided values | `val` constructor properties |
| `var` fields that never change | `val` |
| Getter / setter pairs | Properties |
| `companion object` with only constants | Top-level `const val` or `private const val` |
| Static utility class turned into `object` | Top-level functions or extension functions |
| Java-style builders | Default and named arguments; delete the builder |
| `equals` / `hashCode` / `toString` written by hand | `data class` (when all fields are part of identity) |
| Listener interfaces with one method | `fun interface` or function types |
| `Executor` + callback code | `suspend` functions and `Flow` (only once callers are Kotlin) |
| `if (x != null) { x.foo() }` | `x?.foo()` or smart casts |

Behaviour to double-check after conversion:

- `==` in Kotlin calls `equals`. Java `==` on objects compared references.
- Integer division, `Long` / `Int` literals and overflow in arithmetic the converter rewrote.
- `when` without `else` over a Java enum or int constant.
- Platform types from remaining Java code (`String!`) that the converter treated as non-null.

## Keeping Java callers working

```kotlin
// Static access from Java: DeviceIds.parse(...) instead of DeviceIds.Companion.parse(...)
class DeviceIds {
    companion object {
        @JvmStatic fun parse(raw: String): DeviceId? = ...
        const val PREFIX = "dev-"         // primitives and String: const val
        @JvmField val DEFAULT_TAGS = listOf("new") // other types: @JvmField exposes a field
    }
}

// Default arguments: Java sees only the full signature without @JvmOverloads
class ScanSpec @JvmOverloads constructor(
    val timeoutMs: Long = 10_000,
    val lowLatency: Boolean = false,
)

// Checked exceptions Java callers must catch
@Throws(IOException::class)
fun readConfig(file: File): Config = ...
```

```kotlin
// Bytes.kt: name the class generated for top-level functions (must precede the package line)
@file:JvmName("Bytes")

package com.example.ble

fun ByteArray.toHex(): String = joinToString("") { "%02x".format(it) } // Java: Bytes.toHex(array)
```

- Callbacks for Java callers: `fun interface` instead of Kotlin function types. A Java lambda for
  `(String) -> Unit` must `return Unit.INSTANCE`.
- `suspend` functions are awkward from Java. While Java callers remain, add a Java-facing wrapper that
  returns a `Future` or takes a callback, and delete it with the last Java caller.
- `internal` members get mangled names in Java. Do not rely on calling them from Java.
- `object` singletons are `Foo.INSTANCE` from Java; `@JvmStatic` on their members avoids that.
- Sealed classes and `data class` work from Java, but Java callers do not get Kotlin's exhaustive `when`
  checks. Java branches over them end with a default that throws.

## Java code that Kotlin calls

- Every public signature carries nullability: JSpecify `@NullMarked` packages or AndroidX `@Nullable`
  / `@NonNull`. Without them Kotlin sees platform types and null checks disappear.
- Getters and setters named `getX` / `setX` / `isX` appear as properties in Kotlin.
- Java `List` returns are seen as `(Mutable)List` in Kotlin; return unmodifiable collections so Kotlin's
  read-only view is honest.
- Lombok-generated members are not visible to Kotlin in the same module without the Kotlin Lombok compiler
  plugin. Delombok or convert Lombok classes early.

## Tracking progress

- Measure the Java / Kotlin line ratio per module, not repo-wide, and convert module by module so a module
  can eventually drop Java-specific setup.
- Lint and detekt or ktlint run on converted files from the first commit, so style debt does not accumulate.
- Avoid long-lived migration branches. Small merges to the main line keep conflicts manageable.
