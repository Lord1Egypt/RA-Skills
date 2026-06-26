#!/usr/bin/env bash
set -euo pipefail

# Muster Uninstall Script
# Removes all Muster components. Agent should confirm with human first.
#
# Supports both launchd (macOS) and pm2 (Linux/fallback) service modes.
# Auto-detects and cleans up whichever is in use.
#
# Usage: bash uninstall.sh --confirm [--keep-data] [--export DIR] [--install-dir DIR]
#
# --confirm       Required. Prevents accidental runs.
# --keep-data     Skips database removal.
# --export DIR    Exports database before teardown.

INSTALL_DIR="${INSTALL_DIR:-$HOME/muster}"
CONFIRMED=false
KEEP_DATA=false
EXPORT_DIR=""
OPENCLAW_WORKSPACE=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --confirm) CONFIRMED=true; shift ;;
    --keep-data) KEEP_DATA=true; shift ;;
    --export) EXPORT_DIR="$2"; shift 2 ;;
    --install-dir) INSTALL_DIR="$2"; shift 2 ;;
    --workspace) OPENCLAW_WORKSPACE="$2"; shift 2 ;;
    *) echo "Unknown: $1" >&2; exit 1 ;;
  esac
done

if [ "$CONFIRMED" != "true" ]; then
  echo "[muster-uninstall] Run with --confirm to proceed." >&2
  echo "[muster-uninstall]   --keep-data   Preserve database" >&2
  echo "[muster-uninstall]   --export DIR  Export database first" >&2
  exit 1
fi

log() { echo "[muster-uninstall] $*" >&2; }
REMOVED=()
SKIPPED=()

# Auto-detect workspace if not provided
if [ -z "$OPENCLAW_WORKSPACE" ]; then
  OPENCLAW_WORKSPACE="$HOME/.openclaw/workspace"
fi

# Auto-detect DB mode
detect_db_mode() {
  if [ -f "$INSTALL_DIR/docker-compose.yml" ] && docker compose -f "$INSTALL_DIR/docker-compose.yml" ps --quiet 2>/dev/null | grep -q .; then
    echo "docker"
  elif brew services list 2>/dev/null | grep -q "postgresql.*started"; then
    echo "homebrew"
  elif [ -f "$INSTALL_DIR/docker-compose.yml" ]; then
    echo "docker"
  else
    echo "unknown"
  fi
}

DB_MODE=$(detect_db_mode)
log "Detected DB mode: $DB_MODE"

# --- Phase 1: Export ---
if [ -n "$EXPORT_DIR" ]; then
  log "Phase 1: Exporting..."
  mkdir -p "$EXPORT_DIR"

  EXPORT_FILE="$EXPORT_DIR/muster-export-$(date +%Y%m%d-%H%M%S).sql"
  if [ "$DB_MODE" = "docker" ] && [ -f "$INSTALL_DIR/docker-compose.yml" ]; then
    cd "$INSTALL_DIR"
    docker compose exec -T db pg_dump -U muster muster > "$EXPORT_FILE" 2>/dev/null && {
      REMOVED+=("exported:$EXPORT_FILE"); log "✓ Database exported (Docker)"
    } || SKIPPED+=("database export (pg_dump failed)")
  elif [ "$DB_MODE" = "homebrew" ]; then
    pg_dump muster > "$EXPORT_FILE" 2>/dev/null && {
      REMOVED+=("exported:$EXPORT_FILE"); log "✓ Database exported (Homebrew)"
    } || SKIPPED+=("database export (pg_dump failed)")
  else
    SKIPPED+=("database export (no DB detected)")
  fi

  [ -d "$HOME/.muster" ] && cp -r "$HOME/.muster" "$EXPORT_DIR/muster-state/"
fi

# --- Phase 2: Stop services ---
log "Phase 2: Stopping services..."

# launchd services
for label in com.bai.muster com.bai.muster-tunnel; do
  PLIST="$HOME/Library/LaunchAgents/${label}.plist"
  if launchctl list "$label" &>/dev/null 2>&1; then
    launchctl bootout "gui/$(id -u)/$label" 2>/dev/null || true
    REMOVED+=("launchd:$label"); log "✓ Stopped $label (launchd)"
  else
    SKIPPED+=("launchd:$label (not loaded)")
  fi
  [ -f "$PLIST" ] && { rm -f "$PLIST"; REMOVED+=("plist:$PLIST"); }
done

# pm2 services (clean up if they exist too)
if command -v pm2 &>/dev/null; then
  for proc in muster muster-tunnel; do
    if pm2 describe "$proc" &>/dev/null 2>&1; then
      pm2 stop "$proc" 2>/dev/null; pm2 delete "$proc" 2>/dev/null
      REMOVED+=("pm2:$proc"); log "✓ Stopped $proc (pm2)"
    fi
  done
  pm2 save 2>/dev/null || true
fi

# --- Phase 3: Database ---
log "Phase 3: Removing database..."

if [ "$KEEP_DATA" = "true" ]; then
  SKIPPED+=("database (--keep-data)")
elif [ "$DB_MODE" = "docker" ] && [ -f "$INSTALL_DIR/docker-compose.yml" ]; then
  cd "$INSTALL_DIR"
  docker compose down -v 2>/dev/null; REMOVED+=("database+volumes (Docker)")
elif [ "$DB_MODE" = "homebrew" ]; then
  dropdb muster 2>/dev/null && REMOVED+=("database (Homebrew)") || SKIPPED+=("database (dropdb failed or already gone)")
fi

# --- Phase 4: Clean HEARTBEAT.md ---
log "Phase 4: Cleaning HEARTBEAT.md..."

# Clean all known workspace locations
HEARTBEAT_LOCATIONS=(
  "$OPENCLAW_WORKSPACE/HEARTBEAT.md"
)
# Also check multi-agent workspace paths
for agent_dir in "$HOME"/bai-agent-system/agents/*/workspace; do
  [ -d "$agent_dir" ] && HEARTBEAT_LOCATIONS+=("$agent_dir/HEARTBEAT.md")
done

for HEARTBEAT_FILE in "${HEARTBEAT_LOCATIONS[@]}"; do
  if [ -f "$HEARTBEAT_FILE" ] && grep -q "## Muster check-in" "$HEARTBEAT_FILE"; then
    python3 << PYEOF
import re, sys
hb_path = "${HEARTBEAT_FILE}"
with open(hb_path) as f:
    content = f.read()
content = re.sub(r'\n## Muster check-in.*?(?=\n## |\Z)', '', content, flags=re.DOTALL)
with open(hb_path, 'w') as f:
    f.write(content.strip() + '\n')
PYEOF
    REMOVED+=("HEARTBEAT section:$HEARTBEAT_FILE"); log "✓ Cleaned $HEARTBEAT_FILE"
  fi
done

# --- Phase 5: Remove state and config ---
log "Phase 5: Removing state..."
[ -d "$HOME/.muster" ] && { rm -rf "$HOME/.muster"; REMOVED+=("~/.muster"); } || SKIPPED+=("~/.muster")

# Clean pm2 logs if pm2 exists
if command -v pm2 &>/dev/null; then
  rm -f "$HOME/.pm2/logs/muster-"* "$HOME/.pm2/logs/muster-tunnel-"* 2>/dev/null && REMOVED+=("pm2 logs")
fi

# macOS Keychain
[ "$(uname -s)" = "Darwin" ] && security delete-generic-password -s "Muster API key" 2>/dev/null && REMOVED+=("Keychain entry")

# --- Phase 6: Remove Muster files ---
log "Phase 6: Removing Muster..."
[ -d "$INSTALL_DIR" ] && { rm -rf "$INSTALL_DIR"; REMOVED+=("$INSTALL_DIR"); } || SKIPPED+=("$INSTALL_DIR")

# --- Phase 7: Remove skill (LAST) ---
log "Phase 7: Removing skill..."
for loc in "$OPENCLAW_WORKSPACE/skills/muster" "$HOME/.openclaw/skills/muster"; do
  [ -d "$loc" ] && { rm -rf "$loc"; REMOVED+=("$loc"); log "✓ Removed $loc"; }
done
# Also check multi-agent skill directories
for agent_dir in "$HOME"/bai-agent-system/agents/*/workspace/skills/muster; do
  [ -d "$agent_dir" ] && { rm -rf "$agent_dir"; REMOVED+=("$agent_dir"); log "✓ Removed $agent_dir"; }
done

# --- Report ---
REMOVED_JSON=$(printf '%s\n' "${REMOVED[@]}" | python3 -c "import sys,json;print(json.dumps([l.strip() for l in sys.stdin if l.strip()]))" 2>/dev/null || echo '[]')
SKIPPED_JSON=$(printf '%s\n' "${SKIPPED[@]}" | python3 -c "import sys,json;print(json.dumps([l.strip() for l in sys.stdin if l.strip()]))" 2>/dev/null || echo '[]')

cat <<REPORT_JSON
{
  "success": true,
  "keep_data": ${KEEP_DATA},
  "db_mode": "${DB_MODE}",
  "exported": $([ -n "$EXPORT_DIR" ] && echo "\"$EXPORT_DIR\"" || echo "null"),
  "removed": ${REMOVED_JSON},
  "skipped": ${SKIPPED_JSON},
  "note": "Remove muster entry from ~/.openclaw/openclaw.json manually."
}
REPORT_JSON
log "========================================="
log "  Muster uninstall complete."
log "========================================="
