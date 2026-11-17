#!/bin/bash
# 🛡️ Linux Security Guardian — Backup & Restore Script
# Usage:
#   bash hooks/backup-restore.sh backup    — take a timestamped backup
#   bash hooks/backup-restore.sh restore   — restore latest backup
#   bash hooks/backup-restore.sh list      — list available backups

SKILL_NAME="linux-security-guardian"
SKILL_DIR="/root/.openclaw/workspace/skills-extra/$SKILL_NAME"
BACKUP_PRIMARY="/backup/skills-extra"
BACKUP_SECONDARY="/agent-resources/backup/skills-extra"

case "${1:-help}" in
  backup)
    TS=$(date +%Y%m%d_%H%M%S)
    echo "[🔵] Backing up $SKILL_NAME @ $TS"
    mkdir -p "$BACKUP_PRIMARY" "$BACKUP_SECONDARY"
    cp -a "$SKILL_DIR" "$BACKUP_PRIMARY/$SKILL_NAME.$TS"
    cp -a "$SKILL_DIR" "$BACKUP_SECONDARY/$SKILL_NAME.$TS"
    echo "[✅] Primary:   $BACKUP_PRIMARY/$SKILL_NAME.$TS"
    echo "[✅] Secondary: $BACKUP_SECONDARY/$SKILL_NAME.$TS"
    du -sh "$BACKUP_PRIMARY/$SKILL_NAME.$TS"
    ;;

  restore)
    LATEST_PRIMARY=$(ls -dt "$BACKUP_PRIMARY/$SKILL_NAME."* 2>/dev/null | head -1)
    LATEST_SECONDARY=$(ls -dt "$BACKUP_SECONDARY/$SKILL_NAME."* 2>/dev/null | head -1)

    # Pick the most recent from either location
    if [ -n "$LATEST_PRIMARY" ] && [ -n "$LATEST_SECONDARY" ]; then
      if [ "$LATEST_PRIMARY" -nt "$LATEST_SECONDARY" ] 2>/dev/null; then
        RESTORE_FROM="$LATEST_PRIMARY"
      else
        RESTORE_FROM="$LATEST_SECONDARY"
      fi
    elif [ -n "$LATEST_PRIMARY" ]; then
      RESTORE_FROM="$LATEST_PRIMARY"
    elif [ -n "$LATEST_SECONDARY" ]; then
      RESTORE_FROM="$LATEST_SECONDARY"
    else
      echo "[❌] No backups found!"
      exit 1
    fi

    echo "[🟡] Restoring from: $RESTORE_FROM"
    echo "[🟡] Restoring custom files only (keeping registry modules)..."

    # Files that are custom and need restore
    cp "$RESTORE_FROM/SERVER_PROFILE.md" "$SKILL_DIR/SERVER_PROFILE.md"
    cp "$RESTORE_FROM/AGENT.md" "$SKILL_DIR/AGENT.md"
    cp "$RESTORE_FROM/SOUL.md" "$SKILL_DIR/SOUL.md"
    cp "$RESTORE_FROM/hooks/audit-runner.md" "$SKILL_DIR/hooks/audit-runner.md"
    cp "$RESTORE_FROM/hooks/mail-sender.md" "$SKILL_DIR/hooks/mail-sender.md"
    
    # Directories that may not exist after update
    for sub in audit/results actions/auto-done actions/history actions/pending-confirm \
               cve/scan-results cve/.cache network/firewall-snapshots reports/daily; do
      if [ -d "$RESTORE_FROM/$sub" ]; then
        cp -a "$RESTORE_FROM/$sub/"* "$SKILL_DIR/$sub/" 2>/dev/null || true
      fi
    done

    echo "[✅] Restore complete from: $(basename $RESTORE_FROM)"
    echo "[📋] Restored: SERVER_PROFILE.md, AGENT.md, SOUL.md, hooks, audit history"
    ;;

  list)
    echo "[📋] Available backups:"
    echo "--- Primary (/backup/skills/) ---"
    ls -lht "$BACKUP_PRIMARY/" 2>/dev/null | grep "$SKILL_NAME" || echo "(none)"
    echo ""
    echo "--- Secondary (/agent-resources/backup/skills/) ---"
    ls -lht "$BACKUP_SECONDARY/" 2>/dev/null | grep "$SKILL_NAME" || echo "(none)"
    ;;

  *)
    echo "Usage: bash hooks/backup-restore.sh {backup|restore|list}"
    echo ""
    echo "  backup   — Take timestamped backup (both locations)"
    echo "  restore  — Restore latest backup (custom files only)"
    echo "  list     — List all available backups"
    ;;
esac