#!/bin/bash

# 每日科技新闻推送脚本
# 获取机器之心最新新闻 → 发送到飞书 → 保存到Get笔记

# 检查环境变量
if [ -z "$JI_ZHIXIN_TOKEN" ]; then
    echo "❌ 错误：未配置 JI_ZHIXIN_TOKEN"
    exit 1
fi

if [ -z "$GETNOTE_API_KEY" ]; then
    echo "❌ 错误：未配置 GETNOTE_API_KEY"
    exit 1
fi

if [ -z "$GETNOTE_CLIENT_ID" ]; then
    echo "❌ 错误：未配置 GETNOTE_CLIENT_ID"
    exit 1
fi

if [ -z "$FEISHU_TARGET" ]; then
    echo "❌ 错误：未配置 FEISHU_TARGET"
    exit 1
fi

RSS_URL="https://mcp.applications.jiqizhixin.com/rss?token=$JI_ZHIXIN_TOKEN"

echo "📡 正在获取机器之心新闻..."
RSS_CONTENT=$(curl -s --max-time 30 "$RSS_URL")

if [ $? -ne 0 ]; then
    echo "❌ 获取RSS失败"
    exit 1
fi

# 提取标题和链接（取前10条，跳过前2个网站标题）
TITLES=$(echo "$RSS_CONTENT" | grep -oP '(?<=<title>)[^<]+(?=</title>)' | tail -n +3 | head -10)
LINKS=$(echo "$RSS_CONTENT" | grep -oP '(?<=<link>)[^<]+(?=</link>)' | tail -n +3 | head -10)

# 组装消息内容
CONTENT=""
count=1
while IFS= read -r title && IFS= read -r link <&3; do
    CONTENT="${CONTENT}${count}. ${title}\n${link}\n\n"
    count=$((count + 1))
done <<< "$TITLES" 3<<< "$LINKS"

DATETIME=$(date '+%Y-%m-%d %H:%M')
FULL_CONTENT="📰 机器之心每日科技热榜\n\n${CONTENT}---\n📅 ${DATETIME}"

# 1. 发送到飞书
echo "📨 正在发送到飞书..."
openclaw message send --channel feishu --target "$FEISHU_TARGET" --message "$FULL_CONTENT" 2>/dev/null

if [ $? -eq 0 ]; then
    echo "✅ 飞书消息发送成功"
else
    echo "⚠️ 飞书消息发送失败"
fi

# 2. 保存到Get笔记
echo "📝 正在保存到Get笔记..."

NOTE_JSON=$(cat <<JSON
{
  "title": "机器之心 ${DATETIME} 热榜",
  "content": "${FULL_CONTENT}",
  "note_type": "plain_text",
  "tags": ["机器之心", "科技新闻", "每日热榜"]
}
JSON
)

RESPONSE=$(curl -s --max-time 30 -X POST "https://openapi.biji.com/open/api/v1/resource/note/save" \
  -H "Authorization: $GETNOTE_API_KEY" \
  -H "X-Client-ID: $GETNOTE_CLIENT_ID" \
  -H "Content-Type: application/json" \
  -d "$NOTE_JSON")

if echo "$RESPONSE" | grep -q "success"; then
    echo "✅ 笔记保存成功"
else
    echo "⚠️ 笔记保存失败: $RESPONSE"
fi

echo "🎉 任务完成！"
