# Interview Guide

This is the question bank behind the interview described in SKILL.md. It's organized into rounds you can ask in sequence. Adapt wording and skip anything already answered — this is a reference for coverage and rationale, not a script to read verbatim.

Where the environment supports `ask_user_input_v0`, prefer turning multiple-choice-style questions (package manager, orchestrator, CI provider, license) into button choices — it's faster for the user than typing, and keep open-ended questions (project name, package inventory, purpose) as plain text prompts.

---

## Round 1 — Project identity

- What's this project called? (repo name, and if different, the "product" name)
- One or two sentences: what is this actually for?
- Who's it for — just you, a small team, or something meant to onboard many contributors? This matters because CI rigor, docs depth, and contribution tooling (CODEOWNERS, PR templates, commit linting) are worth setting up for a team repo and often overkill for a solo weekend project. Don't assume — ask.
- Is this greenfield (nothing exists yet) or are there existing folders/code that need to be pulled in? If the latter, this may be a migration rather than a fresh scaffold — flag that the approach differs (see "Not a fit" note in SKILL.md description) and confirm the user still wants this skill to proceed.

## Round 2 — Package/app inventory

This is the round most likely to get a vague answer — push for specifics here more than anywhere else.

- List every app, service, and shared package you want to exist on day one. For each: a name, and one line on what it does.
- Common shapes to probe for if the user is unsure:
  - A web frontend + an API backend + shared types/schema package
  - Multiple frontends (web + admin dashboard) sharing a UI component library
  - A CLI tool + the library it wraps
  - Several backend microservices sharing a common utils/config package
  - A mobile app (React Native/Expo, Flutter) alongside a web app, sharing business logic
- Ask specifically about **shared packages** — most real monorepos have at least one (`packages/ui`, `packages/config`, `packages/types`, `packages/utils`). If the user only names "apps" with nothing shared between them, gently ask if that's intentional — sometimes it is (unrelated tools bundled for convenience), sometimes they just haven't thought about it yet.
- Is the list exhaustive for now, or should the scaffold anticipate future packages (e.g. pre-create an empty `packages/` convention with a README on how to add one) even if only 1-2 exist today?

## Round 3 — Language, framework, and tooling stack

- For each app/package named in Round 2: what language, and what framework (if any)? Don't assume uniformity — a monorepo can mix a Next.js app, a Python FastAPI service, and a Go CLI.
- If JS/TS is involved anywhere:
  - TypeScript or plain JS? (Default to TypeScript unless told otherwise, but ask — some users genuinely want plain JS.)
  - Framework specifics that affect scaffolding: Next.js/Remix/Vite+React/SvelteKit/plain Node, etc.
- Package manager: npm, pnpm, Yarn (Classic or Berry/PnP), or Bun? If the user has no preference, pnpm is the common modern default for JS/TS monorepos (fast, disk-efficient, strict dependency resolution) — say that's the default and ask if that's fine, don't just silently pick it.
- Monorepo orchestrator on top of workspaces — do they want one, and if so which?
  - **Turborepo**: simplest to adopt, great caching, good default for most JS/TS monorepos, works well with Vercel deployments.
  - **Nx**: more powerful (code generators, dependency graph visualization, more plugins), more opinionated, better fit for larger teams or when they want generators/scaffolding built in.
  - **Lerna**: older, mostly relevant now for publishing multiple npm packages with independent versioning; often paired with Nx these days.
  - **Rush**: Microsoft's tool, very rigorous, common in large enterprise TS monorepos; heavier setup.
  - **None** — plain workspaces with hand-written root scripts is a legitimate choice for small repos; don't push tooling on someone who explicitly wants minimal.
- For non-JS ecosystems:
  - Python: uv workspace (fast, modern, good multi-package support), Poetry with path dependencies, or Rye.
  - Go: `go.work` multi-module workspace.
  - Rust: native Cargo workspace.
- Linting/formatting: ESLint + Prettier (mature, widely supported) vs. Biome (fast, single tool, newer, fewer plugins) for JS/TS; language-native tools for others (`ruff`+`black` or `ruff format` for Python, `gofmt`+`golangci-lint` for Go, `rustfmt`+`clippy` for Rust).
- Testing framework(s) per language — Vitest/Jest for JS/TS, Pytest for Python, built-in `testing` package for Go, built-in test framework for Rust.
- Shared TypeScript config: a root `tsconfig.base.json` that per-package configs extend is close to universal in JS/TS monorepos — confirm this is wanted rather than fully independent configs per package.

## Round 4 — CI/CD, versioning, and release

- CI provider: GitHub Actions (default assumption if the repo will live on GitHub and no preference is given — say so explicitly), GitLab CI, CircleCI, or none for now.
- What should CI actually run? At minimum, lint + typecheck + test + build is standard. Ask if the orchestrator supports affected-only runs (Turborepo/Nx both do) — worth enabling since it keeps CI fast as the repo grows.
- Is anything in this repo going to be **published** (an npm package, a PyPI package, a Docker image to a registry)? If yes:
  - Versioning strategy: independent per-package versions vs. fixed/lockstep versioning across the whole repo.
  - Release tooling: Changesets (popular for JS/TS, generates changelogs from PR-time changeset files, plays well with Turborepo/Nx) vs. semantic-release (fully automated from commit messages, needs Conventional Commits) vs. manual.
  - If nothing is published (pure internal apps), skip this entirely rather than forcing release tooling nobody needs.
- Deployment: in scope for this scaffold, or purely local dev + CI checks for now? If in scope, where (Vercel, Fly.io, a container registry + k8s, plain VPS)? Don't build deployment pipelines for platforms the user hasn't chosen — ask rather than guess.

## Round 5 — Environment, containers, docs, and polish

- Environment variables: one `.env` at the repo root, or per-package `.env` files? Want `.env.example` files committed alongside real `.env` (gitignored)? Want runtime validation of env vars (e.g. a `zod` schema per app) so missing/malformed config fails fast instead of causing confusing runtime bugs?
- Containerization: does each app need a `Dockerfile`? Is a root `docker-compose.yml` wanted for local dev (e.g. spinning up a database alongside the apps)? If nothing needs a database or external service locally, this may not be needed yet — ask rather than adding it by default.
- License: MIT is the common default for anything that might go public; ask rather than assume, and skip entirely for closed/private projects if the user prefers.
- Documentation depth: a solid root README (project overview, folder structure, how to install/run/build/test) is always worth including. Beyond that, ask before adding:
  - `CONTRIBUTING.md` (worth it once more than one person touches the repo)
  - Architecture Decision Records (`docs/adr/`) — usually only worth it for teams
  - A dedicated docs site (Docusaurus, Nextra, Starlight) — only for repos where docs are a real deliverable, not a default
- Runtime version pinning: `.nvmrc`/`.node-version` (or `mise`/`asdf` if the user already uses one of those for multi-language pinning), and an `engines` field in `package.json`.
- Commit convention: Conventional Commits + commitlint (pairs well with semantic-release and Changesets) — worth it if the user cares about changelogs or automated releases, otherwise skippable.
- Pre-commit hooks: Husky + lint-staged (JS/TS ecosystem) or `pre-commit`/`lefthook` (language-agnostic) to run lint/format checks before every commit. Ask if they want this — it's a genuine workflow preference, some people find it annoying.

---

## After the interview: confirm before building

Once these rounds are done, restate the plan compactly:

```
Project: <name>
Purpose: <one-liner>
Packages:
  - apps/web      — <framework>, <language>
  - apps/api      — <framework>, <language>
  - packages/ui   — shared component library
  - packages/config — shared eslint/tsconfig
Package manager: <pnpm/npm/yarn/bun>
Orchestrator: <Turborepo/Nx/none/...>
Lint/format: <...>
Testing: <...>
CI: <GitHub Actions running lint/test/build, affected-only>
Versioning/release: <Changesets / none>
Containers: <yes/no, details>
License: <MIT/none/...>
```

Get an explicit go-ahead before writing files. This costs one message and prevents scaffolding the wrong thing.
