#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
API_SRC="${ROOT}/scripts/graymatter_api.sh"

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

assert_file_missing() {
  local path="$1"
  local message="$2"
  if [[ -e "$path" ]]; then
    fail "$message"
  fi
}

make_fake_bin() {
  local dir="$1"

cat >"${dir}/curl" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

out_file=""
headers_file=""
all_args="$*"
if [[ -n "${TEST_CURL_LOG:-}" ]]; then
  printf '%s\n' "$all_args" >>"${TEST_CURL_LOG}"
fi
while [[ $# -gt 0 ]]; do
  case "$1" in
    -o)
      out_file="$2"
      shift 2
      ;;
    -D)
      headers_file="$2"
      shift 2
      ;;
    *)
      shift
      ;;
  esac
done

if [[ -z "$out_file" ]]; then
  echo "Missing -o output file" >&2
  exit 2
fi

case "${TEST_CURL_SCENARIO:-success}" in
  success)
    printf '{"ok":true}\n' >"${out_file}"
    if [[ -n "$headers_file" ]]; then
      printf 'HTTP/1.1 200 OK\n' >"${headers_file}"
    fi
    printf '200'
    ;;
  expired-token-must-refresh-first)
    if [[ "$all_args" == *"/auth/login"* ]]; then
      printf '{"%s":"%s"}\n' token refreshed-token >"${out_file}"
      if [[ -n "$headers_file" ]]; then
        printf 'HTTP/1.1 200 OK\nSet-Cookie: VALKYR_AUTH=refreshed-token; Path=/; HttpOnly\n' >"${headers_file}"
      fi
      printf '200'
    elif [[ "$all_args" == *"expired-jwt-token"* ]]; then
      printf '{"error":"EXPIRED_TOKEN_USED"}\n' >"${out_file}"
      if [[ -n "$headers_file" ]]; then
        printf 'HTTP/1.1 500 Internal Server Error\n' >"${headers_file}"
      fi
      printf '500'
    else
      printf '{"ok":true,"%s":"%s"}\n' token refreshed-token >"${out_file}"
      if [[ -n "$headers_file" ]]; then
        printf 'HTTP/1.1 200 OK\n' >"${headers_file}"
      fi
      printf '200'
    fi
    ;;
  insufficient-funds)
    printf '{"error":"INSUFFICIENT_FUNDS","insufficientFunds":true}\n' >"${out_file}"
    if [[ -n "$headers_file" ]]; then
      printf 'HTTP/1.1 402 Payment Required\n' >"${headers_file}"
    fi
    printf '402'
    ;;
  unauthorized-then-refresh)
    state_file="${TEST_CURL_STATE_FILE:?}"
    count=0
    if [[ -f "$state_file" ]]; then
      count="$(cat "$state_file")"
    fi

    if [[ "$all_args" == *"/auth/login"* ]]; then
      printf '{"%s":"%s"}\n' token refreshed-token >"${out_file}"
      if [[ -n "$headers_file" ]]; then
        printf 'HTTP/1.1 200 OK\nSet-Cookie: VALKYR_AUTH=refreshed-token; Path=/; HttpOnly\n' >"${headers_file}"
      fi
      printf '200'
    elif [[ "$count" == "0" ]]; then
      printf '{"error":"UNAUTHORIZED"}\n' >"${out_file}"
      if [[ -n "$headers_file" ]]; then
        printf 'HTTP/1.1 401 Unauthorized\n' >"${headers_file}"
      fi
      printf '1' >"$state_file"
      printf '401'
    else
      printf '{"ok":true,"%s":"%s"}\n' token refreshed-token >"${out_file}"
      if [[ -n "$headers_file" ]]; then
        printf 'HTTP/1.1 200 OK\n' >"${headers_file}"
      fi
      printf '200'
    fi
    ;;
  transport-fail)
    echo "curl transport failure" >&2
    exit 7
    ;;
  *)
    echo "Unknown TEST_CURL_SCENARIO" >&2
    exit 2
    ;;
esac
EOF
  chmod +x "${dir}/curl"

  cat >"${dir}/security" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

printf '%s\n' "$*" >>"${TEST_SECURITY_LOG}"

cmd="${1:-}"
shift || true

case "$cmd" in
  find-generic-password)
    account=""
    service=""
    want_password=0
    while [[ $# -gt 0 ]]; do
      case "$1" in
        -a)
          account="$2"
          shift 2
          ;;
        -s)
          service="$2"
          shift 2
          ;;
        -w)
          want_password=1
          shift
          ;;
        *)
          shift
          ;;
      esac
    done

    if [[ "$want_password" != "1" ]]; then
      exit 1
    fi

    if [[ "${TEST_SECURITY_SCENARIO:-}" == "missing-token" ]]; then
      exit 44
    fi

    if [[ "$service" == "VALKYR_AUTH" && "$account" == "valor" ]]; then
      if [[ "${TEST_SECURITY_SCENARIO:-}" == "readonly-token" ]]; then
        printf 'eyJhbGciOiJub25lIn0.eyJyb2xlcyI6WyJFVkVSWU9ORSJdLCJzY29wZXMiOlsiU0NPUEVfc2NoZW1hLnJlYWQiXSwidXNlcm5hbWUiOiJ2YWxvciJ9.\n'
      elif [[ "${TEST_SECURITY_SCENARIO:-}" == "expired-jwt-token" ]]; then
        printf 'eyJhbGciOiJub25lIn0.eyJleHAiOjEsInJvbGVzIjpbIkFETUlOIl0sInNjb3BlcyI6WyJTQ09QRV9zY2hlbWEucmVhZCIsIlNDT1BFX3NjaGVtYS53cml0ZSJdLCJ1c2VybmFtZSI6InZhbG9yIn0.invalid\n'
      else
        printf 'expired-token\n'
      fi
      exit 0
    fi

    if [[ "$service" == "VALKYR_AUTH_USERNAME" && "$account" == "default" ]]; then
      printf 'valor\n'
      exit 0
    fi

    if [[ "$service" == "VALKYR_AUTH_PASSWORD" && "$account" == "valor" ]]; then
      printf 'fixture-password\n'
      exit 0
    fi

    if [[ "$service" == "VALKYR_AUTH" && "$account" == "default" ]]; then
      if [[ "${TEST_SECURITY_SCENARIO:-}" == "readonly-token" ]]; then
        printf 'eyJhbGciOiJub25lIn0.eyJyb2xlcyI6WyJFVkVSWU9ORSJdLCJzY29wZXMiOlsiU0NPUEVfc2NoZW1hLnJlYWQiXSwidXNlcm5hbWUiOiJ2YWxvciJ9.\n'
      elif [[ "${TEST_SECURITY_SCENARIO:-}" == "expired-jwt-token" ]]; then
        printf 'eyJhbGciOiJub25lIn0.eyJleHAiOjEsInJvbGVzIjpbIkFETUlOIl0sInNjb3BlcyI6WyJTQ09QRV9zY2hlbWEucmVhZCIsIlNDT1BFX3NjaGVtYS53cml0ZSJdLCJ1c2VybmFtZSI6InZhbG9yIn0.invalid\n'
      else
        printf 'expired-token\n'
      fi
      exit 0
    fi

    exit 44
    ;;
  add-generic-password)
    exit 0
    ;;
  *)
    exit 0
    ;;
esac
EOF
  chmod +x "${dir}/security"

  cat >"${dir}/osascript" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
cat >/dev/null
printf 'osascript called\n' >>"${TEST_OSASCRIPT_LOG}"
exit "${TEST_OSASCRIPT_STATUS:-0}"
EOF
  chmod +x "${dir}/osascript"

  cat >"${dir}/powershell.exe" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
printf 'powershell called\n' >>"${TEST_POWERSHELL_LOG}"
exit "${TEST_POWERSHELL_STATUS:-0}"
EOF
  chmod +x "${dir}/powershell.exe"

  cat >"${dir}/open" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
printf 'open %s\n' "$*" >>"${TEST_OPEN_LOG}"
exit 0
EOF
  chmod +x "${dir}/open"

  cat >"${dir}/xdg-open" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
printf 'xdg-open %s\n' "$*" >>"${TEST_OPEN_LOG}"
exit 0
EOF
  chmod +x "${dir}/xdg-open"

  cat >"${dir}/cmd.exe" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
printf 'cmd.exe %s\n' "$*" >>"${TEST_OPEN_LOG}"
exit 0
EOF
  chmod +x "${dir}/cmd.exe"

  cat >"${dir}/gm-login" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
printf 'gm-login called\n' >>"${TEST_GM_LOGIN_LOG}"
printf 'export VALKYR_API_BASE="https://api-0.valkyrlabs.com/v1"\n'
case "${TEST_GM_LOGIN_SCENARIO:-write-capable}" in
  read-only)
    printf 'export VALKYR_AUTH_TOKEN="%s"\n' 'eyJhbGciOiJub25lIn0.eyJyb2xlcyI6WyJFVkVSWU9ORSJdLCJzY29wZXMiOlsiU0NPUEVfc2NoZW1hLnJlYWQiXSwidXNlcm5hbWUiOiJ2YWxvciJ9.'
    ;;
  *)
    printf 'export VALKYR_AUTH_TOKEN="%s"\n' 'eyJhbGciOiJub25lIn0.eyJyb2xlcyI6WyJFVkVSWU9ORSIsIkFETUlOIl0sInNjb3BlcyI6WyJTQ09QRV9zY2hlbWEucmVhZCIsIlNDT1BFX3NjaGVtYS53cml0ZSJdLCJ1c2VybmFtZSI6InZhbG9yIn0.'
    ;;
esac
EOF
  chmod +x "${dir}/gm-login"

  cat >"${dir}/mktemp" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

target_dir="${TMPDIR:-}"
if [[ -z "${target_dir}" || "${target_dir}" == "/blocked-tmp" ]]; then
  echo "mktemp: simulated default temp failure" >&2
  exit 1
fi

mkdir -p "${target_dir}"

if [[ "${1:-}" == "-d" ]]; then
  template="${2:-tmpdir.XXXXXX}"
  created_dir="${target_dir}/${template/XXXXXX/fixture}"
  mkdir -p "${created_dir}"
  printf '%s\n' "${created_dir}"
  exit 0
fi

if [[ "${1:-}" == "-t" ]]; then
  template="${2:-tmpfile.XXXXXX}"
else
  template="${1:-tmpfile.XXXXXX}"
fi

created_file="${target_dir}/${template/XXXXXX/fixture}"
: >"${created_file}"
printf '%s\n' "${created_file}"
EOF
  chmod +x "${dir}/mktemp"
}

run_api() {
  local bin_dir="$1"
  local script_path="$2"
  local tmp_dir="${3:-/tmp}"

  local output
  local status=0
  set +e
  output="$(
    PATH="${bin_dir}:/usr/bin:/bin" \
    TMPDIR="${tmp_dir}" \
    VALKYR_AUTH_TOKEN=test-token \
    "${script_path}" GET /MemoryEntry/stats 2>&1
  )"
  status=$?
  set -e

  printf '%s\n' "${status}"
  printf '%s' "${output}"
}

with_fixture() {
  local callback="$1"
  local temp_root
  local fake_bin
  local script_copy

  temp_root="$(mktemp -d)"
  fake_bin="${temp_root}/bin"
  script_copy="${temp_root}/graymatter_api.sh"
  mkdir -p "${fake_bin}"

  cp "${API_SRC}" "${script_copy}"
  chmod +x "${script_copy}"
  make_fake_bin "${fake_bin}"

  TEST_OSASCRIPT_LOG="${temp_root}/osascript.log"
  TEST_POWERSHELL_LOG="${temp_root}/powershell.log"
  TEST_OPEN_LOG="${temp_root}/open.log"
  TEST_SECURITY_LOG="${temp_root}/security.log"
  TEST_CURL_STATE_FILE="${temp_root}/curl.state"
  TEST_CURL_LOG="${temp_root}/curl.log"
  TEST_GM_LOGIN_LOG="${temp_root}/gm-login.log"
  export TEST_OSASCRIPT_LOG TEST_POWERSHELL_LOG TEST_OPEN_LOG TEST_SECURITY_LOG TEST_CURL_STATE_FILE TEST_CURL_LOG TEST_GM_LOGIN_LOG

  "${callback}" "${temp_root}" "${fake_bin}" "${script_copy}"
}

test_success_passthrough() {
  local _temp_root="$1"
  local fake_bin="$2"
  local script_copy="$3"

  export TEST_CURL_SCENARIO="success"
  local result
  local status
  local output

  result="$(run_api "${fake_bin}" "${script_copy}" "${_temp_root}")"
  status="$(printf '%s\n' "${result}" | sed -n '1p')"
  output="$(printf '%s\n' "${result}" | tail -n +2)"

  [[ "${status}" == "0" ]] || fail "graymatter_api should return success for HTTP 200"
  assert_contains "${output}" '{"ok":true}' "graymatter_api should print response body on success"
}

test_insufficient_funds_shows_links_and_uses_macos_prompt() {
  local temp_root="$1"
  local fake_bin="$2"
  local script_copy="$3"

  export TEST_CURL_SCENARIO="insufficient-funds"
  export TEST_OSASCRIPT_STATUS="0"
  export TEST_POWERSHELL_STATUS="0"
  export VALKYR_BUY_CREDITS_URL="https://example.com/buy"
  export VALKYR_HUMAN_SIGNUP_URL="https://example.com/signup"

  local result
  local status
  local output

  result="$(run_api "${fake_bin}" "${script_copy}" "${temp_root}")"
  status="$(printf '%s\n' "${result}" | sed -n '1p')"
  output="$(printf '%s\n' "${result}" | tail -n +2)"

  [[ "${status}" == "22" ]] || fail "graymatter_api should return 22 for HTTP errors"
  assert_contains "${output}" "Insufficient credits. Buy credits: https://example.com/buy" "graymatter_api should print buy-credits guidance"
  assert_contains "${output}" "Need an account? Sign up here: https://example.com/signup" "graymatter_api should print signup guidance"
  assert_file_exists "${temp_root}/osascript.log" "graymatter_api should trigger macOS prompt when available"
  assert_file_missing "${temp_root}/powershell.log" "graymatter_api should not invoke Windows prompt when macOS prompt succeeds"
}

test_insufficient_funds_falls_back_to_windows_prompt() {
  local temp_root="$1"
  local fake_bin="$2"
  local script_copy="$3"

  export TEST_CURL_SCENARIO="insufficient-funds"
  export TEST_OSASCRIPT_STATUS="1"
  export TEST_POWERSHELL_STATUS="0"
  export VALKYR_BUY_CREDITS_URL="https://valkyrlabs.com/graymatter/credits?source=graymatter&intent=recharge&operation=memory_query"
  export VALKYR_HUMAN_SIGNUP_URL="https://valkyrlabs.com/graymatter/activate?source=graymatter&intent=signup&operation=memory_query"

  local result
  local status

  result="$(run_api "${fake_bin}" "${script_copy}" "${temp_root}")"
  status="$(printf '%s\n' "${result}" | sed -n '1p')"

  [[ "${status}" == "22" ]] || fail "graymatter_api should still return 22 when insufficient funds occurs"
  assert_file_exists "${temp_root}/osascript.log" "graymatter_api should attempt macOS prompt first"
  assert_file_exists "${temp_root}/powershell.log" "graymatter_api should invoke Windows prompt fallback when macOS prompt fails"
}

with_fixture test_success_passthrough
with_fixture test_insufficient_funds_shows_links_and_uses_macos_prompt
with_fixture test_insufficient_funds_falls_back_to_windows_prompt
test_unauthorized_refreshes_token_from_keychain_credentials() {
  local temp_root="$1"
  local fake_bin="$2"
  local script_copy="$3"

  export TEST_CURL_SCENARIO="unauthorized-then-refresh"
  unset VALKYR_AUTH_TOKEN
  unset GRAYMATTER_USERNAME
  unset GRAYMATTER_PASSWORD
  unset VALKYR_USERNAME
  unset VALKYR_PASSWORD

  local result
  local status
  local output

  result="$(
    PATH="${fake_bin}:/usr/bin:/bin" \
    TMPDIR="${temp_root}" \
    "${script_copy}" GET /MemoryEntry/stats 2>&1
  )"
  status=$?
  output="$(printf '%s\n' "${result}")"

  [[ "${status}" == "0" ]] || fail "graymatter_api should recover from an expired token by refreshing it"
  assert_contains "${output}" "$(printf '{"ok":true,"%s":"%s"}' token refreshed-token)" "graymatter_api should retry the original request after refreshing the token"

  local security_log
  security_log="$(cat "${temp_root}/security.log")"
  assert_contains "${security_log}" "find-generic-password -a default -s VALKYR_AUTH_USERNAME -w" "graymatter_api should load the remembered username from Keychain"
  assert_contains "${security_log}" "find-generic-password -a valor -s VALKYR_AUTH_PASSWORD -w" "graymatter_api should load the remembered password from Keychain"
  assert_contains "${security_log}" "add-generic-password -U -a valor -s VALKYR_AUTH -w refreshed-token" "graymatter_api should update the username-scoped token"
}

test_missing_token_runs_login_before_request() {
  local temp_root="$1"
  local fake_bin="$2"
  local script_copy="$3"

  export TEST_CURL_SCENARIO="success"
  export TEST_SECURITY_SCENARIO="missing-token"
  unset VALKYR_AUTH_TOKEN
  unset GRAYMATTER_USERNAME
  unset GRAYMATTER_PASSWORD
  unset VALKYR_USERNAME
  unset VALKYR_PASSWORD

  local result
  local status
  local output

  result="$(
    PATH="${fake_bin}:/usr/bin:/bin" \
    TMPDIR="${temp_root}" \
    "${script_copy}" GET /MemoryEntry/stats 2>&1
  )"
  status=$?
  output="$(printf '%s\n' "${result}")"

  [[ "${status}" == "0" ]] || fail "graymatter_api should login when no token is available"
  assert_contains "$(cat "${temp_root}/gm-login.log")" "gm-login called" "graymatter_api should invoke gm-login when no token is available"
  assert_contains "${output}" '{"ok":true}' "graymatter_api should run the original request after login"
}

test_expired_keychain_token_refreshes_before_original_request() {
  local temp_root="$1"
  local fake_bin="$2"
  local script_copy="$3"

  export TEST_CURL_SCENARIO="expired-token-must-refresh-first"
  export TEST_SECURITY_SCENARIO="expired-jwt-token"
  unset VALKYR_AUTH_TOKEN
  unset GRAYMATTER_USERNAME
  unset GRAYMATTER_PASSWORD
  unset VALKYR_USERNAME
  unset VALKYR_PASSWORD

  local result
  local status
  local output

  result="$(
    PATH="${fake_bin}:/usr/bin:/bin" \
    TMPDIR="${temp_root}" \
    "${script_copy}" GET /MemoryEntry/stats 2>&1
  )"
  status=$?
  output="$(printf '%s\n' "${result}")"

  [[ "${status}" == "0" ]] || fail "graymatter_api should proactively refresh an expired keychain JWT before calling the target endpoint"
  assert_contains "${output}" "$(printf '{"ok":true,"%s":"%s"}' token refreshed-token)" "graymatter_api should use the refreshed token for the original request"

  local first_curl
  first_curl="$(sed -n '1p' "${temp_root}/curl.log")"
  assert_contains "${first_curl}" "/auth/login" "graymatter_api should call login before the original endpoint when the stored JWT is already expired"
}

test_curl_requests_use_default_timeouts() {
  local temp_root="$1"
  local fake_bin="$2"
  local script_copy="$3"

  export TEST_CURL_SCENARIO="success"

  PATH="${fake_bin}:/usr/bin:/bin" \
  TMPDIR="${temp_root}" \
  VALKYR_AUTH_TOKEN=test-token \
  "${script_copy}" GET /MemoryEntry/stats >/dev/null 2>&1

  local curl_log
  curl_log="$(cat "${temp_root}/curl.log")"
  assert_contains "${curl_log}" "--connect-timeout 5" "graymatter_api should set a default connect timeout"
  assert_contains "${curl_log}" "--max-time 20" "graymatter_api should set a default total request timeout"
}

test_success_uses_fallback_tempdir_when_default_tmp_fails() {
  local _temp_root="$1"
  local fake_bin="$2"
  local script_copy="$3"

  export TEST_CURL_SCENARIO="success"

  local result
  local status
  local output

  result="$(
    PATH="${fake_bin}:/usr/bin:/bin" \
    TMPDIR="/blocked-tmp" \
    VALKYR_AUTH_TOKEN=test-token \
    "${script_copy}" GET /MemoryEntry/stats 2>&1
  )"
  status=$?
  output="$(printf '%s\n' "${result}")"

  [[ "${status}" == "0" ]] || fail "graymatter_api should recover when the default temp directory is unavailable"
  assert_contains "${output}" '{"ok":true}' "graymatter_api should still complete successfully after temp fallback"
}

test_write_rejects_read_only_token_before_network_request() {
  local temp_root
  local fake_bin
  local script_copy
  local result
  local status=0

  temp_root="$(mktemp -d)"
  fake_bin="${temp_root}/bin"
  script_copy="${temp_root}/graymatter_api.sh"
  mkdir -p "${fake_bin}"

  cp "${API_SRC}" "${script_copy}"
  chmod +x "${script_copy}"
  make_fake_bin "${fake_bin}"

  TEST_OSASCRIPT_LOG="${temp_root}/osascript.log"
  TEST_POWERSHELL_LOG="${temp_root}/powershell.log"
  TEST_OPEN_LOG="${temp_root}/open.log"
  TEST_SECURITY_LOG="${temp_root}/security.log"
  TEST_CURL_STATE_FILE="${temp_root}/curl.state"
  TEST_CURL_LOG="${temp_root}/curl.log"
  TEST_GM_LOGIN_LOG="${temp_root}/gm-login.log"
  export TEST_OSASCRIPT_LOG TEST_POWERSHELL_LOG TEST_OPEN_LOG TEST_SECURITY_LOG TEST_CURL_STATE_FILE TEST_CURL_LOG TEST_GM_LOGIN_LOG
  export TEST_CURL_SCENARIO="success"
  export TEST_SECURITY_SCENARIO="readonly-token"
  export TEST_GM_LOGIN_SCENARIO="read-only"

  set +e
  result="$(
    PATH="${fake_bin}:/usr/bin:/bin" \
    TMPDIR="${temp_root}" \
    "${script_copy}" POST /MemoryEntry '{"type":"context","text":"x"}' 2>&1
  )"
  status=$?
  set -e

  [[ "${status}" != "0" ]] || fail "graymatter_api should reject a read-only token for write requests"
  assert_contains "${result}" "read-only" "graymatter_api should explain that the token lacks write access"
}

test_light_mode_allows_local_request_without_token() {
  local temp_root
  local fake_bin
  local script_copy
  local result
  local status=0

  temp_root="$(mktemp -d)"
  fake_bin="${temp_root}/bin"
  script_copy="${temp_root}/graymatter_api.sh"
  mkdir -p "${fake_bin}"

  cp "${API_SRC}" "${script_copy}"
  chmod +x "${script_copy}"
  make_fake_bin "${fake_bin}"

  TEST_OSASCRIPT_LOG="${temp_root}/osascript.log"
  TEST_POWERSHELL_LOG="${temp_root}/powershell.log"
  TEST_OPEN_LOG="${temp_root}/open.log"
  TEST_SECURITY_LOG="${temp_root}/security.log"
  TEST_CURL_STATE_FILE="${temp_root}/curl.state"
  TEST_CURL_LOG="${temp_root}/curl.log"
  TEST_GM_LOGIN_LOG="${temp_root}/gm-login.log"
  export TEST_OSASCRIPT_LOG TEST_POWERSHELL_LOG TEST_OPEN_LOG TEST_SECURITY_LOG TEST_CURL_STATE_FILE TEST_CURL_LOG TEST_GM_LOGIN_LOG
  export TEST_CURL_SCENARIO="success"
  export TEST_SECURITY_SCENARIO="missing-token"

  set +e
  result="$(
    PATH="${fake_bin}:/usr/bin:/bin" \
    TMPDIR="${temp_root}" \
    GRAYMATTER_LIGHT_MODE=true \
    VALKYR_API_BASE="http://localhost:8899" \
    "${script_copy}" POST /MemoryEntry '{"type":"context","text":"local"}' 2>&1
  )"
  status=$?
  set -e

  [[ "${status}" == "0" ]] || fail "graymatter_api should allow local light requests without hosted auth"
  assert_contains "${result}" '{"ok":true}' "graymatter_api should run the local light request"
  assert_file_missing "${temp_root}/gm-login.log" "graymatter_api should not run hosted login in light mode"
}

with_fixture test_success_passthrough
with_fixture test_insufficient_funds_shows_links_and_uses_macos_prompt
with_fixture test_insufficient_funds_falls_back_to_windows_prompt
with_fixture test_unauthorized_refreshes_token_from_keychain_credentials
with_fixture test_missing_token_runs_login_before_request
with_fixture test_expired_keychain_token_refreshes_before_original_request
with_fixture test_curl_requests_use_default_timeouts
with_fixture test_success_uses_fallback_tempdir_when_default_tmp_fails
test_write_rejects_read_only_token_before_network_request
test_light_mode_allows_local_request_without_token

printf 'PASS: graymatter_api_test.sh\n'
