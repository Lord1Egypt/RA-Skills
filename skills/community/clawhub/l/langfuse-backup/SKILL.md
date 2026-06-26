---
name: langfuse-backup
version: 1.0.2
metadata:
  openclaw:
    emoji: "💾"
    requires:
      bins: ["docker"]
      env: []
    network:
      outbound: false
      reason: "Backs up local Docker volumes only. No data is sent to remote servers."
    security_notes: "All operations are local Docker volume copies. No data leaves the local machine. Backup files are stored in a local directory specified by the user."
description: "Docker volume backup and restore for self-hosted Langfuse. Use when: backing up a self-hosted Langfuse instance, restoring Langfuse after a crash or migration, setting up daily cron backups for Langfuse postgres/clickhouse/minio/redis volumes. Backs up postgres (traces, scores), minio (blobs), with optional clickhouse and redis. Includes restore script with validation and 14-day retention pruning."
---
**Last used:** 2026-03-24
**Memory references:** 2
**Status:** Active


# langfuse-backup

Backup and restore Docker volumes for a self-hosted Langfuse instance.

## Scripts

- `scripts/backup_langfuse.sh` — back up postgres + minio volumes (primary data)
- `scripts/restore_langfuse.sh` — restore from a specific backup date

## Quick start

```bash
# Configure (env vars or edit the script defaults)
export LANGFUSE_BACKUP_DIR="$HOME/.langfuse-backups"
export LANGFUSE_COMPOSE_DIR="/path/to/langfuse"   # directory with docker-compose.yml
export LANGFUSE_DB_CONTAINER="langfuse-db-1"       # postgres container name
export LANGFUSE_MINIO_CONTAINER="langfuse-minio-1" # minio container name
export LANGFUSE_DB_NAME="langfuse"                  # postgres database name
export LANGFUSE_DB_USER="langfuse"                  # postgres user

# Run a backup
bash scripts/backup_langfuse.sh

# List available backups
ls "$LANGFUSE_BACKUP_DIR"

# Restore from a date
bash scripts/restore_langfuse.sh 2026-02-27
```

## Env vars

| Var                       | Default                              | Description                         |
|---------------------------|--------------------------------------|-------------------------------------|
| `LANGFUSE_BACKUP_DIR`     | `~/.langfuse-backups`                | Root backup directory               |
| `LANGFUSE_COMPOSE_DIR`    | `~/langfuse`                         | Docker Compose project directory    |
| `LANGFUSE_DB_CONTAINER`   | `langfuse-db-1`                      | Postgres container name             |
| `LANGFUSE_MINIO_CONTAINER`| `langfuse-minio-1`                   | MinIO container name                |
| `LANGFUSE_DB_NAME`        | `langfuse`                           | Postgres database name              |
| `LANGFUSE_DB_USER`        | `langfuse`                           | Postgres user                       |
| `LANGFUSE_RETENTION_DAYS` | `14`                                 | How many days of backups to keep    |

## What gets backed up

| Volume    | Backed up? | Notes                                       |
|-----------|------------|---------------------------------------------|
| Postgres  | ✅ Yes     | `pg_dump` → `.sql.gz` — traces, scores, evals |
| MinIO     | ✅ Yes     | `tar.gz` — uploaded blobs                  |
| ClickHouse| ⚠️ Optional| Large; many users skip (replayed from traces)|
| Redis     | ⚠️ Skip    | Cache only — safe to skip                  |

## Cron setup (macOS LaunchAgent)

```xml
<!-- ~/Library/LaunchAgents/com.yourname.langfuse-backup.plist -->
<key>StartCalendarInterval</key>
<dict>
  <key>Hour</key><integer>2</integer>
  <key>Minute</key><integer>0</integer>
</dict>
<key>ProgramArguments</key>
<array>
  <string>/bin/bash</string>
  <string>/path/to/scripts/backup_langfuse.sh</string>
</array>
<key>StandardOutPath</key>
<string>/tmp/langfuse-backup.log</string>
```

## Restore procedure

```bash
# 1. Stop Langfuse
cd $LANGFUSE_COMPOSE_DIR && docker compose down

# 2. Restore from backup
bash scripts/restore_langfuse.sh 2026-02-27

# 3. Start Langfuse
cd $LANGFUSE_COMPOSE_DIR && docker compose up -d
```
