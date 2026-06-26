#!/bin/bash
# Book-PDF 版本更新脚本模板
#
# 用法：
#   ./update.sh patch "修正某个错误"     # 修订：1.0.0 → 1.0.1
#   ./update.sh minor "更新某部分内容"     # 次版本：1.0.0 → 1.1.0
#   ./update.sh major "新增某个章节"       # 主版本：1.0.0 → 2.0.0
#   ./update.sh build                      # 仅增加build号，不改版本

set -e
cd "$(dirname "$0")"

BUMP_TYPE="${1:-build}"
MESSAGE="${2:-无描述}"
TODAY=$(date +%Y-%m-%d)
VERSION_FILE="version.json"
CHANGELOG="CHANGELOG.md"

# 读取当前版本
CURRENT_VERSION=$(node -e "console.log(require('./$VERSION_FILE').version)")
CURRENT_BUILD=$(node -e "console.log(require('./$VERSION_FILE').build)")

# 计算新版本
IFS='.' read -r MAJOR MINOR PATCH <<< "$CURRENT_VERSION"
case "$BUMP_TYPE" in
  major) MAJOR=$((MAJOR + 1)); MINOR=0; PATCH=0 ;;
  minor) MINOR=$((MINOR + 1)); PATCH=0 ;;
  patch) PATCH=$((PATCH + 1)) ;;
  build) ;; # 只增加build号
  *) echo "❌ 未知类型: $BUMP_TYPE (可选: major/minor/patch/build)"; exit 1 ;;
esac

NEW_VERSION="$MAJOR.$MINOR.$PATCH"
NEW_BUILD=$((CURRENT_BUILD + 1))

echo "📦 版本更新: v$CURRENT_VERSION (#$CURRENT_BUILD) → v$NEW_VERSION (#$NEW_BUILD)"

# 更新 version.json
node -e "
const fs = require('fs');
const v = JSON.parse(fs.readFileSync('$VERSION_FILE', 'utf-8'));
v.version = '$NEW_VERSION';
v.build = $NEW_BUILD;
v.lastUpdate = '$TODAY';
fs.writeFileSync('$VERSION_FILE', JSON.stringify(v, null, 2) + '\n');
"

# 写入 CHANGELOG（仅非build类型）
if [ "$BUMP_TYPE" != "build" ]; then
  node -e "
const fs = require('fs');
let log = fs.readFileSync('$CHANGELOG', 'utf-8');
const entry = '\n## [$NEW_VERSION] $TODAY — $MESSAGE\n\n- $MESSAGE\n';
const firstEntry = log.indexOf('\n## [');
if (firstEntry !== -1) {
  log = log.slice(0, firstEntry) + entry + log.slice(firstEntry);
} else {
  log += entry;
}
fs.writeFileSync('$CHANGELOG', log);
"
  echo "📝 CHANGELOG 已更新"
fi

# 构建 HTML
echo ""
echo "🔨 构建 HTML..."
node build.js

# 构建 PDF
echo ""
echo "📄 生成 PDF..."
node build-pdf.js

# 读取标题用于文件名
TITLE=$(node -e "console.log(require('./$VERSION_FILE').title)")

# 备份到 versions/ 目录（仅非build类型）
if [ "$BUMP_TYPE" != "build" ]; then
  mkdir -p versions
  cp "output/$TITLE-v$NEW_VERSION.pdf" "versions/$TITLE-v$NEW_VERSION.pdf"
  echo "💾 备份: versions/$TITLE-v$NEW_VERSION.pdf"
fi

echo ""
echo "✅ 完成！v$NEW_VERSION (build #$NEW_BUILD)"
echo "   HTML: output/$TITLE-v$NEW_VERSION.html"
echo "   PDF:  output/$TITLE-v$NEW_VERSION.pdf"
