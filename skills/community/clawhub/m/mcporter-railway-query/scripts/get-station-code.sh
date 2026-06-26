#!/bin/bash
# 使用 mcporter 查询车站代码
# 用法: get-station-code.sh <城市名或车站名>

set -e

NAME="$1"
CONFIG_FILE="${2:-$HOME/.mcporter/mcporter.json}"

if [ -z "$NAME" ]; then
    echo "用法: get-station-code.sh <城市名或车站名>"
    echo "示例: get-station-code.sh 上海"
    echo "示例: get-station-code.sh 上海虹桥"
    exit 1
fi

echo "查询: $NAME 的车站代码"
echo ""

# 尝试先按车站名查询，失败则按城市查询
# 注意: 暂时关闭 set -e 以允许第一条命令失败后降级重试
set +e
mcporter call 12306.get-station-code-by-names \
  stationNames="$NAME" \
  --config "$CONFIG_FILE" 2>/dev/null
EXIT_CODE=$?
set -e

if [ $EXIT_CODE -ne 0 ]; then
  # 按车站名查询失败，降级按城市查询
  mcporter call 12306.get-station-code-of-citys \
    citys="$NAME" \
    --config "$CONFIG_FILE"
fi