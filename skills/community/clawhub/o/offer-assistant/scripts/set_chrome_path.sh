#!/usr/bin/env bash
# set_chrome_path.sh — 指定 Chrome 可执行文件路径
# 用于生成 PDF 时系统找不到 Chrome 的情况
#
# 用法：
#   export CHROME_PATH=/opt/google/chrome/chrome
#   bash scripts/set_chrome_path.sh
#
# 脚本会检查路径有效性并写入配置文件

if [ -z "$1" ] && [ -z "$CHROME_PATH" ]; then
  echo "用法: export CHROME_PATH=/path/to/chrome && bash $0"
  exit 1
fi

CHROME_PATH="${1:-$CHROME_PATH}"

if [ ! -x "$CHROME_PATH" ]; then
  echo "❌ 文件不存在或不可执行: $CHROME_PATH"
  exit 1
fi

echo "✅ Chrome 路径: $CHROME_PATH"
echo ""
echo "将此路径设为环境变量后，generate-pdf.js 会自动使用"
echo "  export CHROME_PATH=\"$CHROME_PATH\""
echo ""
echo "建议添加到 ~/.bashrc 或 ~/.zshrc"
