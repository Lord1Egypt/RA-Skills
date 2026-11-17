#!/usr/bin/env bash
# ============================================================
# 话袋笔记 Skill · 搜索笔记
# 用法:
#   ./search.sh "关键词" [page] [size]
#   ./search.sh "早起看书" 1 10
#
# 依赖:
#   - curl
#   - 环境变量 HUADAI_API_KEY
# ============================================================
set -euo pipefail

BASE_URL="${HUADAI_BASE_URL:-https://openapi.ihuadai.cn/open/api/v1}"
API_KEY="${HUADAI_API_KEY:-}"

# --- 参数解析 ---
QUERY="${1:-}"
PAGE="${2:-1}"
SIZE="${3:-10}"

if [ -z "$QUERY" ]; then
  echo '{"error":"缺少搜索关键词。用法: ./search.sh \"关键词\" [page] [size]"}'
  exit 1
fi

if [ -z "$API_KEY" ]; then
  echo '{"error":"未配置 HUADAI_API_KEY 环境变量。请先在话袋开放平台 https://ihuadai.cn/desktop/openai 创建 API Key"}'
  exit 1
fi

# --- 调用 API ---
RESP=$(curl -sS -w '\n%{http_code}' \
  -G "$BASE_URL/search" \
  --data-urlencode "query=$QUERY" \
  --data-urlencode "page=$PAGE" \
  --data-urlencode "size=$SIZE" \
  -H "Authorization: $API_KEY" \
  -H "Content-Type: application/json" 2>&1)

HTTP_CODE=$(echo "$RESP" | tail -1)
BODY=$(echo "$RESP" | sed '$d')

if [ "$HTTP_CODE" != "200" ]; then
  echo "{\"error\":\"搜索失败，HTTP $HTTP_CODE\",\"response\":$BODY}"
  exit 1
fi

# --- 输出格式化 ---
echo "$BODY" | python3 -c '
import json, sys
try:
    data = json.load(sys.stdin)
except:
    print(sys.stdin.read())
    sys.exit(0)

if data.get("code") == 400001:
    print("❌ API Key 无效，请重新创建或配置。")
    print("   打开 https://ihuadai.cn/desktop/openai 创建 Key")
    sys.exit(1)

if data.get("code") != 200:
    msg = data.get("message","未知错误")
    print(f"❌ 搜索失败: {msg}")
    sys.exit(1)

result = data.get("data", {})
total = result.get("total", 0)
items = result.get("data", [])

if total == 0 or not items:
    print("未找到相关笔记。")
    sys.exit(0)

print(f"找到 {total} 条相关笔记：")
print()
for i, item in enumerate(items, 1):
    uid   = item.get("unique_id", "")
    ctype = item.get("type", "")
    ctime = item.get("create_time", "")
    ts    = ""
    if ctime:
        import datetime
        ts = datetime.datetime.fromtimestamp(int(ctime)).strftime("%Y-%m-%d %H:%M")

    # Quill Delta → 纯文本摘要
    content = item.get("content", [])
    text = ""
    if isinstance(content, list):
        for op in content:
            if isinstance(op, dict):
                t = op.get("insert", "")
                if isinstance(t, str):
                    text += t
    elif isinstance(content, str):
        text = content

    summary = text[:120].replace("\n"," ").strip()
    print(f"  [{i}] {summary}")
    print(f"      ID: {uid}")
    if ts:
        print(f"      时间: {ts}")
    if len(text) > 120:
        print(f"      （内容较长，共 {len(text)} 字符）")
    print()

print("提示：如需查看笔记完整内容，启用更新，请使用 unique_id。")
' 2>&1 || echo "$BODY"
