#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

fail() {
  printf 'FAIL: %s\n' "$1" >&2
  exit 1
}

assert_contains() {
  local pattern="$1"
  local file="$2"
  if ! grep -q "$pattern" "$ROOT/$file"; then
    fail "Expected '$pattern' in $file"
  fi
}

assert_absent() {
  local pattern="$1"
  shift
  local matches
  matches="$(grep -R -n "$pattern" "$@" 2>/dev/null || true)"
  if [[ -n "$matches" ]]; then
    printf '%s\n' "$matches" >&2
    fail "Unexpected stale docs or naming pattern"
  fi
}

DOC_FILES=(
  "$ROOT/README.md"
  "$ROOT/SKILL.md"
  "$ROOT/mcp-server/README.md"
  "$ROOT/docs"
  "$ROOT/scripts"
  "$ROOT/tests/gm_light_bootstrap_test.sh"
  "$ROOT/tests/gm_light_up_test.sh"
)

old_smoke="gm-light-"'smoke'
future_sample="future local runnable sample"
future_service="provide a runnable GrayMatter Light local service"

assert_absent "$old_smoke" "${DOC_FILES[@]}"
assert_absent "$future_sample" "${DOC_FILES[@]}"
assert_absent "$future_service" "${DOC_FILES[@]}"

assert_contains "gm-light-json-smoke" "README.md"
assert_contains "gm-light-json-smoke" "docs/graymatter-light.md"
assert_contains "gm-light-json-smoke" "scripts/package_graymatter.py"
assert_contains "THORAPI_TEMPLATE=/app/api.hbs.yaml" "README.md"
assert_contains "THORAPI_SPEC=/app/api.yaml" "README.md"
assert_contains "THORAPI_TEMPLATE=/app/api.hbs.yaml" "docs/graymatter-light.md"
assert_contains "THORAPI_SPEC=/app/api.yaml" "docs/graymatter-light.md"
assert_contains "api.hbs.yaml template" "README.md"
assert_contains "rendered api.yaml" "README.md"
assert_contains "GrayMatter Light" "mcp-server/README.md"
assert_contains "VALKYR_API_BASE=http://localhost:8080" "mcp-server/README.md"

echo "docs_consistency_test: ok"
