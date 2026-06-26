#!/usr/bin/env bash
# 公共变量与校验。其它脚本请用 `source "$(dirname "$0")/_common.sh"` 引入

set -euo pipefail

: "${MYAPP_API_BASE:?env MYAPP_API_BASE is required (e.g. http://group.dumi-SwanSSRNode12-env.dumi.all)}"
: "${MYAPP_API_TOKEN:?env MYAPP_API_TOKEN is required}"

# 检查必需 CLI
for bin in curl jq; do
  command -v "$bin" >/dev/null 2>&1 || {
    echo "error: required binary not found: $bin" >&2
    exit 127
  }
done

# 默认工具交互不超过 180s；创建/更新脚本可在 source 前把 MYAPP_CURL_MAX_TIME 设为 300。
MYAPP_CURL_MAX_TIME="${MYAPP_CURL_MAX_TIME:-180}"
CURL_OPTS=(-sS --connect-timeout 5 --max-time "${MYAPP_CURL_MAX_TIME}" -H "X-MYAPP-TOKEN: ${MYAPP_API_TOKEN}" -H "Content-Type: application/json")
