#!/usr/bin/env bash
# pdf-master 一键环境安装（幂等，可重复执行）
# 用法：
#   bash setup.sh              # 安装核心依赖（覆盖脚本化能力 #1-#15/#20/#25）
#   bash setup.sh --with-ocr   # 追加 OCR 引擎（tesseract + 中文包 + pytesseract）
#   bash setup.sh --with-office# 追加 LibreOffice（复杂版面转换降级管道）
#   bash setup.sh --with-paddle# 追加 PaddleOCR（中文识别 SOTA，体积较大）
#   bash setup.sh --all        # 全部安装
#   bash setup.sh --check      # 不安装，仅输出能力就绪矩阵
set -u
cd "$(dirname "$0")"

WITH_OCR=0; WITH_OFFICE=0; WITH_PADDLE=0; CHECK_ONLY=0
for arg in "$@"; do
  case "$arg" in
    --with-ocr)    WITH_OCR=1 ;;
    --with-office) WITH_OFFICE=1 ;;
    --with-paddle) WITH_PADDLE=1 ;;
    --all)         WITH_OCR=1; WITH_OFFICE=1; WITH_PADDLE=1 ;;
    --check)       CHECK_ONLY=1 ;;
    -h|--help)     sed -n '2,10p' "$0"; exit 0 ;;
    *) echo "未知参数：$arg（-h 查看用法）"; exit 1 ;;
  esac
done

say() { printf '%s\n' "$*"; }

if [ "$CHECK_ONLY" -eq 1 ]; then
  exec python3 scripts/check_env.py
fi

# ---- 0. python3 检测 ----
if ! command -v python3 >/dev/null 2>&1; then
  say "❌ 未找到 python3，请先安装 Python 3.10+ 后重试"; exit 1
fi
say "✔ python3：$(python3 --version 2>&1)"

PIP() {  # pip 安装，权限不足时自动回退 --user
  python3 -m pip install "$@" 2>/dev/null || python3 -m pip install --user "$@"
}

# ---- 1. 核心 Python 依赖 ----
say "▶ 安装核心依赖（requirements.txt）…"
if PIP -r requirements.txt; then
  say "✔ 核心依赖就绪"
else
  say "❌ 核心依赖安装失败，请检查网络/pip 源后重试"; exit 1
fi

# ---- 2. 系统包安装器探测 ----
SUDO=""; [ "$(id -u)" -ne 0 ] && command -v sudo >/dev/null 2>&1 && SUDO="sudo"
sys_install() {  # sys_install <apt包名> <brew包名> <yum包名>
  if command -v apt-get >/dev/null 2>&1; then $SUDO apt-get install -y "$1"
  elif command -v brew >/dev/null 2>&1;   then brew install "$2"
  elif command -v yum >/dev/null 2>&1;    then $SUDO yum install -y "$3"
  else say "⚠️ 未识别的包管理器，请手动安装：$1"; return 1; fi
}

# ---- 3. OCR（可选） ----
if [ "$WITH_OCR" -eq 1 ]; then
  say "▶ 安装 OCR 引擎…"
  command -v tesseract >/dev/null 2>&1 || sys_install tesseract-ocr tesseract tesseract
  # 中文语言包（Linux 独立包；brew 版已内置多语言）
  if command -v apt-get >/dev/null 2>&1 && ! tesseract --list-langs 2>/dev/null | grep -q chi_sim; then
    $SUDO apt-get install -y tesseract-ocr-chi-sim || true
  fi
  PIP pytesseract Pillow && say "✔ OCR 就绪（引擎降级链：PaddleOCR → Tesseract）"
fi

# ---- 4. LibreOffice（可选） ----
if [ "$WITH_OFFICE" -eq 1 ]; then
  say "▶ 安装 LibreOffice…"
  command -v libreoffice >/dev/null 2>&1 || command -v soffice >/dev/null 2>&1 \
    || sys_install libreoffice libreoffice libreoffice
  PIP pdf2docx && say "✔ Office 转换管道就绪"
fi

# ---- 5. PaddleOCR（可选，大体积） ----
if [ "$WITH_PADDLE" -eq 1 ]; then
  say "▶ 安装 PaddleOCR（约 500MB，耐心等候）…"
  PIP paddlepaddle paddleocr && say "✔ PaddleOCR 就绪"
fi

# ---- 6. 自检 ----
say ""
python3 scripts/check_env.py
