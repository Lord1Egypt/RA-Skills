#!/usr/bin/env bash
# =============================================================================
# hermes-restore.sh — Restore Hermes Agent data from a backup archive
#
# Restores: config, secrets, skills, sessions, memories, cron, kanban, etc.
#           into $HERMES_HOME (defaults to ~/.hermes).
#
# Usage:
#   ./hermes-restore.sh <backup.tar.gz>              # restore everything
#   ./hermes-restore.sh <backup.tar.gz> --dry-run    # preview what would happen
#   ./hermes-restore.sh <backup.tar.gz> --merge      # don't overwrite existing
#   ./hermes-restore.sh <backup.tar.gz> --force      # auto-stop running gateway
#   ./hermes-restore.sh <backup.tar.gz> --profile NAME # restore into a profile
#   ./hermes-restore.sh <backup.tar.gz> -t /target   # custom target dir
# =============================================================================

set -euo pipefail

# ── Resolve HERMES_HOME ──────────────────────────────────────────────────────
HERMES_HOME="${HERMES_HOME:-$HOME/.hermes}"

# ── Defaults ──────────────────────────────────────────────────────────────────
DRY_RUN=false
MERGE=false
FORCE=false
PROFILE=""
TARGET=""

# ── Parse args ────────────────────────────────────────────────────────────────
BACKUP_FILE=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run)  DRY_RUN=true; shift ;;
    --merge)    MERGE=true; shift ;;
    --force)    FORCE=true; shift ;;
    --profile)  PROFILE="$2"; shift 2 ;;
    -t|--target) TARGET="$2"; shift 2 ;;
    -h|--help)
      sed -n '2,/^# =\+/p' "$0" | sed 's/^# \?//'
      exit 0 ;;
    -*) echo "Unknown option: $1" >&2; exit 1 ;;
    *)
      if [[ -z "$BACKUP_FILE" ]]; then
        BACKUP_FILE="$1"
      else
        echo "Unexpected argument: $1" >&2
        exit 1
      fi
      shift ;;
  esac
done

if [[ -z "$BACKUP_FILE" ]]; then
  echo "Usage: $0 <backup.tar.gz> [--dry-run] [--merge] [--force] [--profile NAME] [-t /target]"
  exit 1
fi

# Resolve backup file path
if [[ ! "$BACKUP_FILE" = /* ]]; then
  BACKUP_FILE="$(pwd)/$BACKUP_FILE"
fi

if [[ ! -f "$BACKUP_FILE" ]]; then
  echo "ERROR: Backup file not found: $BACKUP_FILE" >&2
  exit 1
fi

# Override target if specified
if [[ -n "$TARGET" ]]; then
  HERMES_HOME="$TARGET"
fi

# If restoring into a profile, set the target accordingly
if [[ -n "$PROFILE" ]]; then
  HERMES_HOME="$HERMES_HOME/profiles/$PROFILE"
fi

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║          Hermes Agent Restore                                 ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo "  Backup:   $BACKUP_FILE"
echo "  Target:   $HERMES_HOME"
echo "  Mode:     $([[ "$MERGE" == "true" ]] && echo "merge (keep existing)" || echo "overwrite")"
echo "  Profile:  ${PROFILE:-<none>}"
echo "  Dry run:  $DRY_RUN"
echo ""

# ── Verify archive integrity first ───────────────────────────────────────────
echo "► Verifying archive integrity..."
if ! tar -tzf "$BACKUP_FILE" &>/dev/null; then
  echo "ERROR: Archive is corrupt or not a valid gzip tar: $BACKUP_FILE" >&2
  exit 1
fi
echo "  ✓ Archive OK"

# ── Check for manifest ─────────────────────────────────────────────────────────
MANIFEST_INFO=$(tar -xzf "$BACKUP_FILE" --wildcards -O "*/BACKUP_MANIFEST.json" 2>/dev/null || true)
if [[ -n "$MANIFEST_INFO" ]]; then
  echo ""
  echo "► Backup manifest:"
  # Extract key fields
  echo "$MANIFEST_INFO" | python3 -c "
import sys, json
try:
    m = json.load(sys.stdin)
    print(f\"  Created:   {m.get('created_at', 'unknown')}\")
    print(f\"  Hostname:  {m.get('hostname', 'unknown')}\")
    print(f\"  User:      {m.get('username', 'unknown')}\")
    print(f\"  Version:   {m.get('hermes_version', 'unknown')}\")
    print(f\"  Full mode: {m.get('full_mode', 'unknown')}\")
    contents = m.get('contents', [])
    print(f\"  Files:     {len(contents)}\")
    total_size = sum(c.get('size', 0) for c in contents)
    print(f\"  Total:     {total_size:,} bytes\")
except Exception as e:
    print(f'  (could not parse manifest: {e})')
" 2>/dev/null || echo "  (manifest present but could not parse)"
else
  echo "  ⚠ No manifest found (legacy or external archive)"
fi

# ── Dry run: list contents ────────────────────────────────────────────────────
if [[ "$DRY_RUN" == "true" ]]; then
  echo ""
  echo "► Dry run — files that would be restored:"
  echo "============================================="
  tar -tzf "$BACKUP_FILE" | grep -v '/$' | head -100 | sed 's|^[^/]*/|  |'
  FILE_COUNT=$(tar -tzf "$BACKUP_FILE" | grep -cv '/$')
  if [[ "$FILE_COUNT" -gt 100 ]]; then
    echo "  ... and $((FILE_COUNT - 100)) more files"
  fi
  echo "============================================="
  echo "Total files: $FILE_COUNT"
  echo ""
  echo "Target directory: $HERMES_HOME"
  echo "(No changes made in dry-run mode)"
  exit 0
fi

# ── Safety: check if Hermes is running ────────────────────────────────────────
GATEWAY_PIDS=""
if pgrep -f "hermes.*gateway\|hermes_cli\.main\|hermes-agent/venv" &>/dev/null 2>&1; then
  GATEWAY_PIDS=$(pgrep -f "hermes.*gateway\|hermes_cli\.main\|hermes-agent/venv" 2>/dev/null | tr '\n' ' ')
  if [[ -n "$GATEWAY_PIDS" ]]; then
    echo "⚠ WARNING: Hermes gateway is running (PIDs: $GATEWAY_PIDS)"
    echo "  Restoring SQLite databases while the gateway is live will CORRUPT them."
    echo "  The gateway holds file handles and will overwrite restored databases."
    echo ""
    if [[ "$FORCE" == "true" ]]; then
      echo "  --force given, stopping gateway automatically..."
      for pid in $GATEWAY_PIDS; do
        kill "$pid" 2>/dev/null || true
      done
      sleep 2
      for pid in $GATEWAY_PIDS; do
        kill -9 "$pid" 2>/dev/null || true
      done
      sleep 1
      echo "  ✓ Gateway stopped."
    else
      echo "  Options:"
      echo "    1. Stop Hermes manually:  hermes gateway stop"
      echo "    2. Use --force to auto-stop and continue"
      echo "    3. Cancel and stop later"
      echo ""
      read -r -p "  Stop gateway now and continue restore? [y/N] " response
      if [[ "$response" =~ ^[yY] ]]; then
        for pid in $GATEWAY_PIDS; do
          kill "$pid" 2>/dev/null || true
        done
        sleep 2
        for pid in $GATEWAY_PIDS; do
          kill -9 "$pid" 2>/dev/null || true
        done
        sleep 1
        echo "  ✓ Gateway stopped."
      else
        echo "Aborted. Stop Hermes before restoring to avoid database corruption."
        exit 1
      fi
    fi
  fi
fi

# ── Create target directory ───────────────────────────────────────────────────
mkdir -p "$HERMES_HOME"
mkdir -p "$HERMES_HOME/profiles" 2>/dev/null || true

# ── Backup existing config if present ─────────────────────────────────────────
if [[ -f "$HERMES_HOME/config.yaml" ]] && [[ "$MERGE" == "false" ]]; then
  BACKUP_TS=$(date +%Y%m%d_%H%M%S)
  EXISTING_BACKUP="$HERMES_HOME/config.yaml.pre-restore.$BACKUP_TS"
  cp -a "$HERMES_HOME/config.yaml" "$EXISTING_BACKUP"
  echo "► Backed up existing config.yaml → $EXISTING_BACKUP"
fi

if [[ -f "$HERMES_HOME/.env" ]] && [[ "$MERGE" == "false" ]]; then
  BACKUP_TS="${BACKUP_TS:-$(date +%Y%m%d_%H%M%S)}"
  EXISTING_ENV_BACKUP="$HERMES_HOME/.env.pre-restore.$BACKUP_TS"
  cp -a "$HERMES_HOME/.env" "$EXISTING_ENV_BACKUP"
  echo "► Backed up existing .env → $EXISTING_ENV_BACKUP"
fi

# ── Extract archive to staging ────────────────────────────────────────────────
echo ""
echo "► Extracting archive to staging area..."

STAGING=$(mktemp -d "${TMPDIR:-/tmp}/hermes-restore.XXXXXX")
trap 'rm -rf "$STAGING"' EXIT

tar -xzf "$BACKUP_FILE" -C "$STAGING"

# Find the top-level directory in the archive (should be hermes-backup/)
STAGE_ROOT=$(find "$STAGING" -maxdepth 1 -type d | tail -1)
if [[ -z "$STAGE_ROOT" ]] || [[ "$STAGE_ROOT" == "$STAGING" ]]; then
  echo "ERROR: Could not find expected directory structure in archive" >&2
  echo "Archive contents:" >&2
  tar -tzf "$BACKUP_FILE" | head -20 >&2
  exit 1
fi

echo "  Staging root: $STAGE_ROOT"

# ── Check if the archive is a profile-specific backup ─────────────────────────
ARCHIVE_HAS_PROFILES=false
if [[ -d "$STAGE_ROOT/profiles" ]]; then
  ARCHIVE_HAS_PROFILES=true
fi

# ── Determine source for restore ──────────────────────────────────────────────
if [[ -n "$PROFILE" ]] && [[ "$ARCHIVE_HAS_PROFILES" == "true" ]]; then
  # Restore a specific profile from a full backup
  PROFILE_SRC="$STAGE_ROOT/profiles/$PROFILE"
  if [[ ! -d "$PROFILE_SRC" ]]; then
    echo "ERROR: Profile '$PROFILE' not found in backup archive" >&2
    echo "Available profiles:" >&2
    ls -1 "$STAGE_ROOT/profiles/" 2>/dev/null >&2 || echo "  (none)" >&2
    exit 1
  fi
  RESTORE_SRC="$PROFILE_SRC"
  
  # Ensure target profile dir exists
  mkdir -p "$HERMES_HOME"
  
  echo "► Restoring profile '$PROFILE' to: $HERMES_HOME"
  
  if [[ "$MERGE" == "true" ]]; then
    rsync -a --info=name0 --ignore-existing "$RESTORE_SRC/" "$HERMES_HOME/"
  else
    rsync -a --info=name0 "$RESTORE_SRC/" "$HERMES_HOME/"
  fi
  
else
  # Normal full restore
  # If the archive has a profiles/ subdir and we're not restoring to a profile,
  # restore the main items + profiles
  
  # Determine if archive is a profile-only backup (contents are directly the profile files)
  # vs a full backup (contents include profiles/ subdir)
  if [[ "$ARCHIVE_HAS_PROFILES" == "false" ]] && [[ -n "$PROFILE" ]]; then
    # This is likely a profile-specific backup; restore its contents to the profile dir
    RESTORE_SRC="$STAGE_ROOT"
    echo "► Restoring profile-specific backup to: $HERMES_HOME"
    
    if [[ "$MERGE" == "true" ]]; then
      rsync -a --info=name0 --ignore-existing "$RESTORE_SRC/" "$HERMES_HOME/" \
        --exclude "BACKUP_MANIFEST.json"
    else
      rsync -a --info=name0 "$RESTORE_SRC/" "$HERMES_HOME/" \
        --exclude "BACKUP_MANIFEST.json"
    fi
  else
    # Full home restore
    echo "► Restoring to: $HERMES_HOME"
    
    # Copy everything except the manifest
    if [[ "$MERGE" == "true" ]]; then
      rsync -a --info=name0 --ignore-existing "$STAGE_ROOT/" "$HERMES_HOME/" \
        --exclude "BACKUP_MANIFEST.json"
    else
      rsync -a --info=name0 "$STAGE_ROOT/" "$HERMES_HOME/" \
        --exclude "BACKUP_MANIFEST.json"
    fi
  fi
fi

# ── Clean stale WAL/SHM files that don't belong to the restored DBs ──────────
echo "► Cleaning stale SQLite WAL/SHM files..."
# Backup's state.db was created via sqlite3 .backup (no WAL). Any pre-existing
# -wal/-shm from the live gateway will mismatch and cause corruption.
for db_name in state.db kanban.db cron/executions.db; do
  db_path="$HERMES_HOME/$db_name"
  if [[ -f "$db_path" ]]; then
    # Only remove WAL/SHM if the backup didn't include them (sqlite3 .backup produces none)
    if [[ ! -f "$STAGE_ROOT/$db_name-wal" ]] && [[ ! -f "$STAGE_ROOT/$db_name-shm" ]]; then
      rm -f "$db_path-wal" "$db_path-shm" 2>/dev/null || true
    fi
  fi
done
# Also clean lock files that gate SQLite access
rm -f "$HERMES_HOME/state.db.repair.lock" "$HERMES_HOME/state.db.fts_rebuild.lock" 2>/dev/null || true
echo "  ✓ Stale WAL/SHM and repair locks cleaned"

# ── Verify SQLite integrity ──────────────────────────────────────────────────
echo "► Verifying SQLite database integrity..."
if command -v sqlite3 &>/dev/null; then
  DB_OK=true
  for db_name in state.db kanban.db cron/executions.db; do
    db_path="$HERMES_HOME/$db_name"
    if [[ -f "$db_path" ]]; then
      result=$(sqlite3 "$db_path" "PRAGMA integrity_check;" 2>&1)
      if [[ "$result" == "ok" ]]; then
        msg_count=$(sqlite3 "$db_path" "SELECT COUNT(*) FROM messages;" 2>/dev/null || echo "?")
        echo "    ✓ $db_name (integrity OK, ${msg_count} rows in messages)"
      else
        echo "    ✗ $db_name CORRUPT: $result"
        DB_OK=false
      fi
    fi
  done
  if [[ "$DB_OK" == "false" ]]; then
    echo ""
    echo "⚠ WARNING: Some databases failed integrity check!"
    echo "  Do NOT start Hermes until this is resolved."
    echo "  The backup archive may contain a valid copy — try restoring again."
    exit 1
  fi
else
  echo "  ⚠ sqlite3 not installed — cannot verify integrity. Install sqlite3!"
fi

# ── Fix permissions ───────────────────────────────────────────────────────────
echo "► Setting permissions..."

# Config and secrets should be private
[[ -f "$HERMES_HOME/config.yaml" ]] && chmod 600 "$HERMES_HOME/config.yaml" 2>/dev/null || true
[[ -f "$HERMES_HOME/.env" ]] && chmod 600 "$HERMES_HOME/.env" 2>/dev/null || true
[[ -f "$HERMES_HOME/auth.json" ]] && chmod 600 "$HERMES_HOME/auth.json" 2>/dev/null || true

# Skills should be readable
[[ -d "$HERMES_HOME/skills" ]] && chmod -R u+rwX,go+rX "$HERMES_HOME/skills" 2>/dev/null || true

# ── Summary ───────────────────────────────────────────────────────────────────
echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║  Restore Complete!                                            ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo "  Target:    $HERMES_HOME"
echo ""

# ── Verify key items ──────────────────────────────────────────────────────────
echo "  Restored items:"
for item in config.yaml .env auth.json SOUL.md skills memories sessions cron kanban.db state.db; do
  full_path="$HERMES_HOME/$item"
  if [[ -e "$full_path" ]]; then
    if [[ -d "$full_path" ]]; then
      count=$(find "$full_path" -type f | wc -l)
      echo "    ✓ $item/ ($count files)"
    else
      size=$(du -h "$full_path" | cut -f1)
      echo "    ✓ $item ($size)"
    fi
  fi
done

# Also check profiles
if [[ -d "$HERMES_HOME/profiles" ]]; then
  for prof in "$HERMES_HOME/profiles"/*/; do
    [[ -d "$prof" ]] || continue
    pcount=$(find "$prof" -type f | wc -l)
    echo "    ✓ profiles/$(basename "$prof")/ ($pcount files)"
  done
fi

echo ""
echo "Next steps:"
echo "  1. Verify config:  cat $HERMES_HOME/config.yaml | head -20"
echo "  2. Check secrets:  ls -la $HERMES_HOME/.env"
echo "  3. Run health check: hermes doctor"
echo "  4. Start Hermes:  hermes"
echo ""
echo "⚠ Note: If API keys or OAuth tokens in .env/auth.json are"
echo "  machine-specific, you may need to re-authenticate with:"
echo "    hermes setup   or   hermes model"
echo ""
if [[ "$MERGE" == "false" ]]; then
  echo "⚠ Existing config.yaml and .env were backed up with .pre-restore.* suffix"
fi
