#!/usr/bin/env bash
# MemCore 一键安装脚本
# 安装到 ~/.openclaw/workspace/scripts/memcore/
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
WS="${HOME}/.openclaw/workspace"
TARGET="${WS}/scripts/memcore"

echo "🧠 MemCore 安装"
echo "   源: ${SKILL_DIR}/scripts/memcore"
echo "   目标: ${TARGET}"

# 1. 创建目标目录
mkdir -p "${TARGET}"

# 2. 复制所有模块
cp "${SKILL_DIR}/scripts/memcore/"*.py "${TARGET}/"

# 3. 首次索引（如果 memory 目录存在）
MEMORY_DIR="${WS}/memory"
if [ -d "${MEMORY_DIR}" ]; then
    echo ""
    echo "📂 检测到已有 memory/ 目录，开始首次索引..."
    cd "${WS}" && python3 -c "
import sys; sys.path.insert(0, '${WS}')
from scripts.memcore.cli import cmd_index, cmd_induce, cmd_feedback, cmd_brief
import argparse
class Args: pass
args = Args()
cmd_index(args)
print()
cmd_induce(args)
print()
cmd_feedback(args)
print()
cmd_brief(args)
" 2>&1 || echo "⚠️ 首次索引失败（可手动运行: python3 scripts/memcore/cli.py run-all）"
fi

echo ""
echo "✅ MemCore 安装完成"
echo ""
echo "📋 下一步："
echo "  1. 手动运行: python3 ~/.openclaw/workspace/scripts/memcore/cli.py stats"
echo "  2. 添加 cron 定时维护（参考 references/cron-setup.md）"
echo "  3. 修改 AGENTS.md 启动流程（参考 references/upgrade-guide.md）"
