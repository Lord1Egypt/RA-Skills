#!/usr/bin/env bash
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Obsidian Inbox Pipeline — 每日自动流水线参考实现
#
# 用法：
#   OBSIDIAN_VAULT_PATH=/path/to/vault \
#   TELEGRAM_BOT_TOKEN=xxx TELEGRAM_CHAT_ID=xxx \
#   ./daily_pipeline.sh "ai-radar" "AI 资讯雷达" "AI" "🤖" "AI 日报"
#
# 前置依赖：
#   - python3
#   - obsidian-cli（可选，用于 print-default）
#   - 目标 radar 技能的 main.py（如 ~/.openclaw/workspace/skills/ai-radar/main.py）
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
set -eo

# ── 校验环境变量 ──────────────────────────────────────
if [[ -z "${OBSIDIAN_VAULT_PATH:-}" ]]; then
  echo "❌ 缺少 OBSIDIAN_VAULT_PATH"
  exit 1
fi

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/.."
RADAR_TYPE="${1:?用法: $0 <radar_type> <name> <category> <emoji> <source>}"
RADAR_NAME="${2:?}"
CATEGORY="${3:?}"
EMOJI="${4:?}"
SOURCE="${5:?}"

TODAY="$(date '+%Y-%m-%d')"
TMP="/tmp/radar_${RADAR_TYPE}.md"

# ── Step 1：生成日报 ──────────────────────────────────
RADAR_MAIN="$SKILL_DIR/../${RADAR_TYPE}/main.py"
if [[ -f "$RADAR_MAIN" ]]; then
  python3 "$RADAR_MAIN" > "$TMP"
else
  echo "⚠️  未找到 $RADAR_MAIN，跳过生成步骤"
  exit 0
fi

# ── Step 2：写入 Obsidian inbox ──────────────────────
# 模板：用 capture.py 写入（结构化版本）
# 如 radar 提供了独立格式脚本，优先用其写入结构化 Obsidian 文件
FORMAT_SCRIPT="$SKILL_DIR/../${RADAR_TYPE}/format_push.py"
if [[ -f "$FORMAT_SCRIPT" ]]; then
  python3 "$FORMAT_SCRIPT" \
    "$RADAR_TYPE" "$RADAR_NAME" "$SOURCE" "$CATEGORY" "$EMOJI" "$TODAY" \
    > /dev/null 2>&1
  OBSIDIAN_PATH="$(python3 -c "
import sys
for line in open('$TMP'):
    if line.startswith('OBSIDIAN|'):
        print(line.split('|',1)[1].strip())
")"
else
  # fallback：用 capture.py 写入
  CONTENT="$(cat "$TMP")"
  python3 "$SKILL_DIR/capture.py" \
    --type daily-report \
    --title "$EMOJI $RADAR_NAME · $TODAY" \
    --source "$SOURCE" \
    --tags "[$CATEGORY, 日报, 知识沉淀]" \
    --category "${CATEGORY,,}" \
    --content "$CONTENT"
fi

# ── Step 3：（可选）推送 Telegram ─────────────────────
if [[ -n "${TELEGRAM_BOT_TOKEN:-}" && -n "${TELEGRAM_CHAT_ID:-}" ]]; then
  PUSH_FILE="/tmp/radar_push_${RADAR_TYPE}.txt"
  python3 - "$PUSH_FILE" << 'PYEOF'
import sys, json, urllib.request, urllib.parse

push_file = sys.argv[1]
with open(push_file) as f:
    text = f.read()

token = os.environ.get("TELEGRAM_BOT_TOKEN")
chat_id = os.environ.get("TELEGRAM_CHAT_ID")

# MarkdownV2 escape
for ch in ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']:
    text = text.replace(ch, '\\' + ch)

data = json.dumps({
    "chat_id": chat_id,
    "text": text,
    "parse_mode": "MarkdownV2"
}).encode()

req = urllib.request.Request(
    f"https://api.telegram.org/bot{token}/sendMessage",
    data=data,
    headers={"Content-Type": "application/json"}
)
urllib.request.urlopen(req, timeout=15)
print("✅ Telegram 推送成功")
PYEOF
fi

# ── Step 4：（可选）推送飞书 ──────────────────────────
if [[ -n "${FEISHU_APP_ID:-}" && -n "${FEISHU_APP_SECRET:-}" ]]; then
  python3 - "$RADAR_TYPE" << 'PYEOF'
import sys, json, urllib.request, ssl

radar_type = sys.argv[1]
ctx = ssl.create_default_context()
app_id = os.environ.get("FEISHU_APP_ID")
app_secret = os.environ.get("FEISHU_APP_SECRET")
receive_id = os.environ.get("FEISHU_RECEIVE_ID", "")

# get token
data = json.dumps({"app_id": app_id, "app_secret": app_secret}).encode()
req = urllib.request.Request(
    "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
    data=data, headers={"Content-Type": "application/json"}
)
resp = json.loads(urllib.request.urlopen(req, timeout=15, context=ctx).read())
token = resp.get("tenant_access_token", "")

# read push file
push_file = f"/tmp/radar_push_{radar_type}.txt"
with open(push_file) as f:
    content = f.read()

# send
payload = json.dumps({
    "receive_id": receive_id or os.environ.get("FEISHU_RECEIVE_ID", ""),
    "receive_id_type": "open_id",
    "msg_type": "text",
    "content": json.dumps({"text": content})
}).encode()
req2 = urllib.request.Request(
    "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id",
    data=payload,
    headers={"Content-Type": "application/json", "Authorization": "Bearer " + token}
)
resp2 = json.loads(urllib.request.urlopen(req2, timeout=15, context=ctx).read())
print("✅ 飞书推送成功" if resp2.get("code") == 0 else f"❌ 飞书错误: {resp2.get('msg')}")
PYEOF
fi

# ── Step 5：（可选）重建索引 ──────────────────────────
if command -v node &> /dev/null; then
  REBUILD_SCRIPT="${OBSIDIAN_VAULT_PATH}/scripts/rebuild_index.mjs"
  if [[ -f "$REBUILD_SCRIPT" ]]; then
    node "$REBUILD_SCRIPT" 2>/dev/null && echo "✅ 索引已重建"
  fi
fi

echo "✅ $RADAR_NAME 流水线完成"
rm -f "$TMP"
