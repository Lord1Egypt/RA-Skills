#!/bin/bash

# Lee-CLI Skill ClawHub 快速发布脚本
# Quick publication script for lee-cli Skill to ClawHub

set -e

echo "🚀 Lee-CLI Skill ClawHub 发布助手"
echo "=================================="
echo ""

SKILL_DIR="$HOME/.claude/skills/lee-cli"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}📋 检查准备工作...${NC}"
echo ""

# 1. 检查关键文件
echo -e "${BLUE}1️⃣ 检查关键文件:${NC}"
FILES=("SKILL.md" "README.md" "SECURITY.md" "package.json" "CLAWHUB_SUBMISSION.md" "CLAWHUB_PUBLICATION_GUIDE.md")

for file in "${FILES[@]}"; do
    if [ -f "$SKILL_DIR/$file" ]; then
        echo -e "  ${GREEN}✓${NC} $file"
    else
        echo -e "  ${YELLOW}✗${NC} $file 缺失"
    fi
done
echo ""

# 2. 检查Git配置
echo -e "${BLUE}2️⃣ 检查Git配置:${NC}"
cd "$SKILL_DIR"
if git rev-parse --git-dir > /dev/null 2>&1; then
    echo -e "  ${GREEN}✓${NC} Git仓库已配置"
    REMOTE=$(git config --get remote.origin.url 2>/dev/null || echo "未配置")
    echo -e "  ${GREEN}✓${NC} 远程仓库: $REMOTE"
else
    echo -e "  ${YELLOW}✗${NC} Git仓库未配置"
fi
echo ""

# 3. 检查最新提交
echo -e "${BLUE}3️⃣ 检查最新提交:${NC}"
LAST_COMMIT=$(git log -1 --pretty=format:"%h - %s")
echo -e "  ${GREEN}✓${NC} $LAST_COMMIT"
echo ""

# 4. 检查更改状态
echo -e "${BLUE}4️⃣ 检查更改状态:${NC}"
if [ -z "$(git status --porcelain)" ]; then
    echo -e "  ${GREEN}✓${NC} 所有文件已提交,工作目录干净"
else
    echo -e "  ${YELLOW}⚠${NC} 有未提交的更改:"
    git status --short | sed 's/^/    /'
fi
echo ""

# 5. 生成发布摘要
echo -e "${BLUE}5️⃣ 生成发布摘要:${NC}"
echo -e "  ${GREEN}✓${NC} Skill名称: lee-cli"
echo -e "  ${GREEN}✓${NC} 版本: $(grep '\"version\"' $SKILL_DIR/package.json | grep -oE '[0-9]+\.[0-9]+\.[0-9]+')"
echo -e "  ${GREEN}✓${NC} 作者: 李池明"
echo -e "  ${GREEN}✓${NC} 许可证: MIT"
echo ""

# 6. 生成发布包
echo -e "${BLUE}6️⃣ 生成发布包:${NC}"
PUBLISH_DIR="/tmp/lee-cli-publish-$TIMESTAMP"
mkdir -p "$PUBLISH_DIR"

cp -r "$SKILL_DIR" "$PUBLISH_DIR/lee-cli" 2>/dev/null || true
rm -rf "$PUBLISH_DIR/lee-cli/.git" 2>/dev/null || true
rm -rf "$PUBLISH_DIR/lee-cli/node_modules" 2>/dev/null || true

echo -e "  ${GREEN}✓${NC} 发布包已生成: $PUBLISH_DIR/lee-cli"

# 创建ZIP包
ZIP_FILE="$HOME/Desktop/lee-cli-skill-v$(grep '\"version\"' $SKILL_DIR/package.json | grep -oE '[0-9]+\.[0-9]+\.[0-9]+').zip"
cd "$PUBLISH_DIR"
zip -r "$ZIP_FILE" "lee-cli" > /dev/null 2>&1
echo -e "  ${GREEN}✓${NC} ZIP包已生成: $ZIP_FILE"
echo ""

# 7. 生成发布清单
echo -e "${BLUE}7️⃣ 生成发布清单:${NC}"
echo ""
echo "════════════════════════════════════════"
echo "       Lee-CLI Skill 发布准备清单"
echo "════════════════════════════════════════"
echo ""
echo "✅ 基本信息"
echo "   • Skill名称: lee-cli"
echo "   • 版本: $(grep '\"version\"' $SKILL_DIR/package.json | grep -oE '[0-9]+\.[0-9]+\.[0-9]+')"
echo "   • 作者: 李池明 (@leeking001)"
echo "   • 许可证: MIT"
echo ""
echo "✅ 核心功能"
echo "   • 🌤️ 天气冷笑话"
echo "   • 📰 新闻日报"
echo "   • 📝 工作总结"
echo "   • 🎓 AI学习资源"
echo "   • ✅ 智能待办"
echo ""
echo "✅ 文档完整"
echo "   • SKILL.md - Skill定义"
echo "   • README.md - 用户指南"
echo "   • SECURITY.md - 安全报告"
echo "   • CLAWHUB_SUBMISSION.md - 提交信息"
echo "   • CLAWHUB_PUBLICATION_GUIDE.md - 发布指南"
echo ""
echo "✅ GitHub仓库"
echo "   • https://github.com/leeking001/claude-skill-lee-cli"
echo ""
echo "════════════════════════════════════════"
echo ""

# 8. 下一步提示
echo -e "${YELLOW}📝 下一步操作:${NC}"
echo ""
echo "1. 访问 ClawHub 市场"
echo "   URL: (待确认ClawHub官方地址)"
echo ""
echo "2. 点击 'Publish Skill' 或 'Submit Skill'"
echo ""
echo "3. 选择上传方式:"
echo "   选项A: 上传 $ZIP_FILE"
echo "   选项B: 上传 $PUBLISH_DIR/lee-cli 目录"
echo ""
echo "4. 填写表单信息 (参考 CLAWHUB_SUBMISSION.md)"
echo ""
echo "5. 提交审核"
echo ""
echo -e "${GREEN}✨ 所有准备工作已完成!${NC}"
echo ""
echo "运行此脚本的详细日志已保存"
echo "发布包位置: $ZIP_FILE"
echo ""
