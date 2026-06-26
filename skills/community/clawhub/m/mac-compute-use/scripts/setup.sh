#!/bin/bash
# Setup mcp-server-macos-use: install via brew + register with mcporter
set -e

echo "🖥️  Setting up mac-compute-use..."

# Check macOS
if [ "$(uname)" != "Darwin" ]; then
  echo "❌ This skill requires macOS."
  exit 1
fi

# Check brew
if ! command -v brew &>/dev/null; then
  echo "❌ Homebrew not found. Install from https://brew.sh"
  exit 1
fi

# Install mcp-server-macos-use
if command -v mcp-server-macos-use &>/dev/null; then
  echo "✅ mcp-server-macos-use already installed: $(which mcp-server-macos-use)"
else
  echo "📦 Installing mcp-server-macos-use..."
  brew tap reedburns/mcp-server-macos-use
  brew install mcp-server-macos-use
  echo "✅ Installed: $(which mcp-server-macos-use)"
fi

# Register with mcporter
if command -v mcporter &>/dev/null; then
  if mcporter list 2>/dev/null | grep -q "macos-use"; then
    echo "✅ macos-use already registered in mcporter"
  else
    echo "🔗 Registering with mcporter..."
    mcporter config add macos-use --transport stdio --command "$(which mcp-server-macos-use)"
    echo "✅ Registered as 'macos-use'"
  fi
else
  echo "⚠️  mcporter not found — install with: npm i -g mcporter"
  echo "   Then register manually:"
  echo "   mcporter config add macos-use --transport stdio --command $(which mcp-server-macos-use)"
fi

echo ""
echo "⚠️  Don't forget: grant Accessibility permission!"
echo "   System Settings → Privacy & Security → Accessibility"
echo "   Add: $(which mcp-server-macos-use)"
echo ""
echo "🔥 Done! Test with: mcporter list macos-use --schema"
