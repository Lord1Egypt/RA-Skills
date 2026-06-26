#!/bin/bash
# List all saved sessions using Oto
# 
# Usage: list-sessions.sh
# 
# Output format:
#   📦 Saved Sessions
#   
#   Platform         Account          Saved
#   ──────────────────────────────────────────
#   amazon           work            Apr 3, 9:00 AM
#   tiktok           work            Apr 3, 9:10 AM

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

node "$OTO_PATH/scripts/list-sessions.js"
