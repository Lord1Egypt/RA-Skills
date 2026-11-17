# Structs — Copying, Embedding, Comparability, and Layout

Structs are values. Every assignment, every function call, every channel send, and every append copies the whole struct. Getting that one fact wrong causes the mutation bugs; the rest of this file is embedding, comparability, and the memory the layout costs you.

## Value Semantics

- `b := a` copies every field. Slice, map, pointer, and channel fields are copied as *references*, so the copy shares the same underlying data: the copy is shallow, and "I copied it so it is safe" is false for any struct with a slice inside.
- Method receivers follow the same rule. `func (c Counter) Inc() { c.n++ }` increments a copy and compiles without complaint.
- Pointer receiver when: any method mutates, the struct is large, or the type contains a `sync.Mutex`. Then use pointer receivers for **all** methods of that type (`idioms.md`).
- Never copy a struct containing a `sync.Mutex`, `sync.WaitGroup`, `sync.Once`, `strings.Builder`, or an `atomic.*` type. `go vet`'s `copylocks` catches the direct cases; it does not catch a copy made through an interface or reflection.
- Returning a large struct by value is usually fine — Go's escape analysis frequently avoids the heap for it, and copying a 100-byte struct is cheaper than a heap allocation plus a GC-scanned pointer (`memory.md`).

## Zero Values and Constructors

- Design so the zero value works: `bytes.Buffer`, `sync.Mutex`, `strings.Builder`, and `http.Client` all do. A type whose zero value panics forces every user to remember a constructor.
- Map and channel fields are the exception — they are nil at zero and writing to a nil map panics. Any struct with a map field needs a constructor, or documented lazy init (`collections.md`).
- Constructor convention: `NewThing(...) *Thing` returning a pointer, or `Thing{...}` composite literals when there is nothing to validate. Do not write a constructor that only sets fields the caller could set.
- Use **field names** in composite literals: `Point{X: 1, Y: 2}`. Positional literals break silently when a field is inserted upstream; `go vet`'s `composites` check flags positional literals for structs from other packages.

## Comparability

- `==` works on structs whose every field is comparable: numbers, strings, bools, pointers, channels, interfaces, and arrays or structs of those. It compares field by field.
- Slices, maps, and funcs are **not** comparable, so a struct containing one is not comparable and cannot be a map key. The compiler catches the direct case.
- The runtime case is the killer: a struct with an `any`/`interface{}` field *is* comparable at compile time, and panics with `comparing uncomparable type []string` when the dynamic value is a slice. Any map keyed on such a struct is one payload away from a crash (`collections.md`).
- Deep comparison in tests: `reflect.DeepEqual` treats a nil slice as different from an empty one and inspects unexported fields; `google/go-cmp` gives readable diffs and explicit options. Prefer go-cmp in tests, an explicit method in production (`testing.md`).
- Adding a `struct{}` field or an incomparable field to an exported struct silently removes `==` and map-key usage from every caller — a breaking change that produces no deprecation warning.

## Embedding

```go
type Server struct {
    *log.Logger      // promoted: srv.Printf(...) works
    mu   sync.Mutex  // named, unexported: not part of the API
    addr string
}
```

- Promotion is delegation, not inheritance. A promoted method's receiver is the **embedded** value: it cannot see the outer struct's fields and cannot call an outer method that shadows it. Code translated from a class hierarchy breaks here first (`interfaces.md`).
- Shadowing is silent. Define the same method on the outer type and it wins, with no keyword and no warning.
- Two embedded types with the same method name at the same depth: legal declaration, compile error only at the ambiguous call site. Depth breaks the tie — a shallower method always wins.
- Embedding an exported type exports its whole API through yours, forever. Embedding `sync.Mutex` publicly means callers can `Lock` your object; embedding a struct means its future methods appear in your API on the next dependency upgrade.
- An embedded **nil pointer** promotes methods that panic on the first call. Useful deliberately for partial test stubs, fatal accidentally.
- Embedding also promotes struct **tags** for encoders: an embedded struct's fields are flattened into the parent's JSON unless the embedded field is named or tagged (`json.md`).

## Tags

- Format is a single backtick string of space-separated `key:"value"` pairs: `json:"name,omitempty" db:"name" validate:"required"`. There is no compile-time checking — a typo like `json: "name"` (space after the colon) silently produces no tag, and `jsonn:"name"` is simply ignored.
- `go vet`'s `structtag` check catches malformed syntax and duplicate keys. Run it; it is the only guardrail here.
- Tags are read by reflection at runtime, which means an unexported field is invisible to every encoder no matter how it is tagged (`json.md`).
- Keep tags to serialization and validation. Encoding business rules in tags moves logic into strings the compiler cannot see.

## Memory Layout

- Fields are laid out in declaration order with padding inserted to satisfy each field's alignment; the struct's own size rounds up to its largest field's alignment. `struct{ a bool; b int64; c bool }` costs 24 bytes on a 64-bit platform; reordering to `int64, bool, bool` costs 16.
- Reordering matters when the struct is allocated in the millions (rows, graph nodes, cache entries). For a config struct allocated once it is noise — declaration order that reads well wins.
- The `fieldalignment` analyzer (in `golang.org/x/tools/go/analysis/passes`, exposed by golangci-lint) reports the savings per type so you do not have to compute padding by hand.
- Pointer fields cost more than their 8 bytes: every pointer is a GC scan target. A `[]Item` of 1M plain structs is one allocation the GC scans as a block; `[]*Item` is 1M objects to trace (`memory.md`).
- `struct{}` is zero-sized: `map[string]struct{}` as a set, and `chan struct{}` as a signal, allocate nothing for the value.
- `unsafe.Sizeof` reports the size including padding; `unsafe.Alignof` and `Offsetof` explain where it went.

## Common Mistakes

| Mistake | Consequence | Fix |
|---|---|---|
| Value receiver on a mutating method | Silent no-op on a copy | Pointer receiver everywhere on that type |
| Mixing value and pointer receivers | Only `*T` satisfies interfaces; readers cannot tell what is safe to copy | Pick one per type |
| Copying a struct with an embedded mutex | Two locks, no mutual exclusion | Pass the pointer; heed `go vet copylocks` |
| Positional composite literal for another package's struct | Breaks silently when they add a field | Named fields |
| Exported struct with all-exported fields as an API boundary | Every field is now a compatibility promise, and callers can build invalid instances | Unexported fields + constructor, or accept the promise deliberately |
| Struct with an `any` field used as a map key | Runtime `comparing uncomparable type` | Key on a derived comparable value |
| Adding fields to a struct returned by value across a module boundary | Callers using positional literals or `==` break | Add a `_ struct{}` guard field deliberately, or return a pointer |

## Back To SKILL.md

Panic messages including `comparing uncomparable type`: SKILL.md "Panics And Fatal Errors". Method sets and interface satisfaction: `interfaces.md`. Allocation consequences: `memory.md`.
