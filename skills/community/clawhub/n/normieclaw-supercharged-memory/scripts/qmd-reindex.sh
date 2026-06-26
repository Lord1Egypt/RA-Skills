#!/usr/bin/env bash
# =============================================================================
# Supercharged Memory — QMD Reindex Script
# Auto-discovers collections, reindexes all, logs results.
# Usage: bash scripts/qmd-reindex.sh [--allow-outside-workspace] [workspace_root]
# =============================================================================

set -euo pipefail
umask 077

# --- Configuration ---
usage() {
  cat <<'EOF'
Usage: bash scripts/qmd-reindex.sh [--allow-outside-workspace] [workspace_root]

By default, workspace_root must be inside this repository.
Use --allow-outside-workspace to intentionally index a path outside the repo.
EOF
}

ALLOW_OUTSIDE_WORKSPACE=0
RAW_WORKSPACE=""

while [ "$#" -gt 0 ]; do
  case "$1" in
    --allow-outside-workspace)
      ALLOW_OUTSIDE_WORKSPACE=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      if [ -n "$RAW_WORKSPACE" ]; then
        echo "[ERROR] Unexpected argument: $1" >&2
        usage >&2
        exit 1
      fi
      RAW_WORKSPACE="$1"
      shift
      ;;
  esac
done

RAW_WORKSPACE="${RAW_WORKSPACE:-$(pwd)}"
if ! WORKSPACE="$(cd "$RAW_WORKSPACE" 2>/dev/null && pwd -P)"; then
  echo "[ERROR] Workspace directory does not exist or is not accessible: $RAW_WORKSPACE" >&2
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" 2>/dev/null && pwd -P)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." 2>/dev/null && pwd -P)"
LOG_FILE="${WORKSPACE}/memory/qmd-reindex.log"
STATE_FILE="${WORKSPACE}/memory/heartbeat-state.json"
SKIP_DIRS=("node_modules" ".git" "__pycache__" "dist" "build" ".venv" ".env" "vendor")
MAX_DEPTH=3

# --- Helpers ---
timestamp() { date "+%Y-%m-%d %H:%M:%S"; }

log() {
  local msg="[$(timestamp)] $1"
  echo "$msg"
  echo "$msg" >> "$LOG_FILE" 2>/dev/null || true
}

die() {
  log "ERROR: $1"
  exit 1
}

# --- Validate environment ---
if ! command -v qmd &>/dev/null; then
  die "qmd is not installed. Install with: brew install qmd  or  cargo install qmd"
fi

if [ ! -d "$WORKSPACE" ]; then
  die "Workspace directory does not exist: $WORKSPACE"
fi

if [ "$ALLOW_OUTSIDE_WORKSPACE" -eq 0 ]; then
  case "${WORKSPACE}/" in
    "${REPO_ROOT}/"*) ;;
    *)
      die "Workspace must be inside repo root: $REPO_ROOT (use --allow-outside-workspace to override)"
      ;;
  esac
fi

# Ensure log directory exists
mkdir -p "$(dirname "$LOG_FILE")" 2>/dev/null || true

log "=== QMD Reindex Starting ==="
log "Workspace: $WORKSPACE"

# --- Build skip arguments for find ---
FIND_PRUNE_ARGS=()
for dir in "${SKIP_DIRS[@]}"; do
  FIND_PRUNE_ARGS+=(-name "$dir" -o)
done
unset 'FIND_PRUNE_ARGS[${#FIND_PRUNE_ARGS[@]}-1]'

# --- Discover indexable directories ---
# Always index these core collections
declare -A COLLECTIONS
COLLECTIONS["workspace"]="$WORKSPACE"
if [ -d "${WORKSPACE}/memory" ]; then
  COLLECTIONS["memory"]="${WORKSPACE}/memory"
fi

# Auto-discover additional directories containing indexable files
while IFS= read -r dir; do
  # Skip if it's the workspace root or memory (already handled)
  [ "$dir" = "$WORKSPACE" ] && continue
  [ "$dir" = "${WORKSPACE}/memory" ] && continue

  # Derive collection name from relative path
  rel_path="${dir#$WORKSPACE/}"
  # Replace slashes with hyphens for collection name
  coll_name="${rel_path//\//-}"
  # Sanitize: lowercase, remove special chars
  coll_name=$(echo "$coll_name" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9-]/-/g' | sed 's/--*/-/g' | sed 's/^-//' | sed 's/-$//')

  if [ -n "$coll_name" ]; then
    COLLECTIONS["$coll_name"]="$dir"
  fi
done < <(
  find "$WORKSPACE" -maxdepth "$MAX_DEPTH" -type d \
    \( "${FIND_PRUNE_ARGS[@]}" \) -prune -o -type d -print 2>/dev/null |
  while IFS= read -r candidate; do
    # Check if directory has indexable files
    file_count=$(find "$candidate" -maxdepth 1 \( -name "*.md" -o -name "*.json" -o -name "*.ts" -o -name "*.js" -o -name "*.py" -o -name "*.sh" \) -type f 2>/dev/null | head -20 | wc -l | tr -d ' ')
    if [ "$file_count" -gt 0 ]; then
      echo "$candidate"
    fi
  done
)

log "Discovered ${#COLLECTIONS[@]} collections"

# --- Reindex each collection ---
SUCCESS_COUNT=0
ERROR_COUNT=0
TOTAL_DOCS=0

for coll_name in "${!COLLECTIONS[@]}"; do
  coll_path="${COLLECTIONS[$coll_name]}"
  log "Indexing: $coll_name ($coll_path)"

  # Detect primary file type for pattern
  md_count=$(find "$coll_path" -maxdepth 2 -name "*.md" -type f 2>/dev/null | wc -l | tr -d ' ')
  ts_count=$(find "$coll_path" -maxdepth 2 \( -name "*.ts" -o -name "*.js" \) -type f 2>/dev/null | wc -l | tr -d ' ')
  py_count=$(find "$coll_path" -maxdepth 2 -name "*.py" -type f 2>/dev/null | wc -l | tr -d ' ')

  # Use broad pattern — qmd handles file filtering
  pattern="**/*.md"
  if [ "$ts_count" -gt "$md_count" ]; then
    pattern="**/*.{ts,js,md}"
  elif [ "$py_count" -gt "$md_count" ]; then
    pattern="**/*.{py,md}"
  fi

  # Create collection if it doesn't exist (ignore errors if already exists)
  qmd collection create "$coll_name" --pattern "$pattern" --path "$coll_path" 2>/dev/null || true

  # Reindex
  if output=$(qmd collection reindex "$coll_name" 2>&1); then
    # Try to extract doc count from output
    doc_count=$(echo "$output" | grep -oE '[0-9]+ (documents|docs|files)' | grep -oE '[0-9]+' | head -1 || echo "?")
    log "  ✅ $coll_name — $doc_count documents"
    SUCCESS_COUNT=$((SUCCESS_COUNT + 1))
    if [[ "$doc_count" =~ ^[0-9]+$ ]]; then
      TOTAL_DOCS=$((TOTAL_DOCS + doc_count))
    fi
  else
    log "  ❌ $coll_name — reindex failed: $output"
    ERROR_COUNT=$((ERROR_COUNT + 1))
  fi
done

# --- Update heartbeat state ---
if [ -f "$STATE_FILE" ]; then
  NOW_EPOCH=$(date +%s)
  # Use python for reliable JSON update (available on macOS and most Linux)
  if command -v python3 &>/dev/null; then
    python3 - "$STATE_FILE" "$NOW_EPOCH" <<'PYEOF'
import json
import sys

try:
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        state = json.load(f)
    state.setdefault("lastChecks", {})["qmd_reindex"] = int(sys.argv[2])
    with open(sys.argv[1], "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)
except Exception as e:
    print(f"Warning: could not update heartbeat state: {e}", file=sys.stderr)
PYEOF
  fi
fi

# --- Summary ---
log "=== QMD Reindex Complete ==="
log "Collections: ${#COLLECTIONS[@]} | Success: $SUCCESS_COUNT | Errors: $ERROR_COUNT | Total docs: $TOTAL_DOCS"

if [ "$ERROR_COUNT" -gt 0 ]; then
  log "⚠️ $ERROR_COUNT collection(s) failed to reindex. Check errors above."
  exit 1
fi

exit 0
