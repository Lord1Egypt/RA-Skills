#!/bin/bash
#
# BizyAir 分镜图生成 Shell 脚本
#
# 使用方法:
#   export BIZYAIR_API_KEY="your_key"
#   ./scripts/bizyair_api.sh "你的描述" [ratio] [batch_size]
#
# 示例:
#   ./scripts/bizyair_api.sh "一个穿汉服的女孩在花园里" 9:16 4
#

# 退出策略：创建任务失败时立即退出，轮询时允许网络重试
set -e  # 创建任务阶段
set +e  # 轮询阶段（在下面切换）

# API 配置
API_ENDPOINT="https://api.bizyair.cn/w/v1/webapp/task/openapi"
WEB_APP_ID=38223

# 超时配置（秒）
POLL_TIMEOUT=900          # 15 分钟轮询超时
POLL_INTERVAL=5           # 5 秒轮询间隔
PROGRESS_INTERVAL=30      # 30 秒进度提示间隔

# 模特提示词
MODEL_SUFFIX=",漏斗身材，大胸展示，moweifei，feifei 妃妃,一位大美女，完美身材，写实人像写真、中式风格、韩式写真、人像写真，氛围海报，艺术摄影,a photo-realistic shoot from a front camera angle about a young woman , a 20-year-old asian woman with light skin and brown hair styled in a single hair bun, looking directly at the camera with a neutral expression, "

# 尺寸映射
get_size() {
    case "$1" in
        "1:1")   echo "1240 1240" ;;
        "4:3")   echo "1080 1440" ;;
        "3:4")   echo "1440 1080" ;;
        "9:16")  echo "928 1664" ;;
        "16:9")  echo "1664 928" ;;
        "1:2")   echo "870 1740" ;;
        "2:1")   echo "1740 870" ;;
        "1:3")   echo "720 2160" ;;
        "3:1")   echo "2160 720" ;;
        "2:3")   echo "960 1440" ;;
        "3:2")   echo "1440 960" ;;
        "2:5")   echo "720 1800" ;;
        "5:2")   echo "1800 720" ;;
        "3:5")   echo "960 1600" ;;
        "5:3")   echo "1600 960" ;;
        "4:5")   echo "1080 1350" ;;
        "5:4")   echo "1350 1080" ;;
        *)       echo "928 1664" ;;
    esac
}

# 检测模特关键词
has_model_keyword() {
    local text="$1"
    local keywords_zh="模特 人物 人像 女性 女士 女孩 美女 穿搭 展示 试穿"
    local keywords_en="model woman female girl portrait character person"

    for kw in $keywords_zh; do
        if echo "$text" | grep -q "$kw"; then
            return 0
        fi
    done

    for kw in $keywords_en; do
        if echo "$text" | grep -qi "$kw"; then
            return 0
        fi
    done

    return 1
}

# 处理 prompt
process_prompt() {
    local prompt="$1"

    if has_model_keyword "$prompt"; then
        if ! echo "$prompt" | grep -q "moweifei"; then
            echo "${prompt}${MODEL_SUFFIX}"
            return
        fi
    fi

    echo "$prompt"
}

# 检查参数
if [ -z "$1" ]; then
    echo "使用方法: $0 \"描述\" [比例] [批次]"
    echo "示例: $0 \"一个穿汉服的女孩\" 9:16 4"
    exit 1
fi

if [ -z "$BIZYAIR_API_KEY" ]; then
    echo "错误: BIZYAIR_API_KEY 环境变量未设置"
    exit 1
fi

# 解析参数
PROMPT="$1"
RATIO="${2:-9:16}"
BATCH_SIZE="${3:-4}"

# 处理 prompt
FINAL_PROMPT=$(process_prompt "$PROMPT")
if [ "$FINAL_PROMPT" != "$PROMPT" ]; then
    echo "🤖 检测到模特关键词，已自动追加提示词"
fi

# 获取尺寸
read -r WIDTH HEIGHT <<< "$(get_size "$RATIO")"

echo "📤 创建任务: prompt='$PROMPT', size=${WIDTH}x${HEIGHT}, batch=$BATCH_SIZE"

# 创建任务
RESPONSE=$(curl -s -X POST "$API_ENDPOINT/create" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $BIZYAIR_API_KEY" \
    -H "X-Bizyair-Task-Async: enable" \
    --max-time 30 \
    -d "{
        \"web_app_id\": $WEB_APP_ID,
        \"suppress_preview_output\": true,
        \"input_values\": {
            \"107:BizyAirSiliconCloudLLMAPI.user_prompt\": \"$FINAL_PROMPT\",
            \"81:EmptySD3LatentImage.width\": $WIDTH,
            \"81:EmptySD3LatentImage.height\": $HEIGHT,
            \"81:EmptySD3LatentImage.batch_size\": $BATCH_SIZE
        }
    }")

# 提取 requestId
REQUEST_ID=$(echo "$RESPONSE" | grep -o '"requestId":"[^"]*"' | cut -d'"' -f4)

if [ -z "$REQUEST_ID" ]; then
    echo "❌ 创建任务失败: $RESPONSE"
    exit 1
fi

echo "✅ 任务已创建，ID: $REQUEST_ID"
echo "💡 图片生成通常需要 3-10 分钟，请耐心等待"

# 轮询状态
echo "⏳ 开始轮询任务状态（预计 3-10 分钟）..."
set +e  # 轮询阶段允许网络失败重试

START_TIME=$(date +%s)
LAST_PROGRESS_TIME=$START_TIME
POLL_COUNT=0

while true; do
    CURRENT_TIME=$(date +%s)
    ELAPSED=$((CURRENT_TIME - START_TIME))
    ELAPSED_MINUTES=$(echo "scale=1; $ELAPSED / 60" | bc)

    # 检查超时
    if [ $ELAPSED -ge $POLL_TIMEOUT ]; then
        echo "❌ 任务轮询超时（$(echo "$POLL_TIMEOUT / 60" | bc) 分钟）"
        exit 1
    fi

    POLL_COUNT=$((POLL_COUNT + 1))

    # 定期输出进度
    if [ $((CURRENT_TIME - LAST_PROGRESS_TIME)) -ge $PROGRESS_INTERVAL ]; then
        echo "⏱️ 任务进行中... 已等待 ${ELAPSED_MINUTES} 分钟 (轮询 ${POLL_COUNT})"
        LAST_PROGRESS_TIME=$CURRENT_TIME
    fi

    # 查询状态（允许失败后重试）
    STATUS_RESP=$(curl -s "$API_ENDPOINT/detail?requestId=$REQUEST_ID" \
        -H "Authorization: Bearer $BIZYAIR_API_KEY" \
        --max-time 20 2>/dev/null)

    # 检查 curl 是否成功
    if [ $? -ne 0 ] || [ -z "$STATUS_RESP" ]; then
        echo "⚠️ [${POLL_COUNT}] 查询失败，继续轮询..."
        sleep $POLL_INTERVAL
        continue
    fi

    STATUS=$(echo "$STATUS_RESP" | grep -o '"status":"[^"]*"' | cut -d'"' -f4)

    echo "🔄 [${POLL_COUNT}] 当前状态: ${STATUS} (${ELAPSED_MINUTES}分钟)"

    if [ "$STATUS" = "Success" ]; then
        echo "✅ 任务完成（总耗时 ${ELAPSED_MINUTES} 分钟，轮询 ${POLL_COUNT} 次）"
        break
    elif [ "$STATUS" = "Failed" ] || [ "$STATUS" = "Canceled" ]; then
        ERROR_INFO=$(echo "$STATUS_RESP" | grep -o '"error_info":{[^}]*}' | head -1)
        ERROR_MSG=$(echo "$ERROR_INFO" | grep -o '"message":"[^"]*"' | cut -d'"' -f4)
        echo "❌ 任务${STATUS}: ${ERROR_MSG:-未知错误}"
        exit 1
    fi

    sleep $POLL_INTERVAL
done

set -e  # 恢复严格错误检查

# 获取结果
echo "📥 获取任务结果..."
OUTPUTS_RESP=$(curl -s "$API_ENDPOINT/outputs?requestId=$REQUEST_ID" \
    -H "Authorization: Bearer $BIZYAIR_API_KEY" \
    --max-time 30)

# 提取 URL
echo ""
echo "============================================================"
echo "🎨 分镜场景图生成结果"
echo "============================================================"
echo "📝 Prompt: ${PROMPT:0:80}..."
echo "📐 尺寸: ${WIDTH}×${HEIGHT}"
echo "⏱️ 耗时: ${ELAPSED_MINUTES} 分钟"
echo ""
echo "| 序号 | 图片 URL |"
echo "| --- | --- |"

IMAGE_COUNT=0
echo "$OUTPUTS_RESP" | grep -o '"object_url":"[^"]*"' | cut -d'"' -f4 | while read -r url; do
    IMAGE_COUNT=$((IMAGE_COUNT + 1))
    echo "| ${IMAGE_COUNT} | ${url} |"
done

echo ""
echo "============================================================"
