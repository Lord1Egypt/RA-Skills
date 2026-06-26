#!/usr/bin/env bash
# backup_langfuse.sh — Back up Langfuse Docker volumes to local backup dir.
# Backs up: postgres (traces, scores, evals) + minio (blob storage)
# ClickHouse and Redis are transient — optional.
#
# Usage:
#   bash scripts/backup_langfuse.sh
#
# Env vars (all optional — sensible defaults):
#   LANGFUSE_BACKUP_DIR       Root backup directory (default: ~/.langfuse-backups)
#   LANGFUSE_COMPOSE_DIR      Docker Compose project directory (default: ~/langfuse)
#   LANGFUSE_DB_CONTAINER     Postgres container name (default: langfuse-db-1)
#   LANGFUSE_MINIO_CONTAINER  MinIO container name (default: langfuse-minio-1)
#   LANGFUSE_DB_NAME          Postgres database name (default: langfuse)
#   LANGFUSE_DB_USER          Postgres user (default: langfuse)
#   LANGFUSE_RETENTION_DAYS   Days of backups to keep (default: 14)

set -euo pipefail

BACKUP_BASE="${LANGFUSE_BACKUP_DIR:-$HOME/.langfuse-backups}"
DATE=$(date +%Y-%m-%d)
BACKUP_DIR="$BACKUP_BASE/$DATE"
DB_CONTAINER="${LANGFUSE_DB_CONTAINER:-langfuse-db-1}"
MINIO_CONTAINER="${LANGFUSE_MINIO_CONTAINER:-langfuse-minio-1}"
DB_NAME="${LANGFUSE_DB_NAME:-langfuse}"
DB_USER="${LANGFUSE_DB_USER:-langfuse}"
RETENTION_DAYS="${LANGFUSE_RETENTION_DAYS:-14}"
LOG="/tmp/langfuse-backup.log"

log() { echo "$(date '+%H:%M:%S')  $*" | tee -a "$LOG"; }

log "=== Langfuse backup: $DATE ==="
mkdir -p "$BACKUP_DIR"

# ── Postgres (main database: traces, scores, sessions) ───────────────────────
log "Backing up Postgres..."
if docker ps --format '{{.Names}}' | grep -q "$DB_CONTAINER"; then
    docker exec "$DB_CONTAINER" \
        pg_dump -U "$DB_USER" "$DB_NAME" 2>/dev/null \
        | gzip > "$BACKUP_DIR/postgres-langfuse.sql.gz"
    SIZE=$(du -sh "$BACKUP_DIR/postgres-langfuse.sql.gz" | cut -f1)
    log "✅ Postgres: $SIZE"
else
    log "⚠️  Postgres container '$DB_CONTAINER' not running — skipping"
    log "    (run 'docker ps' to check container names, set LANGFUSE_DB_CONTAINER)"
fi

# ── MinIO (blob storage: uploaded files/media) ────────────────────────────────
log "Backing up MinIO..."
if docker ps --format '{{.Names}}' | grep -q "$MINIO_CONTAINER"; then
    MINIO_VOL=$(docker inspect "$MINIO_CONTAINER" \
        --format '{{range .Mounts}}{{if eq .Type "volume"}}{{.Name}}{{end}}{{end}}' 2>/dev/null | head -1)
    if [ -n "$MINIO_VOL" ]; then
        docker run --rm \
            -v "$MINIO_VOL":/data:ro \
            -v "$BACKUP_DIR":/backup \
            alpine tar czf /backup/minio-data.tar.gz -C /data . 2>/dev/null
        SIZE=$(du -sh "$BACKUP_DIR/minio-data.tar.gz" | cut -f1)
        log "✅ MinIO: $SIZE"
    else
        log "⚠️  Could not find MinIO volume — skipping"
    fi
else
    log "⚠️  MinIO container '$MINIO_CONTAINER' not running — skipping"
fi

# ── Manifest ─────────────────────────────────────────────────────────────────
FILES=$(ls "$BACKUP_DIR" | grep -v manifest.json | python3 -c "
import sys, json
lines = sys.stdin.read().strip().split('\n')
print(json.dumps([l for l in lines if l]))
" 2>/dev/null || echo "[]")

cat > "$BACKUP_DIR/manifest.json" << MANIFEST
{
  "date": "$DATE",
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "host": "$(hostname)",
  "db_container": "$DB_CONTAINER",
  "minio_container": "$MINIO_CONTAINER",
  "files": $FILES,
  "total_size": "$(du -sh "$BACKUP_DIR" | cut -f1)"
}
MANIFEST
log "Manifest written: $BACKUP_DIR/manifest.json"

# ── Prune old backups ─────────────────────────────────────────────────────────
log "Pruning backups older than $RETENTION_DAYS days..."
find "$BACKUP_BASE" -maxdepth 1 -type d -name "20*" -mtime "+$RETENTION_DAYS" \
    -exec rm -rf {} \; 2>/dev/null || true

TOTAL=$(du -sh "$BACKUP_BASE" 2>/dev/null | cut -f1)
log "=== Done. Backup: $BACKUP_DIR | Total store: $TOTAL ==="
