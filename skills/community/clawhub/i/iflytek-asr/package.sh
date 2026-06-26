#!/bin/bash

echo "📦 打包讯飞语音转文本 Skill"
echo ""

# 设置输出文件名
OUTPUT_NAME="iflytek-asr-skill-$(date +%Y%m%d).zip"

# 检查是否有 .env 文件（警告用户）
if [ -f .env ]; then
    echo "⚠️  警告：检测到 .env 文件！"
    echo "   .env 包含你的 API 凭证，不应该被分发。"
    echo ""
    read -p "确定要继续打包吗？(y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ 已取消打包"
        exit 1
    fi
fi

# 打包（排除敏感文件和输出文件）
echo "📦 打包中..."
cd ..
zip -r "$OUTPUT_NAME" iflytek-asr-skill-template/ \
  -x "*.pyc" \
  -x "**/__pycache__/*" \
  -x "*.env" \
  -x "*.mp3" \
  -x "*.wav" \
  -x "*.txt" \
  -x "*.DS_Store" \
  -x "**/outputs/*" \
  -x "**/downloads/*"

if [ $? -eq 0 ]; then
    echo "✅ 打包完成！"
    echo ""
    echo "📦 输出文件: $OUTPUT_NAME"
    echo "📂 文件大小: $(ls -lh "$OUTPUT_NAME" | awk '{print $5}')"
    echo ""
    echo "✅ 可以分享这个文件了！"
    echo ""
    echo "接收者使用方法："
    echo "  1. unzip $OUTPUT_NAME"
    echo "  2. cd iflytek-asr-skill-template"
    echo "  3. ./install.sh"
else
    echo "❌ 打包失败"
    exit 1
fi
