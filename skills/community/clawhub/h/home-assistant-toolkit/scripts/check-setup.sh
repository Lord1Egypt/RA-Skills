#!/usr/bin/env bash
#
# check-setup.sh — Verify skill configuration before use
#
# Security:
#   - ENV vars: HA_URL, HA_TOKEN, HA_HOST (read-only check)
#   - Endpoints: none (no network calls)
#   - File access: none
#
# Exit codes:
#   0 = configured and connected
#   1 = not configured (needs onboarding)
#   2 = configured but connection failed

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/common.sh"

if [[ -z "${HA_URL:-}" ]] && [[ -z "${HA_HOST:-}" ]]; then
    echo "NOT_CONFIGURED"
    echo "HA_URL and HA_HOST are both empty. Run onboarding first." >&2
    exit 1
fi

# Try to connect
echo "CONFIGURED"
if [[ -n "${HA_URL:-}" ]] && [[ -n "${HA_TOKEN:-}" ]]; then
    echo "Mode: REST API (${HA_URL})"
    if result=$(curl -sf -m 5 -H "Authorization: Bearer ${HA_TOKEN}" "${HA_URL}/api/config" 2>/dev/null); then
        version=$(echo "$result" | jq -r '.version // "unknown"')
        name=$(echo "$result" | jq -r '.location_name // "unknown"')
        echo "Connected: ${name} (HA ${version})"
        exit 0
    else
        echo "REST API connection failed" >&2
        exit 2
    fi
elif [[ -n "${HA_HOST:-}" ]]; then
    echo "Mode: SSH (${HA_SSH_USER}@${HA_HOST}:${HA_SSH_PORT})"
    if ssh_cmd "echo ok" &>/dev/null; then
        echo "SSH connected"
        exit 0
    else
        echo "SSH connection failed" >&2
        exit 2
    fi
fi
