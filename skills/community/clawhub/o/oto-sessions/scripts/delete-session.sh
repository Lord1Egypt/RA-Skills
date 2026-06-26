#!/bin/bash
# Delete a saved session
# 
# Usage: delete-session.sh <platform> [account]
# 
# Examples:
#   delete-session.sh amazon work      # Delete amazon:work
#   delete-session.sh amazon            # Delete amazon:default
#   delete-session.sh tiktok work

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
ACCOUNT="${2:-default}"

if [ -z "$PLATFORM" ]; then
  echo "Usage: delete-session.sh <platform> [account]"
  echo ""
  echo "Examples:"
  echo "  delete-session.sh amazon work"
  echo "  delete-session.sh tiktok"
  exit 1
fi

node "$OTO_PATH/scripts/delete-session.js" "$PLATFORM" "$ACCOUNT"
