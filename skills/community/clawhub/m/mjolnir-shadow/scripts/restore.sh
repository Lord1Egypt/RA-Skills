#!/bin/bash
# 🌑 Mjolnir Shadow (雷神之影) - Restore Tool / 恢复工具
# Security: uses --netrc-file, never exposes credentials in process listings
# v2.0 — Added --auto mode with progress bar for one-click restore

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
CONFIG_FILE="${SKILL_DIR}/config/backup-config.json"
ENCRYPTED_CONFIG="${SKILL_DIR}/config/backup-config.json.gpg"
NETRC_FILE="/tmp/.mjolnir_shadow_netrc_$$"

# ── Colors & Symbols ─────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
DIM='\033[2m'
NC='\033[0m'

STEP_CURRENT=0
STEP_TOTAL=6

cleanup() {
  rm -f "$NETRC_FILE" 2>/dev/null
}
trap cleanup EXIT

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

step_done() {
  echo "       ${GREEN}✓ $1${NC}"
}

step_fail() {
  echo "       ${RED}✗ $1${NC}"
}

banner() {
  echo ""
  echo -e "${BOLD}🌑 ═══════════════════════════════════════════${NC}"
  echo -e "${BOLD}   雷神之影 — $1${NC}"
  echo -e "${BOLD}🌑 ═══════════════════════════════════════════${NC}"
}

# ── Load Config ──────────────────────────────────────────────
decrypt_config() {
  if [ -f "$ENCRYPTED_CONFIG" ]; then
    if [ -n "$MJOLNIR_SHADOW_PASS" ]; then
      gpg --quiet --batch --yes --passphrase "$MJOLNIR_SHADOW_PASS" \
        --decrypt "$ENCRYPTED_CONFIG" 2>/dev/null
    else
      gpg --quiet --batch --yes --decrypt "$ENCRYPTED_CONFIG" 2>/dev/null
    fi
  elif [ -f "$CONFIG_FILE" ]; then
    echo "⚠️  Warning: Using unencrypted config. / 警告：使用未加密配置。" >&2
    cat "$CONFIG_FILE"
  else
    echo "❌ No config found. Run: python3 ${SCRIPT_DIR}/setup_backup.py" >&2
    exit 1
  fi
}

load_config() {
  CONFIG_JSON=$(decrypt_config)
  if [ -z "$CONFIG_JSON" ]; then
    echo -e "${RED}❌ Failed to load config. Check GPG passphrase.${NC}"
    echo -e "${RED}   配置加载失败，检查密码。${NC}"
    exit 1
  fi

  WEBDAV_URL=$(echo "$CONFIG_JSON" | python3 -c "import json,sys; print(json.load(sys.stdin)['webdav_url'])")
  WEBDAV_USER=$(echo "$CONFIG_JSON" | python3 -c "import json,sys; print(json.load(sys.stdin)['webdav_user'])")
  WEBDAV_PASS=$(echo "$CONFIG_JSON" | python3 -c "import json,sys; print(json.load(sys.stdin)['webdav_pass'])")
  REMOTE_DIR=$(echo "$CONFIG_JSON" | python3 -c "import json,sys; print(json.load(sys.stdin)['remote_dir'])")
  WORKSPACE_PATH=$(echo "$CONFIG_JSON" | python3 -c "import json,sys; c=json.load(sys.stdin); print(c.get('workspace_path','$HOME/.openclaw/workspace'))")
  OPENCLAW_DIR=$(echo "$CONFIG_JSON" | python3 -c "import json,sys; c=json.load(sys.stdin); print(c.get('openclaw_dir','$HOME/.openclaw'))")
  FULL_URL="${WEBDAV_URL}/${REMOTE_DIR}"

  # Security: netrc file
  WEBDAV_HOST=$(echo "$WEBDAV_URL" | grep -oP '://\K[^/]+')
  cat > "$NETRC_FILE" << EOF
machine ${WEBDAV_HOST}
login ${WEBDAV_USER}
password ${WEBDAV_PASS}
EOF
  chmod 600 "$NETRC_FILE"
  CURL_AUTH="--netrc-file ${NETRC_FILE}"
}

# ── Download with progress ───────────────────────────────────
download_with_progress() {
  local url="$1"
  local output="$2"
  local tmpfile="${output}.tmp"

  # Get file size first
  local size_bytes
  size_bytes=$(curl -sI $CURL_AUTH "$url" 2>/dev/null | grep -i content-length | tail -1 | tr -dc '0-9')

  if [ -n "$size_bytes" ] && [ "$size_bytes" -gt 0 ] 2>/dev/null; then
    local size_mb=$(echo "scale=1; $size_bytes / 1048576" | bc 2>/dev/null || echo "?")
    echo -e "       ${DIM}文件大小: ${size_mb}MB${NC}"
    # Download with curl progress bar
    curl -# $CURL_AUTH -o "$tmpfile" "$url" 2>&1 | while IFS= read -r -d $'\r' line; do
      # curl -# outputs progress like "###   5.0%"
      local pct
      pct=$(echo "$line" | grep -oP '[\d.]+%' | head -1 | cut -d. -f1)
      if [ -n "$pct" ]; then
        progress_bar "$pct"
        printf "  📥 下载中..."
      fi
    done
    echo ""
  else
    # Fallback: no size info, just download
    curl -s $CURL_AUTH -o "$tmpfile" "$url"
  fi

  mv "$tmpfile" "$output"
}

# ── Find latest backup ───────────────────────────────────────
find_latest_backup() {
  curl -s $CURL_AUTH \
    -X PROPFIND "${FULL_URL}/" -H "Depth: 1" 2>/dev/null \
    | grep -oP 'backup_[^<]+\.tar\.gz' | sort -u | tail -1
}

# ── List backups ─────────────────────────────────────────────
list_backups() {
  banner "可用备份列表"
  echo ""
  local count=0
  curl -s $CURL_AUTH \
    -X PROPFIND "${FULL_URL}/" -H "Depth: 1" 2>/dev/null \
    | grep -oP 'backup_[^<]+\.tar\.gz' | sort -u | while read -r name; do
      count=$((count + 1))
      # Extract date from filename
      local date_part
      date_part=$(echo "$name" | grep -oP '\d{4}-\d{2}-\d{2}_\d{4}' | head -1)
      echo -e "  ${CYAN}${count}.${NC} 📦 ${name}  ${DIM}(${date_part})${NC}"
    done
  echo ""
}

# ── Manual restore (original behavior) ───────────────────────
restore_manual() {
  local BACKUP_FILE="$1"
  local RESTORE_DIR="/tmp/mjolnir_shadow_restore_$$"

  echo "🌑 Restoring / 正在恢复: ${BACKUP_FILE}"
  echo "=========================================="

  mkdir -p "$RESTORE_DIR"

  echo "📥 Downloading... / 下载中..."
  curl -s $CURL_AUTH \
    -o "/tmp/${BACKUP_FILE}" \
    "${FULL_URL}/${BACKUP_FILE}"

  echo "📦 Extracting... / 解压中..."
  tar xzf "/tmp/${BACKUP_FILE}" -C "$RESTORE_DIR"

  echo ""
  echo "📋 Contents / 内容:"
  ls -lh "$RESTORE_DIR/"
  echo ""
  echo "⚠️  Files extracted to / 文件已解压到: ${RESTORE_DIR}"
  echo "    Review before overwriting! / 覆盖前请检查！"
  echo ""
  echo "    Restore workspace / 恢复工作空间:"
  echo "      tar xzf ${RESTORE_DIR}/workspace.tar.gz -C ~/.openclaw/workspace/"
  echo ""
  echo "    Restore config / 恢复配置:"
  echo "      tar xzf ${RESTORE_DIR}/config.tar.gz -C ~/.openclaw/"
  echo ""

  rm -f "/tmp/${BACKUP_FILE}"
  echo "✅ Ready at / 就绪: ${RESTORE_DIR}"
}

# ══════════════════════════════════════════════════════════════
# ── AUTO MODE — One-click full restore with progress bar ─────
# ══════════════════════════════════════════════════════════════
restore_auto() {
  banner "一键全自动恢复"
  echo ""
  echo -e "  ${DIM}所有步骤将自动完成，请稍候...${NC}"

  local RESTORE_DIR="/tmp/mjolnir_shadow_restore_$$"
  local DL_FILE="/tmp/mjolnir_shadow_dl_$$.tar.gz"
  mkdir -p "$RESTORE_DIR"

  # ── Step 1: Load config ──
  step "🔐" "解密配置文件..."
  load_config
  step_done "配置加载成功"

  # ── Step 2: Find latest backup ──
  step "🔍" "查找最新备份..."
  local LATEST
  LATEST=$(find_latest_backup)
  if [ -z "$LATEST" ]; then
    step_fail "未找到任何备份！"
    echo -e "\n  ${RED}❌ 驿站上没有备份文件，请先运行 backup.sh 创建备份。${NC}"
    exit 1
  fi
  local backup_date
  backup_date=$(echo "$LATEST" | grep -oP '\d{4}-\d{2}-\d{2}' | head -1)
  step_done "找到: ${LATEST} (${backup_date})"

  # ── Step 3: Download ──
  step "📥" "下载备份包..."
  download_with_progress "${FULL_URL}/${LATEST}" "$DL_FILE"
  local filesize
  filesize=$(du -h "$DL_FILE" 2>/dev/null | cut -f1)
  step_done "下载完成 (${filesize})"

  # ── Step 4: Extract ──
  step "📦" "解压备份包..."
  tar xzf "$DL_FILE" -C "$RESTORE_DIR"
  rm -f "$DL_FILE"
  local contents
  contents=$(ls "$RESTORE_DIR/" | tr '\n' ', ' | sed 's/,$//')
  step_done "解压完成: ${contents}"

  # ── Step 5: Restore all components ──
  step "🔄" "恢复文件到系统..."

  local restored=0

  # Workspace
  if [ -f "$RESTORE_DIR/workspace.tar.gz" ]; then
    mkdir -p "$WORKSPACE_PATH"
    tar xzf "$RESTORE_DIR/workspace.tar.gz" -C "$WORKSPACE_PATH" 2>/dev/null
    echo -e "       ${GREEN}✓${NC} workspace → ${WORKSPACE_PATH}"
    restored=$((restored + 1))
  fi

  # Config
  if [ -f "$RESTORE_DIR/config.tar.gz" ]; then
    mkdir -p "$OPENCLAW_DIR"
    tar xzf "$RESTORE_DIR/config.tar.gz" -C "$OPENCLAW_DIR" 2>/dev/null
    echo -e "       ${GREEN}✓${NC} config → ${OPENCLAW_DIR}"
    restored=$((restored + 1))
  fi

  # Strategies
  if [ -f "$RESTORE_DIR/strategies.tar.gz" ]; then
    local strat_dir="${OPENCLAW_DIR}/workspace/projects/auto_trading"
    mkdir -p "$strat_dir"
    tar xzf "$RESTORE_DIR/strategies.tar.gz" -C "$strat_dir" 2>/dev/null
    echo -e "       ${GREEN}✓${NC} strategies → ${strat_dir}"
    restored=$((restored + 1))
  fi

  # Skills
  if [ -f "$RESTORE_DIR/skills.tar.gz" ]; then
    local skills_dir="${OPENCLAW_DIR}/workspace/skills"
    mkdir -p "$skills_dir"
    tar xzf "$RESTORE_DIR/skills.tar.gz" -C "${OPENCLAW_DIR}/workspace" 2>/dev/null
    echo -e "       ${GREEN}✓${NC} skills → ${skills_dir}"
    restored=$((restored + 1))
  fi

  step_done "共恢复 ${restored} 个组件"

  # ── Step 6: Restart OpenClaw ──
  step "🚀" "重启 OpenClaw..."
  if command -v openclaw &>/dev/null; then
    openclaw gateway restart 2>/dev/null && \
      step_done "OpenClaw 已重启" || \
      step_done "OpenClaw 重启需手动执行"
  else
    echo -e "       ${YELLOW}⚠ OpenClaw 未安装，跳过重启${NC}"
    echo -e "       ${DIM}  安装: npm install -g openclaw${NC}"
  fi

  # ── Cleanup ──
  rm -rf "$RESTORE_DIR"

  # ── Summary ──
  echo ""
  progress_bar 100
  echo ""
  echo ""
  echo -e "${BOLD}🌑 ═══════════════════════════════════════════${NC}"
  echo -e "${BOLD}   ✅ 恢复完成！${NC}"
  echo -e "${BOLD}🌑 ═══════════════════════════════════════════${NC}"
  echo ""
  echo -e "  📦 备份文件: ${CYAN}${LATEST}${NC}"
  echo -e "  📅 备份日期: ${backup_date}"
  echo -e "  🔄 恢复组件: ${restored} 个"
  echo -e "  📁 工作空间: ${WORKSPACE_PATH}"
  echo ""
  echo -e "  ${DIM}智能体下次醒来就有完整记忆了 🧠${NC}"
  echo ""
}

# ══════════════════════════════════════════════════════════════
# ── Main ─────────────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════
ACTION="${1:---help}"

case "$ACTION" in
  --auto|-a)
    restore_auto
    ;;
  --list|-l)
    load_config
    list_backups
    ;;
  --latest)
    load_config
    LATEST=$(find_latest_backup)
    if [ -z "$LATEST" ]; then
      echo "❌ No backups found / 未找到备份"
      exit 1
    fi
    restore_manual "$LATEST"
    ;;
  --file|-f)
    load_config
    if [ -z "$2" ]; then
      echo "Usage: restore.sh --file <name>"
      exit 1
    fi
    restore_manual "$2"
    ;;
  *)
    echo ""
    echo -e "${BOLD}🌑 雷神之影 — 恢复工具${NC}"
    echo ""
    echo "用法 / Usage:"
    echo ""
    echo -e "  ${CYAN}--auto, -a${NC}     一键全自动恢复（推荐！带进度条）"
    echo -e "  ${CYAN}--list, -l${NC}     列出所有可用备份"
    echo -e "  ${CYAN}--latest${NC}       恢复最新备份（手动模式）"
    echo -e "  ${CYAN}--file, -f${NC}     恢复指定备份文件"
    echo ""
    echo "示例 / Examples:"
    echo ""
    echo "  bash restore.sh --auto              # 一键恢复，小白推荐"
    echo "  bash restore.sh --list              # 看看有哪些备份"
    echo "  bash restore.sh --file backup_xxx   # 恢复指定版本"
    echo ""
    exit 0
    ;;
esac
