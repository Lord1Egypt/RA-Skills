---
name: go-doc-comments
description: Writes and supplements Go source comments to the official Go doc comment standard (go.dev/doc/comment). Use when adding, fixing, or reviewing comments in .go files — package comments, doc comments for exported functions/types/constants/variables, godoc/pkg.go.dev documentation, or when discussing Go commenting conventions. Covers the decision of whether to comment at all, identifier-first sentences, doc-link syntax, gofmt-safe formatting, and matching the existing comment language.
---

# go-doc-comments

Guidance for writing and supplementing Go comments so they are idiomatic, tool-friendly, and conform to [go.dev/doc/comment](https://go.dev/doc/comment).

## Core Principle

**Write code that speaks for itself. In Go, that means clear names and structure for the WHAT, and doc comments that add WHY, contracts, and context.**

Two rules pull in different directions — hold both:

1. **Comment sparingly inside function bodies.** Most implementation code needs no comments; good naming beats a comment. Explain WHY (design decisions, non-obvious trade-offs, workarounds), not WHAT.
2. **But document every exported identifier.** This is a hard Go convention, not a preference. Every exported (capitalized) package, func, type, const, and var *should* have a doc comment. `go doc`, `gopls`, and `pkg.go.dev` extract these. A missing doc comment on an exported symbol is a defect, even when the symbol looks obvious.

The distinction: rule 1 governs comments *inside* bodies; rule 2 governs *doc comments* on declarations. Do not conflate them — "self-documenting code" is never a reason to skip a doc comment on an exported API.

---

## Decision Framework

Run this **before writing any comment**. It decides both *whether* to comment and *what kind*.

### Step 0 — Is this an exported declaration?

- **YES** → a doc comment is **mandatory** (rule 2). Skip the rest of this framework; go to [Doc Comment Conventions](#doc-comment-conventions-by-declaration). "The name is obvious" does not exempt exported API.
- **NO** (unexported symbol, or a line inside a function body) → continue to Step 1. This is where "comment sparingly" applies.

### Step 1 — Is the code self-explanatory?

- **YES** → no comment. Stop.
- **NO** → Step 2.

### Step 2 — Would a better name or a small refactor remove the need?

- **YES** → refactor instead of commenting. Rename the variable, or extract the tangled expression into a well-named function. Prefer this over a clarifying comment.
- **NO** → Step 3.

### Step 3 — Does the comment explain WHY, not WHAT?

- **Explaining WHAT the code does** → the code should say that itself; go back to Step 2 and make it clearer.
- **Explaining WHY** (rationale, constraint, workaround, gotcha, non-obvious algorithm choice, performance bound) → this is a good comment. Write it.

### Refactor over comment — example

```go
// BAD: comment compensates for an unclear condition
// grant access to admins and users with the special flag
if u.role == "admin" || (u.perms != nil && u.perms["special"]) {

// GOOD: the condition names itself; no comment needed
if userHasAdminAccess(u) {
```

---

## Language of Comments

**Detect the existing comment language in the file/package and match it.** If existing comments are in Chinese, write new comments in Chinese; if English, use English. When a file or package has no existing comments, **default to English**.

Regardless of prose language, keep Go's structural idioms in their canonical form:

- The **identifier-first sentence** still starts with the symbol name (e.g. `// Quote 返回 s 的双引号 Go 字符串字面量。` — the leading token is `Quote`, not a translated name).
- `Deprecated:` markers, `TODO(user):`/`BUG(user):` notes, and doc-link syntax `[pkg.Name]` stay in their standard form. `Deprecated:` is a recognized machine token — never translate it.
- Package comments still begin with `Package <name>` (or the command name for `package main`).

---

## Placement Rules (non-negotiable)

- A doc comment sits **immediately before** its declaration with **no blank line** between comment and declaration. A blank line demotes it to an ordinary comment that tools ignore.
- Use `//` line comments. `/* */` is allowed (common for long package comments) but `//` is idiomatic for most doc comments.
- The package comment appears in **exactly one** file of a multi-file package.

---

## Doc Comment Conventions by Declaration

### Package

Begins with `Package <name>`; for a command (`package main`), begins with the capitalized program name describing behavior.

```go
// Package path implements utility routines for manipulating slash-separated
// paths.
//
// The path package should only be used for paths separated by forward
// slashes; to manipulate operating system paths, use [path/filepath].
package path
```

### Functions and methods

Start with the function name. State what it returns, or for side-effect functions what it does.

- Boolean-returning functions: use **"reports whether"**, and omit "or not".
  ```go
  // HasPrefix reports whether the string s begins with prefix.
  func HasPrefix(s, prefix string) bool
  ```
- Refer to parameters and results by their names directly (no special syntax).
- Name results in the comment when it aids clarity; document special cases and error contracts.
  ```go
  // Copy copies from src to dst until either EOF is reached
  // on src or an error occurs. It returns the total number of bytes
  // written and the first error encountered while copying, if any.
  //
  // A successful Copy returns err == nil, not err == EOF.
  func Copy(dst Writer, src Reader) (n int64, err error)
  ```
- Document **complexity or performance bounds** in the doc comment when they are part of the contract, e.g. `// It makes O(n*log(n)) calls to data.Less.`
- Use a **consistent receiver name** across a type's methods.
- Note concurrency only when it deviates from the default (top-level funcs assumed goroutine-safe; type methods assumed single-goroutine unless stated).

### Types

Explain what an instance represents. Document the **zero value** when it is usable, and **concurrency safety** when relevant.

```go
// A Buffer is a variable-sized buffer of bytes with Read and Write methods.
// The zero value for Buffer is an empty buffer ready to use.
type Buffer struct { ... }
```

Document struct fields either in the type comment or with per-field end-of-line/preceding comments:

```go
// A LimitedReader reads from R but limits the amount of
// data returned to just N bytes.
type LimitedReader struct {
    R Reader // underlying reader
    N int64  // max bytes remaining
}
```

### Constants and variables

Grouped declarations can share one doc comment with per-line trailing comments; ungrouped ones get a full doc comment. Typed constant groups often rely on the type's doc comment.

```go
// Version is the Unicode edition from which the tables are derived.
const Version = "13.0.0"

// The result of Scan is one of these tokens or a Unicode character.
const (
    EOF = -(iota + 1)
    Ident
    Int
)
```

---

## Syntax (headings, links, lists, code blocks, notes, deprecation)

Doc comments have a small markup vocabulary, and `gofmt` reformats it. Write comments so `gofmt` leaves them **stable**. Quick reference:

- **Headings:** `# Heading` on an unindented line, blank lines around it.
- **Doc links:** `[Name]`, `[pkg.Name]`, `[io.EOF]`, `[*bytes.Buffer]` — must be surrounded by punctuation/space/line boundary.
- **Web links:** `[Text]` in prose + a `[Text]: https://…` definition line.
- **Lists:** `-` bullets or `1.` numbers; **no nesting**.
- **Code blocks:** tab-indented, blank lines around.
- **Notes:** only `MARKER(uid):` (2+ uppercase letters + a uid) is machine-collected; a bare `TODO:`/`NOTE:` is an ordinary comment.
- **Deprecation:** a paragraph starting with `Deprecated:`.
- **Directives:** `//go:generate` etc. — no space after `//`; not part of docs.

**For the complete rules, examples, and exactly what gofmt does to each construct, read [`references/doc-comment-syntax.md`](references/doc-comment-syntax.md).** Load it whenever authoring anything beyond a plain-prose doc comment.

---

## Workflow: Commenting a Go File or Package

1. **Read the code first.** Understand what each declaration actually does before writing a word — never describe behavior you have not confirmed from the code.
2. **Detect the comment language** already in use (§Language of Comments) and match it.
3. **Inventory exported-but-undocumented declarations.** Every exported package/func/type/const/var missing a doc comment is a target. Report the full list before mass-editing a large package (audit before fix).
4. **Apply the Decision Framework** to each candidate — exported symbols always get a doc comment; body comments only survive if they pass Step 3 (WHY, not WHAT).
5. **Write doc comments** following the per-declaration conventions — identifier-first, contracts, special cases, zero-value, concurrency, complexity bounds.
6. **Keep it gofmt-stable** — correct indentation for lists/code blocks, `#` headings, doc-link syntax. If `gofmt` is available, verify with `gofmt -d file.go`.
7. **Do not invent facts.** If a comment would state a version number, RFC, benchmark bound, or external contract you have not verified, mark it `[UNVERIFIED]` or leave it out rather than asserting it.

---

## Anti-Patterns

### ❌ Skipping doc comments on exported symbols
The most common Go documentation defect. Exported API without a doc comment is incomplete, however obvious the name.

### ❌ Non-identifier-first doc comments
```go
// BAD: This function returns the user's name.
func GetUserName(u User) string
// GOOD:
// GetUserName returns u's display name.
func GetUserName(u User) string
```

### ❌ Redundant / obvious / noise comments (inside bodies)
```go
i++            // increment i          ← delete
// loop over items                     ← delete; the loop is self-evident
```

### ❌ Outdated comments that no longer match the code
A comment that says 5% while the code multiplies by `0.08` is worse than no comment — it actively misleads. When you edit code, update or delete the comment above it in the same change. Never leave a stale doc comment describing old behavior.

### ❌ Blank line between doc comment and declaration
Silently demotes the doc comment; tools stop associating it.

### ❌ Accidental code blocks from indentation
An indented continuation line in a paragraph becomes a preformatted block. Keep continuation lines unindented in prose; indent only real code/lists.

### ❌ Commented-out code and changelog comments
Delete dead code and rely on version control; do not keep `// Modified by X on <date>` history in comments.

### ❌ Translating machine tokens
`Deprecated:`, `TODO(...)`, `//go:...` directives, and doc-link brackets must stay in canonical form even in a non-English file.

---

## Checklist

Before finishing, confirm comments:

- [ ] Every exported declaration has a doc comment
- [ ] Each doc comment starts with the identifier name (package comment starts with `Package <name>`)
- [ ] No blank line between any doc comment and its declaration
- [ ] Boolean functions use "reports whether"
- [ ] Zero-value, concurrency, and complexity bounds documented where relevant
- [ ] Body comments passed the Decision Framework (WHY, not WHAT; no obvious/redundant/dead-code comments)
- [ ] No comment contradicts the code it describes (no stale/outdated comments)
- [ ] Prose language matches the existing file/package (English by default)
- [ ] `Deprecated:`, notes, directives, and doc links are in canonical form
- [ ] Lists/code blocks/headings follow gofmt syntax (would survive `gofmt`)
- [ ] No unverified facts (versions, RFCs, benchmarks) asserted

---

## Summary

| Goal | Approach |
|------|----------|
| **Whether to comment** | Run the Decision Framework — exported ⇒ always; body ⇒ WHY-only or refactor |
| **Exported API** | Always a doc comment, identifier-first, with contracts |
| **Internal bodies** | Comment WHY only; prefer clear names / extraction over comments |
| **Language** | Match existing comments; default English; keep Go tokens canonical |
| **Formatting** | gofmt-stable; details in `references/doc-comment-syntax.md` |
| **Accuracy** | Describe only confirmed behavior; keep comments in sync; never assert unverified facts |
