#!/bin/bash
# Safe OpenClaw Backup Script
# Creates verified backups without reading system files directly

set -e

# Generate timestamp-based backup directory
TIMESTAMP=$(date +"%Y%m%d-%H%M%S")
BACKUP_DIR="$HOME/openclaw-backups/backup-$TIMESTAMP"

echo "🔒 OpenClaw Safe Backup - $TIMESTAMP"
echo "Creating backup directory: $BACKUP_DIR"

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Critical files to backup (copy only, never read)
declare -a FILES=(
    "$HOME/.openclaw/openclaw.json"
    "$HOME/.openclaw/.env"
    "$HOME/.openclaw/agents/main/agent/auth-profiles.json"
)

# Optional files (if they exist)
declare -a OPTIONAL_FILES=(
    "$HOME/Library/LaunchAgents/ai.openclaw.gateway.plist"
)

echo "📁 Backing up critical files..."
for file in "${FILES[@]}"; do
    if [[ -f "$file" ]]; then
        echo "  ✓ $(basename "$file")"
        cp "$file" "$BACKUP_DIR/"
    else
        echo "  ✗ Missing: $file"
        exit 1
    fi
done

echo "📁 Backing up optional files..."
for file in "${OPTIONAL_FILES[@]}"; do
    if [[ -f "$file" ]]; then
        echo "  ✓ $(basename "$file")"
        cp "$file" "$BACKUP_DIR/"
    else
        echo "  - Skipped: $(basename "$file") (not found)"
    fi
done

echo "✅ Verification..."
# Verify JSON files without reading content (just structure)
if python3 -m json.tool "$BACKUP_DIR/openclaw.json" > /dev/null 2>&1; then
    echo "  ✓ openclaw.json is valid JSON"
else
    echo "  ✗ openclaw.json is invalid JSON"
    exit 1
fi

if python3 -m json.tool "$BACKUP_DIR/auth-profiles.json" > /dev/null 2>&1; then
    echo "  ✓ auth-profiles.json is valid JSON"
else
    echo "  ✗ auth-profiles.json is invalid JSON"
    exit 1
fi

# Verify .env file exists and is readable (don't read content)
if [[ -r "$BACKUP_DIR/.env" ]]; then
    echo "  ✓ .env file backed up"
else
    echo "  ✗ .env file backup failed"
    exit 1
fi

echo "🎉 Backup completed successfully!"
echo "📂 Location: $BACKUP_DIR"
echo "📊 Files: $(ls -1 "$BACKUP_DIR" | wc -l | tr -d ' ')"
echo ""
echo "To restore: cp $BACKUP_DIR/* ~/.openclaw/"
echo "Remember: Restart gateway after restore"