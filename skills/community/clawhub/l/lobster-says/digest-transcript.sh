#!/bin/bash
# 虾说 — Transcript 消化脚本
#
# 数据访问声明：
#   - 本脚本读取 OpenClaw 的本地会话日志（~/.openclaw/agents/main/sessions/*.jsonl）
#   - 仅提取 user/assistant 角色的文本内容
#   - smart 模式：在本地消化为摘要后上传到 nixiashuo.com（不含原始对话）
#   - deep 模式：上传原始 transcript 条目到 nixiashuo.com
#   - lightweight 模式：不执行任何读取或上传
#   - 用户在初始化时选择理解模式并可随时切换
#   - 服务端地址：https://nixiashuo.com/api/transcript/digest

set -e

HOURS=6
MAX_ENTRIES=300
MODE=""
BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
CONFIG_FILE="${BASE_DIR}/.lobster-config"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m'

info()  { echo -e "${GREEN}[✓]${NC} $1"; }
warn()  { echo -e "${YELLOW}[!]${NC} $1"; }
error() { echo -e "${RED}[✗]${NC} $1"; exit 1; }
step()  { echo -e "${CYAN}──${NC} $1"; }

while [[ $# -gt 0 ]]; do
  case $1 in
    --hours) HOURS="$2"; shift 2 ;;
    --max-entries) MAX_ENTRIES="$2"; shift 2 ;;
    --mode) MODE="$2"; shift 2 ;;
    *) echo "未知参数: $1"; exit 1 ;;
  esac
done

for cmd in python3 curl; do
  command -v "$cmd" >/dev/null 2>&1 || error "$cmd 不可用"
done

[ -f "$CONFIG_FILE" ] || error ".lobster-config 不存在，请先完成虾的初始化"

USER_ID=$(python3 -c "import json; print(json.load(open('${CONFIG_FILE}'))['user_id'])" 2>/dev/null) || error "无法读取 user_id"
ACCESS_TOKEN=$(python3 -c "import json; print(json.load(open('${CONFIG_FILE}'))['access_token'])" 2>/dev/null) || error "无法读取 access_token"
if [ -z "$MODE" ]; then
  MODE=$(python3 -c "import json; print(json.load(open('${CONFIG_FILE}')).get('memory_mode','smart'))" 2>/dev/null) || MODE="smart"
fi
API_BASE=$(python3 -c "import json; print(json.load(open('${CONFIG_FILE}', encoding='utf-8')).get('api_base','https://nixiashuo.com'))" 2>/dev/null) || API_BASE="https://nixiashuo.com"

case "$MODE" in
  lightweight) info "轻量陪伴模式：不执行 transcript digest"; exit 0 ;;
  smart|deep) ;;
  *) error "mode 必须是 lightweight / smart / deep" ;;
esac

echo ""
echo "🧠 虾说 — Transcript 消化"
echo "  模式: ${MODE}"
echo "  回溯: ${HOURS} 小时"
echo "  最大条目: ${MAX_ENTRIES}"
echo ""

OPENCLAW_BASE="${HOME}/.openclaw"
SESSIONS_DIR="${OPENCLAW_BASE}/agents/main/sessions"
PROFILE=$(printenv OPENCLAW_PROFILE 2>/dev/null || echo "")
if [ -n "$PROFILE" ] && [ "$PROFILE" != "default" ]; then
  PROFILE_DIR="${OPENCLAW_BASE}/agents/main-${PROFILE}/sessions"
  [ -d "$PROFILE_DIR" ] && SESSIONS_DIR="$PROFILE_DIR"
fi
[ -d "$SESSIONS_DIR" ] || { warn "Session 目录不存在，跳过本次消化。"; exit 0; }

PAYLOAD_FILE=$(mktemp /tmp/lobster-digest-XXXXXX.json)
SMART_PAYLOAD_FILE=$(mktemp /tmp/lobster-digest-smart-XXXXXX.json)
DIGEST_TEXT_FILE=""
cleanup() {
  rm -f "$PAYLOAD_FILE" "$SMART_PAYLOAD_FILE"
  if [ -n "$DIGEST_TEXT_FILE" ]; then
    rm -f "$DIGEST_TEXT_FILE"
  fi
}
trap cleanup EXIT

python3 <<PY
import json
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

sessions_dir = "${SESSIONS_DIR}"
hours = int("${HOURS}")
max_entries = int("${MAX_ENTRIES}")
user_id = "${USER_ID}"
cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
APP_TZ = timezone(timedelta(hours=8))
APP_TZ_LABEL = "Asia/Shanghai"

def extract_message_text(raw_content):
    if isinstance(raw_content, str):
        return raw_content.strip()
    texts = []
    def _collect(part):
        if isinstance(part, str):
            text = part.strip()
            if text:
                texts.append(text)
        elif isinstance(part, dict):
            if part.get("type", "") in ("text", "input_text", "output_text"):
                text = (part.get("text") or "").strip()
                if text:
                    texts.append(text)
    if isinstance(raw_content, list):
        for part in raw_content:
            _collect(part)
    elif isinstance(raw_content, dict):
        _collect(raw_content)
    return "\n".join(texts).strip()

def strip_bridge_metadata(text):
    cleaned = (text or "").strip()
    if not cleaned:
        return ""
    fence = re.escape(chr(96) * 3)
    patterns = [
        rf"^Conversation info \(untrusted metadata\):\s*{fence}json\n.*?{fence}\s*",
        rf"^Sender \(untrusted metadata\):\s*{fence}json\n.*?{fence}\s*",
    ]
    for pattern in patterns:
        cleaned = re.sub(pattern, "", cleaned, flags=re.S)
    return cleaned.strip()

signal_tags = {
    "late_night_count": 0,
    "early_morning_count": 0,
    "weekend_active_count": 0,
    "total_user_messages": 0,
    "time_range_hours": hours,
    "timezone": APP_TZ_LABEL,
}

entries = []
source_session_ids = []
time_range_start = None
time_range_end = None
jsonl_files = sorted(Path(sessions_dir).glob("*.jsonl"), key=lambda f: f.stat().st_mtime, reverse=True)

for jsonl_path in jsonl_files:
    mtime = datetime.fromtimestamp(jsonl_path.stat().st_mtime, tz=timezone.utc)
    if mtime < cutoff:
        break
    session_entries = []
    session_has_real_user = False
    try:
        with open(jsonl_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    record = json.loads(line)
                except Exception:
                    continue
                ts_str = record.get("timestamp", record.get("ts", ""))
                if not ts_str:
                    continue
                ts = None
                for fmt in ("%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S%z"):
                    try:
                        ts = datetime.strptime(ts_str, fmt)
                        if ts.tzinfo is None:
                            ts = ts.replace(tzinfo=timezone.utc)
                        break
                    except ValueError:
                        continue
                if ts is None:
                    ts = mtime
                if ts < cutoff:
                    continue
                message_obj = record.get("message") if isinstance(record.get("message"), dict) else None
                if message_obj:
                    role = message_obj.get("role", "")
                    content = extract_message_text(message_obj.get("content"))
                else:
                    role = record.get("role", "")
                    content = extract_message_text(record.get("content", record.get("message", "")))
                if role not in ("user", "human", "assistant"):
                    continue
                content = strip_bridge_metadata(content)
                if not content:
                    continue
                normalized_role = "user" if role in ("user", "human") else "assistant"
                if normalized_role == "user" and (content.startswith("[cron:") or content.startswith("[hook:") or content.startswith("[automation:")):
                    continue
                if normalized_role == "user":
                    session_has_real_user = True
                    signal_tags["total_user_messages"] += 1
                    local_hour = (ts.hour + 8) % 24
                    if 0 <= local_hour < 5:
                        signal_tags["late_night_count"] += 1
                    elif 5 <= local_hour < 7:
                        signal_tags["early_morning_count"] += 1
                    if (ts + timedelta(hours=8)).weekday() >= 5:
                        signal_tags["weekend_active_count"] += 1
                entry_local_ts = ts.astimezone(APP_TZ)
                session_entries.append({
                    "timestamp": f"{entry_local_ts.strftime('%Y-%m-%d %H:%M')} {APP_TZ_LABEL}",
                    "role": normalized_role,
                    "content": content[:5000],
                })
                if time_range_start is None or ts < time_range_start:
                    time_range_start = ts
                if time_range_end is None or ts > time_range_end:
                    time_range_end = ts
    except Exception:
        continue
    if session_entries and session_has_real_user:
        source_session_ids.append(jsonl_path.stem)
        for entry in session_entries:
            if len(entries) < max_entries:
                entries.append(entry)

entries.sort(key=lambda e: e["timestamp"])
payload = {
    "user_id": user_id,
    "entries": entries,
    "signal_tags": signal_tags,
    "source_type": "skill_cron",
    "source_session_ids": source_session_ids,
    "source_sessions": len(source_session_ids),
}
if time_range_start:
    payload["time_range_start"] = time_range_start.strftime("%Y-%m-%dT%H:%M:%S")
if time_range_end:
    payload["time_range_end"] = time_range_end.strftime("%Y-%m-%dT%H:%M:%S")
with open("${PAYLOAD_FILE}", "w", encoding="utf-8") as f:
    json.dump(payload, f, ensure_ascii=False)
print(len(entries))
PY

ENTRY_COUNT=$(python3 -c "import json; print(len(json.load(open('${PAYLOAD_FILE}')).get('entries', [])))" 2>/dev/null) || ENTRY_COUNT=0
[ "$ENTRY_COUNT" -gt 0 ] || { info "过去 ${HOURS} 小时没有新的 transcript 记录，跳过消化。"; exit 0; }

if [ "$MODE" = "smart" ]; then
  step "智能陪伴：本地消化后上传摘要"
  command -v openclaw >/dev/null 2>&1 || { warn "openclaw 不可用，无法本地消化，跳过本次 digest。"; exit 0; }
  SUMMARY_TEXT=$(python3 - <<PY
import json
with open("${PAYLOAD_FILE}", "r", encoding="utf-8") as f:
    payload = json.load(f)
entries = payload.get("entries", [])
signal = payload.get("signal_tags", {})
user_msgs = [e["content"] for e in entries if e.get("role") == "user"][-12:]
parts = []
parts.append("请根据以下用户最近对话，生成 400-1200 字的结构化摘要。")
parts.append("要求：聚焦近期状态、情绪、节奏、项目压力、生活线索；不要引用逐字原话；不要编造。")
parts.append("")
parts.append("近期用户发言摘录：")
for msg in user_msgs:
    parts.append(f"- {msg}")
parts.append("")
parts.append(f"统计信号: {json.dumps(signal, ensure_ascii=False)}")
print("\n".join(parts))
PY
)
  DIGEST_TEXT=$(openclaw run --message "$SUMMARY_TEXT" --session isolated --no-interactive 2>/dev/null | head -c 12000) || DIGEST_TEXT=""
  [ -n "$DIGEST_TEXT" ] || { warn "本地消化失败，跳过本次 digest。"; exit 0; }
  DIGEST_TEXT_FILE=$(mktemp /tmp/lobster-digest-text-XXXXXX.txt)
  printf "%s" "$DIGEST_TEXT" > "$DIGEST_TEXT_FILE"
  DIGEST_TEXT_PATH="$DIGEST_TEXT_FILE" python3 - <<PY
import json
import os
with open("${PAYLOAD_FILE}", "r", encoding="utf-8") as f:
    original = json.load(f)
with open(os.environ["DIGEST_TEXT_PATH"], "r", encoding="utf-8") as f:
    text = f.read()
tags = []
keywords = {
    "deadline": ["deadline", "截止", "上线", "提测", "发版", "ddl"],
    "mood-shift": ["情绪变化", "情绪波动", "焦虑", "烦躁"],
    "milestone": ["完成", "搞定", "里程碑", "上线成功"],
    "life-event": ["生日", "搬家", "旅行", "家人", "宠物"],
    "burnout-risk": ["疲惫", "累", "撑不住", "倦怠"],
    "late-night": ["凌晨", "深夜", "半夜"],
    "weekend-work": ["周末", "周六", "周日"],
}
lower = text.lower()
for tag, kws in keywords.items():
    if any(kw in lower for kw in kws):
        tags.append(tag)
payload = {
    "user_id": original["user_id"],
    "entries": [],
    "signal_tags": original.get("signal_tags", {}),
    "source_type": original.get("source_type", "skill_cron"),
    "source_session_ids": original.get("source_session_ids", []),
    "source_sessions": original.get("source_sessions", 0),
    "privacy_mode": True,
    "pre_digested_summary": text,
    "pre_digested_semantic_tags": tags,
}
for key in ("time_range_start", "time_range_end"):
    if original.get(key):
        payload[key] = original[key]
with open("${SMART_PAYLOAD_FILE}", "w", encoding="utf-8") as f:
    json.dump(payload, f, ensure_ascii=False)
PY
  RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "${API_BASE}/api/transcript/digest" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer ${ACCESS_TOKEN}" \
    -d @"${SMART_PAYLOAD_FILE}")
else
  step "深度陪伴：上传原始 transcript 进行消化"
  RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "${API_BASE}/api/transcript/digest" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer ${ACCESS_TOKEN}" \
    -d @"${PAYLOAD_FILE}")
fi

HTTP_CODE=$(echo "$RESPONSE" | tail -1)
BODY=$(echo "$RESPONSE" | sed '$d')
if [ "$HTTP_CODE" = "200" ]; then
  DIGEST_ID=$(echo "$BODY" | python3 -c "import sys,json; print(json.load(sys.stdin).get('digest_id','?'))" 2>/dev/null) || DIGEST_ID="?"
  SUMMARY_LEN=$(echo "$BODY" | python3 -c "import sys,json; print(len(json.load(sys.stdin).get('digest_summary','')))" 2>/dev/null) || SUMMARY_LEN="?"
  info "Transcript 消化成功：digest_id=${DIGEST_ID}, 摘要长度=${SUMMARY_LEN}"
elif [ "$HTTP_CODE" = "429" ]; then
  warn "Server 限流（429），稍后再试。"
else
  error "Server 返回 HTTP ${HTTP_CODE}: ${BODY}"
fi
