#!/bin/bash
# check-dependencies.sh - 检查系统依赖

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
. "$SCRIPT_DIR/common.sh"

echo "=== 检查系统依赖 ==="

ERRORS=0
OS="$CURRENT_OS"

echo "✅ 操作系统：$OS"
case "$OS" in
    macOS)
        echo "   服务管理：LaunchAgent"
        ;;
    Linux)
        echo "   服务管理：systemd --user（如未启用则回退为手动模式）"
        ;;
    *)
        echo "   服务管理：手动模式"
        echo "   提示：Windows 目前以扫描/校验为主，创建与重启建议手动执行"
        ;;
esac

for cmd in jq curl; do
    if command -v "$cmd" >/dev/null 2>&1; then
        echo "✅ $cmd: 已安装"
    else
        echo "❌ $cmd: 未安装"
        ERRORS=$((ERRORS + 1))
    fi
done

for optional_cmd in lsof ss netstat; do
    if command -v "$optional_cmd" >/dev/null 2>&1; then
        echo "✅ $optional_cmd: 可用"
    fi
done

case "$OS" in
    macOS)
        for cmd in plutil launchctl; do
            if command -v "$cmd" >/dev/null 2>&1; then
                echo "✅ $cmd: 已安装"
            else
                echo "❌ $cmd: 未安装"
                ERRORS=$((ERRORS + 1))
            fi
        done
        ;;
    Linux)
        if command -v systemctl >/dev/null 2>&1; then
            echo "✅ systemctl: 已安装"
        else
            echo "⚠️  systemctl: 未找到，将使用手动模式"
        fi
        ;;
esac

if command -v node >/dev/null 2>&1; then
    NODE_PATH="$(command -v node)"
    echo "✅ Node.js: 已安装 ($NODE_PATH)"
else
    echo "❌ Node.js: 未安装"
    ERRORS=$((ERRORS + 1))
fi

if command -v openclaw >/dev/null 2>&1; then
    echo "✅ OpenClaw: 已安装"
else
    echo "⚠️  OpenClaw: 未找到命令（可能已安装但未在 PATH 中）"
fi

echo ""
if [ "$ERRORS" -eq 0 ]; then
    echo "🎉 所有关键依赖检查通过！"
else
    echo "⚠️  发现 $ERRORS 个关键问题"
    if ! command -v jq >/dev/null 2>&1; then
        echo "📝 安装 jq: macOS 用 brew install jq；Ubuntu/Debian 用 sudo apt install jq"
    fi
fi

exit "$ERRORS"
