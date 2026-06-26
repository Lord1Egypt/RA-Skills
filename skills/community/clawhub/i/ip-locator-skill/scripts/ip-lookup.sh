#!/bin/bash
# IP 归属地查询脚本
# 用法：./ip-lookup.sh [IP 地址...]

API_BASE="http://ip-api.com/json"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 显示使用帮助
show_help() {
    echo "🌐 IP 归属地查询工具"
    echo ""
    echo "用法："
    echo "  $0                    # 查询当前公网 IP"
    echo "  $0 <IP 地址>           # 查询指定 IP"
    echo "  $0 <IP1> <IP2> ...    # 批量查询多个 IP"
    echo ""
    echo "示例："
    echo "  $0 8.8.8.8"
    echo "  $0 1.1.1.1 208.67.222.222"
}

# 查询单个 IP
query_ip() {
    local ip=$1
    local url="$API_BASE/$ip?fields=61439"
    
    # 调用 API
    local response=$(curl -s "$url")
    
    # 检查是否成功
    local status=$(echo "$response" | grep -o '"status":"[^"]*"' | cut -d'"' -f4)
    
    if [ "$status" != "success" ]; then
        echo -e "${RED}❌ 查询失败：$ip${NC}"
        echo "$response" | python3 -m json.tool 2>/dev/null || echo "$response"
        return 1
    fi
    
    # 解析字段
    local country=$(echo "$response" | grep -o '"country":"[^"]*"' | cut -d'"' -f4)
    local countryCode=$(echo "$response" | grep -o '"countryCode":"[^"]*"' | cut -d'"' -f4)
    local region=$(echo "$response" | grep -o '"regionName":"[^"]*"' | cut -d'"' -f4)
    local city=$(echo "$response" | grep -o '"city":"[^"]*"' | cut -d'"' -f4)
    local zip=$(echo "$response" | grep -o '"zip":"[^"]*"' | cut -d'"' -f4)
    local lat=$(echo "$response" | grep -o '"lat":[0-9.-]*' | cut -d':' -f2)
    local lon=$(echo "$response" | grep -o '"lon":[0-9.-]*' | cut -d':' -f2)
    local timezone=$(echo "$response" | grep -o '"timezone":"[^"]*"' | cut -d'"' -f4)
    local isp=$(echo "$response" | grep -o '"isp":"[^"]*"' | cut -d'"' -f4)
    local org=$(echo "$response" | grep -o '"org":"[^"]*"' | cut -d'"' -f4)
    local as=$(echo "$response" | grep -o '"as":"[^"]*"' | cut -d'"' -f4)
    local query=$(echo "$response" | grep -o '"query":"[^"]*"' | cut -d'"' -f4)
    
    # 输出结果
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}🌐 IP 地址：${NC}$query"
    echo -e "${BLUE}📍 位置：${NC}$country $countryCode · $region · $city $zip"
    echo -e "${BLUE}🌍 坐标：${NC}纬度 $lat, 经度 $lon"
    echo -e "${BLUE}🕐 时区：${NC}$timezone"
    echo -e "${BLUE}🌐 运营商：${NC}$isp"
    echo -e "${BLUE}🏢 组织：${NC}$org"
    echo -e "${BLUE}🔗 AS 号：${NC}$as"
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
}

# 主函数
main() {
    # 如果没有参数，查询当前公网 IP
    if [ $# -eq 0 ]; then
        echo -e "${YELLOW}🔍 正在查询当前公网 IP...${NC}"
        echo ""
        query_ip ""
    elif [ "$1" == "-h" ] || [ "$1" == "--help" ]; then
        show_help
    else
        # 批量查询
        for ip in "$@"; do
            echo -e "${YELLOW}🔍 查询：$ip${NC}"
            echo ""
            query_ip "$ip"
        done
    fi
}

# 执行主函数
main "$@"
