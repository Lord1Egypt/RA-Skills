#!/bin/bash
# LOBSTER ULTIMATE RESTORE - EXTERNAL TO INTERNAL FLUID TRANSFER
# Designed for maxleolee-eng/openclaw-sys-guardian-v4.1-resurrection

SOURCE="/Users/maxleolee/Downloads/OpenClaw_Mirror/workplace/"
CONFIG_SOURCE="/Users/maxleolee/Downloads/OpenClaw_Mirror/config/config.json"
TARGET="/Users/maxleolee/.openclaw/workspace/"
CONFIG_TARGET="/Users/maxleolee/.openclaw/config.json"

echo "🦞 Starting Ultimate Restoration..."

if [ ! -d "$SOURCE" ]; then
    echo "❌ Error: Source mirror not found at $SOURCE"
    exit 1
fi

# 1. Restore Workspace (The Soul)
rsync -av --delete "$SOURCE" "$TARGET"
echo "✅ Workspace restored."

# 2. Restore Config (The Body)
if [ -f "$CONFIG_SOURCE" ]; then
    cp "$CONFIG_SOURCE" "$CONFIG_TARGET"
    echo "✅ Configuration restored."
fi

# 3. Post-Restoration Validation
echo "🔍 Triggering Skill Alignment Validator..."
sh ./lobster-validator.sh

echo "🚀 Restoration complete. System ready for Gateway restart."
