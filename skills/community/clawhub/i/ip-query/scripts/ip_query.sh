#!/bin/bash

# IP查询脚本
# 查询当前公共IP地址及相关信息

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# 函数：显示帮助信息
show_help() {
    echo "IP查询工具"
    echo "用法: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  -h, --help     显示此帮助信息"
    echo "  -s, --simple   仅显示IP地址（简单模式）"
    echo "  -d, --detail   显示详细信息（默认模式）"
    echo "  -j, --json     以JSON格式输出"
    echo ""
    echo "示例:"
    echo "  $0              # 显示IP和详细信息"
    echo "  $0 --simple     # 仅显示IP地址"
    echo "  $0 --json       # 以JSON格式输出"
}

# 函数：检查命令是否存在
check_command() {
    if ! command -v "$1" &> /dev/null; then
        echo "错误: 未找到命令 '$1'，请先安装"
        exit 1
    fi
}

# 函数：获取简单IP地址
get_simple_ip() {
    echo "🌐 正在查询IP地址..."
    
    # 尝试多个API，直到成功
    local ip=""
    
    # API列表（按优先级排序）
    local apis=(
        "https://api.ipify.org?format=json"
        "https://icanhazip.com"
        "https://ifconfig.me/ip"
        "https://ipecho.net/plain"
    )
    
    for api in "${apis[@]}"; do
        echo -n "尝试 ${api}... "
        if ip=$(curl -s --connect-timeout 5 "$api" 2>/dev/null); then
            # 如果是JSON格式，提取IP字段
            if [[ "$api" == *ipify* ]]; then
                ip=$(echo "$ip" | grep -o '"ip":"[^"]*"' | cut -d'"' -f4)
            fi
            
            # 检查是否获取到有效的IP
            if [[ "$ip" =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
                echo -e "${GREEN}成功${NC}"
                echo "$ip"
                return 0
            fi
            echo -e "${RED}失败${NC}"
        else
            echo -e "${RED}失败${NC}"
        fi
    done
    
    echo -e "${RED}错误: 无法获取IP地址，请检查网络连接${NC}"
    return 1
}

# 函数：获取详细信息
get_detail_info() {
    echo "🌐 正在查询IP详细信息..."
    
    # 使用ipinfo.io获取详细信息
    local info_json=""
    if info_json=$(curl -s --connect-timeout 10 "https://ipinfo.io/json" 2>/dev/null); then
        if [ -n "$info_json" ]; then
            # 检查是否有错误
            if echo "$info_json" | grep -q '"error":'; then
                echo -e "${RED}错误: API限制，请稍后重试${NC}"
                return 1
            fi
            
            # 如果有jq，使用jq解析
            if command -v jq &> /dev/null; then
                local ip=$(echo "$info_json" | jq -r '.ip // empty')
                local city=$(echo "$info_json" | jq -r '.city // empty')
                local region=$(echo "$info_json" | jq -r '.region // empty')
                local country=$(echo "$info_json" | jq -r '.country // empty')
                local loc=$(echo "$info_json" | jq -r '.loc // empty')
                local org=$(echo "$info_json" | jq -r '.org // empty')
                local postal=$(echo "$info_json" | jq -r '.postal // empty')
                local timezone=$(echo "$info_json" | jq -r '.timezone // empty')
                
                # 从org中提取ISP
                local isp=""
                if [[ -n "$org" ]]; then
                    isp=$(echo "$org" | sed 's/^[^ ]* //')
                fi
                
                # 显示结果
                echo ""
                echo -e "${CYAN}════════════════════════════════════════${NC}"
                echo -e "${GREEN}🌐 您的公共IP地址: ${YELLOW}$ip${NC}"
                echo -e "${CYAN}════════════════════════════════════════${NC}"
                
                if [[ -n "$city" || -n "$region" || -n "$country" ]]; then
                    echo -e "${BLUE}📍 位置信息:${NC}"
                    [[ -n "$city" ]] && echo -e "  - 城市: $city"
                    [[ -n "$region" ]] && echo -e "  - 地区: $region"
                    [[ -n "$country" ]] && echo -e "  - 国家: $country"
                    [[ -n "$postal" ]] && echo -e "  - 邮编: $postal"
                    [[ -n "$loc" ]] && echo -e "  - 经纬度: $loc"
                    [[ -n "$timezone" ]] && echo -e "  - 时区: $timezone"
                    echo ""
                fi
                
                if [[ -n "$org" ]]; then
                    echo -e "${BLUE}🏢 网络信息:${NC}"
                    echo -e "  - 组织: $org"
                    [[ -n "$isp" ]] && echo -e "  - ISP: $isp"
                    echo ""
                fi
                
                echo -e "${BLUE}🔒 隐私提示:${NC}"
                echo "  这是您的公网IP地址，请勿随意分享。"
                echo "  此信息由 ipinfo.io 提供。"
                echo -e "${CYAN}════════════════════════════════════════${NC}"
                
            else
                # 没有jq，显示原始JSON
                echo "$info_json"
            fi
            return 0
        fi
    fi
    
    echo -e "${RED}错误: 无法获取详细信息，请检查网络连接${NC}"
    return 1
}

# 函数：JSON格式输出
get_json_info() {
    local info_json=""
    if info_json=$(curl -s --connect-timeout 10 "https://ipinfo.io/json" 2>/dev/null); then
        if [ -n "$info_json" ]; then
            echo "$info_json"
            return 0
        fi
    fi
    
    # 如果失败，返回简单IP
    local ip=$(get_simple_ip 2>/dev/null)
    if [ -n "$ip" ]; then
        echo "{\"ip\": \"$ip\", \"error\": \"无法获取详细信息\"}"
        return 0
    fi
    
    echo "{\"error\": \"无法获取IP信息\"}"
    return 1
}

# 主函数
main() {
    # 检查curl是否安装
    check_command "curl"
    
    # 解析参数
    local mode="detail"
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_help
                exit 0
                ;;
            -s|--simple)
                mode="simple"
                shift
                ;;
            -d|--detail)
                mode="detail"
                shift
                ;;
            -j|--json)
                mode="json"
                shift
                ;;
            *)
                echo -e "${RED}错误: 未知参数 '$1'${NC}"
                show_help
                exit 1
                ;;
        esac
    done
    
    # 根据模式执行
    case "$mode" in
        "simple")
            get_simple_ip
            ;;
        "detail")
            get_detail_info
            ;;
        "json")
            get_json_info
            ;;
    esac
}

# 运行主函数
main "$@"