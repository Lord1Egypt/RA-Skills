# Idioms — Naming, Packages, Receivers, and Linting

Go has an unusually strong consensus about style, encoded in the language's own standard library. Following it is not aesthetics: consistent Go is faster to read, and every deviation costs a reviewer a moment of "why is this different".

## Naming

- **The package name is part of every identifier.** `http.Server`, not `http.HTTPServer`; `bytes.Buffer`, not `bytes.BytesBuffer`. Stutter is the most common naming defect in Go written by newcomers.
- Package names are short, lowercase, singular, one word, no underscores, no camelCase: `user`, `httputil`, `sqlstore`. `utils`, `common`, `helpers`, `base`, and `misc` are not package names — they are a statement that the boundary was never decided.
- Getters have no `Get` prefix: `u.Name()`, not `u.GetName()`. Setters keep `Set`: `u.SetName(n)`.
- Single-method interfaces take the method's name plus `-er`: `Reader`, `Writer`, `Formatter`, `Notifier` (`interfaces.md`).
- Variable name length scales **inversely** with scope: `i`, `r`, `w`, `b` inside a five-line loop; `userRepository` for a package-level value. A three-word name for a loop index is as wrong as `x` for a package-level variable.
- Initialisms keep their case: `userID`, `serveHTTP`, `apiURL`, `parseJSON` — never `userId` or `parseJson`.
- Error variables start with `Err` (`ErrNotFound`); error types end in `Error` (`ValidationError`) (`errors.md`).
- Error strings are lowercase, no trailing punctuation, no capital: `"open config: permission denied"`. They get wrapped into other messages, and a capital letter mid-sentence gives it away.
- The receiver name is one or two letters, the same for every method on the type: `func (s *Server)` everywhere, never `self` or `this`.

## Package Design

- A package is a **unit of purpose**, not a layer. `user` containing the model, storage, and handlers for users beats `models`/`repositories`/`handlers` split by technical role: the latter guarantees every change touches three packages.
- `internal/` is enforced by the toolchain: code under `internal/` is importable only by code rooted at its parent. That is the only real access control between packages, and the cheapest way to keep an API small while refactoring freely.
- `cmd/<binary>/main.go` when the repo produces more than one binary; a single `main.go` at the root is right for a repo with one. `package_layout` in Configuration records the project's choice.
- `pkg/` is optional community convention, not a Go standard — the standard library has no `pkg/` directory. It costs a path segment on every import and buys nothing the compiler recognizes.
- Import cycles are a compile error with no escape hatch. The fix is almost always an interface in the consumer, or a third package holding the shared type — never a `common` package that everything imports.
- `init()` should be rare. It runs on import, in every test binary and every tool that links the package, in an order you do not control, and it cannot return an error. Prefer an explicit constructor called from `main`.
- Keep `main` thin: parse configuration, build dependencies, call `run`, handle the error (`cli.md`).

## Receivers and Types

- Pointer receiver when the method mutates, the type contains a lock, or the struct is large. Value receiver for small immutable values (`time.Time`, small structs of scalars).
- **Do not mix** value and pointer receivers on one type: only `*T` satisfies interfaces then, and readers cannot tell whether copying the value is safe (`structs.md`).
- Named types over bare primitives at API boundaries: `type UserID string` prevents passing an order ID where a user ID belongs, at zero runtime cost.
- Make the zero value useful when you can (`bytes.Buffer`, `sync.Mutex`). A type that panics at zero forces every user to remember a constructor.
- Return concrete types, accept interfaces — the reason is asymmetric evolution: new methods on a returned struct are additive, while a new method on an accepted interface breaks every implementer (`interfaces.md`).

## Function Signatures

- `ctx context.Context` first, `error` last. Both are enforced by convention strictly enough that deviation reads as a bug (`context.md`).
- More than three or four parameters, or several of the same type in a row, means an options struct. Same-typed adjacent parameters are a silent bug source: `Copy(dst, src string)` has been transposed by everyone at least once.
- Optional configuration: functional options (`WithTimeout(d)`) for a library with many knobs and a long life; a plain config struct for everything else. Functional options cost real complexity — do not adopt them for three fields.
- Return early. Go's culture is a wall of `if err != nil { return ... }` guards with the happy path at the leftmost indentation, not nested `else` blocks.
- Naked returns (a bare `return` with named results) are acceptable only in very short functions; in a long one they force the reader to hunt for what is being returned. The legitimate use of named results is documentation and modifying the result in a defer (`errors.md`).

## Comments and Docs

- A doc comment starts with the identifier's name: `// Server handles incoming requests.` That form is what `go doc` and pkg.go.dev render, and tooling relies on it.
- Every exported identifier gets a doc comment. A package gets one `// Package foo ...` comment, in one file (`doc.go` when it is long).
- Document the **contract**: what the caller must guarantee, what is returned on failure, whether the value is safe for concurrent use, and who owns the resources. "Returns a User" is visible in the signature already.
- `// Deprecated: use X instead.` is the recognized form; editors and linters surface it.
- Comment why, not what. `i++ // increment i` is noise; `// The API returns page numbers 1-based.` is information the code cannot carry.

## Tooling

| Tool | Role |
|---|---|
| `gofmt` / `gofumpt` | Formatting. Non-negotiable and not configurable; gofumpt is a stricter superset |
| `goimports` | Formatting plus import management and grouping |
| `go vet` | Correctness analyzers shipped with the toolchain; a subset runs during `go test` |
| `staticcheck` | The high-signal third-party analyzer set: dead code, misused stdlib, real bugs |
| `golangci-lint` | Runner that aggregates the above plus dozens more, configured per repo |
| `govulncheck` | Reachable vulnerabilities in the dependency graph (`security.md`) |

- `go vet` findings are close to always real. Treat them as build errors.
- Enable linters deliberately: `errcheck` (unchecked errors), `ineffassign`, `staticcheck`, `govet`, plus `bodyclose` and `contextcheck` for services. A maximal linter set produces noise that trains the team to ignore the output.
- Enforce formatting in CI (`gofmt -l . | grep .` fails the build), not in review comments.
- `//nolint:linter // reason` — with the reason. A bare `//nolint` is an unreviewable exception.

## Common Mistakes

| Mistake | Consequence | Fix |
|---|---|---|
| `utils`, `common`, `helpers` packages | Import cycles and a dumping ground nobody owns | Name the package after what it does |
| `user.UserService` | Stutter at every call site | `user.Service` |
| Layer-based packages (`models`, `handlers`) | Every feature change touches every package | Package per domain concept |
| `GetName()` | Non-idiomatic; reviewers stumble | `Name()` |
| Mixed receiver kinds | Interface satisfaction surprises | One kind per type |
| Interfaces defined next to their implementation | Consumers import more than they need | Define in the consumer (`interfaces.md`) |
| `init()` doing configuration or I/O | Untestable, order-dependent, silent | Explicit constructor |
| Naked returns in a long function | Reader cannot see what is returned | Explicit return values |
| A maximal golangci-lint config | Noise, then blanket `//nolint` | A curated set everyone honors |

## Back To SKILL.md

Interface placement and sizing: `interfaces.md`. Struct API decisions: `structs.md`. Error naming and contracts: `errors.md`.
