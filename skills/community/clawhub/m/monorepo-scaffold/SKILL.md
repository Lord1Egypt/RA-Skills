---
name: monorepo-scaffold
description: Initialize a brand-new monorepo project in an empty (or near-empty) folder. Use when the user wants to "set up a monorepo", "scaffold a project", or "bootstrap a repo with multiple packages/apps"; mentions Turborepo, Nx, pnpm/Bun/Yarn workspaces, Lerna, Rush, uv workspace, Cargo workspace, or Go workspaces for something new; or describes several apps/packages/services sharing tooling. Trigger even on vague asks like "start a project with a frontend and backend" or "a workspace for my packages". Runs a mandatory deep interview (identity, package/app inventory, stack per package, package manager & orchestrator, shared tooling, CI/CD, versioning/release, git & hooks, containers, env strategy, docs) before writing any file, then generates a complete, production-grade skeleton, not a toy example. Do NOT use to add one package to an existing monorepo, migrate a large codebase, or scaffold a single standalone app with no shared packages.
---

# Monorepo Scaffold

## Why this skill exists

A monorepo is a long-lived piece of infrastructure. The workspace tool, package manager, folder layout, and shared config choices made on day one are expensive to change later — teams live with them for years. Because of that, this skill treats scaffolding as a **design decision that deserves a real interview**, not a quick default. Guessing the stack and generating something generic is worse than useless here: it produces a skeleton the user has to tear apart and redo, which is slower than if Claude had just asked.

So the rule is simple: **never scaffold before the interview is genuinely complete.** A partial answer ("just use TypeScript") is not complete — dig into the specifics (which package manager, which orchestrator, which apps). It is fine, and expected, for the interview to feel thorough. That's the point.

## Overall flow

1. **Confirm the target folder is safe to scaffold into** (see "Safety check" below).
2. **Run the full interview** (see "The interview" below). Do this in a conversational, adaptive way — don't just dump a giant questionnaire. Ask in focused batches, use the `ask_user_input_v0` tool where available (single-select/multi-select buttons are much faster for the user than typing), and adapt follow-ups to earlier answers.
3. **Summarize the plan back to the user** as a short spec (project name, apps/packages list, stack per package, orchestrator, CI, versioning strategy) and get explicit confirmation before writing files. This is cheap insurance against a wasted scaffold.
4. **Generate the monorepo** following the relevant recipe in `references/stack-recipes.md`, using `references/config-templates.md` for boilerplate config file contents.
5. **Verify** the scaffold: run the package manager's install command, run the build/lint/test scripts if they exist, and confirm the workspace tool actually recognizes all packages (e.g. `turbo run build --dry`, `nx show projects`, `pnpm -r list`).
6. **Report back** with the folder tree, how to install dependencies, how to run each app, and a short "next steps" list (e.g. "add your first real feature to `apps/web`", "set up secrets in CI").

## Safety check

Before touching the filesystem:
- Confirm the target directory exists and list its contents. If it's not empty, stop and tell the user what's already there, then ask whether to proceed (merge into existing files), scaffold into a subfolder instead, or abort. Never silently overwrite existing files.
- Confirm whether the user wants git initialized here, or whether this folder is already inside a git repo (check for a `.git` directory, including in parent directories) — don't run `git init` inside an existing repo without asking.

## The interview

Treat this as a structured but human conversation. Group questions into rounds so the user isn't overwhelmed by twenty questions at once — three or four short rounds work better than one wall of text. Skip a question only if the user has already answered it earlier in the conversation. Never silently assume an answer to a question in the "always ask" list below.

Read `references/interview-guide.md` for the full question bank, good follow-up probes, and rationale for why each topic matters. At minimum, the following must be resolved by the end of the interview — treat these as required, not optional:

1. **Project identity** — project/repo name, one-line purpose, intended scale (a weekend project vs. something meant to scale to a team of 50 — this changes how much tooling rigor is worth setting up).
2. **Package/app inventory** — the concrete list of apps, services, and shared packages that will live in the repo on day one (e.g. `apps/web`, `apps/api`, `packages/ui`, `packages/config`). Push for specifics; "a frontend and a backend" is a start, not an answer — get names and what each one is responsible for.
3. **Language & framework per package** — this can differ per package (e.g. a Next.js web app, a Go API, a shared TypeScript types package). Never assume everything is the same language just because the first package is.
4. **Package manager & monorepo orchestrator** — for JS/TS: npm workspaces, pnpm workspaces, Yarn (classic or Berry) workspaces, or Bun workspaces, plus whether to layer Turborepo, Nx, Lerna, or Rush on top (or none). For Python: uv workspace, Poetry with path dependencies, or Rye. For Go: `go.work`. For Rust: Cargo workspace. For polyglot repos: how the pieces coexist (often plain folder convention plus a task runner like `just`, `make`, or Turborepo's generic task pipeline). Explain trade-offs briefly rather than just listing options — the user may not know these tools.
5. **Shared tooling** — linting/formatting (ESLint+Prettier vs. Biome vs. language-native equivalents), TypeScript config strategy (shared base `tsconfig.json` with per-package extends), testing framework(s), pre-commit hooks (Husky+lint-staged, `pre-commit`, `lefthook`).
6. **CI/CD** — which provider (GitHub Actions is the sane default unless told otherwise), what the pipeline should do (lint, typecheck, test, build — and only run tasks affected by a given change if the orchestrator supports it), and whether deployment is in scope yet or comes later.
7. **Versioning & release strategy** — only relevant if any package will be published (npm, PyPI, etc.) or has independent release cadence. Options include Changesets, semantic-release, or "not needed yet." Don't over-engineer this for an app-only repo with nothing to publish.
8. **Environment & secrets strategy** — per-package `.env` files vs. a root-level shared one, whether to add runtime env validation (e.g. `zod`-based env schemas, `envsafe`), and whether `.env.example` files are wanted.
9. **Containerization** — Docker per app, a root `docker-compose.yml` for local dev, or skip entirely for now.
10. **License and documentation depth** — license choice (MIT is the common default for open work, but ask), and how much scaffolding docs to generate (a solid root README is always included; ask before adding CONTRIBUTING.md, ADRs, or a docs site).

Also worth surfacing, but fine to default sensibly if the user has no opinion (say what you're defaulting to, don't just silently pick): Node/runtime version pinning (`.nvmrc`, `engines` field, or Volta/mise), commit message convention (Conventional Commits + commitlint), and editor consistency (`.editorconfig`).

Do not let the interview become a stalling tactic — once the required items above are resolved, move to confirmation and scaffolding. Overkill means thorough, not endless.

## Generating the scaffold

Once the plan is confirmed:

1. Open `references/stack-recipes.md` and find the recipe matching the chosen package manager/orchestrator combination. If the combination isn't covered exactly (e.g. an unusual polyglot mix), use the closest recipe as a base and adapt — explain the adaptation to the user.
2. Use `references/config-templates.md` for the actual contents of common files (root `package.json`, `turbo.json`/`nx.json`, base `tsconfig.json`, `.eslintrc`/`biome.json`, `.gitignore`, GitHub Actions workflow, `.editorconfig`, `.nvmrc`, Changesets config, Dockerfiles, `docker-compose.yml`) so output is consistent and doesn't need to be reinvented per run.
3. Build the actual folder tree and files using the sandbox's file tools — don't just describe the structure, create it for real.
4. Every app/package gets its own minimal-but-real starter (a working "hello world" that actually runs), not an empty folder — an empty `apps/web/` with no `package.json` isn't a scaffold, it's a TODO.
5. Wire up root-level scripts so the primary commands work immediately: install, dev (run everything relevant), build, lint, test. These should be one command each from the repo root.
6. Initialize git (if agreed in the safety check) with a sensible first commit and a `.gitignore` that actually matches the stack (not a generic catch-all).

## Verifying the scaffold

Before declaring done, actually prove it works rather than assuming the generated config is correct:
- Run the install command for the chosen package manager.
- Run whatever "list packages"/"show projects" command the orchestrator provides, and confirm every package the user asked for shows up.
- Run lint, typecheck, and test scripts if configured, and fix any issue caused by the scaffold itself (not the user's future code).
- If a dev server was set up, at least confirm it starts without crashing (then stop it — don't leave a long-running process hanging).

If the sandbox's network access can't reach the package registry needed (npm, PyPI, crates.io, etc.), say so plainly, still generate every file, and tell the user exactly which command to run locally to finish installing.

## Final report

Close with, in this order:
1. The folder tree (a real tree, not prose).
2. Exact commands to install and run things.
3. A short list of the concrete choices made (orchestrator, package manager, CI provider) so the user has a record.
4. Sensible "what to do next" pointers — don't pad this, three to five items is plenty.

If a file-delivery tool is available in the current environment (e.g. `present_files`), zip the generated project and present it; otherwise the files are already on disk in the working directory and the report should say where.
