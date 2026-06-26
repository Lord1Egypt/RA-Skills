---
name: molt-backup
description: Snapshot and back up OpenClaw brain files (AGENTS.md, SOUL.md, MEMORY.md, memory/, etc.) to an offsite git repository — like a lobster shedding its shell, leaving behind a perfect copy before growing. Use when asked to back up the brain, run a molt, snapshot memory offsite, or schedule/manage brain backups. Also use when setting up or configuring the molt cron job.
---

# molt

Snapshots OpenClaw brain files to a remote git repo — a perfect copy of who you were before you grow. Idempotent — only commits when something changed.

## Security Model

molt sends files **only to a git repository you control** — no third-party servers, no telemetry, no hidden destinations. The target repo is set explicitly by you via `MOLT_REPO_URL` or `--repo-url`.

Sensitive fields are redacted before backup using `openclaw config get`, which is the authoritative redaction source built into OpenClaw itself. The redacted config is the only file containing config data — raw `openclaw.json` is never copied.

This is an intentional, user-initiated backup tool. You own the destination.

## Requirements

- **`git`** — must be installed and on `$PATH`
- **Git authentication** — the script uses `git clone` / `git push` over HTTPS or SSH. You need credentials configured for the remote:
  - **SSH** (recommended): add your SSH key to GitHub/GitLab; use a `git@github.com:...` repo URL
  - **HTTPS with token**: configure a credential helper or use a token in the URL (`https://<token>@github.com/...`)
  - `gh` CLI is **not required** — molt uses plain git only
- **`rsync`** — used for `memory/` sync; standard on macOS and most Linux distros
- **Write access to the remote repo** — the pushing account needs push rights; a dedicated private repo is recommended

No other dependencies. No OpenClaw-specific CLI tools needed at runtime.

## Zero-to-Working Setup

1. **Create a private remote repo** (GitHub, GitLab, etc.) — e.g. `your-org/your-brain`
2. **Ensure git auth works** for that repo from the machine running OpenClaw:
   ```bash
   ssh -T git@github.com   # for SSH — should greet you by name
   ```
3. **Run molt once** with the repo URL:
   ```bash
   MOLT_REPO_URL=git@github.com:your-org/your-brain.git \
     ~/.openclaw/workspace/marv-skills/molt/scripts/molt.sh
   ```
   This clones the repo to `~/.openclaw/molt`, copies brain files, commits, and pushes.
4. **Schedule it** — add a cron job or ask your assistant to set one up via `openclaw cron`.

After the first run, the `MOLT_REPO_URL` env var is no longer needed (the local clone already knows its remote).

## What Gets Backed Up

- `AGENTS.md`, `SOUL.md`, `TOOLS.md`, `IDENTITY.md`, `USER.md`, `HEARTBEAT.md`, `MEMORY.md`
- `memory/` directory (daily notes)
- `cron-jobs/` — exported live from `openclaw cron list` at backup time (JSON + Markdown summary)
- `config-redacted.json` — OpenClaw config with all secrets/tokens replaced by `[REDACTED]`

## Config

Set via environment variables or pass as flags:

| Env var | Flag | Default | Description |
|---|---|---|---|
| `MOLT_WORKSPACE` | `--workspace` | `~/.openclaw/workspace` | Source workspace |
| `MOLT_DIR` | `--backup-dir` | `~/.openclaw/molt` | Local backup repo clone |
| `MOLT_REPO_URL` | `--repo-url` | _(required on first run)_ | Remote git repo URL |
| `MOLT_EXTRA_DIRS` | `--extra-dirs` | _(none)_ | Comma-separated workspace subdirs to include (e.g. `scripts,notes`) |

## Running

```bash
# First run (clones the repo):
MOLT_REPO_URL=https://github.com/your-org/your-brain-repo.git \
  scripts/molt.sh

# Subsequent runs (repo already cloned):
scripts/molt.sh

# Dry run (see what would change without pushing):
scripts/molt.sh --dry-run
```

## Scheduling

To schedule automatic backups, create a cron job pointing at this script. Example for every 6 hours:

```
0 */6 * * * MOLT_DIR=~/.openclaw/molt ~/.openclaw/workspace/marv-skills/molt/scripts/molt.sh >> /tmp/molt.log 2>&1
```

Or use `openclaw cron` to schedule via the assistant.

## First-Time Setup

1. Create the remote repo (GitHub, GitLab, etc.)
2. Set `MOLT_REPO_URL` to the repo URL
3. Run the script once — it will clone and push
4. On subsequent runs, only env var `MOLT_DIR` is needed (defaults to `~/.openclaw/molt`)

