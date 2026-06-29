# CLAUDE.md

Guidance for Claude Code when working in this repository. The public overview is in [README.md](README.md);
the machine contract (JSON shapes, exit codes) is in [AGENTS.md](AGENTS.md). This file captures the
project-specific context those docs leave out.

**Required reading — ClawHub publishing standards (tracked, shared):** the rules for passing
ClawHub inspection live in `.claude/CLAWHUB_STANDARDS.md` and are imported below. Read and follow
them before changing any skill metadata, scopes, `permissions`, docs, or the data-type catalog.

@.claude/CLAWHUB_STANDARDS.md

**Required reading — shared CLI conventions (tracked, mirrored with `speediance-cli`):** the
cross-repo invariants for the config/auth/credential layer (per-user state dir, one app-dir
constant, `0600` secrets, self-describing discovery, fail-fast errors, advertised==actual) live in
`.claude/CLI_CONVENTIONS.md` and are imported below. That file is kept **byte-identical** with the
sibling `speediance-cli` repo — propose changes through the shared agent process before editing it.

@.claude/CLI_CONVENTIONS.md

## What this is (the "why")

`google-health-cli` is a **generic, read-only Google Health data extractor**. It owns OAuth2 login and the
Google Health **v4** REST wire, and emits health data as JSON. It is **self-contained** — no Python, no
external helper binary.

It is a **dumb data collector**: it returns the API's data points verbatim and does **no** filtering,
merging, labeling, or interpretation. Every consuming agent gets all the data and derives whatever it cares
about. For example, a downstream workout agent is the consumer that owns all the personal logic — keeping
elliptical sessions, computing Zone-2 bands, merging, and storing into its own log. None of that lives here.
(This tool used to do that sync itself; that was the wrong ownership and was removed.)

A prior Go CLI for the same API (`ghealth`) was used as a **reference only** — to learn the data-type
catalog and filter syntax. It had **zero runtime dependency** and has since been deleted; this tool is fully
self-contained and owes it nothing at runtime.

## Invariants — don't break these

- **Read-only — and the *metadata* must say so too.** The tool requests only the six read-only
  `googlehealth.*.readonly` scopes and never mutates. `data`/`api` expose no write operations. This extends
  to all *advertised capability*: the embedded catalog (`internal/api/datatypes.json`) may list **only**
  read-only operations (the `readOnlyOps` allowlist: `list`, `get`, `reconcile`, `rollup`, `dailyRollUp`).
  Never add `create`/`update`/`patch`/`delete`/`batchDelete` or any other mutating op, even if the upstream
  API defines it — `init()` in `datatypes.go` **panics at startup** on any op outside the allowlist, and
  `TestCatalogIsReadOnly` guards it.
- **Description must match behavior; warn about sensitive output.** Keep metadata, scopes, the
  `metadata.openclaw.permissions` block, and docs truthful and consistent with what the binary does, and
  keep the `SKILL.md` Privacy + `api get` warnings (guarded by `TestSkillDocWarnsAboutSensitiveOutput`).
  This is the short form of the ClawHub rules in `.claude/CLAWHUB_STANDARDS.md` (imported above) — follow
  that file for the full standard.
- **stdout is data; stderr is hints/logs/errors.** `data list` always prints a JSON array of raw points;
  counts and warnings go to stderr.
- **Raw fidelity.** `data list` emits each data point's bytes unchanged (`DataPoint.Raw`). Don't reshape.
- **Per-type filter formats are live-verified** (the API rejects the wrong one with
  `INVALID_DATA_POINT_FILTER_*`). They live in `internal/api/datatypes.go:formatTimeBound`:
  - `…civil_*` → civil wall-clock, **no** trailing `Z`
  - `…sample_time.physical_time` → RFC3339 instant (UTC `Z`)
  - `…date` → date-only `YYYY-MM-DD`
- **Catalog `defaultTimePath` is the *filterable* member**, which is not always the documented default —
  e.g. `sleep` filters on `interval.civil_end_time`, not `civil_start_time`. The embedded
  `internal/api/datatypes.json` records the working values.

## Dev commands

| Command | What it does |
|---|---|
| `make build` | Build the binary into `./bin` |
| `make test` / `make test-race` | Run tests (with the race detector) |
| `make lint` / `make fmt` / `make vet` | golangci-lint / gofumpt+goimports / go vet |
| `make check` | Full pre-commit gauntlet: `tidy fmt vet lint test-race` |

Go must be on your `PATH`, along with `$(go env GOPATH)/bin` (where `make lint`/`fmt` tools like
`gofumpt` and `golangci-lint` install). If they aren't, prepend them for the session — e.g. in PowerShell,
substituting your own Go install path:
`$env:Path = "C:\path\to\go\bin;$(go env GOPATH)\bin;$env:Path"`.

**Goldens:** `make golden` (the old Python oracle) is obsolete — the Python sources are gone. Regenerate the
Go-produced goldens with `UPDATE_GOLDEN=1 go test ./internal/cli/` (see `assertGolden`).

Run `make check` before committing.

## Releasing

Releases are **tag-driven**: `git tag vX.Y.Z && git push origin vX.Y.Z` (or Actions → Release →
Run workflow) triggers GoReleaser (`.goreleaser.yaml`), which cross-compiles, builds archives +
checksums, and publishes a GitHub Release. Version metadata is injected from the tag via ldflags —
there is **no version constant to bump**. The ClawHub publish workflow (`publish-clawhub.yml`) is
**independent of releases** — it republishes the skill whenever `SKILL.md` changes on `main` (or via
manual `workflow_dispatch`), so a `SKILL.md` fix reaches ClawHub on merge, not on tag.

- **Versioning: SemVer.** A backward-compatible change (e.g. the auto-migrated token-cache default in
  v1.3.0) is a **minor**; breaking the documented JSON shapes / exit codes (`AGENTS.md`) is a **major**.
- **Commit messages: Conventional Commits** (`feat:` / `fix:` / …). GoReleaser auto-groups the release
  changelog by these prefixes (`changelog.groups`): `feat:` → Features, `fix:` → Bug fixes, everything
  else → Other changes; `docs:`/`test:`/`chore:` are excluded. **Unprefixed commits still ship but read
  as "Other changes" — so prefix them, or the auto-notes degrade.** Squash-merge PRs with a `feat:`/`fix:`
  title so each release line is one clean entry.
- **Release notes are automatic on tag** — the grouped changelog plus a static install footer
  (`release.footer`). There is no `CHANGELOG.md` / per-release file to maintain by design; write good
  `feat:`/`fix:` subjects and the notes follow.

## Layout

- `cmd/google-health-cli/` — entry point.
- `internal/cli/` — Cobra commands: `doctor`, `types`, `data`, `rollup`, `sessions`, `api`, `auth`,
  `config`, `version`, `completion`. `rollup daily <type>` returns server-side daily aggregates via the
  `dataPoints:dailyRollUp` POST (civil-day buckets, reconciled across sources); it is the only way to read
  the rollup-only types (`active-minutes`, `total-calories`, `floors`, `calories-in-heart-rate-zone`,
  `time-in-heart-rate-zone`).
- `internal/api/` — v4 client (generic `ListDataPoints` + `RawGet` + `RollUpDaily`), the embedded 31-type
  catalog (`datatypes.json` / `datatypes.go`), and filter building.
- `internal/auth/` — OAuth2 loopback login and the `0600` token cache.
- `internal/config/` — config discovery and precedence (flags > env > file > defaults).
- `internal/health/` — exercise data-point parsing, used only by the `sessions` convenience command.
- `testdata/` — fixtures and golden files that pin the `sessions` output contract.
