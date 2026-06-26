#!/bin/bash

# 爱奇艺影视搜索脚本 v2
# 使用方法: bash search_v2.sh "搜索关键词"

set -e

KEYWORD="$1"

if [ -z "$KEYWORD" ]; then
    echo '{"error": "请提供搜索关键词", "usage": "bash search.sh \"搜索关键词\"", "results": []}'
    exit 1
fi

# URL编码搜索词
ENCODED_KEYWORD=$(printf '%s' "$KEYWORD" | python3 -c "import sys,urllib.parse; print(urllib.parse.quote(sys.stdin.read().strip()))")

# 爱奇艺搜索URL
SEARCH_URL="https://so.iqiyi.com/so/q_${ENCODED_KEYWORD}"

echo "正在搜索爱奇艺: $KEYWORD" >&2

# 创建临时目录
TEMP_DIR=$(mktemp -d)
trap "rm -rf $TEMP_DIR" EXIT

# 使用agent-browser打开页面并等待加载
agent-browser open "$SEARCH_URL" --timeout 30000 2>/dev/null || {
    echo '{"error": "无法打开页面", "results": []}'
    exit 1
}

# 等待页面加载完成
sleep 3

# 获取页面完整HTML
agent-browser eval "document.documentElement.outerHTML" > "$TEMP_DIR/page.html" 2>/dev/null || {
    echo '{"error": "无法获取页面内容", "results": []}'
    agent-browser close 2>/dev/null
    exit 1
}

# 关闭浏览器
agent-browser close 2>/dev/null

# 解析结果
python3 ~/.openclaw/workspace/skills/iqiyi-search/scripts/parse_iqiyi.py "$TEMP_DIR/page.html" "$KEYWORD"
