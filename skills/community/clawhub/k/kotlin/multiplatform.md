# Multiplatform — Source Sets, expect/actual, And The Swift Boundary

KMP shares logic, not platform APIs. The two recurring problems are deciding what belongs in common code, and everything that happens when Kotlin becomes an Objective-C framework that Swift consumes.

## Source Sets

- `commonMain` sees only the Kotlin stdlib and multiplatform libraries. Nothing from `java.*`, no `java.time`, no Android framework, no `System.currentTimeMillis()`.
- Platform source sets (`androidMain`, `iosMain`, `jvmMain`, `jsMain`, `wasmJsMain`) can use everything their platform offers and everything in `commonMain`. Dependencies flow one way: common → platform.
- The default hierarchy template gives intermediate sets (`appleMain`, `nativeMain`) for free — write an `actual` once for all Apple targets instead of three times.
- `commonTest` runs on every target; a test that passes on JVM and fails on iOS is usually a threading or a date/locale assumption.
- Multiplatform replacements for JVM habits: `kotlinx-datetime` for time, `kotlinx-io`/Okio for files, Ktor client for HTTP, `kotlinx.serialization` for JSON, `kotlinx.atomicfu` for atomics, SQLDelight for storage.

## expect / actual

- `expect` declares the shape in common code; every target must provide an `actual`, or the build fails — that is the guarantee it buys.
- `actual typealias PlatformFile = java.io.File` is the cheapest form when a platform type already matches the expected shape.
- Expected classes with default implementations exist but are still constrained; a plain interface in common code plus a platform factory is easier to evolve and easier to fake in tests.
- Prefer dependency injection over `expect/actual` for anything with more than one implementation per platform: `expect` is a compile-time singleton, so it cannot be swapped in a test.
- Keep the expected surface small. Every `expect` is a function that must be written, tested and kept consistent on every target; the shared logic above it is the actual value of KMP.

## The iOS / Swift Boundary

- Kotlin compiles to an Objective-C framework, so the API Swift sees passes through ObjC's type system. What is lost on the way:
  - Generics on classes are erased to `id`-like types in many positions; generic constraints do not survive.
  - Sealed hierarchies arrive as plain classes: Swift gets no exhaustive `switch`.
  - Default arguments disappear — Swift sees one function requiring every parameter.
  - Overloads by parameter type get mangled names (`doThing(x:)`, `doThingX:`), so overloading is hostile to Swift callers.
  - `Int`/`Long` become `KotlinInt`/`KotlinLong` boxed types in generic positions (inside `List`, `Map`, optionals).
- `suspend` functions are exposed to Swift as completion handlers (and async/await via Swift concurrency); `Flow` is *not* exposed usefully — wrap it in a callback-based class in `iosMain`, or use a bridging tool that generates one.
- Exceptions do not cross the boundary as errors unless the function is annotated `@Throws(...)`; an unannotated Kotlin exception crashes the iOS app instead of surfacing as an `NSError`.
- Design the shared API for Swift explicitly: a small facade in `commonMain` with no generics, no default arguments, no overloads and no sealed types on its surface costs a day and saves the iOS team a permanent tax.
- The new Kotlin/Native memory manager (default since Kotlin 1.7.20) removed the object-freezing model: objects can be shared across threads, and the old `freeze()`/`InvalidMutabilityException` advice found in older articles no longer applies.

## Concurrency Across Targets

- Coroutines work on every target, with real multithreading on Native since the new memory manager.
- `Dispatchers.Default` and `Dispatchers.Main` exist everywhere; `Dispatchers.IO` is JVM/Android and Native only, so common code cannot name it — inject the dispatcher from the platform side.
- JS and Wasm are single-threaded: any assumption of parallelism in common code breaks there, and `runBlocking` does not exist on those targets.
- Test the common code with `runTest` rather than `runBlocking` — `runBlocking` is unavailable on JS/Wasm, so a common test written with it will not compile for those targets.
- Platform-specific main dispatchers need their artifacts (`kotlinx-coroutines-android` and the Native/Swift main queue integration); a missing one shows up as "Module with the Main dispatcher is missing".

## Sharing Strategy

| Layer | Share? |
|---|---|
| Domain model, validation, business rules | Yes — the highest-value, lowest-risk share |
| Networking and serialization | Yes, with Ktor client + kotlinx.serialization |
| Persistence | Yes with SQLDelight; no if each platform already has a native store the team trusts |
| Presentation state (state holders, reducers) | Often — the argument is whether each platform wants idiomatic navigation |
| UI | Only with Compose Multiplatform, and only where a non-native look is acceptable; iOS teams frequently reject it |
| Platform integrations (permissions, biometrics, push) | No — thin `expect`/DI wrappers over native implementations |

Start from the bottom of that list and stop where the cost exceeds the sharing benefit. A KMP project that shares only the domain and networking layers is a normal, successful outcome.

## Build And Publishing

- The framework's binary is configured in the Gradle multiplatform block (`baseName`, `isStatic`, `export(...)` for transitive API types). A type from a dependency that appears in your public API must be exported, or Swift cannot name it.
- Consumption on iOS: CocoaPods integration, SPM through a published XCFramework, or a directly built framework. Choose one and script it — a manual framework copy step breaks whenever the shared module changes.
- Build times are the hidden cost: linking a Native framework is slow, and CI needs a macOS runner for the Apple targets.
- Publishing a KMP library publishes one root module plus one per target; consumers resolve their variant through Gradle metadata, which means Maven-only consumers cannot use it.

## Review Checklist

- Nothing platform-specific in `commonMain`, including implicit locale, timezone and file-path assumptions.
- Every `expect` justified against a plain interface plus injection.
- The Swift-facing surface free of generics, default arguments, overloads and sealed types; `@Throws` wherever iOS must handle an error.
- Flows wrapped for Swift, not exposed raw.
- Common tests use `runTest`, and no common code assumes threads.
