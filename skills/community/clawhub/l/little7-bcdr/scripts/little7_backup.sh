#!/usr/bin/env bash
set -euo pipefail
shopt -s nullglob globstar

MODE="${1:-daily}"
case "$MODE" in
  daily) KEEP=180 ;;
  weekly) KEEP=312 ;;
  *)
    echo "Usage: $0 daily|weekly" >&2
    exit 1
    ;;
esac

ROOT="${LITTLE7_WORKSPACE_ROOT:-$HOME/.openclaw/workspace}"
DRIVE_BASE="${LITTLE7_GDRIVE_BASE:-$HOME/Google Drive/Little7}"
DEFAULT_SECRET_PATHS_FILE="$ROOT/docs/LITTLE7_SECRET_PATHS.txt"
SECRET_PATHS_FILE="${LITTLE7_SECRET_PATHS_FILE:-$DEFAULT_SECRET_PATHS_FILE}"
DATE="$(date +%F)"
TMP_BASE="${TMPDIR:-/tmp}/little7-backup-${MODE}-${DATE}-$$"
STAGE_STATE="$TMP_BASE/state"
STAGE_SECRETS="$TMP_BASE/secrets"
OUT_DIR="$DRIVE_BASE/$MODE"
LATEST_DIR="$DRIVE_BASE/latest"
RESTORE_DIR="$DRIVE_BASE/restore-notes"
STATE_NAME="little7-${MODE}-${DATE}.tar.gz"
SECRETS_NAME="little7-${MODE}-secrets-${DATE}.tar.gz"
STATE_OUT="$OUT_DIR/$STATE_NAME"
SECRETS_OUT="$OUT_DIR/$SECRETS_NAME"
LATEST_STATE="$LATEST_DIR/little7-${MODE}-latest.tar.gz"
LATEST_SECRETS="$LATEST_DIR/little7-${MODE}-secrets-latest.tar.gz"
MANIFEST="$TMP_BASE/manifest.txt"

mkdir -p "$STAGE_STATE" "$STAGE_SECRETS" "$OUT_DIR" "$LATEST_DIR" "$RESTORE_DIR"

cleanup() { rm -rf "$TMP_BASE"; }
trap cleanup EXIT

copy_rel() {
  local rel="$1"
  local src="$ROOT/$rel"
  [ -e "$src" ] || return 0
  mkdir -p "$STAGE_STATE/$(dirname "$rel")"
  cp -a "$src" "$STAGE_STATE/$rel"
}

should_skip_state_path() {
  local path="$1"
  case "$path" in
    */.git/*|*/node_modules/*|*/.npm/*|*/.cache/*|*/.runtime/*)
      return 0
      ;;
    *)
      return 1
      ;;
  esac
}

copy_abs_secret() {
  local src="$1"
  [ -e "$src" ] || return 0
  local rel="${src#/}"
  mkdir -p "$STAGE_SECRETS/$(dirname "$rel")"
  cp -a "$src" "$STAGE_SECRETS/$rel"
}

STATE_FILES=(
  AGENTS.md
  SOUL.md
  USER.md
  IDENTITY.md
  MEMORY.md
  TOOLS.md
  HEARTBEAT.md
)

OPTIONAL_FILES=(
  TASK_LEDGER.md
  WORK_LEDGER.md
  BACKLOG_LEDGER.md
  AGILE_LEDGER.md
  DOUBT_LEDGER.md
  DISASTER_RECOVERY.md
)

for rel in "${STATE_FILES[@]}"; do copy_rel "$rel"; done
for rel in "${OPTIONAL_FILES[@]}"; do copy_rel "$rel"; done
for path in "$ROOT"/memory/**/*.md "$ROOT"/memory/**/*.json; do
  [ -e "$path" ] || continue
  copy_rel "${path#$ROOT/}"
done
for path in "$ROOT"/.learnings/LEARNINGS.md "$ROOT"/.learnings/ERRORS.md "$ROOT"/.learnings/FEATURE_REQUESTS.md; do
  [ -e "$path" ] || continue
  copy_rel "${path#$ROOT/}"
done
for path in $(find "$ROOT/scripts" "$ROOT/skills" -type f 2>/dev/null | sort); do
  should_skip_state_path "$path" && continue
  copy_rel "${path#$ROOT/}"
done

if [ -n "$SECRET_PATHS_FILE" ] && [ -f "$SECRET_PATHS_FILE" ]; then
  while IFS= read -r line; do
    line="${line#${line%%[![:space:]]*}}"
    line="${line%${line##*[![:space:]]}}"
    [ -n "$line" ] || continue
    case "$line" in
      \#*) continue ;;
    esac
    copy_abs_secret "$line"
  done < "$SECRET_PATHS_FILE"
fi

cat > "$STAGE_STATE/RESTORE_NOTES.txt" <<RESTORE
Little7 backup ($MODE) created on $DATE.

State archive:
- identity, memory, learnings, scripts, skills, and selected docs
- excludes caches, browser profiles, git metadata, node_modules, and raw session histories

Secrets archive:
- built from the explicit allowlist in LITTLE7_SECRET_PATHS_FILE
- defaults locally to docs/LITTLE7_SECRET_PATHS.txt when present
- keep secret recovery material separate and tightly permissioned

Restore order:
1. Restore core files into the target workspace
2. Restore secrets only onto a trusted machine and set strict permissions
3. Reconnect provider/tooling paths as needed
RESTORE

cat > "$STAGE_SECRETS/README.txt" <<'SECRETS'
Sensitive Little7 continuity material.
Restore only onto a trusted machine.
Recommended permissions after restore:
- private keys: 600
- ~/.ssh directory: 700
SECRETS

( cd "$STAGE_STATE" && find . -type f | sort ) > "$MANIFEST"
{
  echo "Mode: $MODE"
  echo "Date: $DATE"
  echo "State files:"
  sed 's#^#  #g' "$MANIFEST"
  echo "Secrets files:"
  ( cd "$STAGE_SECRETS" && find . -type f | sort | sed 's#^#  #g' )
} > "$RESTORE_DIR/little7-${MODE}-${DATE}-manifest.txt"

( cd "$STAGE_STATE" && tar czf "$STATE_OUT" . )
( cd "$STAGE_SECRETS" && tar czf "$SECRETS_OUT" . )
cp -f "$STATE_OUT" "$LATEST_STATE"
cp -f "$SECRETS_OUT" "$LATEST_SECRETS"
cp -f "$RESTORE_DIR/little7-${MODE}-${DATE}-manifest.txt" "$RESTORE_DIR/little7-${MODE}-latest-manifest.txt"

verify_contains() {
  local archive="$1"
  local needle="$2"
  tar tzf "$archive" | awk -v needle="$needle" '$0 == needle { found = 1 } END { exit found ? 0 : 1 }'
}

verify_contains "$STATE_OUT" "./AGENTS.md"
verify_contains "$STATE_OUT" "./MEMORY.md"
verify_contains "$STATE_OUT" "./scripts/little7_backup.sh"
verify_contains "$SECRETS_OUT" "./README.txt"

prune_keep() {
  local dir="$1"
  local pattern="$2"
  local keep="$3"
  mapfile -t files < <(find "$dir" -maxdepth 1 -type f -name "$pattern" | sort)
  local count="${#files[@]}"
  if (( count <= keep )); then
    return 0
  fi
  local remove_count=$((count - keep))
  for ((i=0; i<remove_count; i++)); do
    rm -f "${files[$i]}"
  done
}

prune_keep "$OUT_DIR" "little7-${MODE}-????-??-??.tar.gz" "$KEEP"
prune_keep "$OUT_DIR" "little7-${MODE}-secrets-????-??-??.tar.gz" "$KEEP"
prune_keep "$RESTORE_DIR" "little7-${MODE}-????-??-??-manifest.txt" "$KEEP"

printf 'Created:\n- %s\n- %s\n' "$STATE_OUT" "$SECRETS_OUT"
