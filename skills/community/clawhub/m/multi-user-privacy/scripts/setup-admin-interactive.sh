#!/bin/bash

# Setup Admin - Interactive Guide
# 交互式管理员设置向导

set -e

SKILL_DIR="$HOME/.openclaw/skills/multi-user-privacy"
CONFIG_FILE="$HOME/.openclaw/workspace/.user-context.json"

echo "🐶 Multi-User Privacy - 管理员设置向导"
echo "======================================"
echo ""

# 检查是否已配置
if [ -f "$CONFIG_FILE" ]; then
  echo "⚠️  配置文件已存在："
  echo ""
  cat "$CONFIG_FILE"
  echo ""
  read -p "是否覆盖现有配置？(y/N): " confirm
  if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
    echo "取消操作"
    exit 0
  fi
fi

echo ""
echo "请选择设置方式："
echo ""
echo "1️⃣  设置自己为管理员"
echo "2️⃣  指定他人为管理员"
echo "3️⃣  退出"
echo ""
read -p "请选择 (1/2/3): " choice

case $choice in
  1)
    echo ""
    echo "设置自己为管理员"
    echo "-----------------"
    read -p "你的账号 ID (如 ou_xxx): " user_id
    read -p "你的称呼 (如 老刘): " user_name
    
    if [ -z "$user_id" ] || [ -z "$user_name" ]; then
      echo "❌ 账号 ID 和称呼不能为空"
      exit 1
    fi
    
    # 创建配置
    cat > "$CONFIG_FILE" << EOF
{
  "_comment": "Multi-User Privacy Configuration - Role-based access control",
  "_version": "0.2.0",
  "_createdAt": "$(date -Iseconds)",
  
  "users": [
    {
      "id": "$user_id",
      "name": "$user_name",
      "role": "admin"
    }
  ],
  
  "privacyMode": "strict"
}
EOF
    
    echo ""
    echo "✅ 管理员设置成功！"
    echo ""
    echo "配置预览:"
    cat "$CONFIG_FILE"
    ;;
    
  2)
    echo ""
    echo "指定他人为管理员"
    echo "-----------------"
    read -p "管理员账号 ID (如 ou_xxx): " admin_id
    read -p "管理员称呼 (如 老刘): " admin_name
    
    if [ -z "$admin_id" ] || [ -z "$admin_name" ]; then
      echo "❌ 账号 ID 和称呼不能为空"
      exit 1
    fi
    
    # 创建配置
    cat > "$CONFIG_FILE" << EOF
{
  "_comment": "Multi-User Privacy Configuration - Role-based access control",
  "_version": "0.2.0",
  "_createdAt": "$(date -Iseconds)",
  
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
    echo "✅ 管理员设置成功！"
    echo ""
    echo "配置预览:"
    cat "$CONFIG_FILE"
    ;;
    
  3)
    echo "退出"
    exit 0
    ;;
    
  *)
    echo "❌ 无效选择"
    exit 1
    ;;
esac

# 创建记忆目录
MEMORY_DIR="$HOME/.openclaw/workspace/memory/users"
mkdir -p "$MEMORY_DIR"

echo ""
echo "✅ 用户记忆目录已创建：$MEMORY_DIR"

echo ""
echo "🎉 设置完成！"
echo ""
echo "下一步:"
echo "1. 重启 OpenClaw: openclaw gateway restart"
echo "2. 开始使用！"
