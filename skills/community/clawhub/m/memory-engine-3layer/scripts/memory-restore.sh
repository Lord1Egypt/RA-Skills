#!/bin/bash
# memory-restore.sh — Restore workspace from GitHub backup after OpenClaw reinstall
#
# Usage:
#   1. Install OpenClaw fresh
#   2. Run: bash memory-restore.sh <github-repo-url>
#   3. Example: bash memory-restore.sh https://github.com/ZackO2o/openclaw-workspace.git
#
# What it restores:
#   - MEMORY.md, memory/*.md (all memories)
#   - SOUL.md, USER.md, IDENTITY.md (personality)
#   - AGENTS.md, TOOLS.md, HEARTBEAT.md (behavior rules)
#   - skills/ (all installed skills)
#   - openclaw.json.backup → ~/.openclaw/openclaw.json
#   - crontab.backup → crontab
#
# What it rebuilds:
#   - .memory/index.sqlite (search index from md files)

set -euo pipefail

REPO_URL="${1:-}"
WORKSPACE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"

if [ -z "$REPO_URL" ]; then
  echo "Usage: bash memory-restore.sh <github-repo-url>"
  echo "Example: bash memory-restore.sh https://<token>@github.com/ZackO2o/openclaw-workspace.git"
  exit 1
fi

echo "=== Memory Engine Restore ==="
echo "Target: $WORKSPACE"
echo "Source: $REPO_URL"
echo ""

# Safety check
if [ -f "$WORKSPACE/MEMORY.md" ]; then
  echo "⚠️  WARNING: $WORKSPACE/MEMORY.md already exists!"
  read -p "Overwrite existing workspace? (y/N) " confirm
  if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
    echo "Aborted."
    exit 1
  fi
fi

# Clone or pull
if [ -d "$WORKSPACE/.git" ]; then
  echo "[restore] Pulling latest from remote..."
  cd "$WORKSPACE" && git pull origin main
else
  echo "[restore] Cloning backup..."
  mkdir -p "$(dirname "$WORKSPACE")"
  git clone "$REPO_URL" "$WORKSPACE"
fi

cd "$WORKSPACE"

# Restore openclaw.json
if [ -f "openclaw.json.backup" ]; then
  echo "[restore] Restoring openclaw.json..."
  cp openclaw.json.backup "$WORKSPACE/../openclaw.json"
  echo "  ✅ openclaw.json restored"
else
  echo "  ⚠️  No openclaw.json.backup found"
fi

# Restore crontab
if [ -f "crontab.backup" ]; then
  echo "[restore] Restoring crontab..."
  crontab crontab.backup
  echo "  ✅ crontab restored"
else
  echo "  ⚠️  No crontab.backup found"
fi

# Rebuild search index
echo "[restore] Rebuilding search index..."
SCRIPTS="$WORKSPACE/skills/memory-engine/scripts"
if [ -f "$SCRIPTS/memory-index.js" ]; then
  node "$SCRIPTS/memory-index.js" --workspace "$WORKSPACE" --force
  echo "  ✅ Search index rebuilt"
else
  echo "  ⚠️  memory-index.js not found, install memory-engine skill first"
fi

# Verify
echo ""
echo "=== Restore Complete ==="
if [ -f "$SCRIPTS/memory-boot.js" ]; then
  node "$SCRIPTS/memory-boot.js" --workspace "$WORKSPACE"
fi
echo ""
echo "Next steps:"
echo "  1. Restart OpenClaw: openclaw gateway restart"
echo "  2. Verify: openclaw status"
echo "  3. Test memory: node $SCRIPTS/memory-search.js \"test query\""
