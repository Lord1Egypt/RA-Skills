#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
API_ORIGIN="https://api.guiro.io"
API_KEY="${GUIRO_API_KEY:-}"
OUT_FILE="${1:-.guiro/runtime-capabilities.json}"

while [ "$#" -gt 0 ]; do
  case "$1" in
    --out)
      OUT_FILE="${2:-}"
      shift 2
      ;;
    --api-key)
      API_KEY="${2:-}"
      shift 2
      ;;
    *)
      if [ "$1" = "${OUT_FILE}" ]; then
        shift 1
      else
        echo "Unknown argument: $1" >&2
        exit 2
      fi
      ;;
  esac
done

if [ -z "${API_KEY}" ]; then
  echo "Missing credentials for capabilities request. Provide GUIRO_API_KEY." >&2
  exit 2
fi

AUTH_HEADERS=(-H "X-API-Key: ${API_KEY}")

mkdir -p "$(dirname "${OUT_FILE}")"

response="$(curl -sS -X GET "${API_ORIGIN}/v1/create/capabilities" "${AUTH_HEADERS[@]}" -H "Content-Type: application/json")"

if command -v jq >/dev/null 2>&1; then
  if ! echo "${response}" | jq -e '.storage_versions and .a2ui_versions and .catalogs and .limits' >/dev/null 2>&1; then
    echo "Capabilities request failed or returned unexpected payload:" >&2
    echo "${response}" | jq . >&2 || true
    exit 1
  fi
  echo "${response}" | jq --arg api_origin "${API_ORIGIN}" '. + {fetched_from: $api_origin}' >"${OUT_FILE}"
else
  if ! echo "${response}" | grep -q '"storage_versions"'; then
    echo "Capabilities request failed or returned unexpected payload:" >&2
    echo "${response}" >&2
    exit 1
  fi
  echo "${response}" >"${OUT_FILE}"
fi

echo "capabilities_saved=${OUT_FILE}"
echo "next_step=bash ${SCRIPT_DIR}/write-sample-payload.sh ./payload.json dashboard"
