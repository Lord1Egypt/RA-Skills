#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AUDIT_SCRIPT="${SCRIPT_DIR}/openclaw_security_audit.sh"
LOG_PATH="${OPENCLAW_AUDIT_LOG:-${HOME}/openclaw-security-audit.log}"

if [[ ! -x "${AUDIT_SCRIPT}" ]]; then
  chmod +x "${AUDIT_SCRIPT}"
fi

START_MARKER="# OPENCLAW_SECURITY_AUDIT_START"
END_MARKER="# OPENCLAW_SECURITY_AUDIT_END"
CRON_LINE="0 23 * * * /bin/bash ${AUDIT_SCRIPT} >> ${LOG_PATH} 2>&1"

CURRENT_CRONTAB="$(mktemp)"
UPDATED_CRONTAB="$(mktemp)"

trap 'rm -f "${CURRENT_CRONTAB}" "${UPDATED_CRONTAB}"' EXIT

crontab -l 2>/dev/null > "${CURRENT_CRONTAB}" || true
awk -v start="${START_MARKER}" -v end="${END_MARKER}" '
  $0 == start { skip = 1; next }
  $0 == end { skip = 0; next }
  skip != 1 { print }
' "${CURRENT_CRONTAB}" > "${UPDATED_CRONTAB}"

{
  cat "${UPDATED_CRONTAB}"
  printf '%s\n' "${START_MARKER}"
  printf '%s\n' "${CRON_LINE}"
  printf '%s\n' "${END_MARKER}"
} | crontab -

printf 'Installed nightly cron at 23:00.\n'
printf 'Log file: %s\n' "${LOG_PATH}"
