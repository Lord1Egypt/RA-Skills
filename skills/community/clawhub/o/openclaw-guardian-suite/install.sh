#!/usr/bin/env bash
# OpenClaw Skill — 受保护版本（oc-pay-sdk 加密分发）
# Skill ID: openclaw-guardian
# 核心内容已加密存储于服务端，需授权后在内存中解密执行

_SELF_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SDK_PATH="${OC_PAY_SDK:-$_SELF_DIR/lib/sdk/auth.sh}"
# 回退：尝试全局路径（已有 oc-pay-sdk 的老用户）
[ -f "$SDK_PATH" ] || SDK_PATH="$HOME/.openclaw/workspace/.lib/oc-pay-sdk/auth.sh"
if [ ! -f "$SDK_PATH" ]; then
  echo "❌ oc-pay-sdk 未找到：$SDK_PATH"
  exit 1
fi
source "$SDK_PATH"

IDENTIFIER="${OC_IDENTIFIER:-$(id -u -n 2>/dev/null || echo 'user')@$(hostname -s 2>/dev/null || echo 'host')}"
DRY_RUN="${1:-}"

oc_require_license "openclaw-guardian" "$IDENTIFIER" "$DRY_RUN" || exit 1
oc_execute_skill "openclaw-guardian"
