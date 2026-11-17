---
name: last-login-janitor
description: "Use when you have developer debt - stacks of repos, venvs, node_modules, Docker images, caches, model files - and need to know what is safe to delete. Scans last-access and last-commit times, sizes every artifact, flags stale-vs-protected, and produces size-sorted deletion candidates with one-command cleanup."
version: 1.0.1
author: Denis Voronin
license: MIT
tags: [disk-cleanup, developer-tools, dev-hygiene, storage, docker, caches, repos]
---

# Last-Login Janitor

## Overview

Developer machines fill with gigabytes of things nobody has touched in a year:
38 cloned repos (7 abandoned), 22 virtualenvs (14 orphaned - their repos are
gone), node_modules directories from failed experiments, 12 versions of the
same Docker image, caches that no longer serve any project, and LLM model
files from an interest that passed.

The danger of cleanup is deleting the WRONG thing: the venv a cron job uses,
the image a stopped-but-important container references, the repo with
uncommitted work, the cache that would take 40 minutes to rebuild before
tomorrow's demo. That's why people don't clean up - and why disks hit 100%.

This skill makes cleanup **decision-safe**:

1. **FIND** every space-consuming artifact (repos, venvs, node_modules,
   Docker images/volumes, pip/npm/uv/HF caches, model weights, build dirs).
2. **DATE** it by the right signal: last *commit* for repos (not file mtime -
   git updates mtimes on checkout), last *atime* for venvs and caches,
   last *run* for Docker images, registry date for model files.
3. **PROTECT** anything with a live reason to exist: dirty worktrees,
   unpushed commits, stashes, active containers, venvs referenced by
   projects newer than themselves, caches modified this week, model files
   referenced by config.
4. **RANK** deletion candidates by size and produce a reviewable manifest +
   ready-to-run cleanup commands - nothing is deleted without your yes.

## When to Use

- "Disk is full" on a dev machine / build server / homelab SBC
- "I have 40 repos in ~/dev, which ones can I archive?"
- "What's eating my disk?" - honest size accounting per artifact type
- Periodic hygiene: quarterly dev-environment audit
- Onboarding/audit of an inherited machine ("what's actually alive here?")
- Before a big install (models, SDKs) that needs space

**Don't use for:** system-package cleanup (`apt autoremove` territory),
photo/video library organization, or deleting anything you can't rebuild or
re-clone. Always run `--dry-run` semantics: this skill reports, YOU decide.

## Artifact types & their truth signals

| Artifact | Truth signal | Protected when |
|---|---|---|
| Git repo | last commit date (`git log -1`) | dirty worktree, unpushed branches, stashes, recent commit < stale threshold |
| Python venv | last access (atime) OR mtime of newest `.py` | referenced by a sibling/parent project modified after venv creation |
| node_modules | mtime of newest file inside | sibling package.json modified recently; sibling node_modules newer than repo staleness |
| Docker image | last container run from it (events/ctimes) | ANY container (running OR stopped) uses it; < N days since pull in active project |
| Docker volume | last mount/write | attached to any container |
| pip cache | dir mtime | modified within cache-warm window (default 14d) |
| npm/pnpm cache | dir mtime | same |
| uv cache | dir mtime | same |
| HF model dir | dir mtime | modified within 30d, or referenced by active config/compose file |
| Build dirs (dist/, target/, build/, .next) | mtime | parent project active |
| IDE indexes (.idea, .vscode+bin) | mtime | project active |

## Files

| File | Purpose |
|---|---|
| `scripts/dev_janitor.py` | The scanner/classifier: finds artifacts, dates them, flags stale/protected, emits ranked report + cleanup manifest |
| `references/cleanup-playbook.md` | Safe-deletion rules per artifact type, restore-cost table, command cookbook |
| `README.md` | The problem, in dollars and gigabytes |

## Usage

```bash
# Audit a whole home dir (read-only, always)
python3 scripts/dev_janitor.py scan ~/dev ~/projects --stale-days 180

# Include Docker (requires docker group membership), exclude model dirs
python3 scripts/dev_janitor.py scan ~/ --docker --skip ~/.cache/huggingface

# Emit a ready-to-review cleanup manifest (NOT auto-executed)
python3 scripts/dev_janitor.py scan ~/dev --stale-days 365 --manifest cleanup.json
```

Output sections: SIZING (bytes per category), STALE candidates (size-sorted,
with reason + restore cost), PROTECTED (with why), then a conservative
cleanup script printed for human review.

## Workflow

1. Run the scanner on candidate roots. Start wide (`~`), narrow later.
2. Read SIZING - know what dominates before touching anything.
3. Walk STALE top-down (biggest first). For each item check the PROTECT
   reason column; the script already excluded protected items, but read
   the reason - "protected" can be overridden by human knowledge ("that
   cron job was removed last month, delete the venv").
4. Generate the manifest, review the printed commands, run them in
   batches - smallest risk first (caches), highest risk last (repos with
   unpushed work: NEVER auto-delete, push first).
5. After cleanup, rerun the scan and report bytes freed.

## Common Pitfalls

1. **mtime lies for git repos.** A `git checkout`/`pull` touches every file.
   Date repos by last COMMIT, not file mtime - the script does this.
2. **Deleting a venv a cron/systemd unit needs.** Check units before
   removing any venv older than the service (`grep -r venv /etc/systemd`).
   The script can't see systemd; you must.
3. **Stopped ≠ dead Docker containers.** A stopped container may be a
   deliberately-paused service; its image must survive. The script treats
   ANY container's image as protected.
4. **atime disabled.** Many filesystems mount with `noatime`/`relatime`;
   venv dating falls back to ctime/mtime - treat as "older than reported".
5. **The unpushed-branch trap.** A repo with zero remotes and dirty files
   contains the ONLY copy of work. Never delete; archive instead
   (`tar czf ~/archive/$(basename $r).tgz $r`).
6. **Caches aren't always rebuildable locally.** On metered/slow links,
   an HF model cache can cost real money/time to re-download. Check the
   restore-cost column, not just size.
7. **One-shot experiments in /tmp die anyway** - don't waste review time
   there; exclude tmp dirs from scans.

## Verification Checklist

- [ ] Scan ran with default (report-only) mode - no deletions happened yet
- [ ] Every deletion candidate has a stated reason + restore cost
- [ ] Repos with dirty worktree / unpushed commits are in PROTECTED (or archived, not deleted)
- [ ] Docker images used by any container are protected
- [ ] Cleanup commands were human-reviewed before execution
- [ ] Post-cleanup rescan confirms freed bytes
