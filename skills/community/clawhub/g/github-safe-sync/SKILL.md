---
name: github-safe-sync
description: "Inspect, trigger, and clean up GitHub mirror repositories that use a safe-sync GitHub Actions workflow. Use when Codex needs to work on repository mirroring or sync automation tasks such as: (1) checking whether a mirror repo is up to date with its upstream, (2) triggering `safe-sync.yml` manually, (3) auditing recent workflow runs, backup branches, or force-push alert issues, (4) closing false-positive sync issues, or (5) deleting stale `backup/` branches after a sync fix."
---

# GitHub Safe Sync

Use this skill for repositories that mirror an upstream GitHub repo and preserve local `.github` workflow files with a `safe-sync.yml` workflow.

## Requirements

- Set `GITHUB_TOKEN` before running the script.
- Pass repositories as `owner/repo`.
- Treat tokens as secrets. Do not write them into the skill or commit them into repo files.

## Quick Start

Inspect a mirror repo:

```bash
export GITHUB_TOKEN=...
./scripts/github_safe_sync.py status \
  --owner grey00758 \
  --repo ai-code-board \
  --upstream grey0758/ai-code-board
```

Trigger a manual sync:

```bash
export GITHUB_TOKEN=...
./scripts/github_safe_sync.py dispatch \
  --owner grey00758 \
  --repo ai-code-board
```

Clean false-positive artifacts after a workflow fix:

```bash
export GITHUB_TOKEN=...
./scripts/github_safe_sync.py close-force-push-issues \
  --owner grey00758 \
  --repo ai-code-board

./scripts/github_safe_sync.py delete-backups \
  --owner grey00758 \
  --repo ai-code-board
```

## Workflow

1. Inspect the mirror repository with `status`.
2. If the workflow is inactive or the latest run failed, review the repo before dispatching anything.
3. If the mirror should sync now, run `dispatch`.
4. If a workflow fix stopped false-positive force-push alerts, run `close-force-push-issues` and `delete-backups`.
5. Re-run `status` to verify the repo is clean.

## Interpreting `status`

- `effective_state=exact`: Mirror and upstream branch heads are identical.
- `effective_state=metadata-ahead`: Mirror is only ahead by local `.github`-only commits. This is normally healthy for safe-sync mirrors.
- `effective_state=behind`: Upstream has newer commits and the mirror has not caught up yet.
- `effective_state=local-ahead`: Mirror has non-metadata commits that do not exist upstream. Inspect before forcing anything.
- `effective_state=metadata-diverged`: Histories differ, but the mirror-only side is metadata-only. This often means the sync workflow logic still needs review.
- `effective_state=diverged`: Mirror and upstream both changed in incompatible ways. Treat this as a real sync problem until proven otherwise.

## Commands

### `status`

Use `status` first. It returns JSON with:

- workflow metadata
- latest workflow runs
- count of open force-push alert issues
- count of `backup/` branches
- optional upstream branch comparison

If the requested upstream branch does not exist, the script falls back to the upstream repo default branch.

### `dispatch`

Use `dispatch` to trigger `workflow_dispatch` on the sync workflow. Add `--force-sync` only when you intentionally want the workflow to ignore the normal no-op path.

### `close-force-push-issues`

Use this only after you have confirmed the force-push alerts were false positives. It closes open issues whose title contains `检测到上游强制推送`.

### `delete-backups`

Use this only after you have confirmed the backup branches are noise. Start with `--dry-run` if you want to preview what would be removed.

## Safety Rules

- Do not close force-push alert issues until you have verified the alert was false.
- Do not delete `backup/` branches until the mirror workflow is healthy and the backups are no longer needed.
- Do not assume `main`; pass `--branch` or `--upstream` explicitly when the repo uses a different upstream default branch.
- Re-run `status` after every write operation.
