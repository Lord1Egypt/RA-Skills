#!/bin/bash
# macOS 系统信息脚本
# 用法：./system_info.sh [选项]

set -euo pipefail

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# 显示帮助
show_help() {
    echo "macOS 系统信息工具"
    echo ""
    echo "用法：$0 [选项]"
    echo ""
    echo "选项:"
    echo "  -a, --all        显示所有信息"
    echo "  -h, --hardware   硬件信息"
    echo "  -s, --software   软件信息"
    echo "  -d, --disk       磁盘信息"
    echo "  -m, --memory     内存信息"
    echo "  -n, --network    网络信息"
    echo "  -b, --battery    电池信息"
    echo "  -j, --json       JSON 格式输出"
    echo "  --short          简要信息（默认）"
    echo "  -h, --help       显示帮助"
}

# 硬件信息
show_hardware() {
    echo -e "${BLUE}💻 硬件信息：${NC}"
    echo ""
    
    # 型号
    local model
    model=$(system_profiler SPHardwareDataType 2>/dev/null | grep "Model Name" | cut -d: -f2 | xargs)
    echo -e "  ${CYAN}型号:${NC} $model"
    
    # 芯片
    local chip
    chip=$(system_profiler SPHardwareDataType 2>/dev/null | grep "Chip" | cut -d: -f2 | xargs)
    if [ -n "$chip" ]; then
        echo -e "  ${CYAN}芯片:${NC} $chip"
    else
        local processor
        processor=$(system_profiler SPHardwareDataType 2>/dev/null | grep "Processor Name" | cut -d: -f2 | xargs)
        echo -e "  ${CYAN}处理器:${NC} $processor"
    fi
    
    # 内存
    local memory
    memory=$(system_profiler SPHardwareDataType 2>/dev/null | grep "Memory" | cut -d: -f2 | xargs)
    echo -e "  ${CYAN}内存:${NC} $memory"
    
    # 序列号
    local serial
    serial=$(system_profiler SPHardwareDataType 2>/dev/null | grep "Serial Number" | cut -d: -f2 | xargs)
    echo -e "  ${CYAN}序列号:${NC} ${serial:0:8}..."
    
    echo ""
}

# 软件信息
show_software() {
    echo -e "${BLUE}📀 软件信息：${NC}"
    echo ""
    
    # macOS 版本
    local macos_version
    macos_version=$(sw_vers -productVersion)
    local macos_build
    macos_build=$(sw_vers -buildVersion)
    local macos_name
    macos_name=$(sw_vers -productName)
    echo -e "  ${CYAN}系统:${NC} $macos_name $macos_version ($macos_build)"
    
    # 启动磁盘
    local startup_disk
    startup_disk=$(df -h / | tail -1 | awk '{print $1}')
    echo -e "  ${CYAN}启动磁盘:${NC} $startup_disk"
    
    # 正常运行时间
    local uptime
    uptime=$(uptime | sed 's/.*up //' | sed 's/,.*//')
    echo -e "  ${CYAN}运行时间:${NC} $uptime"
    
    echo ""
}

# 磁盘信息
show_disk() {
    echo -e "${BLUE}💾 磁盘信息：${NC}"
    echo ""
    
    printf "  %-20s %10s %10s %10s %s\n" "挂载点" "总量" "已用" "可用" "使用率"
    echo "  ───────────────────────────────────────────────────"
    
    df -h | tail -n +2 | grep -E "^/dev" | head -5 | while read -r filesystem size used avail capacity mountpoint; do
        printf "  %-20s %10s %10s %10s %s\n" "$mountpoint" "$size" "$used" "$avail" "$capacity"
    done
    
    echo ""
}

# 内存信息
show_memory() {
    echo -e "${BLUE}🧠 内存信息：${NC}"
    echo ""
    
    # 物理内存
    local phys_mem
    phys_mem=$(sysctl -n hw.memsize 2>/dev/null | awk '{printf "%.1f GB", $1/1024/1024/1024}')
    echo -e "  ${CYAN}物理内存:${NC} $phys_mem"
    
    # 内存使用情况
    local mem_info
    mem_info=$(vm_stat 2>/dev/null)
    
    local page_size=4096  # macOS 默认页面大小
    
    local free_pages
    free_pages=$(echo "$mem_info" | grep "Pages free" | awk -F: '{print $2}' | xargs | cut -d. -f1)
    local active_pages
    active_pages=$(echo "$mem_info" | grep "Pages active" | awk -F: '{print $2}' | xargs | cut -d. -f1)
    local inactive_pages
    inactive_pages=$(echo "$mem_info" | grep "Pages inactive" | awk -F: '{print $2}' | xargs | cut -d. -f1)
    local wired_pages
    wired_pages=$(echo "$mem_info" | grep "Pages wired down" | awk -F: '{print $2}' | xargs | cut -d. -f1)
    
    # 防止空值导致计算错误
    free_pages=${free_pages:-0}
    active_pages=${active_pages:-0}
    wired_pages=${wired_pages:-0}
    
    local free_mem=$((free_pages * page_size / 1024 / 1024))
    local active_mem=$((active_pages * page_size / 1024 / 1024))
    local wired_mem=$((wired_pages * page_size / 1024 / 1024))
    
    echo -e "  ${CYAN}空闲:${NC} ${free_mem} MB"
    echo -e "  ${CYAN}活跃:${NC} ${active_mem} MB"
    echo -e "  ${CYAN}已占用:${NC} ${wired_mem} MB"
    
    echo ""
}

# 网络信息
show_network() {
    echo -e "${BLUE}🌐 网络信息：${NC}"
    echo ""
    
    # 获取网络接口
    local interfaces
    interfaces=$(networksetup -listallhardwareports 2>/dev/null | grep "Hardware Port" | cut -d: -f2 | xargs)
    
    echo -e "  ${CYAN}网络接口:${NC}"
    echo "$interfaces" | while read -r iface; do
        echo "    - $iface"
    done
    
    # 本地 IP
    local local_ip
    local_ip=$(ipconfig getifaddr en0 2>/dev/null || ipconfig getifaddr en1 2>/dev/null || echo "N/A")
    echo -e "  ${CYAN}本地 IP:${NC} $local_ip"
    
    # 公网 IP（可选，可能需要网络）
    # local public_ip
    # public_ip=$(curl -s ifconfig.me 2>/dev/null || echo "N/A")
    # echo -e "  ${CYAN}公网 IP:${NC} $public_ip"
    
    echo ""
}

# 电池信息
show_battery() {
    echo -e "${BLUE}🔋 电池信息：${NC}"
    echo ""
    
    # 检查是否有电池（台式机没有）
    if ! system_profiler SPPowerDataType &>/dev/null; then
        echo "  无电池（台式机）"
        echo ""
        return
    fi
    
    local battery_info
    battery_info=$(pmset -g batt 2>/dev/null)
    
    if echo "$battery_info" | grep -q "Battery"; then
        local percent
        percent=$(echo "$battery_info" | grep -oP '\d+%' | head -1)
        local status
        status=$(echo "$battery_info" | grep -oP '(discharging|charging|AC attached)' | head -1)
        
        echo -e "  ${CYAN}电量:${NC} $percent"
        echo -e "  ${CYAN}状态:${NC} $status"
    else
        echo "  无电池信息"
    fi
    
    echo ""
}

# 简要信息
show_short() {
    echo -e "${BLUE}📊 系统摘要：${NC}"
    echo ""
    
    # 型号
    local model
    model=$(system_profiler SPHardwareDataType 2>/dev/null | grep "Model Name" | cut -d: -f2 | xargs)
    echo -e "  ${CYAN}型号:${NC} $model"
    
    # 芯片
    local chip
    chip=$(system_profiler SPHardwareDataType 2>/dev/null | grep "Chip" | cut -d: -f2 | xargs)
    if [ -n "$chip" ]; then
        echo -e "  ${CYAN}芯片:${NC} $chip"
    fi
    
    # 内存
    local memory
    memory=$(system_profiler SPHardwareDataType 2>/dev/null | grep "Memory" | cut -d: -f2 | xargs)
    echo -e "  ${CYAN}内存:${NC} $memory"
    
    # macOS 版本
    local macos_version
    macos_version=$(sw_vers -productVersion)
    echo -e "  ${CYAN}系统:${NC} macOS $macos_version"
    
    # 磁盘使用
    local disk_usage
    disk_usage=$(df -h / | tail -1 | awk '{print $5}')
    echo -e "  ${CYAN}磁盘使用:${NC} $disk_usage"
    
    # 运行时间
    local uptime
    uptime=$(uptime | sed 's/.*up //' | sed 's/,.*//')
    echo -e "  ${CYAN}运行时间:${NC} $uptime"
    
    echo ""
}

# JSON 格式输出
output_json() {
    local model
    model=$(system_profiler SPHardwareDataType 2>/dev/null | grep "Model Name" | cut -d: -f2 | xargs | sed 's/"/\\"/g')
    
    local macos_version
    macos_version=$(sw_vers -productVersion)
    
    local memory
    memory=$(system_profiler SPHardwareDataType 2>/dev/null | grep "Memory" | cut -d: -f2 | xargs)
    
    local disk_usage
    disk_usage=$(df -h / | tail -1 | awk '{print $5}' | tr -d '%')
    
    cat <<EOF
{
  "hardware": {
    "model": "$model",
    "memory": "$memory"
  },
  "software": {
    "macos_version": "$macos_version"
  },
  "disk": {
    "usage_percent": $disk_usage
  },
  "timestamp": "$(date -Iseconds)"
}
EOF
}

# 主逻辑
main() {
    if [ $# -eq 0 ]; then
        show_short
        exit 0
    fi
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            -a|--all)
                show_hardware
                show_software
                show_disk
                show_memory
                show_network
                show_battery
                shift
                ;;
            -h|--hardware)
                show_hardware
                shift
                ;;
            -s|--software)
                show_software
                shift
                ;;
            -d|--disk)
                show_disk
                shift
                ;;
            -m|--memory)
                show_memory
                shift
                ;;
            -n|--network)
                show_network
                shift
                ;;
            -b|--battery)
                show_battery
                shift
                ;;
            -j|--json)
                output_json
                shift
                ;;
            --short)
                show_short
                shift
                ;;
            --help)
                show_help
                exit 0
                ;;
            *)
                echo -e "${RED}❌ 未知选项：$1${NC}"
                show_help
                exit 1
                ;;
        esac
    done
}

# 运行主函数
main "$@"
