#!/bin/bash
# 选题专家主运行脚本

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
LOG_DIR="$SCRIPT_DIR/logs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/topic_expert_$(date +%Y%m%d_%H%M%S).log"

echo "========================================" | tee -a "$LOG_FILE"
echo "选题专家启动：$(date)" | tee -a "$LOG_FILE"
echo "========================================" | tee -a "$LOG_FILE"

# 1. 获取热点数据
echo "📡 正在获取热点数据..." | tee -a "$LOG_FILE"
python3 "$SCRIPT_DIR/scripts/fetch_hot_topics_ai.py" 2>&1 | tee -a "$LOG_FILE"

if [ ! -f /tmp/hot_topics.json ]; then
    echo "❌ 获取热点数据失败" | tee -a "$LOG_FILE"
    exit 1
fi

# 2. 选题打分
echo "" | tee -a "$LOG_FILE"
echo "📊 正在进行选题打分..." | tee -a "$LOG_FILE"
python3 "$SCRIPT_DIR/scripts/score_topics.py" \
    --hot-data /tmp/hot_topics.json \
    --account-type "AI工具/效率" \
    --min-score 70 \
    2>&1 | tee -a "$LOG_FILE"

if [ ! -f /tmp/scored_topics.json ]; then
    echo "❌ 选题打分失败" | tee -a "$LOG_FILE"
    exit 1
fi

# 检查是否有达标选题
qualified_count=$(cat /tmp/scored_topics.json | python3 -c "import json, sys; print(json.load(sys.stdin)['qualified_topics'])")

if [ "$qualified_count" -eq 0 ]; then
    echo "⚠️  没有达标的选题（≥70分），跳过推送" | tee -a "$LOG_FILE"
    exit 0
fi

# 3. 生成三要素
echo "" | tee -a "$LOG_FILE"
echo "💡 正在生成笔尖三要素..." | tee -a "$LOG_FILE"
python3 "$SCRIPT_DIR/scripts/generate_three_elements.py" \
    --scored-data /tmp/scored_topics.json \
    --account-style "墨云风格/专业实操" \
    --target-platform "公众号" \
    --top-n 3 \
    2>&1 | tee -a "$LOG_FILE"

if [ ! -f /tmp/three_elements.json ]; then
    echo "❌ 生成三要素失败" | tee -a "$LOG_FILE"
    exit 1
fi

# 4. 推送到 Telegram
echo "" | tee -a "$LOG_FILE"
echo "📱 正在推送到 Telegram..." | tee -a "$LOG_FILE"
python3 "$SCRIPT_DIR/scripts/push_to_telegram.py" \
    --data /tmp/three_elements.json \
    2>&1 | tee -a "$LOG_FILE"

echo "" | tee -a "$LOG_FILE"
echo "✅ 选题专家运行完成：$(date)" | tee -a "$LOG_FILE"
echo "========================================" | tee -a "$LOG_FILE"
