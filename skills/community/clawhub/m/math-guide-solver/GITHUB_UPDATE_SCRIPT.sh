#!/bin/bash

# 🚀 Math-Solver Skill v1.1.0 GitHub 更新脚本
# 执行此脚本以完成版本更新和 GitHub 发布

echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║                                                                      ║"
echo "║         🚀 Math-Solver Skill v1.1.0 GitHub 更新                      ║"
echo "║                                                                      ║"
echo "║         将完成以下操作：                                             ║"
echo "║         1. 复制 CHANGELOG.md 和更新的 README                         ║"
echo "║         2. 创建 Git Tag v1.1.0                                       ║"
echo "║         3. 推送更新到 GitHub                                         ║"
echo "║                                                                      ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""

# 进入 math-solver 目录
MATH_SOLVER_PATH="/Users/yshajoy/downloads/math\ resolve\ skill/math-solver"

if [ ! -d "$MATH_SOLVER_PATH" ]; then
    echo "❌ 错误：找不到 math-solver 目录"
    echo "   期望路径：$MATH_SOLVER_PATH"
    echo "   请手动修改脚本中的路径"
    exit 1
fi

cd "$MATH_SOLVER_PATH" || exit 1

echo "✅ 已进入目录：$(pwd)"
echo ""

# 第一步：复制文件
echo "════════════════════════════════════════════════════════════════════════"
echo "第 1 步：复制文件"
echo "════════════════════════════════════════════════════════════════════════"
echo ""

# 检查来源文件
SOURCE_CHANGELOG="/mnt/user-data/outputs/CHANGELOG.md"
SOURCE_README="/mnt/user-data/outputs/README_v1.1.0.md"

if [ ! -f "$SOURCE_CHANGELOG" ]; then
    echo "❌ 错误：找不到 CHANGELOG.md"
    exit 1
fi

if [ ! -f "$SOURCE_README" ]; then
    echo "❌ 错误：找不到 README_v1.1.0.md"
    exit 1
fi

# 复制 CHANGELOG
echo "📋 复制 CHANGELOG.md..."
cp "$SOURCE_CHANGELOG" CHANGELOG.md
if [ -f "CHANGELOG.md" ]; then
    echo "✅ CHANGELOG.md 已复制"
else
    echo "❌ CHANGELOG.md 复制失败"
    exit 1
fi
echo ""

# 备份原 README
if [ -f "README.md" ]; then
    echo "📋 备份原 README.md → README.md.bak"
    cp README.md README.md.bak
    echo "✅ 备份完成"
fi
echo ""

# 复制新 README
echo "📋 复制更新的 README.md..."
cp "$SOURCE_README" README.md
if [ -f "README.md" ]; then
    echo "✅ README.md 已更新"
else
    echo "❌ README.md 更新失败"
    exit 1
fi
echo ""

# 第二步：Git 操作
echo "════════════════════════════════════════════════════════════════════════"
echo "第 2 步：Git 操作"
echo "════════════════════════════════════════════════════════════════════════"
echo ""

# 检查 Git 状态
echo "🔍 检查 Git 状态..."
git status
echo ""

# 添加文件
echo "📝 添加文件到 Git..."
git add CHANGELOG.md README.md
echo "✅ 文件已添加"
echo ""

# 查看要提交的更改
echo "📋 将提交的更改："
git diff --cached --name-only
echo ""

# 提交更改
echo "💾 提交更改..."
git commit -m "docs: Update to v1.1.0

- Add CHANGELOG.md with complete version history
- Update README.md with new features
- Document formula embedding feature
- Add installation and usage instructions
- Include theme and DPI configuration examples
- Add v1.1.0 release notes"

if [ $? -eq 0 ]; then
    echo "✅ 提交成功"
else
    echo "⚠️  提交失败（可能没有新的更改）"
fi
echo ""

# 第三步：创建 Git Tag
echo "════════════════════════════════════════════════════════════════════════"
echo "第 3 步：创建 Git Tag v1.1.0"
echo "════════════════════════════════════════════════════════════════════════"
echo ""

# 检查 Tag 是否已存在
if git rev-parse v1.1.0 >/dev/null 2>&1; then
    echo "⚠️  Tag v1.1.0 已存在"
    echo "   是否删除并重新创建？"
    read -p "   输入 'y' 继续，其他键跳过：" -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🗑️  删除旧 Tag..."
        git tag -d v1.1.0
        git push origin :refs/tags/v1.1.0
    else
        echo "⏭️  跳过 Tag 创建"
    fi
fi

# 创建 Tag
if ! git rev-parse v1.1.0 >/dev/null 2>&1; then
    echo "🏷️  创建 Tag v1.1.0..."
    git tag -a v1.1.0 -m "Release v1.1.0: Add formula embedding in HTML

Features:
- LaTeX formulas automatically render as PNG images
- Formulas embed directly in solution steps
- Support 4 visual themes: light, dark, sepia, chalk
- Automatic LaTeX extraction and formula positioning
- Responsive HTML design

Technical Details:
- Add StepEmbeddedSolutionFormatter class
- Add SolutionRenderer for HTML/JSON output
- Support for multiple DPI settings (150, 300, 600)
- Base64 encoded formula images for portability

Updated Dependencies:
- matplotlib >= 3.5.0
- Pillow >= 9.0.0"

    if [ $? -eq 0 ]; then
        echo "✅ Tag v1.1.0 已创建"
    else
        echo "❌ Tag 创建失败"
        exit 1
    fi
fi
echo ""

# 第四步：推送到 GitHub
echo "════════════════════════════════════════════════════════════════════════"
echo "第 4 步：推送到 GitHub"
echo "════════════════════════════════════════════════════════════════════════"
echo ""

# 推送提交
echo "📤 推送提交到 GitHub..."
git push origin main
if [ $? -eq 0 ]; then
    echo "✅ 提交已推送"
else
    echo "❌ 推送失败，请检查网络和 GitHub 认证"
    exit 1
fi
echo ""

# 推送 Tag
echo "🏷️  推送 Tag 到 GitHub..."
git push origin v1.1.0
if [ $? -eq 0 ]; then
    echo "✅ Tag 已推送"
else
    echo "❌ Tag 推送失败"
    exit 1
fi
echo ""

# 完成
echo "════════════════════════════════════════════════════════════════════════"
echo "✅ 完成！"
echo "════════════════════════════════════════════════════════════════════════"
echo ""
echo "📊 更新摘要："
echo "  • CHANGELOG.md - 已创建/更新"
echo "  • README.md - 已更新（v1.0.0 → v1.1.0）"
echo "  • Git Tag v1.1.0 - 已创建并推送"
echo "  • GitHub 分支 main - 已更新"
echo ""
echo "🚀 下一步："
echo "  1. 访问 GitHub 创建 Release"
echo "     → https://github.com/yshajoy-star/math-solver/releases/new"
echo "  2. 选择 Tag v1.1.0"
echo "  3. 填写发布说明并发布"
echo ""
echo "验证："
echo "  • GitHub Tags: https://github.com/yshajoy-star/math-solver/tags"
echo "  • Commits: https://github.com/yshajoy-star/math-solver/commits/main"
echo ""

