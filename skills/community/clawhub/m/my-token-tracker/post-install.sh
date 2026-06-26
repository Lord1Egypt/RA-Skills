#!/bin/bash
# post-install.sh - TokenTracker Post Install Script
# Run this after copying the skill to install the hook

set -e

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OPENCLAW_DIR="${OPENCLAW_DIR:-$HOME/.openclaw}"
HOOKS_DIR="$OPENCLAW_DIR/hooks"

echo "=========================================="
echo "TokenTracker Post Install"
echo "=========================================="

# 检查 skill 目录
if [ ! -d "$SKILL_DIR/hooks" ]; then
    echo "Error: hooks directory not found in $SKILL_DIR"
    exit 1
fi

# 创建 hook 目录
echo "Creating hook directory..."
mkdir -p "$HOOKS_DIR/token-logger"

# 复制 hook 文件
echo "Installing hook files..."
cp "$SKILL_DIR/hooks/token-logger/HOOK.md" "$HOOKS_DIR/token-logger/"
cp "$SKILL_DIR/hooks/token-logger/handler.js" "$HOOKS_DIR/token-logger/"

echo "✓ Hook files copied to $HOOKS_DIR/token-logger"

# 检查数据目录
DATA_DIR="$OPENCLAW_DIR/workspace/skills/token-tracker"
mkdir -p "$DATA_DIR"
echo "✓ Data directory created: $DATA_DIR"

# 尝试启用 hook
echo ""
echo "Attempting to enable hook..."
if command -v openclaw &> /dev/null; then
    # 尝试使用 openclaw CLI 启用
    openclaw hooks list | grep -q "token-logger" && {
        openclaw hooks enable token-logger 2>/dev/null || true
        echo "✓ Hook enabled!"
    } || {
        echo "Note: Hook not found in openclaw hooks list"
        echo "Please run: openclaw hooks enable token-logger"
    }
else
    echo "Note: OpenClaw CLI not found in PATH"
    echo "Please enable hook manually after Gateway is running:"
    echo "  openclaw hooks enable token-logger"
fi

echo ""
echo "=========================================="
echo "Installation Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Restart Gateway: openclaw gateway restart"
echo "2. Check hook status: openclaw hooks list"
echo "3. Query token usage: python $SKILL_DIR/token_tracker.py today"
echo ""
