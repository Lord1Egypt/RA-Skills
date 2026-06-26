#!/bin/bash
# Multi-Web-Search ClawHub 快速发布脚本

echo "╔═══════════════════════════════════════════════════════════════════════╗"
echo "║          Multi-Web-Search | 多引擎网页搜索 - 发布脚本                 ║"
echo "╚═══════════════════════════════════════════════════════════════════════╝"
echo ""

SKILL_DIR="$HOME/.openclaw/skills/multi-web-search"
META_FILE="$SKILL_DIR/_meta.json"

# 检查是否在正确目录
if [ ! -d "$SKILL_DIR" ]; then
    echo "❌ 错误：找不到技能目录 $SKILL_DIR"
    exit 1
fi

cd "$SKILL_DIR"

# 步骤 1: 检查 ownerId
echo "步骤 1/3: 检查 ownerId..."
if grep -q "PLACEHOLDER_OWNER_ID" "$META_FILE"; then
    echo "⚠️  检测到 PLACEHOLDER_OWNER_ID"
    echo ""
    echo "请先更新您的 ClawHub 用户 ID："
    echo "  1. 运行: openclaw whoami"
    echo "  2. 编辑: $META_FILE"
    echo "  3. 将 PLACEHOLDER_OWNER_ID 替换为您的实际 ID"
    echo ""
    read -p "是否已更新？(y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ 发布取消。请更新 ownerId 后重新运行。"
        exit 1
    fi
fi

echo "✅ ownerId 检查通过"
echo ""

# 步骤 2: 验证文件
echo "步骤 2/3: 验证必需文件..."
REQUIRED_FILES=(
    "SKILL.md"
    "metadata.json"
    "_meta.json"
    "LICENSE"
    "CHANGELOG.md"
    "scripts/search.py"
    "scripts/constants.py"
)

ALL_OK=true
for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✅ $file"
    else
        echo "  ❌ $file - 缺失"
        ALL_OK=false
    fi
done

if [ "$ALL_OK" = false ]; then
    echo ""
    echo "❌ 有文件缺失，发布取消。"
    exit 1
fi

echo "✅ 文件验证通过"
echo ""

# 步骤 3: 发布确认
echo "步骤 3/3: 发布确认..."
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "技能名称：Multi-Web-Search | 多引擎网页搜索"
echo "版    本：v3.4.0"
echo "引擎数量：20 个"
echo "功能特性：图片/新闻/视频/DHT/代理/Fallback"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
read -p "确认发布到 ClawHub？(y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ 发布取消。"
    exit 1
fi

echo ""
echo "🚀 正在发布到 ClawHub..."
echo ""

# 执行发布命令
openclaw publish

# 检查发布结果
if [ $? -eq 0 ]; then
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🎉 发布成功！"
    echo ""
    echo "访问您的技能页面："
    echo "https://clawhub.ai/skills/multi-web-search"
    echo ""
    echo "分享链接："
    echo "https://clawhub.ai/@YOUR_USERNAME/multi-web-search"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
else
    echo ""
    echo "❌ 发布失败。请检查错误信息。"
    exit 1
fi
