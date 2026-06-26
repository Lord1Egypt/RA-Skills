#!/usr/bin/env bash
#
# 健康检查脚本
# 功能：检查飞书语音交互服务的各项依赖和配置
#

set -euo pipefail

# 获取脚本目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

# 激活虚拟环境（如果存在）
VENV_ACTIVATE="$SKILL_DIR/.venv/bin/activate"
if [[ -f "$VENV_ACTIVATE" ]]; then
    source "$VENV_ACTIVATE"
fi

# 颜色定义
readonly COLOR_RED='\033[0;31m'
readonly COLOR_GREEN='\033[0;32m'
readonly COLOR_YELLOW='\033[1;33m'
readonly COLOR_BLUE='\033[0;34m'
readonly COLOR_NC='\033[0m' # No Color

# 状态计数器
ERRORS=0
WARNINGS=0

# ============================================================
# 日志函数（唯一实现，供所有脚本使用）
# ============================================================

log_info() {
    echo -e "${COLOR_BLUE}[INFO]${COLOR_NC} $1"
}

log_success() {
    echo -e "${COLOR_GREEN}[PASS]${COLOR_NC} $1"
}

log_warning() {
    echo -e "${COLOR_YELLOW}[WARN]${COLOR_NC} $1"
    ((WARNINGS++)) || true
}

log_error() {
    echo -e "${COLOR_RED}[FAIL]${COLOR_NC} $1"
    ((ERRORS++)) || true
}

log_section() {
    echo ""
    echo -e "${COLOR_BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${COLOR_NC}"
    echo -e "${COLOR_BLUE}  $1${COLOR_NC}"
    echo -e "${COLOR_BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${COLOR_NC}"
}

# ============================================================
# 辅助函数
# ============================================================

# 检查命令是否存在
check_command() {
    local cmd="$1"
    local desc="${2:-$1}"
    
    if command -v "$cmd" &>/dev/null; then
        log_success "$desc 已安装"
        return 0
    else
        log_error "$desc 未安装"
        return 1
    fi
}

# 检查 Python 包
check_python_package() {
    local package="$1"
    local desc="${2:-$1}"
    
    if python3 -c "import $package" 2>/dev/null; then
        local version
        version=$(python3 -c "import $package; print(getattr($package, '__version__', 'unknown'))" 2>/dev/null || echo "unknown")
        log_success "$desc 已安装 (版本: $version)"
        return 0
    else
        log_error "$desc 未安装"
        return 1
    fi
}

# 检查 Python 包（通过 import 检查，兼容无 pip 的虚拟环境）
check_pip_package() {
    local package="$1"
    local desc="${2:-$1}"
    
    # 使用 python -c 导入包并获取版本（兼容无 pip 的环境）
    local version
    version=$(python3 -c "import $package; print(getattr($package, '__version__', 'unknown'))" 2>/dev/null || echo "")
    
    if [[ -n "$version" ]]; then
        log_success "$desc 已安装 (版本：$version)"
        return 0
    else
        log_error "$desc 未安装"
        return 1
    fi
}

# 检查目录可写
check_directory_writable() {
    local dir="$1"
    local desc="${2:-$1}"
    
    if [[ -d "$dir" ]]; then
        if [[ -w "$dir" ]]; then
            log_success "$desc 目录可写"
            return 0
        else
            log_error "$desc 目录不可写"
            return 1
        fi
    else
        log_error "$desc 目录不存在"
        return 1
    fi
}

# 检查文件存在
check_file_exists() {
    local file="$1"
    local desc="${2:-$1}"
    
    if [[ -f "$file" ]]; then
        log_success "$desc 存在"
        return 0
    else
        log_error "$desc 不存在"
        return 1
    fi
}

# 检查环境变量
check_env_var() {
    local var="$1"
    local desc="${2:-$1}"
    
    if [[ -n "${!var:-}" ]]; then
        log_success "$desc 已设置"
        return 0
    else
        log_error "$desc 未设置"
        return 1
    fi
}

# 检查端口是否可用
check_port_available() {
    local port="$1"
    local desc="${2:-端口 $port}"
    
    if ! command -v nc &>/dev/null && ! command -v netstat &>/dev/null; then
        log_warning "无法检查端口: nc 或 netstat 未安装"
        return 0
    fi
    
    if command -v nc &>/dev/null; then
        if nc -z localhost "$port" 2>/dev/null; then
            log_success "$desc 可用"
            return 0
        else
            log_warning "$desc 未响应"
            return 1
        fi
    fi
    
    return 0
}

# 检查系统资源
check_system_resources() {
    log_info "检查系统资源..."
    
    # 检查内存（兼容中英文输出）
    if command -v free &>/dev/null; then
        local mem_info
        # 尝试匹配英文 "Mem:" 或中文 "内存："
        mem_info=$(free -m | awk '/^Mem:/ || /^内存：/{printf "%.1f", $7/$2 * 100}')
        if [[ -n "$mem_info" ]] && (( $(echo "$mem_info > 10" | bc -l 2>/dev/null || echo "0") )); then
            log_success "内存充足 (${mem_info}% 可用)"
        elif [[ -n "$mem_info" ]]; then
            log_warning "内存不足 (${mem_info}% 可用)"
        else
            log_info "内存检查跳过（无法解析 free 输出）"
        fi
    fi
    
    # 检查磁盘空间
    if command -v df &>/dev/null; then
        local disk_usage
        disk_usage=$(df /tmp 2>/dev/null | awk 'NR==2 {print $5}' | sed 's/%//')
        if [[ -n "$disk_usage" ]] && (( disk_usage < 90 )); then
            log_success "磁盘空间充足 (/tmp: ${disk_usage}% 已用)"
        else
            log_warning "磁盘空间不足 (/tmp: ${disk_usage}% 已用)"
        fi
    fi
}

# ============================================================
# 检查模块
# ============================================================

check_system_deps() {
    log_section "系统依赖"
    
    check_command ffmpeg "FFmpeg"
    check_command ffprobe "FFprobe"
    check_command python3 "Python 3"
    check_command pip3 "pip3"
    check_command bash "Bash"
    
    check_system_resources
}

check_python_deps() {
    log_section "Python 依赖"
    
    # 检查必要的包（使用 Python import 名称，而非 pip 包名）
    check_pip_package edge_tts "Edge TTS"
    check_pip_package faster_whisper "Faster Whisper"
    check_pip_package httpx "HTTPX"
    check_python_package asyncio "AsyncIO"
    
    # 可选包（不计入错误）
    if python3 -c "import psutil" 2>/dev/null; then
        local version
        version=$(python3 -c "import psutil; print(getattr(psutil, '__version__', 'unknown'))" 2>/dev/null || echo "unknown")
        log_success "psutil 已安装 (版本：$version) - 系统资源监控可用"
    else
        log_warning "psutil 未安装，系统资源监控将使用降级方案（可选）"
    fi
}

check_voice_models() {
    log_section "语音模型"
    
    # 获取脚本目录
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    local models_dir="${SCRIPT_DIR}/../models"
    
    if [[ ! -d "$models_dir" ]]; then
        log_warning "模型目录不存在: $models_dir"
        log_info "将在首次使用时自动下载模型"
        return 0
    fi
    
    # 检查 faster-whisper 模型
    local whisper_models
    whisper_models=$(find "$models_dir" -name "*.bin" -o -name "model.pt" 2>/dev/null || true)
    
    if [[ -n "$whisper_models" ]]; then
        log_success "Faster Whisper 模型已下载"
        while IFS= read -r model; do
            local size
            size=$(du -h "$model" 2>/dev/null | cut -f1)
            log_info "  - $(basename "$model") ($size)"
        done <<< "$whisper_models"
    else
        log_warning "Faster Whisper 模型未下载"
        log_info "将在首次使用时自动下载"
    fi
}

check_scripts() {
    log_section "脚本检查"
    
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    
    local scripts=(
        "fast-whisper-fast.sh"
        "tts-voice.sh"
        "feishu-tts.sh"
        "cleanup-tts.sh"
    )
    
    for script in "${scripts[@]}"; do
        local script_path="${SCRIPT_DIR}/${script}"
        if [[ -f "$script_path" ]]; then
            if [[ -x "$script_path" ]]; then
                log_success "$script 存在且可执行"
            else
                log_warning "$script 存在但不可执行"
            fi
        else
            log_error "$script 不存在"
        fi
    done
}

check_environment() {
    log_section "环境配置"
    
    # 检查环境变量文件
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    local env_file="${SCRIPT_DIR}/.env"
    
    if [[ -f "$env_file" ]]; then
        log_success "环境配置文件存在"
        
        # 检查关键配置
        source "$env_file" 2>/dev/null || true
        
        if [[ -n "${FEISHU_APP_ID:-}" ]]; then
            log_success "FEISHU_APP_ID 已配置"
        else
            log_error "FEISHU_APP_ID 未配置"
        fi
        
        if [[ -n "${FEISHU_APP_SECRET:-}" ]]; then
            log_success "FEISHU_APP_SECRET 已配置"
        else
            log_error "FEISHU_APP_SECRET 未配置"
        fi
    else
        log_warning "环境配置文件不存在: $env_file"
    fi
    
    # 检查临时目录
    check_directory_writable "/tmp" "临时目录 /tmp"
}

check_audio_capabilities() {
    log_section "音频能力"
    
    # 检查 ffmpeg 支持的编码器
    if command -v ffmpeg &>/dev/null; then
        log_info "检查 FFmpeg 编码器支持..."
        
        local encoders
        encoders=$(ffmpeg -encoders 2>/dev/null || true)
        
        if echo "$encoders" | grep -q "libopus"; then
            log_success "OPUS 编码器可用"
        else
            log_error "OPUS 编码器不可用"
        fi
        
        if echo "$encoders" | grep -q "libmp3lame"; then
            log_success "MP3 编码器可用"
        else
            log_error "MP3 编码器不可用"
        fi
        
        if echo "$encoders" | grep -q "pcm_s16le"; then
            log_success "PCM 编码器可用"
        else
            log_error "PCM 编码器不可用"
        fi
    fi
}

# ============================================================
# 修复功能
# ============================================================

fix_permissions() {
    log_section "修复脚本权限"
    
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    
    local fixed=0
    for script in "${SCRIPT_DIR}"/*.sh; do
        if [[ -f "$script" && ! -x "$script" ]]; then
            chmod +x "$script"
            log_success "修复权限: $(basename "$script")"
            ((fixed++))
        fi
    done
    
    if (( fixed == 0 )); then
        log_info "所有脚本权限正确"
    fi
}

# ============================================================
# 主程序
# ============================================================

show_usage() {
    cat << EOF
飞书语音交互服务健康检查

用法: $0 [选项]

选项:
    -h, --help      显示帮助信息
    -f, --fix       自动修复可修复的问题
    -q, --quiet     安静模式，只显示错误

示例:
    $0              # 运行完整检查
    $0 --fix        # 运行检查并修复权限
    $0 --quiet      # 只显示问题

EOF
}

main() {
    local fix_mode=false
    local quiet_mode=false
    
    # 解析参数
    while [[ $# -gt 0 ]]; do
        case "$1" in
            -h|--help)
                show_usage
                exit 0
                ;;
            -f|--fix)
                fix_mode=true
                shift
                ;;
            -q|--quiet)
                quiet_mode=true
                shift
                ;;
            *)
                echo "未知选项: $1"
                show_usage
                exit 1
                ;;
        esac
    done
    
    if [[ "$quiet_mode" == true ]]; then
        exec 1>/dev/null
    fi
    
    echo ""
    echo -e "${COLOR_GREEN}飞书语音交互服务健康检查${COLOR_NC}"
    echo "========================================"
    echo "时间: $(date '+%Y-%m-%d %H:%M:%S')"
    echo ""
    
    # 运行所有检查
    check_system_deps
    check_python_deps
    check_voice_models
    check_scripts
    check_environment
    check_audio_capabilities
    
    # 修复模式
    if [[ "$fix_mode" == true ]]; then
        fix_permissions
    fi
    
    # 总结
    log_section "检查结果"
    
    if (( ERRORS == 0 && WARNINGS == 0 )); then
        echo -e "${COLOR_GREEN}✓ 所有检查通过！${COLOR_NC}"
        exit 0
    elif (( ERRORS == 0 )); then
        echo -e "${COLOR_YELLOW}⚠ 发现 $WARNINGS 个警告，但无严重错误${COLOR_NC}"
        exit 0
    else
        echo -e "${COLOR_RED}✗ 发现 $ERRORS 个错误，$WARNINGS 个警告${COLOR_NC}"
        exit 1
    fi
}

# 运行主程序
main "$@"
