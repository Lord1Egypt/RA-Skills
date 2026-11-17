---
name: goenv
description: Go library that reads one environment variable and tells you if you're in prod or dev. `github.com/psyb0t/goenv` wraps `os.Getenv("ENV")` behind three calls. `goenv.Get()` returns the current env as a string (`"prod"` or `"dev"`), `goenv.IsProd()` and `goenv.IsDev()` return bools. It recognizes exactly two environments, `dev` when `ENV` is precisely `"dev"`, and `prod` for everything else (unset, empty, `"production"`, `"DEV"`, anything), a fail-safe default to prod. Exposes constants `goenv.Prod`/`goenv.Dev` and the env-var name as `goenv.EnvVarName`. Zero dependencies beyond the stdlib `os`; no network, no files, no config. Note `Type` is a string *alias*, so it gives no compile-time safety over a bare `string`. Use when the user wants a tiny dependency-free prod/dev switch in a Go program, or is already importing goenv and wants to branch behavior on the environment.
homepage: https://github.com/psyb0t/goenv
user-invocable: true
metadata:
  openclaw:
    emoji: "🌍"
    primaryEnv: ENV
    requires:
      bins:
        - go
permissions:
  filesystem: "Guides adding one import and a few calls to your project's own Go source, and edits `.go` files in the current project only. The library itself writes nothing."
  shell: "The Go toolchain (`go get` / `go build` / `go test`) to add and compile the dependency. No other host access."
  network: "`go get` fetches the module from your configured Go module proxy the first time. The library makes no network calls at runtime."
---

# goenv

A Go library that reads a single environment variable, `ENV`, and answers one question: are you in `prod` or `dev`? That's the whole package. `os.Getenv("ENV")` with a fail-safe default and three named helpers, zero dependencies. Import it and call `goenv.Get()`.

For install, the exact match/default behavior, and a worked example, see [references/setup.md](references/setup.md).

## Security & safety

- **It reads exactly one environment variable, `ENV`, and nothing else.** No other env vars are read, nothing is written to disk, no network calls are made at runtime, and no data leaves your process. Its only import is the stdlib `os`.
- **It's a library you compile into your own binary**, so it has no runtime surface of its own. Whatever your program does with the prod/dev answer is on you, same as any code you'd write by hand.
- **Fail-safe by design:** an unrecognized or unset `ENV` resolves to `prod`, so a misconfigured environment errs toward production-grade behavior rather than accidentally enabling dev-only shortcuts.

## When to use

- A Go program needs a small, dependency-free way to branch behavior between two environments (prod vs dev), e.g. verbose logging in dev, stricter defaults in prod.
- The project already imports `github.com/psyb0t/goenv` and you want to add or read a prod/dev check consistently (`goenv.IsProd()` / `goenv.IsDev()` instead of hand-rolled `os.Getenv` comparisons).
- You want the fail-safe "default to prod" semantics without writing the switch yourself.

## When NOT to use

- You need **more than two environments** (staging, test, ci, local, …): goenv only knows `dev` and `prod`; everything that isn't exactly `"dev"` collapses to `prod`.
- You need to read env vars **other than `ENV`**, or a configurable variable name: goenv reads the hardcoded `ENV` and nothing else. Reach for a real config library (e.g. `gonfiguration`) for anything richer.
- You expect **compile-time type safety** from the `Type` type: it's a `string` alias, so `goenv.Type` *is* `string`; the constants are conveniences, not an enum, and any string is assignable. If you need a distinct nominal type, this isn't it.

## Usage

```go
import "github.com/psyb0t/goenv"

// The current environment as a string ("prod" or "dev"):
switch goenv.Get() {
case goenv.Dev:
    // dev-only behavior
default: // goenv.Prod
    // prod behavior
}

// Or the boolean shortcuts:
if goenv.IsDev() {
    logger.SetLevel("debug")
}
if goenv.IsProd() {
    enableStrictMode()
}

// The recognized values and the variable name are exported constants:
_ = goenv.Prod         // "prod"
_ = goenv.Dev          // "dev"
_ = goenv.EnvVarName   // "ENV"
```

The mapping is exact: `Get()` returns `Dev` only when `ENV` is precisely `"dev"`; every other value (unset, empty, `"DEV"`, `"development"`, `"prod"`, or anything else) returns `Prod`. Set it before your process starts:

```bash
ENV=dev  ./yourapp     # dev
ENV=prod ./yourapp     # prod
./yourapp              # ENV unset → prod (the default)
```

For the module path, supported Go version, and the full behavior table, see [references/setup.md](references/setup.md).
