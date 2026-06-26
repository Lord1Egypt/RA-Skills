#!/bin/bash
# PromptBuddy Lite v2.0.0 安装脚本

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

echo "=========================================="
echo "  PromptBuddy Lite v2.0.0 安装"
echo "=========================================="

[ "$EUID" -ne 0 ] && { echo "请使用: sudo $0"; exit 1; }

# 安装核心脚本
echo "[1/3] 安装核心脚本..."
cp "$SCRIPT_DIR/promptbuddy.sh" /usr/local/bin/pb
chmod +x /usr/local/bin/pb

# 安装预处理脚本
echo "[2/3] 安装预处理脚本..."
cp "$SCRIPT_DIR/preprocess.sh" /usr/local/bin/pb-preprocess
chmod +x /usr/local/bin/pb-preprocess

# 创建配置目录
echo "[3/3] 创建配置..."
mkdir -p /etc/promptbuddy-lite
[ ! -f /etc/promptbuddy-lite/config.json ] && cp "$SKILL_DIR/config/config.json" /etc/promptbuddy-lite/

echo ""
echo "=========================================="
echo "  ✅ 安装完成！"
echo "=========================================="
echo ""
echo "使用方式："
echo "  - 自动激活：已在 SKILL.md 中配置"
echo "  - 手动测试：pb \"你的问题\""
echo "  - 预处理测试：pb-preprocess \"你的问题\""
echo ""
echo "示例:"
echo "  pb \"火箭如何上天\""
echo "  pb-preprocess \"如何制定营销策略\""