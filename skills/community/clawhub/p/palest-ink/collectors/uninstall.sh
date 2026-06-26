#!/bin/bash
# Palest Ink (淡墨) - Uninstallation Script

set -e

PALEST_INK_DIR="$HOME/.palest-ink"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

info() { echo -e "${GREEN}[palest-ink]${NC} $1"; }
warn() { echo -e "${YELLOW}[palest-ink]${NC} $1"; }

# Step 1: Remove launchd agent
PLIST_LABEL="com.palest-ink.collector"
PLIST_PATH="$HOME/Library/LaunchAgents/${PLIST_LABEL}.plist"
info "Removing launchd agent..."
if launchctl list | grep -q "$PLIST_LABEL" 2>/dev/null; then
    launchctl unload "$PLIST_PATH" 2>/dev/null || true
    info "launchd agent unloaded."
fi
if [ -f "$PLIST_PATH" ]; then
    rm -f "$PLIST_PATH"
    info "launchd plist removed."
else
    info "No launchd plist found."
fi

# Also remove legacy cron job if present
if crontab -l 2>/dev/null | grep -q "palest-ink"; then
    crontab -l 2>/dev/null | grep -v "palest-ink" | crontab -
    info "Legacy cron job removed."
fi

# Step 2: Restore git hooks path
info "Restoring git hooks..."
CURRENT_HOOKS=$(git config --global core.hooksPath 2>/dev/null || echo "")
if [ "$CURRENT_HOOKS" = "$PALEST_INK_DIR/hooks" ]; then
    # Check if there was a previous hooks path
    if [ -f "$PALEST_INK_DIR/config.json" ]; then
        PREV_PATH=$(python3 -c "
import json
with open('$PALEST_INK_DIR/config.json') as f:
    cfg = json.load(f)
print(cfg.get('previous_hooks_path', ''))
" 2>/dev/null || echo "")
        if [ -n "$PREV_PATH" ]; then
            git config --global core.hooksPath "$PREV_PATH"
            info "Restored previous hooksPath: $PREV_PATH"
        else
            git config --global --unset core.hooksPath
            info "Removed global hooksPath."
        fi
    else
        git config --global --unset core.hooksPath
        info "Removed global hooksPath."
    fi
fi

# Step 3: Ask about data
echo ""
warn "Data directory: $PALEST_INK_DIR"
read -p "Delete all collected data? (y/N): " DELETE_DATA
if [ "$DELETE_DATA" = "y" ] || [ "$DELETE_DATA" = "Y" ]; then
    rm -rf "$PALEST_INK_DIR"
    info "Data directory removed."
else
    # Only remove hooks and bin, keep data
    rm -rf "$PALEST_INK_DIR/hooks" "$PALEST_INK_DIR/bin"
    info "Hooks and scripts removed. Data preserved at $PALEST_INK_DIR/data/"
fi

info ""
info "Palest Ink uninstalled."
