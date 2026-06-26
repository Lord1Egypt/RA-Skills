#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
GM_ACTIVATE_SRC="${ROOT}/scripts/gm-activate"
GM_LOGIN_SRC="${ROOT}/scripts/gm-login"

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

assert_file_exists() {
  local path="$1"
  local message="$2"
  if [[ ! -e "$path" ]]; then
    fail "$message"
  fi
}

make_fake_bin() {
  local dir="$1"

  cat >"${dir}/jq" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
printf '%s\n' '{"username":"valor-codex","password":"test-password"}'
EOF
  chmod +x "${dir}/jq"

  cat >"${dir}/curl" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

headers_file=""
cookie_jar=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    -D)
      headers_file="$2"
      shift 2
      ;;
    -c)
      cookie_jar="$2"
      shift 2
      ;;
    *)
      shift
      ;;
  esac
done

if [[ -n "${headers_file}" ]]; then
  cat >"${headers_file}" <<'HEADERS'
HTTP/1.1 200 OK
Set-Cookie: VALKYR_AUTH=test-token; Path=/; HttpOnly
HEADERS
fi

if [[ -n "${cookie_jar}" ]]; then
  cat >"${cookie_jar}" <<'COOKIES'
# Netscape HTTP Cookie File
api-0.valkyrlabs.com	FALSE	/	FALSE	0	VALKYR_AUTH	test-token
COOKIES
fi

printf '{}\n'
EOF
  chmod +x "${dir}/curl"

  cat >"${dir}/security" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
printf '%s\n' "$*" >>"${TEST_SECURITY_LOG}"
EOF
  chmod +x "${dir}/security"

  cat >"${dir}/hostname" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
printf 'test-host\n'
EOF
  chmod +x "${dir}/hostname"
}

make_activation_fixture() {
  local fixture_dir="$1"
  local smoke_mode="$2"

  mkdir -p "${fixture_dir}"
  cp "${GM_ACTIVATE_SRC}" "${fixture_dir}/gm-activate"
  cp "${GM_LOGIN_SRC}" "${fixture_dir}/gm-login"
  chmod +x "${fixture_dir}/gm-activate"
  chmod +x "${fixture_dir}/gm-login"

  cat >"${fixture_dir}/gm-install-check" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
printf 'install check passed\n'
EOF
  chmod +x "${fixture_dir}/gm-install-check"

  if [[ "${smoke_mode}" == "success" ]]; then
    cat >"${fixture_dir}/gm-smoke" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
printf 'smoke ok\n'
EOF
  else
    cat >"${fixture_dir}/gm-smoke" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
printf 'curl: (22) The requested URL returned error: 402\n' >&2
printf '{"error":"INSUFFICIENT_FUNDS"}\n' >&2
exit 22
EOF
  fi
  chmod +x "${fixture_dir}/gm-smoke"

  cat >"${fixture_dir}/gm-register-agent" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
: >"${TEST_REGISTER_CALLED}"
printf 'registered\n'
EOF
  chmod +x "${fixture_dir}/gm-register-agent"

  cat >"${fixture_dir}/gm-openapi-sync" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
: >"${TEST_SYNC_CALLED}"
printf 'synced\n'
EOF
  chmod +x "${fixture_dir}/gm-openapi-sync"

  cat >"${fixture_dir}/gm-openapi-summary" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
printf 'summary\n'
EOF
  chmod +x "${fixture_dir}/gm-openapi-summary"
}

run_activate() {
  local smoke_mode="$1"
  local temp_root
  local fake_bin
  local fixture_dir

  temp_root="$(mktemp -d)"
  fake_bin="${temp_root}/bin"
  fixture_dir="${temp_root}/scripts"
  mkdir -p "${fake_bin}"

  make_fake_bin "${fake_bin}"
  make_activation_fixture "${fixture_dir}" "${smoke_mode}"

  export TEST_SECURITY_LOG="${temp_root}/security.log"
  export TEST_REGISTER_CALLED="${temp_root}/register.called"
  export TEST_SYNC_CALLED="${temp_root}/sync.called"

  local output
  local status=0
  set +e
  output="$(
    PATH="${fake_bin}:/usr/bin:/bin" \
    GRAYMATTER_USERNAME="valor-codex" \
    GRAYMATTER_PASSWORD="secret" \
    OPENCLAW_AGENT_NAME="valor-codex" \
    OPENCLAW_AGENT_ROLE="job-automation" \
    "${fixture_dir}/gm-activate" 2>&1
  )"
  status=$?
  set -e

  printf '%s\n' "${status}"
  printf '%s\n' "${temp_root}"
  printf '%s' "${output}"
}

test_activate_stores_runtime_keychain_service() {
  local result
  local status
  local temp_root
  local output

  result="$(run_activate success)"
  status="$(printf '%s\n' "${result}" | sed -n '1p')"
  temp_root="$(printf '%s\n' "${result}" | sed -n '2p')"
  output="$(printf '%s\n' "${result}" | tail -n +3)"

  [[ "${status}" == "0" ]] || fail "gm-activate should succeed in the happy path"

  local security_log
  security_log="$(cat "${temp_root}/security.log")"
  assert_contains "${security_log}" "-s VALKYR_AUTH" "gm-activate should store the token under the VALKYR_AUTH keychain service"
  assert_contains "${output}" "GrayMatter activation complete" "gm-activate should report completion in the happy path"
}

test_activate_continues_when_smoke_query_is_credit_gated() {
  local result
  local status
  local temp_root
  local output

  result="$(run_activate insufficient-funds)"
  status="$(printf '%s\n' "${result}" | sed -n '1p')"
  temp_root="$(printf '%s\n' "${result}" | sed -n '2p')"
  output="$(printf '%s\n' "${result}" | tail -n +3)"

  [[ "${status}" == "0" ]] || fail "gm-activate should continue when gm-smoke fails with insufficient funds"
  assert_file_exists "${temp_root}/register.called" "gm-activate should still register the agent when query credits are unavailable"
  assert_file_exists "${temp_root}/sync.called" "gm-activate should still sync the OpenAPI when query credits are unavailable"
  assert_contains "${output}" "limited memory query capability" "gm-activate should explain the degraded activation state"
}

test_activate_stores_runtime_keychain_service
test_activate_continues_when_smoke_query_is_credit_gated

printf 'PASS: gm_activate_test.sh\n'
