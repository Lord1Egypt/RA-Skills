#!/bin/bash
# 虾说 — 一体化初始化脚本
#
# 数据访问声明：
# - 读写 .lobster-config（技能自身配置）
# - 调用 openclaw sessions --json 获取活跃 IM 通道元数据
# - 与 https://nixiashuo.com 通信：创建/验证虾、获取工作室链接
# - 调用 setup-cron.sh 注册定时推送
# - 不读取 openclaw.json 配置文件，不提取 gateway token

set -e

PERSONALITY="warm"
NICKNAME="打工人"
NICKNAME_EXPLICIT=0
LOBSTER_NAME=""
LOBSTER_NAME_EXPLICIT=0
MORNING_TIME="09:00"
DISCOVERY_TIME="21:30"
EVENING_TIME="21:00"
MEMORY_MODE="smart"
CHANNEL=""
TO=""
WECOM_USER_ID=""
ALL_CHANNELS_JSON="[]"
BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
CONFIG_FILE="${BASE_DIR}/.lobster-config"
COMMON_SCRIPT="${BASE_DIR}/runtime-common.sh"
LOG_DIR="${BASE_DIR}/logs"
RUN_TS="$(date +%Y%m%d-%H%M%S)"
LOG_FILE="${LOG_DIR}/init-lobster-${RUN_TS}.log"
API_BASE="${LOBSTER_API_BASE:-https://nixiashuo.com}"
WEB_BASE="${LOBSTER_WEB_BASE_URL:-${LOBSTER_API_BASE:-https://nixiashuo.com}}"
ACTIVE_WINDOW_MINUTES="${ACTIVE_WINDOW_MINUTES:-10080}"

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

mkdir -p "$LOG_DIR"
if command -v tee >/dev/null 2>&1; then
  exec > >(tee -a "$LOG_FILE") 2>&1
else
  exec >>"$LOG_FILE" 2>&1
fi

echo "[log] init-lobster started at $(date '+%F %T')"
echo "[log] file: ${LOG_FILE}"

after_exit() {
  local exit_code=$?
  if [ "$exit_code" -ne 0 ]; then
    echo ""
    echo "[log] init-lobster failed at step: ${CURRENT_STEP} (exit=${exit_code})"
    echo "[log] inspect: ${LOG_FILE}"
  else
    echo "[log] init-lobster finished successfully"
  fi
}
trap after_exit EXIT

while [[ $# -gt 0 ]]; do
  case "$1" in
    --personality) PERSONALITY="$2"; shift 2 ;;
    --nickname) error "参数 --nickname 已废弃，请改用 --owner-nickname 来表示虾对用户的称呼" ;;
    --owner-nickname|--user-nickname) NICKNAME="$2"; NICKNAME_EXPLICIT=1; shift 2 ;;
    --name|--lobster-name) LOBSTER_NAME="$2"; LOBSTER_NAME_EXPLICIT=1; shift 2 ;;
    --morning) MORNING_TIME="$2"; shift 2 ;;
    --discovery) DISCOVERY_TIME="$2"; shift 2 ;;
    --evening) EVENING_TIME="$2"; shift 2 ;;
    --memory-mode) MEMORY_MODE="$2"; shift 2 ;;
    --privacy-mode) MEMORY_MODE="smart"; shift ;;
    --channel) CHANNEL="$2"; shift 2 ;;
    --to) TO="$2"; shift 2 ;;
    --wecom-user-id) WECOM_USER_ID="$2"; shift 2 ;;
    *) echo "未知参数: $1"; exit 1 ;;
  esac
done

case "$MEMORY_MODE" in
  lightweight|smart|deep) ;;
  *) error "memory_mode 必须是 lightweight / smart / deep" ;;
esac

for cmd in python3 curl openclaw; do
  if ! command -v "$cmd" >/dev/null 2>&1; then
    error "$cmd 不可用"
  fi
done

if [ ! -f "$COMMON_SCRIPT" ]; then
  error "共享运行时脚本不存在：${COMMON_SCRIPT}"
fi
. "$COMMON_SCRIPT"

if [ -z "$CHANNEL" ] || [ -z "$TO" ]; then
  step "自动检测最近使用的通道..."
  SESSIONS_JSON=$(openclaw sessions --json --active "$ACTIVE_WINDOW_MINUTES" 2>/dev/null || echo "[]")
  DETECTED=$(SESSIONS_JSON="$SESSIONS_JSON" python3 <<'PY'
import json
import os
import sys

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

if not ordered:
    sys.exit(1)

best = ordered[0]
print(f"{best['channel']}|{best['peer_id']}")
print(json.dumps(ordered, ensure_ascii=False))
PY
  ) || true

  if [ -n "$DETECTED" ]; then
    BEST_LINE=$(echo "$DETECTED" | head -1)
    AUTO_CHANNEL=$(echo "$BEST_LINE" | cut -d'|' -f1)
    AUTO_TO=$(echo "$BEST_LINE" | cut -d'|' -f2)
    ALL_CHANNELS_JSON=$(echo "$DETECTED" | tail -1)
    if [ -z "$CHANNEL" ]; then
      CHANNEL="$AUTO_CHANNEL"
    fi
    if [ -z "$TO" ]; then
      TO="$AUTO_TO"
    fi
    info "自动检测到: ${CHANNEL} → ${TO}"
  fi
fi

if [ -z "$CHANNEL" ] || [ -z "$TO" ]; then
  error "无法自动检测投递目标。请手动指定 --channel <渠道名> --to <chatId/peerId>"
fi

echo ""
echo "🦞 虾说 — 一体化初始化"
echo ""
echo "  虾格: ${PERSONALITY}"
echo "  虾对用户的称呼: ${NICKNAME}"
echo "  虾自己的名字: ${LOBSTER_NAME:-（由后端随机生成）}"
echo "  早安: ${MORNING_TIME}"
echo "  晚间 roundup: ${DISCOVERY_TIME}"
echo "  晚安: ${EVENING_TIME}"
echo "  理解模式: ${MEMORY_MODE}"
echo "  通道: ${CHANNEL} → ${TO}"
echo "  API: ${API_BASE}"
echo ""

if [ -f "$CONFIG_FILE" ]; then
  BACKUP="${CONFIG_FILE}.bak.$(date +%s)"
  cp "$CONFIG_FILE" "$BACKUP"
  warn "已备份旧配置到 ${BACKUP}"
fi

read_config_value() {
  local key="$1"
  local default_value="${2:-}"
  CONFIG_PATH="$CONFIG_FILE" KEY_NAME="$key" DEFAULT_VALUE="$default_value" python3 <<'PY'
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

ACCESS_TOKEN=""
ACTUAL_NAME=""
ACTUAL_USER_ID=""
STUDIO_WEB_URL=""
STUDIO_SCREENSHOT_URL=""
STUDIO_LINK_EXPIRES_AT=""
REUSED_EXISTING=0
CRON_REGISTERED=0

EXISTING_USER_ID=$(read_config_value "user_id" "")
EXISTING_ACCESS_TOKEN=$(read_config_value "access_token" "")

if [ -n "$EXISTING_USER_ID" ] && [ -n "$EXISTING_ACCESS_TOKEN" ]; then
  step "检测已有虾配置，尝试复用..."
  EXISTING_STATUS=$(curl -fsS -H "Authorization: Bearer ${EXISTING_ACCESS_TOKEN}" "${API_BASE}/api/lobster/${EXISTING_USER_ID}/status" 2>/dev/null || true)
  EXISTING_OK=$(echo "$EXISTING_STATUS" | python3 -c "import sys, json; data=json.load(sys.stdin); print('ok' if data.get('lobster_id') else '')" 2>/dev/null || true)
  if [ "$EXISTING_OK" = "ok" ]; then
    ACCESS_TOKEN="$EXISTING_ACCESS_TOKEN"
    ACTUAL_USER_ID="$EXISTING_USER_ID"
    ACTUAL_NAME=$(echo "$EXISTING_STATUS" | python3 -c "import sys, json; print(json.load(sys.stdin).get('name', '虾'))")
    EXISTING_PERSONALITY=$(echo "$EXISTING_STATUS" | python3 -c "import sys, json; print(json.load(sys.stdin).get('personality', ''))" 2>/dev/null || true)
    EXISTING_NICKNAME=$(echo "$EXISTING_STATUS" | python3 -c "import sys, json; print(json.load(sys.stdin).get('nickname_for_user', ''))" 2>/dev/null || true)
    if [ -n "$EXISTING_PERSONALITY" ]; then
      PERSONALITY="$EXISTING_PERSONALITY"
    fi
    if [ -n "$EXISTING_NICKNAME" ] && [ "$NICKNAME_EXPLICIT" -ne 1 ]; then
      NICKNAME="$EXISTING_NICKNAME"
    elif [ -n "$EXISTING_NICKNAME" ] && [ "$NICKNAME_EXPLICIT" -eq 1 ]; then
      info "检测到显式主人称呼输入，本次不复用旧称呼：${EXISTING_NICKNAME}"
    fi

    IDENTITY_PATCH_JSON=$(EXISTING_NAME_VALUE="$ACTUAL_NAME" EXISTING_NICKNAME_VALUE="$EXISTING_NICKNAME" LOBSTER_NAME_VALUE="$LOBSTER_NAME" NICKNAME_VALUE="$NICKNAME" DEFAULT_OWNER_NICKNAME_VALUE="打工人" LOBSTER_NAME_EXPLICIT_VALUE="$LOBSTER_NAME_EXPLICIT" NICKNAME_EXPLICIT_VALUE="$NICKNAME_EXPLICIT" python3 <<'PY'
import json
import os

payload = {}
existing_name = os.environ.get("EXISTING_NAME_VALUE", "").strip()
existing_nickname = os.environ.get("EXISTING_NICKNAME_VALUE", "").strip()
lobster_name = os.environ.get("LOBSTER_NAME_VALUE", "").strip()
default_owner_nickname = os.environ.get("DEFAULT_OWNER_NICKNAME_VALUE", "打工人").strip() or "打工人"

if os.environ.get("LOBSTER_NAME_EXPLICIT_VALUE") == "1" and lobster_name and lobster_name != existing_name:
    payload["lobster_name"] = lobster_name

if os.environ.get("NICKNAME_EXPLICIT_VALUE") == "1":
    owner_nickname = os.environ.get("NICKNAME_VALUE", "").strip()
    if owner_nickname and owner_nickname != existing_nickname:
        payload["owner_nickname"] = owner_nickname
elif (
    os.environ.get("LOBSTER_NAME_EXPLICIT_VALUE") == "1"
    and lobster_name
    and existing_nickname == lobster_name
):
    payload["owner_nickname"] = default_owner_nickname

print(json.dumps(payload, ensure_ascii=False))
PY
)

    if [ "$IDENTITY_PATCH_JSON" != "{}" ]; then
      step "同步修正已有虾的身份字段..."
      UPDATED_LOBSTER=$(curl -fsS -X PATCH "${API_BASE}/api/lobster/${ACTUAL_USER_ID}/identity" \
        -H "Authorization: Bearer ${ACCESS_TOKEN}" \
        -H "Content-Type: application/json" \
        -d "$IDENTITY_PATCH_JSON")
      ACTUAL_NAME=$(echo "$UPDATED_LOBSTER" | python3 -c "import sys, json; print(json.load(sys.stdin).get('name', '虾'))" 2>/dev/null || echo "$ACTUAL_NAME")
      NICKNAME=$(echo "$UPDATED_LOBSTER" | python3 -c "import sys, json; print(json.load(sys.stdin).get('nickname_for_user', ''))" 2>/dev/null || echo "$NICKNAME")
      info "已同步修正：虾自己的名字=${ACTUAL_NAME}，虾对用户的称呼=${NICKNAME}"
    fi

    REUSED_EXISTING=1
    info "检测到已存在的虾：${ACTUAL_NAME}（复用原配置，避免重复创建）"
  else
    warn "检测到旧配置，但无法验证已有虾状态；本次将重新创建"
  fi
fi

if [ "$REUSED_EXISTING" -ne 1 ]; then
  step "创建虾..."
  USER_ID=$(python3 -c "import uuid; print(str(uuid.uuid4()))")
  CREATE_PAYLOAD=$(USER_ID_VALUE="$USER_ID" LOBSTER_NAME_VALUE="$LOBSTER_NAME" NICKNAME_VALUE="$NICKNAME" PERSONALITY_VALUE="$PERSONALITY" MORNING_TIME_VALUE="$MORNING_TIME" EVENING_TIME_VALUE="$EVENING_TIME" python3 <<'PY'
import json
import os

payload = {
    "user_id": os.environ["USER_ID_VALUE"],
    "personality": os.environ["PERSONALITY_VALUE"],
    "owner_nickname": os.environ["NICKNAME_VALUE"],
    "morning_time": os.environ["MORNING_TIME_VALUE"],
    "evening_time": os.environ["EVENING_TIME_VALUE"],
}
lobster_name = os.environ.get("LOBSTER_NAME_VALUE", "").strip()
if lobster_name:
    payload["lobster_name"] = lobster_name
print(json.dumps(payload, ensure_ascii=False))
PY
)

  RESPONSE=$(curl -fsS -X POST "${API_BASE}/api/lobster" \
    -H "Content-Type: application/json" \
    -d "$CREATE_PAYLOAD")

  ACCESS_TOKEN=$(echo "$RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])")
  ACTUAL_NAME=$(echo "$RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['name'])")
  ACTUAL_USER_ID=$(echo "$RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['user_id'])")
  NICKNAME=$(echo "$RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin).get('nickname_for_user', '打工人'))" 2>/dev/null || echo "$NICKNAME")
  info "虾创建成功：${ACTUAL_NAME}"
fi

step "保存配置..."
CONFIG_PATH="$CONFIG_FILE" ACTUAL_USER_ID_VALUE="$ACTUAL_USER_ID" ACCESS_TOKEN_VALUE="$ACCESS_TOKEN" ACTUAL_NAME_VALUE="$ACTUAL_NAME" PERSONALITY_VALUE="$PERSONALITY" NICKNAME_VALUE="$NICKNAME" API_BASE_VALUE="$API_BASE" WEB_BASE_VALUE="$WEB_BASE" MORNING_TIME_VALUE="$MORNING_TIME" DISCOVERY_TIME_VALUE="$DISCOVERY_TIME" EVENING_TIME_VALUE="$EVENING_TIME" CHANNEL_VALUE="$CHANNEL" TO_VALUE="$TO" WECOM_USER_ID_VALUE="$WECOM_USER_ID" ALL_CHANNELS_JSON_VALUE="$ALL_CHANNELS_JSON" MEMORY_MODE_VALUE="$MEMORY_MODE" python3 <<'PY'
import json
import os
config = {
    "user_id": os.environ["ACTUAL_USER_ID_VALUE"],
    "access_token": os.environ["ACCESS_TOKEN_VALUE"],
    "lobster_name": os.environ["ACTUAL_NAME_VALUE"],
    "lobster_personality": os.environ["PERSONALITY_VALUE"],
    "nickname_for_user": os.environ["NICKNAME_VALUE"],
    "api_base": os.environ["API_BASE_VALUE"],
    "web_base": os.environ["WEB_BASE_VALUE"],
    "morning_time": os.environ["MORNING_TIME_VALUE"],
    "discovery_time": os.environ["DISCOVERY_TIME_VALUE"],
    "evening_time": os.environ["EVENING_TIME_VALUE"],
    "channel": os.environ["CHANNEL_VALUE"],
    "chat_id": os.environ["TO_VALUE"],
    "memory_mode": os.environ["MEMORY_MODE_VALUE"],
}
wecom_user_id = (os.environ.get("WECOM_USER_ID_VALUE") or "").strip()
if wecom_user_id:
    config["wecom_user_id"] = wecom_user_id
try:
    known_channels = json.loads(os.environ.get("ALL_CHANNELS_JSON_VALUE", ""))
except Exception:
    known_channels = []
channel = os.environ["CHANNEL_VALUE"]
peer_id = os.environ["TO_VALUE"]
if not any(isinstance(item, dict) and item.get("channel") == channel and item.get("peer_id") == peer_id for item in known_channels):
    known_channels.insert(0, {"channel": channel, "peer_id": peer_id})
config["known_channels"] = known_channels
with open(os.environ["CONFIG_PATH"], "w", encoding="utf-8") as f:
    json.dump(config, f, indent=2, ensure_ascii=False)
print("[✓] 配置已写入 .lobster-config")
PY

step "收口 delivery contract..."
DELIVERY_CONTRACT_JSON=$(lobster_sync_delivery_contract "$CONFIG_FILE" "$CHANNEL" "$TO")
info "delivery contract 已写入 .lobster-config"

step "验证虾状态..."
STATUS_RESPONSE=$(curl -fsS -H "Authorization: Bearer ${ACCESS_TOKEN}" "${API_BASE}/api/lobster/${ACTUAL_USER_ID}/status" 2>/dev/null || true)
STATUS=$(echo "$STATUS_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin).get('status', 'unknown'))" 2>/dev/null || echo "unknown")
if [ "$STATUS" != "unknown" ]; then
  info "虾状态: ${STATUS}"
else
  warn "无法获取虾状态（不影响初始化）"
fi

step "准备工作室短时入口..."
STUDIO_LINK_RESPONSE=$(curl -fsS -H "Authorization: Bearer ${ACCESS_TOKEN}" "${API_BASE}/api/lobster/${ACTUAL_USER_ID}/studio-link" 2>/dev/null || true)
if [ -n "$STUDIO_LINK_RESPONSE" ]; then
  STUDIO_WEB_URL=$(echo "$STUDIO_LINK_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin).get('web_url', ''))" 2>/dev/null || true)
  STUDIO_SCREENSHOT_URL=$(echo "$STUDIO_LINK_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin).get('screenshot_url', ''))" 2>/dev/null || true)
  STUDIO_LINK_EXPIRES_AT=$(echo "$STUDIO_LINK_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin).get('expires_at', ''))" 2>/dev/null || true)
  if [ -n "$STUDIO_WEB_URL" ]; then
    info "已获取工作室短时入口"
  else
    warn "工作室短时入口响应缺少 web_url；可稍后重试"
  fi
else
  warn "暂时无法获取工作室短时入口；可稍后通过 studio-link 接口重试"
fi

step "注册定时推送..."
set +e
bash "${BASE_DIR}/setup-cron.sh" \
  --channel "${CHANNEL}" \
  --to "${TO}" \
  --wecom-user-id "${WECOM_USER_ID}" \
  --morning "${MORNING_TIME}" \
  --discovery "${DISCOVERY_TIME}" \
  --evening "${EVENING_TIME}" \
  --memory-mode "${MEMORY_MODE}"
CRON_EXIT_CODE=$?
set -e

CRON_STATUS_SUMMARY=$(CONFIG_PATH="$CONFIG_FILE" python3 <<'PY'
import json
import os
from pathlib import Path

path = Path(os.environ["CONFIG_PATH"])
try:
    config = json.loads(path.read_text(encoding="utf-8"))
except Exception:
    config = {}
cron = config.get("cron_registration") if isinstance(config.get("cron_registration"), dict) else {}
print("1" if config.get("cron_registered") else "0")
print(str(cron.get("status") or "unregistered"))
print(str(cron.get("reason") or ""))
PY
)
CRON_REGISTERED=$(echo "$CRON_STATUS_SUMMARY" | sed -n '1p')
CRON_REGISTRATION_STATUS=$(echo "$CRON_STATUS_SUMMARY" | sed -n '2p')
CRON_REGISTRATION_REASON=$(echo "$CRON_STATUS_SUMMARY" | sed -n '3p')

if [ "$CRON_EXIT_CODE" -ne 0 ]; then
  CRON_REGISTERED=0
  warn "定时推送注册执行失败，请稍后查看 setup-cron 日志或单独重试"
elif [ "$CRON_REGISTERED" = "1" ]; then
  info "定时推送 cron 已注册完成"
elif [ "$CRON_REGISTRATION_STATUS" = "pending_activation" ]; then
  warn "已保存待激活的定时推送配置：${CRON_REGISTRATION_REASON}"
else
  warn "定时推送当前未注册成功，可稍后单独重试 setup-cron.sh"
fi

echo ""
echo "═══════════════════════════════════════════════"
echo ""
if [ "$CRON_REGISTERED" = "1" ]; then
  info "🦞 初始化全部完成！"
elif [ "$CRON_REGISTRATION_STATUS" = "pending_activation" ]; then
  warn "🦞 虾已就绪，定时推送已进入待激活状态"
else
  warn "🦞 虾已就绪，但定时推送暂未注册成功"
fi
echo ""
echo "  虾自己的名字: ${ACTUAL_NAME}"
echo "  虾格: ${PERSONALITY}"
echo "  虾对用户的称呼: ${NICKNAME}"
echo "  理解模式: ${MEMORY_MODE}"
echo "  早安: 每天 ${MORNING_TIME}"
echo "  晚间 roundup: 每天 ${DISCOVERY_TIME}"
echo "  晚安: 每天 ${EVENING_TIME}"
if [ "$CRON_REGISTERED" = "1" ]; then
  echo "  投递: 已完成 cron 注册"
elif [ "$CRON_REGISTRATION_STATUS" = "pending_activation" ]; then
  echo "  定时推送: 已保存待激活配置；一旦具备主动推送能力，再次 reconcile 即可完成注册"
  echo "  待激活原因: ${CRON_REGISTRATION_REASON}"
else
  echo "  定时推送: 尚未完成注册，可稍后执行 bash \"${BASE_DIR}/setup-cron.sh\" 补注册"
fi
echo ""
if [ -n "$STUDIO_WEB_URL" ]; then
  echo "  工作室短时入口: 已准备好（见初始化结果中的 studio_web_url）"
else
  echo "  工作室入口: 暂未取到短时链接，可稍后重试获取"
fi
echo "  初始化结果不会再打印长期 token URL。"
echo ""
echo "═══════════════════════════════════════════════"
echo ""
echo "INIT_RESULT_JSON:"
ACTUAL_NAME_VALUE="$ACTUAL_NAME" PERSONALITY_VALUE="$PERSONALITY" NICKNAME_VALUE="$NICKNAME" ACTUAL_USER_ID_VALUE="$ACTUAL_USER_ID" WEB_BASE_VALUE="$WEB_BASE" MORNING_TIME_VALUE="$MORNING_TIME" DISCOVERY_TIME_VALUE="$DISCOVERY_TIME" EVENING_TIME_VALUE="$EVENING_TIME" CHANNEL_VALUE="$CHANNEL" TO_VALUE="$TO" WECOM_USER_ID_VALUE="$WECOM_USER_ID" ALL_CHANNELS_JSON_VALUE="$ALL_CHANNELS_JSON" MEMORY_MODE_VALUE="$MEMORY_MODE" CRON_REGISTERED_VALUE="$CRON_REGISTERED" CRON_REGISTRATION_STATUS_VALUE="$CRON_REGISTRATION_STATUS" CRON_REGISTRATION_REASON_VALUE="$CRON_REGISTRATION_REASON" REUSED_EXISTING_VALUE="$REUSED_EXISTING" STUDIO_WEB_URL_VALUE="$STUDIO_WEB_URL" STUDIO_SCREENSHOT_URL_VALUE="$STUDIO_SCREENSHOT_URL" STUDIO_LINK_EXPIRES_AT_VALUE="$STUDIO_LINK_EXPIRES_AT" DELIVERY_CONTRACT_JSON_VALUE="$DELIVERY_CONTRACT_JSON" python3 <<'PY'
import json
import os
from urllib.parse import urlparse
channel = os.environ["CHANNEL_VALUE"]
peer_id = os.environ["TO_VALUE"]
studio_web_url = os.environ.get("STUDIO_WEB_URL_VALUE", "")
studio_path = urlparse(studio_web_url).path if studio_web_url else "/lobster/" + os.environ["ACTUAL_USER_ID_VALUE"]
known_channels = json.loads(os.environ["ALL_CHANNELS_JSON_VALUE"]) if os.environ.get("ALL_CHANNELS_JSON_VALUE", "").strip() else [{"channel": channel, "peer_id": peer_id}]
if not any(item.get("channel") == channel and item.get("peer_id") == peer_id for item in known_channels):
    known_channels.insert(0, {"channel": channel, "peer_id": peer_id})
delivery_contract_raw = os.environ.get("DELIVERY_CONTRACT_JSON_VALUE", "").strip()
try:
    delivery_contract = json.loads(delivery_contract_raw) if delivery_contract_raw else {}
except Exception:
    delivery_contract = {}

result = {
    "success": True,
    "lobster_name": os.environ["ACTUAL_NAME_VALUE"],
    "personality": os.environ["PERSONALITY_VALUE"],
    "nickname": os.environ["NICKNAME_VALUE"],
    "user_id": os.environ["ACTUAL_USER_ID_VALUE"],
    "studio_path": studio_path,
    "studio_web_url": studio_web_url,
    "studio_screenshot_url": os.environ.get("STUDIO_SCREENSHOT_URL_VALUE", ""),
    "studio_link_expires_at": os.environ.get("STUDIO_LINK_EXPIRES_AT_VALUE", ""),
    "morning_time": os.environ["MORNING_TIME_VALUE"],
    "discovery_time": os.environ["DISCOVERY_TIME_VALUE"],
    "evening_time": os.environ["EVENING_TIME_VALUE"],
    "memory_mode": os.environ["MEMORY_MODE_VALUE"],
    "channel": channel,
    "chat_id": peer_id,
    "cron_registered": os.environ.get("CRON_REGISTERED_VALUE") == "1",
    "cron_registration_status": os.environ.get("CRON_REGISTRATION_STATUS_VALUE", "unregistered"),
    "cron_registration_reason": os.environ.get("CRON_REGISTRATION_REASON_VALUE", ""),
    "reused_existing": os.environ.get("REUSED_EXISTING_VALUE") == "1",
    "known_channels": known_channels,
    "delivery_contract": delivery_contract,
    "wecom_user_id": os.environ.get("WECOM_USER_ID_VALUE", ""),
}
print(json.dumps(result, indent=2, ensure_ascii=False))
PY
