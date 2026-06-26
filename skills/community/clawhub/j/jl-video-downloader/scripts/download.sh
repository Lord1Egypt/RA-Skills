#!/bin/bash

# JL Video Downloader 封装脚本
# 封装 uvx jl-video-downloader 命令，提供环境变量配置和简化接口

set -euo pipefail

# 脚本信息
SCRIPT_NAME="jl-video-downloader"
SCRIPT_VERSION="1.0.0"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

# 默认配置
DEFAULT_OUTPUT_DIR="/mnt/d/output"
DEFAULT_PROXY="http://127.0.0.1:7897"
DEFAULT_LOG_LEVEL="INFO"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 显示帮助信息
show_help() {
    cat << EOF
${SCRIPT_NAME} v${SCRIPT_VERSION} - 视频下载和文案提取工具封装脚本

用法: $0 <命令> [选项] <视频URL>

命令:
  info     获取视频信息
  download 下载视频
  extract  提取文案（语音转文字）
  process  完整处理（下载+提取）
  batch    批量处理URL文件
  help     显示此帮助信息

选项:
  -o, --output DIR     指定输出目录 (默认: ${DEFAULT_OUTPUT_DIR})
  -p, --proxy URL      指定代理服务器 (默认: ${DEFAULT_PROXY})
  --api-key KEY        设置SILI_FLOW_API_KEY
  --deepseek-key KEY   设置DEEPSEEK_API_KEY
  --no-segment         禁用语义分段
  --save-video         提取文案时保存视频
  -h, --help           显示帮助信息
  -v, --version        显示版本信息

环境变量配置:
  可以在 ~/.jl-video-downloader/env 文件中设置以下环境变量:
    SILI_FLOW_API_KEY    # 文案提取API密钥
    DEEPSEEK_API_KEY     # DeepSeek API密钥
    OUTPUT_DIR           # 输出目录
    YOUTUBE_PROXY        # YouTube代理
    GLOBAL_PROXY         # 全局代理
    LOG_LEVEL            # 日志级别

示例:
  $0 info "https://www.douyin.com/video/123456789"
  $0 download "https://v.douyin.com/xxxxx" -o ./videos
  $0 extract "https://www.bilibili.com/video/BV1xxx" --api-key "sk-xxx"
  $0 process "https://www.youtube.com/watch?v=xxxx" --proxy "http://127.0.0.1:7897"
  $0 batch urls.txt -o ./output

支持的平台:
  - 抖音 (Douyin)
  - 快手 (Kuaishou)
  - 小红书 (Xiaohongshu)
  - B站 (Bilibili)
  - YouTube
  - 其他通过yt-dlp支持的平台
EOF
}

# 显示版本信息
show_version() {
    echo "${SCRIPT_NAME} v${SCRIPT_VERSION}"
    echo "封装 uvx jl-video-downloader 命令"
    echo "技能目录: ${SKILL_DIR}"
}

# 加载环境变量配置
load_env_config() {
    local env_file="$HOME/.jl-video-downloader/env"
    
    if [[ -f "$env_file" ]]; then
        log_info "加载环境变量配置: $env_file"
        # 安全地加载环境变量
        while IFS='=' read -r key value || [[ -n "$key" ]]; do
            # 跳过注释和空行
            [[ "$key" =~ ^#.*$ ]] && continue
            [[ -z "$key" ]] && continue
            
            # 去除可能的空格和引号
            key=$(echo "$key" | xargs)
            value=$(echo "$value" | xargs)
            
            # 设置环境变量
            if [[ -n "$key" && -n "$value" ]]; then
                export "$key"="$value"
                log_info "  设置: $key=***"
            fi
        done < "$env_file"
    else
        log_warning "环境变量配置文件不存在: $env_file"
        log_info "可以创建该文件来持久化配置"
    fi
}

# 检查必要工具
check_requirements() {
    local missing_tools=()
    
    # 检查uv
    if ! command -v uv &> /dev/null; then
        missing_tools+=("uv")
    fi
    
    # 检查ffmpeg
    if ! command -v ffmpeg &> /dev/null; then
        missing_tools+=("ffmpeg")
    fi
    
    # 检查jl-video-downloader是否安装
    if ! uv tool list | grep -q "jl-video-downloader"; then
        missing_tools+=("jl-video-downloader (使用 'uv tool install jl-video-downloader' 安装)")
    fi
    
    if [[ ${#missing_tools[@]} -gt 0 ]]; then
        log_error "缺少必要工具:"
        for tool in "${missing_tools[@]}"; do
            echo "  - $tool"
        done
        return 1
    fi
    
    log_success "所有必要工具已安装"
    return 0
}

# 设置默认环境变量
set_default_env() {
    # 输出目录
    if [[ -z "${OUTPUT_DIR:-}" ]]; then
        export OUTPUT_DIR="$DEFAULT_OUTPUT_DIR"
        log_info "使用默认输出目录: $OUTPUT_DIR"
    fi
    
    # 代理设置
    if [[ -z "${YOUTUBE_PROXY:-}" && -z "${GLOBAL_PROXY:-}" ]]; then
        export YOUTUBE_PROXY="$DEFAULT_PROXY"
        export GLOBAL_PROXY="$DEFAULT_PROXY"
        log_info "使用默认代理: $DEFAULT_PROXY"
    fi
    
    # 日志级别
    if [[ -z "${LOG_LEVEL:-}" ]]; then
        export LOG_LEVEL="$DEFAULT_LOG_LEVEL"
    fi
    
    # 创建输出目录
    mkdir -p "$OUTPUT_DIR"
}

# 主函数
main() {
    # 如果没有参数，显示帮助
    if [[ $# -eq 0 ]]; then
        show_help
        exit 0
    fi
    
    # 解析命令
    local command=""
    local url=""
    local args=()
    local output_dir=""
    local proxy=""
    local api_key=""
    local deepseek_key=""
    local no_segment=false
    local save_video=false
    
    # 第一个参数是命令
    command="$1"
    shift
    
    # 解析选项
    while [[ $# -gt 0 ]]; do
        case "$1" in
            -o|--output)
                output_dir="$2"
                shift 2
                ;;
            -p|--proxy)
                proxy="$2"
                shift 2
                ;;
            --api-key)
                api_key="$2"
                shift 2
                ;;
            --deepseek-key)
                deepseek_key="$2"
                shift 2
                ;;
            --no-segment)
                no_segment=true
                shift
                ;;
            --save-video)
                save_video=true
                shift
                ;;
            -h|--help)
                show_help
                exit 0
                ;;
            -v|--version)
                show_version
                exit 0
                ;;
            -*)
                log_error "未知选项: $1"
                show_help
                exit 1
                ;;
            *)
                # 第一个非选项参数视为URL
                if [[ -z "$url" ]]; then
                    url="$1"
                else
                    args+=("$1")
                fi
                shift
                ;;
        esac
    done
    
    # 加载环境配置
    load_env_config
    
    # 检查必要工具
    if ! check_requirements; then
        exit 1
    fi
    
    # 设置默认环境变量
    set_default_env
    
    # 覆盖环境变量（如果通过选项指定）
    if [[ -n "$output_dir" ]]; then
        export OUTPUT_DIR="$output_dir"
        mkdir -p "$OUTPUT_DIR"
    fi
    
    if [[ -n "$proxy" ]]; then
        export YOUTUBE_PROXY="$proxy"
        export GLOBAL_PROXY="$proxy"
    fi
    
    if [[ -n "$api_key" ]]; then
        export SILI_FLOW_API_KEY="$api_key"
    fi
    
    if [[ -n "$deepseek_key" ]]; then
        export DEEPSEEK_API_KEY="$deepseek_key"
    fi
    
    # 构建uvx命令
    local uvx_cmd="uvx jl-video-downloader"
    
    # 根据命令构建参数
    case "$command" in
        info|download|extract|process|batch)
            uvx_cmd="$uvx_cmd $command"
            ;;
        help)
            show_help
            exit 0
            ;;
        *)
            log_error "未知命令: $command"
            show_help
            exit 1
            ;;
    esac
    
    # 添加URL参数
    if [[ -n "$url" ]]; then
        uvx_cmd="$uvx_cmd \"$url\""
    fi
    
    # 添加输出目录
    if [[ -n "$OUTPUT_DIR" ]]; then
        uvx_cmd="$uvx_cmd -o \"$OUTPUT_DIR\""
    fi
    
    # 添加其他选项
    if [[ "$no_segment" == true ]]; then
        uvx_cmd="$uvx_cmd --no-segment"
    fi
    
    if [[ "$save_video" == true ]]; then
        uvx_cmd="$uvx_cmd --save-video"
    fi
    
    # 添加剩余参数
    if [[ ${#args[@]} -gt 0 ]]; then
        uvx_cmd="$uvx_cmd ${args[*]}"
    fi
    
    # 显示执行的命令
    log_info "执行命令: $uvx_cmd"
    log_info "环境变量:"
    log_info "  OUTPUT_DIR: $OUTPUT_DIR"
    log_info "  YOUTUBE_PROXY: ${YOUTUBE_PROXY:-未设置}"
    log_info "  GLOBAL_PROXY: ${GLOBAL_PROXY:-未设置}"
    log_info "  SILI_FLOW_API_KEY: ${SILI_FLOW_API_KEY:+已设置}"
    log_info "  DEEPSEEK_API_KEY: ${DEEPSEEK_API_KEY:+已设置}"
    
    # 执行命令
    eval "$uvx_cmd"
    
    # 检查执行结果
    if [[ $? -eq 0 ]]; then
        log_success "命令执行成功"
        
        # 显示输出文件
        if [[ -d "$OUTPUT_DIR" ]]; then
            log_info "输出目录内容:"
            ls -la "$OUTPUT_DIR/" | head -20
        fi
    else
        log_error "命令执行失败"
        exit 1
    fi
}

# 运行主函数
main "$@"