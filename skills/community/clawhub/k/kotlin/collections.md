# Collections — Choice, Cost, And Mutation

Kotlin's collection API is pleasant enough that people stop thinking about allocation and complexity. Two habits cause most of the damage: chaining eager operators over large inputs, and doing membership tests against a `List`.

## Choosing The Type

| Need | Type | Note |
|---|---|---|
| Ordered, index access | `List` / `ArrayList` | Default; `get` O(1), `contains` O(n) |
| Membership tests | `Set` (`setOf` gives a `LinkedHashSet`) | `contains` O(1), insertion order preserved |
| Key → value | `Map` (`mapOf` gives a `LinkedHashMap`) | Ordered by insertion; `HashMap()` when order is irrelevant |
| Sorted iteration or range queries | `sortedMapOf` / `sortedSetOf` | O(log n) operations, iteration in key order |
| Numeric bulk data | `IntArray`, `LongArray`, `DoubleArray` | No boxing; `List<Int>` boxes every element |
| A fixed set of constants | `enum` with `EnumMap`/`EnumSet` (JVM) | Array-backed, no hashing |
| Queue or stack | `ArrayDeque` | Both ends O(1); `List.removeAt(0)` is O(n) |
| Concurrent access | `ConcurrentHashMap` (JVM), or confinement to one coroutine | Stdlib collections are not thread-safe |

## Read-Only Is Not Immutable

- `listOf`, `mapOf`, `setOf` return read-only *interfaces*. The underlying object may be mutable, and a `MutableList` upcast to `List` is still mutated by whoever kept the original reference.
- On the JVM, `List` is `java.util.List` at runtime: Java code can call `add` on your read-only list, and a list handed to Kotlin from Java can change under you between two reads.
- Defensive copy at the boundary: `toList()`, `toMap()`, `toSet()` allocate a snapshot. `Collections.unmodifiableList` fails loudly on write instead of silently sharing.
- Genuine immutability with structural sharing comes from `kotlinx.collections.immutable` (`persistentListOf`, `ImmutableList`) — also the fix for the UI-stability warnings that make a screen recompose on every state change.
- Exposing state: keep the `MutableStateFlow<List<T>>` private and expose the read-only type. The copy per update is the price of callers not mutating your state.

## Operator Cost

- Every eager operator allocates a new list. `list.map { }.filter { }.map { }` over 10 000 elements allocates three intermediate lists of up to 10 000 entries — 30 000 references created to be discarded.
- `asSequence()` makes the chain lazy: one pass, one output allocation, and short-circuit terminals stop early. `list.asSequence().filter(p).first()` stops at the first match; `list.filter(p).first()` filters all 10 000 elements before taking one.
- The crossover is workload-dependent, not a constant: a sequence pays an iterator and lambda indirection per element per operator, so for a handful of elements and one or two operators the eager list wins. Convert when the chain is long, the input is large, or the terminal short-circuits — and measure before claiming the win.
- Sequences from the `sequence { }` builder and from `Iterator.asSequence()` are single-use: consuming one twice throws `IllegalStateException`.
- `count()` on a `Collection` is O(1) (it reads `size`); `count { predicate }`, and `count()` on a `Sequence`, are O(n).
- `first()`, `last()`, `single()`, `max()`, `reduce()` throw on empty and each has an `…OrNull` variant. `single()` also throws when there is more than one element — that is the point, and why it beats `first()` when the invariant matters.
- `sumOf { }` picks its overload from the lambda's return type: `sumOf { it.priceCents }` over `Int` overflows past 2^31 − 1; return a `Long` from the lambda.

## The O(n²) Shapes

- `for (x in a) if (b.contains(x))` with `b` a `List` is O(n·m). One `val set = b.toSet()` outside the loop makes it O(n+m).
- `list.filter { it.id in other.map { o -> o.id } }` rebuilds the inner list for every element. Hoist it: `val ids = other.mapTo(HashSet()) { it.id }`.
- `list.removeAt(0)` in a loop is O(n²); `ArrayDeque.removeFirst()` is O(1).
- `+=` on a `String` inside a loop allocates a new string per iteration; `buildString { append(…) }` allocates one buffer.
- `groupBy { }` followed by `mapValues { it.value.size }` materializes every group; `groupingBy { }.eachCount()` counts without building the lists.

## Grouping And Aggregation

| Goal | Call |
|---|---|
| Key → all matching elements | `groupBy { it.type }` |
| Key → one element (last wins) | `associateBy { it.id }` |
| Element → computed value | `associateWith { compute(it) }` |
| Key → count | `groupingBy { it.type }.eachCount()` |
| Key → folded aggregate | `groupingBy { }.fold(initial) { acc, e -> … }` |
| Split by predicate | `partition { it.isValid }` → `Pair<List, List>` |
| Flatten nested collections | `flatMap { it.children }` |
| Pairwise or sliding window | `zipWithNext()`, `windowed(size, step)` |
| Fixed-size batches | `chunked(500)` — the shape for batched network or DB writes |

`associateBy` keeps the last entry for a duplicate key without a word. When duplicates are a data error, `groupBy` and assert every group has size 1.

## Data Classes

- Generated `equals`, `hashCode`, `copy`, `toString` cover the constructor properties only (SKILL.md rule 8) — a body property is invisible to all four.
- `copy()` is shallow: the copy shares every mutable object the original referenced, so `copy()` on a state holding a `MutableList` gives two objects with one list.
- `toString()` prints every property, including tokens, passwords and personal data — override it on anything that reaches a log.
- Destructuring is positional: `val (a, b) = point`. Reordering the constructor parameters compiles fine and silently swaps the values at every destructuring site. Do not destructure types you do not own.
- A `data class` with an `Array` property compares by reference; use `List`, or hand-write `equals`/`hashCode` with `contentEquals`/`contentHashCode`.
- `data class` is the wrong model for an entity with identity (a database row): identity is the id, not the field values.
- Adding a parameter to a `data class` is a source-compatible change but a binary-incompatible one for its generated `copy` — it matters for published libraries, not for app code.

## Sorting And Ordering

- `sortedBy` returns a new list; `sortBy` sorts a `MutableList` in place. One letter, two different programs.
- Multi-key: `sortedWith(compareBy({ it.lastName }, { it.firstName }))`, with `thenByDescending` for mixed directions.
- Nulls need an explicit position: `compareBy(nullsLast()) { it.date }`.
- Sorting is stable, so a later sort preserves the earlier order within ties — chain by sorting on the least significant key first.
- `sortedBy { it.name }` is lexicographic and locale-blind; user-visible lists want a `Collator`.
- Comparators over `Double` use total order (`NaN` last, `-0.0` before `0.0`), unlike `==` on primitive doubles (SKILL.md Equality, Copy, And Identity).

## Mutation Traps

- `ConcurrentModificationException` comes from mutating while iterating: use `removeAll { predicate }`, the iterator's own `remove()`, or iterate a copy.
- `getOrPut(key) { expensive() }` runs the lambda only on a miss, but it is not atomic; on a `ConcurrentHashMap` use `computeIfAbsent`.
- `+=` on `var list: List<T>` allocates a new list every time; on `val list: MutableList<T>` it appends in place. Same operator, different complexity class.
- `withIndex()` when you need index and value; `indices` when you need only the range; a manual index `var` in neither case.

## Review Checklist

- No `contains`/`in` against a `List` inside a loop.
- Chains over large inputs are either sequences or justified by a measurement.
- Public API exposes read-only types and returns copies of anything mutable it keeps.
- No `first()`/`max()`/`reduce()` where the collection can legitimately be empty.
- Numeric bulk data in primitive arrays, not `List<Int>`.
- No `toString()` on a data class that carries secrets into logs.
