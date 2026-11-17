#!/usr/bin/env bash
# ============================================================
# 话袋笔记 Skill · 新建笔记
# 用法:
#   ./upload.sh "笔记内容（Markdown）" [unique_id]
#   ./upload.sh "## 会议纪要\n- 完成首页改版\n- 修复登录问题"
#
# 依赖:
#   - curl
#   - 环境变量 HUADAI_API_KEY
# ============================================================
set -euo pipefail

BASE_URL="${HUADAI_BASE_URL:-https://openapi.ihuadai.cn/open/api/v1}"
API_KEY="${HUADAI_API_KEY:-}"

# --- 参数解析 ---
CONTENT="${1:-}"
UNIQUE_ID="${2:-}"

if [ -z "$CONTENT" ]; then
  echo '{"error":"缺少笔记内容。用法: ./upload.sh \"笔记内容\" [unique_id]"}'
  exit 1
fi

if [ -z "$API_KEY" ]; then
  echo '{"error":"未配置 HUADAI_API_KEY 环境变量。请先在话袋开放平台 https://ihuadai.cn/desktop/openai 创建 API Key"}'
  exit 1
fi

# --- 生成 unique_id（如未提供） ---
if [ -z "$UNIQUE_ID" ]; then
  TS=$(date +%s)
  RAND_SUFFIX=$(python3 -c 'import random,string;print("".join(random.choices(string.ascii_lowercase+string.digits,k=8)))' 2>/dev/null || echo "$(date +%N)")
  UNIQUE_ID="b_${TS}_${RAND_SUFFIX}"
fi

CREATE_TIME=$(date +%s)
CONTENT_WITH_NEWLINE="${CONTENT}
"

# --- 调用 API ---
RESP=$(curl -sS -w '\n%{http_code}' \
  -X POST "$BASE_URL/block/upload-block" \
  -H "Authorization: $API_KEY" \
  -H "Content-Type: application/json" \
  -d "$(python3 -c '
import json, sys
print(json.dumps({
    "unique_id": "'"$UNIQUE_ID"'",
    "type": 1,
    "content": sys.argv[1] if len(sys.argv) > 1 else "",
    "create_time": '"$CREATE_TIME"',
    "status": 1,
    "is_collect": 0,
    "is_todo": 0
}))
' "$CONTENT_WITH_NEWLINE")" 2>&1)

HTTP_CODE=$(echo "$RESP" | tail -1)
BODY=$(echo "$RESP" | sed '$d')

if [ "$HTTP_CODE" != "200" ]; then
  echo "{\"error\":\"上传失败，HTTP $HTTP_CODE\",\"response\":$BODY}"
  exit 1
fi

# --- 输出 ---
echo "$BODY" | python3 -c '
import json, sys
data = json.load(sys.stdin)
code = data.get("code", -1)

if code == 200:
    print("✅ 笔记已保存。")
    print(f"   unique_id: '"$UNIQUE_ID"'")
elif code == 400001:
    print("❌ API Key 无效，请重新创建或配置。")
    print("   打开 https://ihuadai.cn/desktop/openai 创建 Key")
elif code == 400024:
    print("❌ 需要有效会员，请在话袋开通对应权益。")
else:
    msg = data.get("message", "未知错误")
    print(f"❌ 保存失败: {msg}")
' 2>&1
