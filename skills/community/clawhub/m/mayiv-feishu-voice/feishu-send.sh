#!/usr/bin/env bash
# feishu-send.sh — Send text + voice simultaneously to Feishu
# Usage: feishu-send.sh "<text>" "<voice_summary>" [receive_id]
#
# Both text and voice are MANDATORY. No exceptions.
# 环境变量：
#   FEISHU_APP_ID       — 飞书 App ID（必填）
#   FEISHU_APP_SECRET  — 飞书 App Secret（必填）
#   FEISHU_RECEIVE_ID  — 接收者 open_id（可选）
#   FEISHU_CHAT_ID     — 群聊 ID（oc_ 开头，可选）

TEXT="$1"
VOICE="$2"

if [ -z "$TEXT" ] || [ -z "$VOICE" ]; then
    echo "Usage: feishu-send.sh <text> <voice_summary> [receive_id]" >&2
    exit 1
fi

# receive_id：参数3 > FEISHU_RECEIVE_ID > FEISHU_CHAT_ID
if [ -n "$3" ]; then
    RECEIVE_ID="$3"
elif [ -n "$FEISHU_RECEIVE_ID" ]; then
    RECEIVE_ID="$FEISHU_RECEIVE_ID"
elif [ -n "$FEISHU_CHAT_ID" ]; then
    RECEIVE_ID="$FEISHU_CHAT_ID"
else
    echo "ERROR: 需要传入 receive_id，或设置 FEISHU_RECEIVE_ID / FEISHU_CHAT_ID 环境变量" >&2
    exit 1
fi

# 凭证校验
if [ -z "$FEISHU_APP_ID" ] || [ -z "$FEISHU_APP_SECRET" ]; then
    echo "ERROR: 需要设置 FEISHU_APP_ID 和 FEISHU_APP_SECRET 环境变量" >&2
    exit 1
fi

# Get token
TOKEN=$(curl -sf -X POST 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal' \
    -H 'Content-Type: application/json' \
    -d "{\"app_id\":\"$FEISHU_APP_ID\",\"app_secret\":\"$FEISHU_APP_SECRET\"}" \
    | python3 -c "import sys,json; print(json.load(sys.stdin)['tenant_access_token'])")

# Send text — 用环境变量传参，零转义问题
FEISHU_TEXT="$TEXT" FEISHU_RID="$RECEIVE_ID" FEISHU_TOKEN="$TOKEN" \
python3 -c "
import json, urllib.request, os

text = os.environ['FEISHU_TEXT'].replace('\\n', '\n').replace('\\r', '\r')
payload = {
    'receive_id': os.environ['FEISHU_RID'],
    'msg_type': 'text',
    'content': json.dumps({'text': text})
}
body = json.dumps(payload).encode()
req = urllib.request.Request(
    'https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id',
    data=body,
    headers={'Authorization': 'Bearer ' + os.environ['FEISHU_TOKEN'], 'Content-Type': 'application/json'}
)
result = json.loads(urllib.request.urlopen(req).read())
code = result.get('code', -1)
mid = result.get('data', {}).get('message_id', '')
print(f'TEXT_OK mid={mid}' if code == 0 else f'TEXT_ERR code={code} msg={result.get(\"msg\")}')
"

# Send voice — 传 receive_id 保证语音发到同一接收者
bash "$(dirname "$0")/feishu-voice-send.sh" "$VOICE" "$RECEIVE_ID"
