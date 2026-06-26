#!/bin/bash
# 牛牛量化技能打包脚本

SKILL_DIR="$HOME/.openclaw/workspace/skills/niuniu-quant"
OUTPUT_DIR="$HOME/.openclaw/workspace/skills"

echo "======================================"
echo "📦 打包牛牛量化技能..."
echo "======================================"
echo ""

# 检查 SKILL.md
if [ ! -f "$SKILL_DIR/SKILL.md" ]; then
    echo "❌ 错误：SKILL.md 不存在"
    exit 1
fi

# 创建 .skill 文件（zip 格式）
cd "$SKILL_DIR/.."
zip -r "$OUTPUT_DIR/niuniu-quant.skill" niuniu-quant/

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ 技能打包成功！"
    echo "📦 文件位置：$OUTPUT_DIR/niuniu-quant.skill"
    echo ""
    echo "查看文件:"
    ls -lh "$OUTPUT_DIR/niuniu-quant.skill"
else
    echo ""
    echo "❌ 打包失败"
    exit 1
fi

echo ""
echo "======================================"
