#!/bin/bash
# memory-booster 安全打包脚本
# 排除 chroma_db/（隐私数据）+ 开发缓存文件
set -e

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SKILL_NAME=$(basename "$SKILL_DIR")
OUTPUT_DIR="$HOME/Desktop"
ZIP_NAME="${SKILL_NAME}.zip"
ZIP_PATH="$OUTPUT_DIR/$ZIP_NAME"

echo "📦 打包 memory-booster skill..."
echo "   源目录: $SKILL_DIR"
echo "   输出: $ZIP_PATH"
echo ""

# 临时目录
TMP_DIR=$(mktemp -d)
trap "rm -rf $TMP_DIR" EXIT

# 复制到临时目录（排除 chroma_db + 缓存）
rsync -av --exclude='chroma_db/' \
          --exclude='__pycache__/' \
          --exclude='*.pyc' \
          --exclude='.DS_Store' \
          --exclude='*.swp' \
          --exclude='*.zip' \
          "$SKILL_DIR/" "$TMP_DIR/$SKILL_NAME/" 2>&1 | tail -3

# 确认 chroma_db 未包含
if [ -d "$TMP_DIR/$SKILL_NAME/chroma_db" ]; then
    echo "❌ 错误: chroma_db 仍在打包中！"
    exit 1
fi

echo "✅ chroma_db 已排除"

# 创建 ZIP
cd "$TMP_DIR"
zip -r "$ZIP_PATH" "$SKILL_NAME" -x "*.zip" > /dev/null

echo ""
echo "✅ 打包完成！"
echo "   📄 $ZIP_PATH"
echo "   📊 大小: $(du -h "$ZIP_PATH" | cut -f1)"
echo ""
echo "包含文件:"
unzip -l "$ZIP_PATH" | sed '1,3d' | sed '$d' | sed '$d'
