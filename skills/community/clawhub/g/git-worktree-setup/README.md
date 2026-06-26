# git-worktree-setup

[![skills.sh](https://skills.sh/b/imsai-sh/git-worktree-setup)](https://skills.sh/imsai-sh/git-worktree-setup)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An [Agent Skill](https://agentskills.io/specification) that teaches an AI coding agent (Claude Code, Codex, Cursor, Gemini CLI, etc.) how to **bootstrap a fresh `git worktree`** so it's actually runnable — `node_modules` linked, `.env` copied, dev port reserved, local DB state shared or isolated as appropriate — with a single per-repo script and a matching tool-specific hook.

## The problem

`git worktree add` checks out source files but **nothing else**. No `.env`. No `node_modules`. No virtualenv. No port reservation. Every fresh worktree forces you (or your agent) to re-do the same setup, debugging missing modules along the way.

Existing solutions tend to be one-off shell scripts wired up by hand per project, with a lot of stack-specific gotchas (e.g. `apps/*/node_modules` aren't covered by hoisted root `node_modules` when bundlers resolve from inside a workspace; symlinking `pgdata` corrupts under concurrent writes; secrets shouldn't be symlinked at all).

## What this skill does

The skill itself is **not** a hook — it doesn't fire on every worktree. It's a **generator** an agent runs **once** when you ask:

> "Set me up worktree auto-bootstrap for this repo."

The agent then:

1. **Audits the repo itself** — reads `package.json`, `.gitignore`, `docker-compose.yml`, agent-tool config dirs, custom Makefile / setup scripts, and anything else relevant. Doesn't bother you with questions about facts it can derive.
2. **Walks in with a concrete draft plan** — three-tier resource classification (Share / Copy / Generate), proposed hook wiring, manual entry point. Marks the open questions it genuinely can't decide (concurrency model, custom resources, multi-tool setups).
3. **Asks 1-3 sharp questions**, not 7.
4. **Generates a tailored `scripts/setup-worktree.sh`** + the matching hook config, then verifies idempotency and end-to-end `dev` startup.

Re-run later when the project structure changes; it diff-edits the existing script.

## Installation

**Recommended** — use the [`skills` CLI](https://github.com/vercel-labs/skills). One command, works with Claude Code, Codex, Cursor, OpenCode, and [50+ other agents](https://skills.sh):

```bash
npx skills add imsai-sh/git-worktree-setup
```

The CLI auto-detects which agent(s) you have installed and drops the skill into the right directory (`.claude/skills/`, `.codex/skills/`, etc.). Pass `-a <agent>` to target a specific agent, `-g` for global install, or `-y` to skip prompts.

Then in any conversation, say something like *"set up worktree auto-bootstrap for this repo"* — your agent will discover and invoke the skill.

### Manual install (fallback)

If you'd rather not run a CLI, clone this repo into your agent's skills directory directly:

```bash
# Claude Code, user-level
git clone https://github.com/imsai-sh/git-worktree-setup.git ~/.claude/skills/git-worktree-setup

# Or project-level (committed into the repo)
git submodule add https://github.com/imsai-sh/git-worktree-setup.git .claude/skills/git-worktree-setup
```

For agents without a standard skills loader, just point yours at this repo: *"read SKILL.md from `<path>` and follow its workflow."* The skill is plain markdown + a few support files — nothing here is Claude Code-specific.

## Repository layout

| File | What it is |
|---|---|
| [`SKILL.md`](SKILL.md) | The skill spec the agent loads. **English, the published version.** |
| [`SKILL.zh.md`](SKILL.zh.md) | 中文版（与英文版内容等价，便于中文开发者审阅 / 参与维护）。 |
| [`setup-worktree.sh`](setup-worktree.sh) | The reusable script template. Drop into `<repo>/scripts/`, edit the resource-declarations block at the bottom. Includes 6 idempotent helpers: `link_resource`, `copy_resource`, `link_glob`, `hash_port`, `clean_branch_name`, `upsert_env`. |
| [`recipes.md`](recipes.md) | Per-stack copy-paste blocks: npm workspaces / pnpm / Yarn Berry / Poetry / uv / Cargo / Go / Wrangler / Docker Compose / Postgres / WorktreeCreate-hook strict-stdout variant + a `worktree-remove.sh` cleanup template. |
| [`hook-config.json`](hook-config.json) | Three candidate Claude Code hook wirings: `SessionStart` (most portable), `WorktreeCreate` (cleanest but Claude-Code-only), and a belt-and-suspenders combo. |

## Design principles

- **Audit first, then ask** — agents shouldn't open with question lists. Investigate the repo, propose a concrete plan, ask only the judgment calls.
- **Three-tier classification, no fourth** — every missing resource is Share, Copy, or Generate. Forces a choice.
- **Idempotency is non-negotiable** — the script must be safe to re-run. Helpers handle this; verification checklist enforces it.
- **Manual entry point always preserved** — even with hooks, `bash scripts/setup-worktree.sh` must work standalone. Hooks fail; tools change; the script is the source of truth.
- **Honest about unknowns** — for agent tools the skill author hasn't characterized (Gemini CLI, Aider), the skill explicitly tells the agent to ask the user for docs rather than fabricate hook configs.
- **Keep the published spec terse** — most prose lives in `recipes.md` and the script comments, not in `SKILL.md`.

## Acknowledgments

Distilled from production experience on a multi-worktree monorepo, plus close reading of two prior art repos:

- [`tfriedel/claude-worktree-hooks`](https://github.com/tfriedel/claude-worktree-hooks) — the canonical reference for Claude Code's `WorktreeCreate` hook contract (stdout = path only, progress to `/dev/tty`, `git worktree add` output suppression). The deterministic-port-by-branch-hash idea is also from there.
- [`mittalyashu/git-worktree`](https://github.com/mittalyashu/git-worktree) — a manual-script approach with `pnpm install` + `docker-compose up` per worktree. Useful baseline for the "no agent hook, just scripts" case.

This skill generalizes both into a tool-agnostic, structure-agnostic generator.

## License

MIT — see [LICENSE](LICENSE).

## Contributing

Issues and PRs welcome. Particularly useful contributions:

- New stack recipes in `recipes.md` (Elixir/Phoenix, Java/Gradle, .NET, etc.)
- Verified hook mechanisms for non-Claude-Code agent tools (Codex, Cursor, Gemini CLI, Aider) — replace the current "ask the user" placeholder with concrete configs
- Additional `setup-worktree.sh` helpers for common patterns
- Real-world failure modes worth adding to the "Common mistakes" section
