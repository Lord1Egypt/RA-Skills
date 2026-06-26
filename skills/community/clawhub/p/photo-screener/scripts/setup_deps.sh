#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────
# photo-screener — Dependency Check & Install
# Uses MobileCLIP2-S0 via open_clip with HuggingFace mirror
# ─────────────────────────────────────────────────────────────
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
REQUIREMENTS="$SKILL_DIR/requirements.txt"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  📦 photo-screener — 依赖检查"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

MISSING_PY=()
ALL_OK=true

# ── 1. Check Python dependencies ───────────────────────────
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

check_python_pkg "torch" "torch"
check_python_pkg "open_clip" "open-clip-torch"
check_python_pkg "PIL" "pillow"
check_python_pkg "numpy" "numpy"

# ── 2. Install missing Python deps ─────────────────────────
if [ ${#MISSING_PY[@]} -gt 0 ]; then
    echo ""
    echo -e "${YELLOW}⚠️  缺少 Python 依赖：${NC}"
    for pkg in "${MISSING_PY[@]}"; do
        echo "    - $pkg"
    done
    echo ""
    echo "  安装命令: pip3 install ${MISSING_PY[*]}"
    echo ""
    read -r -p "是否立即安装？[Y/n] " answer
    answer=${answer:-Y}
    if [[ "$answer" =~ ^[Yy]$ ]]; then
        echo ""
        echo "📦 安装 Python 依赖..."
        pip3 install "${MISSING_PY[@]}"
        echo -e "${GREEN}✓ Python 依赖安装完成${NC}"
    else
        echo "跳过安装。请手动安装后重试。"
        exit 1
    fi
fi

# ── 3. Check MobileCLIP2-S0 model ──────────────────────────
echo ""
echo "🔍 检查 MobileCLIP2-S0 模型..."

MODEL_READY=$(python3 -c "
import sys
try:
    import open_clip
    # Check if model weights are cached
    import os, hashlib
    cache_dir = os.path.expanduser('~/.cache/open_clip')
    # Try to find cached model files
    if os.path.isdir(cache_dir):
        for f in os.listdir(cache_dir):
            if 'mobileclip' in f.lower() and 's0' in f.lower():
                print('yes')
                sys.exit(0)
    # Also check HuggingFace cache
    hf_cache = os.path.expanduser('~/.cache/huggingface/hub')
    if os.path.isdir(hf_cache):
        for d in os.listdir(hf_cache):
            if 'mobileclip' in d.lower():
                print('yes')
                sys.exit(0)
    print('no')
except Exception:
    print('no')
" 2>/dev/null || echo "no")

if [ "$MODEL_READY" = "yes" ]; then
    echo -e "  ${GREEN}✓${NC} MobileCLIP2-S0 模型已缓存"
else
    echo -e "  ${CYAN}ℹ${NC} MobileCLIP2-S0 模型未下载"
    echo ""
    echo "  模型将在首次运行 screen.py 时自动下载。"
    echo "  下载使用国内镜像加速 (hf-mirror.com)，约需下载 ~300MB。"
    echo ""
    read -r -p "是否现在预下载模型？[y/N] " answer
    answer=${answer:-N}
    if [[ "$answer" =~ ^[Yy]$ ]]; then
        echo ""
        echo "📥 使用国内镜像下载 MobileCLIP2-S0 模型..."
        echo "   镜像源: https://hf-mirror.com"
        echo ""
        HF_ENDPOINT=https://hf-mirror.com python3 -c "
import open_clip
print('正在下载 MobileCLIP2-S0 模型...')
model, _, preprocess = open_clip.create_model_and_transforms(
    'MobileCLIP2-S0', pretrained='dfndr2b'
)
print('✅ 模型下载完成！')
"
    else
        echo "  跳过。首次运行脚本时会自动提示下载。"
    fi
fi

# ── 4. Check aesthetic model weights ────────────────────────
echo ""
echo "🔍 检查美学评分模型..."
AESTHETIC_PATH="$HOME/.cache/photo-filter/aesthetic_sac_logos_ava1_l14_linearMSE.pth"
AESTHETIC_URL="https://github.com/christophschuhmann/improved-aesthetic-predictor/raw/main/sac+logos+ava1-l14-linearMSE.pth"

if [ -f "$AESTHETIC_PATH" ]; then
    SIZE_KB=$(($(stat -f%z "$AESTHETIC_PATH" 2>/dev/null || stat -c%s "$AESTHETIC_PATH" 2>/dev/null || echo 0) / 1024))
    echo -e "  ${GREEN}✓${NC} 美学评分权重 (${SIZE_KB}KB)"
else
    echo -e "  ${CYAN}ℹ${NC} 美学评分权重未下载 (~3MB)"
    echo ""
    read -r -p "是否现在下载美学评分模型？[Y/n] " answer
    answer=${answer:-Y}
    if [[ "$answer" =~ ^[Yy]$ ]]; then
        echo ""
        echo "📥 下载美学评分模型..."
        mkdir -p "$HOME/.cache/photo-filter"
        TEMP_PATH="${AESTHETIC_PATH}.downloading"

        # Support resume via curl -C (auto-resume)
        if command -v curl &>/dev/null; then
            curl -L -# -C - -o "$TEMP_PATH" "$AESTHETIC_URL"
        elif command -v wget &>/dev/null; then
            wget -c --show-progress -O "$TEMP_PATH" "$AESTHETIC_URL"
        else
            echo -e "  ${RED}✗${NC} 未找到 curl 或 wget，无法下载"
            echo "  请手动下载: $AESTHETIC_URL"
            echo "  保存到: $AESTHETIC_PATH"
            TEMP_PATH=""
        fi

        if [ -n "$TEMP_PATH" ] && [ -f "$TEMP_PATH" ]; then
            mv "$TEMP_PATH" "$AESTHETIC_PATH"
            SIZE_KB=$(($(stat -f%z "$AESTHETIC_PATH" 2>/dev/null || stat -c%s "$AESTHETIC_PATH" 2>/dev/null || echo 0) / 1024))
            echo -e "  ${GREEN}✓${NC} 美学评分权重已下载 (${SIZE_KB}KB)"
        fi
    else
        echo "  跳过。首次运行脚本时会自动下载。"
    fi
fi

# ── 5. Summary ──────────────────────────────────────────────
echo ""
echo -e "${GREEN}✅ 依赖检查完成！${NC}"
echo ""
echo "使用方法:"
echo "  python3 $SKILL_DIR/scripts/screen.py <thumbnails_dir>"
