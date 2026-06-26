#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────
# photo-grader — Dependency Check & Install
#
# Engine: RawTherapee CLI (rawtherapee-cli)
#
# macOS note: always verify with rawtherapee-cli -h. If it exits with
# 133 / SIGTRAP, macOS likely blocked it before startup. This is common when
# an agent installs RawTherapee via Homebrew and the user has not explicitly
# opened/authorized the app or CLI yet. A user-installed and authorized
# Homebrew CLI can work; otherwise use the official standalone CLI.
# ─────────────────────────────────────────────────────────────
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BOLD='\033[1m'
NC='\033[0m'

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  📦 photo-grader — 依赖检查"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

ALL_OK=true
HAS_RT=false

# ── Check RawTherapee CLI ─────────────────────────────────────
echo -e "${BOLD}检查 RawTherapee CLI...${NC}"
echo ""

if command -v rawtherapee-cli &>/dev/null; then
    RT_PATH=$(command -v rawtherapee-cli)
    set +e
    RT_HELP_OUTPUT=$("$RT_PATH" -h 2>&1)
    RT_RC=$?
    set -e

    if echo "$RT_HELP_OUTPUT" | grep -qi "RawTherapee, version" && echo "$RT_HELP_OUTPUT" | grep -qi "command line"; then
        RT_VER=$(echo "$RT_HELP_OUTPUT" | head -1)
        echo -e "  ${GREEN}✓${NC} rawtherapee-cli ($RT_VER)"
        HAS_RT=true
    else
        echo -e "  ${RED}✗${NC} rawtherapee-cli 找到但不可用: $RT_PATH"
        if [[ "$RT_RC" == "133" ]] || echo "$RT_HELP_OUTPUT" | grep -Eiq "SIGTRAP|trace trap"; then
            echo "       原因: exit 133 / SIGTRAP，常见于 macOS CLI 包签名或公证异常"
        elif [[ "$RT_RC" == "132" ]] || echo "$RT_HELP_OUTPUT" | grep -Eiq "SIGILL|illegal instruction"; then
            echo "       原因: exit 132 / SIGILL，可能是 CLI 构建与当前 CPU/系统不兼容"
        else
            echo "       原因: rawtherapee-cli -h 未输出有效命令行帮助（exit=$RT_RC）"
            echo "$RT_HELP_OUTPUT" | tail -3 | sed 's/^/       /'
        fi
        echo "       请安装官网包中的独立 rawtherapee-cli，并确认: rawtherapee-cli -h"
        ALL_OK=false
    fi
elif command -v rawtherapee &>/dev/null; then
    RT_PATH=$(command -v rawtherapee)
    echo -e "  ${YELLOW}⚠${NC} 找到 rawtherapee GUI ($RT_PATH)，但未找到 rawtherapee-cli"
    echo -e "       确认 rawtherapee-cli 已放入 PATH；macOS 下 Homebrew 安装后可能需要用户手动打开/授权"
    ALL_OK=false
else
    echo -e "  ${RED}✗${NC} rawtherapee-cli — 未安装（必须安装）"
    echo "       macOS: 可用 Homebrew（需用户手动打开/授权）或官网独立 rawtherapee-cli，并放入 PATH"
    echo "       Debian/Ubuntu: sudo apt install rawtherapee-cli"
    echo "       Fedora/RHEL: sudo dnf install RawTherapee"
    echo "       验证: rawtherapee-cli -h"
    ALL_OK=false
fi

# ── Check tomli (Python < 3.11) ───────────────────────────────
echo ""
echo -e "${BOLD}检查 Python 依赖...${NC}"
echo ""

PY_VER=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')" 2>/dev/null || echo "?")
if python3 -c "import tomllib" 2>/dev/null; then
    echo -e "  ${GREEN}✓${NC} tomllib (Python $PY_VER stdlib)"
elif python3 -c "import tomli" 2>/dev/null; then
    echo -e "  ${GREEN}✓${NC} tomli (Python $PY_VER)"
else
    echo -e "  ${YELLOW}⚠${NC} tomli — 未安装（Python < 3.11 需要）"
    echo "       安装中..."
    pip3 install tomli && echo -e "  ${GREEN}✓${NC} tomli 安装完成" || {
        echo -e "  ${RED}✗${NC} tomli 安装失败，请手动运行: pip3 install tomli"
        ALL_OK=false
    }
fi

# ── Summary ──────────────────────────────────────────────────
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if $HAS_RT; then
    echo -e "  ${GREEN}✅ 引擎就绪：RawTherapee CLI${NC}"
else
    echo -e "  ${RED}❌ 引擎不可用：请安装 rawtherapee-cli${NC}"
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if $ALL_OK; then
    exit 0
fi

# ── Install prompt ───────────────────────────────────────────
echo ""
echo -e "${YELLOW}缺少 rawtherapee-cli，请手动安装：${NC}"
echo ""
if [[ "$(uname)" == "Darwin" ]]; then
    echo "  可用 Homebrew（需用户手动打开/授权）或官网独立 rawtherapee-cli，并放入 PATH"
    echo "  安装后验证: rawtherapee-cli -h"
elif command -v dnf &>/dev/null; then
    echo "  sudo dnf install -y RawTherapee"
else
    echo "  sudo apt-get install -y rawtherapee-cli"
fi
echo ""

exit 1
