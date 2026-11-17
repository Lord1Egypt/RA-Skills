# Versions — Release Policy, the go Directive, and Upgrading

Go's compatibility promise is unusually strong: code that compiles today is expected to compile and behave the same on future Go 1.x releases. The consequence is that upgrades are usually boring — and that the few things which *do* change are gated behind explicit switches.

## Release Cadence and Support

- Two major releases a year, roughly February and August, numbered `1.N`. Patch releases (`1.N.x`) arrive as needed for security and serious bugs.
- **Each major release is supported until two newer ones exist** — in practice about a year, so `1.N` stops receiving security fixes when `1.N+2` ships. Running more than two releases behind means running unpatched.
- Being one release behind is a defensible policy; being four behind means every upgrade is now a batch of four sets of behavior changes at once. Which of the two a project wants is the `upgrade_cadence` variable (Configuration), not a judgement to re-litigate per repo.
- Patch releases are safe to take immediately. Major upgrades get the treatment below.

## The go Directive Is a Language Selector

The `go` line in `go.mod` is not documentation — it selects the **language semantics** applied to that module's files:

- `go 1.22` or higher activates per-iteration loop variables. The same source built by the same compiler behaves differently under `go 1.21` (`concurrency.md`).
- New syntax is rejected below its floor even when the installed toolchain supports it, which is the correct behavior: it keeps the module buildable by everyone who satisfies the declared line.
- A `//go:build go1.24` constraint selects files per version, and a per-file `//go:debug` line (`go >=1.21`) can set a GODEBUG default for the main module.
- `min_go` in Configuration records which floor the project targets; emit unguarded features only at or below it.

`toolchain go1.24.0` (`go >=1.21`) declares which toolchain to *run*. When the local Go is older than required, it downloads the right one automatically. `GOTOOLCHAIN=local` disables that, which is what a locked-down CI wants (`modules.md`).

## What Changed, By Release

The floors that affect everyday code (the same table appears in SKILL.md "Version Floors"; this list adds context):

| Release | Highlights |
|---|---|
| 1.13 | `errors.Is`/`As`/`Unwrap` and `%w` — the modern error model starts here |
| 1.16 | Modules on by default, `go:embed`, `io/fs`, `os.ReadFile`, `go install pkg@version`, `-mod=readonly` default |
| 1.17 | `//go:build` lines, module graph pruning (much smaller dependency graphs) |
| 1.18 | Generics, `any`, native fuzzing, workspaces |
| 1.19 | `GOMEMLIMIT`, GC CPU limiter, typed atomics (`atomic.Int64`), doc comment reformatting |
| 1.20 | `errors.Join`, `context.WithCancelCause`, coverage for binaries |
| 1.21 | `slices`/`maps`/`cmp`, `log/slog`, `min`/`max`/`clear`, `toolchain` directive, PGO generally available |
| 1.22 | **Per-iteration loop variables**, `for i := range 10`, method+wildcard patterns in `http.ServeMux`, `math/rand/v2` |
| 1.23 | Range-over-function iterators, `maps.Keys`/`Values` as iterators, unreferenced timers collectable without `Stop`, `unique` |
| 1.24 | Generic type aliases, `os.Root`, `testing.B.Loop`, `tool` directives in go.mod, `omitzero` JSON tag, weak pointers |
| 1.25 | Container-aware default `GOMAXPROCS`, `testing/synctest` |

Two of these change the meaning of existing code rather than adding to it — the loop variable in 1.22 and timer collection in 1.23 — and both are gated on the module's `go` line, so raising that line is the moment to re-read the affected code.

## The Upgrade Procedure

1. **Read the release notes** for every version you are skipping, not just the target. The "Minor changes to the library" section is where behavior differences hide.
2. Upgrade the **toolchain only**, leaving the `go` directive alone. Run `go build ./... && go vet ./... && go test -race -count=1 ./...`. Most upgrades stop here.
3. If something broke, look for a **GODEBUG compatibility switch**: Go ships `GODEBUG=<name>=<old-value>` escape hatches for behavior changes, so you can restore the old behavior, ship, and fix properly afterwards. The available names are listed in the release notes and in `runtime/godebug`.
4. Then raise the `go` directive in go.mod as a **separate commit**. This is the step that activates language changes; keeping it separate makes a bisect meaningful.
5. Re-run vet and the race-enabled suite, and re-run any benchmarks you track — performance changes between releases are usually improvements, and occasionally not (`performance.md`).
6. Update the CI matrix and the builder image in the same change, so local and CI toolchains do not diverge (`deployment.md`).

Upgrade one release at a time when you are behind. Four releases in one commit produces a failure you cannot attribute.

## Deprecations and Removals

- The Go 1 compatibility promise means removals are rare and slow. Deprecated identifiers stay: `ioutil` is deprecated in favor of `os` and `io` (`go >=1.16`) and still compiles.
- Deprecation is marked with `// Deprecated: ...` in the doc comment; `staticcheck` and editors surface it. Treat it as a scheduled task, not an emergency.
- Real behavior removals ship with GODEBUG switches and a stated horizon in the release notes — that is the mechanism to watch, not the deprecation comments.
- `GOEXPERIMENT` gates genuinely experimental work (for example `jsonv2` from `go >=1.25`). Experimental means the API can change or disappear: fine for evaluation, not for a public contract (`json.md`).

## Choosing a Floor For a Library

- A published library's `go` directive is a **requirement on its users**: anyone with an older toolchain cannot build it. Set it as low as the code allows, and raise it only for a feature you actually use.
- Applications have no such constraint — an application should track a recent release, because it gets performance and security work for free.
- A library that needs a newer feature in one place can gate that file with `//go:build go1.N` and provide a fallback, keeping the module's floor low.
- State the supported versions in the README and test them in CI. "Latest two releases" matches Go's own support window and is the default policy worth adopting.

## Back To SKILL.md

The floors table lives in SKILL.md "Version Floors"; `min_go` in Configuration gates what may be emitted. Module mechanics: `modules.md`. GODEBUG for diagnosis: `debugging.md`.
