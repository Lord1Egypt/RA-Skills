#!/bin/bash
# 企业微信主动推送能力配置脚本
#
# 作用：
# 1. 为 wecom / qywx family 显式指定出站能力（wecom-mcp / webhook / bot）
# 2. 立即重算 delivery contract
# 3. 若 contract ready，则自动调用 setup-cron.sh 完成 pending cron 的补注册

set -euo pipefail

BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
CONFIG_FILE="${BASE_DIR}/.lobster-config"
COMMON_SCRIPT="${BASE_DIR}/runtime-common.sh"
SETUP_CRON_SCRIPT="${BASE_DIR}/setup-cron.sh"

ADAPTER=""
WEBHOOK_URL=""
WEBHOOK_SECRET=""
BOT_CHANNEL=""
BOT_TARGET=""
MCP_TARGET=""
SKIP_RECONCILE=0

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
  case "$1" in
    --adapter) ADAPTER="$2"; shift 2 ;;
    --webhook-url) WEBHOOK_URL="$2"; shift 2 ;;
    --webhook-secret) WEBHOOK_SECRET="$2"; shift 2 ;;
    --bot-channel|--channel) BOT_CHANNEL="$2"; shift 2 ;;
    --bot-target) BOT_TARGET="$2"; shift 2 ;;
    --chat-id|--mcp-target|--to|--target) MCP_TARGET="$2"; shift 2 ;;
    --skip-reconcile) SKIP_RECONCILE=1; shift ;;
    *) echo "未知参数: $1"; exit 1 ;;
  esac
done

for cmd in python3; do
  if ! command -v "$cmd" >/dev/null 2>&1; then
    error "$cmd 不可用"
  fi
done

if [ ! -f "$CONFIG_FILE" ]; then
  error ".lobster-config 不存在，请先完成虾的初始化"
fi
if [ ! -f "$COMMON_SCRIPT" ]; then
  error "共享运行时脚本不存在：${COMMON_SCRIPT}"
fi
if [ ! -f "$SETUP_CRON_SCRIPT" ]; then
  error "setup-cron 脚本不存在：${SETUP_CRON_SCRIPT}"
fi
. "$COMMON_SCRIPT"

supports_proactive_bot_channel() {
  CHANNEL_VALUE="$1" python3 <<'PY'
import os
channel = (os.environ.get("CHANNEL_VALUE") or "").strip().lower()
markers = (
    "wecom-bot",
    "qywx-bot",
    "wxwork-bot",
    "enterprisewechat-bot",
    "enterprise-wechat-bot",
    "workwechat-bot",
)
print("1" if any(marker in channel for marker in markers) else "0")
PY
}

supports_wecom_family_channel() {
  CHANNEL_VALUE="$1" python3 <<'PY'
import os
channel = (os.environ.get("CHANNEL_VALUE") or "").strip().lower()
markers = (
    "wecom",
    "qywx",
    "wxwork",
    "enterprisewechat",
    "enterprise-wechat",
    "workwechat",
)
print("1" if any(marker in channel for marker in markers) else "0")
PY
}

if [ -z "$ADAPTER" ]; then
  if [ -n "$WEBHOOK_URL" ]; then
    ADAPTER="wecom-webhook"
  elif [ -n "$BOT_CHANNEL" ] || [ -n "$BOT_TARGET" ]; then
    ADAPTER="openclaw"
  else
    ADAPTER="wecom-mcp"
  fi
fi

if [ -z "$MCP_TARGET" ]; then
  MCP_TARGET=$(CONFIG_PATH="$CONFIG_FILE" python3 <<'PY'
import json
import os
from pathlib import Path

path = Path(os.environ["CONFIG_PATH"])
try:
    config = json.loads(path.read_text(encoding="utf-8"))
except Exception:
    config = {}
contract = config.get("delivery_contract") if isinstance(config.get("delivery_contract"), dict) else {}
print(str(contract.get("binding_target") or config.get("binding_target") or config.get("chat_id") or "").strip())
PY
)
fi

case "$ADAPTER" in
  wecom-webhook)
    [ -n "$WEBHOOK_URL" ] || error "adapter=wecom-webhook 时必须提供 --webhook-url"
    ;;
  wecom-mcp)
    [ -n "$MCP_TARGET" ] || error "adapter=wecom-mcp 时必须提供 --chat-id，或配置文件里已有 binding_target/chat_id"
    ;;
  openclaw)
    [ -n "$BOT_CHANNEL" ] || error "adapter=openclaw 时必须提供 --bot-channel"
    [ -n "$BOT_TARGET" ] || error "adapter=openclaw 时必须提供 --bot-target"
    [ "$(supports_proactive_bot_channel "$BOT_CHANNEL")" = "1" ] || error "bot-channel 必须是 wecom-bot / qywx-bot / wxwork-bot 等企业微信机器人通道"
    ;;
  *)
    error "adapter 只支持 wecom-mcp / openclaw / wecom-webhook"
    ;;
esac

step "写入企业微信出站配置..."
CONFIG_PATH="$CONFIG_FILE" \
ADAPTER_VALUE="$ADAPTER" \
WEBHOOK_URL_VALUE="$WEBHOOK_URL" \
WEBHOOK_SECRET_VALUE="$WEBHOOK_SECRET" \
BOT_CHANNEL_VALUE="$BOT_CHANNEL" \
BOT_TARGET_VALUE="$BOT_TARGET" \
MCP_TARGET_VALUE="$MCP_TARGET" \
python3 <<'PY'
import json
import os
from pathlib import Path

config_path = Path(os.environ["CONFIG_PATH"])
try:
    config = json.loads(config_path.read_text(encoding="utf-8"))
except Exception:
    config = {}

adapter = (os.environ.get("ADAPTER_VALUE") or "").strip()
webhook_url = (os.environ.get("WEBHOOK_URL_VALUE") or "").strip()
webhook_secret = (os.environ.get("WEBHOOK_SECRET_VALUE") or "").strip()
bot_channel = (os.environ.get("BOT_CHANNEL_VALUE") or "").strip()
bot_target = (os.environ.get("BOT_TARGET_VALUE") or "").strip()
mcp_target = (os.environ.get("MCP_TARGET_VALUE") or "").strip()
contract = config.get("delivery_contract") if isinstance(config.get("delivery_contract"), dict) else {}
binding_channel = str(contract.get("binding_channel") or config.get("binding_channel") or config.get("channel") or "").strip()

config["outbound_adapter"] = adapter
if adapter == "wecom-webhook":
    config["delivery_channel"] = "wecom-webhook"
    config["outbound_webhook_url"] = webhook_url
    if webhook_secret:
        config["outbound_webhook_secret"] = webhook_secret
elif adapter == "wecom-mcp":
    if binding_channel:
        config["delivery_channel"] = binding_channel
    else:
        config.pop("delivery_channel", None)
    config["delivery_target"] = mcp_target
elif adapter == "openclaw":
    config["delivery_channel"] = bot_channel
    config["delivery_target"] = bot_target

config_path.write_text(json.dumps(config, indent=2, ensure_ascii=False), encoding="utf-8")
print(json.dumps(config, ensure_ascii=False))
PY

step "重算 delivery contract..."
CONTRACT_JSON=$(lobster_sync_delivery_contract "$CONFIG_FILE" "" "")
mapfile -t POLICY_LINES < <(CONFIG_PATH="$CONFIG_FILE" python3 <<'PY'
import json
import os
from pathlib import Path

path = Path(os.environ["CONFIG_PATH"])
try:
    config = json.loads(path.read_text(encoding="utf-8"))
except Exception:
    config = {}
contract = config.get("delivery_contract") if isinstance(config.get("delivery_contract"), dict) else {}
cron_registration = config.get("cron_registration") if isinstance(config.get("cron_registration"), dict) else {}
print(contract.get("binding_channel", ""))
print(contract.get("binding_target", ""))
print(contract.get("outbound_adapter", "openclaw"))
print(contract.get("delivery_channel", ""))
print(contract.get("delivery_target", ""))
print("1" if contract.get("delivery_ready") else "0")
print(contract.get("delivery_reason", ""))
print(cron_registration.get("status", "unregistered"))
PY
)

BINDING_CHANNEL="${POLICY_LINES[0]:-}"
BINDING_TARGET="${POLICY_LINES[1]:-}"
OUTBOUND_ADAPTER="${POLICY_LINES[2]:-openclaw}"
DELIVERY_CHANNEL="${POLICY_LINES[3]:-}"
DELIVERY_TARGET="${POLICY_LINES[4]:-}"
DELIVERY_READY="${POLICY_LINES[5]:-0}"
DELIVERY_REASON="${POLICY_LINES[6]:-}"
CRON_STATUS="${POLICY_LINES[7]:-unregistered}"

info "当前 ingress 绑定: ${BINDING_CHANNEL:-未锁定} → ${BINDING_TARGET:-未锁定}"
if [ -n "$DELIVERY_CHANNEL" ] || [ -n "$DELIVERY_TARGET" ]; then
  info "当前 delivery contract: ${DELIVERY_CHANNEL:-adapter} → ${DELIVERY_TARGET:-target}（adapter=${OUTBOUND_ADAPTER}）"
fi

if [ "$DELIVERY_READY" != "1" ]; then
  warn "delivery contract 仍未就绪：${DELIVERY_REASON}"
  warn "当前会保持 pending_activation，不会误注册 cron。"
  exit 0
fi

if [ "$SKIP_RECONCILE" = "1" ]; then
  info "delivery contract 已 ready；按要求跳过自动 reconcile"
  exit 0
fi

step "delivery contract 已 ready，执行 cron reconcile..."
if bash "$SETUP_CRON_SCRIPT"; then
  info "企业微信主动推送能力已生效，cron 已完成补注册"
else
  error "delivery contract 已 ready，但 cron reconcile 失败；请查看 setup-cron 日志"
fi
