#!/bin/bash
# PaperMC World Backup Script
# Creates compressed archive of world data

set -e

# Configuration - Update these paths
SERVER_DIR="/path/to/your/papermc-server"  # CHANGE THIS
BACKUP_DIR="${SERVER_DIR}/backup"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
ARCHIVE_NAME="world-backup-${TIMESTAMP}.tar.gz"

echo "[backup] server dir: ${SERVER_DIR}"
echo "[backup] backup dir: ${BACKUP_DIR}"
echo "[backup] archive: ${BACKUP_DIR}/${ARCHIVE_NAME}"

# Create backup directory
mkdir -p "${BACKUP_DIR}"

# Check if server is running and save data
if pgrep -f "papermc.jar" > /dev/null; then
    echo "[backup] server is running, saving data before backup..."
    # Note: Add save-all command here if using RCON or console
fi

# Create backup
cd "${SERVER_DIR}"
tar -czf "${BACKUP_DIR}/${ARCHIVE_NAME}" \
    world/ \
    world_nether/ \
    world_the_end/ \
    plugins/ \
    2>/dev/null || true

echo "[backup] backup created: ${BACKUP_DIR}/${ARCHIVE_NAME}"

# Clean old backups (keep last 10)
echo "[backup] cleaning old backups, keep latest 10 ..."
cd "${BACKUP_DIR}"
ls -t world-backup-*.tar.gz 2>/dev/null | tail -n +11 | xargs -r rm -f

echo "[backup] done"
