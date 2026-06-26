---
name: git-worktree-setup
description: Use when the user explicitly asks to "generate / update a git worktree auto-setup script for this repo." Note this skill is NOT triggered when a new worktree is created — the script and hook it produces are. Workflow is audit-the-repo-first, propose a draft plan, ask the user only the questions you can't infer, then write the tailored setup-worktree script + matching agent-tool hook config (Claude Code SessionStart / WorktreeCreate, Codex/Cursor manual + git hook, Gemini CLI, etc.). Also used to update an existing script as the project structure evolves.
license: MIT
compatibility: Works with any agent that supports the Agent Skills format (Claude Code, Codex, Cursor, OpenCode, Gemini CLI, etc.). Generated setup script requires bash + git + standard POSIX utils (grep, awk, ln, cp, shasum).
---

# Git Worktree Setup

## What this skill is / is not

**Produces**: a tailored `scripts/setup-worktree.sh` (or similar) for the current repo + the matching agent-tool hook config that auto-invokes it + a manual entry-point as a safety net.

**Is NOT**: the thing that runs every time a new worktree is created. **That's the hook.** This skill only runs when the user explicitly asks for it:
- "Set me up worktree auto-bootstrap"
- "Every `git worktree add` requires me to manually install / copy `.env` — automate it"
- "Project structure changed — update the worktree init script"

**Core working style: audit the repo yourself → put a concrete draft on the table → ask only the questions you couldn't infer → land it.**

Don't dump 7 questions on the user upfront — that's annoying. Read the code, read the configs, infer everything inferable, **walk in with a draft proposal**, and let the user adjust.

## 4-step workflow

### Step 1: Audit the repo yourself (do not ask the user)

**This is dynamic inference, not checking boxes off a static list.** The table below is **examples of common signals** — you must expand the investigation based on what you actually find. Any tool, any stack, any project-specific convention is fair game. Read unfamiliar config files; grep for unknown CLI names; if the README / CONTRIBUTING / Makefile / justfile / Taskfile mentions "setup" / "bootstrap" / "install" steps, read them — they often hold the repo's own definition of "what a fresh machine needs."

**Starting signals (examples, not exhaustive):**

| What to look at | What to infer |
|---|---|
| `package.json` (root + `workspaces` field) | npm/pnpm/yarn? monorepo? what workspace globs? |
| `pnpm-workspace.yaml` / `lerna.json` / `nx.json` / `turbo.json` | confirms monorepo tooling |
| `pyproject.toml` / `Pipfile` / `uv.lock` / `requirements.txt` | Python? poetry / uv / pip? share `.venv`? |
| `Cargo.toml` (with `workspace` section) | Rust? share `target/`? |
| `go.mod` | Go? usually nothing to share |
| `Gemfile` / `mix.exs` / `composer.json` / `pubspec.yaml` etc. | other ecosystems — infer their deps dirs analogously |
| `.gitignore` | hunt ignored entries: `node_modules` / `.venv` / `.env` / `dist` / `*.state` etc. — these are the share/copy candidates; don't skip unfamiliar ignores either, they're often project-specific cache |
| `.env.example` / `.dev.vars.example` / `apps/*/.dev.vars.example` / `config/*.example` | hints at which secret / config files need Copy |
| `docker-compose*.yml` / `compose.yml` / `Dockerfile.dev` | stateful services list (pg/redis/mysql) + volume paths + host port bindings |
| `wrangler.toml` / `fly.toml` / `serverless.yml` / `terraform/*` etc. | various IaC / platform configs often imply a local state directory |
| Existence of `.claude/` / `.cursor/` / `.codex/` / `.aider*` / `.opencode/` etc. | infer the user's current agent tooling |
| `Makefile` / `justfile` / `Taskfile.yml` / `bin/setup` / `script/bootstrap` | project's own setup entry point — its install / link / copy steps are gold for worktree bootstrap |
| "Getting started" / "Local dev" sections in `README.md` / `CONTRIBUTING.md` / `docs/setup*.md` | the human-language "what a fresh machine needs" list |
| `.github/workflows/*.yml` / `.gitlab-ci.yml` etc. | how CI sets up the env ≈ what local probably needs |
| `scripts/setup-worktree.sh` / `scripts/setup-worktree.sh` / `bin/worktree-*` etc. | already exists? → decide new-build vs update mode |
| Whether main repo's `node_modules/`, `apps/*/node_modules/`, `.venv/` etc. actually exist on disk | validates the inference + tells you what's currently linkable |
| **Any unfamiliar top-level directory** | e.g. `references/`, `vendor/`, `third_party/`, `fixtures/` — could be deliberate shared resources; ls inside before asking (symlinks? large files? test data?) |

**Expand actively**: each of the above can lead to further investigation. Reading `package.json`, you spot `husky` → check whether `.husky/` should be shared. You spot `playwright` → check whether browser cache (`~/.cache/ms-playwright`) should be shared. Reading `pyproject.toml`, you find `[tool.uv]` → where does uv put its cache. **Don't skip just because something isn't in the table.**

By the end of audit you should have:
- a **resource candidate list** pre-classified into Share / Copy / Generate, each item with its source evidence
- the **inferred agent tool** (based on config dir presence)
- whether a **script already exists** (decides new vs update)
- the **open questions worth asking** (items audit can't decide but are decision-critical)

### Step 2: Walk in with a concrete draft (don't bombard with questions)

Aggregate the audit into a **resource list proposal**, three tiers laid out. **Give a concrete recommendation for what you can infer**; **mark "needs confirmation" for what you can't**. Example:

> I went through the repo: looks like an npm-workspaces monorepo (`apps/api`, `apps/web`, `packages/*`), Cloudflare Workers + Vite. `.claude/settings.json` exists, so Claude Code.
>
> Here's what I'd configure for worktree auto-init:
> - **Share (symlink)**: `node_modules`, `apps/*/node_modules`, `packages/*/node_modules`
> - **Copy**: `apps/api/.dev.vars` (saw `.dev.vars.example`)
> - **Hook**: `.claude/settings.json` add `SessionStart` calling `bash $(...)/scripts/setup-worktree.sh`
> - **Manual entry point**: `bash scripts/setup-worktree.sh` always works
>
> A few I need to confirm:
> 1. **`.wrangler/state`** (Cloudflare local D1/R2 state): share across worktrees? Share = all worktrees see same local DB; isolated = each its own. **Depends on whether you'll run `dev` in multiple worktrees concurrently.**
> 2. Besides Claude Code, do you / your team also use Codex / Cursor / Gemini CLI? Want hooks for those too?
> 3. Didn't see custom reference-repo / build-output sharing needs — confirm none?
>
> Look right?

### Step 3: Tighten with 1-2 follow-ups based on the answer

After the user answers, only ask the necessary follow-ups based on what they said. Common follow-ups:

- User says "yes, I run multiple worktrees concurrently" → "For stateful services (`pgdata`, SQLite WAL), do you want concurrent isolation (Copy) or sharing (Share)? Default recommendation is Copy to prevent corruption."
- User says they also use Codex/Cursor/Gemini → "I'm not familiar with X's hook mechanism — could you point me at the docs / how do you expect it to auto-run? Worst case I can hook in via git's `post-checkout`."
- User mentions a custom resource → "Share or Copy? Is it written to often?"

**Don't open another round of questions** — decide what you can decide.

### Step 4: Generate + verify

1. Copy [`setup-worktree.sh`](setup-worktree.sh) template into `<repo>/scripts/`
2. Fill in the "resource declarations" block at the bottom per the agreed plan (leave the helper functions block as-is)
3. Merge the matching hook config (from [`hook-config.json`](hook-config.json)) into `.claude/settings.json` (or whatever the tool's config location is; multiple tools = multiple hooks)
4. **Run twice to verify idempotency**: first run links, second run skips everything
5. In a freshly-created worktree, actually run `dev` / `test` end-to-end
6. Report back: what was installed, what files changed, how to invoke manually

**When updating an existing script**: use `Edit` to diff-edit the resource declarations block. **Don't touch the helper functions** unless they're genuinely outdated.

## Three-tier strategy (the agent's classification framework)

| Tier | Examples | Why | How |
|---|---|---|---|
| **Share** (symlink) | `node_modules`, package-manager caches, stateful DB shared across worktrees | saves disk + install time; multiple worktrees see same data | `ln -s $MAIN/<path> $WORKTREE/<path>` |
| **Copy** | secrets / env files, signing keys, stateful files used concurrently | each worktree may diverge; mustn't break if main is deleted; mustn't get torn under concurrent writes | `cp -R` once (re-run skips) |
| **Generate** | dev port, `COMPOSE_PROJECT_NAME`, local socket | must differ per-worktree | `hash(branch) % range` for ports; `clean_branch_name` for container names |

**Stateful data**: in single-writer concurrent mode, must be Copy (Postgres, SQLite WAL are single-writer); for sequential use, can be Share. **This must be in Step 2's "needs confirmation" list — don't decide it for the user.**

## Agent tool trigger reference

| Agent tool | Trigger mechanism |
|---|---|
| Claude Code | `SessionStart` hook (most portable) / `WorktreeCreate` hook (only fires for `claude --worktree`, strict stdout contract: print only path, progress to `/dev/tty`) |
| Codex | **No equivalent hook mechanism** currently — manual script + `post-checkout` git hook |
| Cursor | Same as above |
| Gemini CLI | **Not sure — ask the user for docs** |
| Aider / others | **Not sure — ask the user for docs** |
| Multi-tool / no agent tool | Universal fallback: `post-checkout` git hook + manual `bash scripts/setup-worktree.sh` |

**Key principles**:
- For tools you don't know, **don't make up hook configs**. Ask the user.
- **Always preserve the manual entry point** `bash scripts/setup-worktree.sh`. Any hook breaking or tool-switching shouldn't leave you stuck.
- Multi-tool? **Hook them all to the same script** — the script itself is idempotent.

## Quick reference: common resources → default tier

| Resource | Default tier | Note |
|---|---|---|
| Root `node_modules/` | Share | npm workspaces hoist target |
| `apps/*/node_modules/`, `packages/*/node_modules/` | Share — **don't skip** | bundlers walk only one parent up from workspace; subpath exports like `zod/v3` only exist in the workspace's local install |
| `.venv/`, `venv/` | Share (semi-readonly) | Python virtualenv shebangs are absolute-path-baked; same machine OK |
| Build cache (`.next/`, `target/`, `dist/`) | Skip or Share | usually rebuilds fast enough |
| `.env*`, `.dev.vars` | Copy | secrets can't be shared |
| `*.wrangler/state`, `pgdata/`, `redis-data/` | **Depends on concurrency — list as needs-confirmation** | share/copy depends on concurrent use |
| Dev port | Generate | hash branch |
| `COMPOSE_PROJECT_NAME` | Generate | clean branch name |
| Custom (reference-repo symlinks, build artifacts, etc.) | **Find during audit; if unsure list as needs-confirmation in Step 2** | |

## Common mistakes (self-check while writing the script)

- **Linking only root `node_modules`, missing workspaces**: symptom `Could not read from file: .../zod/v4`. Loop both `apps/*` and `packages/*`.
- **`git worktree add` polluting stdout** (under `WorktreeCreate` hook): redirect with `>/dev/null 2>&1`, send progress to `/dev/tty`.
- **Symlinking single-writer stateful directories**: concurrent `dev` corrupts. Step 2 must list as needs-confirmation.
- **Not idempotent**: re-runs must skip everything. Template's `link_resource` handles this.
- **Dead symlinks**: check `[ -e "$target" ]` before linking.
- **Hardcoding the main repo path**: derive with `git rev-parse --git-common-dir`.
- **Symlinking `.env`**: must be Copy (symlink edits leak across worktrees).
- **Skipping audit and bombarding the user with questions**: audit first, infer what's inferrable; questions to the user are judgement calls, not facts.
- **Deciding stateful policy for the user**: Step 2 must ask.

## Implementation resources

- Script template: [`setup-worktree.sh`](setup-worktree.sh)
- Hook config candidates: [`hook-config.json`](hook-config.json)
- Per-stack snippets: [`recipes.md`](recipes.md)

## Verification checklist (run after generate / update)

- [ ] Script runs on fresh `git worktree add` and exits 0
- [ ] Re-run = no-op (all "skip — already linked")
- [ ] `npm run dev` (or stack equivalent) actually starts, no "module not found"
- [ ] Tests / typecheck pass in the new worktree
- [ ] Removing main-repo's optional resource → script logs "skip" not error
- [ ] Under `WorktreeCreate`: stdout contains only the worktree path
- [ ] **Manual entry point** (`bash scripts/setup-worktree.sh`) also runs
- [ ] Confirmed resource list matches what got generated
