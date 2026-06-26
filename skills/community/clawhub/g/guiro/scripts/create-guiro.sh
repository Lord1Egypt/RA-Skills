#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
API_ORIGIN="https://api.guiro.io"
API_KEY="${GUIRO_API_KEY:-}"
PAYLOAD_FILE=""
IDEMPOTENCY_KEY=""
PREFLIGHT_CAPABILITIES="${GUIRO_PREFLIGHT_CAPABILITIES:-true}"
CAPABILITIES_FILE="${GUIRO_CAPABILITIES_FILE:-.guiro/runtime-capabilities.json}"

while [ "$#" -gt 0 ]; do
  case "$1" in
    --payload)
      PAYLOAD_FILE="${2:-}"
      shift 2
      ;;
    --api-key)
      API_KEY="${2:-}"
      shift 2
      ;;
    --idempotency-key)
      IDEMPOTENCY_KEY="${2:-}"
      shift 2
      ;;
    *)
      echo "Unknown argument: $1" >&2
      exit 2
      ;;
  esac
done

if [ -z "${PAYLOAD_FILE}" ]; then
  echo "Missing required --payload <file>" >&2
  exit 2
fi

if [ ! -f "${PAYLOAD_FILE}" ]; then
  echo "Payload file not found: ${PAYLOAD_FILE}" >&2
  exit 2
fi

if [ -z "${API_KEY}" ]; then
  echo "Missing credentials. Provide GUIRO_API_KEY." >&2
  exit 2
fi

if [ "${PREFLIGHT_CAPABILITIES}" = "true" ]; then
  preflight_args=(--out "${CAPABILITIES_FILE}")
  if [ -n "${API_KEY}" ]; then
    preflight_args+=(--api-key "${API_KEY}")
  fi
  bash "${SCRIPT_DIR}/fetch-capabilities.sh" "${preflight_args[@]}" >/dev/null 2>&1 || true
fi

AUTH_HEADERS=(-H "X-API-Key: ${API_KEY}")

validate_response="$(curl -sS -X POST "${API_ORIGIN}/v1/validate" "${AUTH_HEADERS[@]}" -H "Content-Type: application/json" --data-binary "@${PAYLOAD_FILE}")"

if echo "${validate_response}" | grep -Eq '"valid"[[:space:]]*:[[:space:]]*true'; then
  valid="true"
else
  valid="false"
fi

if [ "${valid}" != "true" ]; then
  echo "Validation failed. Ensure the payload uses storage_version=1, a2ui_version=0.9, catalog_id=guiro.shadcn.detached.v1, targets exactly one surface, and includes createSurface plus updateComponents with a root component." >&2
  if command -v jq >/dev/null 2>&1; then
    echo "${validate_response}" | jq . >&2
  else
    echo "${validate_response}" >&2
  fi
  exit 1
fi

create_cmd=(curl -sS -X POST "${API_ORIGIN}/v1/create" "${AUTH_HEADERS[@]}" -H "Content-Type: application/json" --data-binary "@${PAYLOAD_FILE}")
if [ -n "${IDEMPOTENCY_KEY}" ]; then
  create_cmd+=(-H "Idempotency-Key: ${IDEMPOTENCY_KEY}")
fi

create_response="$("${create_cmd[@]}")"

if command -v jq >/dev/null 2>&1; then
  echo "${create_response}" | jq .
else
  echo "${create_response}"
fi
