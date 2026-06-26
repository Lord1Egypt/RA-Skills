#!/bin/bash
WORKSPACE="${MEMORY_WORKSPACE:-${HOME}/.openclaw/workspace}"
KEYWORD=$1

if [ -z "$KEYWORD" ]; then
    echo "用法: bash scripts/search.sh <关键词>"
    echo ""
    echo "📚 记忆概览:"
    echo ""
    for dir in "${WORKSPACE}"/memory/*/; do
        if [[ ! "$dir" == "${WORKSPACE}/memory/"* ]]; then
            continue
        fi
        SUBTYPE=$(basename "$dir" 2>/dev/null)
        COUNT=$(find "$dir" -name "*.md" 2>/dev/null | wc -l | tr -d ' ')
        echo "  [${SUBTYPE}] ${COUNT} 条"
    done
    exit 0
fi

# 路径遍历防护
if [[ "$KEYWORD" == *"../"* ]]; then
    echo "错误: 关键词中包含非法字符"
    exit 1
fi

echo "🔍 搜索: ${KEYWORD}"
echo ""
grep -r -l -- "$$KEYWORD" "${WORKSPACE}"/memory/ 2>/dev/null | head -10 | while read file; do
    if [[ ! "$file" == "${WORKSPACE}/memory/"* ]]; then
        continue
    fi
    echo "📄 $(basename $(dirname $file))/$(basename $file)"
    grep -B1 -A2 "name:\|description:" "$file" 2>/dev/null | grep -v "^--$" | head -6
    echo ""
done
