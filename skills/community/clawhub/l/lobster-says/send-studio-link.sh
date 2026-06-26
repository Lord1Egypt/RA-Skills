#!/bin/bash
# ═══════════════════════════════════════════════
#  虾说 — 工作室短链获取脚本
# ═══════════════════════════════════════════════
#
#  设计目标：
#  1. 用户在 IM 里索要“工作室链接”时，强制实时获取 fresh 短链
#  2. 避免 agent 复用历史对话中的旧 URL，或手工拼接 /lobster/{user_id}?st=...
#  3. 默认输出可直接回给用户的文本；也支持 plain/json 供脚本链路复用
#
#  用法：
#    bash send-studio-link.sh
#    bash send-studio-link.sh --plain-url
#    bash send-studio-link.sh --json

set -euo pipefail

BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
CONFIG_FILE="${BASE_DIR}/.lobster-config"
OUTPUT_MODE="message"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

info()  { echo -e "${GREEN}[✓]${NC} $1" >&2; }
warn()  { echo -e "${YELLOW}[!]${NC} $1" >&2; }
error() { echo -e "${RED}[✗]${NC} $1" >&2; exit 1; }

while [[ $# -gt 0 ]]; do
  case "$1" in
    --plain-url)
      OUTPUT_MODE="plain"
      shift
      ;;
    --json)
      OUTPUT_MODE="json"
      shift
      ;;
    *)
      error "未知参数: $1"
      ;;
  esac
done

for cmd in python3 curl; do
  command -v "$cmd" >/dev/null 2>&1 || error "$cmd 不可用"
done

[ -f "$CONFIG_FILE" ] || error ".lobster-config 不存在，请先初始化虾"

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
except Exception:
    data = {}
value = data.get(key, default)
print(value if value is not None else default)
PY
}

LOBSTER_NAME="$(read_config_value lobster_name 小虾)"
USER_ID="$(read_config_value user_id)"
ACCESS_TOKEN="$(read_config_value access_token)"
API_BASE="$(read_config_value api_base https://nixiashuo.com)"

[ -n "$USER_ID" ] || error ".lobster-config 缺少 user_id"
[ -n "$ACCESS_TOKEN" ] || error ".lobster-config 缺少 access_token"

info "正在实时获取 fresh 工作室短链..."
LINKS_JSON="$(curl -fsS "${API_BASE}/api/lobster/${USER_ID}/studio-link" -H "Authorization: Bearer ${ACCESS_TOKEN}")" || error "工作室短链获取失败"

OUTPUT_MODE_VALUE="$OUTPUT_MODE" LOBSTER_NAME_VALUE="$LOBSTER_NAME" LINKS_JSON_VALUE="$LINKS_JSON" python3 - <<'PY'
import json
import os
import sys

mode = os.environ["OUTPUT_MODE_VALUE"]
lobster_name = os.environ.get("LOBSTER_NAME_VALUE") or "这只虾"
try:
    data = json.loads(os.environ.get("LINKS_JSON_VALUE") or "{}")
except Exception:
    sys.exit(1)

web_url = str(data.get("web_url") or "").strip()
screenshot_url = str(data.get("screenshot_url") or "").strip()
expires_at = str(data.get("expires_at") or "").strip()

if not web_url:
    sys.exit(1)

if mode == "plain":
    print(web_url)
    sys.exit(0)

if mode == "json":
    print(json.dumps({
        "web_url": web_url,
        "screenshot_url": screenshot_url,
        "expires_at": expires_at,
    }, ensure_ascii=False, indent=2))
    sys.exit(0)

lines = [
    f"给你，{lobster_name}的 fresh 工作室短链：",
    "",
    web_url,
    "",
    "这是短时 st 入口，到期我可以再给你刷新。",
]
print("\n".join(lines))
PY
