#!/bin/bash
# install.sh — Setup News Summary Bot nhanh
# Chạy: bash install.sh

set -e

echo "📰 News Summary Bot v2 — Setup"
echo "=============================="

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
WORKSPACE_DIR="$(dirname "$SCRIPT_DIR")"
LOG_DIR="$WORKSPACE_DIR/logs"
NODE_BIN="${NODE_BIN:-/home/$USER/.nvm/versions/node/v22.22.1/bin/node}"

# ── Check dependencies ──────────────────────────────────────────────────────
echo ""
echo "🔍 Kiểm tra dependencies..."

if command -v python3 &>/dev/null; then
    echo "  ✅ Python3: $(python3 --version 2>&1)"
else
    echo "  ❌ Python3 không tìm thấy!"
    exit 1
fi

if [ -x "$NODE_BIN" ]; then
    echo "  ✅ Node.js: $($NODE_BIN --version 2>&1)"
else
    echo "  ⚠️  Node.js không tìm thấy, thử node..."
    if command -v node &>/dev/null; then
        NODE_BIN="node"
        echo "  ✅ Node.js: $(node --version)"
    else
        echo "  ❌ Node.js không tìm thấy!"
        exit 1
    fi
fi

# ── Install Playwright ──────────────────────────────────────────────────────
echo ""
echo "🔍 Kiểm tra Playwright..."

cd "$WORKSPACE_DIR"
if [ -d "node_modules/playwright" ]; then
    echo "  ✅ Playwright đã cài"
else
    echo "  📦 Đang cài Playwright..."
    NODE_PATH="$WORKSPACE_DIR/node_modules" "$NODE_BIN" -e "require('playwright')" 2>/dev/null && echo "  ✅ Playwright OK" || {
        echo "  ❌ Playwright chưa cài. Chạy: npm install playwright && npx playwright install chromium"
    }
fi

# ── Setup directories ───────────────────────────────────────────────────────
mkdir -p "$LOG_DIR"
mkdir -p "$WORKSPACE_DIR/references"

# ── Check config ─────────────────────────────────────────────────────────────
echo ""
echo "⚙️  Cấu hình..."
if [ ! -f "$WORKSPACE_DIR/config.json" ]; then
    cat > "$WORKSPACE_DIR/config.json.example" << 'EOF'
{
  "botToken": "YOUR_BOT_TOKEN_HERE",
  "chatId": "YOUR_CHANNEL_ID_HERE",
  "schedule": ["8", "12", "16"]
}
EOF
    echo "  ⚠️  Chưa có config.json"
    echo "  → Tạo config.json.example — hãy tạo config.json với BOT_TOKEN và CHAT_ID"
    echo ""
    echo "  Hướng dẫn nhanh:"
    echo "  1. Mở @BotFather → tạo bot → lấy BOT_TOKEN"
    echo "  2. Tạo Channel → thêm bot làm Admin → lấy CHAT_ID"
    echo "  3. cp config.json.example config.json"
    echo "  4. Sửa BOT_TOKEN và CHAT_ID trong config.json"
else
    echo "  ✅ config.json đã có"
fi

# ── Add cron job ────────────────────────────────────────────────────────────
echo ""
echo "⏰ Setup cron job..."
SCRIPT_PATH="$SCRIPT_DIR/news_summary_v2.sh"
CRON_LINE="0 8,12,16 * * * $SCRIPT_PATH >> $LOG_DIR/news_summary.log 2>&1"

if crontab -l 2>/dev/null | grep -q "news_summary_v2.sh"; then
    echo "  ✅ Cron job đã có"
else
    echo "  📝 Thêm cron job..."
    (crontab -l 2>/dev/null; echo "$CRON_LINE") | crontab -
    echo "  ✅ Cron job đã thêm!"
    echo "  → Chạy lúc 8h, 12h, 16h hàng ngày"
fi

# ── Test run ────────────────────────────────────────────────────────────────
echo ""
echo "🧪 Test chạy..."
if [ -f "$WORKSPACE_DIR/config.json" ]; then
    echo "  (Bỏ qua test — cần config.json trước)"
else
    echo "  ⚠️  Bỏ qua test — tạo config.json trước"
fi

echo ""
echo "=============================="
echo "✅ Setup hoàn tất!"
echo ""
echo "Tiếp theo:"
echo "  1. Tạo config.json với BOT_TOKEN và CHAT_ID"
echo "  2. Test: bash $SCRIPT_DIR/news_summary_v2.sh"
echo "  3. Kiểm tra Telegram channel"
echo ""
echo "Xem chi tiết: cat $SCRIPT_DIR/../SKILL.md"
