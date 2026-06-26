#!/usr/bin/env bash
# OpenClaw Restore Script ☺️🌸
# Purpose: Clones/pulls the backup from Git and restores it to the .openclaw directory.

set -e

# Fetch repository URL from OpenClaw config
REPO_URL=$(openclaw config get skills.entries.openclaw-backup-restore.env.OPENCLAW_BACKUP_REPO 2>/dev/null | tr -d '"')

if [ -z "$REPO_URL" ] || [ "$REPO_URL" == "null" ]; then
    echo "Error: OPENCLAW_BACKUP_REPO is not set."
    exit 1
fi

BACKUP_DIR="${HOME}/openclaw-backup/"
DEST_DIR="${HOME}/.openclaw/"

echo "[$(date)] Starting OpenClaw restore process..."

# 1. Ensure backup directory exists and is up to date
if [ ! -d "$BACKUP_DIR" ]; then
    echo "Cloning backup repository..."
    git clone "$REPO_URL" "$BACKUP_DIR"
else
    echo "Updating backup repository..."
    cd "$BACKUP_DIR" && git pull origin main
fi

# 2. Sync back to the production directory
# Does not delete new files in production unless explicitly managed
echo "Syncing files to $DEST_DIR..."
mkdir -p "$DEST_DIR"
rsync -av --exclude=".git/" --exclude=".gitignore" "$BACKUP_DIR" "$DEST_DIR"

# 3. Restore dependencies
echo "Restoring node dependencies..."
cd "$DEST_DIR"
# Check for package.json in typical plugin/extension locations
find . -name "package.json" -not -path "*/node_modules/*" -execdir npm install \;

# 4. Fix environment using OpenClaw doctor
echo "Running openclaw doctor to fix environment..."
openclaw doctor --yes

echo "[$(date)] Restore complete! Please restart the gateway. ☺️🌸"
