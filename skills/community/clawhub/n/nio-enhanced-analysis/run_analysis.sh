#!/bin/bash
# NIO增强分析脚本

cd "$(dirname "$0")"

MARKET_TYPE=$1
if [ -z "$MARKET_TYPE" ]; then
    MARKET_TYPE="us"
fi

echo "🚀 开始NIO${MARKET_TYPE}增强分析..."
python3 analyze_nio.py $MARKET_TYPE

# 保存日志
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
LOG_FILE="logs/nio_analysis_${MARKET_TYPE}_${TIMESTAMP}.log"
mkdir -p logs

{
    echo "分析时间: $(date)"
    echo "市场类型: $MARKET_TYPE"
    echo "="*60
    python3 analyze_nio.py $MARKET_TYPE 2>&1
} > "$LOG_FILE"

echo "📋 分析日志已保存到: $LOG_FILE"