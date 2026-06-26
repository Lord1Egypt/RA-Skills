#!/bin/bash
# Li_Feishu_Audio 公共函数库
# 用法: source $(dirname "$0")/common.sh

# 防止重复加载
[ -n "$LI_FEISHU_COMMON_LOADED" ] && return
LI_FEISHU_COMMON_LOADED=1

# 颜色输出
export RED='\033[0;31m'
export GREEN='\033[0;32m'
export YELLOW='\033[1;33m'
export BLUE='\033[0;34m'
export CYAN='\033[0;36m'
export NC='\033[0m'

# 日志级别
LOG_LEVEL=${LOG_LEVEL:-INFO}

# 日志函数
log_debug() { [ "$LOG_LEVEL" = "DEBUG" ] && echo -e "${CYAN}[DEBUG]${NC} $1" >&2; }
log_info() { echo -e "${BLUE}[INFO]${NC} $1" >&2; }
log_ok() { echo -e "${GREEN}[OK]${NC} $1" >&2; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1" >&2; }
log_error() { echo -e "${RED}[ERROR]${NC} $1" >&2; }

# 带重试的执行函数 - 安全版本，避免 eval 注入
run_with_retry() {
    local max_retries=${1:-3}
    local delay=${2:-3}
    shift 2
    local attempt=1
    
    while [ $attempt -le $max_retries ]; do
        log_info "尝试执行 ($attempt/$max_retries)..."
        # 使用 "$@" 直接执行命令，避免 eval 注入风险
        if "$@"; then
            return 0
        fi
        attempt=$((attempt + 1))
        if [ $attempt -le $max_retries ]; then
            log_warn "执行失败，${delay}秒后重试..."
            sleep $delay
        fi
    done
    return 1
}

# 检查命令是否存在
check_command() {
    command -v "$1" &> /dev/null
}

# 获取命令版本 - 安全版本，避免 eval 注入
get_command_version() {
    local cmd=$1
    local version_cmd=${2:-"$1 --version"}
    
    if check_command "$cmd"; then
        # 使用 bash -c 执行版本命令，比 eval 更安全
        bash -c "$version_cmd" 2>/dev/null | head -1 || echo "版本未知"
    else
        echo "未安装"
    fi
}

# 检查 Python 版本
check_python_version() {
    local min_version=${1:-3.9}
    python3 -c "import sys; exit(0 if sys.version_info >= tuple(map(int, '$min_version'.split('.'))) else 1)" 2>/dev/null
}

# 检查虚拟环境
check_venv() {
    local venv_dir=${1:-}
    [ -n "$venv_dir" ] && [ -d "$venv_dir" ] && [ -f "$venv_dir/bin/python" ]
}

# 清理旧临时文件 (保留最近24小时的文件)
cleanup_old_temp_files() {
    local pattern=${1:-"/tmp/tts-*"}
    local hours=${2:-24}
    
    log_info "清理超过 ${hours} 小时的临时文件..."
    find /tmp -name "$(basename "$pattern")" -type f -mmin +$((hours * 60)) -delete 2>/dev/null || true
}

# 验证音频文件
validate_audio_file() {
    local file=$1
    
    # 检查文件是否存在
    if [ ! -f "$file" ]; then
        log_error "音频文件不存在: $file"
        return 1
    fi
    
    # 检查文件大小
    local size
    size=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file" 2>/dev/null || echo "0")
    if [ "$size" -eq 0 ]; then
        log_error "音频文件为空: $file"
        return 1
    fi
    
    # 使用 ffprobe 验证文件完整性
    if check_command ffprobe; then
        if ! ffprobe -v error -show_format -show_streams "$file" &>/dev/null; then
            log_error "音频文件格式无效或已损坏: $file"
            return 1
        fi
    fi
    
    return 0
}

# 获取文件大小 (人类可读)
get_file_size_human() {
    local file=$1
    local size
    size=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file" 2>/dev/null || echo "0")
    numfmt --to=iec "$size" 2>/dev/null || echo "${size} bytes"
}

# 检查磁盘空间
check_disk_space() {
    local path=${1:-/tmp}
    local min_mb=${2:-100}
    
    local avail_kb
    avail_kb=$(df "$path" 2>/dev/null | tail -1 | awk '{print $4}')
    local avail_mb=$((avail_kb / 1024))
    
    if [ "$avail_mb" -lt "$min_mb" ]; then
        log_error "磁盘空间不足: ${avail_mb}MB (需要至少 ${min_mb}MB)"
        return 1
    fi
    
    log_info "磁盘空间充足: ${avail_mb}MB"
    return 0
}

# 设置脚本目录变量
set_skill_dirs() {
    # 如果已经设置则跳过
    [ -n "$SKILL_DIR" ] && return 0
    
    # 获取脚本所在目录
    local script_dir="${SCRIPT_DIR:-}"
    if [ -z "$script_dir" ]; then
        script_dir="$(cd "$(dirname "${BASH_SOURCE[1]:-$0}")" && pwd)"
    fi
    
    export SCRIPTS_DIR="$script_dir"
    export SKILL_DIR="$(cd "$script_dir/.." && pwd)"
    export VENV_DIR="${VENV_DIR:-${SKILL_DIR}/.venv}"
    export MODEL_DIR="${FAST_WHISPER_MODEL_DIR:-${HOME}/.fast-whisper-models}"
    
    log_debug "SKILL_DIR: $SKILL_DIR"
    log_debug "SCRIPTS_DIR: $SCRIPTS_DIR"
    log_debug "VENV_DIR: $VENV_DIR"
    log_debug "MODEL_DIR: $MODEL_DIR"
}

# 加载 .env 配置文件
load_env_config() {
    local env_file="${1:-${SCRIPTS_DIR}/.env}"
    
    if [ -f "$env_file" ]; then
        log_debug "加载配置文件: $env_file"
        # 安全加载，忽略注释和空行
        while IFS='=' read -r key value; do
            # 跳过注释和空行
            [[ "$key" =~ ^[[:space:]]*# ]] && continue
            [[ -z "$key" ]] && continue
            # 去除空格
            key=$(echo "$key" | xargs)
            value=$(echo "$value" | xargs)
            # 导出变量
            export "$key=$value"
        done < "$env_file"
    else
        log_warn "配置文件不存在: $env_file"
    fi
}

# 信号处理：清理函数
cleanup_on_exit() {
    local exit_code=$?
    if [ -n "$TEMP_FILES" ]; then
        for file in $TEMP_FILES; do
            [ -f "$file" ] && rm -f "$file"
        done
    fi
    exit $exit_code
}

# 注册清理函数
register_cleanup() {
    trap cleanup_on_exit EXIT INT TERM
}

# 添加临时文件到清理列表
add_temp_file() {
    TEMP_FILES="${TEMP_FILES:-} $1"
}