#!/bin/bash
# 写入记忆
# 用法: bash scripts/save.sh <type> <name> <description> [content]

TYPE=$1
NAME=$2
DESCRIPTION=$3
CONTENT=$4

# 白名单校验：只允许合法的 type
ALLOWED_TYPES="user feedback project reference"
if [ -z "$TYPE" ] || [[ ! " $ALLOWED_TYPES " =~ " $TYPE " ]]; then
    echo "用法: bash scripts/save.sh <type> <name> <description> [content]"
    echo "type 必须是以下之一: user | feedback | project | reference"
    exit 1
fi

# 输入校验：拒绝路径遍历字符
if [[ "$NAME" == *"../"* ]] || [[ "$DESCRIPTION" == *"../"* ]] || [[ "$CONTENT" == *"../"* ]]; then
    echo "错误: 输入中包含非法字符"
    exit 1
fi

# 使用环境变量而非硬编码路径
WORKSPACE="${MEMORY_WORKSPACE:-${HOME}/.openclaw/workspace}"

NAME=$(echo "$NAME" | cut -c1-100)
DESCRIPTION=$(echo "$DESCRIPTION" | cut -c1-200)

if [ -z "$NAME" ]; then
    echo "错误: name 不能为空"
    exit 1
fi

TODAY=$(date +%Y-%m-%d)
MEMORY_FILE="${WORKSPACE}/memory/${TYPE}/${TODAY}.md"

# 安全验证：确保最终路径在预期范围内
if [[ ! "$MEMORY_FILE" == "${WORKSPACE}/memory/"* ]]; then
    echo "错误: 路径越界"
    exit 1
fi

mkdir -p "${WORKSPACE}/memory/${TYPE}"

if [ ! -f "$MEMORY_FILE" ]; then
    echo "# ${TYPE} 记忆 - ${TODAY}" >> "$MEMORY_FILE"
    echo "" >> "$MEMORY_FILE"
fi

cat >> "$MEMORY_FILE" << EOF
---
name: ${NAME}
description: ${DESCRIPTION}
type: ${TYPE}
date: ${TODAY}
---

${CONTENT:-${DESCRIPTION}}

EOF

echo "✅ 记忆已保存: ${MEMORY_FILE}"
