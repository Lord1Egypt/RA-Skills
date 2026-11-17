#!/bin/sh
# webhook 通知器示例：把 stdin 正文作为 JSON {"text": ...} POST 到 $WEBHOOK_URL。
#
# 依赖：curl + python3（仅用于安全 JSON 转义，无第三方依赖）。
# 成功：curl 返回 0 且 stdout 输出 "SENT"。
# 在 config.yaml 中把本 notifier 的 env.WEBHOOK_URL 换成你的真实 webhook 地址即可。
set -eu

WEBHOOK_URL="${WEBHOOK_URL:-}"
if [ -z "$WEBHOOK_URL" ]; then
  echo "ERROR: WEBHOOK_URL 未配置" >&2
  exit 1
fi

MSG="$(cat)"
PAYLOAD="$(printf '%s' "$MSG" | python3 -c 'import json,sys; print(json.dumps({"text": sys.stdin.read()}, ensure_ascii=False))')"

curl -fsS --max-time "${TIMEOUT:-60}" \
  -H 'Content-Type: application/json' \
  --data "$PAYLOAD" "$WEBHOOK_URL" >/dev/null

echo "SENT"
