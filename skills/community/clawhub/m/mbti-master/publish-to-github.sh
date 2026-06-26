#!/bin/bash

# GitHub发布辅助脚本
# 用法: bash publish-to-github.sh [你的GitHub用户名]

USERNAME=$1

if [ -z "$USERNAME" ]; then
    echo "用法: bash publish-to-github.sh [你的GitHub用户名]"
    echo "示例: bash publish-to-github.sh shven"
    exit 1
fi

echo "═══════════════════════════════════════════════════════════════"
echo "              MBTI Master - GitHub发布助手"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "GitHub用户名: $USERNAME"
echo "仓库名称: mbti-master"
echo ""

# 检查git
if ! command -v git &> /dev/null; then
    echo "❌ 未安装git，请先安装"
    exit 1
fi

# 检查gh CLI
if ! command -v gh &> /dev/null; then
    echo "⚠️  未安装GitHub CLI (gh)"
    echo "建议安装以获得最佳体验: https://cli.github.com/"
    echo ""
    echo "或手动执行以下命令:"
    echo "  git init"
    echo "  git add ."
    echo "  git commit -m 'Initial release v1.0.0'"
    echo "  git remote add origin https://github.com/$USERNAME/mbti-master.git"
    echo "  git push -u origin main"
    exit 1
fi

# 检查登录状态
echo "检查GitHub登录状态..."
if ! gh auth status &> /dev/null; then
    echo "⚠️  未登录GitHub，请先执行: gh auth login"
    exit 1
fi

echo "✓ GitHub CLI已登录"
echo ""

# 确认执行
read -p "确认发布到 github.com/$USERNAME/mbti-master ? [y/N]: " confirm

if [[ $confirm != [yY] && $confirm != [yY][eE][sS] ]]; then
    echo "已取消"
    exit 0
fi

echo ""
echo "开始发布流程..."
echo ""

# 1. 初始化git
echo "1️⃣  初始化git仓库..."
git init
git add .
git commit -m "Initial release v1.0.0 - MBTI personality analysis tool"
echo ""

# 2. 创建GitHub仓库
echo "2️⃣  创建GitHub仓库..."
if gh repo view "$USERNAME/mbti-master" &> /dev/null; then
    echo "⚠️  仓库已存在，使用现有仓库"
    git remote add origin "https://github.com/$USERNAME/mbti-master.git"
else
    gh repo create mbti-master --public --source=. --remote=origin --push
fi
echo ""

# 3. 推送代码
echo "3️⃣  推送代码..."
git branch -M main
if ! git push -u origin main 2>/dev/null; then
    git push -f origin main
fi
echo ""

# 4. 创建标签
echo "4️⃣  创建版本标签..."
git tag -a v1.0.0 -m "v1.0.0 release"
git push origin v1.0.0
echo ""

# 5. 创建发布包
echo "5️⃣  创建发布包..."
RELEASE_FILE="mbti-master-v1.0.0.tar.gz"
tar -czf "$RELEASE_FILE" --exclude='.git' --exclude='*.tar.gz' --exclude='publish-to-github.sh' .
echo "✓ 发布包已创建: $RELEASE_FILE"
echo ""

# 6. 创建Release
echo "6️⃣  创建GitHub Release..."
gh release create v1.0.0 \
    --title "v1.0.0 - Initial Release" \
    --notes "## MBTI Master v1.0.0

由申建开发的MBTI人格分析工具首个正式版本。

### 功能特性
- 🧪 4维度8题快速测试
- 📊 16型人格完整分析
- 💕 人格兼容性匹配
- 🎮 趣味互动游戏
- 📚 荣格认知功能详解

### 安装使用
\`\`\`bash
git clone https://github.com/$USERNAME/mbti-master.git
cd mbti-master
bash scripts/quick_test.sh
\`\`\`

### 作者
申建

### 许可证
MIT License" \
    "$RELEASE_FILE"

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "✅ 发布完成！"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "访问地址:"
echo "  代码仓库: https://github.com/$USERNAME/mbti-master"
echo "  Release页面: https://github.com/$USERNAME/mbti-master/releases"
echo ""
echo "分享链接:"
echo "  \`\`\`bash"
echo "  git clone https://github.com/$USERNAME/mbti-master.git"
echo "  \`\`\`"
echo ""
echo "═══════════════════════════════════════════════════════════════"