#!/usr/bin/env bash
# ============================================================
# 话袋笔记 Skill · 更新笔记
# 用法:
#   ./update.sh <unique_id> "新内容（Markdown）"
#   ./update.sh b_1730000000_a1b2c3d4 "## 更新后的内容"
#
# 注意:
#   - unique_id 必须来自搜索结果或用户明确提供
#   - content 应为更新后的完整内容，非增量追加
#
# 依赖:
#   - curl
#   - 环境变量 HUADAI_API_KEY
# ============================================================
set -euo pipefail

BASE_URL="${HUADAI_BASE_URL:-https://openapi.ihuadai.cn/open/api/v1}"
API_KEY="${HUADAI_API_KEY:-}"

# --- 参数解析 ---
UNIQUE_ID="${1:-}"
CONTENT="${2:-}"

if [ -z "$UNIQUE_ID" ]; then
  echo '{"error":"缺少 unique_id。用法: ./update.sh <unique_id> \"新内容\""}'
  echo '提示：unique_id 可通过 ./search.sh 获取。'
  exit 1
fi

if [ -z "$CONTENT" ]; then
  echo '{"error":"缺少更新内容。用法: ./update.sh <unique_id> \"新内容\""}'
  exit 1
fi

if [ -z "$API_KEY" ]; then
  echo '{"error":"未配置 HUADAI_API_KEY 环境变量。请先在话袋开放平台 https://ihuadai.cn/desktop/openai 创建 API Key"}'
  exit 1
fi

CONTENT_WITH_NEWLINE="${CONTENT}
"

# --- 调用 API ---
RESP=$(curl -sS -w '\n%{http_code}' \
  -X POST "$BASE_URL/block/update-block" \
  -H "Authorization: $API_KEY" \
  -H "Content-Type: application/json" \
  -d "$(python3 -c '
import json, sys
print(json.dumps({
    "unique_id": "'"$UNIQUE_ID"'",
    "type": 1,
    "content": sys.argv[1] if len(sys.argv) > 1 else "",
    "status": 1,
    "is_collect": 0,
    "is_todo": 0
}))
' "$CONTENT_WITH_NEWLINE")" 2>&1)

HTTP_CODE=$(echo "$RESP" | tail -1)
BODY=$(echo "$RESP" | sed '$d')

if [ "$HTTP_CODE" != "200" ]; then
  echo "{\"error\":\"更新失败，HTTP $HTTP_CODE\",\"response\":$BODY}"
  exit 1
fi

# --- 输出 ---
echo "$BODY" | python3 -c '
import json, sys
data = json.load(sys.stdin)
code = data.get("code", -1)

if code == 200:
    print("✅ 笔记已更新。")
    print(f"   unique_id: '"$UNIQUE_ID"'")
elif code == 400001:
    print("❌ API Key 无效，请重新创建或配置。")
    print("   打开 https://ihuadai.cn/desktop/openai 创建 Key")
elif code == 400018:
    print("❌ 笔记不存在。请先用 search.sh 确认目标笔记。")
elif code == 400024:
    print("❌ 需要有效会员，请在话袋开通对应权益。")
else:
    msg = data.get("message", "未知错误")
    print(f"❌ 更新失败: {msg}")
' 2>&1
