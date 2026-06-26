#!/usr/bin/env bash
# benchmark-sign.sh — Sign and execute a Benchmark API request via AWP Wallet.
#
# Usage: benchmark-sign.sh METHOD PATH [BODY]
#
# Environment:
#   BENCHMARK_API_URL  — Server URL (default: https://tapis1.awp.sh)
#   WALLET_ADDRESS     — Cached wallet address (auto-detected if unset)
#   AWP_SESSION_TOKEN  — Cached session token (auto-unlocked if unset)
#
# Examples:
#   benchmark-sign.sh GET  /api/v1/poll
#   benchmark-sign.sh POST /api/v1/questions '{"bs_id":"bs_math",...}'

set -euo pipefail

METHOD="${1:?Usage: benchmark-sign.sh METHOD PATH [BODY]}"
API_PATH="${2:?Usage: benchmark-sign.sh METHOD PATH [BODY]}"
BODY="${3:-}"

BENCHMARK_API_URL="${BENCHMARK_API_URL:-https://tapis1.awp.sh}"

# Auto-unlock wallet if no session token cached
if [ -z "${AWP_SESSION_TOKEN:-}" ]; then
  UNLOCK_OUT=$(awp-wallet unlock --duration 3600 2>/dev/null)
  # Try "sessionToken" first (newer awp-wallet), then "token" (older versions)
  AWP_SESSION_TOKEN=$(echo "$UNLOCK_OUT" \
    | grep -oE '"(sessionToken|token)"\s*:\s*"[^"]*"' | head -1 | sed 's/.*:.*"\(.*\)"/\1/')
  if [ -z "$AWP_SESSION_TOKEN" ]; then
    echo '{"ok":false,"error":"failed to unlock wallet — no session token"}' >&2
    exit 1
  fi
  export AWP_SESSION_TOKEN
fi

# Auto-detect wallet address if not cached
if [ -z "${WALLET_ADDRESS:-}" ]; then
  WALLET_ADDRESS=$(awp-wallet receive 2>/dev/null \
    | grep -oi '0x[0-9a-fA-F]\{40\}' | head -1)
  export WALLET_ADDRESS
fi

TIMESTAMP=$(date +%s)
BODY_HASH=$(printf '%s' "$BODY" | sha256sum | cut -d' ' -f1)
MESSAGE="${METHOD}${API_PATH}${TIMESTAMP}${BODY_HASH}"

# Sign via AWP Wallet (EIP-191 personal_sign)
SIGN_RESULT=$(awp-wallet sign-message \
  --token "$AWP_SESSION_TOKEN" --message "$MESSAGE" 2>/dev/null)
SIGNATURE=$(echo "$SIGN_RESULT" | grep -o '"signature":"[^"]*"' | head -1 | cut -d'"' -f4)
[ -z "$SIGNATURE" ] && SIGNATURE="$SIGN_RESULT"

if [ -n "$BODY" ]; then
  curl -s -X "$METHOD" \
    -H "Content-Type: application/json" \
    -H "X-Worker-Address: $WALLET_ADDRESS" \
    -H "X-Signature: $SIGNATURE" \
    -H "X-Timestamp: $TIMESTAMP" \
    -d "$BODY" \
    "${BENCHMARK_API_URL}${API_PATH}"
else
  curl -s -X "$METHOD" \
    -H "X-Worker-Address: $WALLET_ADDRESS" \
    -H "X-Signature: $SIGNATURE" \
    -H "X-Timestamp: $TIMESTAMP" \
    "${BENCHMARK_API_URL}${API_PATH}"
fi
