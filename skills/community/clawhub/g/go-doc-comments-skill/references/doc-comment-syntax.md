# Go Doc Comment Syntax Reference

Complete gofmt-aware syntax for Go doc comments, per [go.dev/doc/comment](https://go.dev/doc/comment). Write comments so `gofmt` leaves them **stable** — matching gofmt's rules up front avoids reformatting churn. Verify with `gofmt -d file.go`.

## Paragraphs

Spans of unindented non-blank lines, separated by blank lines. Prefer **one sentence (or long phrase) per line** — semantic linefeeds keep diffs clean; gofmt does not rewrap.

```go
// Gofmt formats Go programs.
// It uses tabs for indentation and blanks for alignment.
// Alignment assumes that an editor is using a fixed-width font.
```

Consecutive backticks (`` ` ``) render as a Unicode left quote and consecutive straight single quotes as a right quote — rarely something you need to author deliberately.

## Headings

`# Heading` on an **unindented** line, surrounded by blank lines.

```go
// # Numeric Conversions
```

Not headings: `#NoSpace`, a `#` line that wraps to a second line, or an indented `#` line.

## Doc links (to Go identifiers)

- Current package: `[Name]`, `[Name.Method]`, `[Type.Field]`
- Other package: `[pkg.Name]`, `[io.EOF]`, `[encoding/json.Decoder]`
- Pointer types: `[*bytes.Buffer]`

A doc link must be **preceded and followed by punctuation, space, tab, or a line boundary** — otherwise it is not recognized.

```go
// ReadFrom reads data from r until EOF. Any error except [io.EOF]
// encountered during the read is also returned. If the buffer becomes
// too large, ReadFrom panics with [ErrTooLarge].
func (b *Buffer) ReadFrom(r io.Reader) (n int64, err error)
```

## Web links

Reference `[Text]` in prose, with a definition line elsewhere in the comment:

```go
// Package json implements encoding and decoding of JSON as defined in
// [RFC 7159].
//
// [RFC 7159]: https://tools.ietf.org/html/rfc7159
```

gofmt moves all link definitions to the end of the doc comment (referenced ones first, then unreferenced).

## Lists

**Bullets** use `*`, `+`, `-`, or `•`; gofmt normalizes to `-`, with two spaces before the marker and four-space indent for continuation lines.

```go
//   - the public suffix of "example.com" is "com",
//   - the public suffix of "foo1.foo2.co.uk" is "co.uk", and
//   - the public suffix of "bar.pvt.k12.ma.us" is "pvt.k12.ma.us".
```

**Numbered** lists use a decimal followed by `.` or `)`:

```go
//  1. Replace multiple slashes with a single slash.
//  2. Eliminate each . path name element (the current directory).
//  3. Eliminate each inner .. path name element along with the
//     non-.. element that precedes it.
```

**Nested lists are not supported** — gofmt flattens them. Restructure to a single level, or separate items with blank lines.

## Code blocks

Indent with a tab; surround with blank lines. gofmt normalizes indentation to a single tab and strips common leading whitespace.

```go
// As a more whimsical example, this program guesses your number:
//
//	func GuessingGame() {
//		var s string
//		answer := sort.Search(100, func(i int) bool {
//			return s != "" && s[0] == 'y'
//		})
//		fmt.Printf("Your number is %d.\n", answer)
//	}
```

## Notes

Form: `MARKER(uid): body` — MARKER is **2+ uppercase letters**, `uid` is 1+ character (conventionally a username). Only this form is collected and rendered in a Notes section on pkg.go.dev.

```go
// TODO(rsc): refactor to use the standard library context
// BUG(r): does not handle multi-byte input correctly
```

A bare `NOTE:`, `HACK:`, `WARNING:`, `PERF:`, `SECURITY:` **without** the `(uid)` is just an ordinary comment — useful to readers, but not machine-collected. Use whichever keywords your team standardizes on; only the `MARKER(uid):` form is special to tooling.

## Deprecation

A paragraph beginning `Deprecated:` marks the symbol deprecated. Tools (`gopls`, vet) warn on use; pkg.go.dev hides it by default. `Deprecated:` is a machine token — exact spelling, never translated.

```go
// Reset zeros the key data and makes the Cipher unusable.
//
// Deprecated: Reset can't guarantee the key is removed from process memory.
func (c *Cipher) Reset()
```

## Directives

`//go:generate`, `//go:embed`, `//go:build`, etc. are **not** doc comments and are omitted from rendered docs. Write them with **no space** after `//`. When mixed with a doc comment, gofmt moves directives below the doc text, separated by a blank line.

```go
// An Op is a single regular expression operator.
//
//go:generate stringer -type Op -trimprefix Op
type Op uint8
```

## What gofmt does to doc comments (summary)

- Removes leading/trailing blank lines; collapses duplicate blank lines.
- Does **not** rewrap text (semantic linefeeds preserved).
- Normalizes bullet markers to `-`; numbered lists to `N.`.
- Indents code blocks to a single tab; inserts surrounding blank lines.
- Moves link definitions to the end; moves directives below doc text.
- Reformats old-style (pre-Go 1.19) implicit headings to explicit `#`.
