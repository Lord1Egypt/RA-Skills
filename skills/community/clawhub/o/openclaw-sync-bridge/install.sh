#!/bin/bash
# OpenClaw Sync Bridge Skill v2.0 - 智能安装脚本 (Mac/Linux)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_NAME="openclaw-sync-bridge"

# 检测工作目录
find_workspace() {
    local candidates=(
        "$OPENCLAW_WORKSPACE"
        "$OPENCLAW_STATE_DIR/workspace"
        "$HOME/.openclaw/workspace"
        "$HOME/.config/openclaw/workspace"
        "$HOME/.local/share/openclaw/workspace"
        "./.openclaw/workspace"
        "./workspace"
    )
    
    for candidate in "${candidates[@]}"; do
        if [ -z "$candidate" ]; then continue; fi
        local path="${candidate/#\~/$HOME}"
        if [ -f "$path/SOUL.md" ] || [ -f "$path/AGENTS.md" ]; then
            echo "$path"
            return 0
        fi
    done
    return 1
}

echo "========================================"
echo "🔄 OpenClaw Sync Bridge v2.0 安装"
echo "========================================"
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null; then
    if command -v python &> /dev/null; then
        PYTHON_CMD="python"
    else
        echo "❌ 未找到 Python，请先安装 Python 3.7+"
        echo "   下载地址: https://python.org/downloads"
        exit 1
    fi
else
    PYTHON_CMD="python3"
fi

echo "✅ Python 已找到: $PYTHON_CMD"
$PYTHON_CMD --version

# 自动寻找工作目录
echo ""
echo "🔍 寻找 OpenClaw 工作目录..."
WORKSPACE=$(find_workspace)

if [ -n "$WORKSPACE" ]; then
    echo "✅ 找到工作目录: $WORKSPACE"
    read -p "是否使用此目录? [Y/n]: " confirm
    if [[ $confirm =~ ^[Nn]$ ]]; then
        WORKSPACE=""
    fi
fi

if [ -z "$WORKSPACE" ]; then
    read -p "请输入 OpenClaw 工作目录: " WORKSPACE
fi

WORKSPACE="${WORKSPACE/#\~/$HOME}"
SKILL_DIR="$WORKSPACE/skills/$SKILL_NAME"

# 创建目录
echo ""
echo "📁 安装到: $SKILL_DIR"
mkdir -p "$SKILL_DIR"

# 复制文件
cp "$SCRIPT_DIR/sync_bridge.py" "$SKILL_DIR/"
cp "$SCRIPT_DIR/SKILL.md" "$SKILL_DIR/" 2>/dev/null || true
cp "$SCRIPT_DIR/README.md" "$SKILL_DIR/" 2>/dev/null || true

echo "✅ 文件复制完成"

# 创建快捷命令
echo ""
echo "🔗 创建快捷命令..."

# 添加到 shell 配置
add_alias() {
    local shell_rc="$1"
    local alias_cmd="alias sync-bridge='cd \"$SKILL_DIR\" && $PYTHON_CMD sync_bridge.py'"
    
    if [ -f "$shell_rc" ]; then
        if ! grep -q "alias sync-bridge" "$shell_rc" 2>/dev/null; then
            echo "" >> "$shell_rc"
            echo "# OpenClaw Sync Bridge" >> "$shell_rc"
            echo "$alias_cmd" >> "$shell_rc"
            echo "✅ 已添加快捷命令到 $(basename $shell_rc)"
        fi
    fi
}

add_alias "$HOME/.bashrc"
add_alias "$HOME/.zshrc"

# 创建全局脚本（可选）
GLOBAL_BIN="$HOME/.local/bin"
if [ -d "$GLOBAL_BIN" ] || mkdir -p "$GLOBAL_BIN" 2>/dev/null; then
    cat > "$GLOBAL_BIN/sync-bridge" << EOF
#!/bin/bash
cd "$SKILL_DIR" && $PYTHON_CMD sync_bridge.py "\$@"
EOF
    chmod +x "$GLOBAL_BIN/sync-bridge"
    echo "✅ 全局命令已创建: sync-bridge"
    
    # 检查 PATH
    if [[ ":$PATH:" != *":$GLOBAL_BIN:"* ]]; then
        echo "⚠️  请将 $GLOBAL_BIN 添加到 PATH"
    fi
fi

echo ""
echo "========================================"
echo "✅ 安装完成！"
echo "========================================"
echo ""
echo "📍 安装位置: $SKILL_DIR"
echo ""
echo "🚀 快速开始:"
echo "   cd $SKILL_DIR"
echo "   $PYTHON_CMD sync_bridge.py setup"
echo ""
echo "📖 常用命令:"
echo "   $PYTHON_CMD sync_bridge.py setup   # 交互式配置"
echo "   $PYTHON_CMD sync_bridge.py push    # 上传"
echo "   $PYTHON_CMD sync_bridge.py pull    # 下载"
echo "   $PYTHON_CMD sync_bridge.py diff    # 对比差异"
echo ""
echo "⚙️  GitHub Token 申请:"
echo "   https://github.com/settings/tokens"
echo "   (勾选 'gist' 权限)"
echo ""
echo "💡 提示: 重新打开终端或使用 'source ~/.bashrc' 使快捷命令生效"
echo ""

# 询问是否立即配置
read -p "是否立即运行配置向导? [Y/n]: " run_setup
if [[ ! $run_setup =~ ^[Nn]$ ]]; then
    cd "$SKILL_DIR" && $PYTHON_CMD sync_bridge.py setup
fi
