#!/bin/bash

# OpenClaw Backup - Interactive Setup for Linux/Mac

echo "=========================================="
echo "OpenClaw Backup - Setup Wizard"
echo "=========================================="
echo ""

# Default paths with hostname
hostname=$(hostname)
default_backup_root="$HOME/openclaw_backup/$hostname"
default_old_backup="$HOME/openclaw_backup_old/$hostname"

echo "1. Set backup root directory"
echo "   Default: $default_backup_root"
read -p "   Enter new path (press Enter for default): " backup_root
backup_root=${backup_root:-$default_backup_root}

echo ""
echo "2. Set old backup directory"
echo "   Default: $default_old_backup"
read -p "   Enter new path (press Enter for default): " old_backup_root
old_backup_root=${old_backup_root:-$default_old_backup}

echo ""
echo "3. Set number of backups to keep"
echo "   Default: 3"
read -p "   Enter number (press Enter for default): " keep_count
keep_count=${keep_count:-3}

echo ""
echo "4. Set old backup size limit (GB)"
echo "   Default: 10 (cleanup to 5GB when exceeded)"
read -p "   Enter number (press Enter for default): " max_size
max_old_size_gb=${max_size:-10}

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Backup root: $backup_root"
echo "Old backup: $old_backup_root"
echo "Keep count: $keep_count"
echo "Size limit: ${max_old_size_gb}GB"
echo ""

# Save config
config_file="$(dirname "$0")/config.sh"

cat > "$config_file" << EOF
BACKUP_ROOT="$backup_root"
OLD_BACKUP_ROOT="$old_backup_root"
OPENCLAW_HOME="$HOME/.openclaw"
KEEP_COUNT=$keep_count
MAX_OLD_SIZE_GB=$max_old_size_gb
TARGET_OLD_SIZE_GB=5
EOF

echo "Config saved to: $config_file"
echo ""
echo "Run backup: bash $(dirname "$0")/backup.sh"
