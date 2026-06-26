#!/bin/bash
# 共享运行时辅助函数：候选通道构建、绑定策略判断、delivery contract 持久化、cron 状态收口。

lobster_detect_binding_mode() {
  local channel
  channel=$(printf '%s' "${1:-}" | tr '[:upper:]' '[:lower:]')
  case "$channel" in
    wecom*|*wecom*|wxwork*|qywx*|enterprisewechat*|enterprise-wechat*|workwechat*|wecom-bot*)
      echo "strict"
      ;;
    *)
      echo "prefer"
      ;;
  esac
}

lobster_runtime_policy_json() {
  local config_path="$1"
  CONFIG_PATH="$config_path" python3 <<'PY'
import json
import os
from pathlib import Path

STRICT_MARKERS = (
    "wecom",
    "wecom-bot",
    "wxwork",
    "qywx",
    "enterprisewechat",
    "enterprise-wechat",
    "workwechat",
)
BOT_MARKERS = (
    "wecom-bot",
    "qywx-bot",
    "wxwork-bot",
    "enterprisewechat-bot",
    "enterprise-wechat-bot",
    "workwechat-bot",
)


def detect_mode(channel: str) -> str:
    normalized = (channel or "").strip().lower()
    if any(marker in normalized for marker in STRICT_MARKERS):
        return "strict"
    return "prefer"


def is_wecom_family(channel: str) -> bool:
    return detect_mode(channel) == "strict"


def supports_openclaw_proactive(channel: str) -> bool:
    normalized = (channel or "").strip().lower()
    return any(marker in normalized for marker in BOT_MARKERS)


def default_adapter_for_binding(channel: str, current: str = "") -> str:
    normalized = (current or "").strip().lower()
    if normalized in {"openclaw", "wecom-webhook", "wecom-mcp"}:
        return normalized
    if is_wecom_family(channel):
        return "wecom-mcp"
    return "openclaw"


path = Path(os.environ["CONFIG_PATH"])
try:
    config = json.loads(path.read_text(encoding="utf-8"))
except Exception:
    config = {}

contract = config.get("delivery_contract") if isinstance(config.get("delivery_contract"), dict) else {}
cron_registration = config.get("cron_registration") if isinstance(config.get("cron_registration"), dict) else {}

binding_channel = str(
    contract.get("binding_channel")
    or config.get("binding_channel")
    or config.get("channel")
    or ""
).strip()
binding_target = str(
    contract.get("binding_target")
    or config.get("binding_target")
    or config.get("chat_id")
    or ""
).strip()
binding_mode = str(
    contract.get("binding_mode")
    or config.get("binding_mode")
    or detect_mode(binding_channel)
).strip().lower() or "prefer"
if binding_mode not in {"prefer", "strict"}:
    binding_mode = detect_mode(binding_channel)

outbound_adapter = default_adapter_for_binding(
    binding_channel,
    str(contract.get("outbound_adapter") or config.get("outbound_adapter") or ""),
)

outbound_webhook_url = str(
    contract.get("outbound_webhook_url")
    or config.get("outbound_webhook_url")
    or ""
).strip()
outbound_webhook_secret = str(
    contract.get("outbound_webhook_secret")
    or config.get("outbound_webhook_secret")
    or ""
).strip()
delivery_channel = str(
    contract.get("delivery_channel")
    or config.get("delivery_channel")
    or ""
).strip()
delivery_target = str(
    contract.get("delivery_target")
    or config.get("delivery_target")
    or ""
).strip()

strict_binding = binding_mode == "strict"
delivery_family = "wecom" if strict_binding or is_wecom_family(binding_channel) else "general"
delivery_ready = False
delivery_reason = ""

if delivery_family == "general":
    if not delivery_channel:
        delivery_channel = binding_channel
    if not delivery_target:
        delivery_target = binding_target
    delivery_ready = bool(delivery_channel and delivery_target)
    if not delivery_ready:
        delivery_reason = "缺少投递目标"
else:
    if outbound_adapter == "wecom-webhook":
        if not delivery_channel:
            delivery_channel = "wecom-webhook"
        if not delivery_target:
            delivery_target = binding_target or "webhook"
        delivery_ready = bool(outbound_webhook_url)
        if not delivery_ready:
            delivery_reason = "企业微信 webhook 未配置"
    elif outbound_adapter == "wecom-mcp":
        if not delivery_channel or delivery_channel == "wecom-mcp":
            delivery_channel = binding_channel
        delivery_target = delivery_target or binding_target
        delivery_ready = bool(delivery_channel and delivery_target)
        if not delivery_ready:
            if not delivery_channel:
                delivery_reason = "企业微信长连接投递缺少 channel"
            else:
                delivery_reason = "企业微信长连接投递缺少 chat_id"
    else:
        proactive_delivery_channel = ""
        proactive_delivery_target = ""
        if supports_openclaw_proactive(delivery_channel):
            proactive_delivery_channel = delivery_channel
            proactive_delivery_target = delivery_target or (binding_target if delivery_channel == binding_channel else "")
        elif supports_openclaw_proactive(binding_channel):
            proactive_delivery_channel = binding_channel
            proactive_delivery_target = delivery_target or binding_target

        if proactive_delivery_channel:
            delivery_channel = proactive_delivery_channel
            delivery_target = proactive_delivery_target
            delivery_ready = bool(delivery_channel and delivery_target)
            if not delivery_ready:
                delivery_reason = "企业微信机器人缺少 delivery_target"
        else:
            delivery_channel = ""
            delivery_target = ""
            if not binding_channel or not binding_target:
                delivery_reason = "企业微信严格绑定缺少 binding_channel / binding_target"
            else:
                delivery_reason = "企业微信 strict family 缺少可用的主动推送配置；推荐在技能层从 inbound metadata 读取 sender_id 并传给 --wecom-user-id"

payload = {
    "binding_channel": binding_channel,
    "binding_target": binding_target,
    "binding_mode": binding_mode,
    "strict_binding": strict_binding,
    "channel": str(config.get("channel") or "").strip(),
    "chat_id": str(config.get("chat_id") or "").strip(),
    "outbound_adapter": outbound_adapter,
    "outbound_webhook_url": outbound_webhook_url,
    "outbound_webhook_secret": outbound_webhook_secret,
    "delivery_channel": delivery_channel,
    "delivery_target": delivery_target,
    "delivery_family": delivery_family,
    "delivery_ready": delivery_ready,
    "delivery_reason": delivery_reason,
    "cron_status": str(cron_registration.get("status") or "unregistered").strip() or "unregistered",
    "cron_registered": bool(config.get("cron_registered") or cron_registration.get("registered")),
}
print(json.dumps(payload, ensure_ascii=False))
PY
}

lobster_sync_delivery_contract() {
  local config_path="$1"
  local hinted_channel="${2:-}"
  local hinted_target="${3:-}"
  CONFIG_PATH="$config_path" HINTED_CHANNEL="$hinted_channel" HINTED_TARGET="$hinted_target" python3 <<'PY'
import json
import os
from datetime import datetime, timezone
from pathlib import Path

STRICT_MARKERS = (
    "wecom",
    "wecom-bot",
    "wxwork",
    "qywx",
    "enterprisewechat",
    "enterprise-wechat",
    "workwechat",
)
BOT_MARKERS = (
    "wecom-bot",
    "qywx-bot",
    "wxwork-bot",
    "enterprisewechat-bot",
    "enterprise-wechat-bot",
    "workwechat-bot",
)


def detect_mode(channel: str) -> str:
    normalized = (channel or "").strip().lower()
    if any(marker in normalized for marker in STRICT_MARKERS):
        return "strict"
    return "prefer"


def is_wecom_family(channel: str) -> bool:
    return detect_mode(channel) == "strict"


def supports_openclaw_proactive(channel: str) -> bool:
    normalized = (channel or "").strip().lower()
    return any(marker in normalized for marker in BOT_MARKERS)


def default_adapter_for_binding(channel: str, current: str = "") -> str:
    normalized = (current or "").strip().lower()
    if normalized in {"openclaw", "wecom-webhook", "wecom-mcp"}:
        return normalized
    if is_wecom_family(channel):
        return "wecom-mcp"
    return "openclaw"


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


config_path = Path(os.environ["CONFIG_PATH"])
hinted_channel = (os.environ.get("HINTED_CHANNEL") or "").strip()
hinted_target = (os.environ.get("HINTED_TARGET") or "").strip()
try:
    config = json.loads(config_path.read_text(encoding="utf-8"))
except Exception:
    config = {}

existing_contract = config.get("delivery_contract") if isinstance(config.get("delivery_contract"), dict) else {}

if hinted_channel and hinted_target:
    config["channel"] = hinted_channel
    config["chat_id"] = hinted_target
    config["binding_channel"] = hinted_channel
    config["binding_target"] = hinted_target

binding_channel = str(
    config.get("binding_channel")
    or hinted_channel
    or config.get("channel")
    or existing_contract.get("binding_channel")
    or ""
).strip()
binding_target = str(
    config.get("binding_target")
    or hinted_target
    or config.get("chat_id")
    or existing_contract.get("binding_target")
    or ""
).strip()
binding_mode = str(
    config.get("binding_mode")
    or existing_contract.get("binding_mode")
    or detect_mode(binding_channel)
).strip().lower() or "prefer"
if binding_mode not in {"prefer", "strict"}:
    binding_mode = detect_mode(binding_channel)

outbound_adapter = default_adapter_for_binding(
    binding_channel,
    str(existing_contract.get("outbound_adapter") or config.get("outbound_adapter") or ""),
)

outbound_webhook_url = str(
    existing_contract.get("outbound_webhook_url")
    or config.get("outbound_webhook_url")
    or ""
).strip()
outbound_webhook_secret = str(
    existing_contract.get("outbound_webhook_secret")
    or config.get("outbound_webhook_secret")
    or ""
).strip()

delivery_family = "wecom" if binding_mode == "strict" or is_wecom_family(binding_channel) else "general"
delivery_channel = str(
    existing_contract.get("delivery_channel")
    or config.get("delivery_channel")
    or ""
).strip()
delivery_target = str(
    existing_contract.get("delivery_target")
    or config.get("delivery_target")
    or ""
).strip()
delivery_ready = False
delivery_reason = ""

if delivery_family == "general":
    delivery_channel = hinted_channel or delivery_channel or binding_channel
    delivery_target = hinted_target or delivery_target or binding_target
    delivery_ready = bool(delivery_channel and delivery_target)
    if not delivery_ready:
        delivery_reason = "缺少投递目标"
else:
    if outbound_adapter == "wecom-webhook":
        delivery_channel = "wecom-webhook"
        delivery_target = delivery_target or binding_target or "webhook"
        delivery_ready = bool(outbound_webhook_url)
        if not delivery_ready:
            delivery_reason = "企业微信 webhook 未配置"
    elif outbound_adapter == "wecom-mcp":
        if not delivery_channel or delivery_channel == "wecom-mcp":
            delivery_channel = binding_channel
        delivery_target = delivery_target or binding_target
        delivery_ready = bool(delivery_channel and delivery_target)
        if not delivery_ready:
            if not delivery_channel:
                delivery_reason = "企业微信长连接投递缺少 channel"
            else:
                delivery_reason = "企业微信长连接投递缺少 chat_id"
    else:
        proactive_delivery_channel = ""
        proactive_delivery_target = ""
        if supports_openclaw_proactive(delivery_channel):
            proactive_delivery_channel = delivery_channel
            proactive_delivery_target = delivery_target or (binding_target if delivery_channel == binding_channel else "")
        elif supports_openclaw_proactive(binding_channel):
            proactive_delivery_channel = binding_channel
            proactive_delivery_target = delivery_target or binding_target

        if proactive_delivery_channel:
            delivery_channel = proactive_delivery_channel
            delivery_target = proactive_delivery_target
            delivery_ready = bool(delivery_channel and delivery_target)
            if not delivery_ready:
                delivery_reason = "企业微信机器人缺少 delivery_target"
        else:
            delivery_channel = ""
            delivery_target = ""
            if not binding_channel or not binding_target:
                delivery_reason = "企业微信严格绑定缺少 binding_channel / binding_target"
            else:
                delivery_reason = "企业微信 strict family 缺少可用的主动推送配置；推荐在技能层从 inbound metadata 读取 sender_id 并传给 --wecom-user-id"

contract = {
    "binding_channel": binding_channel,
    "binding_target": binding_target,
    "binding_mode": binding_mode,
    "strict_binding": binding_mode == "strict",
    "delivery_family": delivery_family,
    "outbound_adapter": outbound_adapter,
    "outbound_webhook_url": outbound_webhook_url,
    "outbound_webhook_secret": outbound_webhook_secret,
    "delivery_channel": delivery_channel,
    "delivery_target": delivery_target,
    "delivery_ready": delivery_ready,
    "delivery_reason": delivery_reason,
    "updated_at": now_iso(),
}

config["binding_channel"] = binding_channel
config["binding_target"] = binding_target
config["binding_mode"] = binding_mode
config["outbound_adapter"] = outbound_adapter
if outbound_webhook_url:
    config["outbound_webhook_url"] = outbound_webhook_url
if outbound_webhook_secret:
    config["outbound_webhook_secret"] = outbound_webhook_secret
elif not outbound_webhook_url:
    config.pop("outbound_webhook_secret", None)
if hinted_channel and hinted_target:
    config["channel"] = hinted_channel
    config["chat_id"] = hinted_target
elif binding_channel and binding_target:
    config.setdefault("channel", binding_channel)
    config.setdefault("chat_id", binding_target)
if delivery_channel and delivery_target:
    config["delivery_channel"] = delivery_channel
    config["delivery_target"] = delivery_target
else:
    config.pop("delivery_channel", None)
    config.pop("delivery_target", None)
config["delivery_contract"] = contract
config_path.write_text(json.dumps(config, indent=2, ensure_ascii=False), encoding="utf-8")
print(json.dumps(contract, ensure_ascii=False))
PY
}

lobster_update_cron_registration() {
  local config_path="$1"
  local status="$2"
  local reason="${3:-}"
  local morning_time="${4:-}"
  local discovery_time="${5:-}"
  local evening_time="${6:-}"
  local memory_mode="${7:-}"
  local managed_jobs_json="${8:-[]}"
  CONFIG_PATH="$config_path" \
  CRON_STATUS_VALUE="$status" \
  CRON_REASON_VALUE="$reason" \
  MORNING_TIME_VALUE="$morning_time" \
  DISCOVERY_TIME_VALUE="$discovery_time" \
  EVENING_TIME_VALUE="$evening_time" \
  MEMORY_MODE_VALUE="$memory_mode" \
  MANAGED_JOBS_JSON_VALUE="$managed_jobs_json" \
  python3 <<'PY'
import json
import os
from datetime import datetime, timezone
from pathlib import Path


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


config_path = Path(os.environ["CONFIG_PATH"])
try:
    config = json.loads(config_path.read_text(encoding="utf-8"))
except Exception:
    config = {}

status = (os.environ.get("CRON_STATUS_VALUE") or "unregistered").strip() or "unregistered"
reason = (os.environ.get("CRON_REASON_VALUE") or "").strip()
registered = status == "registered"
cron_registration = config.get("cron_registration") if isinstance(config.get("cron_registration"), dict) else {}
cron_registration["status"] = status
cron_registration["registered"] = registered
cron_registration["ready"] = registered
cron_registration["updated_at"] = now_iso()
if reason:
    cron_registration["reason"] = reason
else:
    cron_registration.pop("reason", None)
if registered:
    cron_registration["last_registered_at"] = cron_registration["updated_at"]

try:
    managed_jobs = json.loads(os.environ.get("MANAGED_JOBS_JSON_VALUE") or "[]")
    if not isinstance(managed_jobs, list):
        managed_jobs = []
except Exception:
    managed_jobs = []
cron_registration["managed_job_names"] = [str(item).strip() for item in managed_jobs if str(item).strip()]
cron_registration["desired_schedule"] = {
    "morning_time": (os.environ.get("MORNING_TIME_VALUE") or "").strip(),
    "discovery_time": (os.environ.get("DISCOVERY_TIME_VALUE") or "").strip(),
    "evening_time": (os.environ.get("EVENING_TIME_VALUE") or "").strip(),
    "memory_mode": (os.environ.get("MEMORY_MODE_VALUE") or "").strip(),
}
config["cron_registration"] = cron_registration
config["cron_registered"] = registered
config_path.write_text(json.dumps(config, indent=2, ensure_ascii=False), encoding="utf-8")
print(json.dumps(cron_registration, ensure_ascii=False))
PY
}

build_candidate_lines_with_policy() {
  local config_path="$1"
  local sessions_json="$2"
  local forced_channel="$3"
  local forced_target="$4"
  CONFIG_PATH="$config_path" \
  SESSIONS_JSON="$sessions_json" \
  FORCED_CHANNEL="$forced_channel" \
  FORCED_TARGET="$forced_target" \
  python3 <<'PY'
import json
import os
from pathlib import Path

STRICT_MARKERS = (
    "wecom",
    "wecom-bot",
    "wxwork",
    "qywx",
    "enterprisewechat",
    "enterprise-wechat",
    "workwechat",
)


def detect_mode(channel: str) -> str:
    normalized = (channel or "").strip().lower()
    if any(marker in normalized for marker in STRICT_MARKERS):
        return "strict"
    return "prefer"


config_path = Path(os.environ["CONFIG_PATH"])
raw_sessions = os.environ.get("SESSIONS_JSON", "[]")
forced_channel = (os.environ.get("FORCED_CHANNEL") or "").strip()
forced_target = (os.environ.get("FORCED_TARGET") or "").strip()

try:
    sessions = json.loads(raw_sessions)
    if not isinstance(sessions, list):
        sessions = [sessions]
except Exception:
    sessions = []

try:
    config = json.loads(config_path.read_text(encoding="utf-8"))
except Exception:
    config = {}

contract = config.get("delivery_contract") if isinstance(config.get("delivery_contract"), dict) else {}
ordered = []
seen = set()


def add(channel, peer_id):
    channel = (channel or "").strip()
    peer_id = (peer_id or "").strip()
    if not channel or not peer_id or channel == "unknown":
        return
    key = (channel, peer_id)
    if key in seen:
        return
    seen.add(key)
    ordered.append({"channel": channel, "peer_id": peer_id})


binding_channel = str(contract.get("binding_channel") or config.get("binding_channel") or config.get("channel") or "").strip()
binding_target = str(contract.get("binding_target") or config.get("binding_target") or config.get("chat_id") or "").strip()
binding_mode = str(contract.get("binding_mode") or config.get("binding_mode") or detect_mode(binding_channel)).strip().lower() or "prefer"
strict_binding = binding_mode == "strict"
delivery_channel = str(contract.get("delivery_channel") or config.get("delivery_channel") or "").strip()
delivery_target = str(contract.get("delivery_target") or config.get("delivery_target") or "").strip()

if forced_channel and forced_target:
    add(forced_channel, forced_target)

if strict_binding:
    add(delivery_channel or binding_channel, delivery_target or binding_target)
else:
    add(delivery_channel or binding_channel, delivery_target or binding_target)
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
        if not parts:
            continue
        if parts[0].lower() in ("cron", "hook"):
            continue
        if len(parts) <= 3 and parts[-1].lower() == "main":
            continue
        if len(parts) >= 5 and parts[0].lower() == "agent":
            channel = parts[2]
            marker = parts[3].lower()
            if marker in ("direct", "dm"):
                add(channel, parts[4])

    for item in config.get("known_channels", []):
        if isinstance(item, dict):
            add(item.get("channel"), item.get("peer_id"))
    add(config.get("channel"), config.get("chat_id"))

for item in ordered:
    print(f"{item['channel']}|{item['peer_id']}")
PY
}

update_config_after_send_with_policy() {
  local config_path="$1"
  local current_channel="$2"
  local current_target="$3"
  local candidate_lines="$4"
  local delivered_at="$5"
  CONFIG_PATH="$config_path" \
  CURRENT_CHANNEL="$current_channel" \
  CURRENT_TARGET="$current_target" \
  CANDIDATE_LINES="$candidate_lines" \
  DELIVERED_AT="$delivered_at" \
  python3 <<'PY'
import json
import os
from pathlib import Path

STRICT_MARKERS = (
    "wecom",
    "wecom-bot",
    "wxwork",
    "qywx",
    "enterprisewechat",
    "enterprise-wechat",
    "workwechat",
)


def detect_mode(channel: str) -> str:
    normalized = (channel or "").strip().lower()
    if any(marker in normalized for marker in STRICT_MARKERS):
        return "strict"
    return "prefer"


config_path = Path(os.environ["CONFIG_PATH"])
current_channel = os.environ.get("CURRENT_CHANNEL", "").strip()
current_target = os.environ.get("CURRENT_TARGET", "").strip()
lines = [line.strip() for line in os.environ.get("CANDIDATE_LINES", "").splitlines() if line.strip()]
delivered_at = os.environ.get("DELIVERED_AT", "").strip()

try:
    config = json.loads(config_path.read_text(encoding="utf-8"))
except Exception:
    config = {}

contract = config.get("delivery_contract") if isinstance(config.get("delivery_contract"), dict) else {}
binding_channel = str(contract.get("binding_channel") or config.get("binding_channel") or config.get("channel") or "").strip()
binding_target = str(contract.get("binding_target") or config.get("binding_target") or config.get("chat_id") or "").strip()
binding_mode = str(contract.get("binding_mode") or config.get("binding_mode") or detect_mode(binding_channel)).strip().lower() or "prefer"
strict_binding = binding_mode == "strict"

ordered = []
seen = set()


def add(channel, peer_id):
    channel = (channel or "").strip()
    peer_id = (peer_id or "").strip()
    if not channel or not peer_id:
        return
    key = (channel, peer_id)
    if key in seen:
        return
    seen.add(key)
    ordered.append({"channel": channel, "peer_id": peer_id})


add(current_channel, current_target)
if binding_channel and binding_target:
    add(binding_channel, binding_target)
for line in lines:
    channel, _, peer_id = line.partition("|")
    add(channel, peer_id)
for item in config.get("known_channels", []):
    if isinstance(item, dict):
        add(item.get("channel"), item.get("peer_id"))

if strict_binding and binding_channel and binding_target:
    config["channel"] = binding_channel
    config["chat_id"] = binding_target
    config["binding_channel"] = binding_channel
    config["binding_target"] = binding_target
else:
    if current_channel and current_target:
        config["channel"] = current_channel
        config["chat_id"] = current_target
        config["binding_channel"] = current_channel
        config["binding_target"] = current_target

config["binding_mode"] = binding_mode
config["known_channels"] = ordered
if current_channel and current_target:
    config["last_delivery_channel"] = current_channel
    config["last_delivery_target"] = current_target
if delivered_at:
    config["last_delivery_at"] = delivered_at

contract["binding_channel"] = str(config.get("binding_channel") or binding_channel or "").strip()
contract["binding_target"] = str(config.get("binding_target") or binding_target or "").strip()
contract["binding_mode"] = binding_mode
if current_channel and current_target:
    contract["delivery_channel"] = current_channel
    contract["delivery_target"] = current_target
config["delivery_contract"] = contract
config_path.write_text(json.dumps(config, indent=2, ensure_ascii=False), encoding="utf-8")
print(json.dumps(config.get("known_channels", []), ensure_ascii=False))
PY
}
