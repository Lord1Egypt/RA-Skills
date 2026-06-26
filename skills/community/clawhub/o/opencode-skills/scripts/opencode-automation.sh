#!/usr/bin/env bash
# Opencode 自动化脚本示例
# 本脚本展示了如何使用 opencode 进行各种自动化任务

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# 打印函数
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 函数：检查 opencode 是否已安装
check_opencode_installed() {
    print_info "检查 opencode 是否已安装..."
    if command -v opencode &> /dev/null; then
        print_success "opencode 已安装"
        print_info "版本：$(opencode --version)"
        return 0
    else
        print_error "opencode 未安装"
        print_info "安装方法：npm install -g opencode"
        return 1
    fi
}

# 函数：启动 opencode Web 服务器
start_web_server() {
    local PORT=${1:-4096}
    local HOST=${2:-127.0.0.1}
    
    print_info "启动 opencode Web 服务器..."
    print_info "端口：$PORT"
    print_info "主机：$HOST"
    
    opencode web --port $PORT --hostname $HOST
}

# 函数：运行 opencode 任务
run_opencode_task() {
    local TASK="$1"
    local OUTPUT_DIR=${2:-"/home/linshui/.openclaw/workspace"}
    
    print_info "运行 opencode 任务..."
    print_info "任务：$TASK"
    print_info "输出目录：$OUTPUT_DIR"
    
    opencode run "$(echo "$TASK" | sed 's/"/"\\"/g')"
}

# 函数：分析项目
analyze_project() {
    local PROJECT_DIR="$1"
    
    print_info "分析项目：$PROJECT_DIR"
    
    # 查看文件数量
    local FILE_COUNT=$(find "$PROJECT_DIR" -type f | wc -l)
    print_info "文件数量：$FILE_COUNT"
    
    # 查看项目大小
    local PROJECT_SIZE=$(du -sh "$PROJECT_DIR" | cut -f1)
    print_info "项目大小：$PROJECT_SIZE"
    
    # 查看文件类型
    echo ""
    print_info "文件类型分布:"
    find "$PROJECT_DIR" -type f | xargs file | sort | uniq -c | sort -rn | head -10
}

# 函数：启动预览服务器
start_preview_server() {
    local PROJECT_DIR="$1"
    local PORT=${2:-8000}
    
    print_info "启动预览服务器..."
    print_info "项目目录：$PROJECT_DIR"
    print_info "端口：$PORT"
    
    python3 -m http.server $PORT -d "$PROJECT_DIR"
}

# 函数：复制文件
copy_files() {
    local SOURCE="$1"
    local DESTINATION="$2"
    
    print_info "复制文件..."
    print_info "源：$SOURCE"
    print_info "目标：$DESTINATION"
    
    cp -r "$SOURCE" "$DESTINATION"
    print_success "复制完成"
}

# 函数：压缩项目
compress_project() {
    local PROJECT_DIR="$1"
    local OUTPUT_FILE="${PROJECT_DIR}.tar.gz"
    
    print_info "压缩项目..."
    print_info "项目目录：$PROJECT_DIR"
    print_info "输出文件：$OUTPUT_FILE"
    
    tar -czf "$OUTPUT_FILE" "$PROJECT_DIR"
    local SIZE=$(du -sh "$OUTPUT_FILE" | cut -f1)
    print_success "压缩完成，大小：$SIZE"
}

# 函数：解压文件
extract_archive() {
    local ARCHIVE_FILE="$1"
    local DESTINATION="${ARCHIVE_FILE%.tar.gz}"
    
    print_info "解压文件..."
    print_info "压缩包：$ARCHIVE_FILE"
    print_info "目标目录：$DESTINATION"
    
    tar -xzf "$ARCHIVE_FILE" -C "$(dirname "$DESTINATION")"
    print_success "解压完成"
}

# 函数：创建压缩包
create_archive() {
    local PROJECT_DIR="$1"
    local OUTPUT_FILE="$2"
    
    print_info "创建压缩包..."
    print_info "项目目录：$PROJECT_DIR"
    print_info "输出文件：$OUTPUT_FILE"
    
    tar -czf "$OUTPUT_FILE" "$PROJECT_DIR"
    local SIZE=$(du -sh "$OUTPUT_FILE" | cut -f1)
    print_success "压缩包创建完成，大小：$SIZE"
}

# 函数：生成项目报告
generate_report() {
    local PROJECT_DIR="$1"
    
    print_info "生成项目报告..."
    
    echo "========================================"
    echo "项目名称：$(basename "$PROJECT_DIR")"
    echo "创建时间：$(date '+%Y-%m-%d %H:%M:%S')"
    echo "========================================"
    echo ""
    
    echo "📁 项目统计:"
    echo "  - 文件数量：$(find "$PROJECT_DIR" -type f | wc -l)"
    echo "  - 目录数量：$(find "$PROJECT_DIR" -type d | wc -l)"
    echo "  - 项目大小：$(du -sh "$PROJECT_DIR" | cut -f1)"
    echo ""
    
    echo "📊 文件类型分布:"
    find "$PROJECT_DIR" -type f | xargs file | sort | uniq -c | sort -rn | head -10
    echo ""
    
    echo "📝 扩展名分布:"
    find "$PROJECT_DIR" -type f -name "*" | sed 's/.*\.//' | sort | uniq -c | sort -rn | head -10
    echo ""
    
    echo "📅 最后修改时间:"
    find "$PROJECT_DIR" -type f -printf "%T+ %p\n" | sort -r | head -20
}

# 函数：监控 opencode 进程
monitor_opencode() {
    print_info "监控 opencode 进程..."
    
    while true; do
        echo ""
        echo "========================================"
        echo "opencode 进程状态"
        echo "========================================"
        ps aux | grep opencode | grep -v grep
        
        sleep 5
    done
}

# 函数：备份项目
backup_project() {
    local PROJECT_DIR="$1"
    local BACKUP_DIR="~/opencode-backups/$(date '+%Y%m%d_%H%M%S')"
    
    print_info "备份项目..."
    print_info "源目录：$PROJECT_DIR"
    print_info "备份目录：$BACKUP_DIR"
    
    mkdir -p "$(dirname "$BACKUP_DIR")"
    cp -r "$PROJECT_DIR"/* "$BACKUP_DIR/"
    print_success "备份完成"
}

# 函数：清理临时文件
cleanup_temp() {
    print_info "清理临时文件..."
    
    # 清理 opencode 缓存
    rm -rf ~/.local/share/opencode/cache/*
    
    # 清理临时目录
    rm -rf /tmp/opencode_*
    
    print_success "清理完成"
}

# 函数：显示帮助
show_help() {
    echo ""
    echo "========================================"
    echo "Opencode 自动化脚本"
    echo "========================================"
    echo ""
    echo "用法：$0 <命令> [参数]"
    echo ""
    echo "可用命令:"
    echo "  check            检查 opencode 安装状态"
    echo "  web <端口>       启动 Web 服务器"
    echo "  task <任务>      运行 opencode 任务"
    echo "  analyze <目录>   分析项目"
    echo "  preview <目录>   启动预览服务器"
    echo "  copy <源> <目标> 复制文件"
    echo "  compress <目录>  压缩项目"
    echo "  extract <文件>   解压文件"
    echo "  archive <目录> <文件> 创建压缩包"
    echo "  report <目录>    生成项目报告"
    echo "  monitor          监控 opencode 进程"
    echo "  backup <目录>    备份项目"
    echo "  cleanup          清理临时文件"
    echo "  help             显示帮助信息"
    echo ""
    echo "示例:"
    echo "  $0 check"
    echo "  $0 web 8080"
    echo "  $0 task \"创建一个网站\" /output"
    echo "  $0 analyze /path/to/project"
    echo ""
}

# 主程序
main() {
    # 显示签名
    echo "========================================"
    echo "  Opencode Automation Script v1.0.0"
    echo "========================================"
    echo ""
    
    # 解析命令
    case "${1:-help}" in
        check)
            check_opencode_installed
            ;;
        web)
            start_web_server "$2" "$3"
            ;;
        task)
            run_opencode_task "$2" "$3"
            ;;
        analyze)
            analyze_project "$2"
            ;;
        preview)
            start_preview_server "$2" "$3"
            ;;
        copy)
            copy_files "$2" "$3"
            ;;
        compress)
            compress_project "$2"
            ;;
        extract)
            extract_archive "$2"
            ;;
        archive)
            create_archive "$2" "$3"
            ;;
        report)
            generate_report "$2"
            ;;
        monitor)
            monitor_opencode
            ;;
        backup)
            backup_project "$2"
            ;;
        cleanup)
            cleanup_temp
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            print_error "未知命令：$1"
            show_help
            exit 1
            ;;
    esac
}

# 运行主程序
main "$@"
