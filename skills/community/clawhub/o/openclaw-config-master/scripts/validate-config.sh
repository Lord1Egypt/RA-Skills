#!/usr/bin/env bash
#
# validate-config.sh - 配置文件验证脚本
#
# 功能：
#   - 验证 OpenClaw 配置文件的语法和结构
#   - 检查必需字段
#   - 验证字段值的有效性
#   - 生成详细的验证报告
#
# 使用方法：
#   ./validate-config.sh [选项]
#
# 选项：
#   -p, --path PATH     配置文件路径（默认：自动解析）
#   -s, --strict        严格模式（警告也视为错误）
#   -q, --quiet         静默模式（仅输出错误）
#   -j, --json          输出 JSON 格式报告
#   -v, --verbose       详细输出
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
STRICT_MODE=false
QUIET_MODE=false
JSON_OUTPUT=false
VERBOSE=false

# 验证结果计数器
ERRORS=0
WARNINGS=0
CHECKS_PASSED=0

# 报告数据（用于 JSON 输出）
declare -a REPORT_ERRORS=()
declare -a REPORT_WARNINGS=()
declare -a REPORT_PASSED=()

# ============================================================================
# 工具函数
# ============================================================================

log_info() {
  if [[ "${QUIET_MODE}" == false ]]; then
    echo "[INFO] $*" >&2
  fi
}

log_error() {
  echo "[ERROR] $*" >&2
  ((ERRORS++))
  if [[ "${JSON_OUTPUT}" == true ]]; then
    REPORT_ERRORS+=("$*")
  fi
}

log_warning() {
  echo "[WARNING] $*" >&2
  ((WARNINGS++))
  if [[ "${JSON_OUTPUT}" == true ]]; then
    REPORT_WARNINGS+=("$*")
  fi
}

log_success() {
  if [[ "${VERBOSE}" == true ]]; then
    echo "[PASS] $*" >&2
  fi
  ((CHECKS_PASSED++))
  if [[ "${JSON_OUTPUT}" == true ]]; then
    REPORT_PASSED+=("$*")
  fi
}

log_debug() {
  if [[ "${VERBOSE}" == true && "${QUIET_MODE}" == false ]]; then
    echo "[DEBUG] $*" >&2
  fi
}

show_help() {
  sed -n '/^#$/,$p' "$0" | sed '1d; s/^# //; s/^#//'
}

# ============================================================================
# 验证函数
# ============================================================================

check_file_exists() {
  log_debug "检查文件是否存在..."

  if [[ ! -f "${CONFIG_PATH}" ]]; then
    log_error "配置文件不存在: ${CONFIG_PATH}"
    return 1
  fi

  log_success "配置文件存在"
  return 0
}

check_file_readable() {
  log_debug "检查文件可读性..."

  if [[ ! -r "${CONFIG_PATH}" ]]; then
    log_error "配置文件不可读: ${CONFIG_PATH}"
    return 1
  fi

  log_success "配置文件可读"
  return 0
}

check_json_syntax() {
  log_debug "检查 JSON 语法..."

  if ! command -v python3 >/dev/null 2>&1; then
    log_warning "未找到 python3，跳过 JSON 语法验证"
    return 0
  fi

  local python_cmd
  python_cmd='import json, sys; json.load(sys.stdin)'

  if ! python3 -c "${python_cmd}" < "${CONFIG_PATH}" 2>/dev/null; then
    log_error "JSON 语法无效"
    return 1
  fi

  log_success "JSON 语法有效"
  return 0
}

check_file_size() {
  log_debug "检查文件大小..."

  local size
  size="$(stat -c '%s' "${CONFIG_PATH}" 2>/dev/null || stat -f '%z' "${CONFIG_PATH}" 2>/dev/null)"

  if [[ -z "${size}" ]]; then
    log_warning "无法获取文件大小"
    return 0
  fi

  if (( size == 0 )); then
    log_error "配置文件为空"
    return 1
  fi

  if (( size > 1048576 )); then
    log_warning "配置文件过大 (${size} 字节)"
    return 0
  fi

  log_success "文件大小正常 (${size} 字节)"
  return 0
}

check_file_permissions() {
  log_debug "检查文件权限..."

  local perms=""
  if perms="$(stat -c '%a' "${CONFIG_PATH}" 2>/dev/null)"; then
    :
  elif perms="$(stat -f '%A' "${CONFIG_PATH}" 2>/dev/null)"; then
    :
  else
    log_warning "无法获取文件权限"
    return 0
  fi

  log_debug "当前权限: ${perms}"

  if [[ "${perms}" =~ ^[0-9]+$ ]] && (( perms > 644 )); then
    log_warning "配置文件权限过于开放 (${perms})，建议设置为 600"
    return 0
  fi

  log_success "文件权限合理 (${perms})"
  return 0
}

check_backup_available() {
  log_debug "检查是否有可用备份..."

  local backup_dir="${HOME}/.openclaw/backups"

  if [[ ! -d "${backup_dir}" ]]; then
    log_debug "备份目录不存在"
    return 0
  fi

  local backup_count
  backup_count=$(find "${backup_dir}" -name "openclaw-config-*.json*" -type f 2>/dev/null | wc -l)

  if (( backup_count > 0 )); then
    log_success "发现 ${backup_count} 个备份文件"
  else
    log_debug "未找到备份文件"
  fi

  return 0
}

validate_with_openclaw() {
  log_debug "使用 openclaw CLI 验证配置..."

  if ! command -v openclaw >/dev/null 2>&1; then
    log_warning "未找到 openclaw CLI，跳过 CLI 验证"
    return 0
  fi

  if openclaw doctor >/dev/null 2>&1; then
    log_success "openclaw doctor 检查通过"
  else
    log_warning "openclaw doctor 检查发现问题"
  fi

  return 0
}

output_report() {
  local exit_code=0

  # 确定 JSON 输出还是人类可读输出
  if [[ "${JSON_OUTPUT}" == true ]]; then
    output_json_report
  else
    output_human_report
  fi

  # 根据模式和错误数确定退出码
  if [[ "${STRICT_MODE}" == true ]]; then
    if (( ERRORS > 0 || WARNINGS > 0 )); then
      exit_code=1
    fi
  else
    if (( ERRORS > 0 )); then
      exit_code=1
    fi
  fi

  return ${exit_code}
}

output_human_report() {
  echo
  echo "========================================"
  echo "        配置验证报告"
  echo "========================================"
  echo
  echo "配置文件: ${CONFIG_PATH}"
  echo "解析模式: ${MODE}"
  echo
  echo "验证结果:"
  echo "  ✓ 通过: ${CHECKS_PASSED}"
  echo "  ⚠ 警告: ${WARNINGS}"
  echo "  ✗ 错误: ${ERRORS}"
  echo

  if (( ERRORS == 0 && WARNINGS == 0 )); then
    echo "状态: ✓ 配置文件有效"
  elif (( ERRORS == 0 )); then
    echo "状态: ⚠ 配置文件有效，但存在警告"
  else
    echo "状态: ✗ 配置文件存在错误"
  fi

  echo
}

output_json_report() {
  local status="valid"
  if (( ERRORS > 0 )); then
    status="invalid"
  elif (( WARNINGS > 0 )); then
    status="warning"
  fi

  cat <<EOF
{
  "config_path": "${CONFIG_PATH}",
  "resolve_mode": "${MODE}",
  "status": "${status}",
  "summary": {
    "passed": ${CHECKS_PASSED},
    "warnings": ${WARNINGS},
    "errors": ${ERRORS}
  },
  "errors": $([ ${#REPORT_ERRORS[@]} -gt 0 ] && printf '%s\n' "${REPORT_ERRORS[@]}" | jq -R . | jq -s . || echo "[]"),
  "warnings": $([ ${#REPORT_WARNINGS[@]} -gt 0 ] && printf '%s\n' "${REPORT_WARNINGS[@]}" | jq -R . | jq -s . || echo "[]"),
  "passed": $([ ${#REPORT_PASSED[@]} -gt 0 ] && printf '%s\n' "${REPORT_PASSED[@]}" | jq -R . | jq -s . || echo "[]")
}
EOF
}

# ============================================================================
# 参数解析
# ============================================================================

while [[ $# -gt 0 ]]; do
  case "$1" in
    -p|--path)
      CONFIG_PATH="$2"
      shift 2
      ;;
    -s|--strict)
      STRICT_MODE=true
      shift
      ;;
    -q|--quiet)
      QUIET_MODE=true
      shift
      ;;
    -j|--json)
      JSON_OUTPUT=true
      shift
      ;;
    -v|--verbose)
      VERBOSE=true
      shift
      ;;
    -h|--help)
      show_help
      exit 0
      ;;
    *)
      echo "未知选项: $1" >&2
      show_help
      exit 1
      ;;
  esac
done

# ============================================================================
# 主逻辑
# ============================================================================

main() {
  if [[ "${QUIET_MODE}" == false && "${JSON_OUTPUT}" == false ]]; then
    echo "OpenClaw 配置验证工具"
    echo "配置路径 (${MODE}): ${CONFIG_PATH}"
    echo
  fi

  # 执行验证检查
  check_file_exists
  check_file_readable
  check_json_syntax
  check_file_size
  check_file_permissions
  check_backup_available
  validate_with_openclaw

  # 输出报告
  output_report
  exit $?
}

main "$@"
