#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SYNC_SRC="${ROOT}/scripts/gm-openapi-sync"

fail() {
  printf 'FAIL: %s\n' "$1" >&2
  exit 1
}

assert_contains() {
  local haystack="$1"
  local needle="$2"
  local message="$3"
  if [[ "$haystack" != *"$needle"* ]]; then
    fail "$message"
  fi
}

tmp="$(mktemp -d)"
mkdir -p "${tmp}/scripts"
cp "${SYNC_SRC}" "${tmp}/scripts/gm-openapi-sync"
chmod +x "${tmp}/scripts/gm-openapi-sync"

cat >"${tmp}/scripts/graymatter_api.sh" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
printf '%s\n' "$*" >>"${TEST_GRAYMATTER_API_LOG:?}"
if [[ "$*" != "GET /api-docs" ]]; then
  echo "unexpected graymatter_api call: $*" >&2
  exit 2
fi
printf '{"openapi":"3.0.1","paths":{"/MemoryEntry":{},"/SwarmOps/graph":{}}}\n'
EOF
chmod +x "${tmp}/scripts/graymatter_api.sh"

export TEST_GRAYMATTER_API_LOG="${tmp}/api.log"
out="${tmp}/tmp/api-docs.json"
"${tmp}/scripts/gm-openapi-sync" "${out}" >/tmp/gm-openapi-sync.out

[[ -s "${out}" ]] || fail "gm-openapi-sync should write the OpenAPI JSON output"
assert_contains "$(cat "${TEST_GRAYMATTER_API_LOG}")" "GET /api-docs" "gm-openapi-sync should use graymatter_api.sh so auth, refresh, hosted base URL, and timeouts are shared"
assert_contains "$(cat "${out}")" '"/MemoryEntry"' "gm-openapi-sync should preserve the API docs payload"

printf 'PASS: gm_openapi_sync_test.sh\n'
