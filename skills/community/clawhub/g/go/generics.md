# Generics — Type Parameters, Constraints, and When Not To

Type parameters arrived in `go >=1.18`. They remove `any` from container and algorithm code; they do not replace interfaces, and used reflexively they make code harder to read for no gain.

## The Decision Rule

Write the concrete version first. Then:

| Situation | Answer |
|---|---|
| Same body, several types, no shared methods (`Map`, `Filter`, `Keys`, `Min`) | Type parameter |
| Behavior differs per type | Interface — dispatch is the point |
| One type today, "maybe more later" | Concrete. Generalize when the second caller exists |
| Container of `T` where the element type must be preserved for the caller | Type parameter (this is what `any` used to cost) |
| Function takes `any` and immediately type-switches | Neither is right: split into typed functions, or accept an interface |

Ian Lance Taylor's formulation, still the best filter: write code, not types — and use type parameters when methods on the type cannot express what you need, or when the implementation is literally identical for every type.

## Constraints

```go
type Number interface{ ~int | ~int64 | ~float64 }   // union with underlying types

func Sum[T Number](xs []T) T {
    var total T                                     // zero value of T
    for _, x := range xs { total += x }
    return total
}
```

- `~int` means "any type whose **underlying** type is int", so a `type Celsius int` satisfies it. Without the tilde, only `int` itself does — and user-defined named types are exactly what generic helpers get called with.
- Built-in constraints: `any` (no restriction), `comparable` (usable with `==`, required for map keys). `golang.org/x/exp/constraints` supplies `Ordered`, `Integer`, `Float`, `Signed` — `cmp.Ordered` is in the standard library from `go >=1.21` and is the one to use.
- A constraint containing a union of types **cannot also declare methods** in the general case, so "numbers that also have a String method" is not expressible directly. Take a second type parameter or an interface argument.
- `comparable` means compile-time comparable. An interface type does not satisfy `comparable` as a type argument even though interface values support `==` — this is deliberate: those comparisons can panic at runtime (`structs.md`).
- Constraints are interfaces; an interface with only methods is a valid constraint and behaves exactly as it does today.

## Type Inference and Its Limits

- Inference works from **arguments**, not from return values. `func Zero[T any]() T` must be called as `Zero[int]()`; there is nothing to infer from.
- `Map[T, U any](xs []T, f func(T) U) []U` infers `T` from `xs` and `U` from the function literal's declared result. An untyped `func(x) { ... }` argument cannot be inferred and needs explicit type arguments.
- Partial instantiation is allowed left to right: `Map[string](xs, f)`.
- **Methods cannot have their own type parameters.** `func (c *Cache) Get[T any](k string) T` does not compile — that is the hard wall generic APIs hit. Options: put the parameter on the type (`Cache[T]`), or make it a package-level function taking the receiver (`Get[T](c *Cache, k string)`).
- Generic type aliases arrived in `go >=1.24`; before that, `type MySlice[T any] = []T` is a compile error and needs a defined type instead.

## What Generics Cost

- Go compiles generics with **GC shape stenciling**: one instantiation per "gc shape" (roughly: per memory layout), with all pointer-shaped type arguments sharing a single body plus a runtime dictionary. So `List[*User]` and `List[*Order]` share code and reach methods through the dictionary — an indirect call, roughly what an interface would cost. `List[int]` gets its own specialized body.
- Practical reading: generics over **value types** (int, float, small structs) can be genuinely faster than the `any` version because boxing disappears. Generics over **pointer types** mostly buy type safety, not speed. Benchmark before claiming a win (`performance.md`).
- Compile time and binary size grow with the number of distinct shapes instantiated.
- Reflection over a type parameter needs `any(v)` first, and once you are type-switching inside a generic function you have written a worse interface.

## Idiomatic Uses

- Collection helpers that the stdlib now provides — check `slices` and `maps` before writing your own (`collections.md`).
- `Ptr[T](v T) *T` for taking the address of a literal (invaluable for API structs full of `*string` fields).
- Result and Option types are possible and are **not** idiomatic Go: multiple return values plus `error` already occupy that space, and every caller would need to learn your combinators (`errors.md`).
- Typed keys and typed caches: `Cache[K comparable, V any]` removes the assertion at every read site.
- Constraining to a set of allowed types for validation or SQL scanning, where the alternative is `any` plus a runtime switch.

## Common Mistakes

| Mistake | Consequence | Fix |
|---|---|---|
| `[T any]` on a function that only ever takes `string` | Extra indirection, worse signature, no benefit | Concrete type |
| Union constraint without `~` | Named types like `type ID int` do not satisfy it | `~int \| ~string` |
| Trying to add a type parameter to a method | Does not compile; discovered halfway through a refactor | Parameter on the type, or a package-level function |
| Expecting inference from the return type | "cannot infer T" with no obvious cause | Explicit type argument |
| Reimplementing `slices`/`maps` helpers | Missed edge cases and no compiler-team optimization | Use the stdlib packages (`go >=1.21`) |
| `var zero T` compared with `== nil` | `T` may not be nilable; does not compile for `int` | Compare against `var zero T`, or constrain to pointer-shaped types |
| Generic function that type-switches on `any(v)` | An interface with extra syntax | Define the interface and dispatch |

## Back To SKILL.md

Interface sizing and placement: `interfaces.md`. Stdlib generic helpers: `collections.md`. Version floors for type parameters and generic aliases: `versions.md`.
