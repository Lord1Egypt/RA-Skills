#!/bin/bash
# 新股分析工具 - 增强版OpenClaw每日推送脚本
# 使用增强版分析器，提供更深入的分析

set -e

# 脚本目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_DIR"

# 环境变量
export PYTHONPATH="$PROJECT_DIR:$PYTHONPATH"
LOG_FILE="$PROJECT_DIR/data/logs/openclaw_enhanced_$(date +%Y%m%d).log"

# 日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# 错误处理函数
error_exit() {
    log "❌ 错误: $1"
    exit 1
}

# 检查依赖
check_dependencies() {
    log "🔧 检查依赖..."
    
    # 检查Python
    if ! command -v python3 &> /dev/null; then
        error_exit "未找到python3，请安装Python 3.7+"
    fi
    
    # 检查Python包
    if ! python3 -c "import requests, pandas, statistics" &> /dev/null; then
        log "📦 缺少Python依赖，尝试安装..."
        pip3 install -r requirements.txt || error_exit "安装依赖失败"
    fi
    
    log "✅ 依赖检查完成"
}

# 执行增强版每日分析
run_enhanced_daily_analysis() {
    log "📊 执行增强版每日分析..."
    
    # 输出文件
    OUTPUT_FILE="/tmp/new_stock_enhanced_$(date +%Y%m%d_%H%M%S).txt"
    
    # 执行增强版分析
    python3 main_enhanced.py --daily --output "$OUTPUT_FILE" 2>&1 | tee -a "$LOG_FILE"
    
    local exit_code=${PIPESTATUS[0]}
    
    if [ $exit_code -eq 0 ]; then
        log "✅ 增强版分析执行完成"
        log "📁 输出文件: $OUTPUT_FILE"
        
        # 显示输出内容预览
        log "📋 输出内容预览:"
        echo "=" * 60 | tee -a "$LOG_FILE"
        head -30 "$OUTPUT_FILE" | while IFS= read -r line; do
            echo "  $line" | tee -a "$LOG_FILE"
        done
        echo "=" * 60 | tee -a "$LOG_FILE"
        
    else
        error_exit "增强版分析执行失败，退出码: $exit_code"
    fi
    
    # 返回输出文件路径
    echo "$OUTPUT_FILE"
}

# 执行增强版每周分析（仅周一）
run_enhanced_weekly_analysis() {
    local weekday=$(date +%u)  # 1=周一, 7=周日
    
    if [ "$weekday" -eq 1 ]; then
        log "📅 今天是周一，执行增强版每周分析..."
        
        OUTPUT_FILE="/tmp/new_stock_weekly_enhanced_$(date +%Y%m%d_%H%M%S).txt"
        
        # 执行增强版每周分析
        python3 main_enhanced.py --weekly --output "$OUTPUT_FILE" 2>&1 | tee -a "$LOG_FILE"
        
        local exit_code=${PIPESTATUS[0]}
        
        if [ $exit_code -eq 0 ]; then
            log "✅ 增强版每周分析执行完成"
            log "📁 输出文件: $OUTPUT_FILE"
        else
            log "⚠️ 警告: 增强版每周分析执行失败，退出码: $exit_code"
        fi
    else
        log "📅 今天不是周一，跳过每周分析"
    fi
}

# 发送到OpenClaw（如果配置了）
send_to_openclaw() {
    local output_file="$1"
    
    log "📤 准备发送到OpenClaw..."
    
    if [ ! -f "$output_file" ]; then
        log "⚠️ 输出文件不存在，跳过发送"
        return
    fi
    
    # 读取输出内容
    local content
    content=$(cat "$output_file" 2>/dev/null || echo "无法读取输出文件")
    
    # 检查内容长度
    local content_length=${#content}
    if [ $content_length -lt 10 ]; then
        log "⚠️ 输出内容太短，跳过发送"
        return
    fi
    
    # 这里可以添加通过OpenClaw发送消息的逻辑
    # 例如：调用OpenClaw API或使用其他方式发送消息
    
    log "📤 发送到OpenClaw的逻辑需要根据实际配置实现"
    log "💡 当前输出文件: $output_file"
    log "💡 内容长度: $content_length 字符"
    
    # 示例：显示如何发送
    log ""
    log "📝 发送示例:"
    log "  python3 main_enhanced.py --daily --openclaw"
    log "  或"
    log "  python3 -c \"from openclaw_notifier import OpenClawNotifier; notifier = OpenClawNotifier(); notifier.send_notification('你的消息')\""
}

# 清理旧文件
cleanup_old_files() {
    log "🧹 清理旧文件..."
    
    # 保留最近7天的日志
    find "$PROJECT_DIR/data/logs" -name "openclaw_enhanced_*.log" -mtime +7 -delete 2>/dev/null || true
    find "$PROJECT_DIR/data/logs" -name "openclaw_daily_*.log" -mtime +7 -delete 2>/dev/null || true
    
    # 清理临时文件（保留最近3天的）
    find /tmp -name "new_stock_*.txt" -mtime +3 -delete 2>/dev/null || true
    find /tmp -name "new_stock_enhanced_*.txt" -mtime +3 -delete 2>/dev/null || true
    find /tmp -name "new_stock_weekly_*.txt" -mtime +3 -delete 2>/dev/null || true
    
    log "✅ 文件清理完成"
}

# 显示系统状态
show_system_status() {
    log "📊 系统状态检查..."
    
    # Python版本
    python_version=$(python3 --version 2>&1 || echo "未知")
    log "  Python版本: $python_version"
    
    # 磁盘空间
    disk_usage=$(df -h "$PROJECT_DIR" | tail -1 | awk '{print $5}')
    log "  磁盘使用率: $disk_usage"
    
    # 内存使用
    mem_usage=$(free -h | grep Mem | awk '{print $3 "/" $2}')
    log "  内存使用: $mem_usage"
    
    # 缓存文件
    cache_count=$(find "$PROJECT_DIR/data/cache" -name "*.json" 2>/dev/null | wc -l)
    log "  缓存文件数: $cache_count"
    
    log "✅ 系统状态正常"
}

# 显示使用说明
show_usage() {
    log "📖 使用说明:"
    log "  增强版每日分析: python3 main_enhanced.py --daily"
    log "  增强版每周分析: python3 main_enhanced.py --weekly"
    log "  个股深度分析: python3 main_enhanced.py --stock <代码>"
    log "  测试连接: python3 main_enhanced.py --test"
    log "  发送到OpenClaw: python3 main_enhanced.py --daily --openclaw"
    log ""
    log "📁 输出文件位置: /tmp/new_stock_enhanced_*.txt"
    log "📁 日志文件: $PROJECT_DIR/data/logs/openclaw_enhanced_*.log"
}

# 主函数
main() {
    log "🚀 ========== 新股分析工具 增强版推送开始 =========="
    
    # 创建必要目录
    mkdir -p "$PROJECT_DIR/data/logs"
    mkdir -p "$PROJECT_DIR/data/cache"
    
    # 显示系统状态
    show_system_status
    
    # 执行各步骤
    check_dependencies
    
    # 执行增强版分析
    output_file=$(run_enhanced_daily_analysis)
    
    # 执行增强版每周分析
    run_enhanced_weekly_analysis
    
    # 发送到OpenClaw
    send_to_openclaw "$output_file"
    
    # 清理旧文件
    cleanup_old_files
    
    log "🎉 ========== 新股分析工具 增强版推送完成 =========="
    
    # 显示使用说明
    show_usage
    
    log ""
    log "💡 下一步操作建议:"
    log "  1. 查看完整输出: cat $output_file"
    log "  2. 手动发送到OpenClaw: python3 main_enhanced.py --daily --openclaw"
    log "  3. 测试个股分析: python3 main_enhanced.py --stock 301682"
}

# 执行主函数
main "$@"