---
name: git-sync-daemon
description: >
  Manage multiple git repositories with a daemon model (periodic add/commit/pull/push).
  Use this skill when you need to set up, run, or troubleshoot automated git sync on
  macOS (launchd) or Linux (systemd), including repo registration and service lifecycle.
---

# Git Sync Daemon

## Purpose

Provide a reusable, daemon-based git auto-sync workflow:
- one repo list file
- one daemon process
- per-repo lock and independent failure isolation
- service management on macOS and Linux

## Files

- Engine: `scripts/git_sync_daemon.sh`
- Control CLI: `scripts/git_sync_ctl.sh`

## Default Runtime Paths

- State dir: `~/.config/git-sync-daemon`
- Repo list: `~/.config/git-sync-daemon/repos.conf`
- Log file: `~/.config/git-sync-daemon/git-sync-daemon.log`

## Repo Entry Format

One line per repo:

```text
/absolute/path/to/repo|remote=origin|branch=main|enabled=1
```

Supported keys:
- `remote` (default `origin`)
- `branch` (default current branch)
- `enabled` (`1/0`, `true/false`, default enabled)

## Quick Start (macOS)

```bash
bash scripts/git_sync_ctl.sh init
bash scripts/git_sync_ctl.sh add-repo /Users/samwei12/Develop/config
bash scripts/git_sync_ctl.sh run-once
bash scripts/git_sync_ctl.sh install-launchd
bash scripts/git_sync_ctl.sh status
```

## Quick Start (Linux)

```bash
bash scripts/git_sync_ctl.sh init
bash scripts/git_sync_ctl.sh add-repo /path/to/repo
bash scripts/git_sync_ctl.sh run-once
sudo bash scripts/git_sync_ctl.sh install-systemd
bash scripts/git_sync_ctl.sh status
```

## Operations

- Add repo: `bash scripts/git_sync_ctl.sh add-repo <path> [branch] [remote]`
- Remove repo: `bash scripts/git_sync_ctl.sh remove-repo <path>`
- List repos: `bash scripts/git_sync_ctl.sh list-repos`
- One cycle now: `bash scripts/git_sync_ctl.sh run-once`
- Status/log tail: `bash scripts/git_sync_ctl.sh status`

Service lifecycle:
- macOS install: `bash scripts/git_sync_ctl.sh install-launchd`
- macOS uninstall: `bash scripts/git_sync_ctl.sh uninstall-launchd`
- Linux install: `sudo bash scripts/git_sync_ctl.sh install-systemd`
- Linux uninstall: `sudo bash scripts/git_sync_ctl.sh uninstall-systemd`

## Production hardening checklist

Before enabling daemon mode in production:

1. SSH/auth baseline
- Ensure service user can run non-interactive git over SSH to each remote.
- Preload host keys (`ssh-keyscan` / `StrictHostKeyChecking=accept-new`) to avoid first-run failures.
- Prefer explicit key routing in `~/.ssh/config` (host/user/port/IdentityFile/IdentitiesOnly).

2. Service identity consistency
- Install service with the same user that owns repo credentials and git config.
- Verify `git config --global user.name/user.email` for that service user.

3. Repo registration policy
- Register only clean, intended repos.
- Keep one canonical branch per repo entry; avoid detached HEAD targets.
- Use `enabled=0` for temporary pauses instead of deleting lines.

4. Observability
- Keep logs in dedicated file and rotate externally if needed.
- Validate `run-once` before enabling persistent service.

## Safety Notes

- The daemon does not force-push.
- Rebase conflicts are logged and isolated to the affected repo.
- If `git-lfs` is required by hooks but missing, that repo is skipped with explicit error log.
- On macOS launchd, PATH is expanded in both service env and daemon script to include Homebrew binaries.
- Recommended migration practice: first successful run should use baseline repos only; then gradually add more repos.
