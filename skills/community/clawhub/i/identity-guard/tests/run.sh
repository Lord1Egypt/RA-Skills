#!/bin/bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC_DIR="${ROOT_DIR}/scripts"

pass_count=0
fail_count=0

fail() {
  echo "FAIL: $*" >&2
  fail_count=$((fail_count + 1))
}

pass() {
  echo "PASS: $*"
  pass_count=$((pass_count + 1))
}

assert_exit() {
  local expected="$1"
  local actual="$2"
  local label="$3"
  if [[ "${expected}" != "${actual}" ]]; then
    fail "${label} (expected exit ${expected}, got ${actual})"
  else
    pass "${label}"
  fi
}

with_temp_env() {
  local tmp_dir
  tmp_dir="$(mktemp -d)"

  mkdir -p "${tmp_dir}/identity-guard"
  cp -R "${SRC_DIR}" "${tmp_dir}/identity-guard/"

  export TEST_ROOT="${tmp_dir}/identity-guard"
  export TEST_SCRIPTS="${tmp_dir}/identity-guard/scripts"

  "$@"

  rm -rf "${tmp_dir}"
}

write_config() {
  cat <<EOF_CONFIG > "${TEST_ROOT}/identities.json"
$1
EOF_CONFIG
}

run_guard() {
  local sender_id="$1"
  local channel="${2:-}"
  if [[ -n "${channel}" ]]; then
    bash "${TEST_SCRIPTS}/guard.sh" "${sender_id}" "${channel}" >/dev/null 2>&1
  else
    bash "${TEST_SCRIPTS}/guard.sh" "${sender_id}" >/dev/null 2>&1
  fi
  echo $?
}

case_missing_config() {
  rm -f "${TEST_ROOT}/identities.json"
  local code
  code="$(run_guard "u1" "feishu")"
  assert_exit 1 "${code}" "deny when identities.json missing"
}

case_master_id_allows_channel() {
  write_config '{
  "channels": {
    "feishu": {
      "master_id": "u1",
      "allowlist": []
    }
  },
  "global_allowlist": []
}'
  local code
  code="$(run_guard "u1" "feishu")"
  assert_exit 0 "${code}" "allow master_id in matching channel"

  code="$(run_guard "u2" "feishu")"
  assert_exit 1 "${code}" "deny non-member in channel"
}

case_allowlist_allows_channel() {
  write_config '{
  "channels": {
    "feishu": {
      "master_id": "u1",
      "allowlist": ["u2"]
    }
  },
  "global_allowlist": []
}'
  local code
  code="$(run_guard "u2" "feishu")"
  assert_exit 0 "${code}" "allow allowlist in matching channel"
}

case_global_allowlist_allows_any_channel() {
  write_config '{
  "channels": {
    "feishu": {
      "master_id": "u1",
      "allowlist": []
    }
  },
  "global_allowlist": ["g1"]
}'
  local code
  code="$(run_guard "g1")"
  assert_exit 0 "${code}" "allow global allowlist without channel"
}

case_channel_isolated() {
  write_config '{
  "channels": {
    "feishu": {
      "master_id": "u1",
      "allowlist": []
    },
    "telegram": {
      "master_id": "u2",
      "allowlist": []
    }
  },
  "global_allowlist": []
}'
  local code
  code="$(run_guard "u2" "feishu")"
  assert_exit 1 "${code}" "deny other-channel master when channel specified"
}

case_allowlist_without_master() {
  write_config '{
  "channels": {
    "feishu": {
      "master_id": "",
      "allowlist": ["u2"]
    }
  },
  "global_allowlist": []
}'
  local code
  code="$(run_guard "u2" "feishu")"
  assert_exit 0 "${code}" "allow allowlist even without master_id"
}

case_add_user_updates_json() {
  write_config '{
  "channels": {
    "feishu": {
      "master_id": "",
      "allowlist": []
    }
  },
  "global_allowlist": []
}'

  set +e
  bash "${TEST_SCRIPTS}/add-user.sh" "u9" "feishu" >/dev/null 2>&1
  local add_code_1="$?"
  bash "${TEST_SCRIPTS}/add-user.sh" "g9" >/dev/null 2>&1
  local add_code_2="$?"
  set -e

  if [[ "${add_code_1}" -ne 0 ]]; then
    fail "add-user (channel) exited ${add_code_1}"
    return
  fi
  if [[ "${add_code_2}" -ne 0 ]]; then
    fail "add-user (global) exited ${add_code_2}"
    return
  fi

  TEST_CONFIG_PATH="${TEST_ROOT}/identities.json"
  set +e
  python3 - "${TEST_CONFIG_PATH}" <<'PY'
import json
from pathlib import Path
import sys

config_path = Path(sys.argv[1])
data = json.loads(config_path.read_text(encoding="utf-8"))
ok = True
ok = ok and "u9" in data["channels"]["feishu"]["allowlist"]
ok = ok and "g9" in data["global_allowlist"]
sys.exit(0 if ok else 1)
PY
  local code="$?"
  set -e
  assert_exit 0 "${code}" "add-user updates JSON correctly"
}

main() {
  with_temp_env case_missing_config
  with_temp_env case_master_id_allows_channel
  with_temp_env case_allowlist_allows_channel
  with_temp_env case_global_allowlist_allows_any_channel
  with_temp_env case_channel_isolated
  with_temp_env case_allowlist_without_master
  with_temp_env case_add_user_updates_json

  echo ""
  echo "Summary: ${pass_count} passed, ${fail_count} failed"
  if [[ ${fail_count} -gt 0 ]]; then
    exit 1
  fi
}

main "$@"
