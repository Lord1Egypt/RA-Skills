# OpenClaw Claude Delegate

Give Claude back to OpenClaw.

A reusable OpenClaw skill for running Claude Code as a **local delegated worker** with:

- dispatch, poll, result, and resume
- profile-based workdir scoping
- optional non-root runner execution
- self-heal hooks for Claude binary, auth sync, and runner-local acpx install

This is the boring, reliable local wrapper lane, not the ACP chat-harness lane.

**Real advantage:** it gives any OpenClaw agent a locally authenticated Claude Code subscription lane, including a non-root `bypassPermissions` worker path, without pretending ACP or third-party harnesses can use Claude subscription access the same way.

## Why people will star it

- It restores Claude inside OpenClaw instead of forcing people to choose one or the other.
- It gives you a real local worker lane, not a fake integration.
- It installs in one command.
- It creates a usable `claude-delegate` CLI, so the workflow is easy to remember.
- It keeps the no-permissions worker path separate from ACP, where it belongs.

## Why this exists

Claude Code subscription access is valuable, but third-party harnesses cannot reliably use that subscription path directly. This wrapper gives any OpenClaw agent a clean delegation lane into local Claude Code without turning the whole runtime into a Claude-specific harness.

Use it when you want:
- a local Claude worker with monitoring and resume
- a bounded workdir instead of full-session sprawl
- a non-root runner model that survives OpenClaw updates better
- a way for other agents to delegate premium Claude work intentionally
- a reliable `bypassPermissions` lane that is separate from the main OpenClaw runtime

## How it works

`claude-delegate` is a thin entrypoint over four layers:

1. `scripts/claude-delegate.sh` — command entrypoint and defaults
2. `scripts/cc-profile.sh` — resolves the chosen profile into a workdir and extra dirs
3. `scripts/cc-orchestrator.sh` — tracks tasks, logs, poll, result, and resume
4. `scripts/run-task.sh` — actually runs Claude, optionally through a non-root runner

If you enable the non-root path, `scripts/ensure-nonroot-delegation.sh` also syncs:
- Claude binary into the runner home
- Claude auth into the runner home
- acpx config into the runner home
- runner-local acpx install under `~/.local/share/clawd/vendor/acpx/`

The wrapper also bootstraps Claude with local coordination context by telling it to discover/read nearby `CLAUDE.delegate.md`, `AGENTS.md`, `TOOLS.md`, and `README.md` files before substantive work.

## What is in this repo

- `SKILL.md` — the skill entrypoint
- `CLAUDE.delegate.md` — repo-level delegate bootstrap guidance
- `scripts/claude-delegate.sh` — stable wrapper command
- `scripts/cc-profile.sh` — profile-aware wrapper
- `scripts/cc-orchestrator.sh` — task registry, dispatch, poll, result, resume
- `scripts/run-task.sh` — low-level Claude runner
- `scripts/delegate-bootstrap.sh` — builds the default delegate bootstrap prompt from nearby doc files
- `scripts/ensure-nonroot-delegation.sh` — non-root runner bootstrap/sync
- `references/setup.md` — setup and portability notes
- `profiles.json` — generic starter profiles

## When to use it

Use this when you want Claude Code to run as a local worker with explicit monitoring and resume support.

Do **not** use this when the user explicitly wants an ACP thread or chat harness. That is a different lane.

## Install

### OpenClaw native install from ClawHub

```bash
openclaw skills install openclaw-claude-delegate
```

That is the easiest path if you are already inside OpenClaw.

### One-line installer

```bash
curl -fsSL https://raw.githubusercontent.com/StoicEnso/openclaw-claude-delegate/v0.2.6/install.sh | bash -s -- --version v0.2.6
```

That will:
- install the skill into `~/.agents/skills/claude-delegate` by default
- create `~/.local/bin/claude-delegate`
- run a setup check against the same runner/OAuth environment the wrapper uses
- include the repo's default `CLAUDE.delegate.md` guidance in the installed package

For a live end-to-end install test, add `--smoke` to dispatch a tiny scratch task after installation.

After install:

```bash
claude-delegate doctor
claude-delegate dispatch scratch 0.10 sonnet smoke "Reply with exactly CLAUDE-DELEGATE-SMOKE-OK"
```

If you prefer a local clone:

### Clone then install

```bash
git clone https://github.com/StoicEnso/openclaw-claude-delegate.git
cd openclaw-claude-delegate
bash install.sh
```

### npm/npx installer (package is publish-ready)

```bash
npx openclaw-claude-delegate
```

This will work once the npm package is published.

## Post-install sanity check

Run:

```bash
claude-delegate doctor
```

That shows:
- runner user
- runner home
- Claude binary path
- selected backend
- profile file in use
- root and runner Claude auth status
- a live Claude probe

## Quick start

If you used the installer and accepted the CLI link:

```bash
claude-delegate doctor
claude-delegate dispatch scratch 0.10 sonnet smoke "Reply with exactly CLAUDE-DELEGATE-SMOKE-OK"
claude-delegate list --all
claude-delegate result <task-id>
```

Repo-local form still works too:

```bash
bash scripts/claude-delegate.sh dispatch scratch 0.10 sonnet smoke "Reply with exactly CLAUDE-DELEGATE-SMOKE-OK"
bash scripts/claude-delegate.sh list --all
bash scripts/claude-delegate.sh result <task-id>
```

## Profiles

`profiles.json` is intentionally generic. For real deployments, either edit it or point to a host-local file:

```bash
export CLAUDE_DELEGATE_PROFILES=/abs/path/to/profiles.json
```

Profile paths support `~` and environment variable expansion like `${HOME}`.

## Delegate instruction files

By default, Claude Delegate appends bootstrap guidance that tells Claude to:
- discover and read the nearest `CLAUDE.delegate.md` files from the workdir, its ancestors, and any `add_dirs`
- inspect nearby `AGENTS.md`, `TOOLS.md`, and `README.md` files before substantive work

Recommended layering:
- workspace-level `CLAUDE.delegate.md`
- shared folder-level `CLAUDE.delegate.md`
- repo or skill-level `CLAUDE.delegate.md`

Knobs:

```bash
export CLAUDE_DELEGATE_BOOTSTRAP=0
export CLAUDE_DELEGATE_DOC_BASENAME=CLAUDE.delegate.md
```

## ACP vs local delegate lane

This part matters.

**No**, the fully delegated no-permissions lane is **not automatically the ACP lane**.

- **ACP lane** = chat/thread harness behavior inside OpenClaw ACP
- **Claude Delegate lane** = local Claude CLI worker launched through this wrapper

The `bypassPermissions` non-root runner path lives in the **local delegate lane**.
That is the real value here.

So if you want:
- Claude subscription access
- local CLI execution
- optional non-root `bypassPermissions`
- resume/poll/result tracking

use **Claude Delegate**, not ACP.

## Non-root runner defaults

The wrapper is adaptive:

- if run as root and `/home/ccbot` exists, it defaults to a `ccbot` runner;
- otherwise it runs as the current user with the current `claude` binary;
- if `CLAUDE_OAUTH_ENV_FILE` exists, it is sourced and `CLAUDE_CODE_OAUTH_TOKEN` is forwarded into the runner environment.

For a `ccbot` runner account the effective defaults are:

- `CLAUDE_RUNNER_USER=ccbot`
- `CLAUDE_RUNNER_HOME=/home/ccbot`
- `CLAUDE_BIN=/home/ccbot/.local/bin/claude`
- `CLAUDE_PERMISSION_MODE=bypassPermissions`
- `CLAUDE_BACKEND=cli`
- `CLAUDE_OAUTH_ENV_FILE=~/.claude/.oauth-token.env` or `/root/.claude/.oauth-token.env` when running as root

Override those if your host layout differs.

## Prerequisites

Minimum:
- OpenClaw installed
- Claude Code installed and authenticated
- bash
- python3

For the full non-root self-heal path, you also want:
- npm
- sudo and permission to switch to the runner user
- a runner user such as `ccbot`

## Important reality checks

- `claude auth status` is **not** enough, use a real prompt probe.
- A plain completion test is **not** proof of tool-call compatibility.
- ACP and local CLI delegation are different products. Pick intentionally.

## License

MIT
