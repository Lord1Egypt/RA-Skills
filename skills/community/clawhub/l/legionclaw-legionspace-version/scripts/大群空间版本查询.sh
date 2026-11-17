#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────────
# LegionSpace 大群空间版本查询 - 入口脚本 (Linux/macOS)
# 自动检测 Python、安装依赖、运行版本查询
# ──────────────────────────────────────────────────────────────

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PY_SCRIPT="$SCRIPT_DIR/legionspace_version_checker.py"

echo "================================================"
echo "  LegionSpace 大群空间版本查询"
echo "================================================"
echo ""

# ── 1. 检测 Python ──────────────────────────────────────────
PYTHON=""
for cmd in python3 python; do
    if command -v "$cmd" &>/dev/null; then
        PYTHON="$cmd"
        break
    fi
done

if [ -z "$PYTHON" ]; then
    echo "[ERROR] 未找到 Python，请安装 Python 3.x"
    exit 1
fi
echo "[OK] Python: $PYTHON ($($PYTHON --version 2>&1))"

# ── 2. 检查并安装依赖 ──────────────────────────────────────
echo "[*] 检查依赖 ..."

# requests
if ! $PYTHON -c "import requests" 2>/dev/null; then
    echo "[*] 安装 requests ..."
    $PYTHON -m pip install requests --quiet
fi
echo "[OK] requests"

# playwright
if ! $PYTHON -c "from playwright.sync_api import sync_playwright" 2>/dev/null; then
    echo "[*] 安装 playwright ..."
    $PYTHON -m pip install playwright --quiet
    echo "[*] 安装 Chromium (playwright) ..."
    $PYTHON -m playwright install chromium --with-deps 2>/dev/null || \
    $PYTHON -m playwright install chromium 2>/dev/null
fi
echo "[OK] playwright + Chromium"
echo ""

# ── 3. 运行版本查询 ────────────────────────────────────────
export no_proxy="*"
export NO_PROXY="*"

$PYTHON "$PY_SCRIPT"
