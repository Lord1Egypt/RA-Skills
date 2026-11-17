# Slices, Arrays, and Maps

A slice is a three-word header — pointer, len, cap — over an array someone else may also be holding. Every slice surprise comes from that sharing. Maps are simpler and have exactly four rules worth memorizing.

## Slice Aliasing

```go
a := []int{0, 1, 2, 3, 4}
b := a[1:3]        // len 2, cap 4  →  cap(a[i:j]) == cap(a) - i
b = append(b, 99)  // writes into a[3]: a is now [0 1 2 99 4]
```

- `append` writes in place whenever `len < cap`, and reallocates otherwise. Whether the caller sees your append is therefore a function of capacity — the same code silently changes behavior when the input grows.
- The three-index form `a[1:3:3]` sets `cap = len`, so the next `append` must allocate. Use it whenever you hand a sub-slice to code you do not control.
- Passing a slice to a function copies the header, not the data: element writes are visible to the caller, but `append` inside the function is not — the callee's new header is discarded. Return the slice or take a `*[]T`.
- A small sub-slice keeps the **entire** backing array alive. Holding `bigBuf[:10]` from a 10 MB read retains all 10 MB. Copy the piece out when the parent is large (`memory.md`).

## Growth and Preallocation

- Growth is roughly: below ~256 elements the capacity doubles; above that it grows by a smaller factor (about 1.25×, adjusted so growth stays smooth), then is rounded up to a size class. Never depend on an exact number — depend on the fact that appending N items without preallocation performs O(log N) copies and allocates O(N) total bytes more than once.
- When the final length is known: `s := make([]T, 0, n)` then append. The `0` matters — `make([]T, n)` gives n zero values and your appends land after them, the single most common preallocation bug.
- `copy(dst, src)` copies `min(len(dst), len(src))` elements and never grows `dst`. `copy(make([]T, 0, n), src)` copies nothing.
- Full copy: `out := append([]T(nil), src...)` or `slices.Clone(src)` (`go >=1.21`). Both are shallow — a `[]*User` clone shares every user.

## Nil vs Empty

| | `var s []T` (nil) | `s := []T{}` (empty) |
|---|---|---|
| `len`, `cap`, `range`, `append` | Work identically | Work identically |
| `s == nil` | true | false |
| JSON encoding | `null` | `[]` |
| Allocation | none | one (for the zero-size header target) |

Prefer nil as the zero value; the only reason to write `[]T{}` is a JSON contract that requires `[]`, and the honest fix for that is `omitempty` plus a documented shape (`json.md`).

## Deleting and Filtering

```go
s = append(s[:i], s[i+1:]...)   // remove index i, order preserved, O(n)
s[i] = s[len(s)-1]; s = s[:len(s)-1]   // O(1), order destroyed
```

- Both leave the removed element's value in the freed tail. With pointer or pointer-containing elements that is a leak: zero the tail (`s[len(s)] = nil` before reslicing) or use `slices.Delete`, which does it for you (`go >=1.21`).
- Filter in place without allocating: `out := s[:0]; for _, v := range s { if keep(v) { out = append(out, v) } }; s = out`. Safe because writes never overtake reads.
- Never remove elements from the slice you are ranging over by index arithmetic — iterate backwards, or build a new slice.
- `clear(s)` (`go >=1.21`) zeros every element and keeps `len`. To empty a slice for reuse, `s = s[:0]` keeps the capacity; `s = nil` releases the array.

## The slices Package (`go >=1.21`)

`slices.Contains`, `Index`, `Sort`, `SortFunc`, `SortStableFunc`, `BinarySearch`, `Clone`, `Compact`, `Equal`, `Reverse`, `Max`, `Min`, `Insert`, `Delete`.

- `slices.Sort` beats `sort.Slice` for ordered types: no interface boxing, no closure call per comparison.
- Migration trap: `sort.Slice` takes a `less(i, j) bool` over **indices**; `slices.SortFunc` takes a `cmp(a, b) int` over **values** returning negative/zero/positive. Copying the old body into the new signature compiles when the types line up and produces a wrong order. Use `cmp.Compare(a.X, b.X)`.
- `slices.BinarySearch` requires the slice already sorted by the same order; on unsorted input it returns a plausible wrong answer, never an error.
- `slices.Compact` removes *consecutive* duplicates only — sort first, or it does almost nothing.

## Maps

- Reading a missing key returns the zero value; use comma-ok when zero is a legal value: `v, ok := m[k]`.
- **Writing to a nil map panics.** Reading a nil map does not. A struct field of map type is nil until the constructor makes it — the most common source of `assignment to entry in nil map`.
- **Iteration order is deliberately randomized** on every range — a two-element map really does re-shuffle between runs, so "it came out sorted in testing" proves nothing. Code that produces output from a map must sort the keys, or its tests are flaky and its diffs are noise.
- Maps are **not** safe for concurrent use. Concurrent writes trigger `fatal error: concurrent map writes`, which cannot be recovered. One writer plus concurrent readers is also a race, even though it often survives (`concurrency.md`).
- `&m[k]` does not compile: map values are not addressable because a growth can move them. For a struct value, read it out, modify, write it back — or store `*T`.
- Deleting during iteration is defined: an entry deleted before it is reached will not be produced. Adding during iteration is undefined — the new key may or may not appear.
- `clear(m)` (`go >=1.21`) removes all entries in place, keeping the allocated buckets. Note the asymmetry with slices, where `clear` zeros rather than empties.
- A map never shrinks its bucket array. A map that peaked at ten million entries and now holds ten still owns that memory; rebuild it into a fresh map to release it (`memory.md`).
- `maps.Keys`/`maps.Values` (`go >=1.23`) return **iterators**, not slices — `slices.Sorted(maps.Keys(m))` is the idiom. The older `golang.org/x/exp/maps.Keys` returned a slice, so code copied from an old answer will not compile.

## Choosing a Key and a Structure

- Any comparable type can be a map key: numbers, strings, bools, pointers, channels, interfaces, and arrays or structs made only of those. Slices, maps, and funcs cannot. A struct key containing an interface field compiles and panics at runtime with `comparing uncomparable type` when the dynamic value is a slice (`structs.md`).
- `map[K]struct{}` is the set: the value costs zero bytes, and `_, ok := m[k]` reads naturally. `map[K]bool` is fine too and slightly easier to print.
- Float keys: `NaN != NaN`, so a `NaN` key can be written and never found again, and each write adds a new entry. Never key on floats.
- Linear scan of a slice beats a map for small collections — the crossover is workload-specific and usually in the tens of elements. Measure before converting a hot small map (`performance.md`).
- Ordered iteration, range queries, or a sorted dump: keep a sorted slice and `slices.BinarySearch`, or maintain both structures explicitly.

## Arrays

- `[3]int` is a value: assignment and function passing **copy** all elements, and `==` compares them element-wise. That copy is why arrays are rare outside fixed-size buffers, hashes, and map keys.
- `len` is part of the type: `[3]int` and `[4]int` are different types, and a function taking `[3]int` cannot receive `[4]int`. Take a slice parameter unless the fixed size is the point.
- `&arr[0]` plus `arr[:]` converts to a slice without copying; the slice then aliases the array for its whole lifetime.

## Back To SKILL.md

Core Rule 7 states the aliasing and three-index rule; Core Rule 8 covers nil maps. Strings and runes: `strings.md`. Retained-memory consequences: `memory.md`.
