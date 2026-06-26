#!/bin/bash

# Multi-User Privacy - 初始化用户上下文配置
# 用法：bash init-user-context.sh

set -e

WORKSPACE="$HOME/.openclaw/workspace"
CONFIG_FILE="$WORKSPACE/.user-context.json"
SKILL_DIR="$HOME/.openclaw/skills/multi-user-privacy"

echo "🐶 Multi-User Privacy 初始化（基于角色的权限管理）"
echo "===================================================="

# 检查配置文件是否已存在
if [ -f "$CONFIG_FILE" ]; then
  echo "⚠️  配置文件已存在：$CONFIG_FILE"
  read -p "是否覆盖？(y/N): " confirm
  if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
    echo "取消操作"
    exit 0
  fi
fi

# 获取用户输入
echo ""
echo "请输入管理员账号信息："
echo "---------------------"

read -p "管理员账号 ID (如 ou_xxx): " admin_id
read -p "管理员称呼 (如 老刘): " admin_name

# 生成配置文件
cat > "$CONFIG_FILE" << EOF
{
  "_comment": "Multi-User Privacy Configuration - Role-based access control",
  "_version": "0.2.0",
  
  "users": [
    {
      "id": "$admin_id",
      "name": "$admin_name",
      "role": "admin"
    }
  ],
  
  "privacyMode": "strict"
}
EOF

echo ""
echo "✅ 配置文件已创建：$CONFIG_FILE"
echo ""
echo "内容预览:"
cat "$CONFIG_FILE"
echo ""

# 创建用户隔离记忆目录
MEMORY_DIR="$WORKSPACE/memory/users"
mkdir -p "$MEMORY_DIR"

# 创建管理员记忆文件
cat > "$MEMORY_DIR/${admin_id}.md" << EOF
# $admin_name ($admin_id)

**角色**: 管理员 (admin)
**首次对话**: $(date '+%Y-%m-%d')

## 权限

- 可查看完整账号信息
- 可讨论账号管理相关话题
- 不受隐私限制

## 备注

由 init-user-context.sh 自动创建
EOF

echo "✅ 用户记忆目录已创建：$MEMORY_DIR"
echo "✅ 管理员记忆文件已创建：$MEMORY_DIR/${admin_id}.md"

# 更新 TOOLS.md（如果存在）
TOOLS_FILE="$WORKSPACE/TOOLS.md"
if [ -f "$TOOLS_FILE" ]; then
  echo ""
  read -p "是否更新 TOOLS.md 添加隐私规则？(Y/n): " update_tools
  if [ "$update_tools" != "n" ] && [ "$update_tools" != "N" ]; then
    # 检查是否已存在隐私规则
    if grep -q "账号隐私规则" "$TOOLS_FILE"; then
      echo "ℹ️  TOOLS.md 已包含隐私规则，跳过更新"
    else
      cat >> "$TOOLS_FILE" << 'EOF'

---

## 🔒 多用户隐私规则（由 multi-user-privacy 技能管理）

**核心原则：** 每个账号的对话都是独立的世界，互不交叉。

- 跟某个账号聊天时，不要提及其他任何账号的存在
- 不要说"主人"、"管理员"等角色给非管理员用户
- 只当世界上只有你和当前对话的人在聊天

**权限管理：** 基于角色（role）而非具体账号

EOF
      echo "✅ TOOLS.md 已更新"
    fi
  fi
fi

echo ""
echo "🎉 初始化完成！"
echo ""
echo "下一步:"
echo "1. 重启 OpenClaw: openclaw gateway restart"
echo "2. 开始使用！每个用户的对话将自动隔离"
echo ""
echo "添加更多用户:"
echo "  编辑 $CONFIG_FILE，在 users 数组中添加新用户"
