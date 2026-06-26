#!/bin/bash
# LifeLog Recorder - 实时记录单条消息到 Notion（只记录日常生活）
# 使用 OpenClaw SubAgent 智能判断日期

# Notion 凭据 - 从环境变量读取
NOTION_KEY="${NOTION_KEY:-}"
DATABASE_ID="${NOTION_DATABASE_ID:-}"

if [[ -z "$NOTION_KEY" ]]; then
    echo "Error: NOTION_KEY environment variable not set" >&2
    echo "Please set: export NOTION_KEY='your-notion-integration-token'" >&2
    echo "And optionally: export NOTION_DATABASE_ID='your-database-id'" >&2
    exit 1
fi

# 如果没有提供 DATABASE_ID，使用默认值（需要用户替换）
if [[ -z "$DATABASE_ID" ]]; then
    echo "Error: NOTION_DATABASE_ID environment variable not set" >&2
    echo "Please set: export NOTION_DATABASE_ID='your-database-id'" >&2
    exit 1
fi
API_VERSION="2022-06-28"
OPENCLAW_URL="http://localhost:421"

# 参数：消息内容 [可选：日期YYYY-MM-DD]
CONTENT="$1"
OPTIONAL_DATE="$2"

# 使用 SubAgent 判断日期
decide_date_with_subagent() {
    local content="$1"
    
    # 调用 OpenClaw subagent
    local result=$(curl -s -X POST "$OPENCLAW_URL/api/sessions" \
        -H "Content-Type: application/json" \
        -d '{
            "runtime": "subagent",
            "model": "minimax/MiniMax-M2.5",
            "task": "你是 LifeLog 系统的日期判断专家。当前是2026年3月14日（北京时间）。根据以下用户输入的文本，判断这条记录应该属于哪一天。\n\n用户输入：'"$content"'\n\n判断规则：\n1. 如果文本中明确提到「昨天」「前天」「今天」「明天」等，使用对应的日期（昨天=2026-03-13，前天=2026-03-12，大前天=2026-03-11）\n2. 如果没有明确日期，分析上下文（比如「早上」「下午」「晚上」等时间词，结合今天正在进行的活动）\n3. 如果仍然无法判断，输出今天的日期：2026-03-14\n\n只输出日期，格式：YYYY-MM-DD，不要输出其他任何内容。",
            "runTimeoutSeconds": 30
        }')
    
    # 解析返回的日期
    local decided_date=$(echo "$result" | grep -oE "[0-9]{4}-[0-9]{2}-[0-9]{2}" | head -1)
    
    if [ -z "$decided_date" ]; then
        echo ""
    else
        echo "$decided_date"
    fi
}

# 备用：简单日期解析（仅当 SubAgent 完全失败时）
parse_date_fallback() {
    local content="$1"
    local today="2026-03-14"
    
    # 昨天/昨儿
    if echo "$content" | grep -qE "昨天|昨日|昨儿"; then
        date -d "yesterday" +%Y-%m-%d
        return
    fi
    
    # 前天
    if echo "$content" | grep -qE "前天"; then
        date -d "2 days ago" +%Y-%m-%d
        return
    fi
    
    # 今天/今儿
    if echo "$content" | grep -qE "今天|今日|今儿"; then
        echo "$today"
        return
    fi
    
    # 无法判断，返回今天
    echo "$today"
}

# 主逻辑
TODAY=$(date +%Y-%m-%d)

# 如果传入了日期参数，直接使用
if [ -n "$OPTIONAL_DATE" ]; then
    TARGET_DATE="$OPTIONAL_DATE"
    echo "📅 使用传入的日期: $TARGET_DATE"
else
    # 没有传入日期，使用 SubAgent 判断（这里保留接口，未来可以在这里调用 subagent）
    # 目前先用备用方案
    echo "🔍 使用默认日期判断..."
    TARGET_DATE=$(parse_date_fallback "$CONTENT")
fi

# 判断是否为补录
IS_BACKDATE=false
if [ "$TARGET_DATE" != "$TODAY" ]; then
    IS_BACKDATE=true
fi

echo "📅 识别到日期: $TARGET_DATE (今天: $TODAY, 补录: $IS_BACKDATE)"

# 时间戳
if [ "$IS_BACKDATE" = true ]; then
    TIMESTAMP=$(date "+📅 %Y-%m-%d %H:%M 🔁补录")
else
    TIMESTAMP=$(date "+📅 %Y-%m-%d %H:%M")
fi

if [ -z "$CONTENT" ]; then
    echo "❌ 消息内容不能为空"
    exit 1
fi

# 检查是否为纯工作指令
is_work_content() {
    local content="$1"
    local emotion_keywords="觉得|感觉|累|烦|开心|有趣|抽象|无语|好玩|难受|爽|想|希望|花了|搞了|折腾"
    if echo "$content" | grep -qE "$emotion_keywords"; then
        return 1
    fi
    
    local work_keywords="帮我写代码|修改代码|部署服务|启动服务器|运行测试|git push|编译"
    if echo "$content" | grep -qE "$work_keywords"; then
        return 0
    fi
    return 1
}

# 检查是否为测试消息
is_test_or_ack() {
    local content="$1"
    if echo "$content" | grep -qE "^测试|^试一下|测试一下|测试测试"; then
        return 0
    fi
    if [ ${#content} -lt 4 ]; then
        return 0
    fi
    return 1
}

# 检查是否为系统消息
is_system_message() {
    local content="$1"
    local sys_keywords="设置记录|配置Notion|修改LifeLog|记录方式|修改偏好"
    if echo "$content" | grep -qE "$sys_keywords"; then
        return 0
    fi
    return 1
}

# 判断是否需要记录
if is_work_content "$CONTENT"; then
    echo "⏭️ 跳过工作内容: ${CONTENT:0:30}..."
    exit 0
fi

if is_system_message "$CONTENT"; then
    echo "⏭️ 跳过系统消息: ${CONTENT:0:30}..."
    exit 0
fi

if is_test_or_ack "$CONTENT"; then
    echo "⏭️ 跳过测试/确认消息: ${CONTENT:0:30}..."
    exit 0
fi

# 检查目标日期是否已有记录
echo "🔍 检查 $TARGET_DATE 是否有记录..."

RESPONSE=$(curl -s -X POST "https://api.notion.com/v1/databases/$DATABASE_ID/query" \
    -H "Authorization: Bearer $NOTION_KEY" \
    -H "Notion-Version: $API_VERSION" \
    -H "Content-Type: application/json" \
    -d "{\"filter\": { \"property\": \"日期\", \"title\": { \"equals\": \"$TARGET_DATE\" } }, \"page_size\": 1}")

COUNT=$(echo "$RESPONSE" | python3 -c "import sys,json; d=json.load(sys.stdin); print(len(d.get('results',[])))")

if [ "$COUNT" -gt 0 ]; then
    # 追加到现有记录
    PAGE_ID=$(echo "$RESPONSE" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['results'][0]['id'])")
    EXISTING=$(echo "$RESPONSE" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['results'][0]['properties'].get('原文',{}).get('rich_text',[{}])[0].get('plain_text',''))")
    
    NEW_CONTENT="${EXISTING}"$'\n'"${TIMESTAMP} ${CONTENT}"
    
    echo "📝 追加到现有记录 ${PAGE_ID:0:8}"
    echo "   原有: ${EXISTING:0:50}..."
    echo "   新增: ${CONTENT}"
    
    RESULT=$(curl -s -X PATCH "https://api.notion.com/v1/pages/$PAGE_ID" \
        -H "Authorization: Bearer $NOTION_KEY" \
        -H "Notion-Version: $API_VERSION" \
        -H "Content-Type: application/json" \
        -d "{
            \"properties\": {
                \"原文\": { \"rich_text\": [{ \"text\": { \"content\": \"$(echo "$NEW_CONTENT" | head -1000 | tr '\n' ' ' | sed 's/\"/\\\"/g')\" } }] }
            }
        }")
    
    if echo "$RESULT" | python3 -c "import sys,json; d=json.load(sys.stdin); print('OK' if d.get('object')=='page' else 'FAIL')" 2>/dev/null | grep -q "OK"; then
        echo "NOTION_OK"
    else
        echo "NOTION_FAIL: $RESULT"
    fi
else
    # 创建新记录
    FORMATTED="${TIMESTAMP} ${CONTENT}"
    
    echo "🆕 创建新记录"
    echo "   内容: ${FORMATTED}"
    
    RESULT=$(curl -s -X POST "https://api.notion.com/v1/pages" \
        -H "Authorization: Bearer $NOTION_KEY" \
        -H "Notion-Version: $API_VERSION" \
        -H "Content-Type: application/json" \
        -d "{
            \"parent\": { \"database_id\": \"$DATABASE_ID\" },
            \"properties\": {
                \"日期\": { \"title\": [{ \"text\": { \"content\": \"$TARGET_DATE\" } }] },
                \"原文\": { \"rich_text\": [{ \"text\": { \"content\": \"$FORMATTED\" } }] }
            }
        }")
    
    if echo "$RESULT" | python3 -c "import sys,json; d=json.load(sys.stdin); print('OK' if d.get('object')=='page' else 'FAIL')" 2>/dev/null | grep -q "OK"; then
        echo "NOTION_OK"
    else
        echo "NOTION_FAIL"
    fi
fi
