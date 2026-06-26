#!/bin/bash
# OpenClaw safe update with Telegram notification
# Usage: bash update.sh [--test-notify] [--dry-run] [--help]
set -euo pipefail

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
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# --- Argument parsing ---
ACTION="update"
for arg in "$@"; do
  case "$arg" in
    --help|-h)
      echo "Usage: bash update.sh [OPTIONS]"
      echo ""
      echo "Options:"
      echo "  --test-notify  Send a test notification and exit"
      echo "  --dry-run      Run pre-update checks only, do not update"
      echo "  --help, -h     Show this help"
      echo ""
      echo "Environment:"
      echo "  OPENCLAW_DIR       Override OpenClaw directory (default: auto-detect)"
      echo "  BACKUP_SCRIPT      Path to backup script to run during pre-flight"
      echo "  TELEGRAM_BOT_TOKEN Bot token (or set in $OPENCLAW_DIR/.telegram-notify.env)"
      echo "  TELEGRAM_CHAT_ID   Chat ID for notifications"
      exit 0
      ;;
    --test-notify)
      ACTION="test-notify"
      ;;
    --dry-run)
      ACTION="dry-run"
      ;;
    *)
      echo "❌ Unknown option: $arg (try --help)"
      exit 1
      ;;
  esac
done

# --- Load notification config ---
ENV_FILE="${OPENCLAW_DIR}/.telegram-notify.env"
if [ -f "$ENV_FILE" ]; then
  set -a; source "$ENV_FILE"; set +a
fi

if [ -z "${TELEGRAM_BOT_TOKEN:-}" ] || [ -z "${TELEGRAM_CHAT_ID:-}" ]; then
  echo "❌ Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID (or create $ENV_FILE)"
  exit 1
fi

notify() {
  local msg="$1"
  local result
  result=$(curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
    -d chat_id="${TELEGRAM_CHAT_ID}" \
    -d text="${msg}" \
    -d parse_mode="Markdown" 2>&1)
  if echo "$result" | grep -q '"ok":true'; then
    echo "📨 Notification sent"
  else
    echo "⚠️  Notification failed: $result"
  fi
}

# --- Test notify ---
if [ "$ACTION" = "test-notify" ]; then
  VERSION=$(openclaw --version 2>/dev/null || echo "unknown")
  notify "🔔 *OpenClaw 通知測試*
版本: $VERSION
時間: $(date '+%Y-%m-%d %H:%M:%S')
✅ 通知功能正常"
  exit 0
fi

OLD_VERSION=$(openclaw --version 2>/dev/null || echo "unknown")

# 1. Pre-update checks
echo "🔍 Running pre-update checks..."
bash "$SCRIPT_DIR/pre-update.sh"

# --- Dry run ---
if [ "$ACTION" = "dry-run" ]; then
  echo "🟡 Dry run complete. No update performed."
  exit 0
fi

# 2. Update (don't rely on exit code — openclaw update may return non-zero even on success)
echo "⬆️  Updating OpenClaw..."
openclaw update 2>&1 || true

# 3. Wait for binary + gateway to come back
echo "⏳ Waiting for OpenClaw to be available..."
NEW_VERSION="unknown"
for i in $(seq 1 60); do
  NEW_VERSION=$(openclaw --version 2>/dev/null || echo "")
  if [ -n "$NEW_VERSION" ]; then
    break
  fi
  sleep 2
done

if [ -z "$NEW_VERSION" ] || [ "$NEW_VERSION" = "" ]; then
  notify "❌ *OpenClaw 更新失敗*
版本: $OLD_VERSION
openclaw 指令在 120 秒後仍無法執行
請手動檢查，或執行 rollback.sh 回退"
  echo "🔴 Update failed — openclaw binary not available"
  exit 1
fi

# 4. Wait for gateway
echo "⏳ Waiting for gateway..."
for i in $(seq 1 30); do
  if openclaw gateway status >/dev/null 2>&1; then
    break
  fi
  sleep 2
done

# 5. Determine success by comparing versions
GATEWAY_STATUS=$(openclaw gateway status 2>&1 | grep -o 'running\|stopped' | head -1 || echo 'unknown')

if [ "$NEW_VERSION" != "$OLD_VERSION" ]; then
  notify "✅ *OpenClaw 更新成功*
$OLD_VERSION → $NEW_VERSION
Gateway: $GATEWAY_STATUS"
  echo "🟢 Update complete: $OLD_VERSION → $NEW_VERSION"
elif [ "$NEW_VERSION" = "$OLD_VERSION" ]; then
  notify "ℹ️ *OpenClaw 版本未變*
版本: $NEW_VERSION（可能已是最新）
Gateway: $GATEWAY_STATUS"
  echo "🟡 Version unchanged: $NEW_VERSION (already up to date?)"
fi
