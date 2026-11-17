# Last-Login Janitor

**Your dev machine has 200 GB of things you haven't touched in a year. You're
afraid to delete any of it. This is why your disk is full.**

## The problem

Every developer accumulates: 38 cloned repos (7 abandoned), 22 virtualenvs
(14 orphaned — their projects are gone), `node_modules` from failed
experiments, 12 versions of the same Docker image, pip/npm/HF caches, and
model files from interests that passed. Homelab SBCs get it worse —
small disks, compile-from-source restores.

Cleanup is dangerous when done blindly:
- Delete the venv a cron job or systemd unit uses → silent service death
- Delete the image a *stopped* container references → can't restart it
- Delete the repo with unpushed commits → the work is gone forever
- Delete an HF model cache on a metered link → 40 GB re-download

So nobody cleans up. Disks hit 100%. Builds fail. Databases corrupt.

## The solution

`dev_janitor.py` makes cleanup **decision-safe**. One read-only scan:

1. **Finds** every artifact class: repos, venvs, node_modules, Docker
   images/volumes, pip/npm/uv/go/gradle/HF caches, build dirs
2. **Dates** each by its truth signal — last *commit* for repos (file mtimes
   lie after a checkout), last access for venvs, container usage for images
3. **Protects** anything with a live reason to exist: dirty worktrees,
   unpushed commits, stashes, images used by any container (running or
   stopped), venvs whose project is newer than they are, warm caches
4. **Ranks** stale candidates by size with reason + restore-cost class
   (A = seconds to rebuild … E = impossible), and prints conservative
   reviewable cleanup commands

It never deletes anything. It produces the evidence for YOUR decision.

## Quick start

```bash
# Audit your dev tree (read-only)
python3 scripts/dev_janitor.py scan ~/dev --stale-days 180

# Full home audit including Docker, with JSON manifest
python3 scripts/dev_janitor.py scan ~ --docker --manifest cleanup.json

# Conservative first move (always safe):
# review only the cache + node_modules + build_dir lines in the manifest
```

## What you get

```
DEV DISK AUDIT — sizing by artifact type
  node_modules       18.2G  (31 items)
  venv                9.4G  (12 items)
  ...
STALE CANDIDATES (review top-down; 23 items, 31.5G reclaimable)
   4.1G  2024-11-02  [node_modules] ~/dev/old-experiment/node_modules
         reason: stale | restore: A (npm ci)
   2.8G  2024-08-15  [repo] ~/dev/abandoned-startup
         reason: clean+pushed | restore: B (re-clone)
PROTECTED (9 items) — do NOT delete on autopilot
   3.2G  [repo] ~/dev/current-job
         dirty worktree; unpushed: feature/auth
SUGGESTED COMMANDS — review each line before running
```

## Who needs this

- Anyone whose laptop/workstation says "disk almost full"
- Homelab / SBC operators (small disks, expensive restores)
- Teams auditing inherited machines ("what here is actually alive?")
- CI boxes drowning in Docker layers and caches

## Files

- `SKILL.md` — workflow, protection rules, pitfalls
- `scripts/dev_janitor.py` — the scanner (stdlib-only, read-only)
- `references/cleanup-playbook.md` — per-artifact deletion safety, restore
  costs, command cookbook, cadence

## Safety

Read-only by design. Output separates STALE (candidates) from PROTECTED
(with reasons). E-class restore items (unpushed work, volumes with data)
are never deletion candidates. Manifest includes per-item reasons so a
second human can review.

## License

MIT © Denis Voronin
