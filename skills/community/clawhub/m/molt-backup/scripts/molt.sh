#!/bin/bash
# molt.sh — Sync OpenClaw brain files to an offsite git repo
#
# Usage:
#   molt.sh [--workspace DIR] [--repo-url URL] [--backup-dir DIR] [--extra-dirs dir1,dir2] [--dry-run]
#
# Config (env or defaults):
#   MOLT_WORKSPACE    Workspace directory (default: ~/.openclaw/workspace)
#   MOLT_REPO_URL     Remote git repo URL (required if backup dir not already a repo)
#   MOLT_DIR          Local backup directory (default: ~/.openclaw/molt)
#   MOLT_EXTRA_DIRS   Comma-separated list of extra workspace dirs to include (e.g. scripts,notes)

set -euo pipefail

# ── Defaults ────────────────────────────────────────────────────────────────

WORKSPACE="${MOLT_WORKSPACE:-$HOME/.openclaw/workspace}"
BACKUP_DIR="${MOLT_DIR:-$HOME/.openclaw/molt}"
REPO_URL="${MOLT_REPO_URL:-}"
EXTRA_DIRS="${MOLT_EXTRA_DIRS:-}"
DRY_RUN=false

# ── Arg parsing ──────────────────────────────────────────────────────────────

while [[ $# -gt 0 ]]; do
  case "$1" in
    --workspace) WORKSPACE="$2"; shift 2 ;;
    --repo-url)  REPO_URL="$2";  shift 2 ;;
    --backup-dir) BACKUP_DIR="$2"; shift 2 ;;
    --extra-dirs) EXTRA_DIRS="$2"; shift 2 ;;
    --dry-run)   DRY_RUN=true;   shift ;;
    *) echo "Unknown arg: $1"; exit 1 ;;
  esac
done

# ── Init backup repo ─────────────────────────────────────────────────────────

if [ ! -d "$BACKUP_DIR/.git" ]; then
  if [ -z "$REPO_URL" ]; then
    echo "[molt] ERROR: Backup dir '$BACKUP_DIR' is not a git repo and --repo-url not set."
    exit 1
  fi
  echo "[molt] Cloning $REPO_URL → $BACKUP_DIR"
  git clone "$REPO_URL" "$BACKUP_DIR"
fi

cd "$BACKUP_DIR"
echo "[molt] Pulling latest from remote..."
git pull --rebase origin "$(git rev-parse --abbrev-ref HEAD)" || {
  echo "[molt] WARNING: git pull failed, continuing with local state"
}

# ── Copy brain files ─────────────────────────────────────────────────────────

echo "[molt] Syncing brain files from $WORKSPACE..."

BRAIN_FILES=(AGENTS.md SOUL.md TOOLS.md IDENTITY.md USER.md HEARTBEAT.md MEMORY.md)

for f in "${BRAIN_FILES[@]}"; do
  src="$WORKSPACE/$f"
  if [ -f "$src" ]; then
    cp "$src" .
    echo "  ✓ $f"
  else
    echo "  - $f (not found, skipping)"
  fi
done

# Memory directory
if [ -d "$WORKSPACE/memory" ]; then
  mkdir -p memory
  rsync -a --delete "$WORKSPACE/memory/" memory/
  echo "  ✓ memory/"
fi

# Extra directories
if [ -n "$EXTRA_DIRS" ]; then
  IFS=',' read -ra DIRS <<< "$EXTRA_DIRS"
  for dir in "${DIRS[@]}"; do
    dir="${dir// /}"  # trim spaces
    src="$WORKSPACE/$dir"
    if [ -d "$src" ]; then
      mkdir -p "$dir"
      rsync -a --delete "$src/" "$dir/"
      echo "  ✓ $dir/ (extra)"
    else
      echo "  - $dir/ (not found, skipping)"
    fi
  done
fi

# ── Export cron jobs + config ─────────────────────────────────────────────────

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if command -v python3 &>/dev/null; then
  python3 "$SCRIPT_DIR/export-cron-jobs.py" "$BACKUP_DIR/cron-jobs"
  # Export redacted config — delegates redaction to `openclaw config get` (authoritative)
  # Falls back to file-based redaction if CLI unavailable
  CONFIG_PATH="$(dirname "$WORKSPACE")/openclaw.json"
  python3 "$SCRIPT_DIR/export-config.py" "$BACKUP_DIR/config-redacted.json" "$CONFIG_PATH"
else
  echo "  - cron-jobs/config (python3 not found, skipping)"
fi

# ── Commit & push ─────────────────────────────────────────────────────────────

git add -A

if git diff --cached --quiet; then
  echo "[molt] Nothing changed — already up to date."
  exit 0
fi

COMMIT_MSG="molt $(date '+%Y-%m-%d %H:%M %Z')"

if [ "$DRY_RUN" = true ]; then
  echo "[molt] DRY RUN — would commit: $COMMIT_MSG"
  git diff --cached --stat
  git restore --staged .
else
  git commit -m "$COMMIT_MSG"
  git push origin "$(git rev-parse --abbrev-ref HEAD)"
  echo "[molt] ✓ Pushed: $COMMIT_MSG"
fi
