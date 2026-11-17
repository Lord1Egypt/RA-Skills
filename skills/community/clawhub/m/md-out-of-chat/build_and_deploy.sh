#!/bin/bash
# md2view 构建 + 部署
# 用法：./build_and_deploy.sh <md文件> [--force]
#
# 流程：
# 1. 检查输入 .md 存在
# 2. dist/ 已有内容时要求 --force 确认（避免误删）
# 3. 生成新的 html 到 dist/
# 4. 显示构建结果（部署由宿主工具完成，本脚本不上传）

set -e
SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
DIST_DIR="$SKILL_DIR/dist"

FORCE=0
ARGS=()
for a in "$@"; do
    if [ "$a" = "--force" ] || [ "$a" = "-f" ]; then
        FORCE=1
    else
        ARGS+=("$a")
    fi
done

# 1. 校验参数
if [ -z "${ARGS[0]:-}" ]; then
    echo "用法: $0 <md文件> [--force]"
    echo "示例: $0 demo.md"
    exit 1
fi

MD_FILE="${ARGS[0]}"
if [ ! -f "$MD_FILE" ]; then
    echo "❌ 找不到: $MD_FILE"
    exit 1
fi

# 2. dist 已有内容时要求显式 --force，绝不无提示删除
if [ -d "$DIST_DIR" ] && [ -n "$(ls -A "$DIST_DIR" 2>/dev/null)" ] && [ "$FORCE" -ne 1 ]; then
    echo "⚠ dist/ 已存在且非空。加 --force 覆盖（旧内容将被删除），或手动清理后重试。"
    exit 1
fi

# 3. 准备 dist 目录
echo "→ 准备 dist 目录..."
rm -rf "$DIST_DIR"
mkdir -p "$DIST_DIR"

# 4. 生成 html（用脚本）
cd "$SKILL_DIR"
python3 md2share.py "$MD_FILE" "$DIST_DIR/index.html"

# 5. 校验：必须有 index.html
if [ ! -f "$DIST_DIR/index.html" ]; then
    echo "❌ 部署失败：没有生成 index.html"
    exit 1
fi

# 6. 显示
echo "→ 构建结果："
ls -la "$DIST_DIR"
echo "→ index.html 大小: $(wc -c < "$DIST_DIR/index.html" | tr -d ' ') bytes"
echo "✅ 构建完成，下一步：用你自己的部署工具发布 dist/"
