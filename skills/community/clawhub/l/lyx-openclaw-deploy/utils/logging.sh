#!/bin/bash
# 日志处理工具 - V1.2
# 提供多级别日志能力：DEBUG / INFO / WARN / ERROR / SUCCESS
# 支持输出到文件和控制台，颜色可关闭

set -euo pipefail

# 日志级别枚举
LOG_LEVEL_DEBUG=0
LOG_LEVEL_INFO=1
LOG_LEVEL_WARN=2
LOG_LEVEL_ERROR=3
LOG_LEVEL_SUCCESS=4

# 全局配置
export LOG_TO_FILE="${LOG_TO_FILE:-false}"
export LOG_FILE="${LOG_FILE:-}"
export LOG_LEVEL="${LOG_LEVEL:-$LOG_LEVEL_INFO}"
export LOG_COLOR="${LOG_COLOR:-true}"

# 颜色定义（可独立开启/关闭）
if [ "$LOG_COLOR" = "true" ]; then
  export COLOR_DEBUG='\033[0;37m'   # 白色
  export COLOR_INFO='\033[0;34m'    # 蓝色
  export COLOR_WARN='\033[1;33m'    # 黄色
  export COLOR_ERROR='\033[0;31m'   # 红色
  export COLOR_SUCCESS='\033[0;32m' # 绿色
  export COLOR_BANNER='\033[1;36m'  # 青色
  export COLOR_TIMER='\033[0;36m'   # 深蓝
  export NC='\033[0m'
else
  export COLOR_DEBUG='' COLOR_INFO='' COLOR_WARN='' COLOR_ERROR=''
  export COLOR_SUCCESS='' COLOR_BANNER='' COLOR_TIMER='' NC=''
fi

# 设置日志文件
log_set_file() {
  LOG_TO_FILE=true
  LOG_FILE="$1"
  mkdir -p "$(dirname "$LOG_FILE")"
  : > "$LOG_FILE"  # 清空或创建文件
}

# 写入日志文件
_log_file() {
  [ "$LOG_TO_FILE" = "true" ] && [ -n "$LOG_FILE" ] && echo "$1" >> "$LOG_FILE"
}

# 各级别日志函数
log_debug() {
  [ "$LOG_LEVEL" -le "$LOG_LEVEL_DEBUG" ] || return 0
  local msg="[$(date '+%H:%M:%S')] [DEBUG] $*"
  [ "$LOG_COLOR" = "true" ] && echo -e "${COLOR_DEBUG}${msg}${NC}" || echo "$msg"
  _log_file "$msg"
}

log_info() {
  [ "$LOG_LEVEL" -le "$LOG_LEVEL_INFO" ] || return 0
  local msg="[$(date '+%H:%M:%S')] [INFO]  $*"
  [ "$LOG_COLOR" = "true" ] && echo -e "${COLOR_INFO}${msg}${NC}" || echo "$msg"
  _log_file "$msg"
}

log_warn() {
  [ "$LOG_LEVEL" -le "$LOG_LEVEL_WARN" ] || return 0
  local msg="[$(date '+%H:%M:%S')] [WARN]  $*"
  [ "$LOG_COLOR" = "true" ] && echo -e "${COLOR_WARN}${msg}${NC}" || echo "$msg"
  _log_file "$msg"
}

log_error() {
  [ "$LOG_LEVEL" -le "$LOG_LEVEL_ERROR" ] || return 0
  local msg="[$(date '+%H:%M:%S')] [ERROR] $*"
  [ "$LOG_COLOR" = "true" ] && echo -e "${COLOR_ERROR}${msg}${NC}" || echo "$msg"
  _log_file "$msg"
}

log_success() {
  [ "$LOG_LEVEL" -le "$LOG_LEVEL_SUCCESS" ] || return 0
  local msg="[$(date '+%H:%M:%S')] [OK]    $*"
  [ "$LOG_COLOR" = "true" ] && echo -e "${COLOR_SUCCESS}${msg}${NC}" || echo "$msg"
  _log_file "$msg"
}

# Banner 输出（用于阶段分隔）
log_banner() {
  local msg="$*"
  local sep="$(printf '=%.0s' $(seq 1 ${#msg}))"
  [ "$LOG_COLOR" = "true" ] && echo -e "${COLOR_BANNER}${sep}${NC}"
  [ "$LOG_COLOR" = "true" ] && echo -e "${COLOR_BANNER}  $msg${NC}"
  [ "$LOG_COLOR" = "true" ] && echo -e "${COLOR_BANNER}${sep}${NC}"
  _log_file "[$sec] === $msg ==="
}

# 耗时计时器
timer_start() { _timer_start=$(date +%s); }
timer_stop() {
  local label="${1:-耗时}"
  local end; end=$(date +%s)
  local elapsed=$((end - ${_timer_start:-end}))
  local msg="[$label] ${elapsed}s"
  [ "$LOG_COLOR" = "true" ] && echo -e "${COLOR_TIMER}${msg}${NC}" || echo "$msg"
  _log_file "$msg"
}

# 分隔线
log_divider() {
  echo "──────────────────────────────────────────"
}
