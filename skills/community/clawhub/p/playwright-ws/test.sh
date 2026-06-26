#!/bin/bash
set -e

echo "Testing Playwright Skill..."

# Check if node is available
if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found"
    exit 1
fi

# Check if scripts exist
if [ ! -f "scripts/screenshot.js" ]; then
    echo "❌ screenshot.js not found"
    exit 1
fi

if [ ! -f "scripts/pdf-export.js" ]; then
    echo "❌ pdf-export.js not found"
    exit 1
fi

echo "✅ All files present"
echo "✅ Ready to use"

# Note: Requires PLAYWRIGHT_WS environment variable
if [ -z "$PLAYWRIGHT_WS" ]; then
    echo "⚠️  Note: Set PLAYWRIGHT_WS environment variable for testing"
else
    echo "✅ PLAYWRIGHT_WS is set"
fi

echo ""
echo "Test complete!"