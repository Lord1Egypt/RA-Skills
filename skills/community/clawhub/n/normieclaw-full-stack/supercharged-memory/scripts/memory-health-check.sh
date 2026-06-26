#!/usr/bin/env bash
# =============================================================================
# Supercharged Memory — Health Check Script
# Validates QMD collections, checks freshness, alerts if stale.
# Usage: bash scripts/memory-health-check.sh [workspace_root]
# =============================================================================

set -euo pipefail
umask 077

# --- Configuration ---
RAW_WORKSPACE="${1:-$(pwd)}"
if ! WORKSPACE="$(cd "$RAW_WORKSPACE" 2>/dev/null && pwd -P)"; then
  echo "[ERROR] Workspace directory does not exist or is not accessible: $RAW_WORKSPACE" >&2
  exit 1
fi
CONFIG_FILE="${WORKSPACE}/config/memory-config.json"
STATE_FILE="${WORKSPACE}/memory/health-state.json"
HEARTBEAT_FILE="${WORKSPACE}/memory/heartbeat-state.json"
MEMORY_MD="${WORKSPACE}/MEMORY.md"
ALERTS=()
WARNINGS=()

# --- Helpers ---
timestamp() { date "+%Y-%m-%d %H:%M:%S"; }
today() { date "+%Y-%m-%d"; }
current_hour() { date "+%H"; }
epoch_now() { date +%s; }

log() { echo "[$(timestamp)] $1"; }

add_alert() {
  ALERTS+=("⚠️ $1")
  log "ALERT: $1"
}

add_ok() {
  log "✅ $1"
}

# --- Load config thresholds (with defaults) ---
MEMORY_MD_STALE_HOURS=48
REINDEX_OVERDUE_HOURS=3
DAILY_NOTES_REQUIRED_AFTER=14
MAX_MEMORY_MD_CHARS=6000

if [ -f "$CONFIG_FILE" ] && command -v python3 &>/dev/null; then
  config_values="$(python3 - "$CONFIG_FILE" <<'PYEOF'
import json
import sys

defaults = (48, 3, 14, 6000)

def to_safe_int(value, default):
    return str(value) if isinstance(value, int) and value >= 0 else str(default)

try:
    with open(sys.argv[1], encoding="utf-8") as f:
        config = json.load(f)
    hc = config.get("health_check", {})
    mm = config.get("memory_md", {})
    values = (
        to_safe_int(hc.get("memory_md_stale_hours", 48), 48),
        to_safe_int(hc.get("reindex_overdue_hours", 3), 3),
        to_safe_int(hc.get("daily_notes_required_after_hour", 14), 14),
        to_safe_int(mm.get("max_memory_md_chars", 6000), 6000),
    )
except Exception:
    values = tuple(str(v) for v in defaults)

print("|".join(values))
PYEOF
)"
  IFS='|' read -r cfg_stale cfg_reindex cfg_daily cfg_maxchars <<< "$config_values"
  [[ "$cfg_stale" =~ ^[0-9]+$ ]] && MEMORY_MD_STALE_HOURS="$cfg_stale"
  [[ "$cfg_reindex" =~ ^[0-9]+$ ]] && REINDEX_OVERDUE_HOURS="$cfg_reindex"
  [[ "$cfg_daily" =~ ^[0-9]+$ ]] && DAILY_NOTES_REQUIRED_AFTER="$cfg_daily"
  [[ "$cfg_maxchars" =~ ^[0-9]+$ ]] && MAX_MEMORY_MD_CHARS="$cfg_maxchars"
fi

log "=== Memory Health Check ==="
log "Workspace: $WORKSPACE"

# --- Check 1: QMD installed and collections exist ---
QMD_COLLECTION_COUNT=0
declare -A QMD_COLLECTIONS

if command -v qmd &>/dev/null; then
  add_ok "QMD is installed"

  # Parse collection list
  while IFS= read -r line; do
    # Try to extract collection name and doc count
    coll=$(echo "$line" | awk '{print $1}' | tr -d ':')
    docs=$(echo "$line" | grep -oE '[0-9]+ (docs|documents|files)' | grep -oE '[0-9]+' | head -1 || echo "0")
    if [ -n "$coll" ] && [ "$coll" != "Name" ] && [ "$coll" != "---" ]; then
      QMD_COLLECTIONS["$coll"]="${docs:-0}"
      QMD_COLLECTION_COUNT=$((QMD_COLLECTION_COUNT + 1))
    fi
  done < <(qmd collection list 2>/dev/null || true)

  if [ "$QMD_COLLECTION_COUNT" -eq 0 ]; then
    add_alert "No QMD collections found. Run scripts/qmd-reindex.sh to create them."
  else
    add_ok "QMD has $QMD_COLLECTION_COUNT collection(s)"

    # Check for expected collections
    for expected in "workspace" "memory"; do
      if [ -z "${QMD_COLLECTIONS[$expected]+x}" ]; then
        add_alert "Expected QMD collection '$expected' is missing. Run reindex."
      else
        docs="${QMD_COLLECTIONS[$expected]}"
        if [ "$docs" = "0" ]; then
          add_alert "QMD collection '$expected' exists but has 0 documents."
        else
          add_ok "Collection '$expected': $docs documents"
        fi
      fi
    done
  fi
else
  add_alert "QMD is not installed. Memory search is degraded (falling back to grep). Install with: brew install qmd"
fi

# --- Check 2: MEMORY.md exists and is fresh ---
if [ -f "$MEMORY_MD" ]; then
  # Check modification time
  if command -v stat &>/dev/null; then
    # macOS stat
    mod_epoch=$(stat -f %m "$MEMORY_MD" 2>/dev/null || stat -c %Y "$MEMORY_MD" 2>/dev/null || echo "0")
    now_epoch=$(epoch_now)
    age_hours=$(( (now_epoch - mod_epoch) / 3600 ))

    if [ "$age_hours" -gt "$MEMORY_MD_STALE_HOURS" ]; then
      add_alert "MEMORY.md hasn't been updated in ${age_hours}h (threshold: ${MEMORY_MD_STALE_HOURS}h). Consolidation may not be running."
    else
      add_ok "MEMORY.md is fresh (updated ${age_hours}h ago)"
    fi
  fi

  # Check size
  char_count=$(wc -c < "$MEMORY_MD" | tr -d ' ')
  if [ "$char_count" -gt "$MAX_MEMORY_MD_CHARS" ]; then
    add_alert "MEMORY.md is ${char_count} chars (target: ${MAX_MEMORY_MD_CHARS}). Consolidation needed to trim."
  else
    add_ok "MEMORY.md size: ${char_count} chars (target: ${MAX_MEMORY_MD_CHARS})"
  fi
else
  add_alert "MEMORY.md does not exist. Create it during setup or first session."
fi

# --- Check 3: Today's daily notes ---
TODAY=$(today)
DAILY_NOTES="${WORKSPACE}/memory/${TODAY}.md"
HOUR=$(current_hour)

if [ -f "$DAILY_NOTES" ]; then
  add_ok "Today's daily notes exist (memory/${TODAY}.md)"
elif [ "$HOUR" -ge "$DAILY_NOTES_REQUIRED_AFTER" ]; then
  add_alert "No daily notes for today (memory/${TODAY}.md) and it's past ${DAILY_NOTES_REQUIRED_AFTER}:00. Session capture may not be working."
else
  add_ok "No daily notes yet today (still early — before ${DAILY_NOTES_REQUIRED_AFTER}:00)"
fi

# --- Check 4: Last QMD reindex freshness ---
if [ -f "$HEARTBEAT_FILE" ] && command -v python3 &>/dev/null; then
  last_reindex="$(python3 - "$HEARTBEAT_FILE" <<'PYEOF'
import json
import sys
try:
    with open(sys.argv[1], encoding="utf-8") as f:
        state = json.load(f)
    value = state.get("lastChecks", {}).get("qmd_reindex", 0)
    print(value if isinstance(value, int) and value >= 0 else 0)
except Exception:
    print(0)
PYEOF
)"

  if [ "$last_reindex" != "0" ]; then
    now_epoch=$(epoch_now)
    reindex_age_hours=$(( (now_epoch - last_reindex) / 3600 ))
    if [ "$reindex_age_hours" -gt "$REINDEX_OVERDUE_HOURS" ]; then
      add_alert "QMD reindex is overdue (${reindex_age_hours}h ago, threshold: ${REINDEX_OVERDUE_HOURS}h). Run scripts/qmd-reindex.sh."
    else
      add_ok "QMD reindex is fresh (${reindex_age_hours}h ago)"
    fi
  else
    add_alert "No QMD reindex timestamp found. Has the reindex script ever run?"
  fi
else
  if [ ! -f "$HEARTBEAT_FILE" ]; then
    add_alert "Heartbeat state file missing (memory/heartbeat-state.json). Run setup."
  fi
fi

# --- Check 5: Heartbeat state validity ---
if [ -f "$HEARTBEAT_FILE" ]; then
  if command -v python3 &>/dev/null; then
    valid="$(python3 - "$HEARTBEAT_FILE" <<'PYEOF'
import json
import sys
try:
    with open(sys.argv[1], encoding="utf-8") as f:
        state = json.load(f)
    print("valid" if isinstance(state.get("lastChecks"), dict) else "invalid")
except Exception:
    print("invalid")
PYEOF
)"
    if [ "$valid" = "valid" ]; then
      add_ok "Heartbeat state file is valid"
    else
      add_alert "Heartbeat state file is malformed. Re-run setup."
    fi
  fi
fi

# --- Check 6: Vector DB (optional) ---
VECTOR_ENABLED=false
VECTOR_COUNT=0

if [ -f "$CONFIG_FILE" ] && command -v python3 &>/dev/null; then
  VECTOR_ENABLED="$(python3 - "$CONFIG_FILE" <<'PYEOF'
import json
import sys
try:
    with open(sys.argv[1], encoding="utf-8") as f:
        config = json.load(f)
    print("true" if config.get("vector_db", {}).get("enabled", False) else "false")
except Exception:
    print("false")
PYEOF
)"
fi

if [ "$VECTOR_ENABLED" = "true" ]; then
  # Check if Qdrant is reachable
  if curl -sf http://localhost:6333/healthz &>/dev/null; then
    add_ok "Qdrant is running"
    # Try to get collection info
    VECTOR_COUNT="$(curl -sf http://localhost:6333/collections/user_memory 2>/dev/null | python3 - <<'PYEOF'
import json
import sys
try:
    data = json.load(sys.stdin)
    points_count = data.get("result", {}).get("points_count", 0)
    print(points_count if isinstance(points_count, int) and points_count >= 0 else 0)
except Exception:
    print(0)
PYEOF
)"
    add_ok "Vector DB: $VECTOR_COUNT vectors"
  else
    add_alert "Vector DB is enabled but Qdrant is not reachable at localhost:6333."
  fi
fi

# --- Write health state file ---
if command -v python3 &>/dev/null; then
  # Write alerts to a temp file to avoid bash string escaping issues
  ALERT_TMPFILE=$(mktemp)
  for alert in "${ALERTS[@]}"; do
    echo "$alert" >> "$ALERT_TMPFILE"
  done

  VECTOR_COLL=$( [ "$VECTOR_ENABLED" = "true" ] && echo "user_memory" || echo "" )

  python3 - "$ALERT_TMPFILE" "$STATE_FILE" "$(today)" "$QMD_COLLECTION_COUNT" "$VECTOR_ENABLED" "$VECTOR_COUNT" "$VECTOR_COLL" <<'PYEOF'
import json
import sys

# Read alerts from temp file
alerts = []
try:
    with open(sys.argv[1], encoding="utf-8") as f:
        alerts = [line.strip() for line in f if line.strip()]
except Exception:
    pass

vector_enabled = sys.argv[5].lower() == "true"
try:
    qmd_collection_count = int(sys.argv[4])
except ValueError:
    qmd_collection_count = 0
try:
    vector_count = int(sys.argv[6])
except ValueError:
    vector_count = 0

state = {
    "date": sys.argv[3],
    "qmd": {
        "collection_count": qmd_collection_count,
        "collections": {}
    },
    "mem0": {
        "enabled": vector_enabled,
        "vector_count": vector_count,
        "collection": sys.argv[7]
    },
    "last_qmd_reindex": "",
    "last_consolidation": "",
    "alerts": alerts
}

with open(sys.argv[2], "w", encoding="utf-8") as f:
    json.dump(state, f, indent=2)
PYEOF

  rm -f "$ALERT_TMPFILE"
fi 2>/dev/null || log "Warning: could not write health state file"

# --- Summary ---
echo ""
echo "=== Health Check Summary ==="
echo "Date: $(today) $(timestamp)"
echo "QMD Collections: $QMD_COLLECTION_COUNT"
echo "Vector DB: $( [ "$VECTOR_ENABLED" = "true" ] && echo "enabled ($VECTOR_COUNT vectors)" || echo "not enabled")"
echo ""

if [ ${#ALERTS[@]} -gt 0 ]; then
  echo "ALERTS (${#ALERTS[@]}):"
  for alert in "${ALERTS[@]}"; do
    echo "  $alert"
  done
  echo ""
  exit 1
else
  echo "✅ All checks passed. Memory system is healthy."
  exit 0
fi
