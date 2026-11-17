# Stack Recipes

Pick the recipe matching the confirmed plan. Each recipe lists the folder tree, the commands to run, and which files to pull from `config-templates.md`. Adapt package/app names to whatever the user actually specified in the interview — the trees below use placeholder names (`web`, `api`, `ui`, `config`).

Every recipe assumes the safety check already passed and git initialization was already decided.

---

## Recipe A — pnpm workspaces + Turborepo (TypeScript) — the common default

Good default when the user has no strong opinion and the repo is JS/TS. Fast, simple mental model, great caching, minimal ceremony.

```
.
├── apps/
│   ├── web/
│   │   ├── package.json
│   │   ├── tsconfig.json
│   │   └── src/...
│   └── api/
│       ├── package.json
│       ├── tsconfig.json
│       └── src/...
├── packages/
│   ├── ui/
│   │   ├── package.json
│   │   └── src/index.ts
│   └── config/
│       ├── package.json
│       ├── eslint-preset.js
│       └── tsconfig.base.json
├── .github/workflows/ci.yml
├── .gitignore
├── .editorconfig
├── .nvmrc
├── package.json            (root)
├── pnpm-workspace.yaml
├── turbo.json
├── tsconfig.base.json
└── README.md
```

Steps:
1. `pnpm init` at root, then hand-edit root `package.json` per `config-templates.md` (private: true, workspaces via `pnpm-workspace.yaml`, root scripts delegate to `turbo run <task>`).
2. Write `pnpm-workspace.yaml` listing `apps/*` and `packages/*`.
3. Install Turborepo as a root devDependency, write `turbo.json` with pipeline entries for `build`, `dev`, `lint`, `test`, `typecheck` (mark `build` as depending on `^build` for correct ordering, `dev` as persistent/no-cache).
4. Scaffold each app/package with a real minimal working entrypoint (not an empty folder) — a real `package.json`, `tsconfig.json` extending the root base config, and enough source to actually run.
5. Write shared config: root `tsconfig.base.json`, plus lint config in `packages/config` if the user wants a shared preset rather than duplicated per-package config.
6. Write `.github/workflows/ci.yml` running install (with pnpm cache), then `turbo run lint test build` — use `--filter=...[HEAD^]` or Turborepo's affected-detection if the user wants affected-only CI.
7. If publishing is in scope, add Changesets (`@changesets/cli`), run `npx changeset init`, and wire a release workflow.
8. `pnpm install` at root to verify everything resolves, then `pnpm turbo run build lint test --dry-run` (or without `--dry-run` if the user wants a real first run) to confirm the graph is correct.

---

## Recipe B — pnpm/npm/Yarn workspaces, no orchestrator

For small repos where the user explicitly doesn't want Turborepo/Nx overhead. Root scripts call into each package directly (or use a lightweight tool like `npm-run-all`/`concurrently` for parallel dev servers).

```
.
├── apps/...
├── packages/...
├── package.json   (root — scripts use --filter/-w or concurrently, no turbo.json)
├── pnpm-workspace.yaml   (or "workspaces" field in root package.json for npm/Yarn)
├── .github/workflows/ci.yml   (loops installs + each package's scripts explicitly)
└── README.md
```

Keep this recipe genuinely minimal — that's the point of choosing it. Don't sneak in an orchestrator "for good measure."

---

## Recipe C — Nx (TypeScript, possibly polyglot)

Choose when the user wants generators, a dependency graph UI, or is anticipating a larger team/repo.

```
.
├── apps/
│   ├── web/
│   └── api/
├── libs/                    (Nx convention: "libs" not "packages")
│   ├── ui/
│   └── shared-types/
├── nx.json
├── package.json
├── pnpm-workspace.yaml (or npm/yarn equivalent — Nx supports all)
├── tsconfig.base.json
├── .github/workflows/ci.yml   (use nx affected commands)
└── README.md
```

Steps:
1. Use `npx create-nx-workspace@latest` non-interactively where possible (pass flags for package manager and preset) rather than hand-rolling `nx.json` from scratch — Nx's generators keep the config in the shape Nx's own tooling expects.
2. Use Nx generators to add each app/library (`nx g @nx/next:app web`, `nx g @nx/node:app api`, `nx g @nx/js:lib ui`, etc.) matching the frameworks confirmed in the interview, rather than hand-writing package.json/tsconfig for each — this is Nx's whole value proposition and hand-rolling fights the tool.
3. Wire CI around `nx affected -t lint test build` for speed on larger repos.
4. Verify with `nx show projects` (confirms every package registered) and `nx graph --file=graph.json` (or skip the file output if no need to inspect it) to sanity check the dependency graph.

---

## Recipe D — Python: uv workspace

For repos that are Python-first (or Python-only shared packages inside a polyglot repo).

```
.
├── apps/
│   └── api/
│       ├── pyproject.toml
│       └── src/api/...
├── packages/
│   └── shared/
│       ├── pyproject.toml
│       └── src/shared/...
├── pyproject.toml           (root — [tool.uv.workspace] members = ["apps/*", "packages/*"])
├── uv.lock
├── .python-version
├── .github/workflows/ci.yml
├── .gitignore
└── README.md
```

Steps:
1. Root `pyproject.toml` declares the workspace via `[tool.uv.workspace]` with `members`.
2. Each app/package gets its own `pyproject.toml`; internal dependencies between packages are declared as workspace sources (`{ workspace = true }` under `[tool.uv.sources]`) so `packages/shared` can be imported by `apps/api` without publishing it anywhere.
3. Use `ruff` for lint+format (single fast tool, common modern default) unless the user wants `black`+`flake8`/`isort` separately — ask if unspecified rather than assuming.
4. Testing via `pytest`, one `pytest.ini`/`pyproject.toml` `[tool.pytest.ini_options]` section at root, with each package's tests discoverable from root.
5. CI: `uv sync`, then `uv run ruff check`, `uv run pytest`.
6. Verify: `uv sync` at root, `uv run python -c "import shared"` from within `apps/api`'s environment (or run the app's actual entrypoint) to confirm workspace linking works.

---

## Recipe E — Go workspace (`go.work`)

```
.
├── apps/
│   └── api/
│       ├── go.mod
│       └── main.go
├── packages/
│   └── shared/
│       ├── go.mod
│       └── shared.go
├── go.work
├── go.work.sum
├── .github/workflows/ci.yml
├── .gitignore
└── README.md
```

Steps:
1. `go work init` at root, then `go work use ./apps/api ./packages/shared` (repeat per module).
2. Each module keeps its own `go.mod`/`go.sum`; the root `go.work` ties them together for local development without needing to publish `packages/shared` to a real module proxy.
3. Lint via `golangci-lint`, format via `gofmt`/`goimports` (near-universal Go defaults — no need to belabor this choice in the interview).
4. CI: `go build ./...`, `go vet ./...`, `go test ./...`, `golangci-lint run` — run once per module or from root depending on how `go.work` resolves it; verify both work.
5. Verify: `go build ./...` from root succeeds and actually produces binaries.

---

## Recipe F — Rust (Cargo workspace)

```
.
├── crates/
│   ├── api/
│   │   ├── Cargo.toml
│   │   └── src/main.rs
│   └── shared/
│       ├── Cargo.toml
│       └── src/lib.rs
├── Cargo.toml         (root — [workspace] members = ["crates/*"])
├── Cargo.lock
├── .github/workflows/ci.yml
├── .gitignore
└── README.md
```

Steps: root `[workspace]` table lists members; per-crate Cargo.toml declares path dependencies on sibling crates (`shared = { path = "../shared" }`). `cargo fmt` + `cargo clippy` for lint/format, `cargo test --workspace` for tests, `cargo build --workspace` to verify.

---

## Recipe G — Polyglot repo (e.g. TS frontend + Go or Python backend)

No single package manager spans languages, so the "orchestrator" is usually a thin task runner at the root plus per-language tooling inside each app, following whichever recipe above matches that app.

```
.
├── apps/
│   ├── web/        (Recipe A's app shape — pnpm-managed)
│   └── api/        (Recipe D or E's shape — its own lockfile/workspace)
├── packages/
│   └── shared-types/   (if types need to cross the language boundary, consider
│                        generating one language's types from the other, e.g.
│                        OpenAPI/JSON Schema as the source of truth, rather than
│                        hand-syncing two type systems — flag this trade-off to the user)
├── justfile   (or Makefile — root-level task runner: `just dev`, `just build`, `just test`
│               fan out to each app's own tooling)
├── .github/workflows/ci.yml   (separate jobs per language, can run in parallel)
├── .gitignore   (union of both ecosystems' ignores)
└── README.md
```

Be upfront with the user that polyglot repos have less "one command does everything" magic than single-language ones — a root task runner (`just`/`make`) fanning out to per-app scripts is the honest solution, not a fake unified build system.

---

## General notes that apply to every recipe

- **`.gitignore`** must actually match the stack(s) in use — `node_modules/`, `.turbo/`, `dist/` for JS/TS; `__pycache__/`, `.venv/`, `*.egg-info/` for Python; `/target` for Rust; compiled binaries for Go. Don't paste a generic catch-all that ignores half the wrong things.
- **README** is not optional in any recipe — see `config-templates.md` for the structure.
- Always run the real install/build/verify commands at the end (see SKILL.md "Verifying the scaffold") rather than trusting the generated config by inspection alone.
