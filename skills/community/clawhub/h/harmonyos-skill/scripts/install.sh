#!/bin/bash
# =============================================================================
# 鸿蒙代码工坊 — 一键安装脚本
# 将构建产物安装到当前项目目录
# =============================================================================
# 用法: 
#   先构建: bash scripts/build-dist.sh
#   再安装: bash scripts/install.sh [工具名称]
#   示例:   bash scripts/install.sh           # 安装所有
#           bash scripts/install.sh cursor    # 仅安装 Cursor
#           bash scripts/install.sh trae      # 仅安装 Trae
# =============================================================================

set -e

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
DIST="$SKILL_DIR/dist"
TARGET="${1:-all}"

echo "🚀 鸿蒙代码工坊 — 一键安装"
echo "=============================="
echo "目标项目: $(pwd)"
echo "安装工具: $TARGET"
echo ""

# 检查 dist 是否存在
if [ ! -d "$DIST" ]; then
    echo "❌ 错误: 找不到 dist/ 目录，请先运行 bash scripts/build-dist.sh"
    exit 1
fi

install_item() {
    local name="$1"
    local src="$2"
    local dst="$3"
    shift 3
    
    if [ "$TARGET" != "all" ] && [ "$TARGET" != "$name" ]; then
        return
    fi
    
    if [ -d "$src" ]; then
        echo "[$name] 📦 复制 $src → $dst"
        cp -r "$src"/* "$dst/"
        echo "  ✅ 完成"
    else
        echo "[$name] ⚠️ 源目录不存在: $src"
    fi
}

install_file() {
    local name="$1"
    local src="$2"
    local dst="$3"
    shift 3
    
    if [ "$TARGET" != "all" ] && [ "$TARGET" != "$name" ]; then
        return
    fi
    
    if [ -f "$src" ]; then
        mkdir -p "$(dirname "$dst")"
        echo "[$name] 📄 复制 $src → $dst"
        cp "$src" "$dst"
        echo "  ✅ 完成"
    else
        echo "[$name] ⚠️ 文件不存在: $src"
    fi
}

# --- Claude Code ---
install_item "claude" "$DIST/claude" "$HOME/.claude/skills"

# --- Cursor ---
install_item "cursor" "$DIST/cursor" "$(pwd)"

# --- Trae ---
install_item "trae" "$DIST/trae" "$(pwd)"

# --- Copilot ---
install_item "copilot" "$DIST/copilot" "$(pwd)"

# --- Windsurf ---
install_file "windsurf" "$DIST/windsurf/.windsurfrules" "$(pwd)/.windsurfrules"

# --- Continue.dev ---
install_item "continue" "$DIST/continue" "$(pwd)"

# --- Gemini CLI ---
install_file "gemini" "$DIST/gemini/GEMINI.md" "$(pwd)/GEMINI.md"

echo ""
echo "=============================="
echo "✅ 安装完成！"
echo ""
echo "💡 验证方法："
echo "  在项目中新建一个 .ets 文件，输入"鸿蒙"或"API"，"
echo "  观察 AI 工具是否自动弹出补全建议。"
echo "=============================="
