#!/usr/bin/env bash
# setup.sh — Offer Assistant 环境安装脚本
# 检测并安装所有依赖（macOS / Linux）
#
# 用法：bash scripts/setup.sh

set -e

echo "🔧 Offer Assistant 依赖安装"
echo "================================"

# --- Node.js ---
if command -v node &>/dev/null; then
  echo "✅ Node.js: $(node -v)"
else
  echo "❌ Node.js not found. Please install Node.js >= 16"
  echo "   https://nodejs.org/"
  exit 1
fi

# --- ws (WebSocket) ---
if node -e "require('ws')" 2>/dev/null; then
  echo "✅ npm ws: 已安装"
else
  echo "📦 安装 ws..."
  npm install ws 2>/dev/null || npm install -g ws 2>/dev/null || {
    echo "⚠️  ws 安装失败，请手动执行: npm install ws"
  }
fi

# --- Chrome ---
CHROME=""
for c in google-chrome-stable google-chrome chromium chromium-browser; do
  if command -v "$c" &>/dev/null; then
    CHROME="$c"
    break
  fi
done

if [ -n "$CHROME" ]; then
  echo "✅ Chrome: $CHROME"
else
  echo ""
  echo "❌ 未检测到 Chrome/Chromium"
  echo "   Linux:   sudo apt install google-chrome-stable"
  echo "   macOS:   brew install --cask google-chrome"
  echo "   或用 set_chrome_path.sh 指定自定义路径"
fi

# --- Tesseract ---
if command -v tesseract &>/dev/null; then
  echo "✅ tesseract: $(tesseract --version 2>&1 | head -1)"
  # 检测中文语言包
  if tesseract --list-langs 2>&1 | grep -q chi_sim; then
    echo "✅ tesseract 中文包 (chi_sim): 已安装"
  else
    echo ""
    echo "⚠️  tesseract 中文语言包未安装"
    echo "   macOS: brew install tesseract-lang"
    echo "   Ubuntu: sudo apt install tesseract-ocr-chi-sim"
    echo "   CentOS: sudo yum install tesseract-langpack-chi-sim"
  fi
else
  echo ""
  echo "❌ tesseract not found"
  echo "   macOS: brew install tesseract"
  echo "   Ubuntu: sudo apt install tesseract-ocr tesseract-ocr-chi-sim"
  echo "   CentOS: sudo yum install tesseract"
fi

echo ""
echo "================================"
echo "✅ 检查完成"
echo ""
echo "Fast Start:"
echo "  clawhub install offer-assistant"
echo "  cd ~/.openclaw/workspace/skills/offer-assistant"
echo "  bash scripts/setup.sh"
