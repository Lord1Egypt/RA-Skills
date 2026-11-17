# Interfaces — Nil Traps, Method Sets, and Sizing

An interface value is two words: a type descriptor and a data pointer. Almost every interface surprise in Go follows from that representation, or from where the interface is declared.

## The Nil Trap

```go
var p *MyType            // nil pointer
var i interface{} = p    // type=*MyType, value=nil
i == nil                 // FALSE
```

An interface is nil only when **both** words are nil. Assigning any typed nil gives a non-nil interface that panics the moment a method dereferences the receiver.

- The production form: a function declared `func f() error` whose body returns a `*MyErr` variable that happens to be nil. Every `if err != nil` upstream fires (`errors.md`).
- Rule: declare the return type as the interface and return the literal `nil`. Never `var e *MyErr; ...; return e`.
- Detecting it after the fact needs reflection (`reflect.ValueOf(i).IsNil()`), which is a sign the API is wrong rather than a fix.
- A nil pointer receiver is legal and useful when the method does not dereference: `func (t *Tree) Size() int { if t == nil { return 0 } ... }`. That is a deliberate design, not the trap.

## Method Sets

| Receiver | `T` satisfies | `*T` satisfies |
|---|---|---|
| `func (t T) M()` | yes | yes |
| `func (t *T) M()` | **no** | yes |

- The compile error is `T does not implement I (method M has pointer receiver)`. Fix by passing `&v`, not by changing the receiver — switching a mutating method to a value receiver makes it mutate a copy and compile cleanly.
- Values inside a map or a slice of `T` are not addressable through the index expression in every position: `m["k"].M()` with a pointer-receiver method does not compile. Store `*T` in the map, or copy out to a local first.
- Do not mix receiver kinds on one type. Pick pointer receivers if any method mutates or the struct is large, and use them everywhere on that type (`idioms.md`).
- Satisfaction is implicit and structural. Rename a method on your type and the compiler says nothing until an assignment fails somewhere far away. Assert it at compile time in the implementing package:

```go
var _ io.ReadCloser = (*MyFile)(nil)   // zero cost, breaks the build at the right place
```

## Type Assertions and Switches

- `v := i.(T)` panics on mismatch. `v, ok := i.(T)` never panics — use the comma-ok form everywhere except when a failure genuinely means the program is broken.
- Asserting to an *interface* type checks the method set of the dynamic type, not identity: `if rc, ok := r.(io.Closer); ok { rc.Close() }` is the standard "does this thing also support X" probe used throughout the stdlib.
- Type switches list concrete types; `case nil:` matches the nil interface, and `default:` is the branch that fires when an implementer you did not anticipate arrives. Always write `default` — a silent no-op there is how new types get dropped.
- A type switch cannot branch on a type parameter `T` in generic code; the value must be converted to `any` first, and needing that usually means an interface fits better than a type parameter (`generics.md`).
- `errors.As` is the type-switch replacement for error chains; a bare assertion on a wrapped error fails (`errors.md`).

## Sizing and Placement

- **Declare interfaces in the consuming package, not next to the implementation.** The consumer knows the two methods it needs; the producer would export ten. This is what makes fakes trivial in tests without a mock framework (`testing.md`).
- One or two methods is the norm in Go — `io.Reader`, `io.Writer`, `error`, `http.Handler`, `sort.Interface` is already a large one at three. An interface with ten methods is a struct with extra steps: nobody implements it twice, and nobody can fake it in a test.
- "Accept interfaces, return structs" is a guideline with a real reason: returning a concrete type lets callers reach new methods you add later without a breaking change, while accepting an interface lets them pass anything. The exception is a factory whose whole point is polymorphism.
- Do not define an interface for a type with exactly one implementation and no test double need. Add it when the second implementation arrives; the refactor is mechanical.
- Interface method calls are indirect, which blocks inlining and devirtualization in hot loops. Relevant only after a profile says so (`performance.md`).

## Embedding

- Embedding a type promotes its methods: `struct{ io.Writer }` satisfies `io.Writer` by delegation. Embedding an interface with a nil value compiles and panics on the first promoted call — a common pattern for "implement only the methods I care about" test stubs, and a common crash when the stub is used more than expected.
- Embedding an *interface* in a struct is the way to build a partial implementation; embedding a **pointer to an interface** is almost always a mistake — an interface is already a reference-like two-word value.
- Shadowing is silent: define `func (s *S) Write(...)` on a struct that embeds `io.Writer` and yours wins, with no `override` keyword and no warning. Grep for the method name before adding one to an embedding type.
- Promotion is not inheritance. A promoted method called on the outer type still has the *inner* receiver: it cannot see the outer struct's fields or call the outer struct's overrides. Code ported from a class hierarchy breaks here first (`structs.md`).
- Ambiguous promotion (two embedded types with the same method at the same depth) is a compile error only at the call site, not at the type declaration.

## any and Reflection

- `any` is an alias for `interface{}` (`go >=1.18`), not a new type. It accepts everything and asserts nothing; in a signature it moves a compile error into someone else's runtime.
- Before reaching for `reflect`: a small interface, a type switch over a closed set, or a type parameter usually removes the need. Reflection costs allocation and readability, and its errors are runtime panics.
- Where reflection is genuinely the answer: struct tags for encoders (`json.md`), generic deep equality in tests (`reflect.DeepEqual`), and dependency wiring. `reflect.DeepEqual` treats nil and empty slices as different and compares unexported fields — in tests prefer an explicit comparison or `go-cmp` (`testing.md`).

## Common Mistakes

| Mistake | Consequence | Fix |
|---|---|---|
| `func f() *MyErr` used as an `error` by callers | Typed nil compares non-nil | Return `error` |
| Interface defined in the producer package | Every consumer imports a package it does not need; fakes must implement all ten methods | Define the two-method interface where it is used |
| `i.(string)` without comma-ok on decoded JSON | `interface conversion` panic on the first unexpected payload | `s, ok := i.(string)` and handle the miss (`json.md`) |
| Value receiver on a mutating method | Mutation applies to a copy; the caller sees nothing and nothing errors | Pointer receiver |
| `interface{}` parameter "for flexibility" | The API documents nothing and every caller guesses | Concrete type, small interface, or type parameter |
| Embedded `sync.Mutex` on an exported struct | `Lock`/`Unlock` become part of your public API and callers deadlock you | Unexported field `mu sync.Mutex` |

## Back To SKILL.md

Core Rule 3 states the nil-interface rule. Struct embedding and layout: `structs.md`. Type parameters: `generics.md`.
