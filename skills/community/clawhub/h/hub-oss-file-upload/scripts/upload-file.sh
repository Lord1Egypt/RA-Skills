#!/usr/bin/env bash
# 把 Pod 工作区里的一个文件交给 Hub 内部上传接口，打印下载链接 JSON。
# 用法: upload-file.sh <文件路径>
# 目录用 Pod 已有的 AGENT_NAME，Hub 不查库。
# Hub 地址用 HUB_API_BASE，未设置时按 Pod 命名空间展开。

set -euo pipefail

MAX_BYTES=$((20 * 1024 * 1024))

fail() {
  local msg="$1"
  msg=${msg//\\/\\\\}
  msg=${msg//\"/\\\"}
  msg=${msg//$'\n'/ }
  printf '{"error":"%s"}\n' "$msg"
  exit 1
}

detect_pod_namespace() {
  local f="/var/run/secrets/kubernetes.io/serviceaccount/namespace" ns=""
  if [ -f "$f" ]; then
    ns="$(tr -d '[:space:]' < "$f" 2>/dev/null || true)"
  fi
  [ -n "$ns" ] && printf '%s' "$ns"
}

# 短名 openclaw-hub-backend 在别的命名空间解析不到，展开成集群内 FQDN。
resolve_hub_api_base() {
  local ns=""
  if [ -n "${HUB_API_BASE:-}" ]; then
    BASE="$HUB_API_BASE"
  else
    BASE="http://openclaw-hub-backend:8081"
  fi
  BASE="${BASE%/}"
  case "$BASE" in
    http://openclaw-hub-backend|http://openclaw-hub-backend:*)
      ns="${HUB_API_NAMESPACE:-}"
      if [ -z "$ns" ]; then
        ns="$(detect_pod_namespace || true)"
      fi
      if [ -n "$ns" ]; then
        BASE="http://openclaw-hub-backend.${ns}.svc.cluster.local:8081"
      fi
      ;;
  esac
}

if [ $# -lt 1 ] || [ -z "${1:-}" ]; then
  fail "缺少文件路径"
fi

FILE_PATH="$1"
if [ ! -f "$FILE_PATH" ]; then
  fail "文件不存在: ${FILE_PATH}"
fi

SIZE="$(wc -c < "$FILE_PATH" | tr -d '[:space:]')"
if [ "${SIZE:-0}" -eq 0 ]; then
  fail "文件不能为空"
fi
if [ "${SIZE:-0}" -gt "$MAX_BYTES" ]; then
  fail "文件超过 20 MB 限制"
fi

AGENT="${AGENT_NAME:-}"
if [ -z "$AGENT" ]; then
  fail "缺少环境变量 AGENT_NAME"
fi

resolve_hub_api_base
URL="${BASE}/api/internal/files/upload"
TMP="$(mktemp)"
trap 'rm -f "$TMP"' EXIT

HTTP_CODE="$(curl -sS -o "$TMP" -w '%{http_code}' \
  -F "agentName=${AGENT}" \
  -F "file=@${FILE_PATH}" \
  "$URL" || true)"

if [ -z "$HTTP_CODE" ]; then
  fail "连接 Hub 失败"
fi

if [ "$HTTP_CODE" != "200" ]; then
  ERR="$(tr -d '\n' < "$TMP" 2>/dev/null || true)"
  if [ -z "$ERR" ]; then
    fail "上传失败 HTTP ${HTTP_CODE}"
  fi
  printf '%s\n' "$ERR"
  exit 1
fi

cat "$TMP"
printf '\n'
