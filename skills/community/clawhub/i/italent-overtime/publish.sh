#!/bin/bash
# 北森 iTalent 加班管理 Skill - 打包发布脚本

set -e

SKILL_NAME="italent-overtime"
SKILL_DIR="$HOME/.openclaw/skills/$SKILL_NAME"
RELEASE_DIR="$HOME/.openclaw/skills/releases"
VERSION="1.1.0"

echo "======================================"
echo " 北森 iTalent 加班管理 Skill 打包"
echo "======================================"
echo ""

# 检查 Skill 目录
if [ ! -d "$SKILL_DIR" ]; then
    echo "❌ 错误：Skill 目录不存在：$SKILL_DIR"
    exit 1
fi

echo "✅ Skill 目录：$SKILL_DIR"

# 创建发布目录
mkdir -p "$RELEASE_DIR"

# 验证必要文件
echo ""
echo "验证必要文件..."
required_files=("SKILL.md" "skill.json" "scripts/italent-overtime-simple.py")
for file in "${required_files[@]}"; do
    if [ -f "$SKILL_DIR/$file" ]; then
        echo "  ✅ $file"
    else
        echo "  ❌ $file (缺失)"
        exit 1
    fi
done

# 创建压缩包
echo ""
echo "创建压缩包..."
cd "$HOME/.openclaw/skills"
PACKAGE_NAME="${SKILL_NAME}-v${VERSION}.tar.gz"
tar -czvf "$RELEASE_DIR/$PACKAGE_NAME" "$SKILL_NAME/"

echo ""
echo "✅ 打包完成！"
echo ""
echo "======================================"
echo " 发布信息"
echo "======================================"
echo ""
echo "📦 压缩包：$RELEASE_DIR/$PACKAGE_NAME"
echo "📊 大小：$(ls -lh "$RELEASE_DIR/$PACKAGE_NAME" | awk '{print $5}')"
echo "📝 版本：v$VERSION"
echo ""
echo "======================================"
echo " 安装说明"
echo "======================================"
echo ""
echo "方式 1：本地安装"
echo "  cp $RELEASE_DIR/$PACKAGE_NAME ~/.openclaw/skills/"
echo "  cd ~/.openclaw/skills/"
echo "  tar -xzvf $PACKAGE_NAME"
echo ""
echo "方式 2：发布到 Skill 仓库"
echo "  1. 上传 $PACKAGE_NAME 到 Skill 仓库"
echo "  2. 更新技能索引"
echo "  3. 通知用户安装"
echo ""
echo "方式 3：Git 发布"
echo "  cd $SKILL_DIR"
echo "  git add ."
echo "  git commit -m 'Release v$VERSION'"
echo "  git tag v$VERSION"
echo "  git push origin main --tags"
echo ""
echo "======================================"
echo " 使用示例"
echo "======================================"
echo ""
echo "安装后首次使用："
echo "  python3 ~/.openclaw/skills/$SKILL_NAME/scripts/italent-overtime-simple.py auth \\"
echo "      --key 你的 AppKey --secret 你的 AppSecret --save"
echo ""
echo "推送加班："
echo "  python3 ~/.openclaw/skills/$SKILL_NAME/scripts/italent-overtime-simple.py push \\"
echo "      --email xxx@company.com --start '2024-01-01 18:00:00' --end '2024-01-01 20:00:00'"
echo ""
echo "======================================"
