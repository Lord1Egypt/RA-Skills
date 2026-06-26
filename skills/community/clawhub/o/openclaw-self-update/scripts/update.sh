#!/bin/bash
# OpenClaw Self-Update Script
# Updates OpenClaw to the latest version via npm

set -e

echo "🔍 Checking versions..."

CURRENT=$(openclaw --version 2>/dev/null || echo "not installed")
LATEST=$(npm show openclaw version 2>/dev/null || echo "unknown")

echo "   Current: $CURRENT"
echo "   Latest:  $LATEST"

if [ "$CURRENT" = "$LATEST" ]; then
    echo "✅ Already on latest version ($CURRENT)"
    exit 0
fi

if [ "$LATEST" = "unknown" ]; then
    echo "❌ Could not fetch latest version from npm"
    exit 1
fi

echo ""
echo "📦 Updating OpenClaw: $CURRENT → $LATEST"
echo ""

# Update via npm
npm install -g openclaw@latest

echo ""
echo "🔄 Restarting gateway..."

# Restart gateway
openclaw gateway restart 2>/dev/null || {
    echo "⚠️  Gateway restart failed, trying stop + start..."
    openclaw gateway stop 2>/dev/null || true
    sleep 2
    openclaw gateway start
}

# Wait for gateway to be ready
sleep 3

# Verify update
NEW_VERSION=$(openclaw --version 2>/dev/null || echo "unknown")

echo ""
if [ "$NEW_VERSION" = "$LATEST" ]; then
    echo "✅ Update complete: $CURRENT → $NEW_VERSION"
else
    echo "⚠️  Version mismatch after update"
    echo "   Expected: $LATEST"
    echo "   Got: $NEW_VERSION"
    exit 1
fi

# Show brief changelog hint
echo ""
echo "📝 View changelog:"
echo "   cat \$(npm root -g)/openclaw/CHANGELOG.md | head -100"
