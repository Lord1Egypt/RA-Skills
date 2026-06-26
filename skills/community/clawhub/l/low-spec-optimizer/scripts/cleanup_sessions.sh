#!/bin/bash
# cleanup_sessions.sh — Free memory by cleaning stale OpenClaw sessions and caches
# Options:
#   --dry-run    Show what would be cleaned without doing it
#   --aggressive Also clear npm/pip caches and journal logs

set -euo pipefail

DRY_RUN=false
AGGRESSIVE=false

for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=true ;;
    --aggressive) AGGRESSIVE=true ;;
  esac
done

freed_kb=0

clean() {
  local desc="$1" path="$2"
  if [ -d "$path" ] || [ -f "$path" ]; then
    size=$(du -sk "$path" 2>/dev/null | awk '{print $1}')
    if [ "$DRY_RUN" = true ]; then
      echo "[DRY-RUN] Would clean: $desc ($path) — ${size}KB"
    else
      rm -rf "$path"
      echo "[CLEANED] $desc — freed ${size}KB"
      freed_kb=$((freed_kb + size))
    fi
  fi
}

echo "=== OpenClaw Session Cleanup ==="
echo ""

# 1. Stale subagent sessions (older than 1h)
if [ -d /home/nvi/.openclaw/sessions ]; then
  stale_count=$(find /home/nvi/.openclaw/sessions -maxdepth 1 -type d -mmin +60 2>/dev/null | wc -l)
  if [ "$stale_count" -gt 1 ]; then
    echo "Found $((stale_count - 1)) stale session(s)"
    if [ "$DRY_RUN" = true ]; then
      find /home/nvi/.openclaw/sessions -maxdepth 1 -type d -mmin +60 -exec echo "[DRY-RUN] Would remove: {}" \;
    else
      find /home/nvi/.openclaw/sessions -maxdepth 1 -type d -mmin +60 -exec rm -rf {} + 2>/dev/null || true
      echo "[CLEANED] Stale sessions removed"
    fi
  fi
fi

# 2. Trash folder (if > 50MB)
if [ -d /home/nvi/.openclaw/trash ]; then
  trash_mb=$(du -sm /home/nvi/.openclaw/trash 2>/dev/null | awk '{print $1}')
  if [ "${trash_mb:-0}" -gt 50 ]; then
    clean "OpenClaw trash (${trash_mb}MB)" /home/nvi/.openclaw/trash
  fi
fi

# 3. Browser profiles cache
clean "Browser cache" /home/nvi/.cache/ms-playwright

# 4. Aggressive cleanups
if [ "$AGGRESSIVE" = true ]; then
  echo ""
  echo "=== Aggressive Cleanup ==="

  # npm cache
  if command -v npm &>/dev/null; then
    if [ "$DRY_RUN" = true ]; then
      echo "[DRY-RUN] Would run: npm cache clean --force"
    else
      npm cache clean --force 2>/dev/null && echo "[CLEANED] npm cache"
    fi
  fi

  # pip cache
  if command -v pip3 &>/dev/null; then
    if [ "$DRY_RUN" = true ]; then
      echo "[DRY-RUN] Would run: pip3 cache purge"
    else
      pip3 cache purge 2>/dev/null && echo "[CLEANED] pip cache"
    fi
  fi

  # journal logs older than 3 days
  if command -v journalctl &>/dev/null; then
    if [ "$DRY_RUN" = true ]; then
      echo "[DRY-RUN] Would run: journalctl --vacuum-time=3d"
    else
      journalctl --vacuum-time=3d 2>/dev/null && echo "[CLEANED] journal logs"
    fi
  fi
fi

# Summary
echo ""
if [ "$DRY_RUN" = true ]; then
  echo "=== Dry run complete (no changes made) ==="
else
  freed_mb=$((freed_kb / 1024))
  echo "=== Done — freed ~${freed_mb}MB ==="
fi
