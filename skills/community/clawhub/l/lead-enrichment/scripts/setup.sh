#!/bin/bash
# lead-enrichment/scripts/setup.sh — Initialize config and data directories

set -euo pipefail

LE_DIR="${LE_DIR:-$HOME/.config/lead-enrichment}"
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"

echo "🔍 Lead Enrichment Setup"
echo "━━━━━━━━━━━━━━━━━━━━━━"

# Create config and data directories
mkdir -p "$LE_DIR/data/leads"
mkdir -p "$LE_DIR/data/cache"
mkdir -p "$LE_DIR/data/batch-runs"
mkdir -p "$LE_DIR/exports"
echo "✓ Created config and data directories in $LE_DIR"

# Copy example config if none exists
if [ ! -f "$LE_DIR/config.json" ]; then
  cp "$SKILL_DIR/config.example.json" "$LE_DIR/config.json"
  echo "✓ Created config.json (from example — edit with your preferences)"
else
  echo "• config.json already exists (skipped)"
fi

# Check for required tools
for tool in jq curl; do
  if ! command -v "$tool" &> /dev/null; then
    echo "⚠ Prerequisite missing: '$tool'. Please install it to continue."
    # On macOS: brew install jq
    # On Debian/Ubuntu: sudo apt-get install jq
    exit 1
  fi
done
echo "✓ Prerequisites (jq, curl) are installed."


# Check for optional premium source API keys
PREMIUM_SOURCES_FOUND=false
if [ -f "$HOME/.clawdbot/secrets.env" ]; then
  if grep -q "HUNTER_API_KEY" "$HOME/.clawdbot/secrets.env" 2>/dev/null; then
    echo "  ✓ Hunter.io API key found"
    PREMIUM_SOURCES_FOUND=true
  fi
  if grep -q "CLEARBIT_API_KEY" "$HOME/.clawdbot/secrets.env" 2>/dev/null; then
    echo "  ✓ Clearbit API key found"
    PREMIUM_SOURCES_FOUND=true
  fi
    if grep -q "APOLLO_API_KEY" "$HOME/.clawdbot/secrets.env" 2>/dev/null; then
    echo "  ✓ Apollo API key found"
    PREMIUM_SOURCES_FOUND=true
  fi
fi

if [ "$PREMIUM_SOURCES_FOUND" = true ]; then
    echo "✓ Optional: Premium data source API keys detected. Enable them in config.json."
else
    echo "• Optional: No premium API keys (Hunter, Clearbit, Apollo) found. Skill will use public sources."
fi


echo ""
echo "Next steps:"
echo "  1. (Optional) Edit $LE_DIR/config.json to customize enrichment depth and sources."
echo "  2. Test with: $(dirname "$0")/enrich.sh --name \"Elon Musk\" --company \"Tesla\""
echo ""
echo "🕵️  Lead Enrichment is ready to investigate."
