#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
STOPPER="$SCRIPT_DIR/scripts/stop_web_app.py"
RUNTIME_DIR="$SCRIPT_DIR/skill-data/runtime"
UNIT_PATH="$HOME/.config/systemd/user/openai-auth-switcher-web-preview.service"

if [[ -t 1 ]]; then
  C_RESET=$'\033[0m'; C_BOLD=$'\033[1m'; C_GREEN=$'\033[32m'; C_YELLOW=$'\033[33m'; C_RED=$'\033[31m'; C_BLUE=$'\033[34m'; C_CYAN=$'\033[36m'
else
  C_RESET=''; C_BOLD=''; C_GREEN=''; C_YELLOW=''; C_RED=''; C_BLUE=''; C_CYAN=''
fi
section() { printf "\n%s%s== %s ==%s\n" "$C_BLUE" "$C_BOLD" "$1" "$C_RESET"; }
ok() { printf "%s[OK]%s %s\n" "$C_GREEN" "$C_RESET" "$1"; }
warn() { printf "%s[WARN]%s %s\n" "$C_YELLOW" "$C_RESET" "$1"; }
err() { printf "%s[ERROR]%s %s\n" "$C_RED" "$C_RESET" "$1" >&2; }
keyv() { printf "%s%-12s%s %s%s%s\n" "$C_CYAN" "$1" "$C_RESET" "$C_BOLD" "$2" "$C_RESET"; }

if ! command -v python3 >/dev/null 2>&1; then
  err "未找到 python3，无法执行卸载清理。"
  exit 1
fi
if [[ ! -f "$STOPPER" ]]; then
  err "缺少停止脚本：$STOPPER"
  exit 1
fi

section "OPENAI AUTH SWITCHER PUBLIC"
ok "开始卸载 Web 预览入口"

set +e
STOP_JSON="$(python3 "$STOPPER" 2>&1)"
STOP_CODE=$?
set -e
if [[ $STOP_CODE -ne 0 ]]; then
  warn "停止服务阶段返回非 0，继续尝试清理残留。"
  printf "%s\n" "$STOP_JSON"
else
  ok "服务停止指令已执行"
fi

UNIT_REMOVED=false
if [[ -f "$UNIT_PATH" ]]; then
  rm -f "$UNIT_PATH"
  systemctl --user daemon-reload >/dev/null 2>&1 || true
  UNIT_REMOVED=true
fi

REMOVED_FILES=0
if [[ -d "$RUNTIME_DIR" ]]; then
  while IFS= read -r -d '' f; do
    rm -f "$f"
    REMOVED_FILES=$((REMOVED_FILES + 1))
  done < <(find "$RUNTIME_DIR" -maxdepth 1 -type f -print0)
fi

section "RESULT"
ok "卸载清理完成"
if [[ "$UNIT_REMOVED" == true ]]; then
  ok "systemd unit 已删除"
else
  warn "未发现本地 systemd unit 文件，可能此前走的是后台模式"
fi
keyv "RUNTIME" "$RUNTIME_DIR"
keyv "REMOVED" "$REMOVED_FILES files"

section "NEXT"
printf "%s%s%s\n" "$C_BOLD" "现在可安全执行：clawhub uninstall openai-auth-switcher-public" "$C_RESET"
