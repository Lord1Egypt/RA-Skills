#!/bin/bash
# 飞书卡片发送器安装脚本

echo "🚀 开始安装飞书卡片发送器..."

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误：需要Python 3.7+ 环境"
    exit 1
fi

# 检查pip
if ! command -v pip3 &> /dev/null; then
    echo "❌ 错误：需要pip3"
    exit 1
fi

# 安装依赖
echo "📦 安装依赖包..."
pip3 install requests

# 创建符号链接（可选）
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

echo "✅ 安装完成！"
echo ""
echo "📋 下一步："
echo "1. 设置环境变量："
echo "   export FEISHU_APP_ID='your_app_id'"
echo "   export FEISHU_APP_SECRET='your_app_secret'"
echo ""
echo "2. 测试安装："
echo "   python3 $SKILL_DIR/feishu_card_sender_advanced.py"
echo ""
echo "📚 查看文档："
echo "   cat $SKILL_DIR/feishu_card_integration_guide.md"