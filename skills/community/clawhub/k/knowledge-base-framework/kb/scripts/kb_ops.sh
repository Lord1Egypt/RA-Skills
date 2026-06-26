#!/bin/bash
# KB Operations Script - Backup, Restore, and Maintenance

# ===== DRY RUN FLAG =====
DRY_RUN=false
case "$1" in
    --dry-run)
        DRY_RUN=true
        shift
        ;;
esac

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KB_DIR="${HOME}/.openclaw/kb"
BACKUP_DIR="${KB_DIR}/backup"
DB_PATH="${KB_DIR}/library/biblio.db"
CHROMA_PATH="${KB_DIR}/library/chroma_db"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log() {
    echo -e "${GREEN}[KB-OPS]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1" && exit 1
}

# ===== BACKUP =====
cmd_backup() {
    if [ "$DRY_RUN" = true ]; then
        echo "[DRY-RUN] Would create backup: kb_backup_$(date +%Y%m%d_%H%M%S)"
        echo "[DRY-RUN] Would backup: $DB_PATH and $CHROMA_PATH"
        return
    fi
    
    local timestamp=$(date +%Y%m%d_%H%M%S)
    local backup_name="kb_backup_${timestamp}"
    local backup_path="${BACKUP_DIR}/${backup_name}"
    
    log "Creating backup: ${backup_name}"
    
    mkdir -p "${backup_path}"
    
    # Backup SQLite DB
    if [ -f "${DB_PATH}" ]; then
        cp "${DB_PATH}" "${backup_path}/"
        log "Database backed up"
    else
        warn "Database not found at ${DB_PATH}"
    fi
    
    # Backup ChromaDB
    if [ -d "${CHROMA_PATH}" ]; then
        cp -r "${CHROMA_PATH}" "${backup_path}/"
        log "ChromaDB backed up"
    else
        warn "ChromaDB not found at ${CHROMA_PATH}"
    fi
    
    # Create metadata
    echo "Backup created: $(date)" > "${backup_path}/backup_info.txt"
    echo "KB Version: $(cat ${SCRIPT_DIR}/../config.py | grep '__version__' | head -1)" >> "${backup_path}/backup_info.txt" 2>/dev/null || true
    
    log "Backup complete: ${backup_path}"
    
    # Cleanup old backups (keep last 10)
    local backup_count=$(find "${BACKUP_DIR}" -maxdepth 1 -type d -name "kb_backup_*" | wc -l)
    if [ $backup_count -gt 10 ]; then
        log "Cleaning up old backups..."
        find "${BACKUP_DIR}" -maxdepth 1 -type d -name "kb_backup_*" -mtime +7 -exec rm -rf {} + 2>/dev/null || true
    fi
}

# ===== RESTORE =====
cmd_restore() {
    if [ "$DRY_RUN" = true ]; then
        echo "[DRY-RUN] Would restore from backup: $1"
        return
    fi
    
    local backup_name="$1"
    
    if [ -z "$backup_name" ]; then
        log "Available backups:"
        find "${BACKUP_DIR}" -maxdepth 1 -type d -name "kb_backup_*" -exec basename {} \; | sort -r | head -10
        read -p "Enter backup name to restore: " backup_name
    fi
    
    local backup_path="${BACKUP_DIR}/${backup_name}"
    
    if [ ! -d "$backup_path" ]; then
        error "Backup not found: $backup_path"
    fi
    
    warn "This will overwrite current database. Continue? (y/N)"
    read -r confirm
    if [[ ! $confirm =~ ^[Yy]$ ]]; then
        log "Restore cancelled"
        exit 0
    fi
    
    log "Restoring from: $backup_name"
    
    # Restore SQLite
    if [ -f "${backup_path}/biblio.db" ]; then
        mkdir -p "$(dirname ${DB_PATH})"
        cp "${backup_path}/biblio.db" "${DB_PATH}"
        log "Database restored"
    fi
    
    # Restore ChromaDB
    if [ -d "${backup_path}/chroma_db" ]; then
        rm -rf "${CHROMA_PATH}"
        cp -r "${backup_path}/chroma_db" "${CHROMA_PATH}"
        log "ChromaDB restored"
    fi
    
    log "Restore complete!"
}

# ===== MIGRATE =====
cmd_migrate() {
    if [ "$DRY_RUN" = true ]; then
        echo "[DRY-RUN] Would run database migrations"
        return
    fi
    
    log "Running database migrations..."
    python3 -m kb.scripts.migrate --execute
}

# ===== SYNC =====
cmd_sync() {
    if [ "$DRY_RUN" = true ]; then
        echo "[DRY-RUN] Would sync ChromaDB with SQLite"
        return
    fi
    
    log "Syncing ChromaDB with SQLite..."
    python3 -m kb.scripts.sync_chroma --execute
}

# ===== AUDIT =====
cmd_audit() {
    if [ "$DRY_RUN" = true ]; then
        echo "[DRY-RUN] Would run full KB audit"
        return
    fi
    
    log "Running KB audit..."
    python3 kb/scripts/kb_full_audit.py
}

# ===== HELP =====
cmd_help() {
    cat << EOF
KB Operations Tool

Usage: kb_ops.sh <command> [options]

Commands:
    backup              Create a new backup
    restore [name]      Restore from backup (interactive if no name)
    migrate             Run database migrations
    sync                Sync ChromaDB with SQLite
    audit               Run full KB audit
    help                Show this help

Examples:
    kb_ops.sh backup
    kb_ops.sh restore
    kb_ops.sh restore kb_backup_20260413_120000
    kb_ops.sh migrate
    kb_ops.sh sync

EOF
}

# ===== MAIN =====
case "${1:-help}" in
    backup)
        cmd_backup
        ;;
    restore)
        cmd_restore "$2"
        ;;
    migrate)
        cmd_migrate
        ;;
    sync)
        cmd_sync
        ;;
    audit)
        cmd_audit
        ;;
    help|--help|-h)
        cmd_help
        ;;
    *)
        error "Unknown command: $1. Use 'kb_ops.sh help' for usage."
        ;;
esac
