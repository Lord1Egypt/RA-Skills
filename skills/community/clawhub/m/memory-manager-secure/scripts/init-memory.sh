#!/bin/bash
# 初始化 MEMORY.md

WORKSPACE="$HOME/.openclaw/workspace"
TEMPLATE="$WORKSPACE/skills/memory-manager/templates/MEMORY.md.template"
MEMORY_FILE="$WORKSPACE/MEMORY.md"

if [ -f "$MEMORY_FILE" ]; then
    echo "⚠️  MEMORY.md 已存在，是否覆盖？(y/N)"
    read -r response
    if [[ "$response" != "y" ]]; then
        echo "已取消"
        exit 0
    fi
fi

if [ -f "$TEMPLATE" ]; then
    cp "$TEMPLATE" "$MEMORY_FILE"
    echo "✅ MEMORY.md 已创建"
else
    # 使用内置模板
    cat > "$MEMORY_FILE" << 'EOF'
# MEMORY.md - 长期记忆

## 👤 关于用户
- 称呼：
- 时区：

## 🏠 系统环境
- OpenClaw 版本：

## 📅 重要事件
- 

## 📌 待办事项
- [ ] 

EOF
    echo "✅ MEMORY.md 已创建 (基础模板)"
fi

chmod 600 "$MEMORY_FILE"
echo "🔒 文件权限已设置为 600"
