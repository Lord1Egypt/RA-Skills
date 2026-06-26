#!/bin/bash
# OpenClaw Restore Script
# Usage: ./restore.sh [backup_file]
# If no backup file specified, restores the latest backup

BACKUP_DIR="${HOME}/openclaw-backups"
LATEST_BACKUP=$(ls -t "$BACKUP_DIR"/openclaw-*.tar.gz 2>/dev/null | head -1)
BACKUP_FILE="${1:-$LATEST_BACKUP}"

if [ -z "$BACKUP_FILE" ]; then
    echo "❌ No backup found in $BACKUP_DIR"
    exit 1
fi

if [ ! -f "$BACKUP_FILE" ]; then
    echo "❌ Backup file not found: $BACKUP_FILE"
    exit 1
fi

echo "📦 Restoring from: $BACKUP_FILE"

# Stop gateway
echo "🛑 Stopping gateway..."
openclaw gateway stop

# Backup current state
if [ -d "$HOME/.openclaw" ]; then
    mv "$HOME/.openclaw" "$HOME/.openclaw-pre-restore-$(date +%Y%m%d_%H%M)"
    echo "✅ Current state backed up to ~/.openclaw-pre-restore-*"
fi

# Extract backup
tar -xzf "$BACKUP_FILE" -C "$HOME"

if [ $? -eq 0 ]; then
    echo "✅ Restore completed successfully"
    
    # Restart gateway
    echo "🔄 Starting gateway..."
    openclaw gateway start
    
    echo "✅ Gateway restarted"
    exit 0
else
    echo "❌ Restore failed"
    echo "💡 You can restore from: $HOME/.openclaw-pre-restore-*"
    exit 1
fi
