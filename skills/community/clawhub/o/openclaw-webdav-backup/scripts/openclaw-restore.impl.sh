#!/usr/bin/env bash
set -euo pipefail
shopt -s inherit_errexit 2>/dev/null || true

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# OpenClaw 轻量版恢复脚本（本地恢复版）
#
# 用法：
#   bash scripts/openclaw-restore.sh --from <backup_dir>
#   bash scripts/openclaw-restore.sh --from <backup_dir> --decrypt-config
#   bash scripts/openclaw-restore.sh --from <backup_dir> --decrypt-config --dry-run
#   bash scripts/openclaw-restore.sh --list                 # 列出所有可用备份
#   bash scripts/openclaw-restore.sh --latest               # 恢复最新备份
#   bash scripts/openclaw-restore.sh                        # 交互式选择版本
#
# 说明：
# - 默认恢复到 ~/.openclaw/
# - 会恢复 workspace / extensions
# - 如果存在 openclaw.json.enc，可选解密为 ~/.openclaw/openclaw.json
# - 默认不自动重启 gateway

BACKUP_DIR=""
DRY_RUN=0
DECRYPT_CONFIG=0
LIST_BACKUPS=0
USE_LATEST=0
DELETE_BACKUP=""
DELETE_OLD_DAYS=""
DIFF_MODE=0
DIFF_FORMAT="summary"
CHECK_DEPS=0
VERIFY_RESTORE=0

# 声明日志函数先，确保在函数定义前可用
log() { printf '[restore] %s\n' "$*"; }

# 自动检测备份根目录
detect_backup_root() {
  if [[ -n "${OPENCLAW_WORKSPACE_DIR:-}" ]]; then
    echo "${OPENCLAW_WORKSPACE_DIR}/backups/openclaw"
  else
    local base_dir
    base_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
    echo "${base_dir}/backups/openclaw"
  fi
}

BACKUP_ROOT="$(detect_backup_root)"

# 列出所有可用备份
list_available_backups() {
  if [[ ! -d "${BACKUP_ROOT}" ]]; then
    echo "No backup directory found: ${BACKUP_ROOT}" >&2
    exit 1
  fi

  local backups=()
  while IFS= read -r -d '' dir; do
    local name
    name=$(basename "$dir")
    [[ "$name" == ".snapshots" ]] && continue
    if [[ -f "$dir/workspace.tar.gz" ]]; then
      backups+=("$name")
    fi
  done < <(find "${BACKUP_ROOT}" -mindepth 1 -maxdepth 1 -type d -print0 2>/dev/null | sort -z -r)

  if [[ ${#backups[@]} -eq 0 ]]; then
    echo "No backups found in ${BACKUP_ROOT}" >&2
    exit 1
  fi

  printf '\n📦 Available Backup Versions:\n\n'
  printf '%-4s %-20s %-8s %-12s %-10s\n' "No." "Timestamp" "Level" "Size" "Encrypted"
  printf '%s\n' "─────────────────────────────────────────────────────────"

  local i=1
  for backup in "${backups[@]}"; do
    local dir="${BACKUP_ROOT}/${backup}"
    local size="-"
    local level="-"
    local encrypted="-"

    # 计算大小
    if [[ -f "$dir/workspace.tar.gz" ]]; then
      local ws_size ext_size=0
      ws_size=$(du -h "$dir/workspace.tar.gz" 2>/dev/null | cut -f1)
      if [[ -f "$dir/extensions.tar.gz" ]]; then
        ext_size=$(du -h "$dir/extensions.tar.gz" 2>/dev/null | cut -f1)
        size="${ws_size}+${ext_size}"
      else
        size="${ws_size}"
      fi
    fi

    # 读取备份级别元数据
    if [[ -f "$dir/workspace.meta" ]]; then
      level=$(grep "^level=" "$dir/workspace.meta" 2>/dev/null | cut -d= -f2 || echo "?")
    fi

    # 检查是否有加密配置
    if [[ -f "$dir/openclaw.json.enc" ]]; then
      encrypted="🔒"
    elif [[ -f "$dir/openclaw.json" ]]; then
      encrypted="No"
    fi

    printf '%-4s %-20s %-8s %-12s %-10s\n' "${i}." "${backup}" "${level}" "${size}" "${encrypted}"
    ((i++))
  done
  printf '\n'
  printf 'Use: --from %s/<timestamp> to restore specific version\n' "${BACKUP_ROOT}"
  printf '     --latest to restore the most recent backup\n'
  printf '     (no args) for interactive selection\n'
}

# 交互式选择备份版本
interactive_select_backup() {
  local backups=()
  while IFS= read -r -d '' dir; do
    local name
    name=$(basename "$dir")
    [[ "$name" == ".snapshots" ]] && continue
    if [[ -f "$dir/workspace.tar.gz" ]]; then
      backups+=("$name")
    fi
  done < <(find "${BACKUP_ROOT}" -mindepth 1 -maxdepth 1 -type d -print0 2>/dev/null | sort -z -r)

  if [[ ${#backups[@]} -eq 0 ]]; then
    echo "No backups found in ${BACKUP_ROOT}" >&2
    exit 1
  fi

  list_available_backups

  printf 'Enter backup number to restore (1-%d): ' "${#backups[@]}"
  local choice
  read -r choice

  if ! [[ "$choice" =~ ^[0-9]+$ ]] || [[ "$choice" -lt 1 ]] || [[ "$choice" -gt ${#backups[@]} ]]; then
    echo "Invalid selection: $choice" >&2
    exit 1
  fi

  local selected="${backups[$((choice-1))]}"
  BACKUP_DIR="${BACKUP_ROOT}/${selected}"
  echo ""
  log "Selected backup: ${selected}"
}

# 依赖项检查函数
check_dependencies() {
  local PASS=0 WARN=0 FAIL=0
  local NODE_MIN="18.0.0"
  local REQUIRED_SPACE_MB=500  # 至少500MB可用空间

  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "🔍  OpenClaw Restore - Dependency Check"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo ""

  # 1. Node.js 检查
  echo "📦 Runtime Environment:"
  if command -v node >/dev/null 2>&1; then
    local NODE_VER
    NODE_VER=$(node --version 2>/dev/null | sed 's/v//')
    if [[ -n "$NODE_VER" ]]; then
      local MAJOR
      MAJOR=$(echo "$NODE_VER" | cut -d. -f1)
      if [[ "$MAJOR" -ge 18 ]]; then
        echo "  ✅ Node.js: v${NODE_VER} (>= ${NODE_MIN})"
        PASS=$((PASS + 1))
      else
        echo "  ⚠️  Node.js: v${NODE_VER} (推荐 >= ${NODE_MIN})"
        WARN=$((WARN + 1))
      fi
    else
      echo "  ⚠️  Node.js: 已安装但无法获取版本"
      WARN=$((WARN + 1))
    fi
  else
    echo "  ❌ Node.js: 未安装 (OpenClaw 需要 Node.js)"
    FAIL=$((FAIL + 1))
  fi

  # npm 检查
  if command -v npm >/dev/null 2>&1; then
    local NPM_VER
    NPM_VER=$(npm --version 2>/dev/null)
    echo "  ✅ npm: v${NPM_VER}"
    PASS=$((PASS + 1))
  else
    echo "  ⚠️  npm: 未安装"
    WARN=$((WARN + 1))
  fi

  echo ""
  echo "🔧 System Commands:"

  # 2. 系统命令检查
  local REQUIRED_CMDS=(tar gzip curl openssl git)
  for cmd in "${REQUIRED_CMDS[@]}"; do
    if command -v "$cmd" >/dev/null 2>&1; then
      echo "  ✅ $cmd"
      PASS=$((PASS + 1))
    else
      echo "  ❌ $cmd (必需)"
      FAIL=$((FAIL + 1))
    fi
  done

  echo ""
  echo "💾 Disk Space:"

  # 3. 磁盘空间检查
  local TARGET_DIR="${OPENCLAW_HOME:-$HOME/.openclaw}"
  if [[ -d "$TARGET_DIR" ]] || [[ -d "$(dirname "$TARGET_DIR")" ]]; then
    local FREE_KB
    if [[ -d "$TARGET_DIR" ]]; then
      FREE_KB=$(df -k "$TARGET_DIR" 2>/dev/null | awk 'NR==2 {print $4}')
    else
      FREE_KB=$(df -k "$HOME" 2>/dev/null | awk 'NR==2 {print $4}')
    fi
    
    if [[ -n "$FREE_KB" ]]; then
      local FREE_MB=$((FREE_KB / 1024))
      if [[ $FREE_MB -ge $REQUIRED_SPACE_MB ]]; then
        echo "  ✅ 可用空间: ${FREE_MB} MB (要求: ${REQUIRED_SPACE_MB} MB)"
        PASS=$((PASS + 1))
      else
        echo "  ⚠️  可用空间: ${FREE_MB} MB (推荐: >= ${REQUIRED_SPACE_MB} MB)"
        WARN=$((WARN + 1))
      fi
    else
      echo "  ⚠️  无法获取磁盘空间信息"
      WARN=$((WARN + 1))
    fi
  else
    echo "  ⚠️  目标目录不存在"
    WARN=$((WARN + 1))
  fi

  echo ""
  echo "🔐 Permissions:"

  # 4. 目录权限检查
  if [[ -d "$TARGET_DIR" ]]; then
    if [[ -w "$TARGET_DIR" ]]; then
      echo "  ✅ ${TARGET_DIR}: 可写"
      PASS=$((PASS + 1))
    else
      echo "  ❌ ${TARGET_DIR}: 无写入权限"
      FAIL=$((FAIL + 1))
    fi
  else
    # 检查父目录是否可写
    local PARENT
    PARENT=$(dirname "$TARGET_DIR")
    if [[ -w "$PARENT" ]]; then
      echo "  ✅ ${PARENT}: 可创建目标目录"
      PASS=$((PASS + 1))
    else
      echo "  ❌ ${PARENT}: 无写入权限，无法创建目标目录"
      FAIL=$((FAIL + 1))
    fi
  fi

  echo ""
  echo "🌐 Network:"

  # 5. 网络连通性检查（可选）
  if curl -s --max-time 5 -o /dev/null https://api.telegram.org 2>/dev/null; then
    echo "  ✅ 外部网络: 可访问 (telegram.org)"
    PASS=$((PASS + 1))
  else
    echo "  ⚠️  外部网络: 受限或不可访问 (不影响本地恢复)"
    WARN=$((WARN + 1))
  fi

  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "📊 Check Summary:"
  echo "   ✅ Pass: ${PASS}   ⚠️  Warn: ${WARN}   ❌ Fail: ${FAIL}"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

  if [[ $FAIL -gt 0 ]]; then
    echo ""
    echo "❌ Dependency check FAILED. Please fix the issues above before restoring."
    echo ""
    return 1
  elif [[ $WARN -gt 0 ]]; then
    echo ""
    echo "⚠️  Dependency check PASSED with warnings."
    echo "   You may proceed, but some features may not work correctly."
    echo ""
    return 0
  else
    echo ""
    echo "✅ All dependencies satisfied!"
    echo ""
    return 0
  fi
}

# 获取最新备份
get_latest_backup() {
  local latest
  latest=$(find "${BACKUP_ROOT}" -mindepth 1 -maxdepth 1 -type d -name "20*" ! -name ".snapshots" -printf '%f\n' 2>/dev/null | sort -r | head -1)
  if [[ -z "$latest" ]]; then
    echo "No backups found in ${BACKUP_ROOT}" >&2
    exit 1
  fi
  echo "${BACKUP_ROOT}/${latest}"
}

# 删除指定备份
delete_specific_backup() {
  local target_name="$1"
  local target_dir="${BACKUP_ROOT}/${target_name}"

  if [[ ! -d "$target_dir" ]]; then
    log "❌ Backup not found: ${target_name}"
    exit 1
  fi

  if [[ ! -f "$target_dir/workspace.tar.gz" ]]; then
    log "❌ Invalid backup directory: ${target_name}"
    exit 1
  fi

  if [[ ${DRY_RUN} -eq 1 ]]; then
    log "DRY RUN: Would delete ${target_dir}"
    return 0
  fi

  read -r -p "Are you sure you want to delete backup '${target_name}'? [y/N] " confirm
  if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
    log "Delete cancelled"
    exit 0
  fi

  rm -rf "$target_dir"
  log "✅ Deleted backup: ${target_name}"
}

# 删除旧备份
delete_old_backups() {
  local days="$1"
  local count=0

  if [[ ${DRY_RUN} -eq 1 ]]; then
    log "DRY RUN: Would delete backups older than ${days} days"
  fi

  while IFS= read -r -d '' dir; do
    local name
    name=$(basename "$dir")
    [[ "$name" == ".snapshots" ]] && continue
    if [[ -f "$dir/workspace.tar.gz" ]]; then
      if [[ ${DRY_RUN} -eq 1 ]]; then
        log "DRY RUN: Would delete ${name}"
      else
        rm -rf "$dir"
        log "Deleted: ${name}"
      fi
      ((count++)) || true
    fi
  done < <(find "${BACKUP_ROOT}" -mindepth 1 -maxdepth 1 -type d -mtime "+${days}" ! -name ".snapshots" -print0 2>/dev/null)

  if [[ ${count} -eq 0 ]]; then
    log "No backups older than ${days} days found"
  else
    log "✅ Deleted ${count} backup(s) older than ${days} days"
  fi
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --from)
      BACKUP_DIR="$2"
      shift 2
      ;;
    --dry-run)
      DRY_RUN=1
      shift
      ;;
    --decrypt-config)
      DECRYPT_CONFIG=1
      shift
      ;;
    --list)
      LIST_BACKUPS=1
      shift
      ;;
    --latest)
      USE_LATEST=1
      shift
      ;;
    --delete)
      DELETE_BACKUP="$2"
      shift 2
      ;;
    --delete-old)
      DELETE_OLD_DAYS="$2"
      shift 2
      ;;
    --diff)
      DIFF_MODE=1
      shift
      ;;
    --diff-format)
      DIFF_FORMAT="$2"
      shift 2
      ;;
    --check-deps)
      CHECK_DEPS=1
      shift
      ;;
    --verify-restore|--test-restore)
      VERIFY_RESTORE=1
      shift
      ;;
    --help|-h)
      echo "Usage: bash scripts/openclaw-restore.sh [OPTIONS]"
      echo ""
      echo "Options:"
      echo "  --from <dir>        Restore from specific backup directory"
      echo "  --latest            Restore the most recent backup"
      echo "  --list              List all available backup versions"
      echo "  --delete <ts>       Delete specific backup by timestamp"
      echo "  --delete-old <n>    Delete backups older than n days"
      echo "  --decrypt-config    Decrypt openclaw.json.enc if present"
      echo "  --diff              Preview changes before restore"
      echo "  --diff-format <fmt> Diff format: summary|full|json"
      echo "  --check-deps        Check dependencies before restore"
      echo "  --verify-restore    Verify backup can be restored without overwriting"
      echo "  --dry-run           Show what would be done without executing"
      echo "  --help, -h          Show this help message"
      echo ""
      echo "Examples:"
      echo "  bash scripts/openclaw-restore.sh --list"
      echo "  bash scripts/openclaw-restore.sh --latest --decrypt-config"
      echo "  bash scripts/openclaw-restore.sh --from backups/openclaw/2026-04-02-030000"
      echo "  bash scripts/openclaw-restore.sh --delete 2026-04-01-030000"
      echo "  bash scripts/openclaw-restore.sh --delete-old 7"
      echo "  bash scripts/openclaw-restore.sh --check-deps"
      echo "  bash scripts/openclaw-restore.sh --from <dir> --verify-restore --decrypt-config"
      echo "  bash scripts/openclaw-restore.sh --from <dir> --diff"
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      echo "Use --help for usage information" >&2
      exit 1
      ;;
  esac
done

# 处理模式选择
if [[ ${LIST_BACKUPS} -eq 1 ]]; then
  list_available_backups
  exit 0
fi

if [[ -n "${DELETE_BACKUP}" ]]; then
  # 支持完整路径或纯时间戳
  if [[ -d "${DELETE_BACKUP}" ]]; then
    DELETE_BACKUP="$(basename "${DELETE_BACKUP}")"
  fi
  delete_specific_backup "${DELETE_BACKUP}"
  exit 0
fi

if [[ -n "${DELETE_OLD_DAYS}" ]]; then
  if [[ ! "${DELETE_OLD_DAYS}" =~ ^[0-9]+$ ]]; then
    echo "Invalid days value: ${DELETE_OLD_DAYS}" >&2
    exit 1
  fi
  delete_old_backups "${DELETE_OLD_DAYS}"
  exit 0
fi

# 处理依赖检查模式
if [[ ${CHECK_DEPS} -eq 1 ]]; then
  check_dependencies
  exit $?
fi

if [[ ${DIFF_MODE} -eq 1 ]]; then
  # Run diff instead of restore
  DIFF_SCRIPT="${SCRIPT_DIR}/openclaw-diff.sh"
  if [[ ! -x "${DIFF_SCRIPT}" ]]; then
    echo "Error: diff script not found: ${DIFF_SCRIPT}" >&2
    exit 1
  fi
  
  # If no backup specified, show list and ask
  if [[ -z "${BACKUP_DIR}" ]]; then
    list_available_backups
    printf '\nEnter backup number to diff (or timestamp): '
    local choice
    read -r choice
    
    # Check if numeric choice
    if [[ "$choice" =~ ^[0-9]+$ ]]; then
      local backups=()
      while IFS= read -r -d '' dir; do
        local name
        name=$(basename "$dir")
        [[ "$name" == ".snapshots" ]] && continue
        if [[ -f "$dir/workspace.tar.gz" ]]; then
          backups+=("$name")
        fi
      done < <(find "${BACKUP_ROOT}" -mindepth 1 -maxdepth 1 -type d -print0 2>/dev/null | sort -z -r)
      
      if [[ "$choice" -ge 1 && "$choice" -le ${#backups[@]} ]]; then
        BACKUP_DIR="${BACKUP_ROOT}/${backups[$((choice-1))]}"
      else
        echo "Invalid selection: $choice" >&2
        exit 1
      fi
    else
      # Treat as timestamp
      if [[ -d "${BACKUP_ROOT}/${choice}" ]]; then
        BACKUP_DIR="${BACKUP_ROOT}/${choice}"
      elif [[ -d "$choice" ]]; then
        BACKUP_DIR="$choice"
      else
        echo "Backup not found: $choice" >&2
        exit 1
      fi
    fi
  fi
  
  exec "${DIFF_SCRIPT}" --from "${BACKUP_DIR}" --format "${DIFF_FORMAT}"
fi

if [[ ${USE_LATEST} -eq 1 ]]; then
  BACKUP_DIR="$(get_latest_backup)"
  log "Using latest backup: $(basename "$BACKUP_DIR")"
fi

# 如果没有指定备份目录，进入交互模式
if [[ -z "${BACKUP_DIR}" ]]; then
  interactive_select_backup
fi

BACKUP_DIR="$(cd "${BACKUP_DIR}" && pwd)"
HOME_DIR="${HOME}"
STATE_DIR="${HOME_DIR}/.openclaw"
WORKSPACE_TARGET="${STATE_DIR}/workspace"
EXTENSIONS_TARGET="${STATE_DIR}/extensions"
CONFIG_TARGET="${STATE_DIR}/openclaw.json"
if [[ -n "${OPENCLAW_WORKSPACE_DIR:-}" ]]; then
  ENV_FILE="${OPENCLAW_WORKSPACE_DIR}/.env.backup"
  SECRET_FILE="${OPENCLAW_WORKSPACE_DIR}/.env.backup.secret"
else
  BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
  ENV_FILE="${BASE_DIR}/.env.backup"
  SECRET_FILE="${BASE_DIR}/.env.backup.secret"
fi

need_cmd() { command -v "$1" >/dev/null 2>&1 || { echo "Missing command: $1" >&2; exit 1; }; }
resolve_encrypt_pass() {
  if [[ -n "${BACKUP_ENCRYPT_PASS:-}" ]]; then
    return 0
  fi
  if [[ -f "${SECRET_FILE}" ]]; then
    # shellcheck disable=SC1090
    source "${SECRET_FILE}"
  fi
  if [[ -n "${BACKUP_ENCRYPT_PASS:-}" ]]; then
    export BACKUP_ENCRYPT_PASS
    return 0
  fi
  if [[ -t 0 ]]; then
    read -r -s -p 'Enter backup decryption password: ' BACKUP_ENCRYPT_PASS
    echo
    [[ -n "${BACKUP_ENCRYPT_PASS}" ]] || { echo "Empty decryption password" >&2; exit 1; }
    export BACKUP_ENCRYPT_PASS
    return 0
  fi
  echo "Missing BACKUP_ENCRYPT_PASS. Set env var, provide .env.backup.secret, or run interactively." >&2
  exit 1
}
run() {
  if [[ ${DRY_RUN} -eq 1 ]]; then
    printf '[restore] DRY RUN: %s\n' "$*"
  else
    eval "$@"
  fi
}

verify_backup_integrity() {
  local backup_dir="$1"
  local errors=0

  log "Verifying backup integrity..."

  if [[ -f "${backup_dir}/workspace.tar.gz" ]]; then
    if tar -tzf "${backup_dir}/workspace.tar.gz" >/dev/null 2>&1; then
      log "  ✅ workspace.tar.gz is valid"
    else
      log "  ❌ workspace.tar.gz is corrupted"
      errors=$((errors + 1))
    fi
  else
    log "  ❌ workspace.tar.gz is missing"
    errors=$((errors + 1))
  fi

  if [[ -f "${backup_dir}/extensions.tar.gz" ]]; then
    if tar -tzf "${backup_dir}/extensions.tar.gz" >/dev/null 2>&1; then
      log "  ✅ extensions.tar.gz is valid"
    else
      log "  ❌ extensions.tar.gz is corrupted"
      errors=$((errors + 1))
    fi
  fi

  if [[ -f "${backup_dir}/manifest.txt" ]]; then
    log "  ✅ manifest.txt exists"
  else
    log "  ⚠️ manifest.txt is missing"
  fi

  if [[ ${errors} -gt 0 ]]; then
    log "ERROR: Backup integrity check failed with ${errors} error(s)"
    return 1
  fi

  log "✅ Backup integrity verified"
  return 0
}

verify_restore_feasibility() {
  local backup_dir="$1"
  local temp_root
  temp_root="$(mktemp -d "${TMPDIR:-/tmp}/openclaw-restore-verify.XXXXXX")"
  trap 'rm -rf "${temp_root}"' RETURN

  log "Running restore verification (no overwrite)"
  verify_backup_integrity "$backup_dir"

  if [[ -f "${backup_dir}/checksums.sha256" ]]; then
    need_cmd sha256sum
    log "Verifying SHA-256 checksums"
    (
      cd "$backup_dir" || exit 1
      sha256sum -c checksums.sha256 >/dev/null
    ) || {
      log "ERROR: Checksum verification failed"
      return 1
    }
    log "  ✅ checksums.sha256 verified"
  else
    log "  ⚠️ checksums.sha256 missing, skip checksum verification"
  fi

  local workspace_probe="${temp_root}/workspace"
  local extensions_probe="${temp_root}/state"
  mkdir -p "$workspace_probe" "$extensions_probe"

  log "Extracting workspace archive to temp dir"
  tar -xzf "${backup_dir}/workspace.tar.gz" -C "$workspace_probe"
  if find "$workspace_probe" -mindepth 1 -maxdepth 1 | grep -q .; then
    log "  ✅ workspace archive extracted"
  else
    log "ERROR: workspace archive extracted but appears empty"
    return 1
  fi

  if [[ -f "${backup_dir}/extensions.tar.gz" ]]; then
    log "Extracting extensions archive to temp dir"
    tar -xzf "${backup_dir}/extensions.tar.gz" -C "$extensions_probe"
    log "  ✅ extensions archive extracted"
  else
    log "  ⚠️ extensions.tar.gz missing, skip extensions restore probe"
  fi

  if [[ -f "${backup_dir}/manifest.txt" ]]; then
    log "Checking manifest fields"
    grep -q '^workspace_archive=' "${backup_dir}/manifest.txt" || {
      log "ERROR: manifest.txt missing workspace_archive entry"
      return 1
    }
    log "  ✅ manifest.txt contains workspace_archive"
  fi

  if [[ -f "${backup_dir}/openclaw.json.enc" ]]; then
    resolve_encrypt_pass
    : "${BACKUP_ENCRYPT_PASS:?BACKUP_ENCRYPT_PASS is required for encrypted config verification}"
    need_cmd openssl
    log "Testing encrypted config decryption to temp dir"
    openssl enc -d -aes-256-cbc -pbkdf2 \
      -in "${backup_dir}/openclaw.json.enc" \
      -out "${temp_root}/openclaw.json" \
      -pass env:BACKUP_ENCRYPT_PASS >/dev/null 2>&1 || {
      log "ERROR: encrypted config decryption failed"
      return 1
    }
    python3 -m json.tool "${temp_root}/openclaw.json" >/dev/null 2>&1 || {
      log "ERROR: decrypted openclaw.json is not valid JSON"
      return 1
    }
    log "  ✅ encrypted config can be decrypted"
  elif [[ -f "${backup_dir}/openclaw.json" ]]; then
    python3 -m json.tool "${backup_dir}/openclaw.json" >/dev/null 2>&1 || {
      log "ERROR: openclaw.json is not valid JSON"
      return 1
    }
    log "  ✅ plain config is valid JSON"
  else
    log "  ⚠️ no config file found in backup"
  fi

  log "✅ Restore verification passed (no files overwritten)"
  return 0
}

need_cmd tar
mkdir -p "${STATE_DIR}"

if [[ ! -f "${BACKUP_DIR}/workspace.tar.gz" ]]; then
  echo "Missing workspace.tar.gz in ${BACKUP_DIR}" >&2
  exit 1
fi

if [[ ${VERIFY_RESTORE} -eq 1 ]]; then
  log "Preparing restore verification from ${BACKUP_DIR}"
  check_dependencies || exit 1
  verify_restore_feasibility "${BACKUP_DIR}"
  exit $?
fi

log "Preparing restore from ${BACKUP_DIR}"

# 自动运行依赖检查（除非是 dry-run）
if [[ ${DRY_RUN} -eq 0 ]]; then
  check_dependencies || exit 1
fi

# Verify backup integrity before restore
if [[ ${DRY_RUN} -eq 0 ]]; then
  verify_backup_integrity "${BACKUP_DIR}" || exit 1
fi

run "mkdir -p '${WORKSPACE_TARGET}'"
log "Restoring workspace"
run "tar -xzf '${BACKUP_DIR}/workspace.tar.gz' -C '${WORKSPACE_TARGET}'"

if [[ -f "${BACKUP_DIR}/extensions.tar.gz" ]]; then
  log "Restoring extensions"
  run "mkdir -p '${STATE_DIR}'"
  run "tar -xzf '${BACKUP_DIR}/extensions.tar.gz' -C '${STATE_DIR}'"
fi

if [[ -f "${BACKUP_DIR}/openclaw.json" ]]; then
  log "Restoring plain config"
  run "cp '${BACKUP_DIR}/openclaw.json' '${CONFIG_TARGET}'"
elif [[ -f "${BACKUP_DIR}/openclaw.json.enc" ]]; then
  if [[ ${DECRYPT_CONFIG} -eq 1 ]]; then
    resolve_encrypt_pass
    : "${BACKUP_ENCRYPT_PASS:?BACKUP_ENCRYPT_PASS is required for config decryption}"
    need_cmd openssl
    log "Decrypting config"
    if [[ ${DRY_RUN} -eq 1 ]]; then
      printf '[restore] DRY RUN: decrypt %s -> %s\n' "${BACKUP_DIR}/openclaw.json.enc" "${CONFIG_TARGET}"
    else
      openssl enc -d -aes-256-cbc -pbkdf2 -in "${BACKUP_DIR}/openclaw.json.enc" -out "${CONFIG_TARGET}" -pass env:BACKUP_ENCRYPT_PASS >/dev/null 2>&1
    fi
  else
    log "Encrypted config found but not decrypted (use --decrypt-config if needed)"
  fi
fi

log "Restore flow completed"
log "Recommended next steps:"
log "  1. openclaw status"
log "  2. openclaw gateway restart"
log "  3. verify Telegram / Weixin / model / plugins.allow / memory"
