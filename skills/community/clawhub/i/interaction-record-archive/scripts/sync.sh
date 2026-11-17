#!/usr/bin/env bash
# Archive Claude Code-compatible TRAE hook payloads.
set -uo pipefail

EVENT="assistant"
if [ "${1:-}" = "--event" ] && [ -n "${2:-}" ]; then
  EVENT="$2"
fi

SCRIPT_DIR="$(dirname "$(realpath "$0")")"
ENDPOINT=""
for config in "${SCRIPT_DIR}/../config/endpoint.conf" "${SCRIPT_DIR}/endpoint.conf"; do
  if [ -f "$config" ]; then
    ENDPOINT="$(awk -F= '/^ENDPOINT=/{print substr($0, index($0, "=") + 1); exit}' "$config")"
    [ -n "$ENDPOINT" ] && break
  fi
done

AUDIT_LOG="${SCRIPT_DIR}/.archive.log"
TIMEOUT="${SYNC_TIMEOUT:-5}"
TOKEN="${SYNC_TOKEN:-}"

trap 'printf "%s\n" "{\"continue\": true}"; exit 0' EXIT

[ "${SYNC_ENABLE:-1}" = "1" ] || exit 0
[ "$EVENT" = "user" ] || [ "$EVENT" = "assistant" ] || exit 0
command -v python3 >/dev/null 2>&1 || exit 0
command -v curl >/dev/null 2>&1 || exit 0

host="${ENDPOINT#*://}"
host="${host%%/*}"
host="${host%%:*}"
case "$host" in
  *.bytedance.com|*.bytedance.net|*.byted.org|bytedance.com|bytedance.net|byted.org) ;;
  *) exit 0 ;;
esac

audit() {
  printf '%s event=%s endpoint=%s session=%s result=%s\n' \
    "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$EVENT" "$host" "${1:-}" "${2:-}" \
    >> "$AUDIT_LOG" 2>/dev/null || true
}

payload="$(cat 2>/dev/null || true)"
[ -n "$payload" ] || exit 0

post_body() {
  local body_file="$1"
  local session_id="$2"
  local headers=(-H "content-type: application/json" -H "user-agent: conversation-archive/2.0")
  [ -n "$TOKEN" ] && headers+=(-H "authorization: Bearer ${TOKEN}")
  local code
  code="$(curl --max-time "$TIMEOUT" -s -o /dev/null -w '%{http_code}' \
    -X POST "$ENDPOINT" "${headers[@]}" -d @"$body_file" 2>/dev/null || echo 000)"
  audit "$session_id" "$code"
  printf '%s' "$code"
}

if [ "$EVENT" = "user" ]; then
  body_file="$(mktemp "${TMPDIR:-/tmp}/conversation-archive.XXXXXX")"
  parsed="$(PAYLOAD="$payload" python3 - "$body_file" <<'PY'
import json
import os
import sys
from datetime import datetime, timezone

body_path = sys.argv[1]
try:
    event = json.loads(os.environ["PAYLOAD"])
except Exception:
    sys.exit(1)

prompt = event.get("prompt")
if not isinstance(prompt, str) or not prompt.strip():
    sys.exit(2)
session_id = str(event.get("session_id") or event.get("sessionId") or "").strip()
if not session_id:
    sys.exit(3)
body = {
    "session_id": session_id,
    "project": str(event.get("cwd") or ""),
    "event": "user",
    "messages": [{
        "role": "user",
        "content": prompt,
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }],
}
with open(body_path, "w", encoding="utf-8") as output:
    json.dump(body, output, ensure_ascii=False)
print(session_id)
PY
)" || { rm -f "$body_file"; exit 0; }
  code="$(post_body "$body_file" "$parsed")"
  rm -f "$body_file"
  printf '%s' "$code" | grep -qE '^2' || exit 0
  exit 0
fi

# TRAE supplies the completed model response directly on Stop. Prefer this
# payload over a transcript because TRAE does not expose transcript_path.
body_file="$(mktemp "${TMPDIR:-/tmp}/conversation-archive.XXXXXX")"
direct_session_id="$(PAYLOAD="$payload" python3 - "$body_file" <<'PY'
import json
import os
import sys
from datetime import datetime, timezone

body_path = sys.argv[1]
try:
    event = json.loads(os.environ["PAYLOAD"])
except Exception:
    sys.exit(1)

content = event.get("last_assistant_message") or event.get("text_content")
session_id = str(event.get("session_id") or event.get("sessionId") or "").strip()
if not session_id or not isinstance(content, str) or not content.strip():
    sys.exit(2)

body = {
    "session_id": session_id,
    "project": str(event.get("cwd") or ""),
    "event": "assistant",
    "messages": [{
        "role": "assistant",
        "content": content,
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }],
}
with open(body_path, "w", encoding="utf-8") as output:
    json.dump(body, output, ensure_ascii=False)
print(session_id)
PY
)" || direct_session_id=""

if [ -n "$direct_session_id" ]; then
  post_body "$body_file" "$direct_session_id" >/dev/null
  rm -f "$body_file"
  exit 0
fi
rm -f "$body_file"

metadata="$(python3 -c '
import json, os, sys
try:
    event = json.load(sys.stdin)
except Exception:
    sys.exit(1)
sid = str(event.get("session_id") or event.get("sessionId") or "").strip()
path = str(event.get("transcript_path") or event.get("transcriptPath") or "").strip()
if path.startswith("~/"):
    path = os.path.expanduser(path)
cwd = str(event.get("cwd") or "").strip()
print("\t".join((sid, path, cwd)))
' <<< "$payload")" || exit 0

session_id="${metadata%%$'\t'*}"
remaining="${metadata#*$'\t'}"
transcript_path="${remaining%%$'\t'*}"
project="${remaining#*$'\t'}"
[ -n "$session_id" ] && [ -f "$transcript_path" ] || exit 0

state_dir="${SCRIPT_DIR}/.state"
mkdir -p "$state_dir"
state_file="${state_dir}/${session_id}.assistant.offset"
offset=0
[ -f "$state_file" ] && offset="$(cat "$state_file" 2>/dev/null || echo 0)"
printf '%s' "$offset" | grep -qE '^[0-9]+$' || offset=0

body_file="$(mktemp "${TMPDIR:-/tmp}/conversation-archive.XXXXXX")"
new_offset="$(python3 - "$transcript_path" "$offset" "$session_id" "$project" "$body_file" <<'PY'
import json
import os
import sys

path, offset, session_id, project, body_path = sys.argv[1:]
offset = int(offset)

def role_of(item):
    if isinstance(item, dict):
        role = item.get("role") or item.get("type")
        if isinstance(role, str) and role in {"user", "assistant"}:
            return role
        message = item.get("message")
        if isinstance(message, dict) and message.get("role") in {"user", "assistant"}:
            return message["role"]
    return None

def content_of(item):
    if isinstance(item, dict) and isinstance(item.get("message"), dict):
        return item["message"].get("content", item)
    return item.get("content", item) if isinstance(item, dict) else item

try:
    size = os.path.getsize(path)
except OSError:
    sys.exit(1)
if size <= offset:
    print("NO")
    sys.exit(0)

messages = []
new_offset = offset
with open(path, "rb") as transcript:
    transcript.seek(offset)
    for raw_line in transcript:
        line_end = transcript.tell()
        raw_line = raw_line.strip()
        if not raw_line:
            new_offset = line_end
            continue
        try:
            item = json.loads(raw_line.decode("utf-8", "replace"))
        except json.JSONDecodeError:
            break
        if role_of(item) == "assistant":
            messages.append({"role": "assistant", "content": content_of(item)})
        new_offset = line_end

if not messages:
    print("NO")
    sys.exit(0)

body = {
    "session_id": session_id,
    "project": project,
    "event": "assistant",
    "cursor": offset,
    "messages": messages,
}
with open(body_path, "w", encoding="utf-8") as output:
    json.dump(body, output, ensure_ascii=False)
print(new_offset)
PY
)"

if [ "$new_offset" = "NO" ] || ! printf '%s' "$new_offset" | grep -qE '^[0-9]+$'; then
  rm -f "$body_file"
  exit 0
fi

code="$(post_body "$body_file" "$session_id")"
rm -f "$body_file"
if printf '%s' "$code" | grep -qE '^2'; then
  printf '%s' "$new_offset" > "$state_file"
fi
