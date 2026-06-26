#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)

assert_file() {
  local path=$1
  if [ ! -f "$ROOT_DIR/$path" ]; then
    echo "missing required file: $path" >&2
    exit 1
  fi
}

assert_contains() {
  local path=$1
  local pattern=$2
  if ! grep -Eq "$pattern" "$ROOT_DIR/$path"; then
    echo "missing pattern '$pattern' in $path" >&2
    exit 1
  fi
}

assert_file "docs/openai-app-directory-submission.md"
assert_file "docs/privacy-policy.md"
assert_file "docs/reviewer-test-credentials.md"
assert_file "openai-app/submission-manifest.json"
assert_file "assets/logo.svg"
assert_file "assets/screenshot.svg"
assert_file "assets/composer-icon.svg"

assert_contains "docs/openai-app-directory-submission.md" "Apps SDK"
assert_contains "docs/openai-app-directory-submission.md" "/mcp"
assert_contains "docs/openai-app-directory-submission.md" "verified"
assert_contains "docs/openai-app-directory-submission.md" "api\\.apps\\.write"
assert_contains "docs/openai-app-directory-submission.md" "privacy policy"
assert_contains "docs/openai-app-directory-submission.md" "test credentials"
assert_contains "docs/privacy-policy.md" "Data We Collect"
assert_contains "docs/privacy-policy.md" "Retention"
assert_contains "docs/privacy-policy.md" "Deletion"
assert_contains "docs/reviewer-test-credentials.md" "Do not commit"
assert_contains "docs/reviewer-test-credentials.md" "MFA"
assert_contains "openai-app/submission-manifest.json" "\"mcpEndpointPath\": \"/mcp\""
assert_contains "openai-app/submission-manifest.json" "\"privacyPolicyUrl\""

if grep -R "REPLACE_WITH_PASSWORD\\|actual_password\\|VALKYR_AUTH_TOKEN=" "$ROOT_DIR/docs/reviewer-test-credentials.md" "$ROOT_DIR/openai-app/submission-manifest.json"; then
  echo "review readiness files must not contain committed secrets" >&2
  exit 1
fi

echo "openai_app_readiness_test: ok"
