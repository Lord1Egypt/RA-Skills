#!/bin/bash
set -e

# ==========================================
# BOOTSTRAP: ROLLBACK SCRIPT
# ==========================================
# Rollback Hard Copy (Physical Sync)

perform_hard_copy_rollback() {
    local SLUG=$(basename "$PWD")
    local HOME_DIR="${HOME_MOCK:-$HOME}"
    local OPENCLAW_DIR="$HOME_DIR/.openclaw"
    local SKILLS_DIR="$OPENCLAW_DIR/skills"
    local RELEASES_DIR="$OPENCLAW_DIR/.releases/$SLUG"
    local PROD_DIR="$SKILLS_DIR/$SLUG"

    echo "[$(date '+%H:%M:%S')] Starting hard-copy rollback flow for $SLUG"

    if [ ! -d "$RELEASES_DIR" ]; then
        echo "❌ No releases directory found at $RELEASES_DIR"
        exit 1
    fi

    local LATEST_BACKUP=$(ls -t "$RELEASES_DIR"/backup_*.tar.gz 2>/dev/null | head -n 1)

    if [ -z "$LATEST_BACKUP" ]; then
        echo "❌ No backup tarballs found in $RELEASES_DIR"
        exit 1
    fi

    echo "📦 Found latest backup: $LATEST_BACKUP"

    # 1. Clear current production directory safely
    local OLD_DIR="$SKILLS_DIR/.old_$SLUG"
    rm -rf "$OLD_DIR"
    if [ -e "$PROD_DIR" ]; then
        echo "🗑️ Moving broken directory out of the way..."
        mv "$PROD_DIR" "$OLD_DIR"
    fi

    # 2. Restore backup
    echo "♻️ Restoring backup to $PROD_DIR..."
    tar -xzf "$LATEST_BACKUP" -C "$SKILLS_DIR"
    rm -rf "$OLD_DIR"

    # 3. Gateway Reload
    if [ -z "$HOME_MOCK" ]; then
        echo "🔄 Restarting OpenClaw gateway..."
        openclaw gateway restart || echo "⚠️ Gateway restart failed or not available."
    fi

    echo "✅ ROLLBACK SUCCESS: $SLUG restored from backup."
}

perform_hard_copy_rollback "$@"
