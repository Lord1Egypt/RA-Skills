#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCRIPT_SRC="${ROOT}/scripts/gm-install-check"

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

  cat >"${dir}/security" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
if [[ "$*" == *"-a default -s VALKYR_AUTH -w"* ]]; then
  printf '%s\n' 'eyJhbGciOiJub25lIn0.eyJyb2xlcyI6WyJFVkVSWU9ORSIsIkZSRUUiXSwiYXV0aG9yaXRpZXMiOlsiRlJFRSJdLCJzY29wZXMiOlsiU0NPUEVfc2NoZW1hLnJlYWQiXX0.'
  exit 0
fi
if [[ "$*" == *"-a default -s VALKYR_AUTH_USERNAME -w"* ]]; then
  printf '%s\n' 'valor'
  exit 0
fi
exit 1
EOF
  chmod +x "${dir}/security"

  cat >"${dir}/gm-login" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
printf 'export VALKYR_API_BASE="https://api-0.valkyrlabs.com/v1"\n'
printf 'export VALKYR_AUTH_TOKEN="eyJhbGciOiJub25lIn0.eyJyb2xlcyI6WyJFVkVSWU9ORSIsIkFETUlOIl0sInNjb3BlcyI6WyJTQ09QRV9zY2hlbWEucmVhZCIsIlNDT1BFX3NjaGVtYS53cml0ZSJdLCJleHAiOjQxMDI0NDQ4MDB9."\n'
printf 'export VALKYR_USERNAME="valor"\n'
EOF
  chmod +x "${dir}/gm-login"

  cat >"${dir}/curl" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
printf '{}'
EOF
  chmod +x "${dir}/curl"
}

test_install_check_relogs_when_keychain_token_is_read_only() {
  local temp_root
  local fake_bin
  local script_copy
  local output

  temp_root="$(mktemp -d)"
  fake_bin="${temp_root}/bin"
  script_copy="${temp_root}/gm-install-check"
  mkdir -p "${fake_bin}"

  cp "${SCRIPT_SRC}" "${script_copy}"
  chmod +x "${script_copy}"
  make_fake_bin "${fake_bin}"

  output="$(PATH="${fake_bin}:/usr/bin:/bin" "${script_copy}" 2>&1)"

  assert_contains "${output}" "GrayMatter install check passed" "gm-install-check should pass after automatic re-login replaces a read-only token"
  assert_contains "${output}" "GrayMatter auth source detected" "gm-install-check should report auth success after re-login"
}

test_install_check_relogs_when_keychain_token_is_read_only

printf 'PASS: gm_install_check_test.sh\n'
