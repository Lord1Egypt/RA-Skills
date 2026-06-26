#!/bin/bash
# OpenClaw Gateway Restart Script
# 一键重启 Gateway

OPENCLAW_BIN="$HOME/.nvm/versions/node/v24.14.0/bin/openclaw"

echo "🔄 正在重启 OpenClaw Gateway..."

$OPENCLAW_BIN gateway restart

echo ""
echo "✅ 重启完成！"
