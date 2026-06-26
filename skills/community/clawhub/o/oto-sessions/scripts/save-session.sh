#!/bin/bash
# Save a new session (opens browser for manual login)
# 
# Usage: save-session.sh <platform> <url> [account]
# 
# Examples:
#   save-session.sh amazon https://www.amazon.com work
#   save-session.sh tiktok https://www.tiktok.com/login work
#   save-session.sh shopify https://accounts.shopify.com work
#   save-session.sh indeed https://employers.indeed.com personal
# 
# Process:
#   1. Opens browser to <url>
#   2. You log in manually
#   3. Press ENTER when logged in
#   4. Session saved as platform:account
#   5. Ready to reuse in automation

set -e

OTO_PATH="${OTO_PATH:=$HOME/oto}"

if [ ! -d "$OTO_PATH" ]; then
  echo "❌ Error: Oto not found at $OTO_PATH"
  echo ""
  echo "Install Oto:"
  echo "  git clone https://github.com/mbahar/oto.git ~/oto"
  echo "  cd ~/oto && npm install"
  exit 1
fi

PLATFORM="$1"
URL="$2"
ACCOUNT="${3:-default}"

if [ -z "$PLATFORM" ] || [ -z "$URL" ]; then
  echo "Usage: save-session.sh <platform> <url> [account]"
  echo ""
  echo "Examples:"
  echo "  save-session.sh amazon    https://www.amazon.com          work"
  echo "  save-session.sh tiktok    https://www.tiktok.com/login    work"
  echo "  save-session.sh shopify   https://accounts.shopify.com    work"
  echo "  save-session.sh indeed    https://employers.indeed.com    personal"
  echo "  save-session.sh poshmark  https://poshmark.com/login      personal"
  echo "  save-session.sh ebay      https://signin.ebay.com         work"
  exit 1
fi

node "$OTO_PATH/scripts/save-session.js" "$PLATFORM" "$URL" "$ACCOUNT"
