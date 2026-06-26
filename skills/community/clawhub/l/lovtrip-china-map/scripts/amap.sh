#!/bin/bash
# amap.sh — 高德地图 API 兜底脚本（无需 MCP Server）
# 用法: AMAP_API_KEY=xxx ./amap.sh <command> [args...]
#
# 命令:
#   geocode <address> [city]          地理编码
#   reverse <lng> <lat>               逆地理编码
#   nearby <lng> <lat> <keywords>     周边搜索
#   route <o_lng> <o_lat> <d_lng> <d_lat> [mode]  路线规划
#   detail <poi_id>                   地点详情

set -euo pipefail

cmd="${1:-help}"
shift || true

# help 不需要 API Key
if [ "$cmd" = "help" ] || [ "$cmd" = "--help" ] || [ "$cmd" = "-h" ]; then
  echo "高德地图 API 兜底脚本"
  echo ""
  echo "用法: AMAP_API_KEY=xxx ./amap.sh <command> [args...]"
  echo ""
  echo "命令:"
  echo "  geocode <address> [city]                       地理编码"
  echo "  reverse <lng> <lat>                            逆地理编码"
  echo "  nearby <lng> <lat> <keywords> [radius]         周边搜索"
  echo "  route <o_lng> <o_lat> <d_lng> <d_lat> [mode]   路线规划"
  echo "  detail <poi_id>                                地点详情"
  exit 0
fi

API_KEY="${AMAP_API_KEY:?请设置 AMAP_API_KEY 环境变量}"
BASE="https://restapi.amap.com/v3"

case "$cmd" in
  geocode)
    address="${1:?用法: amap.sh geocode <address> [city]}"
    city="${2:-}"
    url="$BASE/geocode/geo?key=$API_KEY&address=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$address'))")"
    [ -n "$city" ] && url="$url&city=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$city'))")"
    curl -s "$url" | python3 -m json.tool
    ;;

  reverse)
    lng="${1:?用法: amap.sh reverse <lng> <lat>}"
    lat="${2:?用法: amap.sh reverse <lng> <lat>}"
    curl -s "$BASE/geocode/regeo?key=$API_KEY&location=$lng,$lat" | python3 -m json.tool
    ;;

  nearby)
    lng="${1:?用法: amap.sh nearby <lng> <lat> <keywords>}"
    lat="${2:?用法: amap.sh nearby <lng> <lat> <keywords>}"
    keywords="${3:?用法: amap.sh nearby <lng> <lat> <keywords>}"
    radius="${4:-2000}"
    curl -s "$BASE/place/around?key=$API_KEY&location=$lng,$lat&keywords=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$keywords'))")&radius=$radius" | python3 -m json.tool
    ;;

  route)
    o_lng="${1:?用法: amap.sh route <o_lng> <o_lat> <d_lng> <d_lat> [mode]}"
    o_lat="$2"
    d_lng="$3"
    d_lat="$4"
    mode="${5:-transit}"
    if [ "$mode" = "transit" ]; then
      curl -s "$BASE/direction/transit/integrated?key=$API_KEY&origin=$o_lng,$o_lat&destination=$d_lng,$d_lat&city=北京" | python3 -m json.tool
    elif [ "$mode" = "driving" ]; then
      curl -s "$BASE/direction/driving?key=$API_KEY&origin=$o_lng,$o_lat&destination=$d_lng,$d_lat" | python3 -m json.tool
    else
      curl -s "$BASE/direction/walking?key=$API_KEY&origin=$o_lng,$o_lat&destination=$d_lng,$d_lat" | python3 -m json.tool
    fi
    ;;

  detail)
    poi_id="${1:?用法: amap.sh detail <poi_id>}"
    curl -s "$BASE/place/detail?key=$API_KEY&id=$poi_id" | python3 -m json.tool
    ;;

  *)
    echo "Unknown command: $cmd"
    echo "Run './amap.sh help' for usage."
    exit 1
    ;;
esac
