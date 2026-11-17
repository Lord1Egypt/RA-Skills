# Performance — Allocation, Boxing, And What Inlining Really Costs

Kotlin's abstractions are mostly free, with a short list of exceptions that are invisible in source and obvious in bytecode. Measure first: the rules below tell you where to look, not what to rewrite on sight.

## Where The Cost Hides

| Source construct | Hidden cost | When it matters |
|---|---|---|
| `List<Int>`, `Map<String, Int>` | Every element boxed into `Integer` | Thousands of elements, or a hot loop |
| `Int?`, generic `T` holding a number | Boxed even for a single value | Per-frame or per-request code |
| Non-inline lambda parameter | One `Function` object per call, plus captures | Called in a loop |
| `vararg` call | Array allocation per call, twice with a spread (`*arr`) | Logging helpers on a hot path |
| Delegated property (`by`) | One delegate object per property per instance | Classes with many delegates, created often |
| `data class copy()` | A new instance plus its property copies | State updates per frame |
| Eager collection chain | One intermediate list per operator | Large inputs |
| String `+=` in a loop | A new `String` per iteration | Any loop over more than a few items |
| Exception throw | Stack trace capture | Exception-driven parsing or control flow |
| `kotlin-reflect` call | Slow lookup, large artifact | Anything per-request; any Android build |

## Boxing And Primitives

- Generics on the JVM cannot hold primitives: `List<Int>` is a list of `Integer`. Use `IntArray`/`LongArray`/`DoubleArray` for bulk numeric data, and primitive-specialized loops (`for (i in 0 until n)` over an `IntArray`) for hot code.
- Small `Int` values may come from a cache and compare equal by identity, larger ones do not — never use `===` on boxed numbers, and be aware that `Int?` comparisons go through `equals`.
- `@JvmInline value class` erases to its underlying type in most positions, *but boxes* when it is nullable, when it is a generic argument, when it is used through an implemented interface, or when it appears in an array. A `value class Id(val v: Long)` in a `List<Id>` is boxed twice over.
- Value-class functions get mangled JVM names, which is why they are a poor fit on a Java-facing API surface.
- `Sequence<Int>` boxes at every step; a primitive array loop does not. Sequences are a memory-shape optimization, not a numeric one.

## Inlining

- `inline` removes the lambda object and enables non-local returns — that is why `forEach`, `let`, `use` and `withLock` cost nothing over a hand-written loop.
- The cost is bytecode duplication at every call site. A large inline function inflates the artifact, slows compilation, and can hurt instruction-cache locality; the compiler warns when a function has no lambda parameter precisely because there is nothing to gain.
- `noinline` for a lambda you need to store; `crossinline` when the lambda runs in another context. Both are correctness tools, not performance knobs.
- Public inline functions bake their body into consumers: changing one has no effect until consumers recompile — a real constraint for libraries, irrelevant inside an app.
- `crossinline`/`noinline` on a hot path force the allocation you were trying to avoid; if the lambda must be stored, accept the object and stop calling the function inline.

## Collections And Sequences

- One eager operator = one new list. A three-operator chain over 10 000 elements allocates three lists of up to 10 000 references.
- `asSequence()` collapses the chain into one pass with one output allocation, and short-circuits: `asSequence().filter(p).first()` stops at the first match.
- The crossover depends on element count, operator count and lambda cost; for a few elements and one operator the eager list wins because a sequence pays iterator indirection per element per stage. Convert on measurement, not on principle.
- Pre-size when the result size is known: `ArrayList(expectedSize)`, `HashMap(expectedSize)`, or `mapTo(ArrayList(n))` — growth means repeated array copies.
- `contains` on a `List` is O(n): convert to a `Set` once outside the loop.

## Coroutines

- A coroutine costs far less than a thread — the cheap part is suspension, not creation of thousands of jobs with their contexts. Launching one coroutine per list element to do microsecond work is overhead, not parallelism.
- `withContext` on the same dispatcher still allocates and schedules; wrap the boundary where the work changes nature, not every function.
- `Dispatchers.Default` has parallelism equal to CPU cores: CPU-bound work already saturates it, and adding coroutines only adds scheduling.
- `flow` operators allocate per stage; `conflate`/`buffer` add a channel. Fine per user event, worth reviewing per sensor sample.
- Cancellation cost is negligible compared to work that keeps running because it never checked (SKILL.md rule 4).

## Android-Specific

- Allocation in a per-frame path (composition, `onDraw`, scroll listeners) feeds the GC and shows up as jank, not as CPU time. Hoist allocations out of those callbacks.
- R8 shrinks and optimizes release builds: the honest way to size an artifact or benchmark code is a release build with R8 on, never a debug build.
- Baseline profiles turn interpreted startup code into AOT-compiled code; startup and scroll benchmarks (macrobenchmark) measure it, guesses do not.
- Reflection-based libraries need keep rules and defeat shrinking on the classes they touch — a real size and startup cost, and the reason codegen alternatives exist.

## Measuring

- JVM: JMH (or kotlinx-benchmark for multiplatform) with warmup, because the JIT makes the first thousand iterations meaningless. A microbenchmark written as a `for` loop with `System.nanoTime()` measures the JIT, not the code.
- Allocation profiling beats CPU profiling for Kotlin-idiomatic code: the usual finding is garbage, not compute.
- Android: macrobenchmark for startup/scroll, the profiler's allocation tracker for the rest, and the compose recomposition counts for UI.
- Decompiling (Tools → Kotlin → Show Kotlin Bytecode → Decompile) settles every "does this allocate" argument in about a minute.
- Report ranges, not single numbers, and re-measure after R8 — a difference that disappears in a release build was never a difference.

## Review Checklist

- No boxing of primitives in bulk data or hot loops.
- No collection chain over a large input without a measurement or a sequence.
- No allocation inside per-frame or per-request inner loops.
- Value classes kept out of generic, nullable and array positions where they box.
- Every performance claim in a review backed by a benchmark or by bytecode, not by intuition.
