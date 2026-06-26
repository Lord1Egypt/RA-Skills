#!/usr/bin/env bash
[ -n "${BASH_VERSION:-}" ] || exec bash "$0" "$@"

usage() {
  cat <<'EOF'
Usage:
  myreels-doctor.sh
  myreels-doctor.sh -h | --help

Description:
  Run environment checks for the MyReels shell scripts:
  - config file presence
  - required variables
  - local dependencies
  - live connectivity to /api/v1/models/api
  - response shape sanity check

Notes:
  The doctor checks live model discovery directly.
  It does not perform a full token validation because there is no dedicated
  lightweight auth-check endpoint in this skill package.
EOF
}

extract_message() {
  local payload="${1:-}"
  echo "$payload" | jq -r '
    .message
    // .error
    // (if (.data | type) == "object" then .data.message else null end)
    // "unknown"
  ' 2>/dev/null || echo "unknown"
}

case "${1:-}" in
  -h|--help)
    usage
    exit 0
    ;;
esac

source "$(dirname "$0")/_common.sh"

PASS="OK"
FAIL="FAIL"
WARN="WARN"
errors=0

echo "=== MyReels Environment Diagnostic ==="
echo ""

config_path="$(myreels_config_path)"

if [[ -f "$config_path" ]]; then
  echo "$PASS Config file found: $config_path"
else
  echo "$WARN Config file not found: $config_path"
  echo "  Environment variables can still work."
  echo "  Suggested config:"
  echo '  mkdir -p ~/.myreels && cat > ~/.myreels/config << EOF'
  echo '  MYREELS_BASE_URL="https://api.myreels.ai"'
  echo '  MYREELS_ACCESS_TOKEN="YOUR_ACCESS_TOKEN"'
  echo '  EOF'
fi

if [[ -n "${MYREELS_BASE_URL:-}" ]]; then
  echo "$PASS MYREELS_BASE_URL is set: $MYREELS_BASE_URL"
else
  echo "$FAIL MYREELS_BASE_URL is not set"
  errors=$((errors + 1))
fi

if [[ -n "${MYREELS_ACCESS_TOKEN:-}" ]]; then
  echo "$PASS MYREELS_ACCESS_TOKEN is set: $(myreels_mask_secret "$MYREELS_ACCESS_TOKEN")"
else
  echo "$FAIL MYREELS_ACCESS_TOKEN is not set"
  echo "  Create one at: https://myreels.ai/developer"
  errors=$((errors + 1))
fi

echo ""
for cmd in curl jq; do
  if command -v "$cmd" >/dev/null 2>&1; then
    ver=$("$cmd" --version 2>&1 | head -1)
    echo "$PASS $cmd is installed: $ver"
  else
    echo "$FAIL $cmd is not installed"
    echo "  Install it before using the bundled scripts."
    errors=$((errors + 1))
  fi
done

echo ""
if command -v curl >/dev/null 2>&1 && command -v jq >/dev/null 2>&1 && [[ -n "${MYREELS_BASE_URL:-}" ]]; then
  tmp_body=$(mktemp)
  tmp_err=$(mktemp)
  http_code=$(curl -sS \
    --connect-timeout 10 \
    --max-time 30 \
    -H "Accept: application/json" \
    -o "$tmp_body" \
    -w '%{http_code}' \
    "${MYREELS_BASE_URL%/}/api/v1/models/api" 2>"$tmp_err" || echo "000")
  resp=$(cat "$tmp_body")
  curl_err=$(cat "$tmp_err")
  rm -f "$tmp_body" "$tmp_err"

  if [[ "$http_code" == "200" ]]; then
    echo "$PASS Network: can reach ${MYREELS_BASE_URL%/}/api/v1/models/api"
    if jq -e '.data.items | type == "array"' >/dev/null 2>&1 <<<"$resp"; then
      model_count=$(echo "$resp" | jq '.data.items | length')
      echo "$PASS Live model response shape looks correct: $model_count model(s)"
    else
      echo "$FAIL Live model response is not in the expected shape"
      echo "  Message: $(extract_message "$resp")"
      errors=$((errors + 1))
    fi
  elif [[ "$http_code" == "000" ]]; then
    echo "$FAIL Network request failed before receiving an HTTP response"
    echo "  Curl error: ${curl_err:-unknown}"
    errors=$((errors + 1))
  else
    echo "$FAIL Live model endpoint returned HTTP $http_code"
    echo "  Message: $(extract_message "$resp")"
    errors=$((errors + 1))
  fi
else
  echo "$WARN Network check skipped because curl or jq is missing"
fi

echo ""
if [[ -n "${MYREELS_ACCESS_TOKEN:-}" ]]; then
  echo "$WARN Token validation is not fully exercised by myreels-doctor.sh"
  echo "  The token will be definitively checked on the first generate/query request."
fi

echo ""
echo "=== Summary ==="
if [[ "$errors" -eq 0 ]]; then
  echo "$PASS All required checks passed."
else
  echo "$FAIL $errors issue(s) found."
fi

exit "$errors"
