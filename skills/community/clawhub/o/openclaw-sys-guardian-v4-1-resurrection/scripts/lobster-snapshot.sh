#!/bin/bash
BACKUP_ROOT="$HOME/openclaw-backups-vault/daily"
TIMESTAMP=$(date +"%Y-%m-%d")
mkdir -p "${BACKUP_ROOT}/${TIMESTAMP}"
cp "$HOME/.openclaw/openclaw.json" "${BACKUP_ROOT}/${TIMESTAMP}/"
[ -f "$HOME/.openclaw/agents/main/agent/auth-profiles.json" ] && cp "$HOME/.openclaw/agents/main/agent/auth-profiles.json" "${BACKUP_ROOT}/${TIMESTAMP}/"
cp "$HOME/.openclaw/workspace/"*.md "${BACKUP_ROOT}/${TIMESTAMP}/"
find "${BACKUP_ROOT}" -type d -mtime +7 -exec rm -rf {} +
