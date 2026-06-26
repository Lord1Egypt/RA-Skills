#!/usr/bin/env bash
set -euo pipefail

WS="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
DIST="${OPENCLAW_UI_ASSETS_DIR:-/opt/homebrew/lib/node_modules/openclaw/dist/control-ui/assets}"

BACKUP_ROOT="$WS/_deleted/ponddepth-install-backups"

echo "Uninstall: PondDepth Levels"
echo "- workspace: $WS"
echo "- ui assets:  $DIST"

# 1) Best-effort restore from most recent backup
if [[ -d "$BACKUP_ROOT" ]]; then
  LAST_BACKUP="$(ls -1 "$BACKUP_ROOT" 2>/dev/null | sort | tail -n 1)" || true
  if [[ -n "${LAST_BACKUP:-}" && -d "$BACKUP_ROOT/$LAST_BACKUP" ]]; then
    if [[ -f "$BACKUP_ROOT/$LAST_BACKUP/ponddepth-badge.js" ]]; then
      echo "Restoring ponddepth-badge.js from backup: $LAST_BACKUP"
      cp -f "$BACKUP_ROOT/$LAST_BACKUP/ponddepth-badge.js" "$DIST/ponddepth-badge.js"
    fi
  fi
fi

# 2) Remove PondDepth assets
if [[ -f "$DIST/ponddepth-badge.js" ]]; then
  echo "Removing: $DIST/ponddepth-badge.js"
  rm -f "$DIST/ponddepth-badge.js"
fi

if [[ -d "$DIST/ponddepth-icons" ]]; then
  echo "Removing: $DIST/ponddepth-icons/"
  rm -rf "$DIST/ponddepth-icons"
fi

echo "OK: removed PondDepth UI assets. Hard refresh Control UI."