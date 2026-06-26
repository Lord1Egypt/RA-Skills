#!/bin/bash
# macOS 自动化工作流示例
# 用法：./automation_workflows.sh [工作流名称]

set -euo pipefail

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo -e "${BLUE}🤖 macOS 自动化工作流${NC}"
echo ""

# 工作流 1: 晨会准备
workflow_morning_prep() {
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}🌅 工作流：晨会准备${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    
    echo "1️⃣  打开日历应用..."
    open -a "Calendar" 2>/dev/null || echo "  ⚠️  Calendar 未安装"
    sleep 1
    
    echo "2️⃣  打开邮件应用..."
    open -a "Mail" 2>/dev/null || echo "  ⚠️  Mail 未安装"
    sleep 1
    
    echo "3️⃣  打开 Teams/钉钉..."
    open -a "Microsoft Teams" 2>/dev/null || open -a "DingTalk" 2>/dev/null || echo "  ⚠️  会议应用未安装"
    sleep 1
    
    echo "4️⃣  截屏保存当前状态..."
    bash "$SCRIPT_DIR/screenshot.sh" -o ~/Desktop/morning_prep_$(date +%H%M%S).png
    
    echo ""
    echo -e "${GREEN}✅ 晨会准备工作流完成！${NC}"
    echo ""
}

# 工作流 2: 专注模式
workflow_focus_mode() {
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}🎯 工作流：专注模式${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    
    echo "1️⃣  关闭社交媒体应用..."
    for app in "Google Chrome" "Safari"; do
        if pgrep -x "$app" > /dev/null 2>&1; then
            echo "  关闭 $app..."
            osascript -e "tell application \"$app\" to quit" 2>/dev/null || true
        fi
    done
    
    echo "2️⃣  最小化娱乐应用..."
    for app in "Music" "TV"; do
        if pgrep -x "$app" > /dev/null 2>&1; then
            echo "  最小化 $app..."
            osascript -e "tell application \"$app\" to activate" 2>/dev/null
            osascript -e "tell application \"System Events\" to keystroke \"m\" using command down" 2>/dev/null || true
        fi
    done
    
    echo "3️⃣  打开工作应用..."
    open -a "Visual Studio Code" 2>/dev/null || echo "  ⚠️  VS Code 未安装"
    open -a "Terminal" 2>/dev/null || echo "  ⚠️  Terminal 未安装"
    
    echo "4️⃣  设置勿扰模式（需要 macOS 12+）..."
    # macOS 12+ 可以使用 defaults 命令
    if [[ $(sw_vers -productVersion) > "12.0" ]]; then
        echo "  启用专注模式..."
        # 这里可以添加控制 Focus Mode 的命令
    fi
    
    echo ""
    echo -e "${GREEN}✅ 专注模式已启用！${NC}"
    echo ""
}

# 工作流 3: 下班清理
workflow_cleanup() {
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}🏠 工作流：下班清理${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    
    echo "1️⃣  关闭所有工作应用..."
    work_apps=("Visual Studio Code" "Terminal" "iTerm2" "Xcode")
    for app in "${work_apps[@]}"; do
        if pgrep -x "$app" > /dev/null 2>&1; then
            echo "  关闭 $app..."
            osascript -e "tell application \"$app\" to quit" 2>/dev/null || true
        fi
    done
    
    echo "2️⃣  整理桌面截屏..."
    if [ -d ~/Desktop/OpenClaw-Screenshots ]; then
        screenshot_count=$(ls -1 ~/Desktop/OpenClaw-Screenshots/*.png 2>/dev/null | wc -l)
        echo "  发现 $screenshot_count 张截屏"
    fi
    
    echo "3️⃣  保存当前状态..."
    echo "  保存进程列表..."
    bash "$SCRIPT_DIR/processes.sh" -g > ~/Desktop/running_apps_$(date +%Y%m%d).txt 2>/dev/null
    
    echo ""
    echo -e "${GREEN}✅ 下班清理完成！明天见！${NC}"
    echo ""
}

# 工作流 4: 演示模式
workflow_presentation() {
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}📊 工作流：演示模式${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    
    echo "1️⃣  关闭通知（需要权限）..."
    echo "  ⚠️  请手动开启勿扰模式"
    
    echo "2️⃣  打开演示应用..."
    open -a "Keynote" 2>/dev/null || open -a "Microsoft PowerPoint" 2>/dev/null || echo "  ⚠️  演示应用未安装"
    
    echo "3️⃣  调整窗口到全屏..."
    echo "  ⚠️  按 F5 开始演示"
    
    echo "4️⃣  准备截屏..."
    echo "  使用 Cmd+Shift+3 全屏截图"
    echo "  使用 Cmd+Shift+4 区域截图"
    
    echo ""
    echo -e "${GREEN}✅ 演示准备完成！祝演讲顺利！${NC}"
    echo ""
}

# 工作流 5: 系统诊断
workflow_diagnostic() {
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}🔧 工作流：系统诊断${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    
    local report_file=~/Desktop/system_diagnostic_$(date +%Y%m%d_%H%M%S).txt
    
    echo "1️⃣  收集系统信息..."
    echo -e "   ${YELLOW}⏳ 正在收集硬件信息...${NC}"
    {
        echo "=== 系统诊断报告 ==="
        echo "日期：$(date)"
        echo ""
        
        echo "=== 硬件信息 ==="
        bash "$SCRIPT_DIR/system_info.sh" -h 2>/dev/null
        echo -e "   ✅ 硬件信息完成"
        
        echo "=== 运行应用 ==="
        bash "$SCRIPT_DIR/processes.sh" -g 2>/dev/null
        echo -e "   ✅ 应用列表完成"
        
        echo "=== 磁盘使用 ==="
        bash "$SCRIPT_DIR/system_info.sh" -d 2>/dev/null
        echo -e "   ✅ 磁盘信息完成"
        
        echo "=== 内存使用 ==="
        bash "$SCRIPT_DIR/system_info.sh" -m 2>/dev/null
        echo -e "   ✅ 内存信息完成"
    } > "$report_file"
    
    echo ""
    echo "2️⃣  生成报告..."
    local file_size=$(ls -lh "$report_file" 2>/dev/null | awk '{print $5}')
    echo -e "${GREEN}✅ 报告已保存：$report_file${NC}"
    echo "   文件大小：$file_size"
    
    echo ""
    echo "3️⃣  打开报告..."
    if open "$report_file" 2>/dev/null; then
        echo -e "   ${GREEN}✅ 已打开报告${NC}"
    else
        echo -e "   ${YELLOW}⚠️  请手动打开报告文件${NC}"
    fi
    
    echo ""
}

# 工作流 6: 批量截图
workflow_batch_screenshot() {
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}📸 工作流：批量截图${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    
    local count="${1:-5}"
    local interval="${2:-2}"
    
    echo "1️⃣  准备批量截图..."
    echo "  数量：$count 张"
    echo "  间隔：${interval}秒"
    echo ""
    
    echo "2️⃣  开始截图（3 秒后开始）..."
    sleep 3
    
    for i in $(seq 1 $count); do
        echo "  📸 截图 $i/$count..."
        bash "$SCRIPT_DIR/screenshot.sh" -o ~/Desktop/batch_screenshot_$(date +%H%M%S).png
        if [ $i -lt $count ]; then
            sleep $interval
        fi
    done
    
    echo ""
    echo -e "${GREEN}✅ 批量截图完成！${NC}"
    echo "  保存位置：~/Desktop/batch_screenshot_*.png"
    echo ""
}

# 显示帮助
show_help() {
    echo "用法：$0 [工作流名称]"
    echo ""
    echo "可用工作流:"
    echo "  morning      晨会准备"
    echo "  focus        专注模式"
    echo "  cleanup      下班清理"
    echo "  presentation 演示模式"
    echo "  diagnostic   系统诊断"
    echo "  screenshot   批量截图"
    echo ""
    echo "示例:"
    echo "  $0 morning"
    echo "  $0 focus"
    echo "  $0 screenshot 10 3  # 截图 10 张，间隔 3 秒"
}

# 主逻辑
main() {
    if [ $# -eq 0 ]; then
        show_help
        exit 0
    fi
    
    case $1 in
        morning)
            workflow_morning_prep
            ;;
        focus)
            workflow_focus_mode
            ;;
        cleanup)
            workflow_cleanup
            ;;
        presentation)
            workflow_presentation
            ;;
        diagnostic)
            workflow_diagnostic
            ;;
        screenshot)
            workflow_batch_screenshot "${2:-5}" "${3:-2}"
            ;;
        -h|--help)
            show_help
            ;;
        *)
            echo -e "${RED}❌ 未知工作流：$1${NC}"
            show_help
            exit 1
            ;;
    esac
}

# 运行主函数
main "$@"
