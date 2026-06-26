#!/usr/bin/env bash
# memory-oracle: uninstall.sh
# Safe rollback — removes cron, database, and restores MEMORY.md backup.
#
# Usage:
#   bash uninstall.sh              # Interactive uninstall
#   bash uninstall.sh --force      # Skip confirmations
#   bash uninstall.sh --keep-db    # Remove cron but keep database

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PYTHON="${PYTHON:-python3}"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

info()  { echo -e "${GREEN}[memory-oracle]${NC} $*"; }
warn()  { echo -e "${YELLOW}[memory-oracle]${NC} $*"; }
error() { echo -e "${RED}[memory-oracle]${NC} $*"; }

FORCE=false
KEEP_DB=false
while [[ $# -gt 0 ]]; do
    case "$1" in
        --force)    FORCE=true; shift ;;
        --keep-db)  KEEP_DB=true; shift ;;
        -h|--help)
            echo "Usage: bash uninstall.sh [--force] [--keep-db]"
            echo "  --force    Skip all confirmations"
            echo "  --keep-db  Remove cron and restore MEMORY.md but keep SQLite database"
            exit 0 ;;
        *) shift ;;
    esac
done

# Load settings to find paths
if [[ -f "$SCRIPT_DIR/config/settings.json" ]]; then
    DB_PATH=$("$PYTHON" -c "
import json, os
with open('$SCRIPT_DIR/config/settings.json') as f:
    s = json.load(f)
print(os.path.expanduser(s['paths']['db']))
" 2>/dev/null || echo "")
    MEMORY_PATH=$("$PYTHON" -c "
import json, os
with open('$SCRIPT_DIR/config/settings.json') as f:
    s = json.load(f)
print(os.path.expanduser(s['paths']['memory_md']))
" 2>/dev/null || echo "")
    WORKSPACE=$("$PYTHON" -c "
import json, os
with open('$SCRIPT_DIR/config/settings.json') as f:
    s = json.load(f)
print(os.path.expanduser(s['paths']['workspace']))
" 2>/dev/null || echo "")
else
    DB_PATH="$HOME/.openclaw/workspace/memory-oracle.db"
    MEMORY_PATH="$HOME/.openclaw/workspace/MEMORY.md"
    WORKSPACE="$HOME/.openclaw/workspace"
fi

info "Memory Oracle — Uninstall"
info ""

# 1. Export state before removing anything
if [[ -f "$DB_PATH" && "$KEEP_DB" == "false" ]]; then
    EXPORT_PATH="${WORKSPACE}/memory-oracle-export-$(date +%Y%m%d-%H%M%S).json"
    info "Exporting full memory state to: $EXPORT_PATH"
    "$PYTHON" "$SCRIPT_DIR/scripts/maintenance.py" --export "$EXPORT_PATH" 2>/dev/null || true
    if [[ -f "$EXPORT_PATH" ]]; then
        info "  Export saved. You can re-import later if needed."
    fi
fi

# 2. Remove cron jobs
CRON_COUNT=$(crontab -l 2>/dev/null | grep -c "memory-oracle" || true)
if [[ "$CRON_COUNT" -gt 0 ]]; then
    if [[ "$FORCE" == "true" ]]; then
        CONFIRM="y"
    else
        warn "Found $CRON_COUNT memory-oracle cron job(s)."
        read -r -p "Remove them? [Y/n] " CONFIRM
        CONFIRM="${CONFIRM:-y}"
    fi
    if [[ "$CONFIRM" =~ ^[Yy]$ ]]; then
        crontab -l 2>/dev/null | grep -v "memory-oracle" | crontab -
        info "  Cron jobs removed."
    else
        warn "  Cron jobs kept."
    fi
else
    info "  No cron jobs found."
fi

# 3. Restore MEMORY.md from backup
BACKUP_PATH="${MEMORY_PATH}.pre-oracle-backup"
if [[ -f "$BACKUP_PATH" ]]; then
    if [[ "$FORCE" == "true" ]]; then
        CONFIRM="y"
    else
        info "Found MEMORY.md backup from before installation."
        read -r -p "Restore original MEMORY.md? [Y/n] " CONFIRM
        CONFIRM="${CONFIRM:-y}"
    fi
    if [[ "$CONFIRM" =~ ^[Yy]$ ]]; then
        cp "$BACKUP_PATH" "$MEMORY_PATH"
        info "  MEMORY.md restored from backup."
    else
        warn "  MEMORY.md backup kept at: $BACKUP_PATH"
    fi
else
    warn "  No MEMORY.md backup found (was not modified during install, or backup was removed)."
fi

# 4. Remove database
if [[ "$KEEP_DB" == "false" ]]; then
    if [[ -f "$DB_PATH" ]]; then
        if [[ "$FORCE" == "true" ]]; then
            CONFIRM="y"
        else
            DB_SIZE=$(du -h "$DB_PATH" 2>/dev/null | cut -f1)
            FACT_COUNT=$("$PYTHON" -c "
import sqlite3
c = sqlite3.connect('$DB_PATH')
print(c.execute('SELECT COUNT(*) FROM facts WHERE status=\"active\"').fetchone()[0])
c.close()
" 2>/dev/null || echo "unknown")
            warn "Database: $DB_PATH ($DB_SIZE, $FACT_COUNT active facts)"
            read -r -p "Delete database? [y/N] " CONFIRM
        fi
        if [[ "$CONFIRM" =~ ^[Yy]$ ]]; then
            rm -f "$DB_PATH" "${DB_PATH}-wal" "${DB_PATH}-shm"
            info "  Database deleted."
        else
            warn "  Database kept."
        fi
    fi
else
    info "  Database kept (--keep-db)."
fi

# 5. Clean up ancillary files
for F in "${WORKSPACE}/memory-oracle-pending.json"; do
    [[ -f "$F" ]] && rm -f "$F" && info "  Removed: $F"
done

# Clean reflection files
REFLECTIONS_DIR="${WORKSPACE}/memory/reflections"
FAILED_DIR="${WORKSPACE}/memory/failed_reflections"
if [[ -d "$REFLECTIONS_DIR" || -d "$FAILED_DIR" ]]; then
    if [[ "$FORCE" == "true" ]]; then
        CONFIRM="y"
    else
        read -r -p "Remove reflection files? [y/N] " CONFIRM
    fi
    if [[ "$CONFIRM" =~ ^[Yy]$ ]]; then
        [[ -d "$REFLECTIONS_DIR" ]] && rm -rf "$REFLECTIONS_DIR" && info "  Removed reflections/"
        [[ -d "$FAILED_DIR" ]] && rm -rf "$FAILED_DIR" && info "  Removed failed_reflections/"
    fi
fi

info ""
info "=============================="
info " Uninstall complete."
info "=============================="
info ""
info "Manual steps remaining:"
info "  1. Remove the Memory Oracle Protocol section from your AGENTS.md"
info "  2. Remove the checkpoint.py reference from your compaction config"
info "  3. Optionally: rm -rf $SCRIPT_DIR  (remove skill files)"
info ""
if [[ -f "${WORKSPACE}/memory-oracle-export-"* ]] 2>/dev/null; then
    info "Your memory export is saved at: ${WORKSPACE}/memory-oracle-export-*.json"
    info "You can re-import it if you reinstall."
fi
