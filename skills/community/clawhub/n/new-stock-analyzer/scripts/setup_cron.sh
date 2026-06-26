#!/bin/bash
# 新股分析工具 - 定时任务设置脚本

set -e

# 脚本目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 日志函数
log() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查系统
check_system() {
    log "检查系统环境..."
    
    # 检查Python
    if ! command -v python3 &> /dev/null; then
        error "未找到python3，请先安装Python 3.8+"
        exit 1
    fi
    
    PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    log "Python版本: $PYTHON_VERSION"
    
    # 检查pip
    if ! command -v pip3 &> /dev/null; then
        warn "未找到pip3，尝试安装..."
        if command -v apt-get &> /dev/null; then
            sudo apt-get update && sudo apt-get install -y python3-pip
        elif command -v yum &> /dev/null; then
            sudo yum install -y python3-pip
        else
            error "无法自动安装pip3，请手动安装"
            exit 1
        fi
    fi
    
    log "✅ 系统检查完成"
}

# 安装依赖
install_dependencies() {
    log "安装Python依赖..."
    
    cd "$PROJECT_DIR"
    
    if [ -f "requirements.txt" ]; then
        pip3 install -r requirements.txt
        if [ $? -eq 0 ]; then
            log "✅ 依赖安装完成"
        else
            warn "依赖安装有警告，但继续执行"
        fi
    else
        warn "未找到requirements.txt，安装基础依赖..."
        pip3 install requests pandas beautifulsoup4 lxml pyyaml python-dotenv
    fi
    
    # 测试导入
    log "测试Python模块..."
    if python3 -c "import requests, pandas, bs4, yaml, dotenv"; then
        log "✅ Python模块测试通过"
    else
        warn "部分模块导入失败，但继续执行"
    fi
}

# 创建目录结构
create_directories() {
    log "创建目录结构..."
    
    mkdir -p "$PROJECT_DIR/data/cache"
    mkdir -p "$PROJECT_DIR/data/logs"
    mkdir -p "$PROJECT_DIR/config"
    
    log "✅ 目录创建完成"
}

# 测试工具功能
test_tool() {
    log "测试工具功能..."
    
    cd "$PROJECT_DIR"
    
    # 测试连接
    log "测试数据连接..."
    if python3 main_fixed.py --test; then
        log "✅ 数据连接测试通过"
    else
        warn "数据连接测试有警告"
    fi
    
    # 测试分析
    log "测试分析功能..."
    if python3 main_fixed.py --daily --no-print; then
        log "✅ 分析功能测试通过"
    else
        warn "分析功能测试有警告"
    fi
    
    log "✅ 工具功能测试完成"
}

# 设置定时任务
setup_cron() {
    log "设置定时任务..."
    
    # 默认执行时间：每天10:00
    CRON_TIME="0 10 * * *"
    
    # 构建cron命令
    CRON_CMD="$CRON_TIME cd '$PROJECT_DIR' && bash scripts/openclaw_daily.sh >> '$PROJECT_DIR/data/logs/cron.log' 2>&1"
    
    # 检查是否已存在
    if crontab -l 2>/dev/null | grep -q "openclaw_daily.sh"; then
        warn "检测到已存在的定时任务"
        echo "当前crontab内容:"
        crontab -l 2>/dev/null | grep -A2 -B2 "openclaw_daily.sh"
        
        read -p "是否替换现有任务？(y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            # 删除现有任务
            crontab -l 2>/dev/null | grep -v "openclaw_daily.sh" | crontab -
            log "已删除现有任务"
        else
            log "保留现有任务，跳过设置"
            return
        fi
    fi
    
    # 添加新任务
    (crontab -l 2>/dev/null; echo "$CRON_CMD") | crontab -
    
    if [ $? -eq 0 ]; then
        log "✅ 定时任务设置成功"
        log "执行时间: 每天 $CRON_TIME"
        log "执行命令: $CRON_CMD"
    else
        error "定时任务设置失败"
        exit 1
    fi
    
    # 显示crontab
    log "当前crontab内容:"
    crontab -l 2>/dev/null
}

# 显示使用说明
show_usage() {
    echo "================================================"
    echo "新股分析工具 - 定时任务设置"
    echo "================================================"
    echo ""
    echo "功能:"
    echo "  1. 检查系统环境"
    echo "  2. 安装Python依赖"
    echo "  3. 创建必要目录"
    echo "  4. 测试工具功能"
    echo "  5. 设置定时任务（默认每天10:00）"
    echo ""
    echo "定时任务将执行:"
    echo "  - 每日新股分析"
    echo "  - 通过OpenClaw发送通知"
    echo "  - 自动清理日志"
    echo ""
    echo "手动测试命令:"
    echo "  python3 main_fixed.py --test      # 测试连接"
    echo "  python3 main_fixed.py --daily     # 执行分析"
    echo "  bash scripts/openclaw_daily.sh    # 完整推送"
    echo ""
    echo "================================================"
}

# 主函数
main() {
    show_usage
    
    echo ""
    read -p "是否继续设置？(Y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Nn]$ ]]; then
        log "用户取消设置"
        exit 0
    fi
    
    log "开始设置新股分析工具..."
    
    # 执行设置步骤
    check_system
    install_dependencies
    create_directories
    test_tool
    setup_cron
    
    echo ""
    log "🎉 ========== 设置完成 =========="
    log "✅ 系统检查完成"
    log "✅ 依赖安装完成"
    log "✅ 目录创建完成"
    log "✅ 工具测试完成"
    log "✅ 定时任务设置完成"
    echo ""
    log "定时任务将在每天10:00自动执行"
    log "首次执行时间: 明天10:00"
    log "日志文件: $PROJECT_DIR/data/logs/"
    echo ""
    log "手动测试命令:"
    log "  cd $PROJECT_DIR"
    log "  python3 main_fixed.py --test"
    log "  python3 main_fixed.py --daily"
    echo ""
    log "🛡️ 你的助理 佑安"
}

# 执行主函数
main "$@"