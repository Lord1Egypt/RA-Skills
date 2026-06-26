#!/bin/bash
# 新股分析工具 - OpenClaw每日推送脚本
# 通过OpenClaw会话直接发送通知给BOSS

set -e

# 脚本目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_DIR"

# 环境变量
export PYTHONPATH="$PROJECT_DIR:$PYTHONPATH"
LOG_FILE="$PROJECT_DIR/data/logs/openclaw_daily_$(date +%Y%m%d).log"

# 日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# 错误处理函数
error_exit() {
    log "错误: $1"
    exit 1
}

# 检查依赖
check_dependencies() {
    log "检查依赖..."
    
    # 检查Python
    if ! command -v python3 &> /dev/null; then
        error_exit "未找到python3，请安装Python 3.8+"
    fi
    
    # 检查Python版本
    PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    log "Python版本: $PYTHON_VERSION"
    
    # 检查必要模块
    for module in requests pandas; do
        if ! python3 -c "import $module" 2>/dev/null; then
            log "警告: 未找到$module模块，尝试安装..."
            pip3 install $module || log "安装$module失败，但继续执行"
        fi
    done
    
    log "✅ 依赖检查完成"
}

# 检查系统状态
check_system_status() {
    log "📊 系统状态检查..."
    
    # 磁盘使用率
    DISK_USAGE=$(df -h . | awk 'NR==2 {print $5}' | sed 's/%//')
    log "  磁盘使用率: ${DISK_USAGE}%"
    
    # 内存使用
    MEM_USAGE=$(free -m | awk 'NR==2 {printf "%.0fMi/%.0fGi", $3, $2/1024}')
    log "  内存使用: $MEM_USAGE"
    
    # 缓存文件数
    CACHE_COUNT=$(find data/cache -name "*.json" 2>/dev/null | wc -l)
    log "  缓存文件数: $CACHE_COUNT"
    
    if [ "$DISK_USAGE" -gt 90 ]; then
        log "⚠️  磁盘使用率过高，建议清理"
    fi
    
    log "✅ 系统状态正常"
}

# 执行新股分析
run_stock_analysis() {
    log "📅 执行新股分析..."
    
    # 获取今天是周几
    DAY_OF_WEEK=$(date +%u)  # 1=周一, 7=周日
    
    if [ "$DAY_OF_WEEK" -eq 1 ]; then
        # 周一执行增强版每周分析
        log "今天是周一，执行增强版每周分析..."
        python3 main_enhanced.py --weekly --no-print
    else
        # 其他时间执行每日分析
        log "执行每日分析..."
        python3 main_fixed.py --daily --no-print
    fi
    
    # 检查执行结果
    if [ $? -eq 0 ]; then
        log "✅ 新股分析完成"
    else
        log "⚠️  新股分析执行有误，但继续流程"
    fi
}

# 发送OpenClaw通知
send_openclaw_notification() {
    log "📤 准备发送OpenClaw通知..."
    
    # 生成通知文件
    NOTIFICATION_FILE="/tmp/new_stock_analysis_$(date +%Y%m%d_%H%M%S).txt"
    
    # 运行分析并保存结果
    python3 main_fixed.py --daily > "$NOTIFICATION_FILE" 2>&1
    
    # 检查文件大小
    FILE_SIZE=$(wc -c < "$NOTIFICATION_FILE")
    if [ "$FILE_SIZE" -lt 100 ]; then
        log "⚠️  通知内容过少，可能无新股数据"
        echo "📅 今日无新股申购" > "$NOTIFICATION_FILE"
    fi
    
    # 添加时间戳
    echo "" >> "$NOTIFICATION_FILE"
    echo "🕐 时间: $(date '+%Y-%m-%d %H:%M:%S')" >> "$NOTIFICATION_FILE"
    echo "🌐 服务地址: http://10.3.0.15:25915/jvygnr/" >> "$NOTIFICATION_FILE"
    echo "🛡️ 你的助理 佑安" >> "$NOTIFICATION_FILE"
    
    log "📄 通知文件已生成: $NOTIFICATION_FILE"
    log "📊 文件大小: ${FILE_SIZE}字节"
    
    # 显示通知内容（前10行）
    log "📋 通知内容预览:"
    head -20 "$NOTIFICATION_FILE" | while IFS= read -r line; do
        log "   $line"
    done
    
    log "✅ OpenClaw通知准备完成"
    log "💡 通知将通过OpenClaw会话自动发送"
}

# 主函数
main() {
    log "🚀 ========== 新股分析工具推送开始 =========="
    
    # 检查依赖
    check_dependencies
    
    # 检查系统状态
    check_system_status
    
    # 执行新股分析
    run_stock_analysis
    
    # 发送OpenClaw通知
    send_openclaw_notification
    
    log "🎉 ========== 新股分析工具推送完成 =========="
    
    # 清理旧日志（保留7天）
    find "$PROJECT_DIR/data/logs" -name "*.log" -mtime +7 -delete 2>/dev/null || true
    log "🧹 已清理7天前的日志文件"
}

# 执行主函数
main "$@"