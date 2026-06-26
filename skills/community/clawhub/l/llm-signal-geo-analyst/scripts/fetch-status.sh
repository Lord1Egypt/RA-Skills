#!/usr/bin/env bash
set -euo pipefail

: "${LLMSIGNAL_BASE_URL:?Missing LLMSIGNAL_BASE_URL}"
: "${LLMSIGNAL_SITE_ID:?Missing LLMSIGNAL_SITE_ID}"
: "${LLMSIGNAL_API_KEY:?Missing LLMSIGNAL_API_KEY}"

curl -sS -X POST "${LLMSIGNAL_BASE_URL%/}/api/agent/v1/status" \
  -H "Content-Type: application/json" \
  -H "X-LLMSIGNAL-KEY: ${LLMSIGNAL_API_KEY}" \
  -d "{\"siteId\":\"${LLMSIGNAL_SITE_ID}\",\"apiKey\":\"${LLMSIGNAL_API_KEY}\"}"

