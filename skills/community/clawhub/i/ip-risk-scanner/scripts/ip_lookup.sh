#!/usr/bin/env bash
# IP 信息查询脚本
# 用途：查询 IP 的地理位置、运营商、ASN 等基本信息

set -e

IP_ADDRESS="$1"

if [ -z "$IP_ADDRESS" ]; then
    echo "用法：$0 <IP 地址>"
    echo "示例：$0 45.129.228.121"
    exit 1
fi

# 验证 IP 格式
if ! [[ $IP_ADDRESS =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$ ]]; then
    echo "错误：无效的 IP 地址格式"
    exit 1
fi

echo "正在查询 IP: $IP_ADDRESS"
echo "======================================"

# 1. 反向 DNS 查询
echo -e "\n📌 反向 DNS 查询:"
dig -x "$IP_ADDRESS" +short 2>/dev/null || nslookup "$IP_ADDRESS" 2>/dev/null | grep "name =" | cut -d'=' -f2 || echo "无反向 DNS 记录"

# 2. WHOIS 查询（简略）
echo -e "\n📌 WHOIS 信息:"
whois "$IP_ADDRESS" 2>/dev/null | grep -E "^(OrgName|NetName|Country|State|City):" | head -10 || echo "WHOIS 查询失败"

# 3. 地理位置查询（使用多种 API）
echo -e "\n📌 地理位置查询:"

# 尝试 ip-api.com (免费，有限制)
GEO_RESULT=$(curl -s "http://ip-api.com/json/$IP_ADDRESS" 2>/dev/null)
if [ -n "$GEO_RESULT" ] && ! echo "$GEO_RESULT" | grep -q '"status":"fail"'; then
    COUNTRY=$(echo "$GEO_RESULT" | grep -o '"country":"[^"]*"' | cut -d'"' -f4)
    REGION=$(echo "$GEO_RESULT" | grep -o '"regionName":"[^"]*"' | cut -d'"' -f4)
    CITY=$(echo "$GEO_RESULT" | grep -o '"city":"[^"]*"' | cut -d'"' -f4)
    ISP=$(echo "$GEO_RESULT" | grep -o '"isp":"[^"]*"' | cut -d'"' -f4)
    ORG=$(echo "$GEO_RESULT" | grep -o '"org":"[^"]*"' | cut -d'"' -f4)
    AS=$(echo "$GEO_RESULT" | grep -o '"as":"[^"]*"' | cut -d'"' -f4)

    echo "  国家：$COUNTRY"
    echo "  省份/州：$REGION"
    echo "  城市：$CITY"
    echo "  ISP: $ISP"
    echo "  组织：$ORG"
    echo "  ASN: $AS"
else
    echo "  ip-api.com 查询失败，尝试其他 API..."
    # 备用 API: ipapi.co
    GEO_RESULT2=$(curl -s "https://ipapi.co/$IP_ADDRESS/json/" 2>/dev/null)
    if [ -n "$GEO_RESULT2" ]; then
        echo "$GEO_RESULT2" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print(f\"  国家：{data.get('country_name', 'N/A')}\")
    print(f\"  省份：{data.get('region', 'N/A')}\")
    print(f\"  城市：{data.get('city', 'N/A')}\")
    print(f\"  ISP: {data.get('org', 'N/A')}\")
    print(f\"  ASN: {data.get('asn', 'N/A')}\")
except:
    print('  API 查询失败')
" 2>/dev/null || echo "  所有 API 查询失败"
    fi
fi

# 4. 网络延迟测试
echo -e "\n📌 网络延迟测试:"
ping -c 2 -W 2 "$IP_ADDRESS" 2>/dev/null | tail -1 || echo "Ping 测试失败"

echo ""
echo "======================================"
echo "✅ IP 基础信息查询完成"
