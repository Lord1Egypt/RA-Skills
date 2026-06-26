#!/bin/bash
# ClawHub 一键发布脚本
# 用法: bash publish-clawhub.sh

set -e

SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
SLUG="ielts-tuyaya-upload"
NAME="IELTS Tuyaya Upload 雅思成绩一键上传"
VERSION="1.3.2"
TAGS="latest"
CHANGELOG="v1.3.2: 域名迁移 tuyaya.online → www.liuxue.online（旧域名因 ICP 备案审核已全站 403 不可用）。sync-review.sh/upload.js 默认 API 地址、所有提示文案、README/SKILL 文档全部切换。老用户必须 --force 更新，已存 token 仍有效。\n\nv1.3.1: 文档大改造，README/SKILL 全面阐释 v1.3.0 OAuth 风格浏览器授权流——新旧流程对比表 + 安全设计四大保障 + Q&A 答疑。同步推送 GitHub。\n\nv1.3.0: 跟随 ielts-reading-review v5.4.0 升级——sync-review.sh 在 IELTS_USER_TOKEN 缺失时，自动调用 setup-client-mode.sh 走浏览器授权流（不再要求用户 F12 手动复制 token）。"

echo "📦 准备发布到 ClawHub..."
echo "   Slug: $SLUG"
echo "   Version: $VERSION"
echo "   Path: $SKILL_DIR"
echo ""

# 检查 clawhub CLI 是否安装
if ! command -v clawhub &> /dev/null; then
    echo "⚠️  clawhub CLI 未安装，正在安装..."
    npm i -g clawhub
fi

# 检查是否已登录
echo "🔐 检查登录状态..."
if ! clawhub whoami &> /dev/null 2>&1; then
    echo "⚠️  未登录，请先运行: clawhub login"
    clawhub login
fi

# 发布
echo ""
echo "🚀 开始发布..."
clawhub publish "$SKILL_DIR" \
    --slug "$SLUG" \
    --name "$NAME" \
    --version "$VERSION" \
    --tags "$TAGS" \
    --changelog "$CHANGELOG"

echo ""
echo "✅ 发布完成！"
echo "   查看: https://clawhub.ai/skill/$SLUG"
echo "   安装: clawhub install $SLUG"

# === 自动同步本地副本到 ~/.workbuddy/skills/ ===
echo ""
echo "🔄 同步本地副本（确保 WorkBuddy 立即用上新版本）..."

USER_SKILLS_DIR="$HOME/.workbuddy/skills"
TARGET="$USER_SKILLS_DIR/$SLUG"
BACKUP="$USER_SKILLS_DIR/$SLUG.bak-$(date +%s)"

# 旧版本可能装在 ielts-review-upload，一并备份
LEGACY_TARGET="$USER_SKILLS_DIR/ielts-review-upload"
if [ -d "$LEGACY_TARGET" ]; then
    mv "$LEGACY_TARGET" "$USER_SKILLS_DIR/ielts-review-upload.bak-$(date +%s)"
    echo "   📦 移除旧 ielts-review-upload 目录（已备份）"
fi

if [ -d "$TARGET" ]; then
    mv "$TARGET" "$BACKUP"
    echo "   📦 旧版本备份: $BACKUP"
fi

cd "$USER_SKILLS_DIR"
clawhub install "$SLUG" --force

if [ -d "$USER_SKILLS_DIR/skills/$SLUG" ] && [ ! -d "$TARGET" ]; then
    mv "$USER_SKILLS_DIR/skills/$SLUG" "$TARGET"
    rmdir "$USER_SKILLS_DIR/skills" 2>/dev/null || true
fi

if [ -d "$TARGET" ]; then
    echo "   ✅ 本地副本已更新: $TARGET"
    echo "   💡 如需回滚: mv $BACKUP $TARGET"
else
    echo "   ❌ 本地副本更新失败，已回滚"
    [ -d "$BACKUP" ] && mv "$BACKUP" "$TARGET"
    exit 1
fi
