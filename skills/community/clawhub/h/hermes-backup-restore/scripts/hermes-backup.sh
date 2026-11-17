#!/usr/bin/env bash
# =============================================================================
# hermes-backup.sh — Pack Hermes Agent data into a portable archive
#
# Backs up: config, secrets, skills, sessions (state.db), memories, cron,
#           kanban, soul, hooks, skins, plugins, widgets, pets, profiles.
# Excludes: source code, caches, locks, sockets, logs, runtime ephemera.
#
# Usage:
#   ./hermes-backup.sh                    # default output to ./hermes-backup-<date>.tar.gz
#   ./hermes-backup.sh -o /path/to/backup.tar.gz
#   ./hermes-backup.sh --full             # include hermes-agent source code too
#   ./hermes-backup.sh --profile NAME     # back up only a specific profile
#   ./hermes-backup.sh --dry-run          # list what would be backed up
# =============================================================================

set -euo pipefail

# ── Resolve HERMES_HOME ──────────────────────────────────────────────────────
HERMES_HOME="${HERMES_HOME:-$HOME/.hermes}"

if [[ ! -d "$HERMES_HOME" ]]; then
  echo "ERROR: Hermes home directory not found: $HERMES_HOME" >&2
  exit 1
fi

# ── Defaults ──────────────────────────────────────────────────────────────────
OUTPUT=""
FULL=false
DRY_RUN=false
PROFILE=""

# ── Parse args ────────────────────────────────────────────────────────────────
while [[ $# -gt 0 ]]; do
  case "$1" in
    -o|--output) OUTPUT="$2"; shift 2 ;;
    --full)      FULL=true; shift ;;
    --dry-run)   DRY_RUN=true; shift ;;
    --profile)   PROFILE="$2"; shift 2 ;;
    -h|--help)
      sed -n '2,/^# =\+/p' "$0" | sed 's/^# \?//'
      exit 0 ;;
    *) echo "Unknown option: $1" >&2; exit 1 ;;
  esac
done

# ── Generate default output filename ─────────────────────────────────────────
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
HOSTNAME_F=$(hostname -s 2>/dev/null || echo "host")
if [[ -z "$OUTPUT" ]]; then
  if [[ -n "$PROFILE" ]]; then
    OUTPUT="$HOME/hermes-backup-${PROFILE}-${TIMESTAMP}.tar.gz"
  else
    OUTPUT="$HOME/hermes-backup-${HOSTNAME_F}-${TIMESTAMP}.tar.gz"
  fi
fi

# Resolve absolute path
OUTPUT="$(cd "$(dirname "$OUTPUT")" && pwd)/$(basename "$OUTPUT")"

# ── Create staging directory ─────────────────────────────────────────────────
STAGING=$(mktemp -d "${TMPDIR:-/tmp}/hermes-backup.XXXXXX")
trap 'rm -rf "$STAGING"' EXIT

STAGE_DIR="$STAGING/hermes-backup"
mkdir -p "$STAGE_DIR"

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║          Hermes Agent Backup                                  ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo "  Source:    $HERMES_HOME"
echo "  Output:    $OUTPUT"
echo "  Full mode: $FULL"
echo "  Profile:   ${PROFILE:-<default (whole home)>}"
echo ""

# ── If backing up a specific profile, redirect source ────────────────────────
if [[ -n "$PROFILE" ]]; then
  PROFILE_DIR="$HERMES_HOME/profiles/$PROFILE"
  if [[ ! -d "$PROFILE_DIR" ]]; then
    echo "ERROR: Profile '$PROFILE' not found at $PROFILE_DIR" >&2
    exit 1
  fi
  # For profile backup, we only archive that profile's directory
  BACKUP_SRC="$PROFILE_DIR"
  BACKUP_BASENAME="profiles/$PROFILE"
else
  BACKUP_SRC="$HERMES_HOME"
  BACKUP_BASENAME=""
fi

# ── Files and directories to INCLUDE (relative to HERMES_HOME) ────────────────
INCLUDE_ITEMS=(
  "config.yaml"
  ".env"
  "auth.json"
  "SOUL.md"
  "skills"
  "memories"
  "sessions"
  "cron"
  "kanban.db"
  "hooks"
  "channel_directory.json"
  "platforms"
  "skins"
  "desktop-plugins"
  "tui-widgets"
  "pets"
  "bin"
)

# If full mode, also include the source code
if [[ "$FULL" == "true" ]]; then
  INCLUDE_ITEMS+=("hermes-agent")
fi

# ── Patterns to EXCLUDE (runtime/cache/ephemera) ──────────────────────────────
EXCLUDE_PATTERNS=(
  "*.lock"
  "*.sock"
  "*.pid"
  "*-wal"
  "*-shm"
  "gateway.sock"
  "gateway.pid"
  "gateway.lock"
  "auth.lock"
  "audio_cache"
  "image_cache"
  "cache"
  "logs"
  "models_dev_cache.json"
  "models_dev_cache.etag"
  "provider_models_cache.json"
  "ollama_cloud_models_cache.json"
  "config.yaml.bak.*"
  ".skills_prompt_snapshot.json"
  ".update_check"
  ".hermes_history"
  "gateway_state.json"
  "gateway-starts.log"
  "terminal-sessions"
  "pending_messages"
  "pairing"
  "state.db.fts_rebuild.lock"
  "state.db.repair.lock"
  "*.dispatch.lock"
  "*.init.lock"
)

# ── Staging: copy selected items into staging dir ─────────────────────────────
echo "► Staging data..."

if [[ -n "$PROFILE" ]]; then
  # Profile mode: stage the entire profile dir with excludes
  STAGE_PROFILE="$STAGE_DIR/profiles/$PROFILE"
  mkdir -p "$(dirname "$STAGE_PROFILE")"
  
  RSYNC_ARGS=(-a --info=name0)
  for pat in "${EXCLUDE_PATTERNS[@]}"; do
    RSYNC_ARGS+=(--exclude "$pat")
  done
  rsync "${RSYNC_ARGS[@]}" "$PROFILE_DIR/" "$STAGE_PROFILE/"
  
  # Handle SQLite DBs inside profile
  for db in "$STAGE_PROFILE"/*.db; do
    [[ -f "$db" ]] || continue
    db_name=$(basename "$db")
    orig_db="$PROFILE_DIR/$db_name"
    # Re-export consistent snapshot
    if command -v sqlite3 &>/dev/null; then
      sqlite3 "$orig_db" ".backup '$db'" 2>/dev/null || true
    fi
  done
else
  # Full home backup: copy each include item individually
  for item in "${INCLUDE_ITEMS[@]}"; do
    src="$HERMES_HOME/$item"
    if [[ -e "$src" ]]; then
      dest="$STAGE_DIR/$item"
      mkdir -p "$(dirname "$dest")"
      
      if [[ -d "$src" ]]; then
        RSYNC_ARGS=(-a --info=name0)
        for pat in "${EXCLUDE_PATTERNS[@]}"; do
          RSYNC_ARGS+=(--exclude "$pat")
        done
        rsync "${RSYNC_ARGS[@]}" "$src/" "$dest/"
      else
        rsync -a --info=name0 "$src" "$dest"
      fi
      echo "  ✓ $item"
    else
      echo "  - $item (not present, skipped)"
    fi
  done
fi

# ── Handle SQLite databases: create consistent snapshots ─────────────────────
echo "► Processing SQLite databases..."

SQLITE_DBS=("state.db" "kanban.db" "cron/executions.db")
for db_name in "${SQLITE_DBS[@]}"; do
  if [[ -n "$PROFILE" ]]; then
    db_path="$PROFILE_DIR/$db_name"
    stage_db="$STAGE_PROFILE/$db_name"
  else
    db_path="$HERMES_HOME/$db_name"
    stage_db="$STAGE_DIR/$db_name"
  fi
  
  if [[ ! -f "$db_path" ]]; then
    continue
  fi
  
  # Ensure parent dir exists for nested paths like cron/executions.db
  mkdir -p "$(dirname "$stage_db")"
  
  # Remove the copied version (might be inconsistent due to WAL)
  rm -f "$stage_db" "$stage_db-wal" "$stage_db-shm" 2>/dev/null || true
  
  if command -v sqlite3 &>/dev/null; then
    # Use sqlite3 .backup for a transactionally-consistent snapshot
    if sqlite3 "$db_path" ".backup '$stage_db'" 2>/dev/null; then
      echo "  ✓ $db_name (consistent snapshot via sqlite3)"
    else
      # Fallback: copy db + wal + shm
      cp -a "$db_path" "$stage_db"
      [[ -f "$db_path-wal" ]] && cp -a "$db_path-wal" "$stage_db-wal"
      [[ -f "$db_path-shm" ]] && cp -a "$db_path-shm" "$stage_db-shm"
      echo "  ⚠ $db_name (sqlite3 backup failed, raw copy with WAL)"
    fi
  else
    # No sqlite3 available, copy db + wal + shm
    cp -a "$db_path" "$stage_db"
    [[ -f "$db_path-wal" ]] && cp -a "$db_path-wal" "$stage_db-wal"
    [[ -f "$db_path-shm" ]] && cp -a "$db_path-shm" "$stage_db-shm"
    echo "  ⚠ $db_name (raw copy — sqlite3 not installed)"
  fi
done

# ── Also back up any profile-specific SQLite DBs ──────────────────────────────
if [[ -z "$PROFILE" ]] && [[ -d "$HERMES_HOME/profiles" ]]; then
  echo "► Including profiles directory..."
  mkdir -p "$STAGE_DIR/profiles"
  for prof_dir in "$HERMES_HOME/profiles"/*/; do
    [[ -d "$prof_dir" ]] || continue
    prof_name=$(basename "$prof_dir")
    dest_prof="$STAGE_DIR/profiles/$prof_name"
    mkdir -p "$dest_prof"
    
    RSYNC_ARGS=(-a --info=name0)
    for pat in "${EXCLUDE_PATTERNS[@]}"; do
      RSYNC_ARGS+=(--exclude "$pat")
    done
    rsync "${RSYNC_ARGS[@]}" "$prof_dir/" "$dest_prof/"
    
    # Handle profile-level SQLite DBs
    for db in "$prof_dir"*.db; do
      [[ -f "$db" ]] || continue
      db_name=$(basename "$db")
      stage_db="$dest_prof/$db_name"
      rm -f "$stage_db" "$stage_db-wal" "$stage_db-shm" 2>/dev/null || true
      if command -v sqlite3 &>/dev/null; then
        if sqlite3 "$db" ".backup '$stage_db'" 2>/dev/null; then
          echo "  ✓ profiles/$prof_name/$db_name"
        else
          cp -a "$db" "$stage_db"
          [[ -f "${db}-wal" ]] && cp -a "${db}-wal" "$stage_db-wal"
          [[ -f "${db}-shm" ]] && cp -a "${db}-shm" "$stage_db-shm"
        fi
      else
        cp -a "$db" "$stage_db"
        [[ -f "${db}-wal" ]] && cp -a "${db}-wal" "$stage_db-wal"
        [[ -f "${db}-shm" ]] && cp -a "${db}-shm" "$stage_db-shm"
      fi
    done
  done
fi

# ── Generate manifest ─────────────────────────────────────────────────────────
echo "► Generating manifest..."

MANIFEST="$STAGE_DIR/BACKUP_MANIFEST.json"
{
  echo "{"
  echo "  \"backup_type\": \"hermes-agent\","
  echo "  \"backup_version\": 1,"
  echo "  \"created_at\": \"$(date -Iseconds 2>/dev/null || date)\","
  echo "  \"hostname\": \"$(hostname 2>/dev/null || echo unknown)\","
  echo "  \"username\": \"$(whoami 2>/dev/null || echo unknown)\","
  echo "  \"hermes_home\": \"$HERMES_HOME\","
  echo "  \"full_mode\": $FULL,"
  echo "  \"profile\": \"${PROFILE:-null}\","
  if command -v hermes &>/dev/null; then
    echo "  \"hermes_version\": \"$(hermes --version 2>/dev/null | head -1 || echo unknown)\","
  fi
  echo "  \"sqlite3_available\": $(command -v sqlite3 &>/dev/null && echo true || echo false),"
  echo "  \"contents\": ["
  first=true
  while IFS= read -r f; do
    rel="${f#$STAGE_DIR/}"
    [[ "$first" == "true" ]] && first=false || echo ","
    printf '    {"path": "%s", "size": %s}' "$rel" "$(stat -c%s "$f" 2>/dev/null || echo 0)"
  done < <(find "$STAGE_DIR" -type f -not -path "$STAGE_DIR/BACKUP_MANIFEST.json" | sort) | tr -d '\n'
  echo ""
  echo "  ]"
  echo "}"
} > "$MANIFEST"

# ── Dry run ───────────────────────────────────────────────────────────────────
if [[ "$DRY_RUN" == "true" ]]; then
  echo ""
  echo "► Dry run — contents that would be archived:"
  echo "============================================="
  find "$STAGE_DIR" -type f | sed "s|$STAGE_DIR/||" | sort
  echo "============================================="
  total=$(du -sh "$STAGE_DIR" | cut -f1)
  echo "Total staged size: $total"
  echo "(No archive created in dry-run mode)"
  exit 0
fi

# ── Create tar.gz archive ─────────────────────────────────────────────────────
echo "► Creating archive: $OUTPUT"

TAR_DIR="$(dirname "$STAGE_DIR")"
TAR_BASENAME="$(basename "$STAGE_DIR")"

tar -czf "$OUTPUT" -C "$TAR_DIR" "$TAR_BASENAME"

# ── Verify archive ────────────────────────────────────────────────────────────
echo "► Verifying archive integrity..."
if tar -tzf "$OUTPUT" &>/dev/null; then
  echo "  ✓ Archive verified OK"
else
  echo "  ✗ Archive verification FAILED!" >&2
  exit 1
fi

# ── Summary ───────────────────────────────────────────────────────────────────
ARCHIVE_SIZE=$(du -sh "$OUTPUT" | cut -f1)
FILE_COUNT=$(tar -tzf "$OUTPUT" | grep -c -v '/$')

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║  Backup Complete!                                             ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo "  Archive:    $OUTPUT"
echo "  Size:      $ARCHIVE_SIZE"
echo "  Files:     $FILE_COUNT"
echo "  Manifest:  included (BACKUP_MANIFEST.json)"
echo ""
echo "To restore on another machine:"
echo "  ./hermes-restore.sh $OUTPUT"
echo ""
echo "To inspect contents:"
echo "  tar -tzf $OUTPUT | head -30"
