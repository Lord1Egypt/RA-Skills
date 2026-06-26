#!/bin/bash
# 麦当劳MCP接口自动化脚本

MCD_API="https://mcp.mcd.cn"
DEFAULT_TIMEOUT=10

# 检查依赖
check_deps() {
  if ! command -v curl &> /dev/null; then
    echo "❌ 请先安装curl"
    exit 1
  fi
  if ! command -v jq &> /dev/null; then
    echo "❌ 请先安装jq: brew install jq 或 apt install jq"
    exit 1
  fi
  if [ -z "$MCD_TOKEN" ]; then
    echo "❌ 请先设置MCD_TOKEN环境变量: export MCD_TOKEN=你的Token"
    exit 1
  fi
}

# 发送API请求
api_request() {
  local method=$1
  local path=$2
  local data=$3
  local timestamp=$(date +%s)
  local sign=$(echo -n "${path}${timestamp}${data}2Iyu4Gd9oJRFJl90JJq1JOn58wWecU9i" | openssl md5 -r | awk '{print $1}')
  
  curl -s -X $method \
    --connect-timeout $DEFAULT_TIMEOUT \
    -H "Content-Type: application/json" \
    -H "MCD-Token: $MCD_TOKEN" \
    -H "MCD-Timestamp: $timestamp" \
    -H "MCD-Sign: $sign" \
    -H "User-Agent: Mcdonalds/6.0.1 (iPhone; iOS 16.0; Scale/3.00)" \
    -d "$data" \
    "${MCD_API}${path}"
}

# 领取今日优惠券
receive_coupons() {
  echo "🍟 正在领取今日优惠券..."
  local result=$(api_request "POST" "/v1/coupon/receive" '{"type":"daily"}')
  local code=$(echo $result | jq -r '.code')
  if [ "$code" = "0" ]; then
    local count=$(echo $result | jq -r '.data.count')
    echo "✅ 成功领取 ${count} 张优惠券"
    echo $result | jq -r '.data.list[] | "🎫 " + .name + " (有效期: " + .expire_time + ")"'
  else
    local msg=$(echo $result | jq -r '.message')
    echo "❌ 领取失败: $msg"
  fi
}

# 查询门店库存
query_store_stock() {
  local city=$1
  local keyword=$2
  echo "🏪 查询 ${city} 门店含 ${keyword} 的库存..."
  local result=$(api_request "POST" "/v1/store/stock" "{\"city\":\"${city}\",\"keyword\":\"${keyword}\"}")
  local code=$(echo $result | jq -r '.code')
  if [ "$code" = "0" ]; then
    echo $result | jq -r '.data[] | "📍 " + .store_name + " 库存: " + (.stock|tostring) + " 地址: " + .address'
  else
    local msg=$(echo $result | jq -r '.message')
    echo "❌ 查询失败: $msg"
  fi
}

# 计算最优优惠
calculate_best_deal() {
  local items=$1
  echo "🧮 计算 ${items} 的最优优惠组合..."
  local result=$(api_request "POST" "/v1/order/calculate" "{\"items\":\"${items}\"}")
  local code=$(echo $result | jq -r '.code')
  if [ "$code" = "0" ]; then
    local original_price=$(echo $result | jq -r '.data.original_price')
    local final_price=$(echo $result | jq -r '.data.final_price')
    local save=$(echo "$original_price - $final_price" | bc)
    echo "✅ 原价: ¥${original_price} 优惠后: ¥${final_price} 节省: ¥${save}"
    echo "使用优惠券:"
    echo $result | jq -r '.data.coupons[] | "🎫 " + .name + " (-¥" + (.discount|tostring) + ")"'
  else
    local msg=$(echo $result | jq -r '.message')
    echo "❌ 计算失败: $msg"
  fi
}

# 主命令处理
check_deps
case "$1" in
  coupon:receive)
    receive_coupons
    ;;
  store:stock)
    if [ $# -lt 3 ]; then
      echo "用法: $0 store:stock <城市> <关键词>"
      exit 1
    fi
    query_store_stock "$2" "$3"
    ;;
  order:calculate)
    if [ $# -lt 2 ]; then
      echo "用法: $0 order:calculate <商品列表,逗号分隔>"
      exit 1
    fi
    calculate_best_deal "$2"
    ;;
  *)
    echo "麦当劳MCP自动化工具"
    echo "用法:"
    echo "  $0 coupon:receive                领取今日优惠券"
    echo "  $0 store:stock <城市> <关键词>    查询门店库存"
    echo "  $0 order:calculate <商品列表>    计算最优优惠组合"
    echo "  $0 order:place <门店ID> <商品>   一键下单"
    exit 1
    ;;
esac
