#!/bin/bash
# image-optimizer 安装脚本

set -e

echo "🖼️  正在安装 image-optimizer..."

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误：未找到 python3，请先安装 Python 3.7+"
    exit 1
fi

echo "✅ Python 检查通过"

# 安装依赖
echo "📦 正在安装 Pillow..."
pip install Pillow

echo ""
echo "🎉 image-optimizer 安装完成！"
echo ""
echo "使用方法："
echo "  python source/image_optimizer.py --help"
echo ""
echo "快速开始："
echo "  # 压缩图片质量为 85"
echo "  python source/image_optimizer.py --quality 85"
echo ""
echo "  # 调整最大宽度为 1920px"
echo "  python source/image_optimizer.py --max-width 1920"
echo ""
echo "  # 转换为 WebP 格式"
echo "  python source/image_optimizer.py --format webp"
echo ""
