#!/usr/bin/env bash
# Private Search for OpenClaw — Brave Search Setup Script
# Guides user through getting a Brave Search API key and configuring their OpenClaw environment

set -e

echo ""
echo "🔍 Private Search for OpenClaw — Setup"
echo "======================================="
echo ""
echo "This script will configure Brave Search as your OpenClaw search engine."
echo "Brave Search has an independent index and does not monetize your queries."
echo ""

# Check for existing key
if [ -n "$BRAVE_API_KEY" ]; then
  echo "✅ BRAVE_API_KEY already set in environment."
  echo "   Current key: ${BRAVE_API_KEY:0:8}..."
  echo ""
  read -p "Replace with a new key? (y/N): " replace
  if [[ "$replace" != "y" && "$replace" != "Y" ]]; then
    echo "Keeping existing key."
    exit 0
  fi
fi

echo "Step 1: Get your free Brave Search API key"
echo "------------------------------------------"
echo ""
echo "👉 Open this URL in your browser:"
echo "   https://api.search.brave.com/"
echo ""
echo "   - Create a free account"
echo "   - Go to API Keys → Create Key"
echo "   - Free tier: 2,000 queries/month"
echo "   - Paid: \$3/mo for 20,000 queries"
echo ""
read -p "Paste your Brave Search API key here: " brave_key

if [ -z "$brave_key" ]; then
  echo "❌ No key provided. Exiting."
  exit 1
fi

# Validate key format (Brave keys are typically BSA... format)
echo ""
echo "✅ Key received: ${brave_key:0:8}..."
echo ""

# Detect OpenClaw config location
CONFIG_FILE="$HOME/.openclaw/.env"
if [ ! -f "$CONFIG_FILE" ]; then
  CONFIG_FILE="$HOME/.env"
fi

echo "Step 2: Save to environment"
echo "---------------------------"
echo ""
echo "Writing BRAVE_API_KEY to $CONFIG_FILE"

# Remove existing entry if present
if [ -f "$CONFIG_FILE" ]; then
  grep -v "^BRAVE_API_KEY=" "$CONFIG_FILE" > "$CONFIG_FILE.tmp" && mv "$CONFIG_FILE.tmp" "$CONFIG_FILE"
fi

echo "BRAVE_API_KEY=$brave_key" >> "$CONFIG_FILE"
echo "PRIVATE_SEARCH_ENGINE=brave" >> "$CONFIG_FILE"
echo "PRIVATE_SEARCH_STRIP_TRACKING=true" >> "$CONFIG_FILE"

echo ""
echo "✅ Configuration saved."
echo ""
echo "Step 3: Verify"
echo "--------------"
echo ""
echo "Testing Brave Search API connection..."

response=$(curl -sf -H "Accept: application/json" \
  -H "Accept-Encoding: gzip" \
  -H "X-Subscription-Token: $brave_key" \
  "https://api.search.brave.com/res/v1/web/search?q=test+query+openclaw&count=1" 2>&1)

if echo "$response" | grep -q '"results"'; then
  echo "✅ Brave Search API is working!"
  echo ""
  echo "🎉 Setup complete. Your OpenClaw agent will now use Brave Search for all web queries."
  echo ""
  echo "To use Kagi instead, run: PRIVATE_SEARCH_ENGINE=kagi"
  echo "To self-host with SearXNG, see references/privacy-engines.md"
else
  echo "⚠️  API test returned unexpected response. Check your key and try again."
  echo "   Response: $response"
  exit 1
fi
