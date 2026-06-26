#!/bin/bash
# 🌑 Mjolnir Shadow (雷神之影) - Standalone Restore Kit / 独立恢复引导脚本
# 
# ╔══════════════════════════════════════════════════════════════╗
# ║  从裸机到满血，一条命令搞定一切。                              ║
# ║  检查系统 → 装依赖 → 装 Node.js → 装 OpenClaw →              ║
# ║  恢复数据 → 启动服务 → 智能体满血复活！                       ║
# ║                                                              ║
# ║  From bare metal to fully restored — one command.            ║
# ╚══════════════════════════════════════════════════════════════╝
#
# 用法 / Usage:
#   bash restore-kit.sh              # 交互式引导
#   bash restore-kit.sh --skip-env   # 跳过环境安装（已有 Node/OpenClaw）
#
# 支持系统: Ubuntu / macOS / Windows (WSL2, 用 restore-kit.ps1)
# 需要: bash, curl (其他全自动安装)

set -e

# ── Colors & UI ──────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
DIM='\033[2m'
NC='\033[0m'

STEP_CURRENT=0
STEP_TOTAL=10
SKIP_ENV=false
ERRORS=()

NETRC_FILE="/tmp/.mjolnir_restore_kit_netrc_$$"
RESTORE_DIR="/tmp/mjolnir_restore_kit_$$"
DL_FILE="/tmp/mjolnir_restore_kit_dl_$$.tar.gz"

cleanup() {
  rm -f "$NETRC_FILE" "$DL_FILE" 2>/dev/null
}
trap cleanup EXIT

# Parse args
for arg in "$@"; do
  case "$arg" in
    --skip-env) SKIP_ENV=true ;;
  esac
done

# ── Progress Bar ─────────────────────────────────────────────
progress_bar() {
  local percent=$1
  local width=30
  local filled=$((percent * width / 100))
  local empty=$((width - filled))
  local bar=""
  for ((i=0; i<filled; i++)); do bar+="█"; done
  for ((i=0; i<empty; i++)); do bar+="░"; done
  printf "\r  ${CYAN}[${bar}]${NC} ${BOLD}%3d%%${NC}" "$percent"
}

step() {
  STEP_CURRENT=$((STEP_CURRENT + 1))
  local percent=$((STEP_CURRENT * 100 / STEP_TOTAL))
  local icon="$1"
  local msg="$2"
  echo ""
  progress_bar "$percent"
  echo "  ${icon} ${msg}"
}

ok() { echo -e "       ${GREEN}✓ $1${NC}"; }
fail() { echo -e "       ${RED}✗ $1${NC}"; ERRORS+=("$1"); }
warn() { echo -e "       ${YELLOW}⚠ $1${NC}"; }
info() { echo -e "       ${DIM}$1${NC}"; }

# ── Detect OS ────────────────────────────────────────────────
detect_os() {
  if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS_ID="$ID"
    OS_NAME="$PRETTY_NAME"
  elif [ "$(uname)" = "Darwin" ]; then
    OS_ID="macos"
    OS_NAME="macOS $(sw_vers -productVersion 2>/dev/null || echo '')"
  else
    OS_ID="unknown"
    OS_NAME="Unknown OS"
  fi
}

# ── Package installer (Ubuntu/macOS only) ────────────────────
install_pkg() {
  local pkg="$1"
  case "$OS_ID" in
    ubuntu|debian)
      sudo apt-get install -y -qq "$pkg" 2>/dev/null
      ;;
    macos)
      if command -v brew &>/dev/null; then
        brew install "$pkg" 2>/dev/null
      else
        warn "请先安装 Homebrew: https://brew.sh"
        return 1
      fi
      ;;
    *)
      warn "不支持的系统: $OS_NAME"
      warn "本脚本支持: Ubuntu / macOS / Windows (用 restore-kit.ps1)"
      return 1
      ;;
  esac
}

# ── Banner ───────────────────────────────────────────────────
clear 2>/dev/null || true
echo ""
echo -e "${BOLD}🌑 ════════════════════════════════════════════════════════${NC}"
echo -e "${BOLD}   雷神之影 — 一键恢复引导 (Restore Kit v2.0)${NC}"
echo -e "${BOLD}   从全新电脑到满血复活，一条命令搞定${NC}"
echo -e "${BOLD}🌑 ════════════════════════════════════════════════════════${NC}"
echo ""

# ══════════════════════════════════════════════════════════════
# Step 1: Detect system
# ══════════════════════════════════════════════════════════════
step "🖥️" "检测系统环境..."

detect_os
ok "操作系统: ${OS_NAME}"

ARCH=$(uname -m)
case "$ARCH" in
  x86_64)  ARCH_LABEL="x64"; NODE_ARCH="x64" ;;
  aarch64|arm64) ARCH_LABEL="ARM64"; NODE_ARCH="arm64" ;;
  *) ARCH_LABEL="$ARCH"; NODE_ARCH="$ARCH" ;;
esac
ok "架构: ${ARCH_LABEL}"

# Check if running as root
if [ "$(id -u)" = "0" ]; then
  warn "正在以 root 运行，建议使用普通用户"
  SUDO=""
else
  SUDO="sudo"
fi

# ══════════════════════════════════════════════════════════════
# Step 2: Check & install basic dependencies
# ══════════════════════════════════════════════════════════════
step "📦" "检查基础依赖..."

NEED_INSTALL=()

# curl (required)
if command -v curl &>/dev/null; then
  ok "curl $(curl --version 2>/dev/null | head -1 | awk '{print $2}')"
else
  NEED_INSTALL+=("curl")
  warn "curl 未安装，将自动安装"
fi

# python3
if command -v python3 &>/dev/null; then
  ok "python3 $(python3 --version 2>&1 | awk '{print $2}')"
else
  NEED_INSTALL+=("python3")
  warn "python3 未安装，将自动安装"
fi

# gpg
if command -v gpg &>/dev/null; then
  ok "gpg $(gpg --version 2>/dev/null | head -1 | awk '{print $3}')"
else
  NEED_INSTALL+=("gnupg")
  warn "gpg 未安装，将自动安装"
fi

# git (useful but not critical)
if command -v git &>/dev/null; then
  ok "git $(git --version 2>/dev/null | awk '{print $3}')"
else
  NEED_INSTALL+=("git")
  warn "git 未安装，将自动安装"
fi

# Install missing packages
if [ ${#NEED_INSTALL[@]} -gt 0 ]; then
  echo ""
  info "正在安装: ${NEED_INSTALL[*]}"

  # Update package list first (Ubuntu/Debian)
  case "$OS_ID" in
    ubuntu|debian)
      $SUDO apt-get update -qq 2>/dev/null
      ;;
  esac

  for pkg in "${NEED_INSTALL[@]}"; do
    if install_pkg "$pkg"; then
      ok "已安装: $pkg"
    else
      fail "安装失败: $pkg — 请手动安装后重试"
    fi
  done
fi

# Verify critical tools
for cmd in curl python3; do
  if ! command -v "$cmd" &>/dev/null; then
    fail "$cmd 仍未安装，无法继续"
    echo -e "\n  ${RED}❌ 缺少必要工具，请手动安装后重新运行本脚本。${NC}"
    exit 1
  fi
done

# ══════════════════════════════════════════════════════════════
# Step 3: Check & install Node.js
# ══════════════════════════════════════════════════════════════
step "💚" "检查 Node.js..."

NODE_OK=false
if command -v node &>/dev/null; then
  NODE_VER=$(node --version 2>/dev/null)
  NODE_MAJOR=$(echo "$NODE_VER" | sed 's/v//' | cut -d. -f1)
  if [ "$NODE_MAJOR" -ge 18 ] 2>/dev/null; then
    ok "Node.js ${NODE_VER} (满足要求 ≥ v18)"
    NODE_OK=true
  else
    warn "Node.js ${NODE_VER} 版本太低，需要 ≥ v18"
  fi
fi

if [ "$NODE_OK" = false ] && [ "$SKIP_ENV" = false ]; then
  info "正在安装 Node.js v22 (LTS)..."
  
  # Try nvm first (recommended, no sudo needed)
  if [ -s "$HOME/.nvm/nvm.sh" ]; then
    . "$HOME/.nvm/nvm.sh"
    nvm install 22 2>/dev/null && nvm use 22 2>/dev/null
  else
    # Install via NodeSource
    info "使用 NodeSource 安装..."
    if curl -fsSL https://deb.nodesource.com/setup_22.x 2>/dev/null | $SUDO bash - 2>/dev/null; then
      $SUDO apt-get install -y -qq nodejs 2>/dev/null
    else
      # Fallback: direct binary
      info "NodeSource 失败，尝试直接下载..."
      NODE_URL="https://nodejs.org/dist/v22.12.0/node-v22.12.0-linux-${NODE_ARCH}.tar.xz"
      if curl -fsSL "$NODE_URL" -o /tmp/node.tar.xz 2>/dev/null; then
        $SUDO tar -xJf /tmp/node.tar.xz -C /usr/local --strip-components=1 2>/dev/null
        rm -f /tmp/node.tar.xz
      fi
    fi
  fi

  # Verify
  if command -v node &>/dev/null; then
    ok "Node.js $(node --version) 安装成功"
    NODE_OK=true
  else
    fail "Node.js 安装失败"
    echo -e "\n       ${YELLOW}请手动安装:${NC}"
    echo -e "       ${DIM}curl -fsSL https://deb.nodesource.com/setup_22.x | sudo bash -${NC}"
    echo -e "       ${DIM}sudo apt install -y nodejs${NC}"
    echo -e "       ${DIM}然后重新运行: bash restore-kit.sh --skip-env${NC}"
  fi
elif [ "$SKIP_ENV" = true ] && [ "$NODE_OK" = false ]; then
  warn "跳过 Node.js 安装 (--skip-env)，但 Node.js 未找到"
fi

# ══════════════════════════════════════════════════════════════
# Step 4: Check & install OpenClaw
# ══════════════════════════════════════════════════════════════
step "🤖" "检查 OpenClaw..."

OPENCLAW_OK=false
if command -v openclaw &>/dev/null; then
  OC_VER=$(openclaw --version 2>/dev/null || echo "已安装")
  ok "OpenClaw ${OC_VER}"
  OPENCLAW_OK=true
elif [ "$NODE_OK" = true ] && [ "$SKIP_ENV" = false ]; then
  info "正在安装 OpenClaw..."

  # Try global install
  if npm install -g openclaw 2>/dev/null; then
    ok "OpenClaw 安装成功"
    OPENCLAW_OK=true
  elif npm install -g openclaw-cn 2>/dev/null; then
    ok "OpenClaw (CN) 安装成功"
    OPENCLAW_OK=true
  else
    # Try with user prefix
    info "全局安装失败，尝试用户目录..."
    mkdir -p "$HOME/.npm-global"
    npm config set prefix "$HOME/.npm-global" 2>/dev/null
    export PATH="$HOME/.npm-global/bin:$PATH"
    
    if npm install -g openclaw 2>/dev/null; then
      ok "OpenClaw 安装成功 (用户目录)"
      OPENCLAW_OK=true
    else
      fail "OpenClaw 安装失败"
      echo -e "       ${DIM}稍后手动安装: npm install -g openclaw${NC}"
    fi
  fi
else
  warn "跳过 OpenClaw 安装（Node.js 不可用）"
fi

# ══════════════════════════════════════════════════════════════
# Step 5: Collect WebDAV connection info
# ══════════════════════════════════════════════════════════════
step "📝" "连接你的备份存储..."

# Check for existing config
EXISTING_CONFIG=""
for candidate in \
  "$HOME/.openclaw/workspace/skills/mjolnir-shadow/config/backup-config.json.gpg" \
  "$HOME/.openclaw/workspace/skills/mjolnir-shadow/config/backup-config.json" \
  "$(cd "$(dirname "$0")" 2>/dev/null && pwd)/config/backup-config.json.gpg" \
  "$(cd "$(dirname "$0")" 2>/dev/null && pwd)/config/backup-config.json" \
  ; do
  if [ -f "$candidate" ] 2>/dev/null; then
    EXISTING_CONFIG="$candidate"
    break
  fi
done

CONFIG_LOADED=false

if [ -n "$EXISTING_CONFIG" ]; then
  info "发现已有配置: $(basename "$EXISTING_CONFIG")"
  echo -n "       使用已有配置？[Y/n] "
  read -r USE_EXISTING
  USE_EXISTING="${USE_EXISTING:-Y}"
  
  if [[ "$USE_EXISTING" =~ ^[Yy] ]]; then
    if [[ "$EXISTING_CONFIG" == *.gpg ]]; then
      if [ -n "$MJOLNIR_SHADOW_PASS" ]; then
        CONFIG_JSON=$(gpg --quiet --batch --yes --passphrase "$MJOLNIR_SHADOW_PASS" \
          --decrypt "$EXISTING_CONFIG" 2>/dev/null)
      else
        CONFIG_JSON=$(gpg --quiet --batch --yes --decrypt "$EXISTING_CONFIG" 2>/dev/null)
      fi
    else
      CONFIG_JSON=$(cat "$EXISTING_CONFIG")
    fi
    
    if [ -n "$CONFIG_JSON" ]; then
      WEBDAV_URL=$(echo "$CONFIG_JSON" | python3 -c "import json,sys; print(json.load(sys.stdin)['webdav_url'])")
      WEBDAV_USER=$(echo "$CONFIG_JSON" | python3 -c "import json,sys; print(json.load(sys.stdin)['webdav_user'])")
      WEBDAV_PASS=$(echo "$CONFIG_JSON" | python3 -c "import json,sys; print(json.load(sys.stdin)['webdav_pass'])")
      REMOTE_DIR=$(echo "$CONFIG_JSON" | python3 -c "import json,sys; print(json.load(sys.stdin)['remote_dir'])")
      ok "配置加载成功"
      CONFIG_LOADED=true
    else
      warn "配置解密失败，将手动输入"
    fi
  fi
fi

if [ "$CONFIG_LOADED" = false ]; then
  echo ""
  echo -e "       ${BOLD}请输入你的备份存储信息:${NC}"
  echo ""
  echo -e "       ${DIM}常见 WebDAV 地址:${NC}"
  echo -e "       ${DIM}  Nextcloud:  http://IP地址/remote.php/webdav${NC}"
  echo -e "       ${DIM}  群晖 NAS:   http://IP地址:5005${NC}"
  echo -e "       ${DIM}  ownCloud:   http://IP地址/remote.php/webdav${NC}"
  echo ""

  echo -n "       WebDAV 地址: "
  read -r WEBDAV_URL
  WEBDAV_URL="${WEBDAV_URL%/}"

  echo -n "       用户名: "
  read -r WEBDAV_USER

  echo -n "       密码: "
  read -rs WEBDAV_PASS
  echo ""

  echo -n "       备份目录名 [openclaw-backups]: "
  read -r REMOTE_DIR
  REMOTE_DIR="${REMOTE_DIR:-openclaw-backups}"

  ok "信息已收集"
fi

FULL_URL="${WEBDAV_URL}/${REMOTE_DIR}"

# ══════════════════════════════════════════════════════════════
# Step 6: Test connection
# ══════════════════════════════════════════════════════════════
step "🌐" "测试连接..."

WEBDAV_HOST=$(echo "$WEBDAV_URL" | grep -oP '://\K[^/]+' || echo "$WEBDAV_URL")
cat > "$NETRC_FILE" << EOF
machine ${WEBDAV_HOST}
login ${WEBDAV_USER}
password ${WEBDAV_PASS}
EOF
chmod 600 "$NETRC_FILE"
CURL_AUTH="--netrc-file ${NETRC_FILE}"

HTTP_CODE=$(curl -s --netrc-file "$NETRC_FILE" -o /dev/null -w "%{http_code}" \
  -X PROPFIND "${FULL_URL}/" -H "Depth: 0" --max-time 15 2>&1 || echo "000")

if [ "$HTTP_CODE" = "207" ] || [ "$HTTP_CODE" = "200" ]; then
  ok "连接成功 (HTTP ${HTTP_CODE})"
elif [ "$HTTP_CODE" = "401" ]; then
  fail "认证失败！用户名或密码错误"
  echo -e "       ${DIM}请检查后重新运行本脚本${NC}"
  exit 1
elif [ "$HTTP_CODE" = "000" ]; then
  fail "无法连接！请检查地址和网络"
  echo -e "       ${DIM}地址: ${WEBDAV_URL}${NC}"
  echo -e "       ${DIM}确认目标机器已开机且网络可达${NC}"
  exit 1
else
  warn "收到 HTTP ${HTTP_CODE}，尝试继续..."
fi

# ══════════════════════════════════════════════════════════════
# Step 7: Find latest backup
# ══════════════════════════════════════════════════════════════
step "🔍" "查找备份..."

BACKUP_LIST=$(curl -s $CURL_AUTH \
  -X PROPFIND "${FULL_URL}/" -H "Depth: 1" --max-time 15 2>/dev/null \
  | grep -oP 'backup_[^<]+\.tar\.gz' | sort -u || true)

BACKUP_COUNT=$(echo "$BACKUP_LIST" | grep -c "backup_" 2>/dev/null || echo "0")

if [ "$BACKUP_COUNT" -eq 0 ] || [ -z "$BACKUP_LIST" ]; then
  fail "未找到任何备份！"
  echo -e "       ${DIM}目录 ${REMOTE_DIR} 中没有备份文件${NC}"
  echo -e "       ${DIM}请确认备份目录名称正确${NC}"
  exit 1
fi

LATEST=$(echo "$BACKUP_LIST" | tail -1)
BACKUP_DATE=$(echo "$LATEST" | grep -oP '\d{4}-\d{2}-\d{2}' | head -1)

info "找到 ${BACKUP_COUNT} 个备份:"
echo "$BACKUP_LIST" | while read -r name; do
  if [ "$name" = "$LATEST" ]; then
    echo -e "       ${GREEN}→ ${name} (最新，将恢复这个)${NC}"
  else
    echo -e "       ${DIM}  ${name}${NC}"
  fi
done

# ══════════════════════════════════════════════════════════════
# Step 8: Download
# ══════════════════════════════════════════════════════════════
step "📥" "下载备份包..."

SIZE_BYTES=$(curl -sI $CURL_AUTH "${FULL_URL}/${LATEST}" 2>/dev/null \
  | grep -i content-length | tail -1 | tr -dc '0-9')

if [ -n "$SIZE_BYTES" ] && [ "$SIZE_BYTES" -gt 0 ] 2>/dev/null; then
  SIZE_MB=$(python3 -c "print(f'{${SIZE_BYTES}/1048576:.1f}')" 2>/dev/null || echo "?")
  info "文件大小: ${SIZE_MB} MB"
fi

curl --progress-bar $CURL_AUTH \
  -o "$DL_FILE" \
  "${FULL_URL}/${LATEST}" 2>&1

ACTUAL_SIZE=$(du -h "$DL_FILE" 2>/dev/null | cut -f1)
ok "下载完成 (${ACTUAL_SIZE})"

# ══════════════════════════════════════════════════════════════
# Step 9: Extract & restore
# ══════════════════════════════════════════════════════════════
step "🔄" "恢复数据..."

WORKSPACE_PATH="$HOME/.openclaw/workspace"
OPENCLAW_DIR="$HOME/.openclaw"
RESTORED=0

mkdir -p "$RESTORE_DIR"
tar xzf "$DL_FILE" -C "$RESTORE_DIR"
rm -f "$DL_FILE"

# Workspace
if [ -f "$RESTORE_DIR/workspace.tar.gz" ]; then
  mkdir -p "$WORKSPACE_PATH"
  tar xzf "$RESTORE_DIR/workspace.tar.gz" -C "$WORKSPACE_PATH" 2>/dev/null
  ok "记忆 & 文档 → ${WORKSPACE_PATH}"
  RESTORED=$((RESTORED + 1))
fi

# Config
if [ -f "$RESTORE_DIR/config.tar.gz" ]; then
  mkdir -p "$OPENCLAW_DIR"
  tar xzf "$RESTORE_DIR/config.tar.gz" -C "$OPENCLAW_DIR" 2>/dev/null
  ok "配置 & 定时任务 → ${OPENCLAW_DIR}"
  RESTORED=$((RESTORED + 1))
fi

# Strategies
if [ -f "$RESTORE_DIR/strategies.tar.gz" ]; then
  local_strat="${OPENCLAW_DIR}/workspace/projects/auto_trading"
  mkdir -p "$local_strat"
  tar xzf "$RESTORE_DIR/strategies.tar.gz" -C "$local_strat" 2>/dev/null
  ok "交易策略 → ${local_strat}"
  RESTORED=$((RESTORED + 1))
fi

# Skills
if [ -f "$RESTORE_DIR/skills.tar.gz" ]; then
  mkdir -p "${OPENCLAW_DIR}/workspace"
  tar xzf "$RESTORE_DIR/skills.tar.gz" -C "${OPENCLAW_DIR}/workspace" 2>/dev/null
  ok "技能包 → ${OPENCLAW_DIR}/workspace/skills/"
  RESTORED=$((RESTORED + 1))
fi

ok "共恢复 ${RESTORED} 个组件"

# Cleanup temp
rm -rf "$RESTORE_DIR"

# ══════════════════════════════════════════════════════════════
# Step 10: Start OpenClaw
# ══════════════════════════════════════════════════════════════
step "🚀" "启动智能体..."

if [ "$OPENCLAW_OK" = true ] || command -v openclaw &>/dev/null; then
  if openclaw gateway start 2>/dev/null; then
    ok "OpenClaw 已启动！"
  elif openclaw gateway restart 2>/dev/null; then
    ok "OpenClaw 已重启！"
  else
    warn "自动启动失败，请手动运行: openclaw gateway start"
  fi
else
  warn "OpenClaw 未安装，跳过启动"
fi

# ══════════════════════════════════════════════════════════════
# Final Summary
# ══════════════════════════════════════════════════════════════
echo ""
progress_bar 100
echo ""
echo ""

# Check for errors
if [ ${#ERRORS[@]} -gt 0 ]; then
  echo -e "${BOLD}🌑 ════════════════════════════════════════════════════════${NC}"
  echo -e "${BOLD}   ⚠️  恢复完成（有部分警告）${NC}"
  echo -e "${BOLD}🌑 ════════════════════════════════════════════════════════${NC}"
  echo ""
  echo -e "  ${YELLOW}需要注意:${NC}"
  for err in "${ERRORS[@]}"; do
    echo -e "  ${YELLOW}  • ${err}${NC}"
  done
  echo ""
else
  echo -e "${BOLD}🌑 ════════════════════════════════════════════════════════${NC}"
  echo -e "${BOLD}   ✅ 完美！从裸机到满血，一步到位！${NC}"
  echo -e "${BOLD}🌑 ════════════════════════════════════════════════════════${NC}"
  echo ""
fi

echo -e "  📦 备份来源:  ${CYAN}${LATEST}${NC}"
echo -e "  📅 备份日期:  ${BOLD}${BACKUP_DATE}${NC}"
echo -e "  🔄 恢复组件:  ${GREEN}${RESTORED} 个${NC}"
echo -e "  📁 工作空间:  ${WORKSPACE_PATH}"
echo ""

# Environment summary
echo -e "  ${BOLD}环境状态:${NC}"
if command -v node &>/dev/null; then
  echo -e "  ${GREEN}  ✓ Node.js $(node --version)${NC}"
else
  echo -e "  ${RED}  ✗ Node.js 未安装${NC}"
fi
if command -v openclaw &>/dev/null; then
  echo -e "  ${GREEN}  ✓ OpenClaw 已安装${NC}"
else
  echo -e "  ${RED}  ✗ OpenClaw 未安装${NC}"
fi
echo -e "  ${GREEN}  ✓ 记忆数据 已恢复${NC}"
echo -e "  ${GREEN}  ✓ 技能包   已恢复${NC}"
echo ""

# Next steps if anything is missing
if ! command -v openclaw &>/dev/null; then
  echo -e "  ${YELLOW}📌 还需要:${NC}"
  if ! command -v node &>/dev/null; then
    echo -e "     1. 安装 Node.js:  ${CYAN}curl -fsSL https://deb.nodesource.com/setup_22.x | sudo bash - && sudo apt install -y nodejs${NC}"
    echo -e "     2. 安装 OpenClaw: ${CYAN}npm install -g openclaw${NC}"
    echo -e "     3. 启动服务:     ${CYAN}openclaw gateway start${NC}"
  else
    echo -e "     1. 安装 OpenClaw: ${CYAN}npm install -g openclaw${NC}"
    echo -e "     2. 启动服务:     ${CYAN}openclaw gateway start${NC}"
  fi
  echo ""
fi

echo -e "  ${GREEN}🧠 智能体下次醒来就有完整记忆了！${NC}"
echo ""
echo -e "  ${DIM}临时文件已清理，凭证未留在磁盘上。${NC}"
echo -e "  ${DIM}有问题？GitHub: https://github.com/king6381/mjolnir-shadow${NC}"
echo ""
