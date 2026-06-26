#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

echo "========================================"
echo " PPT Pro v9.6.0 -- 环境自检 & 依赖安装"
echo "========================================"

OK=0; WARN=0; FAIL=0

check_ok()   { echo "  ✓ $1"; OK=$((OK+1)); }
check_warn() { echo "  ⚠ $1"; WARN=$((WARN+1)); }
check_fail() { echo "  ✗ $1"; FAIL=$((FAIL+1)); }

echo ""
echo "[1/5] Python 环境"
if command -v python3 &>/dev/null; then
    PY_VER=$(python3 --version 2>&1)
    check_ok "Python3: $PY_VER"
else
    check_fail "Python3 未安装"
fi

echo ""
echo "[2/5] Python 依赖"
for pkg in pptx PIL lxml fontTools; do
    if python3 -c "import $pkg" 2>/dev/null; then
        check_ok "python: $pkg"
    else
        check_warn "python: $pkg 缺失，尝试安装..."
        pip install python-pptx Pillow lxml fonttools 2>/dev/null && check_ok "已安装 $pkg" || check_fail "$pkg 安装失败"
    fi
done

echo ""
echo "[3/5] 截图后端 (PNG 管线)"

SCREENSHOT_OK=0

if python3 -c "from playwright.sync_api import sync_playwright" 2>/dev/null; then
    PW_CHROMIUM=$(python3 -c "
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    path = p.chromium.executable_path
    print(path if path else 'none')
" 2>/dev/null || echo "error")

    if [ -f "$PW_CHROMIUM" ] 2>/dev/null; then
        check_ok "Playwright + Chromium: $PW_CHROMIUM"
        SCREENSHOT_OK=1
    else
        check_warn "Playwright 已安装但 Chromium 缺失"
        echo "        修复: playwright install chromium"
    fi
else
    check_warn "Playwright 未安装 (pip install playwright && playwright install chromium)"
fi

if command -v node &>/dev/null; then
    NODE_VER=$(node --version 2>&1)
    check_ok "Node.js: $NODE_VER"
    if node -e "require('puppeteer')" 2>/dev/null; then
        check_ok "Puppeteer 可用"
        SCREENSHOT_OK=1
    else
        check_warn "Puppeteer 未安装 (npm install puppeteer)"
    fi
else
    check_warn "Node.js 未安装 (截图后端备选)"
fi

if [ "$SCREENSHOT_OK" -eq 0 ]; then
    check_fail "无可用截图后端! PNG 管线将不可用"
    echo "        至少安装一种:"
    echo "          pip install playwright && playwright install chromium"
    echo "          npm install puppeteer"
fi

echo ""
echo "[4/5] 可编辑管线 (Puppeteer + python-pptx)"

EDIT_OK=0
if command -v node &>/dev/null; then
    NODE_VER_NUM=$(node -e "console.log(parseInt(process.version.slice(1)))" 2>/dev/null || echo "0")
    if [ "$NODE_VER_NUM" -ge 18 ] 2>/dev/null; then
        check_ok "Node.js >= 18: $(node --version)"
        if [ -d "$SCRIPT_DIR/node_modules/puppeteer" ]; then
            check_ok "puppeteer 已安装"
            if python3 -c "import pptx" 2>/dev/null; then
                check_ok "python-pptx 可用 (PPTX 组装)"
                EDIT_OK=1
            else
                check_warn "python-pptx 缺失 (pip install python-pptx)"
            fi
        else
            check_warn "puppeteer 未安装，尝试 npm install..."
            (cd "$SCRIPT_DIR" && npm install 2>/dev/null) && check_ok "依赖安装成功" && EDIT_OK=1 || check_warn "依赖安装失败 (cd scripts && npm install)"
        fi
    else
        check_warn "Node.js < 18 (需要 18+)，可编辑管线不可用"
    fi
else
    check_warn "Node.js 未安装，可编辑管线不可用"
fi

if [ "$EDIT_OK" -eq 0 ]; then
    check_warn "可编辑管线不可用，用户可选择 PNG 管线"
fi

echo ""
echo "[5/5] Skill 文件完整性"
REF_COUNT=$(find "$SKILL_DIR/references" -name "*.md" 2>/dev/null | wc -l)
SCRIPT_COUNT=$(find "$SKILL_DIR/scripts" -name "*.py" 2>/dev/null | wc -l)

if [ "$REF_COUNT" -ge 60 ]; then
    check_ok "References: $REF_COUNT 个 md 文件"
else
    check_warn "References: 仅 $REF_COUNT 个 md 文件 (预期 >= 60)"
fi

if [ "$SCRIPT_COUNT" -ge 6 ]; then
    check_ok "Scripts: $SCRIPT_COUNT 个 Python 脚本"
else
    check_warn "Scripts: 仅 $SCRIPT_COUNT 个 Python 脚本 (预期 >= 6)"
fi

if [ -f "$SKILL_DIR/SKILL.md" ]; then
    check_ok "SKILL.md 存在"
else
    check_fail "SKILL.md 缺失!"
fi

echo ""
echo "========================================"
echo " 结果: ✓ $OK 通过  ⚠ $WARN 警告  ✗ $FAIL 失败"
echo "========================================"

if [ "$FAIL" -gt 0 ]; then
    echo "请修复失败项后重试。"
    exit 1
else
    echo "环境就绪！"
    exit 0
fi
