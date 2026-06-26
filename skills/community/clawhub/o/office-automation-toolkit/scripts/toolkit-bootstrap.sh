#!/bin/bash
# toolkit-bootstrap.sh — 办公自动化工具跨平台初始化
# 支持：macOS / Ubuntu-Debian / CentOS-RHEL / Windows WSL
# 用法：bash toolkit-bootstrap.sh [--check-only] [--yes]
#   --check-only  只检查不安装
#   --yes         跳过确认自动安装

set -e

# ============================================================
# 颜色输出
# ============================================================
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

info()  { echo -e "${BLUE}[INFO]${NC} $1"; }
ok()    { echo -e "${GREEN}[OK]${NC} $1"; }
warn()  { echo -e "${YELLOW}[WARN]${NC} $1"; }
fail()  { echo -e "${RED}[MISS]${NC} $1"; }

# ============================================================
# 参数解析
# ============================================================
CHECK_ONLY=false
AUTO_YES=false
for arg in "$@"; do
  case $arg in
    --check-only) CHECK_ONLY=true ;;
    --yes) AUTO_YES=true ;;
  esac
done

# ============================================================
# 检测操作系统
# ============================================================
detect_os() {
  if [[ -f /proc/version ]] && grep -qi microsoft /proc/version 2>/dev/null; then
    OS="wsl"
    PKG_MGR="apt"
  elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
    PKG_MGR="brew"
  elif [[ -f /etc/debian_version ]]; then
    OS="debian"
    PKG_MGR="apt"
  elif [[ -f /etc/redhat-release ]]; then
    OS="redhat"
    PKG_MGR="yum"
  else
    OS="unknown"
    PKG_MGR="unknown"
  fi
  info "操作系统: $OS (包管理器: $PKG_MGR)"
}

# ============================================================
# 工具定义（按类别）
# ============================================================

# 格式: "命令名|类别|重要性|pip包名|brew包名|apt包名|说明"
# 重要性: required / recommended / optional
TOOLS=(
  # === Python 办公文档 ===
  "python3|基础|required|—|python3|python3|Python3 运行时"
  "pip3|基础|required|—|—|python3-pip|Python 包管理器"
  "openpyxl|Excel|recommended|openpyxl|—|—|Excel 读写"
  "pandas|Excel|recommended|pandas|—|—|数据分析/透视表"
  "python-docx|Word|recommended|python-docx|—|—|Word 读写"
  "python-pptx|PPT|recommended|python-pptx|—|—|PPT 创建/编辑"
  "pypdf|PDF|recommended|pypdf|—|—|PDF 合并/拆分"
  "pymupdf|PDF|recommended|pymupdf|—|—|PDF 文字/表格提取"
  "pdfplumber|PDF|optional|pdfplumber|—|—|PDF 精确表格提取"
  "reportlab|PDF|optional|reportlab|—|—|PDF 生成"
  "markitdown|通用|recommended|markitdown|—|—|Office 全格式→Markdown"

  # === 浏览器自动化 ===
  "playwright|浏览器|recommended|playwright|—|—|无头浏览器自动化"

  # === WPS 本地自动化 ===
  "pywpsrpc|WPS|optional|pywpsrpc|—|—|WPS 本地 Python 接口（需已装 WPS）"

  # === 网络/抓取 ===
  "httpx|网络|recommended|httpx|—|—|异步 HTTP 客户端"
  "requests|网络|recommended|requests|—|—|HTTP 请求库"
  "beautifulsoup4|抓取|recommended|beautifulsoup4|—|—|HTML 解析"

  # === 数据处理 CLI ===
  "jq|数据|required|—|jq|jq|JSON 处理 CLI"
  "csvkit|数据|optional|csvkit|—|—|CSV CLI 工具集"

  # === 系统 CLI 工具 ===
  "pandoc|文档|optional|—|pandoc|pandoc|万能格式转换"
  "ffmpeg|媒体|optional|—|ffmpeg|ffmpeg|音视频处理"
  "tesseract|OCR|optional|—|tesseract|tesseract|OCR 文字识别"
  "git|基础|required|—|git|git|版本控制"
  "curl|网络|required|—|curl|curl|HTTP 命令行工具"
)

# ============================================================
# 检查函数
# ============================================================

check_command() {
  command -v "$1" &>/dev/null
}

check_python_module() {
  python3 -c "import $1" 2>/dev/null
}

# ============================================================
# 安装函数
# ============================================================

install_pip() {
  local pkg="$1"
  info "pip3 install $pkg"
  if [[ "$AUTO_YES" == true ]]; then
    pip3 install --quiet "$pkg" 2>/dev/null || pip install --quiet "$pkg" 2>/dev/null
  else
    pip3 install "$pkg" 2>/dev/null || pip install "$pkg" 2>/dev/null
  fi
}

install_brew() {
  local pkg="$1"
  if ! command -v brew &>/dev/null; then
    warn "Homebrew 未安装，跳过 $pkg"
    return 1
  fi
  info "brew install $pkg"
  if [[ "$AUTO_YES" == true ]]; then
    brew install --quiet "$pkg" 2>/dev/null
  else
    brew install "$pkg" 2>/dev/null
  fi
}

install_apt() {
  local pkg="$1"
  info "apt install $pkg"
  if [[ "$AUTO_YES" == true ]]; then
    sudo apt-get install -y -qq "$pkg" 2>/dev/null
  else
    sudo apt-get install -y "$pkg" 2>/dev/null
  fi
}

install_yum() {
  local pkg="$1"
  info "yum install $pkg"
  if [[ "$AUTO_YES" == true ]]; then
    sudo yum install -y -q "$pkg" 2>/dev/null
  else
    sudo yum install -y "$pkg" 2>/dev/null
  fi
}

install_tool() {
  local cmd="$1" category="$2" importance="$3" pip_pkg="$4" brew_pkg="$5" apt_pkg="$6" desc="$7"

  # 检查是否已安装
  if [[ "$pip_pkg" != "—" ]]; then
    local module_name="$pip_pkg"
    # 特殊映射
    case "$pip_pkg" in
      beautifulsoup4) module_name="bs4" ;;
      python-docx) module_name="docx" ;;
      python-pptx) module_name="pptx" ;;
      lark-oapi) module_name="lark_oapi" ;;
      pymupdf) module_name="fitz" ;;
    esac
    if check_python_module "$module_name"; then
      ok "$desc ($cmd)"
      return 0
    fi
  fi

  if check_command "$cmd"; then
    ok "$desc ($cmd)"
    return 0
  fi

  # 未安装
  fail "$desc ($cmd) [$importance]"

  if [[ "$CHECK_ONLY" == true ]]; then
    return 0
  fi

  # 安装
  if [[ "$pip_pkg" != "—" ]]; then
    install_pip "$pip_pkg"
  elif [[ "$PKG_MGR" == "brew" && "$brew_pkg" != "—" ]]; then
    install_brew "$brew_pkg"
  elif [[ "$PKG_MGR" == "apt" && "$apt_pkg" != "—" ]]; then
    install_apt "$apt_pkg"
  elif [[ "$PKG_MGR" == "yum" && "$apt_pkg" != "—" ]]; then
    install_yum "$apt_pkg"
  else
    warn "无法自动安装 $cmd，请手动安装"
    return 1
  fi
}

# ============================================================
# 主流程
# ============================================================

echo ""
echo "========================================="
echo "  办公自动化工具 · 环境初始化"
echo "========================================="
echo ""

detect_os

if [[ "$CHECK_ONLY" == true ]]; then
  info "模式：仅检查（不安装）"
else
  info "模式：检查并安装缺失工具"
fi
echo ""

# 统计
TOTAL=0
INSTALLED=0
MISSING_REQUIRED=0
MISSING_RECOMMENDED=0
MISSING_OPTIONAL=0

for entry in "${TOOLS[@]}"; do
  IFS='|' read -r cmd category importance pip_pkg brew_pkg apt_pkg desc <<< "$entry"
  TOTAL=$((TOTAL + 1))

  if install_tool "$cmd" "$category" "$importance" "$pip_pkg" "$brew_pkg" "$apt_pkg" "$desc"; then
    INSTALLED=$((INSTALLED + 1))
  else
    case "$importance" in
      required)    MISSING_REQUIRED=$((MISSING_REQUIRED + 1)) ;;
      recommended) MISSING_RECOMMENDED=$((MISSING_RECOMMENDED + 1)) ;;
      optional)    MISSING_OPTIONAL=$((MISSING_OPTIONAL + 1)) ;;
    esac
  fi
done

# Playwright 浏览器二进制
if check_python_module "playwright" && ! python3 -c "from playwright.sync_api import sync_playwright; p=sync_playwright().start(); p.chromium" 2>/dev/null; then
  warn "Playwright 已安装但 Chromium 浏览器未下载"
  if [[ "$CHECK_ONLY" == false ]]; then
    info "正在下载 Chromium..."
    playwright install chromium 2>/dev/null || warn "Chromium 下载失败，请手动运行: playwright install chromium"
  fi
fi

# ============================================================
# 汇总报告
# ============================================================
echo ""
echo "========================================="
echo "  检查报告"
echo "========================================="
echo ""
echo "  操作系统:     $OS"
echo "  总工具数:     $TOTAL"
echo "  已就绪:       $INSTALLED"
echo "  缺失(必须):   $MISSING_REQUIRED"
echo "  缺失(推荐):   $MISSING_RECOMMENDED"
echo "  缺失(可选):   $MISSING_OPTIONAL"
echo ""

if [[ $MISSING_REQUIRED -gt 0 ]]; then
  fail "有 $MISSING_REQUIRED 个必须工具缺失，部分功能将无法使用"
fi

if [[ $MISSING_RECOMMENDED -gt 0 && "$CHECK_ONLY" == true ]]; then
  warn "有 $MISSING_RECOMMENDED 个推荐工具缺失，建议安装以获得完整功能"
fi

if [[ $MISSING_REQUIRED -eq 0 && $MISSING_RECOMMENDED -eq 0 ]]; then
  ok "所有必须和推荐工具已就绪！"
fi

# ============================================================
# 通信平台检测与配置
# ============================================================
echo ""
echo "========================================="
echo "  通信平台检测"
echo "========================================="
echo ""

PLATFORM_DETECTED=false

if [[ -n "$FEISHU_APP_ID" ]]; then
  ok "检测到飞书环境（App ID: $FEISHU_APP_ID）"
  if command -v lark-cli &>/dev/null; then
    info "正在绑定 lark-cli..."
    echo "" | lark-cli config bind --source hermes --identity bot-only 2>/dev/null && ok "lark-cli 已绑定到 Hermes 飞书凭证" || warn "lark-cli 绑定失败，请手动运行: lark-cli config bind --source hermes"
  else
    warn "lark-cli 未安装，飞书自动化不可用"
  fi
  PLATFORM_DETECTED=true
fi

if [[ -n "$WECOM_CORP_ID" ]]; then
  ok "检测到企业微信环境（Corp ID: $WECOM_CORP_ID）"
  PLATFORM_DETECTED=true
fi

if [[ -n "$DINGTALK_APP_KEY" ]]; then
  ok "检测到钉钉环境"
  PLATFORM_DETECTED=true
fi

if [[ "$PLATFORM_DETECTED" == false ]]; then
  warn "未检测到通信平台凭证（飞书/企业微信/钉钉）"
  warn "消息类功能需手动配置环境变量"
fi

echo ""
echo "========================================="
if [[ "$CHECK_ONLY" == true ]]; then
  info "如需自动安装，请运行: bash toolkit-bootstrap.sh --yes"
fi
echo "========================================="
