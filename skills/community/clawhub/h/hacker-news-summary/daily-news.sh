#!/bin/bash

# ============================================================
# Hacker News 每日新闻汇总 + 百度翻译 + 飞书推送
# 使用前请设置以下环境变量：
#   BAIDU_APPID      - 百度翻译 API 的 App ID
#   BAIDU_SECRET     - 百度翻译 API 的密钥
#   FEISHU_WEBHOOK   - 飞书自定义机器人的 Webhook URL（可选，不设置则不推送）
# ============================================================

# 检查必要环境变量
if [ -z "$BAIDU_APPID" ] || [ -z "$BAIDU_SECRET" ]; then
    echo "错误：请设置环境变量 BAIDU_APPID 和 BAIDU_SECRET"
    exit 1
fi

# 翻译函数（使用百度翻译 API）
translate() {
    local text="$1"
    local salt=$(date +%s)
    local sign=$(echo -n "$BAIDU_APPID$text$salt$BAIDU_SECRET" | md5sum | cut -d ' ' -f1)
    local encoded_text=$(echo -n "$text" | jq -sRr @uri)
    local result=$(curl -s "https://fanyi-api.baidu.com/api/trans/vip/translate?q=$encoded_text&from=en&to=zh&appid=$BAIDU_APPID&salt=$salt&sign=$sign")
    echo "$result" | jq -r '.trans_result[0].dst // ""'
}

# 配置
OUTPUT="$HOME/daily-news.md"
DATE=$(date '+%Y-%m-%d')
TMPFILE=$(mktemp)

# 获取前10条新闻ID
curl -s https://hacker-news.firebaseio.com/v0/topstories.json | jq -r '.[0:10][]' > "$TMPFILE"

# 生成 Markdown 文件
echo "# 每日新闻汇总 - $DATE" > "$OUTPUT"
echo "" >> "$OUTPUT"
echo "## Hacker News 前 10 条新闻（英中双语）" >> "$OUTPUT"
echo "" >> "$OUTPUT"

COUNT=0
while read ID; do
    COUNT=$((COUNT+1))
    ITEM=$(curl -s "https://hacker-news.firebaseio.com/v0/item/$ID.json")
    TITLE_EN=$(echo "$ITEM" | jq -r '.title')
    URL=$(echo "$ITEM" | jq -r '.url')
    [ "$URL" = "null" ] && URL="https://news.ycombinator.com/item?id=$ID"

    ZH_TITLE=$(translate "$TITLE_EN")

    echo "**$COUNT. $TITLE_EN**" >> "$OUTPUT"
    if [ -n "$ZH_TITLE" ] && [ "$ZH_TITLE" != "null" ]; then
        echo "   - 中文: $ZH_TITLE" >> "$OUTPUT"
    fi
    echo "   - 链接: $URL" >> "$OUTPUT"
    echo "" >> "$OUTPUT"

    sleep 1   # 百度免费版 QPS=1
done < "$TMPFILE"

rm "$TMPFILE"
echo "✅ 共抓取 $COUNT 条真实新闻" >> "$OUTPUT"

# 飞书推送（可选）
if [ -n "$FEISHU_WEBHOOK" ]; then
    NEWS_CONTENT=$(head -c 3000 "$OUTPUT")
    MESSAGE=$(jq -n --arg content "$NEWS_CONTENT" '{"msg_type":"text","content":{"text":$content}}')
    curl -X POST -H "Content-Type: application/json" -d "$MESSAGE" "$FEISHU_WEBHOOK" > /dev/null 2>&1
    echo "✅ 已推送到飞书"
fi

echo "新闻汇总已完成！文件位置：$OUTPUT"
