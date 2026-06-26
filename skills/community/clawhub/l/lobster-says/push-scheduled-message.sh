#!/bin/bash
# ═══════════════════════════════════════════════
#  虾说 — 运行时定时推送脚本
# ═══════════════════════════════════════════════
#
#  数据访问声明：
#  - 读取 .lobster-config（技能自身配置，含 user_id/access_token/通道偏好）
#  - 调用 openclaw sessions --json 获取最近活跃 IM 通道元数据（通道名+ID）
#  - 通用 IM 通道使用 openclaw message send 发送消息（多通道 fallback）
#  - 企业微信定时推送主链路走 --emit-message-text：脚本只输出最终消息文本，由 cron isolated agent 使用 message 工具私聊直达
#  - --generate-only JSON 模式保留为调试/兼容能力，不再作为企微 cron 主链路
#  - 与 https://nixiashuo.com 通信：生成消息、报告送达结果
#  - 不读取 openclaw.json 配置文件，不提取 gateway token
#
#  设计目标：
#  1. --emit-message-text 模式：仅输出最终消息文本到 stdout，不执行任何发送
#     适用于：企业微信 cron 链路——由 isolated agent 直接把 stdout 原文作为 message 工具参数发送
#  2. --generate-only 模式：输出 JSON 到 stdout，保留为调试/兼容能力
#  3. 完整模式（默认）：生成消息 + 多通道 fallback 发送
#     适用于：Telegram/Discord/飞书等通用 IM 通道
#  4. 各模式共享消息生成、init-ready 管理、送达报告等基础设施
#
#  使用方式：
#    bash push-scheduled-message.sh --slot morning|discovery|evening
#    bash push-scheduled-message.sh --slot morning --emit-message-text
#    bash push-scheduled-message.sh --slot morning --generate-only

set -u

BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
CONFIG_FILE="${BASE_DIR}/.lobster-config"
COMMON_SCRIPT="${BASE_DIR}/runtime-common.sh"
SETUP_CRON_SCRIPT="${BASE_DIR}/setup-cron.sh"
LOG_DIR="${BASE_DIR}/logs"
RUN_TS="$(date +%Y%m%d-%H%M%S)"
LOG_FILE="${LOG_DIR}/push-scheduled-message-${RUN_TS}.log"
SLOT=""
FORCED_CHANNEL=""
FORCED_TARGET=""
EXTRA_CONTEXT=""
CONTENT_PREFIX=""
MANAGED_JOB_NAME=""
JOB_KIND="scheduled-message"
GENERATE_ONLY=0
EMIT_MESSAGE_TEXT=0
ACTIVE_WINDOW_MINUTES="${ACTIVE_WINDOW_MINUTES:-10080}"
INIT_READY_MAX_ATTEMPTS="${INIT_READY_MAX_ATTEMPTS:-4}"
INIT_READY_RETRY_MINUTES="${INIT_READY_RETRY_MINUTES:-15}"
# Telegram 原生 Bot API 可稳定处理 sendPhoto/URL 图片；
# 企业微信/飞书等机器人协议对图片通常要求 webhook 特定 payload 或上传素材，
# 统一经 OpenClaw CLI 时更适合优先走文本 + 链接，避免假成功或媒体协议不兼容。
MEDIA_SEND_CHANNELS="telegram discord googlechat slack mattermost signal imessage msteams"
GENERATE_RESPONSE_FILE=""
PARSED_JSON_FILE=""
_SEND_STDERR_FILE=""

cleanup() {
  [ -n "$GENERATE_RESPONSE_FILE" ] && [ -f "$GENERATE_RESPONSE_FILE" ] && rm -f "$GENERATE_RESPONSE_FILE"
  [ -n "$PARSED_JSON_FILE" ] && [ -f "$PARSED_JSON_FILE" ] && rm -f "$PARSED_JSON_FILE"
  [ -n "$_SEND_STDERR_FILE" ] && [ -f "$_SEND_STDERR_FILE" ] && rm -f "$_SEND_STDERR_FILE"
  [ -n "${STICKER_IMAGE_FILE:-}" ] && [ -f "${STICKER_IMAGE_FILE:-}" ] && rm -f "$STICKER_IMAGE_FILE"
}

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m'

_ts()   { date '+%Y-%m-%d %H:%M:%S'; }
# --emit-message-text / --generate-only 模式下，info/warn/error/step 输出到 stderr，stdout 保留给消息文本或 JSON
info()  { echo -e "${GREEN}[✓]${NC} $(_ts) $1" >&2; }
warn()  { echo -e "${YELLOW}[!]${NC} $(_ts) $1" >&2; }
error() { echo -e "${RED}[✗]${NC} $(_ts) $1" >&2; exit 1; }
CURRENT_STEP="启动"
step()  { CURRENT_STEP="$1"; echo -e "${CYAN}──${NC} $(_ts) $1" >&2; }

if [ ! -f "$COMMON_SCRIPT" ]; then
  echo "共享运行时脚本不存在：${COMMON_SCRIPT}" >&2
  exit 1
fi
. "$COMMON_SCRIPT"

mkdir -p "$LOG_DIR"
# 日志始终写文件；tee 只用于非 generate-only 模式的 stderr
exec 3>>"$LOG_FILE"

echo "[log] push-scheduled-message started at $(date '+%F %T')" >&3
echo "[log] file: ${LOG_FILE}" >&3

after_exit() {
  local exit_code=$?
  cleanup
  if [ "$exit_code" -ne 0 ]; then
    echo "" >&3
    echo "[log] push-scheduled-message failed at step: ${CURRENT_STEP} (exit=${exit_code})" >&3
    echo "[log] inspect: ${LOG_FILE}" >&3
  else
    echo "[log] push-scheduled-message finished successfully" >&3
  fi
  exec 3>&-
}
trap after_exit EXIT

while [[ $# -gt 0 ]]; do
  case "$1" in
    --slot) SLOT="$2"; shift 2 ;;
    --channel) FORCED_CHANNEL="$2"; shift 2 ;;
    --to|--target) FORCED_TARGET="$2"; shift 2 ;;
    --extra-context) EXTRA_CONTEXT="$2"; shift 2 ;;
    --content-prefix) CONTENT_PREFIX="$2"; shift 2 ;;
    --job-kind) JOB_KIND="$2"; shift 2 ;;
    --managed-job-name|--remove-cron-job-name) MANAGED_JOB_NAME="$2"; shift 2 ;;
    --generate-only) GENERATE_ONLY=1; shift ;;
    --emit-message-text) EMIT_MESSAGE_TEXT=1; shift ;;
    *) echo "未知参数: $1" >&2; exit 1 ;;
  esac
done

if [[ ! "$SLOT" =~ ^(morning|discovery|evening|event|sticker|wallpaper)$ ]]; then
  error "--slot 必须是 morning / discovery / evening / event / sticker / wallpaper"
fi

for cmd in python3 curl openclaw; do
  if ! command -v "$cmd" >/dev/null 2>&1; then
    error "$cmd 不可用"
  fi
done

if [ ! -f "$CONFIG_FILE" ]; then
  error ".lobster-config 不存在，请先初始化虾"
fi

read_config_value() {
  local key="$1"
  local default_value="${2:-}"
  CONFIG_PATH="$CONFIG_FILE" KEY_NAME="$key" DEFAULT_VALUE="$default_value" python3 - <<'PY'
import json
import os
from pathlib import Path
path = Path(os.environ["CONFIG_PATH"])
key = os.environ["KEY_NAME"]
default = os.environ.get("DEFAULT_VALUE", "")
try:
    data = json.loads(path.read_text(encoding='utf-8'))
    value = data.get(key, default)
    print(value if value is not None else default)
except Exception:
    print(default)
PY
}

supports_media() {
  local channel="$1"
  for ch in $MEDIA_SEND_CHANNELS; do
    if [ "$ch" = "$channel" ]; then
      return 0
    fi
  done
  return 1
}

build_candidate_lines() {
  local sessions_json="$1"
  local forced_channel="$2"
  local forced_target="$3"
  build_candidate_lines_with_policy "$CONFIG_FILE" "$sessions_json" "$forced_channel" "$forced_target"
}

load_runtime_policy() {
  POLICY_JSON=$(lobster_runtime_policy_json "$CONFIG_FILE")
  POLICY_JSON_VALUE="$POLICY_JSON" python3 <<'PY'
import json
import os
policy = json.loads(os.environ["POLICY_JSON_VALUE"])
print(policy.get("binding_channel", ""))
print(policy.get("binding_target", ""))
print(policy.get("binding_mode", "prefer"))
print("1" if policy.get("strict_binding") else "0")
print(policy.get("outbound_adapter", "openclaw"))
print(policy.get("outbound_webhook_url", ""))
print(policy.get("outbound_webhook_secret", ""))
print(policy.get("delivery_channel", ""))
print(policy.get("delivery_target", ""))
print("1" if policy.get("delivery_ready") else "0")
print(policy.get("delivery_reason", ""))
print(policy.get("cron_status", "unregistered"))
PY
}

sync_known_channels_after_send() {
  local current_channel="$1"
  local current_target="$2"
  local candidate_lines="$3"
  local delivered_at="$4"
  update_config_after_send_with_policy "$CONFIG_FILE" "$current_channel" "$current_target" "$candidate_lines" "$delivered_at"
}

append_delivery_ledger() {
  local stage="$1"
  local status="$2"
  local detail="${3:-}"
  local channel="${4:-}"
  local target="${5:-}"
  local delivery_mode="${6:-}"
  local message_id="${7:-}"
  mkdir -p "$LOG_DIR"
  LOG_DIR_VALUE="$LOG_DIR" \
  LEDGER_STAGE="$stage" \
  LEDGER_STATUS="$status" \
  LEDGER_DETAIL="$detail" \
  LEDGER_CHANNEL="$channel" \
  LEDGER_TARGET="$target" \
  LEDGER_MODE="$delivery_mode" \
  LEDGER_MESSAGE_ID="$message_id" \
  LEDGER_SLOT="$SLOT" \
  LEDGER_JOB_KIND="$JOB_KIND" \
  LEDGER_RUN_TS="$RUN_TS" \
  python3 <<'PY'
import json
import os
from datetime import datetime, timezone
from pathlib import Path

message_id_raw = (os.environ.get("LEDGER_MESSAGE_ID") or "").strip()
try:
    message_id = int(message_id_raw) if message_id_raw else None
except ValueError:
    message_id = None

entry = {
    "ts": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
    "run_ts": os.environ.get("LEDGER_RUN_TS"),
    "script": "push-scheduled-message.sh",
    "slot": os.environ.get("LEDGER_SLOT"),
    "job_kind": os.environ.get("LEDGER_JOB_KIND"),
    "stage": os.environ.get("LEDGER_STAGE"),
    "status": os.environ.get("LEDGER_STATUS"),
    "detail": os.environ.get("LEDGER_DETAIL") or None,
    "channel": os.environ.get("LEDGER_CHANNEL") or None,
    "target": os.environ.get("LEDGER_TARGET") or None,
    "delivery_mode": os.environ.get("LEDGER_MODE") or None,
    "message_id": message_id,
}
ledger_path = Path(os.environ["LOG_DIR_VALUE"]) / "delivery-ledger.jsonl"
with ledger_path.open("a", encoding="utf-8") as fh:
    fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
PY
}

update_init_ready_state() {
  [ "$JOB_KIND" = "init-ready" ] || return 0
  local state="$1"
  local attempt_count="${2:-}"
  local message_id="${3:-}"
  local error_message="${4:-}"
  local channel="${5:-}"
  local target="${6:-}"
  local extra_field="${7:-}"
  local extra_value="${8:-}"
  INIT_STATE="$state" \
  INIT_ATTEMPT_COUNT="$attempt_count" \
  INIT_MESSAGE_ID="$message_id" \
  INIT_ERROR="$error_message" \
  INIT_CHANNEL="$channel" \
  INIT_TARGET="$target" \
  INIT_EXTRA_FIELD="$extra_field" \
  INIT_EXTRA_VALUE="$extra_value" \
  CONFIG_PATH="$CONFIG_FILE" \
  python3 <<'PY'
import json
import os
from datetime import datetime, timezone
from pathlib import Path

config_path = Path(os.environ["CONFIG_PATH"])
try:
    config = json.loads(config_path.read_text(encoding="utf-8"))
except Exception:
    config = {}

init_ready = config.get("init_ready") if isinstance(config.get("init_ready"), dict) else {}
now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
state = os.environ.get("INIT_STATE") or init_ready.get("state") or "unknown"
init_ready["state"] = state
init_ready["updated_at"] = now
if state in {"attempting", "delivery_failed", "retry_scheduled", "scheduled"}:
    init_ready["last_attempt_at"] = now
attempt_count = (os.environ.get("INIT_ATTEMPT_COUNT") or "").strip()
if attempt_count:
    try:
        init_ready["attempts"] = int(attempt_count)
    except ValueError:
        pass
message_id = (os.environ.get("INIT_MESSAGE_ID") or "").strip()
if message_id:
    try:
        init_ready["last_message_id"] = int(message_id)
    except ValueError:
        pass
error_message = (os.environ.get("INIT_ERROR") or "").strip()
if error_message:
    init_ready["last_error"] = error_message
channel = (os.environ.get("INIT_CHANNEL") or "").strip()
target = (os.environ.get("INIT_TARGET") or "").strip()
if channel:
    init_ready["last_delivery_channel"] = channel
if target:
    init_ready["last_delivery_target"] = target
if state == "sent":
    init_ready["sent_at"] = now
extra_field = (os.environ.get("INIT_EXTRA_FIELD") or "").strip()
extra_value = (os.environ.get("INIT_EXTRA_VALUE") or "").strip()
if extra_field:
    init_ready[extra_field] = extra_value
config["init_ready"] = init_ready
config_path.write_text(json.dumps(config, indent=2, ensure_ascii=False), encoding="utf-8")
PY
}

begin_init_ready_attempt() {
  [ "$JOB_KIND" = "init-ready" ] || { echo "0"; return 0; }
  CONFIG_PATH="$CONFIG_FILE" python3 <<'PY'
import json
import os
from datetime import datetime, timezone
from pathlib import Path

config_path = Path(os.environ["CONFIG_PATH"])
try:
    config = json.loads(config_path.read_text(encoding="utf-8"))
except Exception:
    config = {}
init_ready = config.get("init_ready") if isinstance(config.get("init_ready"), dict) else {}
attempts = int(init_ready.get("attempts") or 0) + 1
now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
init_ready["attempts"] = attempts
init_ready["state"] = "attempting"
init_ready["last_attempt_at"] = now
init_ready["updated_at"] = now
config["init_ready"] = init_ready
config_path.write_text(json.dumps(config, indent=2, ensure_ascii=False), encoding="utf-8")
print(attempts)
PY
}

init_ready_already_sent() {
  [ "$JOB_KIND" = "init-ready" ] || return 1
  CONFIG_PATH="$CONFIG_FILE" python3 <<'PY'
import json
import os
from pathlib import Path

config_path = Path(os.environ["CONFIG_PATH"])
try:
    config = json.loads(config_path.read_text(encoding="utf-8"))
except Exception:
    config = {}
state = ""
if isinstance(config.get("init_ready"), dict):
    state = str(config["init_ready"].get("state") or "")
print("yes" if state == "sent" else "no")
PY
}

finalize_managed_job() {
  [ -n "$MANAGED_JOB_NAME" ] || return 0
  [ -f "$SETUP_CRON_SCRIPT" ] || return 0
  bash "$SETUP_CRON_SCRIPT" --remove-job-by-name "$MANAGED_JOB_NAME" >/dev/null 2>&1 || true
}

schedule_init_ready_retry() {
  local attempt_count="$1"
  local reason="$2"
  [ "$JOB_KIND" = "init-ready" ] || return 0
  if [ "$attempt_count" -ge "$INIT_READY_MAX_ATTEMPTS" ]; then
    warn "init-ready 已达到最大尝试次数 ${INIT_READY_MAX_ATTEMPTS}，停止自动重试"
    update_init_ready_state "failed" "$attempt_count" "" "$reason"
    append_delivery_ledger "retry_exhausted" "failed" "$reason"
    finalize_managed_job
    return 0
  fi

  if bash "$SETUP_CRON_SCRIPT" --schedule-init-ready-delay "$INIT_READY_RETRY_MINUTES" >/dev/null 2>&1; then
    update_init_ready_state "retry_scheduled" "$attempt_count" "" "$reason" "" "" "retry_delay_minutes" "$INIT_READY_RETRY_MINUTES"
    append_delivery_ledger "retry_scheduled" "scheduled" "$reason"
    info "init-ready 已重排，${INIT_READY_RETRY_MINUTES} 分钟后重试"
  else
    warn "init-ready 重排失败，请稍后手动执行 setup-cron.sh"
    update_init_ready_state "delivery_failed" "$attempt_count" "" "$reason"
    append_delivery_ledger "retry_schedule_failed" "failed" "$reason"
  fi
}

report_delivery() {
  local message_id="$1"
  local status="$2"
  local channel="$3"
  local target="$4"
  local delivery_mode="$5"
  local delivered_text="$6"
  local screenshot_url="$7"
  local error_message="$8"

  REPORT_RESULT=$(REPORT_USER_ID="$USER_ID" REPORT_MESSAGE_ID="$message_id" REPORT_STATUS="$status" REPORT_CHANNEL="$channel" REPORT_TARGET="$target" REPORT_MODE="$delivery_mode" REPORT_TEXT="$delivered_text" REPORT_SCREENSHOT_URL="$screenshot_url" REPORT_ERROR="$error_message" python3 <<'PY'
import json
import os
payload = {
    "user_id": os.environ["REPORT_USER_ID"],
    "message_id": int(os.environ["REPORT_MESSAGE_ID"]),
    "status": os.environ["REPORT_STATUS"],
    "channel": os.environ.get("REPORT_CHANNEL") or None,
    "target": os.environ.get("REPORT_TARGET") or None,
    "delivery_mode": os.environ.get("REPORT_MODE") or None,
    "delivered_text": os.environ.get("REPORT_TEXT") or None,
    "delivered_screenshot_url": os.environ.get("REPORT_SCREENSHOT_URL") or None,
    "error_message": os.environ.get("REPORT_ERROR") or None,
}
print(json.dumps(payload, ensure_ascii=False))
PY
)

  curl -fsS -X POST "${API_BASE}/api/delivery/report" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer ${ACCESS_TOKEN}" \
    -d "$REPORT_RESULT" >/dev/null 2>&1 || warn "送达结果回写失败（不影响用户已收到的消息）"
}

build_text_message() {
  local include_url="$1"
  LOBSTER_NAME_VALUE="$LOBSTER_NAME" GENERATED_CONTENT_VALUE="$GENERATED_CONTENT" WEB_URL_VALUE="$WEB_URL" SCREENSHOT_URL_VALUE="$SCREENSHOT_URL" INCLUDE_URL_VALUE="$include_url" python3 <<'PY'
import os
lobster_name = os.environ["LOBSTER_NAME_VALUE"]
content = os.environ["GENERATED_CONTENT_VALUE"]
web_url = os.environ["WEB_URL_VALUE"]
screenshot_url = os.environ["SCREENSHOT_URL_VALUE"]
include_url = os.environ.get("INCLUDE_URL_VALUE") == "true"
lines = [f"🦞 {lobster_name}说：「{content}」", ""]
if include_url and screenshot_url:
    lines.append(f"📸 {lobster_name}的工作室截图：{screenshot_url}")
lines.append(f"👀 看看{lobster_name}在干嘛 → {web_url}")
print("\n".join(lines))
PY
}

# ═══════════════════════════════════════════════
#  读取配置
# ═══════════════════════════════════════════════
USER_ID=$(read_config_value "user_id")
ACCESS_TOKEN=$(read_config_value "access_token")
LOBSTER_NAME=$(read_config_value "lobster_name" "虾")
API_BASE=$(read_config_value "api_base" "https://nixiashuo.com")
WEB_BASE=$(read_config_value "web_base" "$API_BASE")
WECOM_USER_ID=$(read_config_value "wecom_user_id")

if [ -z "$USER_ID" ] || [ -z "$ACCESS_TOKEN" ]; then
  error ".lobster-config 缺少 user_id 或 access_token"
fi

mapfile -t POLICY_LINES < <(load_runtime_policy)
BOUND_CHANNEL="${POLICY_LINES[0]:-}"
BOUND_TARGET="${POLICY_LINES[1]:-}"
BINDING_MODE="${POLICY_LINES[2]:-prefer}"
STRICT_BINDING="${POLICY_LINES[3]:-0}"
OUTBOUND_ADAPTER="${POLICY_LINES[4]:-openclaw}"
OUTBOUND_WEBHOOK_URL="${POLICY_LINES[5]:-}"
OUTBOUND_WEBHOOK_SECRET="${POLICY_LINES[6]:-}"
DELIVERY_CHANNEL="${POLICY_LINES[7]:-}"
DELIVERY_TARGET="${POLICY_LINES[8]:-}"
DELIVERY_READY="${POLICY_LINES[9]:-0}"
DELIVERY_REASON="${POLICY_LINES[10]:-}"
CRON_STATUS="${POLICY_LINES[11]:-unregistered}"

if [ "$STRICT_BINDING" = "1" ]; then
  OUTBOUND_ADAPTER="wecom-direct-message"
  DELIVERY_CHANNEL="wecom"
  if [ -n "$WECOM_USER_ID" ]; then
    DELIVERY_TARGET="$WECOM_USER_ID"
    DELIVERY_READY="1"
    DELIVERY_REASON=""
  else
    DELIVERY_TARGET=""
    DELIVERY_READY="0"
    DELIVERY_REASON="企业微信定时推送缺少 sender_id / wecom_user_id；请在技能层从 inbound metadata 传入 sender_id"
  fi
fi

# ═══════════════════════════════════════════════
#  init-ready 前置检查
# ═══════════════════════════════════════════════
if [ "$JOB_KIND" = "init-ready" ] && [ "$(init_ready_already_sent)" = "yes" ]; then
  info "init-ready 已经送达过，本次跳过重复执行"
  append_delivery_ledger "duplicate_skip" "skipped" "init-ready already sent"
  finalize_managed_job
  exit 0
fi

INIT_READY_ATTEMPT_NUMBER=0
if [ "$JOB_KIND" = "init-ready" ]; then
  INIT_READY_ATTEMPT_NUMBER=$(begin_init_ready_attempt)
  append_delivery_ledger "attempt_started" "running" "init-ready attempt=${INIT_READY_ATTEMPT_NUMBER}"
fi

if [ "$DELIVERY_READY" != "1" ]; then
  LAST_ERROR="${DELIVERY_REASON:-delivery contract not ready}"
  append_delivery_ledger "delivery_contract_not_ready" "failed" "$LAST_ERROR" "$DELIVERY_CHANNEL" "$DELIVERY_TARGET" "$OUTBOUND_ADAPTER"
  [ "$JOB_KIND" = "init-ready" ] && schedule_init_ready_retry "$INIT_READY_ATTEMPT_NUMBER" "$LAST_ERROR"
  error "$LAST_ERROR"
fi

# ═══════════════════════════════════════════════
#  生成消息
# ═══════════════════════════════════════════════
step "生成 ${SLOT} 消息..."
GENERATE_RESPONSE_FILE=$(mktemp "${TMPDIR:-/tmp}/lobster-generate-response.XXXXXX.json")
PARSED_JSON_FILE=$(mktemp "${TMPDIR:-/tmp}/lobster-generate-parsed.XXXXXX.json")
GENERATE_REQUEST_JSON=$(GENERATE_USER_ID="$USER_ID" GENERATE_SLOT="$SLOT" GENERATE_EXTRA_CONTEXT="$EXTRA_CONTEXT" python3 <<'PY'
import json
import os
payload = {
    "user_id": os.environ["GENERATE_USER_ID"],
    "message_type": os.environ["GENERATE_SLOT"],
    "include_screenshot_base64": False,
}
extra_context = (os.environ.get("GENERATE_EXTRA_CONTEXT") or "").strip()
if extra_context:
    payload["extra_context"] = extra_context
print(json.dumps(payload, ensure_ascii=False))
PY
)

if ! curl -fsS -X POST "${API_BASE}/api/generate" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -d "$GENERATE_REQUEST_JSON" \
  -o "$GENERATE_RESPONSE_FILE"; then
  LAST_ERROR="调用 /api/generate 失败"
  append_delivery_ledger "generate_failed" "failed" "$LAST_ERROR"
  [ "$JOB_KIND" = "init-ready" ] && schedule_init_ready_retry "$INIT_READY_ATTEMPT_NUMBER" "$LAST_ERROR"
  error "$LAST_ERROR"
fi

SKIPPED_CHECK=$(python3 - "$GENERATE_RESPONSE_FILE" <<'PY'
import json
import sys
from pathlib import Path
try:
    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    if data.get("skipped"):
        print(data.get("reason", "unknown"))
    else:
        print("no")
except Exception:
    print("no")
PY
)

if [ "$SKIPPED_CHECK" != "no" ]; then
  info "📋 本次 ${SLOT} 生成被跳过: ${SKIPPED_CHECK}"
  append_delivery_ledger "generate_skipped" "skipped" "$SKIPPED_CHECK"
  [ "$JOB_KIND" = "init-ready" ] && schedule_init_ready_retry "$INIT_READY_ATTEMPT_NUMBER" "$SKIPPED_CHECK"
  exit 0
fi

PARSE_RESULT=$(python3 - "$GENERATE_RESPONSE_FILE" "$PARSED_JSON_FILE" <<'PY'
import json
import sys
from pathlib import Path

response_path = Path(sys.argv[1])
parsed_path = Path(sys.argv[2])

try:
    data = json.loads(response_path.read_text(encoding="utf-8"))
except Exception as exc:
    print(f"parse_error|{exc}")
    sys.exit(1)

message = data.get("message") or {}
required = {
    "message_id": message.get("id"),
    "content": message.get("raw_content") or message.get("content"),
    "web_url": data.get("web_url"),
    "screenshot_url": data.get("screenshot_url"),
}
missing = [k for k, v in required.items() if v in (None, "")]
if missing:
    print("missing|" + ",".join(missing))
    sys.exit(1)
required["sticker_image_base64"] = data.get("sticker_image_base64") or ""
required["sticker_theme"] = data.get("sticker_theme") or ""
required["is_sticker"] = bool(data.get("sticker_image_base64"))
required["is_wallpaper"] = message.get("message_type") == "wallpaper"
required["is_media"] = required["is_sticker"] or required["is_wallpaper"]
parsed_path.write_text(json.dumps(required, ensure_ascii=False), encoding="utf-8")
print("ok")
PY
)
if [ "$PARSE_RESULT" != "ok" ]; then
  LAST_ERROR="解析 /api/generate 响应失败: ${PARSE_RESULT:-unknown}"
  append_delivery_ledger "parse_failed" "failed" "$LAST_ERROR"
  [ "$JOB_KIND" = "init-ready" ] && schedule_init_ready_retry "$INIT_READY_ATTEMPT_NUMBER" "$LAST_ERROR"
  error "$LAST_ERROR"
fi

MESSAGE_ID=$(python3 - "$PARSED_JSON_FILE" <<'PY'
import json
import sys
from pathlib import Path
print(json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))["message_id"])
PY
)
GENERATED_CONTENT=$(python3 - "$PARSED_JSON_FILE" <<'PY'
import json
import sys
from pathlib import Path
print(json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))["content"])
PY
)
WEB_URL=$(python3 - "$PARSED_JSON_FILE" <<'PY'
import json
import sys
from pathlib import Path
print(json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))["web_url"])
PY
)
SCREENSHOT_URL=$(python3 - "$PARSED_JSON_FILE" <<'PY'
import json
import sys
from pathlib import Path
print(json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))["screenshot_url"])
PY
)
append_delivery_ledger "generated" "ok" "message generated" "" "" "queued" "$MESSAGE_ID"
report_delivery "$MESSAGE_ID" "pending" "${BOUND_CHANNEL:-$FORCED_CHANNEL}" "${BOUND_TARGET:-$FORCED_TARGET}" "queued" "" "$SCREENSHOT_URL" ""
update_init_ready_state "generated" "$INIT_READY_ATTEMPT_NUMBER" "$MESSAGE_ID"

if [ -n "$CONTENT_PREFIX" ]; then
  GENERATED_CONTENT=$(CONTENT_PREFIX_VALUE="$CONTENT_PREFIX" GENERATED_CONTENT_VALUE="$GENERATED_CONTENT" python3 <<'PY'
import os
prefix = (os.environ.get("CONTENT_PREFIX_VALUE") or "").strip()
content = (os.environ.get("GENERATED_CONTENT_VALUE") or "").strip()
print(f"{prefix}{content}" if content else prefix)
PY
)
fi

IS_STICKER=$(python3 - "$PARSED_JSON_FILE" <<'PY'
import json
import sys
from pathlib import Path
data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
print("true" if data.get("is_media") or data.get("is_sticker") else "false")
PY
)
IS_WALLPAPER=$(python3 - "$PARSED_JSON_FILE" <<'PY'
import json
import sys
from pathlib import Path
data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
print("true" if data.get("is_wallpaper") else "false")
PY
)
STICKER_IMAGE_FILE=""
if [ "$IS_STICKER" = "true" ]; then
  MEDIA_TYPE_LABEL="表情包"
  [ "$IS_WALLPAPER" = "true" ] && MEDIA_TYPE_LABEL="壁纸"
  step "${MEDIA_TYPE_LABEL}类型：解码图片到临时文件..."
  OPENCLAW_MEDIA_DIR="${HOME}/.openclaw/media"
  mkdir -p "$OPENCLAW_MEDIA_DIR"
  STICKER_IMAGE_FILE=$(mktemp "${OPENCLAW_MEDIA_DIR}/lobster-media.XXXXXX.png")
  python3 - "$PARSED_JSON_FILE" "$STICKER_IMAGE_FILE" <<'PY'
import base64
import json
import sys
from pathlib import Path
data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
b64 = data.get("sticker_image_base64", "")
if b64:
    Path(sys.argv[2]).write_bytes(base64.b64decode(b64))
    print("ok")
else:
    print("no_data")
    sys.exit(1)
PY
  if [ $? -ne 0 ] || [ ! -s "$STICKER_IMAGE_FILE" ]; then
    warn "${MEDIA_TYPE_LABEL}图片解码失败，降级为普通消息推送"
    IS_STICKER="false"
    STICKER_IMAGE_FILE=""
  else
    info "${MEDIA_TYPE_LABEL}图片已保存: $(du -h "$STICKER_IMAGE_FILE" | cut -f1)"
    if [ "$IS_WALLPAPER" = "true" ]; then
      GENERATED_CONTENT="🦞 ${LOBSTER_NAME}给你画了一张专属壁纸~"
    else
      GENERATED_CONTENT="🦞 ${LOBSTER_NAME}给你画了一张表情包~"
    fi
  fi
fi

# ═══════════════════════════════════════════════
#  模式分流：--emit-message-text / --generate-only / 企微 CLI fallback / 通用多通道 fallback
# ═══════════════════════════════════════════════

if [ "$EMIT_MESSAGE_TEXT" = "1" ]; then
  # ───────────────────────────────────────────
  #  emit-message-text 模式：仅输出最终消息文本到 stdout
  #  供 isolated agent 直接把 stdout 原文作为 message 工具参数发送
  # ───────────────────────────────────────────
  step "emit-message-text 模式：输出最终消息文本到 stdout..."
  FINAL_TEXT=$(build_text_message true)
  echo "$FINAL_TEXT"
  append_delivery_ledger "emit_message_text" "ok" "plain text output to stdout for agent message tool" "" "" "emit_message_text" "$MESSAGE_ID"
  info "emit-message-text 完成，最终消息文本已输出到 stdout"
  exit 0
fi

if [ "$GENERATE_ONLY" = "1" ]; then
  # ───────────────────────────────────────────
  #  generate-only 模式：仅输出消息 JSON 到 stdout（保留作为备用能力）
  # ───────────────────────────────────────────
  step "generate-only 模式：输出消息 JSON 到 stdout..."

  FINAL_TEXT=$(build_text_message true)

  GENERATE_ONLY_OUTPUT=$(FINAL_TEXT_VALUE="$FINAL_TEXT" \
    GENERATED_CONTENT_VALUE="$GENERATED_CONTENT" \
    MESSAGE_ID_VALUE="$MESSAGE_ID" \
    LOBSTER_NAME_VALUE="$LOBSTER_NAME" \
    WEB_URL_VALUE="$WEB_URL" \
    SCREENSHOT_URL_VALUE="$SCREENSHOT_URL" \
    SLOT_VALUE="$SLOT" \
    IS_STICKER_VALUE="$IS_STICKER" \
    IS_WALLPAPER_VALUE="$IS_WALLPAPER" \
    STICKER_IMAGE_FILE_VALUE="${STICKER_IMAGE_FILE:-}" \
    python3 <<'PY'
import json
import os

output = {
    "message_text": os.environ["FINAL_TEXT_VALUE"],
    "raw_content": os.environ["GENERATED_CONTENT_VALUE"],
    "message_id": int(os.environ["MESSAGE_ID_VALUE"]),
    "lobster_name": os.environ["LOBSTER_NAME_VALUE"],
    "web_url": os.environ["WEB_URL_VALUE"],
    "screenshot_url": os.environ["SCREENSHOT_URL_VALUE"],
    "slot": os.environ["SLOT_VALUE"],
    "is_sticker": os.environ.get("IS_STICKER_VALUE") == "true",
    "is_wallpaper": os.environ.get("IS_WALLPAPER_VALUE") == "true",
    "sticker_image_file": os.environ.get("STICKER_IMAGE_FILE_VALUE") or None,
}
print(json.dumps(output, ensure_ascii=False))
PY
)

  echo "$GENERATE_ONLY_OUTPUT"
  append_delivery_ledger "generate_only_output" "ok" "JSON output to stdout for agent delivery" "" "" "generate_only" "$MESSAGE_ID"
  info "generate-only 完成，消息已输出到 stdout"
  exit 0
fi

if [ "$OUTBOUND_ADAPTER" = "wecom-direct-message" ]; then
  # ───────────────────────────────────────────
  #  企微 CLI fallback：仅保留给手动调试/非 cron 场景
  #  2.5.3 起不再作为企微 cron 主链路
  # ───────────────────────────────────────────
  WECOM_SEND_TARGET="${FORCED_TARGET:-${WECOM_USER_ID:-${DELIVERY_TARGET:-}}}"
  WECOM_SEND_CHANNEL="${FORCED_CHANNEL:-openclaw-wecom-bot}"

  if [ -z "$WECOM_SEND_TARGET" ]; then
    LAST_ERROR="企业微信定时推送缺少 sender_id / wecom_user_id"
    append_delivery_ledger "wecom_target_missing" "failed" "$LAST_ERROR" "$WECOM_SEND_CHANNEL" "" "wecom_cli_direct" "$MESSAGE_ID"
    [ "$JOB_KIND" = "init-ready" ] && schedule_init_ready_retry "$INIT_READY_ATTEMPT_NUMBER" "$LAST_ERROR"
    error "$LAST_ERROR"
  fi

  if [ "$IS_STICKER" = "true" ]; then
    DELIVERED_TEXT="🦞 ${LOBSTER_NAME}给你准备了一张图片礼物，先去工作室看看吧 → ${WEB_URL}"
  else
    DELIVERED_TEXT=$(build_text_message true)
  fi

  step "企微 CLI fallback：openclaw message send → ${WECOM_SEND_CHANNEL} → ${WECOM_SEND_TARGET}..."
  _SEND_STDERR_FILE=$(mktemp "${TMPDIR:-/tmp}/lobster-send-stderr.XXXXXX")
  SEND_RESULT=$(openclaw message send \
    --channel "$WECOM_SEND_CHANNEL" \
    --target "$WECOM_SEND_TARGET" \
    --message "$DELIVERED_TEXT" 2>"$_SEND_STDERR_FILE")
  SEND_RC=$?
  SEND_STDERR=""
  [ -f "$_SEND_STDERR_FILE" ] && SEND_STDERR=$(cat "$_SEND_STDERR_FILE" 2>/dev/null)

  if [ $SEND_RC -eq 0 ]; then
    # 检查假成功
    if echo "$SEND_STDERR" | grep -qiE '(wsclient|websocket|not.connected|connection.refused|connection.reset|connection.timeout|no.active.session|failed.to.send|send.failed|delivery.failed)'; then
      LAST_ERROR="企微 CLI 假成功(exit=0 但检测到连接问题): ${SEND_STDERR}"
      append_delivery_ledger "wecom_cli_direct" "failed" "$LAST_ERROR" "$WECOM_SEND_CHANNEL" "$WECOM_SEND_TARGET" "wecom_cli_direct" "$MESSAGE_ID"
      [ "$JOB_KIND" = "init-ready" ] && schedule_init_ready_retry "$INIT_READY_ATTEMPT_NUMBER" "$LAST_ERROR"
      error "$LAST_ERROR"
    fi

    DELIVERED_AT_UTC=$(date -u '+%Y-%m-%dT%H:%M:%SZ')
    report_delivery "$MESSAGE_ID" "sent" "$WECOM_SEND_CHANNEL" "$WECOM_SEND_TARGET" "wecom_cli_direct" "$DELIVERED_TEXT" "$SCREENSHOT_URL" ""
    append_delivery_ledger "wecom_cli_direct" "sent" "企微 CLI fallback 发送成功" "$WECOM_SEND_CHANNEL" "$WECOM_SEND_TARGET" "wecom_cli_direct" "$MESSAGE_ID"
    update_init_ready_state "sent" "$INIT_READY_ATTEMPT_NUMBER" "$MESSAGE_ID" "" "$WECOM_SEND_CHANNEL" "$WECOM_SEND_TARGET"
    [ "$JOB_KIND" = "init-ready" ] && finalize_managed_job
    info "📮 企微 CLI fallback 发送成功: slot=${SLOT} message_id=${MESSAGE_ID} channel=${WECOM_SEND_CHANNEL} target=${WECOM_SEND_TARGET}"
    echo "DELIVERY_OK slot=${SLOT} message_id=${MESSAGE_ID} channel=${WECOM_SEND_CHANNEL} mode=wecom_cli_direct" >&2
    exit 0
  else
    LAST_ERROR="企微 CLI 发送失败 (rc=${SEND_RC}): ${SEND_STDERR}"
    report_delivery "$MESSAGE_ID" "failed" "$WECOM_SEND_CHANNEL" "$WECOM_SEND_TARGET" "wecom_cli_direct" "" "$SCREENSHOT_URL" "$LAST_ERROR"
    append_delivery_ledger "wecom_cli_direct" "failed" "$LAST_ERROR" "$WECOM_SEND_CHANNEL" "$WECOM_SEND_TARGET" "wecom_cli_direct" "$MESSAGE_ID"
    [ "$JOB_KIND" = "init-ready" ] && update_init_ready_state "delivery_failed" "$INIT_READY_ATTEMPT_NUMBER" "$MESSAGE_ID" "$LAST_ERROR" "$WECOM_SEND_CHANNEL" "$WECOM_SEND_TARGET"
    [ "$JOB_KIND" = "init-ready" ] && schedule_init_ready_retry "$INIT_READY_ATTEMPT_NUMBER" "$LAST_ERROR"
    error "$LAST_ERROR"
  fi
fi

# ═══════════════════════════════════════════════
#  完整发送模式：多通道 fallback（Telegram 等通用通道）
# ═══════════════════════════════════════════════
step "扫描最近活跃的 IM 通道..."
if [ -n "$FORCED_CHANNEL" ] && [ -n "$FORCED_TARGET" ]; then
  info "显式指定通道: ${FORCED_CHANNEL} → ${FORCED_TARGET}（最高优先级）"
fi

SESSIONS_JSON=$(openclaw sessions --json --active "$ACTIVE_WINDOW_MINUTES" 2>/dev/null || echo "[]")
CANDIDATE_LINES=$(build_candidate_lines "$SESSIONS_JSON" "$FORCED_CHANNEL" "$FORCED_TARGET")
if [ -z "$CANDIDATE_LINES" ]; then
  LAST_ERROR="没有找到可用的投递通道。请先在 Telegram / 微信 / 飞书等任一通道里和虾说一句话，或在 setup-cron.sh 时指定 --channel 和 --to。"
  append_delivery_ledger "candidate_resolve_failed" "failed" "$LAST_ERROR"
  [ "$JOB_KIND" = "init-ready" ] && schedule_init_ready_retry "$INIT_READY_ATTEMPT_NUMBER" "$LAST_ERROR"
  error "$LAST_ERROR"
fi
FIRST_CANDIDATE=$(echo "$CANDIDATE_LINES" | head -1)
info "本次优先尝试最近使用的通道：${FIRST_CANDIDATE%%|*}"

LAST_ERROR=""
LAST_CHANNEL=""
LAST_TARGET=""
SUCCESS_CHANNEL=""
SUCCESS_TARGET=""
SUCCESS_MODE=""
DELIVERED_TEXT=""
ATTEMPT_COUNT=0
_SEND_STDERR_FILE=$(mktemp "${TMPDIR:-/tmp}/lobster-send-stderr.XXXXXX")

reliable_send() {
  _SEND_FAIL_REASON=""
  openclaw message send "$@" >"$_SEND_STDERR_FILE" 2>&1
  local rc=$?
  local stderr_content=""
  [ -f "$_SEND_STDERR_FILE" ] && stderr_content=$(cat "$_SEND_STDERR_FILE" 2>/dev/null)
  if [ $rc -ne 0 ]; then
    _SEND_FAIL_REASON="exit_code=${rc} ${stderr_content}"
    return 1
  fi
  if echo "$stderr_content" | grep -qiE '(wsclient|websocket|not.connected|connection.refused|connection.reset|connection.timeout|no.active.session|failed.to.send|send.failed|delivery.failed)'; then
    _SEND_FAIL_REASON="假成功(exit=0 但检测到连接问题): ${stderr_content}"
    return 1
  fi
  return 0
}

while IFS='|' read -r channel target; do
  [ -z "$channel" ] && continue
  [ -z "$target" ] && continue
  ATTEMPT_COUNT=$((ATTEMPT_COUNT + 1))
  LAST_CHANNEL="$channel"
  LAST_TARGET="$target"
  step "尝试投递到 ${channel} → ${target} (attempt #${ATTEMPT_COUNT})"
  append_delivery_ledger "channel_attempt" "running" "attempt=${ATTEMPT_COUNT}" "$channel" "$target" "" "$MESSAGE_ID"

  if [ "$IS_STICKER" = "true" ] && [ -n "$STICKER_IMAGE_FILE" ] && [ -f "$STICKER_IMAGE_FILE" ]; then
    STUDIO_ENTRY_LINE="👀 看看${LOBSTER_NAME}在干嘛 → ${WEB_URL}"
    if [ "$IS_WALLPAPER" = "true" ]; then
      STICKER_TEXT="🦞 ${LOBSTER_NAME}给你画了一张专属壁纸~
${STUDIO_ENTRY_LINE}"
      MEDIA_LABEL="壁纸"
    else
      STICKER_TEXT="🦞 ${LOBSTER_NAME}给你画了一张表情包~
${STUDIO_ENTRY_LINE}"
      MEDIA_LABEL="表情包"
    fi
    if supports_media "$channel"; then
      if reliable_send --channel "$channel" --to "$target" --message "$STICKER_TEXT"; then
        if reliable_send --channel "$channel" --to "$target" --media "$STICKER_IMAGE_FILE"; then
          SUCCESS_CHANNEL="$channel"
          SUCCESS_TARGET="$target"
          SUCCESS_MODE="media"
          DELIVERED_TEXT="$STICKER_TEXT"
          info "${MEDIA_LABEL}文本 + 图片发送成功"
          break
        fi
        warn "${channel} ${MEDIA_LABEL}图片发送失败 (${_SEND_FAIL_REASON})，降级为文字提示"
      fi
    fi
    FALLBACK_TEXT="🦞 ${LOBSTER_NAME}画了一张${MEDIA_LABEL}给你，不过这个通道暂时看不了图~去虾的工作室看看吧 → ${WEB_URL}"
    if reliable_send --channel "$channel" --to "$target" --message "$FALLBACK_TEXT"; then
      SUCCESS_CHANNEL="$channel"
      SUCCESS_TARGET="$target"
      SUCCESS_MODE="url"
      DELIVERED_TEXT="$FALLBACK_TEXT"
      info "${MEDIA_LABEL}降级为文字提示发送成功"
      break
    fi
    LAST_ERROR="${channel} ${MEDIA_LABEL}所有模式都发送失败: ${_SEND_FAIL_REASON}"
    warn "$LAST_ERROR，继续回退下一个通道"
    append_delivery_ledger "channel_attempt" "failed" "$LAST_ERROR" "$channel" "$target" "url" "$MESSAGE_ID"
    continue
  fi

  if supports_media "$channel"; then
    TEXT_MESSAGE=$(build_text_message false)
    if reliable_send --channel "$channel" --target "$target" --message "$TEXT_MESSAGE"; then
      if reliable_send --channel "$channel" --target "$target" --media "$SCREENSHOT_URL"; then
        SUCCESS_CHANNEL="$channel"
        SUCCESS_TARGET="$target"
        SUCCESS_MODE="media"
        DELIVERED_TEXT="$TEXT_MESSAGE"
        info "文本 + 原生截图发送成功"
        break
      fi
      warn "${channel} 原生截图发送失败 (${_SEND_FAIL_REASON})，降级为补发截图 URL"
      URL_FALLBACK=$(build_text_message true)
      if reliable_send --channel "$channel" --target "$target" --message "$URL_FALLBACK"; then
        SUCCESS_CHANNEL="$channel"
        SUCCESS_TARGET="$target"
        SUCCESS_MODE="degraded_url"
        DELIVERED_TEXT="$URL_FALLBACK"
        info "已降级为文本 + 截图 URL"
        break
      fi
      LAST_ERROR="${channel} 原生图片与 URL 降级都失败: ${_SEND_FAIL_REASON}"
      warn "$LAST_ERROR，继续回退下一个通道"
      append_delivery_ledger "channel_attempt" "failed" "$LAST_ERROR" "$channel" "$target" "degraded_url" "$MESSAGE_ID"
      continue
    fi
    LAST_ERROR="${channel} 文本消息发送失败: ${_SEND_FAIL_REASON}"
    warn "$LAST_ERROR，继续回退下一个通道"
    append_delivery_ledger "channel_attempt" "failed" "$LAST_ERROR" "$channel" "$target" "text_only" "$MESSAGE_ID"
    continue
  fi

  TEXT_MESSAGE=$(build_text_message true)
  if reliable_send --channel "$channel" --to "$target" --message "$TEXT_MESSAGE"; then
    SUCCESS_CHANNEL="$channel"
    SUCCESS_TARGET="$target"
    SUCCESS_MODE="url"
    DELIVERED_TEXT="$TEXT_MESSAGE"
    info "纯文本 + 截图 URL 发送成功"
    break
  fi

  LAST_ERROR="${channel} 文本消息发送失败: ${_SEND_FAIL_REASON}"
  warn "$LAST_ERROR，继续回退下一个通道"
  append_delivery_ledger "channel_attempt" "failed" "$LAST_ERROR" "$channel" "$target" "url" "$MESSAGE_ID"
done <<< "$CANDIDATE_LINES"

if [ -n "$SUCCESS_CHANNEL" ]; then
  DELIVERED_AT_UTC=$(date -u '+%Y-%m-%dT%H:%M:%SZ')
  report_delivery "$MESSAGE_ID" "sent" "$SUCCESS_CHANNEL" "$SUCCESS_TARGET" "$SUCCESS_MODE" "$DELIVERED_TEXT" "$SCREENSHOT_URL" ""
  UPDATED_KNOWN=$(sync_known_channels_after_send "$SUCCESS_CHANNEL" "$SUCCESS_TARGET" "$CANDIDATE_LINES" "$DELIVERED_AT_UTC")
  append_delivery_ledger "delivery_succeeded" "sent" "attempts=${ATTEMPT_COUNT}" "$SUCCESS_CHANNEL" "$SUCCESS_TARGET" "$SUCCESS_MODE" "$MESSAGE_ID"
  update_init_ready_state "sent" "$INIT_READY_ATTEMPT_NUMBER" "$MESSAGE_ID" "" "$SUCCESS_CHANNEL" "$SUCCESS_TARGET"
  [ "$JOB_KIND" = "init-ready" ] && finalize_managed_job
  info "📮 送达成功: slot=${SLOT} message_id=${MESSAGE_ID} channel=${SUCCESS_CHANNEL} target=${SUCCESS_TARGET} mode=${SUCCESS_MODE} attempts=${ATTEMPT_COUNT}"
  echo "DELIVERY_OK slot=${SLOT} message_id=${MESSAGE_ID} channel=${SUCCESS_CHANNEL} mode=${SUCCESS_MODE}" >&2
  echo "KNOWN_CHANNELS=${UPDATED_KNOWN}" >&2
  exit 0
fi

warn "📮 送达失败: slot=${SLOT} message_id=${MESSAGE_ID} last_channel=${LAST_CHANNEL} attempts=${ATTEMPT_COUNT} error=${LAST_ERROR}"
report_delivery "$MESSAGE_ID" "failed" "${LAST_CHANNEL:-$BOUND_CHANNEL}" "${LAST_TARGET:-$BOUND_TARGET}" "text_only" "" "$SCREENSHOT_URL" "$LAST_ERROR"
append_delivery_ledger "delivery_failed" "failed" "$LAST_ERROR" "${LAST_CHANNEL:-$BOUND_CHANNEL}" "${LAST_TARGET:-$BOUND_TARGET}" "text_only" "$MESSAGE_ID"
[ "$JOB_KIND" = "init-ready" ] && update_init_ready_state "delivery_failed" "$INIT_READY_ATTEMPT_NUMBER" "$MESSAGE_ID" "$LAST_ERROR" "${LAST_CHANNEL:-$BOUND_CHANNEL}" "${LAST_TARGET:-$BOUND_TARGET}"
[ "$JOB_KIND" = "init-ready" ] && schedule_init_ready_retry "$INIT_READY_ATTEMPT_NUMBER" "$LAST_ERROR"
error "所有候选通道都投递失败：${LAST_ERROR:-未知错误}"
