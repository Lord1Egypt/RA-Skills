#!/bin/bash
# LoR (Loop of Resilience) Setup Script

# 切換到腳本所在的目錄的父目錄
cd "$(dirname "$0")/.."

TARGET_DIR="$HOME/.openclaw/skills/lor"

echo "🔧 Installing LoR System to $TARGET_DIR..."

mkdir -p "$TARGET_DIR"

# 只複製必要的生產環境檔案
cp -r engine/ SKILL.md package.json "$TARGET_DIR/"

echo "✅ LoR installed successfully."
echo "[REGISTER_LOR_SKILL]"
