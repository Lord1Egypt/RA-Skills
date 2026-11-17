#!/usr/bin/env bash

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=scripts/_lib.sh
source "$SCRIPT_DIR/_lib.sh"

if [ "$#" -lt 1 ]; then
  die "usage: $0 <mode:mw|zh> [text] [--messages-file FILE] [--max-tokens NUMBER]"
fi

MODE="$1"
shift

case "$MODE" in
  mw)
    SYSTEM_PROMPT="请只用纯传统蒙古文回答，不要包含任何中文汉字。"
    ;;
  zh)
    SYSTEM_PROMPT="请使用简体中文回答。若用户输入包含传统蒙古文，请先理解原文语义，再直接给出针对用户请求的中文回复正文。只输出最终中文回复正文；禁止添加问候、自我介绍、解释过程、标题、原文复述或无关补充。若用户明确要求翻译，请不要使用本模板，应改用 POST /translation/。"
    ;;
  *)
    die "mode must be 'mw' or 'zh'"
    ;;
esac

TEXT=""
MESSAGES_FILE=""
MAX_TOKENS=""

while [ "$#" -gt 0 ]; do
  case "$1" in
    --messages-file)
      [ "$#" -ge 2 ] || die "--messages-file requires a path"
      MESSAGES_FILE="$2"
      shift 2
      ;;
    --max-tokens)
      [ "$#" -ge 2 ] || die "--max-tokens requires a number"
      MAX_TOKENS="$2"
      shift 2
      ;;
    --)
      shift
      [ "$#" -gt 0 ] || die "text must follow --"
      TEXT="$*"
      break
      ;;
    -*)
      die "unknown option: $1"
      ;;
    *)
      [ -z "$TEXT" ] || die "text must be supplied as one quoted argument"
      TEXT="$1"
      shift
      ;;
  esac
done

[ -z "$TEXT" ] || [ -z "$MESSAGES_FILE" ] ||
  die "use either text or --messages-file, not both"

if [ -n "$MESSAGES_FILE" ]; then
  validate_file "$MESSAGES_FILE"
else
  if [ -z "$TEXT" ]; then
    TEXT=$(read_text_argument "$@")
  fi
  [ -n "$TEXT" ] || die "chat text must not be empty"
fi

require_commands curl python3

LAST_USER_LENGTH=$(python3 - "$TEXT" "$MESSAGES_FILE" <<'PY'
import json
import sys

text, path = sys.argv[1], sys.argv[2]
if path:
    with open(path, "r", encoding="utf-8") as handle:
        messages = json.load(handle)
    if not isinstance(messages, list) or not messages:
        raise SystemExit("history must be a non-empty JSON array")
    for message in messages:
        if not isinstance(message, dict):
            raise SystemExit("every history item must be an object")
        if message.get("role") not in {"user", "assistant"}:
            raise SystemExit("history roles must be user or assistant")
        if not isinstance(message.get("content"), str):
            raise SystemExit("history content must be a string")
    users = [message["content"] for message in messages if message["role"] == "user"]
    if not users or messages[-1]["role"] != "user":
        raise SystemExit("history must end with a user message")
    text = users[-1]
print(len(text))
PY
)

if [ -z "$MAX_TOKENS" ]; then
  if [ "$LAST_USER_LENGTH" -le 50 ]; then
    MAX_TOKENS=256
  elif [ "$LAST_USER_LENGTH" -le 200 ]; then
    MAX_TOKENS=768
  elif [ "$LAST_USER_LENGTH" -le 1000 ]; then
    MAX_TOKENS=3072
  else
    MAX_TOKENS=6144
  fi
fi

case "$MAX_TOKENS" in
  *[!0-9]*|'') die "--max-tokens must be an integer from 1 to 8192" ;;
esac
if [ "$MAX_TOKENS" -lt 1 ] || [ "$MAX_TOKENS" -gt 8192 ]; then
  die "--max-tokens must be an integer from 1 to 8192"
fi

load_key

HEADER_FILE=$(mktemp)
BODY_FILE=$(mktemp)
REQUEST_FILE=$(mktemp)
trap 'rm -f "$HEADER_FILE" "$BODY_FILE" "$REQUEST_FILE"' EXIT

python3 - "$SYSTEM_PROMPT" "$TEXT" "$MESSAGES_FILE" "$MAX_TOKENS" \
  > "$REQUEST_FILE" <<'PY'
import json
import sys

system_prompt, text, history_path, max_tokens = sys.argv[1:]
messages = [{"role": "system", "content": system_prompt}]
if history_path:
    with open(history_path, "r", encoding="utf-8") as handle:
        messages.extend(json.load(handle))
else:
    messages.append({"role": "user", "content": text})

print(json.dumps({
    "model": "gpt-5-mw",
    "messages": messages,
    "temperature": 0.5,
    "max_tokens": int(max_tokens),
}, ensure_ascii=False))
PY

perform_request POST "$HEADER_FILE" "$BODY_FILE" \
  "$BASE_URL/chat/completions/" \
  -H "Authorization: Bearer $KEY" \
  -H "Content-Type: application/json" \
  --max-time 60 \
  --data-binary "@$REQUEST_FILE"

RESULT=$(json_extract_first "$BODY_FILE" choices.0.message.content 2>/dev/null) ||
  die "the service response did not contain a chat result"

if [ "$MODE" = "mw" ] && python3 - "$RESULT" <<'PY'
import re
import sys
raise SystemExit(0 if re.search(r"[\u3400-\u4dbf\u4e00-\u9fff]", sys.argv[1]) else 1)
PY
then
  die "the service returned Han characters for a Traditional Mongolian-only request; retry only with user approval"
fi

if [ "$MODE" = "zh" ] && python3 - "$RESULT" <<'PY'
import re
import sys
raise SystemExit(0 if re.search(r"[\u1800-\u18af]", sys.argv[1]) else 1)
PY
then
  die "the service returned Traditional Mongolian for a Chinese-response request; retry only with user approval"
fi

printf '%s\n' "$RESULT"
emit_billing_summary "$HEADER_FILE" "$BODY_FILE"
