#!/usr/bin/env bash
# restore_langfuse.sh — Restore Langfuse Docker volumes from a backup.
#
# Usage:
#   bash scripts/restore_langfuse.sh <YYYY-MM-DD>
#   bash scripts/restore_langfuse.sh latest
#
# Env vars (same as backup script):
#   LANGFUSE_BACKUP_DIR       Root backup directory (default: ~/.langfuse-backups)
#   LANGFUSE_COMPOSE_DIR      Docker Compose project directory (default: ~/langfuse)
#   LANGFUSE_DB_CONTAINER     Postgres container name (default: langfuse-db-1)
#   LANGFUSE_MINIO_CONTAINER  MinIO container name (default: langfuse-minio-1)
#   LANGFUSE_DB_NAME          Postgres database name (default: langfuse)
#   LANGFUSE_DB_USER          Postgres user (default: langfuse)

set -euo pipefail

BACKUP_BASE="${LANGFUSE_BACKUP_DIR:-$HOME/.langfuse-backups}"
COMPOSE_DIR="${LANGFUSE_COMPOSE_DIR:-$HOME/langfuse}"
DB_CONTAINER="${LANGFUSE_DB_CONTAINER:-langfuse-db-1}"
MINIO_CONTAINER="${LANGFUSE_MINIO_CONTAINER:-langfuse-minio-1}"
DB_NAME="${LANGFUSE_DB_NAME:-langfuse}"
DB_USER="${LANGFUSE_DB_USER:-langfuse}"

log() { echo "$(date '+%H:%M:%S')  $*"; }
err() { echo "❌  ERROR: $*" >&2; exit 1; }

# Resolve backup date
DATE_ARG="${1:-latest}"
if [ "$DATE_ARG" = "latest" ]; then
    BACKUP_DATE=$(ls -1 "$BACKUP_BASE" | grep -E '^20[0-9]{2}-[0-9]{2}-[0-9]{2}$' | sort | tail -1)
    if [ -z "$BACKUP_DATE" ]; then
        err "No backups found in $BACKUP_BASE"
    fi
    log "Resolved 'latest' → $BACKUP_DATE"
else
    BACKUP_DATE="$DATE_ARG"
fi

BACKUP_DIR="$BACKUP_BASE/$BACKUP_DATE"
[ -d "$BACKUP_DIR" ] || err "Backup directory not found: $BACKUP_DIR"

log "=== Langfuse restore: $BACKUP_DATE ==="

# ── Validate manifest ─────────────────────────────────────────────────────────
if [ -f "$BACKUP_DIR/manifest.json" ]; then
    log "Manifest:"
    cat "$BACKUP_DIR/manifest.json"
    echo ""
else
    log "⚠️  No manifest.json found — proceeding anyway"
fi

# ── Validate backup files exist ───────────────────────────────────────────────
PG_FILE="$BACKUP_DIR/postgres-langfuse.sql.gz"
MINIO_FILE="$BACKUP_DIR/minio-data.tar.gz"

[ -f "$PG_FILE" ] && log "✅ Found: postgres-langfuse.sql.gz" || log "⚠️  Missing: postgres-langfuse.sql.gz"
[ -f "$MINIO_FILE" ] && log "✅ Found: minio-data.tar.gz" || log "⚠️  Missing: minio-data.tar.gz"

# ── Confirm ───────────────────────────────────────────────────────────────────
echo ""
echo "⚠️  WARNING: This will overwrite the current Langfuse database and MinIO data."
echo "   Restore from: $BACKUP_DIR"
echo "   Langfuse must be STOPPED before restoring."
echo ""
read -r -p "Continue? [y/N] " CONFIRM
[ "$CONFIRM" = "y" ] || { log "Aborted."; exit 0; }

# ── Check Langfuse is stopped ─────────────────────────────────────────────────
if docker ps --format '{{.Names}}' | grep -q "langfuse"; then
    echo ""
    echo "⚠️  Langfuse containers appear to be running."
    echo "   Stop them first: cd $COMPOSE_DIR && docker compose down"
    echo ""
    read -r -p "Stop them now and continue? [y/N] " STOP_CONFIRM
    if [ "$STOP_CONFIRM" = "y" ]; then
        (cd "$COMPOSE_DIR" && docker compose down) || true
        sleep 3
    else
        log "Aborted — stop Langfuse first."
        exit 1
    fi
fi

# ── Start only the DB container for restore ───────────────────────────────────
log "Starting DB container for restore..."
(cd "$COMPOSE_DIR" && docker compose up -d langfuse-db) 2>/dev/null || \
(cd "$COMPOSE_DIR" && docker compose up -d db) 2>/dev/null || true
sleep 5

# ── Restore Postgres ──────────────────────────────────────────────────────────
if [ -f "$PG_FILE" ]; then
    log "Restoring Postgres from $PG_FILE..."
    
    # Drop and recreate the database
    docker exec "$DB_CONTAINER" psql -U "$DB_USER" postgres \
        -c "DROP DATABASE IF EXISTS $DB_NAME;" 2>/dev/null || true
    docker exec "$DB_CONTAINER" psql -U "$DB_USER" postgres \
        -c "CREATE DATABASE $DB_NAME;" 2>/dev/null || true
    
    # Restore
    zcat "$PG_FILE" | docker exec -i "$DB_CONTAINER" \
        psql -U "$DB_USER" "$DB_NAME" -q
    
    log "✅ Postgres restored"
else
    log "⚠️  Skipping Postgres restore (no backup file)"
fi

# ── Start MinIO for restore ───────────────────────────────────────────────────
if [ -f "$MINIO_FILE" ]; then
    log "Restoring MinIO from $MINIO_FILE..."
    
    (cd "$COMPOSE_DIR" && docker compose up -d minio) 2>/dev/null || \
    (cd "$COMPOSE_DIR" && docker compose up -d langfuse-minio) 2>/dev/null || true
    sleep 5
    
    MINIO_VOL=$(docker inspect "$MINIO_CONTAINER" \
        --format '{{range .Mounts}}{{if eq .Type "volume"}}{{.Name}}{{end}}{{end}}' 2>/dev/null | head -1)
    
    if [ -n "$MINIO_VOL" ]; then
        # Clear and restore
        docker run --rm \
            -v "$MINIO_VOL":/data \
            -v "$BACKUP_DIR":/backup:ro \
            alpine sh -c "rm -rf /data/* && tar xzf /backup/minio-data.tar.gz -C /data"
        log "✅ MinIO restored from volume $MINIO_VOL"
    else
        log "⚠️  Could not find MinIO volume — skipping"
    fi
else
    log "⚠️  Skipping MinIO restore (no backup file)"
fi

# ── Done ──────────────────────────────────────────────────────────────────────
log ""
log "=== Restore complete ==="
log "Start Langfuse: cd $COMPOSE_DIR && docker compose up -d"
