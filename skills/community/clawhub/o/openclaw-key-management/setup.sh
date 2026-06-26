#!/bin/bash

# OpenClaw Key Management Skill Setup Script
# Run this after installation to configure your security preferences

set -e

WORKSPACE_PATH="${1:-$HOME/.openclaw/zhaining}"
CONFIG_FILE="$WORKSPACE_PATH/skills/openclaw-key-management/config/key_management.json"

echo "⚙️  OpenClaw Key Management Skill Setup"
echo "Workspace: $WORKSPACE_PATH"

if [ ! -f "$CONFIG_FILE" ]; then
    echo "❌ Configuration file not found. Please install the skill first."
    exit 1
fi

echo ""
echo "Security Mode Options:"
echo "1. Convenience Mode (system key) - Automatic decryption, no password required"
echo "2. High-Security Mode (passphrase) - Password required at each session start"
echo ""

read -p "Choose security mode (1 or 2) [1]: " SECURITY_MODE
SECURITY_MODE=${SECURITY_MODE:-1}

case $SECURITY_MODE in
    1)
        echo "Setting convenience mode (system key)..."
        sed -i 's/"master_key_mode": "passphrase"/"master_key_mode": "system_key"/' "$CONFIG_FILE"
        ;;
    2)
        echo "Setting high-security mode (passphrase)..."
        sed -i 's/"master_key_mode": "system_key"/"master_key_mode": "passphrase"/' "$CONFIG_FILE"
        ;;
    *)
        echo "Invalid choice. Using default (convenience mode)."
        ;;
esac

echo ""
echo "Additional Options:"
echo "Enable automatic backups? (y/n) [y]: "
read BACKUP_CHOICE
BACKUP_CHOICE=${BACKUP_CHOICE:-y}

if [[ $BACKUP_CHOICE == "n" || $BACKUP_CHOICE == "N" ]]; then
    sed -i 's/"enabled": true/"enabled": false/' "$CONFIG_FILE"
    echo "Backups disabled."
else
    echo "Backups enabled (default)."
fi

echo ""
echo "Credential timeout (seconds) [30]: "
read TIMEOUT_CHOICE
TIMEOUT_CHOICE=${TIMEOUT_CHOICE:-30}

if [[ $TIMEOUT_CHOICE =~ ^[0-9]+$ ]]; then
    sed -i "s/\"credential_timeout_seconds\": [0-9]*/\"credential_timeout_seconds\": $TIMEOUT_CHOICE/" "$CONFIG_FILE"
    echo "Credential timeout set to $TIMEOUT_CHOICE seconds."
else
    echo "Using default timeout (30 seconds)."
fi

echo ""
echo "✅ Setup complete!"
echo "Configuration updated: $CONFIG_FILE"
echo ""
echo "You can manually edit the configuration file for advanced settings."