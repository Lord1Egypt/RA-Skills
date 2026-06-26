# Claude Delegate setup

## What this package gives you

A local Claude Code delegation lane with:
- dispatch, poll, result, resume
- optional non-root runner execution
- profile-based workdir scoping
- runner self-heal for Claude binary, auth file, and acpx install when you use the provided ensure script
- a practical way for any OpenClaw agent to reach a locally authenticated Claude subscription worker
- default bootstrap guidance that tells Claude to discover/read nearby `CLAUDE.delegate.md`, `AGENTS.md`, `TOOLS.md`, and `README.md` files before substantive work

The real advantage is the **local delegated non-root `bypassPermissions` lane**. That is separate from ACP and exists because third-party harnesses do not reliably get Claude subscription access.

## Quick install

### Recommended bootstrap

```bash
curl -fsSL https://raw.githubusercontent.com/StoicEnso/openclaw-claude-delegate/v0.2.6/install.sh | bash -s -- --version v0.2.6
```

That installs the skill into `~/.agents/skills/claude-delegate` by default, creates `~/.local/bin/claude-delegate`, and runs a setup check using the same runner/OAuth environment as the wrapper.

To force an end-to-end live test during install:

```bash
curl -fsSL https://raw.githubusercontent.com/StoicEnso/openclaw-claude-delegate/v0.2.6/install.sh | bash -s -- --version v0.2.6 --smoke
```

The smoke test dispatches the `scratch` profile and should return `CLAUDE-DELEGATE-SMOKE-OK`.

### Clone/install flow

1. Install Claude Code and log in once.
2. Clone this repo.
3. Run `bash install.sh`.
4. Edit `profiles.json` for your project roots, or keep a host-local profiles file and export `CLAUDE_DELEGATE_PROFILES=/abs/path/to/profiles.json`.
5. If you want a non-root runner, set these as needed:
   - `CLAUDE_RUNNER_USER`
   - `CLAUDE_RUNNER_HOME`
   - `CLAUDE_BIN`
   - `CLAUDE_PERMISSION_MODE`
   - `CLAUDE_BACKEND`
   - `CLAUDE_OAUTH_ENV_FILE`
6. Run `claude-delegate doctor` or `bash scripts/claude-delegate.sh doctor`.

## Install result

After a normal install you should have:
- skill folder: `~/.agents/skills/claude-delegate`
- CLI path: `~/.local/bin/claude-delegate`
- repo-level delegate guidance file: `CLAUDE.delegate.md`

If `~/.local/bin` is not on your `PATH`, add it in your shell profile.

## Delegate instruction files

By default, Claude Delegate appends bootstrap guidance that tells Claude to:
- discover and read the nearest `CLAUDE.delegate.md` files from the workdir, its ancestors, and any `add_dirs`
- inspect nearby `AGENTS.md`, `TOOLS.md`, and `README.md` files before substantive work

Recommended layering:
- workspace-level `CLAUDE.delegate.md`
- shared folder-level `CLAUDE.delegate.md`
- repo or skill-level `CLAUDE.delegate.md`

Knobs:
- `CLAUDE_DELEGATE_BOOTSTRAP=0` disables the default bootstrap prompt
- `CLAUDE_DELEGATE_DOC_BASENAME=SomethingElse.md` changes the filename Claude looks for

## Stable commands

```bash
claude-delegate dispatch <profile> <budget> <model> <label> "<task>"
claude-delegate poll <task-id>
claude-delegate result <task-id>
claude-delegate resume <task-id> <budget> "<follow-up>"
claude-delegate list --all
claude-delegate doctor
```

Repo-local form:

```bash
bash scripts/claude-delegate.sh dispatch <profile> <budget> <model> <label> "<task>"
```

## Profiles

`cc-profile.sh` reads `profiles.json` next to the skill by default.

Override it per host:

```bash
export CLAUDE_DELEGATE_PROFILES=/abs/path/to/profiles.json
```

Path values inside profiles support:
- `~`
- `${HOME}` and other environment variables

## Non-root runner notes

`ensure-nonroot-delegation.sh` is the boring path when you want root-owned OpenClaw to launch Claude as another user.

It can sync these from a source install into the runner account:
- Claude binary
- Claude auth file
- acpx config
- runner-local acpx install

If your host uses different source paths, override them before calling the wrapper:
- `OPENCLAW_ACPX_PACKAGE`
- `ROOT_CLAUDE_LINK`
- `ROOT_CLAUDE_CREDS`
- `ROOT_ACPX_CONFIG`
- `DEFAULT_ACPX_SPEC`

The wrapper is adaptive:
- if run as root and `/home/ccbot` exists, it defaults to `CLAUDE_RUNNER_USER=ccbot`;
- otherwise it runs as the current user with the current `claude` binary;
- if `CLAUDE_OAUTH_ENV_FILE` exists, it is sourced and `CLAUDE_CODE_OAUTH_TOKEN` is forwarded into the runner environment.

## ACP vs delegate lane

Do not blur these together:

- **ACP** is the OpenClaw chat/thread harness lane
- **Claude Delegate** is the local Claude CLI wrapper lane

If you want the non-root `bypassPermissions` worker path, use **Claude Delegate**.
Do not assume ACP automatically inherits that execution model.

## What not to assume

- A healthy `claude auth status` is not enough. Run a real prompt probe.
- A plain text completion test does not prove tool-call compatibility.
- ACP and local CLI delegation are different lanes. Pick one on purpose.

## Recommended sanity checks

1. `bash scripts/setup.sh --check-only`
2. `bash scripts/claude-delegate.sh doctor`
3. `bash scripts/claude-delegate.sh dispatch scratch 0.10 sonnet smoke "Reply with exactly CLAUDE-DELEGATE-SMOKE-OK"`
4. `bash scripts/claude-delegate.sh result <task-id>`

## npm / npx note

This repo now includes `package.json` and a small installer bin so it is npm-publish ready. The intended command is:

```bash
npx openclaw-claude-delegate
```

That package still needs to be published to npm before this command works for the public.

## Packaging note

This skill intentionally keeps host-specific profiles outside the core workflow. For open-source sharing, keep the skill generic and put personal repo paths in your local `CLAUDE_DELEGATE_PROFILES` file.
