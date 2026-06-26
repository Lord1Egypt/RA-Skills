#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOGIN_SRC="${ROOT}/scripts/gm-login"

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

make_fake_bin() {
  local dir="$1"

  cat >"${dir}/jq" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
if [[ "${1:-}" == "-nc" ]]; then
  printf '{"username":"%s","password":"%s"}\n' valor fixture-password
else
  /usr/bin/jq "$@"
fi
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

if [[ -n "$headers_file" ]]; then
  case "${TEST_LOGIN_SCENARIO:-write-capable}" in
    read-only)
      cat >"${headers_file}" <<'HEADERS'
HTTP/1.1 200 OK
Set-Cookie: VALKYR_AUTH=eyJhbGciOiJub25lIn0.eyJyb2xlcyI6WyJFVkVSWU9ORSJdLCJzY29wZXMiOlsiU0NPUEVfc2NoZW1hLnJlYWQiXSwidXNlcm5hbWUiOiJ2YWxvciJ9.; Path=/; HttpOnly
HEADERS
      ;;
    *)
      cat >"${headers_file}" <<'HEADERS'
HTTP/1.1 200 OK
Set-Cookie: VALKYR_AUTH=eyJhbGciOiJub25lIn0.eyJyb2xlcyI6WyJFVkVSWU9ORSIsIkFETUlOIl0sInNjb3BlcyI6WyJTQ09QRV9zY2hlbWEucmVhZCIsIlNDT1BFX3NjaGVtYS53cml0ZSJdLCJ1c2VybmFtZSI6InZhbG9yIn0.; Path=/; HttpOnly
HEADERS
      ;;
  esac
fi

if [[ -n "$cookie_jar" ]]; then
  case "${TEST_LOGIN_SCENARIO:-write-capable}" in
    read-only)
      cat >"${cookie_jar}" <<'COOKIES'
# Netscape HTTP Cookie File
api-0.valkyrlabs.com	FALSE	/	FALSE	0	VALKYR_AUTH	eyJhbGciOiJub25lIn0.eyJyb2xlcyI6WyJFVkVSWU9ORSJdLCJzY29wZXMiOlsiU0NPUEVfc2NoZW1hLnJlYWQiXSwidXNlcm5hbWUiOiJ2YWxvciJ9.
COOKIES
      ;;
    *)
      cat >"${cookie_jar}" <<'COOKIES'
# Netscape HTTP Cookie File
api-0.valkyrlabs.com	FALSE	/	FALSE	0	VALKYR_AUTH	eyJhbGciOiJub25lIn0.eyJyb2xlcyI6WyJFVkVSWU9ORSIsIkFETUlOIl0sInNjb3BlcyI6WyJTQ09QRV9zY2hlbWEucmVhZCIsIlNDT1BFX3NjaGVtYS53cml0ZSJdLCJ1c2VybmFtZSI6InZhbG9yIn0.
COOKIES
      ;;
  esac
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

  cat >"${dir}/osascript" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
cat >/dev/null
printf 'osascript called\n' >>"${TEST_OSASCRIPT_LOG}"
if [[ "${TEST_OSASCRIPT_STATUS:-0}" != "0" ]]; then
  exit "${TEST_OSASCRIPT_STATUS}"
fi
printf '%s\n' "${TEST_OSASCRIPT_RESPONSE:-popup-password}"
EOF
  chmod +x "${dir}/osascript"

  cat >"${dir}/mktemp" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

target_dir="${TMPDIR:-}"
if [[ -z "${target_dir}" || "${target_dir}" == "/blocked-tmp" ]]; then
  echo "mktemp: simulated default temp failure" >&2
  exit 1
fi

if [[ "${1:-}" == "-d" ]]; then
  template="${2:-tmpdir.XXXXXX}"
  mkdir -p "${target_dir}"
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

mkdir -p "${target_dir}"
created_file="${target_dir}/${template/XXXXXX/fixture}"
: >"${created_file}"
printf '%s\n' "${created_file}"
EOF
  chmod +x "${dir}/mktemp"
}

test_login_stores_token_and_reusable_credentials() {
  local temp_root
  local fake_bin
  local script_copy
  local output

  temp_root="$(mktemp -d)"
  fake_bin="${temp_root}/bin"
  script_copy="${temp_root}/gm-login"
  mkdir -p "${fake_bin}"

  cp "${LOGIN_SRC}" "${script_copy}"
  chmod +x "${script_copy}"
  make_fake_bin "${fake_bin}"
  export TEST_SECURITY_LOG="${temp_root}/security.log"
  export TEST_OSASCRIPT_LOG="${temp_root}/osascript.log"

  output="$(
    PATH="${fake_bin}:/usr/bin:/bin" \
    TMPDIR="${temp_root}" \
    TEST_LOGIN_SCENARIO="write-capable" \
    GRAYMATTER_USERNAME="valor" \
    GRAYMATTER_PASSWORD=fixture-password \
    "${script_copy}" keychain 2>&1
  )"

  local security_log
  security_log="$(cat "${temp_root}/security.log")"
  assert_contains "${security_log}" "add-generic-password -U -a valor -s VALKYR_AUTH -w eyJhbGciOiJub25lIn0.eyJyb2xlcyI6WyJFVkVSWU9ORSIsIkFETUlOIl0sInNjb3BlcyI6WyJTQ09QRV9zY2hlbWEucmVhZCIsIlNDT1BFX3NjaGVtYS53cml0ZSJdLCJ1c2VybmFtZSI6InZhbG9yIn0." "gm-login should store a username-scoped token"
  assert_contains "${security_log}" "add-generic-password -U -a default -s VALKYR_AUTH -w eyJhbGciOiJub25lIn0.eyJyb2xlcyI6WyJFVkVSWU9ORSIsIkFETUlOIl0sInNjb3BlcyI6WyJTQ09QRV9zY2hlbWEucmVhZCIsIlNDT1BFX3NjaGVtYS53cml0ZSJdLCJ1c2VybmFtZSI6InZhbG9yIn0." "gm-login should preserve the legacy default token alias"
  assert_contains "${security_log}" "add-generic-password -U -a default -s VALKYR_AUTH_USERNAME -w valor" "gm-login should remember the username for autonomous refresh"
  assert_contains "${security_log}" "add-generic-password -U -a valor -s VALKYR_AUTH_PASSWORD -w fixture-password" "gm-login should store the password under a username-scoped keychain entry"
  assert_contains "${output}" "Stored GrayMatter credentials securely in macOS/iCloud Keychain" "gm-login should report credential persistence"
}

test_login_uses_secure_password_popup_when_password_missing() {
  local temp_root
  local fake_bin
  local script_copy

  temp_root="$(mktemp -d)"
  fake_bin="${temp_root}/bin"
  script_copy="${temp_root}/gm-login"
  mkdir -p "${fake_bin}"

  cp "${LOGIN_SRC}" "${script_copy}"
  chmod +x "${script_copy}"
  make_fake_bin "${fake_bin}"
  export TEST_SECURITY_LOG="${temp_root}/security.log"
  export TEST_OSASCRIPT_LOG="${temp_root}/osascript.log"

  PATH="${fake_bin}:/usr/bin:/bin" \
  TMPDIR="${temp_root}" \
  TEST_LOGIN_SCENARIO="write-capable" \
  GRAYMATTER_USERNAME="valor" \
  "${script_copy}" keychain >/dev/null 2>&1

  local security_log
  security_log="$(cat "${temp_root}/security.log")"
  assert_contains "$(cat "${temp_root}/osascript.log")" "osascript called" "gm-login should use the macOS secure password popup when no password is available"
  assert_contains "${security_log}" "add-generic-password -U -a valor -s VALKYR_AUTH_PASSWORD -w popup-password" "gm-login should persist the password returned by the secure popup"
}

test_login_falls_back_when_popup_and_default_tmp_fail() {
  local temp_root
  local fake_bin
  local script_copy
  local output

  temp_root="$(TMPDIR=/tmp mktemp -d)"
  fake_bin="${temp_root}/bin"
  script_copy="${temp_root}/gm-login"
  mkdir -p "${fake_bin}"

  cp "${LOGIN_SRC}" "${script_copy}"
  chmod +x "${script_copy}"
  make_fake_bin "${fake_bin}"
  export TEST_SECURITY_LOG="${temp_root}/security.log"
  export TEST_OSASCRIPT_LOG="${temp_root}/osascript.log"
  export TEST_OSASCRIPT_STATUS="1"
  unset TEST_OSASCRIPT_RESPONSE

  output="$(
    printf 'fallback-password\n' | \
    PATH="${fake_bin}:/usr/bin:/bin" \
    TMPDIR="/blocked-tmp" \
    TEST_LOGIN_SCENARIO="write-capable" \
    GRAYMATTER_USERNAME="valor" \
    "${script_copy}" keychain 2>&1
  )"

  local security_log
  security_log="$(cat "${temp_root}/security.log")"
  assert_contains "$(cat "${temp_root}/osascript.log")" "osascript called" "gm-login should still attempt the macOS password popup first"
  assert_contains "${security_log}" "add-generic-password -U -a valor -s VALKYR_AUTH_PASSWORD -w fallback-password" "gm-login should fall back to terminal input when the popup fails"
  assert_contains "${output}" "Stored GrayMatter credentials securely in macOS/iCloud Keychain" "gm-login should still complete after temp and popup fallback"
}

test_login_rejects_read_only_token_by_default() {
  local temp_root
  local fake_bin
  local script_copy
  local output
  local status=0

  temp_root="$(mktemp -d)"
  fake_bin="${temp_root}/bin"
  script_copy="${temp_root}/gm-login"
  mkdir -p "${fake_bin}"

  cp "${LOGIN_SRC}" "${script_copy}"
  chmod +x "${script_copy}"
  make_fake_bin "${fake_bin}"
  export TEST_SECURITY_LOG="${temp_root}/security.log"
  export TEST_OSASCRIPT_LOG="${temp_root}/osascript.log"

  set +e
  output="$(
    PATH="${fake_bin}:/usr/bin:/bin" \
    TMPDIR="${temp_root}" \
    TEST_LOGIN_SCENARIO="read-only" \
    GRAYMATTER_USERNAME="valor" \
    GRAYMATTER_PASSWORD=fixture-password \
    "${script_copy}" keychain 2>&1
  )"
  status=$?
  set -e

  [[ "${status}" != "0" ]] || fail "gm-login should reject a read-only token by default"
  assert_contains "${output}" "read-only" "gm-login should explain that the issued token is read-only"
}

test_login_stores_token_and_reusable_credentials
test_login_uses_secure_password_popup_when_password_missing
test_login_falls_back_when_popup_and_default_tmp_fail
test_login_rejects_read_only_token_by_default

printf 'PASS: gm_login_test.sh\n'
