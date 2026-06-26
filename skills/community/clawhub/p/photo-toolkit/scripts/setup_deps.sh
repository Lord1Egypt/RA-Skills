#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────
# photo-toolkit — Dependency Check & Install
# ─────────────────────────────────────────────────────────────
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
REQUIREMENTS="$SKILL_DIR/requirements.txt"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  📦 photo-toolkit — 依赖检查"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

MISSING_SYS=()
MISSING_PY=()
ALL_OK=true

# ── 1. Check system dependency: libraw ──────────────────────
echo "🔍 检查系统依赖..."
if [ -f /usr/lib/libraw.so ] || [ -f /usr/lib64/libraw.so ] || [ -f /usr/lib/x86_64-linux-gnu/libraw.so ] || ldconfig -p 2>/dev/null | grep -q libraw; then
    echo -e "  ${GREEN}✓${NC} libraw (system)"
elif command -v brew &>/dev/null && brew list libraw &>/dev/null 2>&1; then
    echo -e "  ${GREEN}✓${NC} libraw (Homebrew)"
else
    echo -e "  ${RED}✗${NC} libraw — 未安装"
    MISSING_SYS+=("libraw")
    ALL_OK=false
fi

if command -v ffmpeg &>/dev/null; then
    FFMPEG_VER=$(ffmpeg -version 2>&1 | head -1 | awk '{print $3}')
    echo -e "  ${GREEN}✓${NC} ffmpeg ($FFMPEG_VER)"
else
    echo -e "  ${YELLOW}ℹ${NC} ffmpeg — 未安装（assemble.py 需要，可选）"
fi

# ── 2. Check Python dependencies ───────────────────────────
echo ""
echo "🔍 检查 Python 依赖..."

check_python_pkg() {
    local import_name="$1"
    local pip_name="$2"
    if python3 -c "import $import_name" 2>/dev/null; then
        local ver
        ver=$(python3 -c "import $import_name; print(getattr($import_name, '__version__', getattr($import_name, 'VERSION', '?')))" 2>/dev/null || echo "?")
        echo -e "  ${GREEN}✓${NC} $pip_name ($ver)"
    else
        echo -e "  ${RED}✗${NC} $pip_name — 未安装"
        MISSING_PY+=("$pip_name")
        ALL_OK=false
    fi
}

check_python_pkg "rawpy" "rawpy"
check_python_pkg "PIL" "pillow"
check_python_pkg "numpy" "numpy"

# ── 3. Summary & Install ───────────────────────────────────
echo ""
if $ALL_OK; then
    echo -e "${GREEN}✅ 所有依赖已就绪！${NC}"
    exit 0
fi

echo -e "${YELLOW}⚠️  缺少以下依赖：${NC}"

if [ ${#MISSING_SYS[@]} -gt 0 ]; then
    echo ""
    echo "  系统依赖:"
    for pkg in "${MISSING_SYS[@]}"; do
        echo "    - $pkg"
    done
    echo ""
    if [[ "$(uname)" == "Darwin" ]]; then
        echo "  安装命令: brew install ${MISSING_SYS[*]}"
    elif command -v dnf &>/dev/null; then
        echo "  安装命令: sudo dnf install LibRaw-devel"
    elif command -v yum &>/dev/null; then
        echo "  安装命令: sudo yum install LibRaw-devel"
    else
        echo "  安装命令: sudo apt-get install ${MISSING_SYS[*]/%/-dev}"
    fi
fi

if [ ${#MISSING_PY[@]} -gt 0 ]; then
    echo ""
    echo "  Python 依赖:"
    for pkg in "${MISSING_PY[@]}"; do
        echo "    - $pkg"
    done
    echo ""
    echo "  安装命令: pip3 install ${MISSING_PY[*]}"
fi

echo ""
read -r -p "是否立即安装缺少的依赖？[Y/n] " answer
answer=${answer:-Y}

if [[ "$answer" =~ ^[Yy]$ ]]; then
    # Install system deps
    if [ ${#MISSING_SYS[@]} -gt 0 ]; then
        echo ""
        echo "📦 安装系统依赖..."
        if [[ "$(uname)" == "Darwin" ]]; then
            brew install "${MISSING_SYS[@]}"
        elif command -v dnf &>/dev/null; then
            sudo dnf install -y LibRaw-devel
        elif command -v yum &>/dev/null; then
            sudo yum install -y LibRaw-devel
        else
            sudo apt-get install -y "${MISSING_SYS[@]/%/-dev}"
        fi
    fi

    # Install Python deps
    if [ ${#MISSING_PY[@]} -gt 0 ]; then
        echo ""
        echo "📦 安装 Python 依赖..."
        pip3 install "${MISSING_PY[@]}"
    fi

    echo ""
    echo -e "${GREEN}✅ 安装完成！${NC}"
else
    echo ""
    echo "跳过安装。请手动安装后重试。"
    exit 1
fi
