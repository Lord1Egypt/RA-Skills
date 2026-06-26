#!/usr/bin/env bash
#
# backup-config.sh - 配置文件备份脚本
#
# 功能：
#   - 备份 OpenClaw 配置文件到指定目录
#   - 支持自动命名（时间戳）
#   - 支持压缩备份
#   - 支持备份历史管理
#
# 使用方法：
#   ./backup-config.sh [选项]
#
# 选项：
#   -d, --dir DIR       备份目录（默认：~/.openclaw/backups）
#   -c, --compress      使用 gzip 压缩备份
#   -k, --keep NUM      保留最近 N 个备份（默认：10）
#   -n, --name NAME     自定义备份名称（可选）
#   -h, --help          显示帮助信息
#

set -euo pipefail

# ============================================================================
# 配置路径解析函数（与 openclaw-config-check.sh 保持一致）
# ============================================================================

resolve_config_path() {
  if [[ -n "${OPENCLAW_CONFIG_PATH:-}" ]]; then
    echo "${OPENCLAW_CONFIG_PATH}"
    return 0
  fi

  local state_dir
  state_dir="${OPENCLAW_STATE_DIR:-${CLAWDBOT_STATE_DIR:-$HOME/.openclaw}}"
  echo "${state_dir%/}/openclaw.json"
}

resolve_mode() {
  if [[ -n "${OPENCLAW_CONFIG_PATH:-}" ]]; then
    echo "OPENCLAW_CONFIG_PATH"
    return 0
  fi
  if [[ -n "${OPENCLAW_STATE_DIR:-}" || -n "${CLAWDBOT_STATE_DIR:-}" ]]; then
    echo "OPENCLAW_STATE_DIR"
    return 0
  fi
  echo "default"
}

# ============================================================================
# 默认配置
# ============================================================================

CONFIG_PATH="$(resolve_config_path)"
MODE="$(resolve_mode)"
BACKUP_DIR="${HOME}/.openclaw/backups"
COMPRESS=false
KEEP_COUNT=10
CUSTOM_NAME=""

# ============================================================================
# 工具函数
# ============================================================================

log_info() {
  echo "[INFO] $*" >&2
}

log_error() {
  echo "[ERROR] $*" >&2
}

log_success() {
  echo "[SUCCESS] $*" >&2
}

show_help() {
  sed -n '/^#$/,$p' "$0" | sed '1d; s/^# //; s/^#//'
}

cleanup_old_backups() {
  local backup_dir="$1"
  local keep_count="$2"

  log_info "清理旧备份（保留最近 ${keep_count} 个）..."

  local count
  count=$(find "${backup_dir}" -name "openclaw-config-*.json*" -type f | wc -l)

  if (( count > keep_count )); then
    local delete_count=$((count - keep_count))
    log_info "将删除 ${delete_count} 个旧备份"

    find "${backup_dir}" -name "openclaw-config-*.json*" -type f \
      | sort -r \
      | tail -n "${delete_count}" \
      | xargs rm -f

    log_success "已清理 ${delete_count} 个旧备份"
  else
    log_info "备份数量未超过限制，无需清理"
  fi
}

# ============================================================================
# 参数解析
# ============================================================================

while [[ $# -gt 0 ]]; do
  case "$1" in
    -d|--dir)
      BACKUP_DIR="$2"
      shift 2
      ;;
    -c|--compress)
      COMPRESS=true
      shift
      ;;
    -k|--keep)
      KEEP_COUNT="$2"
      shift 2
      ;;
    -n|--name)
      CUSTOM_NAME="$2"
      shift 2
      ;;
    -h|--help)
      show_help
      exit 0
      ;;
    *)
      log_error "未知选项: $1"
      show_help
      exit 1
      ;;
  esac
done

# ============================================================================
# 主逻辑
# ============================================================================

main() {
  log_info "OpenClaw 配置备份工具"
  log_info "配置路径 (${MODE}): ${CONFIG_PATH}"

  # 检查配置文件是否存在
  if [[ ! -f "${CONFIG_PATH}" ]]; then
    log_error "配置文件不存在: ${CONFIG_PATH}"
    exit 1
  fi

  # 创建备份目录
  if [[ ! -d "${BACKUP_DIR}" ]]; then
    log_info "创建备份目录: ${BACKUP_DIR}"
    mkdir -p "${BACKUP_DIR}"
  fi

  # 生成备份文件名
  local timestamp
  timestamp="$(date '+%Y%m%d-%H%M%S')"

  if [[ -n "${CUSTOM_NAME}" ]]; then
    backup_file="${BACKUP_DIR}/openclaw-config-${CUSTOM_NAME}-${timestamp}.json"
  else
    backup_file="${BACKUP_DIR}/openclaw-config-${timestamp}.json"
  fi

  # 执行备份
  log_info "备份配置文件到: ${backup_file}"

  if cp "${CONFIG_PATH}" "${backup_file}"; then
    log_success "备份成功"

    # 获取文件大小
    local size
    size="$(du -h "${backup_file}" | cut -f1)"
    log_info "备份大小: ${size}"

    # 压缩备份（如果需要）
    if [[ "${COMPRESS}" == true ]]; then
      log_info "压缩备份文件..."
      if gzip "${backup_file}"; then
        backup_file="${backup_file}.gz"
        size="$(du -h "${backup_file}" | cut -f1)"
        log_success "压缩完成: ${backup_file} (${size})"
      else
        log_error "压缩失败，保留未压缩备份"
      fi
    fi

    # 清理旧备份
    cleanup_old_backups "${BACKUP_DIR}" "${KEEP_COUNT}"

    # 列出当前备份
    log_info "当前备份列表:"
    ls -lh "${BACKUP_DIR}"/openclaw-config-*.json* 2>/dev/null || true

    log_success "备份完成"
    exit 0
  else
    log_error "备份失败"
    exit 1
  fi
}

main "$@"
