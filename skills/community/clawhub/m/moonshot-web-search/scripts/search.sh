#!/bin/bash
set -euo pipefail

API_KEY="${MOONSHOT_API_KEY:-}"
QUERY="$*"

if [ -z "$API_KEY" ]; then
  echo "请设置 MOONSHOT_API_KEY 环境变量" >&2
  exit 1
fi

if [ -z "$QUERY" ]; then
  echo "Usage: $0 <query>"
  exit 1
fi

API_URL="https://api.moonshot.cn/v1/chat/completions"

# 第一轮：触发搜索
ROUND1=$(curl -fsS "$API_URL" \
  -H "Authorization: Bearer $API_KEY" \
  -H 'Content-Type: application/json' \
  -d "$(python3 - "$QUERY" <<'PY'
import json
import sys

print(json.dumps({
    'model': 'moonshot-v1-128k',
    'messages': [{'role': 'user', 'content': sys.argv[1]}],
    'tools': [{'type': 'builtin_function', 'function': {'name': '$web_search'}}],
    'tool_choice': 'auto',
}))
PY
)")

ROUND1_INFO=$(echo "$ROUND1" | python3 -c "
import json, sys

try:
    data = json.load(sys.stdin)
except json.JSONDecodeError as exc:
    print(f'第一轮响应不是合法 JSON: {exc}', file=sys.stderr)
    sys.exit(1)

if data.get('error'):
    print(f\"第一轮 API 错误: {data['error']}\", file=sys.stderr)
    sys.exit(1)

choices = data.get('choices') or []
message = choices[0].get('message') if choices else None
tool_calls = (message or {}).get('tool_calls') or []

if not tool_calls:
    content = (message or {}).get('content') or ''
    finish_reason = choices[0].get('finish_reason') if choices else None
    print('第一轮未返回 tool_calls。', file=sys.stderr)
    if finish_reason is not None:
        print(f'finish_reason: {finish_reason}', file=sys.stderr)
    if content:
        print(content, file=sys.stderr)
    sys.exit(1)

tool_call = tool_calls[0]
print(tool_call['id'])
print(tool_call['function']['arguments'])
")

TOOL_CALL_ID=$(printf '%s\n' "$ROUND1_INFO" | sed -n '1p')
TOOL_ARGS=$(printf '%s\n' "$ROUND1_INFO" | sed -n '2p')

# 第二轮：把搜索结果喂回去
ROUND2=$(curl -fsS "$API_URL" \
  -H "Authorization: Bearer $API_KEY" \
  -H 'Content-Type: application/json' \
  -d "$(python3 - "$QUERY" "$TOOL_CALL_ID" "$TOOL_ARGS" <<'PY'
import json
import sys

query, tool_call_id, tool_args = sys.argv[1], sys.argv[2], sys.argv[3]
payload = {
    'model': 'moonshot-v1-128k',
    'messages': [
        {'role': 'user', 'content': query},
        {'role': 'assistant', 'content': '', 'tool_calls': [{'id': tool_call_id, 'type': 'builtin_function', 'function': {'name': '$web_search', 'arguments': tool_args}}]},
        {'role': 'tool', 'tool_call_id': tool_call_id, 'content': tool_args},
    ],
    'tools': [{'type': 'builtin_function', 'function': {'name': '$web_search'}}],
}
print(json.dumps(payload))
PY
)")

echo "$ROUND2" | python3 -c "
import json, sys

try:
    data = json.load(sys.stdin)
except json.JSONDecodeError as exc:
    print(f'第二轮响应不是合法 JSON: {exc}', file=sys.stderr)
    sys.exit(1)

if data.get('error'):
    print(f\"第二轮 API 错误: {data['error']}\", file=sys.stderr)
    sys.exit(1)

choices = data.get('choices') or []
message = choices[0].get('message') if choices else None
content = (message or {}).get('content')

if not content:
    finish_reason = choices[0].get('finish_reason') if choices else None
    print('第二轮未返回可展示的内容。', file=sys.stderr)
    if finish_reason is not None:
        print(f'finish_reason: {finish_reason}', file=sys.stderr)
    sys.exit(1)

print(content)
"
