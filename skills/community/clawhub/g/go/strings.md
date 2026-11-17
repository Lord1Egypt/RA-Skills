# Strings, Bytes, and Runes

A Go string is an immutable slice of **bytes** with no declared encoding; the language assumes UTF-8 only in `range`, in conversions, and in `unicode/utf8`. Nearly every string bug is a byte treated as a character, or a conversion nobody knew was a copy.

## Bytes, Runes, Characters

| Expression | Yields |
|---|---|
| `len(s)` | Bytes, always. `len("café") == 5` |
| `s[i]` | One **byte** (`byte` = `uint8`), not a character |
| `for i, r := range s` | `r` is a `rune` (int32 code point); `i` is the **byte** offset, so it jumps by 1-4 |
| `utf8.RuneCountInString(s)` | Code points |
| `[]rune(s)` | Copies into a code-point slice — O(n) allocation, then indexable |

- Slicing cuts on bytes: `s[:3]` on `"café"` is fine, `s[:4]` cuts the é in half and produces invalid UTF-8. Truncating user text needs a rune-aware walk, not a byte bound.
- Invalid UTF-8 in `range` yields `utf8.RuneError` (U+FFFD) with size 1, advancing one byte — so a loop over binary data terminates but produces garbage rather than an error. Validate with `utf8.ValidString` at the boundary.
- A code point is still not a user-perceived character: "é" can be one code point or `e` + a combining accent, and emoji with modifiers span several. Counting "characters" for a UI limit needs grapheme clusters (`golang.org/x/text`), not `RuneCountInString`.
- `unicode.ToUpper` is per-rune and locale-blind. Case-insensitive comparison of ASCII-ish input is `strings.EqualFold`; correct case mapping for Turkish dotless i or German ß needs `golang.org/x/text/cases`.

## Conversions and Copies

- `[]byte(s)` and `string(b)` **allocate and copy**. The compiler elides the copy in specific proven-safe positions — a `string(b)` used only as a map key, or a `[]byte(s)` ranged over immediately — but never assume it; check with `-benchmem` (`performance.md`).
- `string(65)` is `"A"`, not `"65"`: an integer converts as a code point. `go vet` flags the literal case. Use `strconv.Itoa(n)` or `strconv.FormatInt`.
- `strconv` over `fmt` in hot paths: `strconv.Itoa` does one small allocation, `fmt.Sprintf("%d", n)` goes through reflection and interface boxing. In non-hot code `fmt` is more readable and the difference is irrelevant.
- Parsing: `strconv.Atoi` for ints, `ParseFloat(s, 64)`, `ParseBool`. All return an error — an ignored parse error is how zeros appear in production data.
- A substring **shares** the parent's bytes. `line[:8]` from a 2 MB read keeps 2 MB alive; `strings.Clone(s)` (`go >=1.18`) makes an independent copy (`memory.md`).

## Building Strings

```go
var b strings.Builder
b.Grow(estimatedBytes)      // one allocation when the estimate holds
for _, part := range parts {
    b.WriteString(part)     // never returns a real error
}
return b.String()           // no copy: Builder hands over its buffer
```

- `s += part` in a loop is O(n²) bytes copied: each iteration allocates a new string and copies everything so far. Fine for three concatenations, catastrophic for ten thousand.
- `strings.Builder` must not be copied after first use — passing it by value panics with "illegal use of non-zero Builder copied by value". Pass `*strings.Builder`.
- `strings.Join(parts, sep)` is the right answer when the parts are already in a slice: it sizes the buffer exactly, in one pass.
- `bytes.Buffer` when the output is bytes or must satisfy `io.Writer`; `strings.Builder` when the output is a string. Builder avoids the final copy that `Buffer.String()` performs.
- `fmt.Fprintf(&b, ...)` writes formatted output straight into either one, avoiding an intermediate string.

## The strings Package Worth Memorizing

- `Cut(s, sep)` (`go >=1.18`) returns `before, after, found` — replaces the `Index`-then-slice dance and the `SplitN(s, sep, 2)` idiom for key/value parsing.
- `TrimPrefix`/`TrimSuffix` remove one exact affix. `Trim(s, cutset)` takes a **set of runes**, not a substring: `strings.Trim(name, "go")` strips every leading and trailing `g` and `o`. This is the most misread signature in the package.
- `TrimSpace` handles all Unicode whitespace, including non-breaking space, which `Trim(s, " ")` does not.
- `Split("", sep)` returns a one-element slice containing the empty string, not an empty slice — a loop over a split of empty input runs once.
- `Fields(s)` splits on runs of whitespace and drops empties; `Split(s, " ")` does not. For "split a command line", `Fields` is almost always what was meant.
- `EqualFold` for case-insensitive equality; `strings.ToLower(a) == strings.ToLower(b)` allocates twice and is wrong for some scripts.
- `Replace(s, old, new, -1)` vs `ReplaceAll` — the same function; use `ReplaceAll` for readability.
- `strings.NewReader(s)` gives an `io.Reader` over a string with no copy, which is how you feed a string to any streaming API (`io.md`).

## Formatting with fmt

| Verb | Prints |
|---|---|
| `%v` / `%+v` | Default / with struct field names |
| `%#v` | Go syntax, including types — the debugging verb |
| `%q` | Quoted and escaped; makes trailing spaces and invisible characters visible |
| `%T` | The dynamic type — first move when an interface holds the wrong thing |
| `%w` | Wraps an error; only valid in `fmt.Errorf` (`errors.md`) |

- A type with a `String() string` method controls its own `%v`. Calling `fmt.Sprintf("%v", x)` **inside** that method recurses until the stack dies — format the underlying value or a converted alias type instead.
- `%s` on a type that implements `error` prints via `Error()`; on a struct without either method it prints `%!s(...)`, which is the runtime telling you the verb does not match.
- `fmt` reaches unexported fields through reflection for printing, so `%+v` on a struct holding a secret puts it in the log (`security.md`, `logging.md`).

## Regexp

- `regexp` uses RE2: linear time, no catastrophic backtracking, and **no backreferences or lookahead**. A pattern copied from a PCRE-flavored language fails to compile rather than misbehaving.
- Compile once into a package-level `var re = regexp.MustCompile(...)`. Compiling inside a handler or a loop dominates the cost of the match itself.
- For a fixed substring, `strings.Contains`/`HasPrefix`/`Cut` beat a regexp by a wide margin — reach for `regexp` when the pattern is genuinely a pattern.
- `FindStringSubmatch` returns nil on no match; indexing it without a nil check is a panic on the first non-matching input.

## Common Mistakes

| Mistake | Consequence | Fix |
|---|---|---|
| `s[i]` to read a character | Bytes, so any non-ASCII input mangles | `[]rune(s)` once, or `range` |
| `+=` in a loop | O(n²) copying | `strings.Builder` with `Grow` |
| `strings.Trim(s, "prefix")` | Strips a character set, not the prefix | `strings.TrimPrefix` |
| `string(intVal)` | Code point instead of digits; `go vet` warns | `strconv.Itoa` |
| Holding a substring of a huge buffer | Whole buffer retained | `strings.Clone` |
| Comparing user input with `==` after `ToLower` | Two allocations, and wrong for some scripts | `strings.EqualFold` |
| Regexp built per call | Compilation cost on every request | Package-level `MustCompile` |

## Back To SKILL.md

Slices and maps: `collections.md`. Encoding at I/O boundaries: `io.md`. Retained-buffer diagnosis: `memory.md`.
