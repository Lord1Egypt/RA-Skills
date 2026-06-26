#!/usr/bin/env bash

set -euo pipefail

VIRUSTOTAL_ALLOW_UPLOADS="${VIRUSTOTAL_ALLOW_UPLOADS:-0}"

usage() {
  cat <<'EOF'
Usage:
  openclaw_virustotal_check.sh --url <url>
  openclaw_virustotal_check.sh --file <path>

This helper is API-free. It prepares public VirusTotal review steps for the
OpenClaw browser tool.
EOF
}

fail() {
  printf '[FAIL] %s\n' "$*" >&2
  exit 1
}

info() {
  printf '[INFO] %s\n' "$*"
}

warn() {
  printf '[WARN] %s\n' "$*"
}

require_file() {
  [[ -f "$1" ]] || fail "File not found: $1"
}

sha256_file() {
  if command -v sha256sum >/dev/null 2>&1; then
    sha256sum "$1" | awk '{print $1}'
    return 0
  fi
  if command -v shasum >/dev/null 2>&1; then
    shasum -a 256 "$1" | awk '{print $1}'
    return 0
  fi
  fail "No SHA-256 tool found. Install sha256sum or shasum."
}

check_url() {
  local url="$1"

  [[ -n "${url}" ]] || fail "URL must not be empty."

  info "VirusTotal API-free URL workflow prepared."
  printf 'VT_BROWSER_URL=%s\n' "https://www.virustotal.com/gui/home/url"
  printf 'VT_SUBMIT_URL=%s\n' "${url}"
  printf 'OPENCLAW_BROWSER_COMMAND=%s\n' "browser.navigate https://www.virustotal.com/gui/home/url"
  printf 'OPENCLAW_BROWSER_NOTE=%s\n' "Use browser.snapshot and browser.act to submit the URL and inspect detections."
}

check_file() {
  local file_path="$1"
  local sha256
  local report_url

  require_file "${file_path}"
  sha256="$(sha256_file "${file_path}")"
  report_url="https://www.virustotal.com/gui/file/${sha256}/detection"

  info "VirusTotal API-free file workflow prepared."
  printf 'VT_FILE_SHA256=%s\n' "${sha256}"
  printf 'VT_GUI_REPORT=%s\n' "${report_url}"
  printf 'VT_BROWSER_UPLOAD=%s\n' "https://www.virustotal.com/gui/home/upload"
  printf 'OPENCLAW_BROWSER_NOTE=%s\n' "Open the report URL first. If no report exists and uploads are approved, use browser.upload on the upload page."

  if [[ "${VIRUSTOTAL_ALLOW_UPLOADS}" -eq 1 ]]; then
    printf 'VT_UPLOAD_ALLOWED=%s\n' "1"
  else
    printf 'VT_UPLOAD_ALLOWED=%s\n' "0"
    warn "Website upload is disabled unless the user explicitly approves it."
  fi
  printf 'USER_DECISION_REQUIRED=%s\n' "If VirusTotal flags this file, ask the user whether to keep or remove it."
}

main() {
  case "${1:-}" in
    --url)
      [[ $# -eq 2 ]] || { usage; exit 1; }
      check_url "$2"
      ;;
    --file)
      [[ $# -eq 2 ]] || { usage; exit 1; }
      check_file "$2"
      ;;
    *)
      usage
      exit 1
      ;;
  esac
}

main "$@"
