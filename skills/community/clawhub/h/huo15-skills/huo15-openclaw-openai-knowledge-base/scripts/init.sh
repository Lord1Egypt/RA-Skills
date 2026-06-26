#!/bin/bash
# init.sh — 已弃用，请使用 activate.sh（Agent 隔离架构）
# 保留此脚本以兼容旧版工作流

echo "⚠️  init.sh 已弃用，自动转发到 activate.sh（Agent 隔离架构）"
echo ""

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
exec "$SCRIPT_DIR/activate.sh" "$@"
