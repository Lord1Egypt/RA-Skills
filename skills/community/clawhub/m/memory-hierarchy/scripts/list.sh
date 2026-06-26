#!/bin/bash
WORKSPACE="${MEMORY_WORKSPACE:-${HOME}/.openclaw/workspace}"

TYPE=$1

# 白名单校验
ALLOWED_TYPES="user feedback project reference"
if [ -n "$TYPE" ] && [[ ! " $ALLOWED_TYPES " =~ " $TYPE " ]]; then
    echo "错误: type 必须是以下之一: user | feedback | project | reference"
    exit 1
fi

if [ -z "$TYPE" ]; then
    echo "📚 所有记忆:"
    echo ""
    for dir in "${WORKSPACE}"/memory/*/; do
        if [[ ! "$dir" == "${WORKSPACE}/memory/"* ]]; then
            continue
        fi
        SUBTYPE=$(basename "$dir" 2>/dev/null)
        echo "━━━ ${SUBTYPE} ━━━"
        for file in "${dir}"*.md; do
            if [ -f "$file" ]; then
                echo "  $(basename $file)"
                grep "^name:\|^description:" "$file" 2>/dev/null | head -2 | sed 's/^/    /'
            fi
        done
        echo ""
    done
else
    echo "📚 ${TYPE} 记忆:"
    echo ""
    for file in "${WORKSPACE}/memory/${TYPE}"/*.md; do
        if [ -f "$file" ]; then
            echo "━━━ $(basename $file) ━━━"
            cat "$file"
            echo ""
        fi
    done
fi
