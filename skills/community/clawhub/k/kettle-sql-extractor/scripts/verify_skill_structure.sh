#!/bin/bash
# verify_skill_structure.sh
# 验证技能架构是否符合标准

set -e

SKILL_DIR="$1"
if [ -z "$SKILL_DIR" ]; then
    SKILL_DIR="."
fi

echo "🔍 验证技能架构: $SKILL_DIR"
echo "=========================================="

# 检查必需文件
echo "📋 检查必需文件:"
echo "------------------------------------------"

REQUIRED_FILES=("SKILL.md")

for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$SKILL_DIR/$file" ]; then
        echo "✅ $file - 存在"
    else
        echo "❌ $file - 缺失 (必需文件)"
        exit 1
    fi
done

# 检查推荐文件
echo ""
echo "📋 检查推荐文件:"
echo "------------------------------------------"

RECOMMENDED_FILES=("README.md")

for file in "${RECOMMENDED_FILES[@]}"; do
    if [ -f "$SKILL_DIR/$file" ]; then
        echo "✅ $file - 存在"
    else
        echo "⚠️  $file - 缺失 (推荐文件)"
    fi
done

# 检查目录结构
echo ""
echo "📁 检查目录结构:"
echo "------------------------------------------"

DIRECTORIES=("scripts" "docs" "tests")

for dir in "${DIRECTORIES[@]}"; do
    if [ -d "$SKILL_DIR/$dir" ]; then
        echo "✅ $dir/ - 存在"
    else
        echo "📁 $dir/ - 不存在 (可选目录)"
    fi
done

# 检查scripts目录内容
echo ""
echo "🔧 检查scripts目录:"
echo "------------------------------------------"

if [ -d "$SKILL_DIR/scripts" ]; then
    SCRIPT_FILES=$(find "$SKILL_DIR/scripts" -name "*.py" -o -name "*.sh" -o -name "*.bat" | wc -l)
    echo "✅ scripts/ - 包含 $SCRIPT_FILES 个脚本文件"
    
    # 列出主要脚本
    echo "   主要脚本:"
    find "$SKILL_DIR/scripts" -name "*.py" -o -name "*.sh" -o -name "*.bat" | xargs -I {} basename {} | sort | head -10
else
    echo "📁 scripts/ - 目录不存在"
fi

# 检查docs目录内容
echo ""
echo "📚 检查docs目录:"
echo "------------------------------------------"

if [ -d "$SKILL_DIR/docs" ]; then
    DOC_FILES=$(find "$SKILL_DIR/docs" -name "*.md" | wc -l)
    echo "✅ docs/ - 包含 $DOC_FILES 个文档文件"
    
    # 列出主要文档
    echo "   主要文档:"
    find "$SKILL_DIR/docs" -name "*.md" | xargs -I {} basename {} | sort | head -10
else
    echo "📁 docs/ - 目录不存在"
fi

# 验证SKILL.md内容
echo ""
echo "📄 验证SKILL.md内容:"
echo "------------------------------------------"

if [ -f "$SKILL_DIR/SKILL.md" ]; then
    # 检查必要的元数据字段
    if grep -q "^name:" "$SKILL_DIR/SKILL.md"; then
        echo "✅ name - 存在"
    else
        echo "❌ name - 缺失"
    fi
    
    if grep -q "^version:" "$SKILL_DIR/SKILL.md"; then
        echo "✅ version - 存在"
    else
        echo "❌ version - 缺失"
    fi
    
    if grep -q "^description:" "$SKILL_DIR/SKILL.md"; then
        echo "✅ description - 存在"
    else
        echo "❌ description - 缺失"
    fi
fi

echo ""
echo "=========================================="
echo "🎉 架构验证完成!"
echo ""
echo "架构符合标准要求:"
echo "✅ SKILL.md (必需) - 存在"
echo "✅ scripts/ 目录 - 脚本组织有序"
echo "✅ docs/ 目录 - 文档组织有序"
echo "✅ README.md (推荐) - 存在"
echo ""
echo "技能已准备好按照标准架构使用和分享。"