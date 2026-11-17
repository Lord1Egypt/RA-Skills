# Build — Tags, Cross-Compilation, Embedding, cgo, Linker Flags

Go's build model is one command, no build file, and a small set of environment variables. The complexity lives in three places: build constraints, cgo, and what the linker puts in the binary.

## Build Constraints

```go
//go:build linux && (amd64 || arm64) && !nocgo

package thing
```

- The `//go:build` line (`go >=1.17`) must appear **before the package clause**, followed by a blank line. A constraint placed after the package clause is a plain comment and silently does nothing — the most common build-tag bug.
- The old `// +build` syntax still parses; `gofmt` keeps both in sync when both are present. New files use `//go:build` only.
- **Filename suffixes are constraints too**: `x_linux.go`, `x_windows.go`, `x_amd64.go`, `x_linux_arm64.go`. They apply automatically with no comment, and they are the cleaner way to split platform code. `_test.go` is the same mechanism.
- Custom tags: `//go:build integration` plus `go test -tags=integration ./...` keeps slow suites out of the default run (`testing.md`).
- `//go:build ignore` on a `package main` file excludes it from the build and is how `go generate` helper programs live in the tree.
- A file excluded by every constraint on every platform is invisible to `go vet` and to your editor — dead code that compiles nowhere and rots quietly.

## Cross-Compilation

```bash
CGO_ENABLED=0 GOOS=linux   GOARCH=amd64 go build -o bin/app-linux-amd64  ./cmd/app
CGO_ENABLED=0 GOOS=darwin  GOARCH=arm64 go build -o bin/app-darwin-arm64 ./cmd/app
CGO_ENABLED=0 GOOS=windows GOARCH=amd64 go build -o bin/app.exe          ./cmd/app
go tool dist list                     # every supported GOOS/GOARCH pair
```

- With `CGO_ENABLED=0` cross-compilation needs no toolchain for the target — that is Go's distribution advantage, and it disappears the moment a dependency needs cgo.
- `GOARCH=arm` additionally needs `GOARM` (5, 6, 7); `GOARCH=amd64` accepts `GOAMD64=v1..v4` micro-architecture levels, where anything above v1 will `SIGILL` on older CPUs.
- Build for the platform you deploy on, not the one you develop on: an arm64 laptop building for an amd64 server without `GOARCH` produces a binary the server cannot execute (`deployment.md`).
- `go vet` and tests do not run cross-platform. Platform-specific code needs a CI matrix, or its bugs ship.

## cgo

- `CGO_ENABLED=1` (the default when a C toolchain is present) turns on cgo. Consequences, all at once: cross-compilation needs a target C toolchain, the binary links against the host libc, build times grow, and the resulting binary is not static.
- The Alpine trap: a binary built on Debian with cgo links glibc and dies on Alpine (musl) with "no such file or directory" pointing at an interpreter that exists — the message names the dynamic loader, not the binary. Build with `CGO_ENABLED=0`, or build on the target's libc (`deployment.md`).
- DNS resolution changes with cgo: `CGO_ENABLED=1` uses the system resolver (honoring `nsswitch.conf` and NSS modules), `CGO_ENABLED=0` uses Go's pure-Go resolver. Split-horizon corporate DNS can therefore resolve in one build and fail in the other. `GODEBUG=netdns=go|cgo|2` forces and traces the choice.
- Each cgo call crosses a stack boundary and costs on the order of tens of nanoseconds versus a couple for a Go call — irrelevant once per request, fatal inside a per-pixel loop. Batch at the boundary.
- Memory rules: Go pointers passed to C must not point to memory containing Go pointers, and C must not retain a Go pointer after the call returns. Violations are caught by `GODEBUG=cgocheck=1` and corrupt the heap when they are not.
- `cgo` blocks the race detector's view into C code and makes the goroutine that calls it hold an OS thread for the duration.
- Common libraries that pull cgo in: `mattn/go-sqlite3` (pure-Go alternatives exist), image codecs, and some crypto bindings. `cgo` in Configuration records the project's stance.

## go:embed

```go
import _ "embed"                 // needed for the string/[]byte forms

//go:embed templates/*.html
var templates embed.FS

//go:embed VERSION
var version string
```

- The directive must sit immediately above a package-level `var` with no blank line between them.
- Paths are relative to the **source file's directory** and cannot escape it: no `..`, no absolute paths, no symlinks out. A `web/` directory outside the package needs its own package with its own embed file.
- By default `*` does not match files starting with `.` or `_`. `//go:embed all:static` includes them — the standard fix for a missing `.well-known` or a `_next` directory in an embedded frontend.
- An `embed.FS` satisfies `fs.FS`, so the same handler code serves from disk in development and from the binary in production (`io.md`).
- Everything embedded is in the binary and in memory when touched. A 200 MB asset directory produces a 200 MB binary.

## Linker Flags and Binary Size

```bash
go build -trimpath -ldflags "-s -w -X main.version=$(git describe --tags)" ./cmd/app
```

- `-X importpath.name=value` sets a **string** package-level variable at link time — the standard way to stamp a version. It works only on strings, and only on variables that are not constants.
- `-s -w` strip the symbol table and DWARF debug info, typically shaving on the order of 20-30% off the binary. It also makes the binary undebuggable with delve and degrades panic stack traces — measure before adopting it in a service you may need to profile (`debugging.md`).
- `-trimpath` removes local filesystem paths from the binary: smaller, reproducible, and it stops leaking `/Users/you/...` in stack traces.
- From `go >=1.18` the build embeds VCS revision and dirty state, readable through `runtime/debug.ReadBuildInfo()` — a `--version` flag can work with no `-X` at all (`cli.md`).
- Go binaries are large because the runtime and reflection metadata ship with them; a few MB is normal. If size is critical, the levers are `-s -w`, `-trimpath`, and dropping dependencies — not compression tricks that break `exec`.

## go generate and Tools

- `go generate ./...` runs `//go:generate` directives and **never runs automatically** as part of a build. Generated files are committed, and CI verifies them by regenerating and diffing.
- Pin tool versions. `go >=1.24` supports `tool` directives in go.mod (`go get -tool …`, then `go tool <name>`), replacing the older `tools.go` file with blank imports under a build tag (`modules.md`).
- Generated files carry the standard header line `// Code generated by X. DO NOT EDIT.` — linters, coverage tools, and reviewers all key on that exact form.

## Reproducibility and Caching

- The build cache lives in `go env GOCACHE`; `go clean -cache` empties it. `go build -a` forces a full rebuild and is almost never necessary — reach for it only when you suspect cache corruption.
- Reproducible builds need `-trimpath`, a pinned toolchain version, and either vendoring or a fixed module graph. `GOFLAGS` set in the environment silently changes builds; print `go env` in CI logs.
- Cross-compiling in CI is faster than a per-arch runner matrix for pure-Go binaries, and impossible for cgo ones — that trade is usually what decides the pipeline shape.

## Back To SKILL.md

Container images and static binaries: `deployment.md`. Dependency resolution: `modules.md`. Build tags for slow tests: `testing.md`.
