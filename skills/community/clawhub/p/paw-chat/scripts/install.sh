#!/usr/bin/env bash
# Paw Chat 安装脚本
# 将 Paw 安装到 OpenClaw Gateway 的 control-ui-static 目录

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ASSETS_DIR="$SCRIPT_DIR/../assets"

# 获取 OpenClaw 配置目录
if [ -n "$OPENCLAW_HOME" ]; then
    OPENCLAW_DIR="$OPENCLAW_HOME"
elif [ -d "$HOME/.openclaw" ]; then
    OPENCLAW_DIR="$HOME/.openclaw"
else
    echo "❌ 未找到 OpenClaw 配置目录"
    echo "请确保 OpenClaw 已安装，或设置 OPENCLAW_HOME 环境变量"
    exit 1
fi

# 获取 control-ui-static 目录
UIROOT="$OPENCLAW_DIR/control-ui-static"

# 如果目录不存在，尝试从配置获取
if [ ! -d "$UIROOT" ]; then
    echo "📁 创建 control-ui-static 目录..."
    mkdir -p "$UIROOT"
fi

echo "🐾 安装 Paw Chat 到 $UIROOT"
echo ""

# 复制文件
cp "$ASSETS_DIR/index.html" "$UIROOT/chat.html"
cp "$ASSETS_DIR/paw-app.js" "$UIROOT/"
cp "$ASSETS_DIR/marked.min.js" "$UIROOT/"
cp "$ASSETS_DIR/highlight.min.js" "$UIROOT/"
cp "$ASSETS_DIR/github-dark.min.css" "$UIROOT/"
cp "$ASSETS_DIR/logo.jpg" "$UIROOT/"

echo "✅ 安装完成！"
echo ""
echo "访问地址:"
echo "  - 本地: http://localhost:<gateway-port>/chat.html"
echo "  - 远程: https://<your-domain>/<basePath>/chat.html"
echo ""
echo "启动本地服务器:"
echo "  cd \"$ASSETS_DIR\" && ./start.sh"
