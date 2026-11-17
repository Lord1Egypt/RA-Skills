# The Dev-Cleanup Playbook

Companion to `dev_janitor.py`. Rules of engagement, per-artifact deletion
safety, restore-cost thinking, and the command cookbook.

## 1. The prime directive

**Nothing is deleted by a script. Scripts produce manifests; humans execute.**
The only exceptions are artifacts that are (a) trivially rebuildable and
(b) unattached to any live project - compiled caches, orphaned build dirs.
Even then: batch-execute smallest-risk first, rescan between batches.

## 2. Decision matrix

```
                    rebuildable cheaply?
                    yes                no
active project    | keep             | keep
stale, attached   | keep (project    | keep; ask owner
                  | may wake)        | about the project
stale, orphaned   | DELETE           | ARCHIVE then delete
protected flag    | keep             | keep
```

"Orphaned" = no project references it AND project is itself stale.
"Archive" = compressed tarball moved to cold storage (external disk,
network share) with a manifest line noting where.

## 3. Per-artifact rules

### Git repos
- Date = last commit (`git log -1 --format=%ct`). NOT file mtimes.
- PROTECT if: dirty worktree, stashes, unpushed commits on any branch,
  no remote configured AND any local-only commits, commit < stale window.
- Safe delete = clean, fully pushed, stale beyond window. Re-clone cost is
  seconds-to-minutes; your fork/clone URL is in `git remote -v` - record it
  in the manifest before deleting.
- Before deleting a repo with local-only branches: `git bundle create
  ../$(basename $PWD).bundle --all` - 10 MB insurance for years.

### Python virtualenvs
- A venv is disposable ONLY if (a) no active project references its path and
  (b) rebuilding is cheap (requirements lockfile present). Check for
  `requirements.txt` / `pyproject.toml` / `poetry.lock` / `uv.lock` in the
  referencing project before deleting its venv.
- Search for references: `grep -rn "<venvpath>" <project roots> /etc/systemd`
  (activation scripts, IDE configs, cron lines, systemd units).
- Rebuild cost: `pip install -r requirements.txt` - minutes on fast link,
  hours on ARM SBCs compiling numpy. The manifest estimates this.

### node_modules
- Almost always safe to delete when the project is stale; `npm ci` restores
  exactly from lockfile. The whole POINT of node_modules is disposability.
- Danger: projects with patched/node_modules-symlink setups (pnpm workspaces,
  yarn link, patched packages). If `.patches/`, `patches/`, or workspace
  root has `pnpm-workspace.yaml` - downgrade to manual review.

### Docker
- Images: `docker image ls --format` + `docker ps -a` cross-reference.
  Image used by ANY container (running or exited) = PROTECTED.
- Dangling images (`<none>` tags) are layers from interrupted builds -
  genuinely safe: `docker image prune -f`.
- Tagged but unused: `docker image prune -a --filter "until=720h"` after
  human review of the list.
- Volumes: `docker volume ls -f dangling=true`. A dangling volume may hold
  a DATABASE - list contents (`docker run --rm -v VOL:/data alpine ls /data`)
  before deleting. Never bulk-delete volumes.
- Build cache: `docker builder prune` - safe, often 10-50 GB on CI boxes.

### Caches (pip/npm/uv/poetry/go/hf)
- pip: `pip cache purge` or `rm -rf ~/.cache/pip` - always rebuildable.
- npm: `npm cache clean --force`.
- uv: `uv cache clean`.
- HF models: NOT always cheap - a 40 GB Llama re-download on slow/metered
  link costs hours/money. Check `~/.cache/huggingface/hub` per-model mtimes;
  protect models < 30d or referenced by active configs (grep configs for
  model IDs).

### Model weight files (~/models, *.gguf, *.safetensors)
- Date by mtime; protect if any config/compose/script references the
  filename (grep the repo roots). These are expensive to restore -
  archive to cold storage rather than delete when in doubt.

### Build artifacts (dist/, build/, target/, .next/, out/)
- Safe when the project is stale; rebuild cost = one build. Deleting
  build dirs of ACTIVE projects wastes the next build's cache - keep.

## 4. Restore-cost classes

| Class | Examples | Cost to restore |
|---|---|---|
| A - seconds | node_modules (npm ci), pip cache | just do it |
| B - minutes | venv with lockfile, public repo re-clone | fine |
| C - tens of minutes | compiled-from-source deps on SBC, big image pull | fine if planned |
| D - hours / metered | HF model cache, private images no longer tagged | archive first |
| E - impossible | unpushed commits, uncommitted work, dead-volume data | never delete |

The manifest prints the class for every candidate. E-class items are never
candidates - they're PROTECTED with reason.

## 5. Command cookbook

```bash
# Who ate my disk (the honest version)
du -xh --max-depth=2 ~ 2>/dev/null | sort -rh | head -30

# Repo staleness at a glance
for r in $(find ~/dev -maxdepth 3 -name .git -type d | sed 's|/.git||'); do
  echo "$(git -C $r log -1 --format=%cs 2>/dev/null || echo NOGIT) $r"
done | sort

# Unpushed check per repo (any branch with commits not on a remote)
git fetch --quiet && git for-each-ref --format='%(refname:short) %(upstream:track)' refs/heads | grep -v '\[gone\]'

# Docker truth
docker system df -v          # the full table
docker ps -a --format '{{.Image}} {{.Status}}'

# venv referenced by cron/systemd?
grep -rn "venv\|virtualenv" /etc/systemd/ /etc/cron* ~/.crontab 2>/dev/null
```

## 6. Suggested cadence

- **Weekly (2 min):** `docker builder prune`, `pip cache purge` on CI boxes.
- **Quarterly (30 min):** full janitor scan, review manifest, batch 1
  (caches + build dirs), maybe batch 2 (orphaned venvs).
- **Yearly:** repo archive-or-delete pass; model-file audit.

## 7. Homelab/SBC notes (Orange Pi / RPi class)

- SD/eMMC wear: prefer deleting caches over thrashing big tar operations;
  `fstrim` after large deletions on SSD-backed storage.
- Compile-heavy restores (numpy on Cortex-A53) are class C-D, not B -
  weigh deleting source-built venvs accordingly.
- Watch `log2ram`/tmpfs sizes - full /tmp on small boards mimics disk-full.
