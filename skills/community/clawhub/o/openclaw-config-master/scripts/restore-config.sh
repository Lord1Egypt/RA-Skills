#!/usr/bin/env bash
#
# restore-config.sh - 配置文件恢复脚本
#
# 功能：
#   - 从备份恢复 OpenClaw 配置文件
#   - 支持列出可用备份
#   - 支持交互式选择备份
#   - 支持恢复前备份当前配置
#
# 使用方法：
#   ./restore-config.sh [选项] [备份文件]
#
# 选项：
#   -d, --dir DIR       备份目录（默认：~/.openclaw/backups）
#   -l, --list          列出可用备份
#   -b, --backup        恢复前备份当前配置
#   -f, --force         强制恢复，不提示确认
#   -h, --help          显示帮助信息
#
# 参数：
#   备份文件            要恢复的备份文件路径（可选，未提供时交互选择）
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
LIST_ONLY=false
BACKUP_BEFORE_RESTORE=false
FORCE=false
SELECTED_BACKUP=""

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

log_warning() {
  echo "[WARNING] $*" >&2
}

show_help() {
  sed -n '/^#$/,$p' "$0" | sed '1d; s/^# //; s/^#//'
}

list_backups() {
  log_info "可用备份列表:"
  echo

  local backups
  backups=$(find "${BACKUP_DIR}" -name "openclaw-config-*.json*" -type f 2>/dev/null | sort -r)

  if [[ -z "${backups}" ]]; then
    log_warning "未找到任何备份文件"
    return 1
  fi

  local index=1
  echo "${backups}" | while read -r backup; do
    local size
    local date
    size="$(du -h "${backup}" | cut -f1)"

    # 从文件名提取时间戳
    local filename
    filename="$(basename "${backup}")"
    date="$(echo "${filename}" | grep -oP '\d{8}-\d{6}' || echo '未知')"

    # 判断是否压缩
    local is_compressed=""
    if [[ "${backup}" =~ \.gz$ ]]; then
      is_compressed=" [已压缩]"
    fi

    printf "%3d) %s  %s  %s%s\n" "${index}" "${date}" "${size}" "${filename}" "${is_compressed}"
    ((index++))
  done

  echo
  log_info "备份目录: ${BACKUP_DIR}"
  return 0
}

select_backup_interactive() {
  local backups
  backups=()

  while IFS= read -r backup; do
    backups+=("${backup}")
  done < <(find "${BACKUP_DIR}" -name "openclaw-config-*.json*" -type f 2>/dev/null | sort -r)

  if [[ ${#backups[@]} -eq 0 ]]; then
    log_error "未找到任何备份文件"
    return 1
  fi

  log_info "选择要恢复的备份:"
  echo

  local index=1
  for backup in "${backups[@]}"; do
    local size
    local date
    size="$(du -h "${backup}" | cut -f1)"
    local filename
    filename="$(basename "${backup}")"
    date="$(echo "${filename}" | grep -oP '\d{8}-\d{6}' || echo '未知')"

    printf "%3d) %s  %s  %s\n" "${index}" "${date}" "${size}" "${filename}"
    ((index++))
  done

  echo
  read -rp "请输入备份编号 (1-${#backups[@]}): " selection

  if ! [[ "${selection}" =~ ^[0-9]+$ ]] || (( selection < 1 || selection > ${#backups[@]} )); then
    log_error "无效的选择"
    return 1
  fi

  SELECTED_BACKUP="${backups[$((selection - 1))]}"
  log_info "已选择备份: ${SELECTED_BACKUP}"
  return 0
}

backup_current_config() {
  if [[ ! -f "${CONFIG_PATH}" ]]; then
    log_warning "当前配置文件不存在，跳过备份"
    return 0
  fi

  local pre_restore_backup
  local timestamp
  timestamp="$(date '+%Y%m%d-%H%M%S')"
  pre_restore_backup="${BACKUP_DIR}/pre-restore-${timestamp}.json"

  log_info "恢复前备份当前配置到: ${pre_restore_backup}"

  if mkdir -p "${BACKUP_DIR}" && cp "${CONFIG_PATH}" "${pre_restore_backup}"; then
    log_success "当前配置已备份"
    return 0
  else
    log_error "备份当前配置失败"
    return 1
  fi
}

restore_backup() {
  local backup_file="$1"

  # 检查备份文件是否存在
  if [[ ! -f "${backup_file}" ]]; then
    log_error "备份文件不存在: ${backup_file}"
    return 1
  fi

  # 确认恢复操作
  if [[ "${FORCE}" == false ]]; then
    echo
    log_warning "即将恢复配置文件！"
    log_info "备份来源: ${backup_file}"
    log_info "目标位置: ${CONFIG_PATH}"
    echo
    read -rp "确认恢复？[y/N] " confirm

    if [[ "${confirm}" != "y" && "${confirm}" != "Y" ]]; then
      log_info "恢复操作已取消"
      return 1
    fi
  fi

  # 恢复前备份当前配置
  if [[ "${BACKUP_BEFORE_RESTORE}" == true ]]; then
    if ! backup_current_config; then
      log_error "恢复前备份失败，终止恢复操作"
      return 1
    fi
  fi

  # 确保目标目录存在
  local target_dir
  target_dir="$(dirname "${CONFIG_PATH}")"

  if [[ ! -d "${target_dir}" ]]; then
    log_info "创建目标目录: ${target_dir}"
    mkdir -p "${target_dir}"
  fi

  # 执行恢复
  log_info "正在恢复配置文件..."

  local temp_file="${target_dir}/.openclaw.json.tmp"

  # 处理压缩备份
  if [[ "${backup_file}" =~ \.gz$ ]]; then
    if ! gunzip -c "${backup_file}" > "${temp_file}"; then
      log_error "解压备份文件失败"
      rm -f "${temp_file}"
      return 1
    fi
  else
    if ! cp "${backup_file}" "${temp_file}"; then
      log_error "复制备份文件失败"
      rm -f "${temp_file}"
      return 1
    fi
  fi

  # 原子移动
  if mv "${temp_file}" "${CONFIG_PATH}"; then
    log_success "配置文件恢复成功"
    log_info "已恢复到: ${CONFIG_PATH}"

    # 设置适当的权限
    chmod 600 "${CONFIG_PATH}"
    log_info "已设置权限为 600"

    return 0
  else
    log_error "恢复失败"
    rm -f "${temp_file}"
    return 1
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
    -l|--list)
      LIST_ONLY=true
      shift
      ;;
    -b|--backup)
      BACKUP_BEFORE_RESTORE=true
      shift
      ;;
    -f|--force)
      FORCE=true
      shift
      ;;
    -h|--help)
      show_help
      exit 0
      ;;
    -*)
      log_error "未知选项: $1"
      show_help
      exit 1
      ;;
    *)
      SELECTED_BACKUP="$1"
      shift
      ;;
  esac
done

# ============================================================================
# 主逻辑
# ============================================================================

main() {
  log_info "OpenClaw 配置恢复工具"
  log_info "配置路径 (${MODE}): ${CONFIG_PATH}"
  echo

  # 仅列出备份
  if [[ "${LIST_ONLY}" == true ]]; then
    list_backups
    exit $?
  fi

  # 确定要恢复的备份
  if [[ -z "${SELECTED_BACKUP}" ]]; then
    if ! select_backup_interactive; then
      exit 1
    fi
  else
    # 如果提供了路径，使用它
    if [[ ! "${SELECTED_BACKUP}" =~ ^/ ]]; then
      # 相对路径，在备份目录中查找
      SELECTED_BACKUP="${BACKUP_DIR}/${SELECTED_BACKUP}"
    fi
  fi

  # 执行恢复
  if restore_backup "${SELECTED_BACKUP}"; then
    echo
    log_success "恢复完成！"
    echo
    log_info "建议运行以下命令验证配置:"
    echo "  ./openclaw-config-check.sh"
    exit 0
  else
    log_error "恢复失败"
    exit 1
  fi
}

main "$@"
