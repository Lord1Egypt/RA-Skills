#!/bin/bash
# 虾说 — 定时推送 Cron 注册脚本
#
# 数据访问声明：
# - 读取 .lobster-config（技能自身配置）
# - 调用 openclaw sessions --json 获取活跃 IM 通道元数据
# - 调用 openclaw cron add/remove/list 管理定时任务
# - 不读取 openclaw.json 配置文件，不提取 gateway token
# - gateway 认证仅通过用户显式设置的 OPENCLAW_GATEWAY_TOKEN 环境变量
#
# 重构设计（v2.5.3 可测版）：
# - 企微通道：cron 注册带 --channel openclaw-wecom-bot --to <sender_id>（delivery 兜底）
#   agent prompt 只做两件事：执行 push-scheduled-message.sh --emit-message-text 取得最终文本，
#   然后必须使用 message 工具发送私聊；不再依赖脚本内 CLI 直发
# - 通用通道（Telegram等）：仍由脚本完整模式执行，多通道 fallback + delivery 兜底
# - openclaw cron add 继续使用 --to；但 openclaw message send 一律使用 --target，避免 CLI 参数漂移

set -u

ACTION="reconcile"
CHANNEL=""
TO=""
WECOM_USER_ID=""
MORNING_TIME=""
DISCOVERY_TIME=""
EVENING_TIME=""
MEMORY_MODE=""
REMOVE_JOB_NAME=""
SCHEDULE_INIT_READY_DELAY=""
INIT_READY_DELAY_MINUTES="${INIT_READY_DELAY_MINUTES:-3}"
INIT_READY_MIN_LEAD_MINUTES="${INIT_READY_MIN_LEAD_MINUTES:-2}"
INIT_READY_VERIFY_ATTEMPTS="${INIT_READY_VERIFY_ATTEMPTS:-3}"
ACTIVE_WINDOW_MINUTES="${ACTIVE_WINDOW_MINUTES:-10080}"
BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
CONFIG_FILE="${BASE_DIR}/.lobster-config"
COMMON_SCRIPT="${BASE_DIR}/runtime-common.sh"
LOG_DIR="${BASE_DIR}/logs"
RUN_TS="$(date +%Y%m%d-%H%M%S)"
LOG_FILE="${LOG_DIR}/setup-cron-${RUN_TS}.log"
PUSH_SCRIPT="${BASE_DIR}/push-scheduled-message.sh"
OPENCLAW_CRON_ARGS=()
INIT_READY_JOB_NAME="lobster-says-init-ready"
DETECTED_KNOWN_JSON="[]"
DELIVERY_CHANNEL=""
DELIVERY_TARGET=""
DELIVERY_READY="0"
DELIVERY_REASON=""
DELIVERY_FAMILY="general"
OUTBOUND_ADAPTER="openclaw"
BINDING_CHANNEL=""
BINDING_TARGET=""
BINDING_MODE="prefer"

MANAGED_JOB_NAMES=(
  "lobster-says-morning"
  "lobster-says-discovery"
  "lobster-says-evening"
  "lobster-says-init-ready"
  "lobster-says-sticker"
  "lobster-says-wallpaper"
  "lobster-says-digest"
)

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m'

info()  { echo -e "${GREEN}[✓]${NC} $1"; }
warn()  { echo -e "${YELLOW}[!]${NC} $1"; }
error() { echo -e "${RED}[✗]${NC} $1"; exit 1; }
CURRENT_STEP="启动"
step()  { CURRENT_STEP="$1"; echo -e "${CYAN}──${NC} $1"; }

if [ ! -f "$COMMON_SCRIPT" ]; then
  error "共享运行时脚本不存在：${COMMON_SCRIPT}"
fi
. "$COMMON_SCRIPT"

mkdir -p "$LOG_DIR"
if command -v tee >/dev/null 2>&1; then
  exec > >(tee -a "$LOG_FILE") 2>&1
else
  exec >>"$LOG_FILE" 2>&1
fi

echo "[log] setup-cron started at $(date '+%F %T')"
echo "[log] file: ${LOG_FILE}"

after_exit() {
  local exit_code=$?
  if [ "$exit_code" -ne 0 ]; then
    echo ""
    echo "[log] setup-cron failed at step: ${CURRENT_STEP} (exit=${exit_code})"
    echo "[log] inspect: ${LOG_FILE}"
  else
    echo "[log] setup-cron finished successfully"
  fi
}
trap after_exit EXIT

while [[ $# -gt 0 ]]; do
  case "$1" in
    --channel) CHANNEL="$2"; shift 2 ;;
    --to) TO="$2"; shift 2 ;;
    --morning) MORNING_TIME="$2"; shift 2 ;;
    --discovery) DISCOVERY_TIME="$2"; shift 2 ;;
    --evening) EVENING_TIME="$2"; shift 2 ;;
    --memory-mode) MEMORY_MODE="$2"; shift 2 ;;
    --wecom-user-id) WECOM_USER_ID="$2"; shift 2 ;;
    --remove-job-by-name) ACTION="remove-job-by-name"; REMOVE_JOB_NAME="$2"; shift 2 ;;
    --schedule-init-ready-delay) ACTION="schedule-init-ready-delay"; SCHEDULE_INIT_READY_DELAY="$2"; shift 2 ;;
    *) echo "未知参数: $1"; exit 1 ;;
  esac
done

for cmd in openclaw python3; do
  if ! command -v "$cmd" >/dev/null 2>&1; then
    error "$cmd 不可用"
  fi
done

if [ ! -f "$CONFIG_FILE" ]; then
  error ".lobster-config 不存在，请先完成虾的初始化"
fi

if [ ! -f "$PUSH_SCRIPT" ]; then
  error "运行时推送脚本不存在：${PUSH_SCRIPT}"
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
    data = json.loads(path.read_text(encoding="utf-8"))
    value = data.get(key, default)
    print(value if value is not None else default)
except Exception:
    print(default)
PY
}

load_gateway_auth() {
  OPENCLAW_CRON_ARGS=()
  local token="${OPENCLAW_GATEWAY_TOKEN:-}"
  if [ -n "$token" ]; then
    OPENCLAW_CRON_ARGS+=(--token "$token")
  fi
}

list_managed_jobs() {
  local raw
  raw=$(openclaw cron list "${OPENCLAW_CRON_ARGS[@]}" --json 2>/dev/null || echo "")
  CRON_DATA="$raw" python3 <<'PY'
import json
import os
import sys

raw = os.environ.get("CRON_DATA", "")
if not raw.strip():
    raise SystemExit(0)
json_str = None
for i, ch in enumerate(raw):
    if ch in ("{", "["):
        json_str = raw[i:]
        break
if not json_str:
    raise SystemExit(0)
try:
    data = json.loads(json_str)
except Exception:
    raise SystemExit(0)
jobs = data.get("jobs", []) if isinstance(data, dict) else data if isinstance(data, list) else []
target_names = {
    "lobster-says-morning",
    "lobster-says-discovery",
    "lobster-says-evening",
    "lobster-says-init-ready",
    "lobster-says-sticker",
    "lobster-says-wallpaper",
    "lobster-says-digest",
}
for job in jobs:
    if isinstance(job, dict) and job.get("name") in target_names and job.get("id"):
        print(f"{job['name']}|{job['id']}")
PY
}

remove_job_by_name() {
  local name="$1"
  local found=0
  while IFS='|' read -r job_name job_id; do
    [ -z "$job_id" ] && continue
    [ "$job_name" = "$name" ] || continue
    found=1
    warn "删除旧任务: ${job_name} (${job_id})"
    openclaw cron remove "$job_id" >/dev/null 2>&1 || warn "删除失败: ${job_name} (${job_id})"
  done <<< "$(list_managed_jobs)"
  if [ "$found" -eq 0 ]; then
    info "没有找到任务: ${name}"
  fi
}

remove_all_managed_jobs() {
  local jobs
  jobs=$(list_managed_jobs)
  if [ -z "$jobs" ]; then
    info "没有发现旧任务"
    return 0
  fi
  while IFS='|' read -r name job_id; do
    [ -z "$job_id" ] && continue
    warn "删除旧任务: ${name} (${job_id})"
    openclaw cron remove "${OPENCLAW_CRON_ARGS[@]}" "$job_id" >/dev/null 2>&1 || warn "删除失败: ${name} (${job_id})"
  done <<< "$jobs"
}

read_job_snapshot_by_name() {
  local name="$1"
  local raw
  raw=$(openclaw cron list "${OPENCLAW_CRON_ARGS[@]}" --json 2>/dev/null || echo "")
  CRON_DATA="$raw" TARGET_JOB_NAME="$name" python3 <<'PY'
import json
import os

raw = os.environ.get("CRON_DATA", "")
target_name = os.environ.get("TARGET_JOB_NAME", "")
if not raw.strip() or not target_name:
    raise SystemExit(0)

json_str = None
for i, ch in enumerate(raw):
    if ch in ("{", "["):
        json_str = raw[i:]
        break
if not json_str:
    raise SystemExit(0)

try:
    data = json.loads(json_str)
except Exception:
    raise SystemExit(0)

if isinstance(data, dict):
    jobs = data.get("jobs", [])
    if not isinstance(jobs, list):
        jobs = data.get("data", []) if isinstance(data.get("data"), list) else []
elif isinstance(data, list):
    jobs = data
else:
    jobs = []


def pick_text(payload, keys):
    if not isinstance(payload, dict):
        return ""
    for key in keys:
        value = payload.get(key)
        if value not in (None, ""):
            return str(value).strip()
    return ""


def pick_nested(payload, path_groups):
    for path in path_groups:
        current = payload
        valid = True
        for key in path:
            if not isinstance(current, dict):
                valid = False
                break
            current = current.get(key)
        if valid and current not in (None, ""):
            return current
    return None


def normalize_next_run(value):
    if value in (None, ""):
        return ""
    if isinstance(value, str):
        text = value.strip()
        if not text:
            return ""
        if text.isdigit():
            value = int(text)
        else:
            return text
    if isinstance(value, (int, float)):
        timestamp = float(value)
        if timestamp > 1000000000000:
            timestamp /= 1000.0
        from datetime import datetime, timezone
        return datetime.fromtimestamp(timestamp, tz=timezone.utc).isoformat().replace("+00:00", "Z")
    return str(value).strip()

for job in jobs:
    if not isinstance(job, dict) or str(job.get("name") or "").strip() != target_name:
        continue
    next_run_value = pick_nested(job, [
        ("nextRun",),
        ("next_run",),
        ("nextRunAt",),
        ("next_run_at",),
        ("nextExecution",),
        ("next_execution",),
        ("nextExecutionAt",),
        ("next_execution_at",),
        ("nextFireAt",),
        ("next_fire_at",),
        ("schedule", "nextRun"),
        ("schedule", "next_run"),
        ("schedule", "nextRunAt"),
        ("schedule", "next_run_at"),
        ("schedule", "nextExecution"),
        ("schedule", "next_execution"),
        ("schedule", "nextExecutionAt"),
        ("schedule", "next_execution_at"),
        ("schedule", "nextFireAt"),
        ("schedule", "next_fire_at"),
        ("state", "nextRunAtMs"),
        ("state", "next_run_at_ms"),
        ("state", "nextRunAt"),
        ("state", "next_run_at"),
        ("state", "nextExecutionAt"),
        ("state", "next_execution_at"),
    ])
    next_run = normalize_next_run(next_run_value)
    state_payload = job.get("state") if isinstance(job.get("state"), dict) else {}
    status = pick_text(job, ("status",)) or pick_text(state_payload, ("status", "phase", "name"))
    print(str(job.get("id") or "").strip())
    print(next_run)
    print(status)
    print(json.dumps(job, ensure_ascii=False))
    break
PY
}

validate_init_ready_next_run() {
  local next_run="$1"
  NEXT_RUN_VALUE="$next_run" python3 <<'PY'
from datetime import datetime, timedelta, timezone
import os

raw = (os.environ.get("NEXT_RUN_VALUE") or "").strip()
if not raw or raw.lower() == "null":
    print("invalid|nextRun 为空")
    raise SystemExit(0)

app_tz = timezone(timedelta(hours=8))
now = datetime.now(app_tz)


def mark(dt, label):
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=app_tz)
    else:
        dt = dt.astimezone(app_tz)
    if dt <= now:
        print(f"invalid|nextRun 已过期: {label}")
    else:
        print(f"ok|{label}")
    raise SystemExit(0)

try:
    mark(datetime.fromisoformat(raw.replace("Z", "+00:00")), raw)
except Exception:
    pass

for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y/%m/%d %H:%M:%S", "%Y/%m/%d %H:%M"):
    try:
        mark(datetime.strptime(raw, fmt), raw)
    except Exception:
        pass

print(f"ok|{raw}")
PY
}

parse_time() {
  local time_str="$1"
  local hour
  local minute
  hour=$(echo "$time_str" | cut -d: -f1 | sed 's/^0//')
  minute=$(echo "$time_str" | cut -d: -f2 | sed 's/^0//')
  echo "${minute:-0} ${hour:-0} * * *"
}

compute_init_ready_schedule() {
  local delay_minutes="$1"
  INIT_READY_DELAY_VALUE="$delay_minutes" INIT_READY_MIN_LEAD_VALUE="$INIT_READY_MIN_LEAD_MINUTES" MORNING_TIME_VALUE="$MORNING_TIME" DISCOVERY_TIME_VALUE="$DISCOVERY_TIME" EVENING_TIME_VALUE="$EVENING_TIME" python3 <<'PY'
from datetime import datetime, timedelta, timezone
import os

app_tz = timezone(timedelta(hours=8))
now = datetime.now(app_tz)
rounded_now = now.replace(second=0, microsecond=0)
if rounded_now < now:
    rounded_now += timedelta(minutes=1)
delay = max(int(os.environ.get("INIT_READY_DELAY_VALUE", "5") or "5"), 1)
minimum_lead = max(int(os.environ.get("INIT_READY_MIN_LEAD_VALUE", "2") or "2"), 1)
target = rounded_now + timedelta(minutes=delay)
if (target - now).total_seconds() < minimum_lead * 60:
    target = rounded_now + timedelta(minutes=minimum_lead)
reserved_slots = {
    (os.environ.get("MORNING_TIME_VALUE") or "").strip(),
    (os.environ.get("DISCOVERY_TIME_VALUE") or "").strip(),
    (os.environ.get("EVENING_TIME_VALUE") or "").strip(),
}
reserved_slots = {slot for slot in reserved_slots if slot}
shifted = 0
while target.strftime("%H:%M") in reserved_slots and shifted < 15:
    target += timedelta(minutes=1)
    shifted += 1
cron_expr = f"{target.minute} {target.hour} {target.day} {target.month} *"
print(cron_expr)
print(target.strftime("%H:%M"))
print(str(shifted))
PY
}

persist_local_config() {
  local known_json="$1"
  local config_channel="$2"
  local config_target="$3"
  local wecom_user_id="$4"
  CONFIG_FILE="$CONFIG_FILE" MORNING_TIME="$MORNING_TIME" DISCOVERY_TIME="$DISCOVERY_TIME" EVENING_TIME="$EVENING_TIME" MEMORY_MODE_VALUE="$MEMORY_MODE" CHANNEL_VALUE="$config_channel" TO_VALUE="$config_target" WECOM_USER_ID_VALUE="$wecom_user_id" KNOWN_JSON="$known_json" python3 <<'PY'
import json
import os
from pathlib import Path

config_path = Path(os.environ["CONFIG_FILE"])
try:
    config = json.loads(config_path.read_text(encoding="utf-8"))
except Exception:
    config = {}

config["morning_time"] = os.environ["MORNING_TIME"]
config["discovery_time"] = os.environ["DISCOVERY_TIME"]
config["evening_time"] = os.environ["EVENING_TIME"]
config["memory_mode"] = os.environ["MEMORY_MODE_VALUE"]

channel = os.environ.get("CHANNEL_VALUE", "").strip()
target = os.environ.get("TO_VALUE", "").strip()
wecom_user_id = os.environ.get("WECOM_USER_ID_VALUE", "").strip()
if channel and target:
    config["channel"] = channel
    config["chat_id"] = target
if wecom_user_id:
    config["wecom_user_id"] = wecom_user_id

ordered = []
seen = set()

def add(ch, peer_id):
    ch = (ch or "").strip()
    peer_id = (peer_id or "").strip()
    if not ch or not peer_id:
        return
    key = (ch, peer_id)
    if key in seen:
        return
    seen.add(key)
    ordered.append({"channel": ch, "peer_id": peer_id})

if channel and target:
    add(channel, target)

for preferred in (
    (config.get("binding_channel"), config.get("binding_target")),
    (config.get("delivery_channel"), config.get("delivery_target")),
):
    add(*preferred)

try:
    detected = json.loads(os.environ.get("KNOWN_JSON", "[]"))
except Exception:
    detected = []
for item in detected:
    if isinstance(item, dict):
        add(item.get("channel"), item.get("peer_id"))
for item in config.get("known_channels", []):
    if isinstance(item, dict):
        add(item.get("channel"), item.get("peer_id"))

config["known_channels"] = ordered
config_path.write_text(json.dumps(config, indent=2, ensure_ascii=False), encoding="utf-8")
print("[✓] .lobster-config 已更新")
PY
}

sync_delivery_contract() {
  local hint_channel="$1"
  local hint_target="$2"
  local contract_json
  contract_json=$(lobster_sync_delivery_contract "$CONFIG_FILE" "$hint_channel" "$hint_target")
  mapfile -t CONTRACT_LINES < <(CONTRACT_JSON_VALUE="$contract_json" python3 <<'PY'
import json
import os
contract = json.loads(os.environ["CONTRACT_JSON_VALUE"])
print(contract.get("binding_channel", ""))
print(contract.get("binding_target", ""))
print(contract.get("binding_mode", "prefer"))
print(contract.get("delivery_channel", ""))
print(contract.get("delivery_target", ""))
print("1" if contract.get("delivery_ready") else "0")
print(contract.get("delivery_reason", ""))
print(contract.get("delivery_family", "general"))
print(contract.get("outbound_adapter", "openclaw"))
PY
)
  BINDING_CHANNEL="${CONTRACT_LINES[0]:-}"
  BINDING_TARGET="${CONTRACT_LINES[1]:-}"
  BINDING_MODE="${CONTRACT_LINES[2]:-prefer}"
  DELIVERY_CHANNEL="${CONTRACT_LINES[3]:-}"
  DELIVERY_TARGET="${CONTRACT_LINES[4]:-}"
  DELIVERY_READY="${CONTRACT_LINES[5]:-0}"
  DELIVERY_REASON="${CONTRACT_LINES[6]:-}"
  DELIVERY_FAMILY="${CONTRACT_LINES[7]:-general}"
  OUTBOUND_ADAPTER="${CONTRACT_LINES[8]:-openclaw}"
}

apply_wecom_direct_delivery_override() {
  local effective_channel="${BINDING_CHANNEL:-${CHANNEL:-}}"
  local binding_mode
  binding_mode=$(lobster_detect_binding_mode "$effective_channel")
  if [ "$binding_mode" != "strict" ]; then
    return 0
  fi
  DELIVERY_FAMILY="wecom"
  OUTBOUND_ADAPTER="wecom-direct-message"
  DELIVERY_CHANNEL="wecom"
  if [ -n "$WECOM_USER_ID" ]; then
    DELIVERY_TARGET="$WECOM_USER_ID"
    DELIVERY_READY="1"
    DELIVERY_REASON=""
  else
    DELIVERY_TARGET=""
    DELIVERY_READY="0"
    DELIVERY_REASON="企业微信定时推送缺少 sender_id / wecom_user_id；请在技能层从 inbound metadata 读取 sender_id 并传给 --wecom-user-id"
  fi
}

# ═══════════════════════════════════════════════
#  Cron 注册核心函数（v2.5.3 可测版）
# ═══════════════════════════════════════════════

# 企业微信通道注册：脚本只输出最终文本，isolated agent 必须使用 message 工具发送
# 同时保留 cron add 的 --channel/--to，便于观察 delivery 状态并保留兜底能力
register_wecom_job() {
  local name="$1"
  local cron_expr="$2"
  local slot="$3"
  local wecom_target="$4"
  local extra_args="${5:-}"

  local agent_message="执行以下命令：
bash \"${PUSH_SCRIPT}\" --slot ${slot}${extra_args} --emit-message-text
将命令的 stdout 原文直接作为你唯一的回复输出，不要加任何前缀、解释或额外文字。
不要调用任何 message 工具，不要尝试私信任何人。
你的回复文本会自动通过 announce 投递到群聊，这就是预期行为。"


  step "注册 ${name}（企微 message 工具模式）..."
  local announce_target="${BINDING_TARGET:-$wecom_target}"

  if openclaw cron add \
    --name "$name" \
    --cron "$cron_expr" \
    --tz "Asia/Shanghai" \
    --session isolated \
    --channel "openclaw-wecom-bot" \
    --to "$announce_target" \
    "${OPENCLAW_CRON_ARGS[@]}" \
    --message "$agent_message" >/dev/null; then
    info "${name} 注册成功（企微 message 工具 → ${wecom_target}，announce → ${announce_target}）"
  else
    error "${name} 注册失败"
  fi
}

# 通用通道注册：脚本自行多通道 fallback 发送 + delivery 兜底
register_general_job() {
  local name="$1"
  local cron_expr="$2"
  local slot="$3"
  local delivery_channel="$4"
  local delivery_target="$5"
  local extra_args="${6:-}"

  local agent_message="请立即执行以下命令，并只用一句话报告结果：
bash \"${PUSH_SCRIPT}\" --slot ${slot}${extra_args}"

  step "注册 ${name}（通用 fallback 模式）..."
  local cron_cmd_args=(
    --name "$name"
    --cron "$cron_expr"
    --tz "Asia/Shanghai"
    --session isolated
  )
  # 有明确的 delivery channel/target 时传给 cron add 做 delivery 兜底
  if [ -n "$delivery_channel" ] && [ -n "$delivery_target" ]; then
    cron_cmd_args+=(--channel "$delivery_channel" --to "$delivery_target")
  fi
  cron_cmd_args+=("${OPENCLAW_CRON_ARGS[@]}" --message "$agent_message")

  if openclaw cron add "${cron_cmd_args[@]}" >/dev/null; then
    info "${name} 注册成功"
  else
    error "${name} 注册失败"
  fi
}

register_init_ready_job() {
  local delay_minutes="$1"
  local wecom_target="$2"
  local push_script="$3"
  local init_ready_suffix="$4"

  step "注册 init-ready 一次性任务（${delay_minutes} 分钟后触发）..."

  local trigger_at
  trigger_at=$(DELAY_MINUTES_V="$delay_minutes" python3 <<'PYTS'
from datetime import datetime, timezone, timedelta
import os
delay = int(os.environ.get("DELAY_MINUTES_V", "3"))
t = datetime.now(timezone.utc).replace(microsecond=0) + timedelta(minutes=delay)
print(t.isoformat().replace("+00:00", "Z"))
PYTS
)
  [ -n "$trigger_at" ] || { error "init-ready trigger_at 计算失败"; }

  INIT_READY_EFFECTIVE_TIME=$(TRIGGER_AT_V="$trigger_at" python3 -c "
from datetime import datetime, timezone, timedelta
t = datetime.fromisoformat('$trigger_at'.replace('Z','+00:00'))
print(t.astimezone(timezone(timedelta(hours=8))).strftime('%H:%M'))
" 2>/dev/null || echo "$trigger_at")

  if [ "$OUTBOUND_ADAPTER" = "wecom-direct-message" ] && [ -n "$wecom_target" ]; then
    # 企微 init-ready：直接让 isolated agent 调用 message 工具，避免再经过 shell CLI
    local lobster_name
    lobster_name=$(read_config_value "lobster_name" "虾")
    local message_for_agent="执行以下命令：
bash \"${push_script}\" --slot event${init_ready_suffix} --emit-message-text
将 stdout 原文直接作为你唯一的回复输出，不要加任何前缀、解释或额外文字。
不要调用任何 message 工具，不要尝试私信任何人。
你的回复文本会自动通过 announce 投递到群聊，这就是预期行为。"

    local init_ready_announce_target="${BINDING_TARGET:-$wecom_target}"
    local cron_result rc
    cron_result=$(openclaw cron add \
      --name "lobster-says-init-ready" \
      --at "$trigger_at" \
      --session isolated \
      --message "$message_for_agent" \
      --delete-after-run \
      --channel "openclaw-wecom-bot" \
      --to "$init_ready_announce_target" \
      "${OPENCLAW_CRON_ARGS[@]}" 2>&1)
    rc=$?
    [ $rc -eq 0 ] || error "init-ready 注册失败: ${cron_result}"
    info "init-ready 注册成功（at=${trigger_at}, 企微 message 工具 → ${wecom_target}）"
  else
    # 通用通道 init-ready：脚本完整模式执行
    local init_message="请立即执行以下命令，并只用一句话报告结果：
bash \"${push_script}\" --slot event${init_ready_suffix}"

    local cron_cmd_args=(
      --name "$INIT_READY_JOB_NAME"
      --at "$trigger_at"
      --session isolated
      --delete-after-run
    )
    if [ -n "$DELIVERY_CHANNEL" ] && [ -n "$DELIVERY_TARGET" ]; then
      cron_cmd_args+=(--channel "$DELIVERY_CHANNEL" --to "$DELIVERY_TARGET")
    fi
    cron_cmd_args+=("${OPENCLAW_CRON_ARGS[@]}" --message "$init_message")

    if openclaw cron add "${cron_cmd_args[@]}" >/dev/null; then
      info "init-ready 注册成功（at=${trigger_at}）"
    else
      error "init-ready 注册失败"
    fi
  fi

  update_init_ready_schedule_state "scheduled" "$INIT_READY_EFFECTIVE_TIME" "$trigger_at" "" "at=${trigger_at}"
}


update_init_ready_schedule_state() {
  local state="$1"
  local scheduled_for="${2:-}"
  local verified_next_run="${3:-}"
  local job_id="${4:-}"
  local note="${5:-}"
  CONFIG_PATH="$CONFIG_FILE" INIT_READY_STATE_VALUE="$state" INIT_READY_SCHEDULED_FOR_VALUE="$scheduled_for" INIT_READY_VERIFIED_NEXT_RUN_VALUE="$verified_next_run" INIT_READY_JOB_ID_VALUE="$job_id" INIT_READY_NOTE_VALUE="$note" python3 <<'PY'
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
state = (os.environ.get("INIT_READY_STATE_VALUE") or "scheduled").strip() or "scheduled"
scheduled_for = (os.environ.get("INIT_READY_SCHEDULED_FOR_VALUE") or "").strip()
verified_next_run = (os.environ.get("INIT_READY_VERIFIED_NEXT_RUN_VALUE") or "").strip()
job_id = (os.environ.get("INIT_READY_JOB_ID_VALUE") or "").strip()
note = (os.environ.get("INIT_READY_NOTE_VALUE") or "").strip()

init_ready["state"] = state
init_ready["updated_at"] = now
if scheduled_for:
    init_ready["scheduled_for"] = scheduled_for
if verified_next_run:
    init_ready["last_verified_next_run"] = verified_next_run
if job_id:
    init_ready["job_id"] = job_id
if note:
    init_ready["schedule_note"] = note
if state == "scheduled":
    init_ready.pop("last_error", None)
elif note:
    init_ready["last_error"] = note
config["init_ready"] = init_ready
config_path.write_text(json.dumps(config, indent=2, ensure_ascii=False), encoding="utf-8")
PY
}

ensure_init_ready_job_registered() {
  local requested_delay_minutes="$1"
  local init_ready_suffix="$2"
  local attempt=0
  local effective_delay="$requested_delay_minutes"
  local job_id next_run status validation validation_status validation_detail schedule cron_expr schedule_time shift_minutes

  while [ "$attempt" -lt "$INIT_READY_VERIFY_ATTEMPTS" ]; do
    mapfile -t JOB_SNAPSHOT < <(read_job_snapshot_by_name "$INIT_READY_JOB_NAME")
    job_id="${JOB_SNAPSHOT[0]:-}"
    next_run="${JOB_SNAPSHOT[1]:-}"
    status="${JOB_SNAPSHOT[2]:-}"
    validation=$(validate_init_ready_next_run "$next_run")
    validation_status="${validation%%|*}"
    validation_detail="${validation#*|}"
    if [ -n "$job_id" ] && [ "$validation_status" = "ok" ]; then
      update_init_ready_schedule_state "scheduled" "$INIT_READY_EFFECTIVE_TIME" "$validation_detail" "$job_id" "cron_verified:${status:-unknown}"
      info "init-ready 已确认排入计划：${validation_detail}"
      return 0
    fi

    attempt=$((attempt + 1))
    if [ "$attempt" -ge "$INIT_READY_VERIFY_ATTEMPTS" ]; then
      break
    fi

    warn "init-ready 校验未通过（${validation_detail:-nextRun 为空}），顺延后重排..."
    effective_delay=$((requested_delay_minutes + attempt * INIT_READY_MIN_LEAD_MINUTES))
    remove_job_by_name "$INIT_READY_JOB_NAME"
    register_init_ready_job "$effective_delay" "${WECOM_USER_ID:-}" "$PUSH_SCRIPT" "$init_ready_suffix"
  done

  update_init_ready_schedule_state "schedule_failed" "$INIT_READY_EFFECTIVE_TIME" "" "$job_id" "init-ready nextRun 校验失败"
  error "init-ready 单次任务校验失败，请稍后重新执行 setup-cron.sh"
}

register_all_jobs() {
  local morning_cron discovery_cron evening_cron
  morning_cron=$(parse_time "$MORNING_TIME")
  discovery_cron=$(parse_time "$DISCOVERY_TIME")
  evening_cron=$(parse_time "$EVENING_TIME")
  INIT_READY_EFFECTIVE_TIME=""
  INIT_READY_EFFECTIVE_SHIFT="0"

  echo ""
  echo "🦞 虾说 — 注册定时推送"
  echo ""
  echo "  早安时间: ${MORNING_TIME} (cron: ${morning_cron})"
  echo "  晚间 roundup: ${DISCOVERY_TIME} (cron: ${discovery_cron})"
  echo "  晚安时间: ${EVENING_TIME} (cron: ${evening_cron})"
  echo "  delivery family: ${DELIVERY_FAMILY}"
  echo "  delivery adapter: ${OUTBOUND_ADAPTER}"
  if [ -n "$BINDING_CHANNEL" ] && [ -n "$BINDING_TARGET" ]; then
    echo "  当前绑定: ${BINDING_CHANNEL} → ${BINDING_TARGET} (${BINDING_MODE})"
  fi
  if [ -n "$DELIVERY_CHANNEL" ] && [ -n "$DELIVERY_TARGET" ]; then
    echo "  主动投递: ${DELIVERY_CHANNEL} → ${DELIVERY_TARGET}"
  else
    echo "  主动投递: 将由 adapter=${OUTBOUND_ADAPTER} 决定"
  fi
  echo ""

  step "清理旧的定时任务..."
  remove_all_managed_jobs

  local init_ready_suffix=" --job-kind init-ready --managed-job-name ${INIT_READY_JOB_NAME}"

  if [ "$OUTBOUND_ADAPTER" = "wecom-direct-message" ] && [ -n "$WECOM_USER_ID" ]; then
    # ─────────────────────────────────────────
    #  企微通道：agent prompt = --emit-message-text + message 工具
    # ─────────────────────────────────────────
    register_wecom_job "lobster-says-morning" "$morning_cron" "morning" "$WECOM_USER_ID"
    register_wecom_job "lobster-says-discovery" "$discovery_cron" "discovery" "$WECOM_USER_ID"
    register_wecom_job "lobster-says-evening" "$evening_cron" "evening" "$WECOM_USER_ID"

    register_wecom_job "lobster-says-sticker" "30 15 * * 3,6" "sticker" "$WECOM_USER_ID"
    register_wecom_job "lobster-says-wallpaper" "0 16 * * 0" "wallpaper" "$WECOM_USER_ID"

    register_init_ready_job "$INIT_READY_DELAY_MINUTES" "$WECOM_USER_ID" "$PUSH_SCRIPT" "$init_ready_suffix"
  else
    # ─────────────────────────────────────────
    #  通用通道（Telegram等）：脚本完整模式 + delivery 兜底
    # ─────────────────────────────────────────
    register_general_job "lobster-says-morning" "$morning_cron" "morning" "$DELIVERY_CHANNEL" "$DELIVERY_TARGET"
    register_general_job "lobster-says-discovery" "$discovery_cron" "discovery" "$DELIVERY_CHANNEL" "$DELIVERY_TARGET"
    register_general_job "lobster-says-evening" "$evening_cron" "evening" "$DELIVERY_CHANNEL" "$DELIVERY_TARGET"

    register_general_job "lobster-says-sticker" "30 15 * * 3,6" "sticker" "$DELIVERY_CHANNEL" "$DELIVERY_TARGET"
    register_general_job "lobster-says-wallpaper" "0 16 * * 0" "wallpaper" "$DELIVERY_CHANNEL" "$DELIVERY_TARGET"

    register_init_ready_job "$INIT_READY_DELAY_MINUTES" "" "$PUSH_SCRIPT" "$init_ready_suffix"
  fi

  if [ "$MEMORY_MODE" != "lightweight" ]; then
    local digest_message="请执行以下命令来消化用户的对话记录：
bash \"${BASE_DIR}/digest-transcript.sh\" --mode ${MEMORY_MODE}
执行完毕后，简要报告结果。"
    local digest_cron_args=(
      --name "lobster-says-digest"
      --cron "0 3,9,15,21 * * *"
      --tz "Asia/Shanghai"
      --session isolated
    )
    if [ -n "$DELIVERY_CHANNEL" ] && [ -n "$DELIVERY_TARGET" ]; then
      digest_cron_args+=(--channel "$DELIVERY_CHANNEL" --to "$DELIVERY_TARGET")
    fi
    digest_cron_args+=("${OPENCLAW_CRON_ARGS[@]}" --message "$digest_message")
    step "注册 lobster-says-digest..."
    if openclaw cron add "${digest_cron_args[@]}" >/dev/null; then
      info "lobster-says-digest 注册成功"
    else
      warn "lobster-says-digest 注册失败（不影响主推送）"
    fi
  else
    info "轻量陪伴模式：不注册 transcript digest cron"
  fi

  lobster_update_cron_registration "$CONFIG_FILE" "registered" "cron reconcile completed" "$MORNING_TIME" "$DISCOVERY_TIME" "$EVENING_TIME" "$MEMORY_MODE" '["lobster-says-morning","lobster-says-discovery","lobster-says-evening","lobster-says-init-ready","lobster-says-sticker","lobster-says-wallpaper","lobster-says-digest"]' >/dev/null

  echo ""
  info "定时推送注册完成！"
  echo ""
  echo "  🌅 早安推送: 每天 ${MORNING_TIME}"
  echo "  📰 晚间 roundup: 每天 ${DISCOVERY_TIME}"
  echo "  🌙 晚安推送: 每天 ${EVENING_TIME}"
  if [ "$INIT_READY_EFFECTIVE_SHIFT" -gt 0 ] 2>/dev/null; then
    echo "  👋 初始化问候: ${INIT_READY_EFFECTIVE_TIME:-${INIT_READY_DELAY_MINUTES}分钟后}（一次性 at 调度）"
  else
    echo "  👋 初始化问候: ${INIT_READY_EFFECTIVE_TIME:-${INIT_READY_DELAY_MINUTES}分钟后}（一次性 at 调度）"
  fi
  echo "  🎨 表情包: 每周三/六 15:30"
  echo "  🖼️ 壁纸: 每周日 16:00"
  if [ "$MEMORY_MODE" = "lightweight" ]; then
    echo "  🧠 Transcript digest: 已关闭"
  else
    echo "  🧠 Transcript digest: 每 6 小时一次（模式: ${MEMORY_MODE}）"
  fi
  if [ "$OUTBOUND_ADAPTER" = "wecom-direct-message" ]; then
    echo ""
    echo "  📲 企微推送模式: emit-message-text + agent message 工具直达"
    echo "  📲 所有企微 cron 均带 --channel openclaw-wecom-bot --to ${WECOM_USER_ID} 作为 delivery 兜底"
  else
    echo ""
    echo "  📲 通用推送模式: 脚本多通道 fallback + delivery 兜底"
  fi
}

schedule_init_ready_retry_job() {
  local delay_minutes="$1"
  if [ "$DELIVERY_READY" != "1" ]; then
    error "主动推送能力未就绪，无法重排 init-ready：${DELIVERY_REASON}"
  fi
  local init_ready_suffix=" --job-kind init-ready --managed-job-name ${INIT_READY_JOB_NAME}"
  step "重排 init-ready 单次任务..."
  remove_job_by_name "$INIT_READY_JOB_NAME"
  register_init_ready_job "$delay_minutes" "${WECOM_USER_ID:-}" "$PUSH_SCRIPT" "$init_ready_suffix"
  info "init-ready 已重排（${delay_minutes} 分钟后触发）"
}

if [ -z "$MORNING_TIME" ]; then
  MORNING_TIME=$(read_config_value "morning_time" "09:00")
fi
if [ -z "$DISCOVERY_TIME" ]; then
  DISCOVERY_TIME=$(read_config_value "discovery_time" "21:30")
fi
if [ -z "$EVENING_TIME" ]; then
  EVENING_TIME=$(read_config_value "evening_time" "21:00")
fi
if [ -z "$MEMORY_MODE" ]; then
  MEMORY_MODE=$(read_config_value "memory_mode" "smart")
fi
if [ -z "$CHANNEL" ]; then
  CHANNEL=$(read_config_value "binding_channel" "")
fi
if [ -z "$TO" ]; then
  TO=$(read_config_value "binding_target" "")
fi
if [ -z "$CHANNEL" ]; then
  CHANNEL=$(read_config_value "channel" "")
fi
if [ -z "$TO" ]; then
  TO=$(read_config_value "chat_id" "")
fi
if [ -z "$WECOM_USER_ID" ]; then
  WECOM_USER_ID=$(read_config_value "wecom_user_id" "")
fi

case "$MEMORY_MODE" in
  lightweight|smart|deep) ;;
  *) error "memory_mode 必须是 lightweight / smart / deep" ;;
esac

load_gateway_auth
if [ ${#OPENCLAW_CRON_ARGS[@]} -gt 0 ]; then
  info "检测到 gateway token 环境变量：cron 命令将自动携带 token"
fi

if [ "$ACTION" = "remove-job-by-name" ]; then
  step "按名称移除任务..."
  remove_job_by_name "$REMOVE_JOB_NAME"
  exit 0
fi

step "扫描最近活跃的通道（用于 fallback 与待激活补注册）..."
SESSIONS_JSON=$(openclaw sessions --json --active "$ACTIVE_WINDOW_MINUTES" 2>/dev/null || echo "[]")
DETECTED=$(SESSIONS_JSON="$SESSIONS_JSON" python3 <<'PY'
import json
import os

try:
    sessions = json.loads(os.environ.get("SESSIONS_JSON", "[]"))
    if not isinstance(sessions, list):
        sessions = [sessions]
except Exception:
    sessions = []

ordered = []
seen = set()

def add(channel, peer_id):
    channel = (channel or "").strip()
    peer_id = (peer_id or "").strip()
    if not channel or channel == "unknown" or not peer_id:
        return
    key = (channel, peer_id)
    if key in seen:
        return
    seen.add(key)
    ordered.append({"channel": channel, "peer_id": peer_id})

for session in sessions:
    direct_channel = session.get("channel") or session.get("platform") or session.get("imChannel") or ""
    direct_target = session.get("peer_id") or session.get("peerId") or session.get("target") or session.get("chat_id") or session.get("chatId") or ""
    if direct_channel and direct_target:
        add(direct_channel, direct_target)
        continue

    key = session.get("sessionKey") or session.get("key") or session.get("id") or ""
    if not key:
        continue
    parts = key.split(":")
    if not parts or parts[0].lower() in ("cron", "hook"):
        continue
    if len(parts) <= 3 and parts[-1].lower() == "main":
        continue
    if len(parts) >= 5 and parts[0].lower() == "agent":
        channel = parts[2]
        marker = parts[3].lower()
        if marker in ("direct", "dm"):
            add(channel, parts[4])

best = ordered[0] if ordered else {"channel": "", "peer_id": ""}
print(f"{best['channel']}|{best['peer_id']}")
print(json.dumps(ordered, ensure_ascii=False))
PY
)

DETECTED_TARGET=$(echo "$DETECTED" | head -1)
DETECTED_CHANNEL=$(echo "$DETECTED_TARGET" | cut -d'|' -f1)
DETECTED_TO=$(echo "$DETECTED_TARGET" | cut -d'|' -f2)
DETECTED_KNOWN_JSON=$(echo "$DETECTED" | tail -1)

if [ -z "$CHANNEL" ] && [ -n "$DETECTED_CHANNEL" ]; then
  CHANNEL="$DETECTED_CHANNEL"
fi
if [ -z "$TO" ] && [ -n "$DETECTED_TO" ]; then
  TO="$DETECTED_TO"
fi

step "更新本地配置..."
persist_local_config "$DETECTED_KNOWN_JSON" "$CHANNEL" "$TO" "$WECOM_USER_ID"

step "同步 delivery contract..."
sync_delivery_contract "$CHANNEL" "$TO"
apply_wecom_direct_delivery_override
info "binding: ${BINDING_CHANNEL:-未锁定} → ${BINDING_TARGET:-未锁定} (${BINDING_MODE})"
if [ "$DELIVERY_READY" = "1" ]; then
  if [ "$OUTBOUND_ADAPTER" = "wecom-direct-message" ]; then
    info "delivery: wecom → ${DELIVERY_TARGET:-未设置}（adapter=wecom-direct-message，sender_id 直达私聊）"
  else
    info "delivery: ${DELIVERY_CHANNEL:-adapter} → ${DELIVERY_TARGET:-target}（adapter=${OUTBOUND_ADAPTER}）"
  fi
else
  warn "delivery contract 待激活：${DELIVERY_REASON}"
fi

if [ "$ACTION" = "schedule-init-ready-delay" ]; then
  schedule_init_ready_retry_job "$SCHEDULE_INIT_READY_DELAY"
  exit 0
fi

if [ "$DELIVERY_READY" != "1" ]; then
  step "主动推送能力未就绪，暂不注册 cron..."
  remove_all_managed_jobs
  lobster_update_cron_registration "$CONFIG_FILE" "pending_activation" "$DELIVERY_REASON" "$MORNING_TIME" "$DISCOVERY_TIME" "$EVENING_TIME" "$MEMORY_MODE" '[]' >/dev/null
  echo ""
  warn "已保存待激活的定时推送配置，当前不会误注册 cron。"
  echo "  - delivery family: ${DELIVERY_FAMILY}"
  echo "  - 原因: ${DELIVERY_REASON}"
  echo "  - 一旦补齐主动推送能力，再次执行 setup-cron.sh 即会完成补注册。"
  exit 0
fi

register_all_jobs
