#!/bin/bash
# memory-backup.sh — Auto-backup workspace to GitHub
# Run via cron or manually. Only pushes if there are changes.

set -euo pipefail

WORKSPACE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
cd "$WORKSPACE"

# Ensure git is initialized
if [ ! -d .git ]; then
  echo "[backup] No git repo in workspace, skipping"
  exit 0
fi

# Backup openclaw.json (lives outside workspace)
OPENCLAW_CFG="$WORKSPACE/../openclaw.json"
[ -f "$OPENCLAW_CFG" ] && cp "$OPENCLAW_CFG" "$WORKSPACE/openclaw.json.backup"

# Backup crontab
crontab -l > "$WORKSPACE/crontab.backup" 2>/dev/null || true

# Check for changes
git add -A
if git diff --cached --quiet; then
  echo "[backup] No changes to push"
  exit 0
fi

# Commit and push
TIMESTAMP=$(date '+%Y-%m-%d %H:%M')
git commit -m "auto-backup: $TIMESTAMP" --quiet
git push origin main --quiet 2>&1 && echo "[backup] Pushed at $TIMESTAMP" || echo "[backup] Push failed (check network)"
