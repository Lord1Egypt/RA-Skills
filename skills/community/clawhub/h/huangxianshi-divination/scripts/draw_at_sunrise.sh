#!/bin/bash
# 黄仙师灵签 - 日出时分解签
# 每天获取当天真正日出时间并摇签

cd /workspace/skills/huangxianshi-divination

# 获取上海日出时间
SUNRISE=$(curl -s "wttr.in/Shanghai?format=%S" 2>/dev/null)
if [ -z "$SUNRISE" ]; then
    echo "获取日出时间失败，使用默认 6:06"
    SUNRISE="06:06:04"
fi

# 提取小时和分钟
HOUR=$(echo "$SUNRISE" | cut -d: -f1)
MIN=$(echo "$SUNRISE" | cut -d: -f2)

echo "今日上海日出: $HOUR:$MIN"

# 计算等待时间（等待到日出时刻）
CURRENT_HOUR=$(date +%H)
CURRENT_MIN=$(date +%M)

# 转换为总分钟数
CURRENT_TOTAL=$((10#$CURRENT_HOUR * 60 + 10#$CURRENT_MIN))
SUNRISE_TOTAL=$((10#$HOUR * 60 + 10#$MIN))

# 计算等待分钟数
WAIT_MIN=$((SUNRISE_TOTAL - CURRENT_TOTAL))

if [ $WAIT_MIN -gt 0 ]; then
    echo "等待 $WAIT_MIN 分钟到日出..."
    sleep $((WAIT_MIN * 60))
fi

echo "===== 日出时分到，摇签！====="

# 运行抽签
python3 scripts/lot_cli.py draw-ritual 2>&1
