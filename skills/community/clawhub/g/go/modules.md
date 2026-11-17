# Modules — go.mod, Versions, and Dependency Failures

Go's dependency resolution is Minimal Version Selection: the build uses the **highest version any module in the graph explicitly requires**, and nothing newer. That single rule explains most surprises here — including the ones where "it should have upgraded".

## The Files

- `go.mod` — module path, `go` directive, `require`, `replace`, `exclude`, `retract`, `toolchain`. Edit it with commands (`go get`, `go mod tidy`) rather than by hand; hand edits are legal but easy to leave inconsistent.
- `go.sum` — cryptographic hashes of every module version in the graph, including ones not currently used. **Commit it.** It is not a lockfile in the npm sense: it does not choose versions, it verifies the ones MVS chose.
- The `go` directive is a **language-version selector**, not just metadata: it gates per-iteration loop variables, new syntax, and some behavior changes, per file. Raising it can change the meaning of existing code (`versions.md`).
- `toolchain` (`go >=1.21`) declares which Go toolchain to use, and a newer one is downloaded automatically when the local Go is older than required. `GOTOOLCHAIN=local` disables that if your CI must pin exactly what it installed.

## Version Selection

- MVS is deterministic and does not silently upgrade. Adding a dependency that requires `x v1.4.0` when you require `v1.2.0` builds with `v1.4.0` — the maximum of the *required* versions, still not the latest published.
- `go get example.com/x@v1.5.0` sets an explicit requirement. `go get -u ./...` upgrades direct and indirect dependencies to their latest minor/patch; `go get -u=patch` restricts it to patch releases.
- `go mod tidy` adds what the code imports, removes what it does not, and rewrites `go.sum`. It also downloads test dependencies of your dependencies, which is why it needs network access even when the build does not.
- `go list -m -u all` shows available upgrades without applying them. `go mod graph` prints the full requirement edges; `go mod why -m <module>` explains why a module is in the build at all — the first command to run when an unexpected dependency appears.
- Pseudo-versions (`v0.0.0-20240115120000-abcdef123456`) encode a timestamp and commit for modules with no tags. They order by timestamp, so a pseudo-version always sorts below a later real tag.

## Major Versions

- **v2 and above must carry the major version in the module path**: `module example.com/x/v2`, imported as `example.com/x/v2`. Without it, `go get example.com/x@v2.0.0` fails with an "invalid version: should be v0 or v1" style error.
- The consequence is that v1 and v2 of the same library are *different modules* and can coexist in one build. That is deliberate — it is what makes a gradual migration possible when a transitive dependency pins the old major.
- Publishing v2 means updating the module path, every internal import, and the import path in your README. A subdirectory `/v2/` layout is one option; a branch is another.
- `retract` in go.mod marks your own published versions as withdrawn, so `go get` skips them and `go list -m -versions` shows the retraction. It is the only way to un-publish, because the module proxy is immutable.

## replace, exclude, workspaces

- `replace` is honored **only in the main module's go.mod** — a `replace` in a library you depend on is ignored. Libraries therefore cannot patch their own transitive dependencies, and a published module with a `replace` pointing at a local path is broken for everyone.
- Local development against an unpublished change: `replace example.com/x => ../x`. Remove it before tagging a release, or use a workspace instead.
- `go work` (`go >=1.18`) is the supported multi-module local setup: `go work init ./api ./worker ./shared` creates `go.work`, which overrides module resolution for everything inside it. **Do not commit `go.work`** in a library repo — it changes the build for anyone who checks out the tree. Committing it is defensible in a private monorepo where everyone wants the same overlay.
- `exclude` blocks a specific bad version; MVS then picks the next acceptable one. Rare, and usually a sign the right fix is an explicit `require` of a fixed version.

## Private Modules and the Proxy

- Default flow: `GOPROXY=https://proxy.golang.org,direct` and `GOSUMDB=sum.golang.org`. Every public module is fetched through the proxy and verified against the checksum database.
- `GOPRIVATE=github.com/mycorp/*` is the one variable to set for private code: it implies `GONOPROXY` and `GONOSUMDB`, so those paths bypass both the proxy and the checksum database.
- Git authentication for private repos: a `.netrc`, an SSH rewrite (`git config --global url."git@github.com:".insteadOf "https://github.com/"`), or a token. The failure mode is a `410 Gone` or a terminal prompt hanging in CI — set `GIT_TERMINAL_PROMPT=0` so it fails fast instead.
- Vendoring: `go mod vendor` writes `vendor/`, and with `go >=1.14` its presence makes `-mod=vendor` the default. It guarantees a hermetic build with no network, at the cost of a large diff on every dependency change. Choose it for air-gapped or compliance builds, not by default.
- `GOFLAGS=-mod=readonly` (the default from `go >=1.16`) makes the build fail rather than silently editing go.mod — keep it, and run `go mod tidy` deliberately.

## Errors and What They Mean

| Error | Cause | Fix |
|---|---|---|
| `missing go.sum entry for module ...` | Requirement added without updating sums | `go mod tidy`, or `go mod download <module>` |
| `checksum mismatch` / `SECURITY ERROR` | The module's content changed for a version already recorded | Do not bypass. Verify upstream; a retagged release is the benign cause, tampering is the other one |
| `ambiguous import: found package X in multiple modules` | Two modules provide the same import path, usually a pre-modules fork | `go mod why` both, then drop or `replace` one |
| `module declares its path as X but was required as Y` | Repo was renamed, or v2+ without the `/v2` suffix | Require the declared path |
| `updates to go.mod needed; to update it: go mod tidy` | `-mod=readonly` doing its job | Run tidy, review the diff |
| `invalid version: unknown revision` | Tag deleted, branch renamed, or private repo without auth | Check access first, then the tag |
| `go.mod requires go >= 1.x (running go 1.y)` | Dependency needs a newer toolchain | Upgrade Go, or pin the dependency lower |

## Hygiene

- Commit `go.mod` and `go.sum`; verify in CI with `go mod tidy && git diff --exit-code` so a drifting go.mod fails the build rather than a colleague's laptop.
- `go mod verify` re-checks the downloaded module cache against go.sum.
- `govulncheck ./...` reports known vulnerabilities that your code actually **reaches** in the call graph, which is what makes it usable compared with a plain dependency scan (`security.md`).
- Upgrade on a cadence, in small batches, with the test suite and `-race` — a six-month batch upgrade is unreviewable and unbisectable. The cadence itself is the `upgrade_cadence` variable (Configuration, default `monthly`); under `security-only` the trigger is a `govulncheck` finding rather than the calendar.
- Keep the dependency count deliberate. Every module is code you ship, a supply-chain surface, and a future upgrade obligation; the standard library covers more than most Go projects assume.

## Back To SKILL.md

Language-version effects of the `go` directive: `versions.md`. Build flags and vendoring at compile time: `build.md`. Vulnerability scanning: `security.md`.
