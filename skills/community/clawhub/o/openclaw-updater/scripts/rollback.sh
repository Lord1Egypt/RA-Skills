#!/bin/bash
# Rollback OpenClaw to previous version and restore config if needed
# Usage: bash rollback.sh [--confirm] [--help]
set -e

# --- Argument parsing ---
CONFIRMED=false
for arg in "$@"; do
  case "$arg" in
    --help|-h)
      echo "Usage: bash rollback.sh [OPTIONS]"
      echo ""
      echo "Options:"
      echo "  --confirm  Skip confirmation prompt and proceed"
      echo "  --help, -h Show this help"
      exit 0
      ;;
    --confirm)
      CONFIRMED=true
      ;;
    *)
      echo "❌ Unknown option: $arg (try --help)"
      exit 1
      ;;
  esac
done

# Auto-detect OpenClaw directory
if [ -n "${OPENCLAW_DIR:-}" ]; then
  :
elif [ -d "$HOME/.openclaw" ]; then
  OPENCLAW_DIR="$HOME/.openclaw"
elif [ -d "$HOME/clawd" ]; then
  OPENCLAW_DIR="$HOME/clawd"
else
  OPENCLAW_DIR="$HOME/.openclaw"
fi

# 1. Determine previous version
if [ -f /tmp/openclaw-prev-version.txt ]; then
  PREV_VERSION=$(cat /tmp/openclaw-prev-version.txt)
  echo "📌 Previous version: $PREV_VERSION"
else
  echo "❌ No previous version recorded. Specify manually:"
  echo "   npm install -g openclaw@<version>"
  exit 1
fi

CURRENT_VERSION=$(openclaw --version 2>/dev/null || echo "unknown")
echo "📌 Current version: $CURRENT_VERSION"

# 2. Confirmation
if [ "$CONFIRMED" != true ]; then
  read -p "⚠️  Rollback $CURRENT_VERSION → $PREV_VERSION? [y/N] " yn
  if [[ ! "$yn" =~ ^[Yy]$ ]]; then
    echo "❌ Aborted"
    exit 0
  fi
fi

# 3. Rollback package
echo "⏪ Rolling back to openclaw@$PREV_VERSION..."
npm install -g "openclaw@$PREV_VERSION"

# 4. Restore config if needed
if [ -f /tmp/openclaw.json.bak ]; then
  read -p "Restore openclaw.json from backup? [y/N] " yn
  if [[ "$yn" =~ ^[Yy]$ ]]; then
    cp /tmp/openclaw.json.bak "$OPENCLAW_DIR/openclaw.json"
    echo "✅ Config restored"
  fi
fi

# 5. Restart gateway
echo "🔄 Restarting gateway..."
openclaw gateway restart 2>/dev/null || echo "⚠️  Gateway restart failed — check manually"

echo ""
openclaw --version
echo "🟢 Rollback complete"
