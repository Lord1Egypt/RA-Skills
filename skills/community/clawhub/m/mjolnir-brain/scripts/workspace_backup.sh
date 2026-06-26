#!/bin/bash
# workspace_backup.sh — Backup workspace to remote targets
# Supports: WebDAV (Nextcloud etc.) + SSH (any server)
# Cron: 0 4 * * * (daily at 04:00)
# Configure targets via environment variables (see below)
#
# ╔══════════════════════════════════════════════════════════════════╗
# ║                      ⚠️  SECURITY WARNING                       ║
# ╠══════════════════════════════════════════════════════════════════╣
# ║ This script packs the ENTIRE workspace into a tar.gz archive,  ║
# ║ including MEMORY.md, daily logs, and any sensitive data.        ║
# ║                                                                ║
# ║ Before enabling:                                               ║
# ║  1. Review backup targets — ensure they are TRUSTED locations  ║
# ║  2. No remote backup is enabled by default; you must manually  ║
# ║     set environment variables (BACKUP_WEBDAV_*, BACKUP_SSH_*)  ║
# ║  3. Run with DRY_RUN=1 first to see what would happen:        ║
# ║       DRY_RUN=1 ./workspace_backup.sh                         ║
# ║  4. Or run manually once before adding to cron                 ║
# ╚══════════════════════════════════════════════════════════════════╝

set -e

WORKSPACE="${MJOLNIR_BRAIN_WORKSPACE:-$HOME/.openclaw/workspace}"
BACKUP_DIR="/tmp/mjolnir-brain-backup"
LOG_FILE="$WORKSPACE/memory/backup.log"
KEEP_COUNT=7  # Number of backup copies to keep

# --- Configuration (set these env vars or edit below) ---
# WebDAV target:
#   BACKUP_WEBDAV_URL="http://your-server/remote.php/webdav/backup/"
#   BACKUP_WEBDAV_USER="user"
#   BACKUP_WEBDAV_PASS="pass"
#
# SSH target:
#   BACKUP_SSH_HOST="your-ssh-alias-or-user@host"
#   BACKUP_SSH_PATH="/path/to/backup/"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# --- DRY_RUN mode: print actions without executing ---
DRY_RUN="${DRY_RUN:-0}"

if [ "$DRY_RUN" = "1" ]; then
    log "=== DRY RUN MODE — no changes will be made ==="
    log "Workspace: $WORKSPACE"
    log "Would create archive in: $BACKUP_DIR"
    if [ -n "$BACKUP_WEBDAV_URL" ]; then
        log "Would upload to WebDAV: $BACKUP_WEBDAV_URL"
    else
        log "WebDAV target: not configured (skipped)"
    fi
    if [ -n "$BACKUP_SSH_HOST" ]; then
        log "Would upload via SSH to: $BACKUP_SSH_HOST:$BACKUP_SSH_PATH"
    else
        log "SSH target: not configured (skipped)"
    fi
    log "=== DRY RUN complete ==="
    exit 0
fi

log "=== Backup started ==="

TIMESTAMP=$(date '+%Y%m%d_%H%M%S')
ARCHIVE="$BACKUP_DIR/workspace_${TIMESTAMP}.tar.gz"
mkdir -p "$BACKUP_DIR"

cd "$WORKSPACE"
tar czf "$ARCHIVE" \
    --exclude='.git' \
    --exclude='node_modules' \
    --exclude='memory/archive' \
    --warning=no-file-changed \
    . 2>/dev/null || [ $? -eq 1 ]

SIZE=$(du -h "$ARCHIVE" | cut -f1)
log "Archive: $ARCHIVE ($SIZE)"

# === Target 1: WebDAV ===
if [ -n "$BACKUP_WEBDAV_URL" ] && [ -n "$BACKUP_WEBDAV_USER" ]; then
    curl -s -X MKCOL -u "$BACKUP_WEBDAV_USER:$BACKUP_WEBDAV_PASS" "$BACKUP_WEBDAV_URL" 2>/dev/null || true
    HTTP=$(curl -s -o /dev/null -w "%{http_code}" \
        -u "$BACKUP_WEBDAV_USER:$BACKUP_WEBDAV_PASS" \
        -T "$ARCHIVE" \
        "${BACKUP_WEBDAV_URL}workspace_${TIMESTAMP}.tar.gz" \
        --connect-timeout 10 --max-time 120 2>/dev/null)
    if [ "$HTTP" = "201" ] || [ "$HTTP" = "204" ]; then
        log "✅ WebDAV: uploaded (HTTP $HTTP)"
    else
        log "❌ WebDAV: failed (HTTP $HTTP)"
    fi
fi

# === Target 2: SSH ===
if [ -n "$BACKUP_SSH_HOST" ] && [ -n "$BACKUP_SSH_PATH" ]; then
    ssh "$BACKUP_SSH_HOST" "mkdir -p $BACKUP_SSH_PATH" 2>/dev/null
    if scp -q "$ARCHIVE" "$BACKUP_SSH_HOST:$BACKUP_SSH_PATH/" 2>/dev/null; then
        log "✅ SSH: uploaded to $BACKUP_SSH_HOST:$BACKUP_SSH_PATH"
        # Rotate old backups
        ssh "$BACKUP_SSH_HOST" "cd $BACKUP_SSH_PATH && ls -t workspace_*.tar.gz | tail -n +$((KEEP_COUNT+1)) | xargs rm -f 2>/dev/null" || true
    else
        log "❌ SSH: upload failed"
    fi
fi

# Cleanup local temp
rm -f "$ARCHIVE"
rmdir "$BACKUP_DIR" 2>/dev/null || true

log "=== Backup complete ==="
