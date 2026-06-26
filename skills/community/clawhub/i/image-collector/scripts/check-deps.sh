#!/bin/bash
# image-collector 依赖检查脚本

echo "🔍 检查 image-collector 依赖..."

# 检查 Python 版本
if command -v python3 &> /dev/null; then
    python_version=$(python3 --version | cut -d' ' -f2)
    echo "✓ Python: $python_version"
else
    echo "✗ Python3 未安装"
    exit 1
fi

# 检查 Pillow
if python3 -c "from PIL import Image" 2>/dev/null; then
    echo "✓ Pillow: 已安装"
else
    echo "✗ Pillow: 未安装"
    echo "  安装命令：pip3 install Pillow"
    exit 1
fi

# 检查 Requests
if python3 -c "import requests" 2>/dev/null; then
    echo "✓ Requests: 已安装"
else
    echo "✗ Requests: 未安装"
    echo "  安装命令：pip3 install requests"
    exit 1
fi

# 检查输出目录
output_dir="/home/node/.openclaw/workspace/article-images"
if [ -d "$output_dir" ]; then
    echo "✓ 输出目录：$output_dir"
else
    echo "✓ 创建输出目录：$output_dir"
    mkdir -p "$output_dir"
fi

echo ""
echo "✅ 所有依赖检查通过！"
echo ""
echo "使用示例："
echo "  python3 ~/.openclaw/workspace/skills/image-collector/scripts/collect_images.py \\"
echo "    --news \"苹果国行 AI 凌晨偷跑\" \\"
echo "    --keywords \"Apple,Intelligence,Baidu\" \\"
echo "    --source \"apple.com\""
