#!/bin/bash
# optimize_memory.sh - Reduce macOS background memory usage
# Expected savings: 1~2GB RAM
# Requires: sudo for some operations

set -e

echo "=============================="
echo "  Memory Optimization"
echo "=============================="
echo ""

SAVED_MB=0

# 1. Disable Spotlight indexing
echo "[1/6] Disabling Spotlight indexing..."
if sudo mdutil -a -i off 2>/dev/null; then
    echo "  -> Spotlight disabled (saves ~200-400MB)"
    SAVED_MB=$((SAVED_MB + 300))
else
    echo "  -> Spotlight: skipped (needs sudo)"
fi

# 2. Disable Siri
echo "[2/6] Disabling Siri..."
defaults write com.apple.assistant.support "Assistant Enabled" -bool false 2>/dev/null && \
    echo "  -> Siri disabled" || echo "  -> Siri: already disabled or skipped"
# Kill siriknowledged and other Siri processes
killall siriknowledged 2>/dev/null || true
killall assistantd 2>/dev/null || true
SAVED_MB=$((SAVED_MB + 100))

# 3. Disable photo analysis
echo "[3/6] Disabling photo analysis..."
killall photoanalysisd 2>/dev/null && echo "  -> photoanalysisd stopped" || echo "  -> photoanalysisd: not running"
killall photolibraryd 2>/dev/null && echo "  -> photolibraryd stopped" || echo "  -> photolibraryd: not running"
SAVED_MB=$((SAVED_MB + 150))

# 4. Disable analytics and diagnostics
echo "[4/6] Disabling analytics..."
killall analyticsd 2>/dev/null || true
killall diagnosticd 2>/dev/null || true
# Disable crash reporter dialog
defaults write com.apple.CrashReporter DialogType -string "none" 2>/dev/null || true
echo "  -> Analytics/diagnostics reduced"
SAVED_MB=$((SAVED_MB + 100))

# 5. Disable unnecessary iCloud sync processes
echo "[5/6] Reducing iCloud sync overhead..."
killall bird 2>/dev/null && echo "  -> iCloud sync daemon stopped" || echo "  -> iCloud sync: not active"
killall cloudd 2>/dev/null || true
SAVED_MB=$((SAVED_MB + 200))

# 6. Purge inactive memory
echo "[6/6] Purging inactive memory..."
if sudo purge 2>/dev/null; then
    echo "  -> Memory purged"
    SAVED_MB=$((SAVED_MB + 500))
else
    echo "  -> Purge: skipped (needs sudo)"
fi

echo ""
echo "=============================="
echo "  Estimated savings: ~${SAVED_MB}MB"
echo "=============================="
echo ""
echo "Note: Some services may restart after reboot."
echo "To make changes persistent, disable services in System Settings:"
echo "  - Apple ID > iCloud: turn off unnecessary sync"
echo "  - Siri & Spotlight: disable Siri"
echo "  - Notifications: reduce notifications"
