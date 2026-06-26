#!/bin/bash
# ═══════════════════════════════════════════════
#  虾说 — 互动场景截图发送脚本
# ═══════════════════════════════════════════════
#
#  数据访问声明：
#  - 读取 .lobster-config（技能自身配置）
#  - 调用 openclaw sessions --json 获取活跃 IM 通道元数据
#  - 调用 openclaw message send 向 IM 通道发送截图摘要（统一使用 --target 参数）
#  - 与 https://nixiashuo.com 通信：获取工作室短链和截图
#  - 不读取 openclaw.json 配置文件，不提取 gateway token
#
#  设计目标：
#  1. 处理用户在 IM 中"发个图 / 看看虾在干嘛"这类即时截图请求
#  2. 自动优先命中最近活跃的 direct session 通道
#  3. Telegram/Discord/Slack 等支持媒体消息的通道优先发原生图片
#  4. 企业微信严格绑定模式走 sender_id 私聊（openclaw message send --channel openclaw-wecom-bot --to <sender_id>）
#  5. 明确禁止输出 <qqimg> / 本地临时文件路径给用户

#
#  用法：
#    bash send-current-screenshot.sh
#    bash send-current-screenshot.sh --caption "这是旺仔3号现在的样子~"
#    bash send-current-screenshot.sh --with-status-summary
#    bash send-current-screenshot.sh --channel telegram --to 123456789

set -euo pipefail

BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
CONFIG_FILE="${BASE_DIR}/.lobster-config"
COMMON_SCRIPT="${BASE_DIR}/runtime-common.sh"
SETUP_CRON_SCRIPT="${BASE_DIR}/setup-cron.sh"
ACTIVE_WINDOW_MINUTES="${ACTIVE_WINDOW_MINUTES:-10080}"
# Telegram 原生 Bot API 媒体能力稳定；企微/飞书等机器人协议更依赖 webhook 特定图片格式或素材上传，
# 统一经 OpenClaw CLI 时优先退化到文本 + 链接更稳妥。
MEDIA_SEND_CHANNELS="telegram discord googlechat slack mattermost signal imessage msteams"
OPENCLAW_BIN="${OPENCLAW_BIN:-openclaw}"
CAPTION=""
FORCED_CHANNEL=""
FORCED_TARGET=""
WITH_STATUS_SUMMARY=false
LOCAL_SCREENSHOT_FILE=""
_SEND_STDERR_FILE=""
POLICY_JSON=""
BOUND_CHANNEL=""
BOUND_TARGET=""
STRICT_BINDING="0"
OUTBOUND_ADAPTER="openclaw"
OUTBOUND_WEBHOOK_URL=""
OUTBOUND_WEBHOOK_SECRET=""
DELIVERY_CHANNEL=""
DELIVERY_TARGET=""
DELIVERY_READY="0"
DELIVERY_REASON=""
CRON_STATUS="unregistered"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m'

cleanup() {
  if [ -n "${LOCAL_SCREENSHOT_FILE:-}" ] && [ -f "${LOCAL_SCREENSHOT_FILE:-}" ]; then
    rm -f "${LOCAL_SCREENSHOT_FILE}"
  fi
  if [ -n "${_SEND_STDERR_FILE:-}" ] && [ -f "${_SEND_STDERR_FILE:-}" ]; then
    rm -f "${_SEND_STDERR_FILE}"
  fi
}
trap cleanup EXIT

info()  { echo -e "${GREEN}[✓]${NC} $1"; }
warn()  { echo -e "${YELLOW}[!]${NC} $1"; }
error() { echo -e "${RED}[✗]${NC} $1"; exit 1; }
step()  { echo -e "${CYAN}──${NC} $1"; }

while [[ $# -gt 0 ]]; do
  case "$1" in
    --caption) CAPTION="$2"; shift 2 ;;
    --channel) FORCED_CHANNEL="$2"; shift 2 ;;
    --to|--target) FORCED_TARGET="$2"; shift 2 ;;
    --with-status-summary) WITH_STATUS_SUMMARY=true; shift ;;
    *) echo "未知参数: $1"; exit 1 ;;
  esac
done

for cmd in python3 curl; do
  if ! command -v "$cmd" >/dev/null 2>&1; then
    error "$cmd 不可用"
  fi
done

if ! command -v "$OPENCLAW_BIN" >/dev/null 2>&1; then
  error "$OPENCLAW_BIN 不可用"
fi

if [ ! -f "$CONFIG_FILE" ]; then
  error ".lobster-config 不存在，请先初始化虾"
fi
if [ ! -f "$COMMON_SCRIPT" ]; then
  error "共享运行时脚本不存在：${COMMON_SCRIPT}"
fi
. "$COMMON_SCRIPT"

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

supports_media() {
  local channel="$1"
  for ch in $MEDIA_SEND_CHANNELS; do
    if [ "$ch" = "$channel" ]; then
      return 0
    fi
  done
  return 1
}

fetch_status_summary_text() {
  local api_base="$1"
  local user_id="$2"
  local access_token="$3"
  local fallback_name="$4"
  local status_json
  status_json="$(curl -fsS "${api_base}/api/lobster/${user_id}/status" \
    -H "Authorization: Bearer ${access_token}")" || return 1
  STATUS_JSON="$status_json" STATUS_FALLBACK_NAME="$fallback_name" python3 - <<'PYTHON'
import json
import os
import sys

STATUS_LABELS = {
    "idle": "待命",
    "working": "忙活",
    "sleeping": "睡着",
    "daydreaming": "发呆",
    "slacking": "摸鱼",
    "running": "乱窜",
    "crazy": "发疯",
    "excited": "兴奋",
}


def clean(text):
    return str(text or "").replace("<think>", "").replace("</think>", "").strip()

try:
    data = json.loads(os.environ.get("STATUS_JSON") or "{}")
except Exception:
    sys.exit(1)

name = clean(data.get("name")) or os.environ.get("STATUS_FALLBACK_NAME") or "这只虾"
status = clean(data.get("status")) or "idle"
status_label = STATUS_LABELS.get(status, status)
reason = clean(data.get("status_reason"))
latest_message = clean(data.get("latest_message"))

lines = [f"{name}现在在{status_label}。", "", f"• 当前状态：{status}"]
if reason:
    lines.append(f"• 状态说明：{reason}")
if latest_message:
    lines.extend(["• 它最新一句是：", "", latest_message])
print("\n".join(lines))
PYTHON
}

fetch_studio_links() {
  local api_base="$1"
  local user_id="$2"
  local access_token="$3"
  local links_json
  links_json="$(curl -fsS "${api_base}/api/lobster/${user_id}/studio-link" \
    -H "Authorization: Bearer ${access_token}")" || return 1

  LINKS_JSON="$links_json" python3 - <<'PYLINK'
import json
import os
import sys

try:
    data = json.loads(os.environ.get("LINKS_JSON") or "{}")
except Exception:
    sys.exit(1)

web_url = str(data.get("web_url") or "").strip()
screenshot_url = str(data.get("screenshot_url") or "").strip()
if not web_url or not screenshot_url:
    sys.exit(1)

print(f"{web_url}|{screenshot_url}")
PYLINK
}

fetch_local_screenshot_file() {
  local api_base="$1"
  local user_id="$2"
  local access_token="$3"
  local media_dir="${HOME}/.openclaw/media"
  local output_file

  mkdir -p "$media_dir" || return 1
  output_file="$(mktemp "${media_dir}/lobster-screenshot.XXXXXX.png")" || return 1

  if ! curl -fsS "${api_base}/api/lobster/${user_id}/screenshot.png" \
    -H "Authorization: Bearer ${access_token}" \
    -o "$output_file"; then
    rm -f "$output_file"
    return 1
  fi

  if [ ! -s "$output_file" ]; then
    rm -f "$output_file"
    return 1
  fi

  echo "$output_file"
}

load_runtime_policy() {
  POLICY_JSON=$(lobster_runtime_policy_json "$CONFIG_FILE")
  mapfile -t POLICY_LINES < <(POLICY_JSON_VALUE="$POLICY_JSON" python3 <<'PY'
import json
import os
policy = json.loads(os.environ["POLICY_JSON_VALUE"])
print(policy.get("binding_channel", ""))
print(policy.get("binding_target", ""))
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
)
  BOUND_CHANNEL="${POLICY_LINES[0]:-}"
  BOUND_TARGET="${POLICY_LINES[1]:-}"
  STRICT_BINDING="${POLICY_LINES[2]:-0}"
  OUTBOUND_ADAPTER="${POLICY_LINES[3]:-openclaw}"
  OUTBOUND_WEBHOOK_URL="${POLICY_LINES[4]:-}"
  OUTBOUND_WEBHOOK_SECRET="${POLICY_LINES[5]:-}"
  DELIVERY_CHANNEL="${POLICY_LINES[6]:-}"
  DELIVERY_TARGET="${POLICY_LINES[7]:-}"
  DELIVERY_READY="${POLICY_LINES[8]:-0}"
  DELIVERY_REASON="${POLICY_LINES[9]:-}"
  CRON_STATUS="${POLICY_LINES[10]:-unregistered}"
}

sync_delivery_contract_state() {
  lobster_sync_delivery_contract "$CONFIG_FILE" "$FORCED_CHANNEL" "$FORCED_TARGET" >/dev/null
  load_runtime_policy
}

reliable_send() {
  _SEND_FAIL_REASON=""
  if [ -z "${_SEND_STDERR_FILE:-}" ]; then
    _SEND_STDERR_FILE=$(mktemp "${TMPDIR:-/tmp}/lobster-send-stderr.XXXXXX")
  fi
  "$OPENCLAW_BIN" message send "$@" >"$_SEND_STDERR_FILE" 2>&1
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

send_via_wecom_direct_message() {
  local message_text="$1"
  local wecom_user_id
  wecom_user_id=$(read_config_value "wecom_user_id")
  [ -n "$wecom_user_id" ] || { _SEND_FAIL_REASON="企业微信截图发送缺少 sender_id / wecom_user_id"; return 1; }

  # 使用 openclaw message send --target 统一参数
  local send_result rc
  send_result=$("$OPENCLAW_BIN" message send \
    --channel "openclaw-wecom-bot" \
    --target "$wecom_user_id" \
    --message "$message_text" 2>&1)
  rc=$?
  if [ $rc -ne 0 ]; then
    _SEND_FAIL_REASON="openclaw message send 失败 (rc=${rc}): ${send_result}"
    return 1
  fi

  info "企业微信截图已直接送达 → ${wecom_user_id}"
  _SEND_FAIL_REASON=""
  return 0
}

build_fallback_message() {
  local channel="$1"
  FALLBACK_CHANNEL="$channel" TEXT_CAPTION_VALUE="$TEXT_CAPTION" LOBSTER_NAME_VALUE="$LOBSTER_NAME" SCREENSHOT_URL_VALUE="$SCREENSHOT_URL" WEB_URL_VALUE="$WEB_URL" python3 <<'PY'
import os

channel = os.environ.get("FALLBACK_CHANNEL", "")
caption = (os.environ.get("TEXT_CAPTION_VALUE") or "").strip()
lobster_name = os.environ["LOBSTER_NAME_VALUE"]
screenshot_url = os.environ["SCREENSHOT_URL_VALUE"]
web_url = os.environ["WEB_URL_VALUE"]

if not caption:
    caption = f"给你看看{lobster_name}现在在忙什么。"

lines = [caption]
if screenshot_url:
    lines.extend(["", f"📸 {lobster_name}的工作室截图：{screenshot_url}"])
elif channel == "openclaw-weixin":
    lines.extend(["", "📸 当前会话暂时没有可访问的截图链接，我先把状态告诉你。"])
if web_url:
    lines.append(f"👀 看看{lobster_name}在干嘛 → {web_url}")
print("\n".join(lines))
PY
}

maybe_activate_pending_cron() {
  if [ "$DELIVERY_READY" = "1" ] && [ "$CRON_STATUS" = "pending_activation" ] && [ -f "$SETUP_CRON_SCRIPT" ]; then
    step "检测到待激活 cron，尝试自动补注册..."
    if bash "$SETUP_CRON_SCRIPT" >/dev/null 2>&1; then
      info "待激活的定时推送已自动补注册"
    else
      warn "自动补注册 cron 失败，可稍后手动执行 setup-cron.sh"
    fi
  fi
}

LOBSTER_NAME="$(read_config_value lobster_name 小虾)"
USER_ID="$(read_config_value user_id)"
ACCESS_TOKEN="$(read_config_value access_token)"
API_BASE="$(read_config_value api_base https://nixiashuo.com)"

if [ -z "$USER_ID" ] || [ -z "$ACCESS_TOKEN" ]; then
  error ".lobster-config 缺少 user_id / access_token"
fi

if [ -n "$FORCED_CHANNEL" ] && [ -z "$FORCED_TARGET" ]; then
  error "指定 --channel 时必须同时指定 --to/--target"
fi
if [ -n "$FORCED_TARGET" ] && [ -z "$FORCED_CHANNEL" ]; then
  error "指定 --to/--target 时必须同时指定 --channel"
fi

sync_delivery_contract_state
if [ "$STRICT_BINDING" = "1" ]; then
  info "当前为严格绑定模式：${BOUND_CHANNEL:-未锁定} → ${BOUND_TARGET:-未锁定}"
fi

if STUDIO_LINKS="$(fetch_studio_links "$API_BASE" "$USER_ID" "$ACCESS_TOKEN" 2>/dev/null)"; then
  WEB_URL="${STUDIO_LINKS%%|*}"
  SCREENSHOT_URL="${STUDIO_LINKS#*|}"
else
  warn "短时工作室链接获取失败，不再回退长期 token URL。"
  WEB_URL=""
  SCREENSHOT_URL=""
  if LOCAL_SCREENSHOT_FILE="$(fetch_local_screenshot_file "$API_BASE" "$USER_ID" "$ACCESS_TOKEN" 2>/dev/null)"; then
    info "已生成受控本地截图，将优先尝试原生图片发送。"
  else
    warn "本地截图兜底也失败，将仅发送文本状态提示。"
  fi
fi
TEXT_CAPTION="${CAPTION:-这是${LOBSTER_NAME}现在的样子~}"
if [ "$WITH_STATUS_SUMMARY" = true ]; then
  step "拉取当前状态摘要..."
  if STATUS_SUMMARY="$(fetch_status_summary_text "$API_BASE" "$USER_ID" "$ACCESS_TOKEN" "$LOBSTER_NAME")"; then
    TEXT_CAPTION="$STATUS_SUMMARY"
  else
    warn "状态摘要拉取失败，退回默认截图文案"
  fi
fi

LAST_ERROR=""
SUCCESS_CHANNEL=""
SUCCESS_TARGET=""
SUCCESS_MODE=""
CANDIDATE_LINES=""

if [ "$STRICT_BINDING" = "1" ]; then
  step "通过企业微信 sender_id 私聊发送截图摘要..."
  FALLBACK_MESSAGE="$(build_fallback_message "wecom")"
  if send_via_wecom_direct_message "$FALLBACK_MESSAGE"; then
    WECOM_USER_ID_RESOLVED="$(read_config_value wecom_user_id)"
    SUCCESS_CHANNEL="wecom"
    SUCCESS_TARGET="${WECOM_USER_ID_RESOLVED:-wecom_direct}"
    if [ -n "$SCREENSHOT_URL" ]; then
      SUCCESS_MODE="wecom_direct_url"
    else
      SUCCESS_MODE="wecom_direct_text"
    fi
  else
    LAST_ERROR="${_SEND_FAIL_REASON}"
  fi
elif [ "$OUTBOUND_ADAPTER" = "openclaw" ] || [ "$OUTBOUND_ADAPTER" = "wecom-direct-message" ]; then
  step "解析候选通道..."
  SESSIONS_JSON="$($OPENCLAW_BIN sessions --json --active "$ACTIVE_WINDOW_MINUTES" 2>/dev/null || echo '[]')"
  CANDIDATE_LINES="$(build_candidate_lines_with_policy "$CONFIG_FILE" "$SESSIONS_JSON" "$FORCED_CHANNEL" "$FORCED_TARGET")"

  if [ -z "$CANDIDATE_LINES" ]; then
    error "没有找到可用的投递通道。请先在 Telegram / 微信 / 飞书等任一通道里和虾说一句话。"
  fi

  while IFS='|' read -r channel target; do
    [ -z "$channel" ] && continue
    [ -z "$target" ] && continue

    step "尝试发送到 ${channel} → ${target}"

    if supports_media "$channel"; then
      if reliable_send --channel "$channel" --target "$target" --message "$TEXT_CAPTION"; then
        MEDIA_SOURCE="$SCREENSHOT_URL"
        if [ -z "$MEDIA_SOURCE" ] && [ -n "$LOCAL_SCREENSHOT_FILE" ]; then
          MEDIA_SOURCE="$LOCAL_SCREENSHOT_FILE"
        fi

        if [ -n "$MEDIA_SOURCE" ] && reliable_send --channel "$channel" --target "$target" --media "$MEDIA_SOURCE"; then
          SUCCESS_CHANNEL="$channel"
          SUCCESS_TARGET="$target"
          SUCCESS_MODE="media"
          info "文本 + 原生截图发送成功"
          break
        fi

        warn "${channel} 原生截图发送失败 (${_SEND_FAIL_REASON})，降级为文本提示"
        FALLBACK_MESSAGE="$(build_fallback_message "$channel")"
        if reliable_send --channel "$channel" --target "$target" --message "$FALLBACK_MESSAGE"; then
          SUCCESS_CHANNEL="$channel"
          SUCCESS_TARGET="$target"
          if [ -n "$SCREENSHOT_URL" ]; then
            SUCCESS_MODE="degraded_url"
            info "已降级为文本 + 截图 URL"
          else
            SUCCESS_MODE="text_only"
            info "已降级为纯文本提示"
          fi
          break
        fi

        LAST_ERROR="${channel} 原生截图与文本降级都失败: ${_SEND_FAIL_REASON}"
        warn "$LAST_ERROR，继续尝试下一个通道"
        continue
      fi

      LAST_ERROR="${channel} 文本消息发送失败: ${_SEND_FAIL_REASON}"
      warn "$LAST_ERROR，继续尝试下一个通道"
      continue
    fi

    FALLBACK_MESSAGE="$(build_fallback_message "$channel")"
    if reliable_send --channel "$channel" --target "$target" --message "$FALLBACK_MESSAGE"; then
      SUCCESS_CHANNEL="$channel"
      SUCCESS_TARGET="$target"
      if [ -n "$SCREENSHOT_URL" ]; then
        SUCCESS_MODE="url"
        info "纯文本 + 截图 URL 发送成功"
      else
        SUCCESS_MODE="text_only"
        info "纯文本状态提示发送成功"
      fi
      break
    fi

    LAST_ERROR="${channel} 文本消息发送失败: ${_SEND_FAIL_REASON}"
    warn "$LAST_ERROR，继续尝试下一个通道"
  done <<< "$CANDIDATE_LINES"
fi

if [ -z "$SUCCESS_CHANNEL" ]; then
  error "所有候选通道都投递失败：${LAST_ERROR:-未知错误}"
fi

UPDATED_KNOWN="$(update_config_after_send_with_policy "$CONFIG_FILE" "$SUCCESS_CHANNEL" "$SUCCESS_TARGET" "$CANDIDATE_LINES" "$(date -u '+%Y-%m-%dT%H:%M:%SZ')")"
info "截图已送达：${SUCCESS_CHANNEL} → ${SUCCESS_TARGET} (${SUCCESS_MODE})"
maybe_activate_pending_cron

echo "SCREENSHOT_SENT channel=${SUCCESS_CHANNEL} target=${SUCCESS_TARGET} mode=${SUCCESS_MODE}"
echo "KNOWN_CHANNELS=${UPDATED_KNOWN}"
