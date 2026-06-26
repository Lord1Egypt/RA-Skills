#!/usr/bin/env bash
set -euo pipefail

# =============================================================================
# kemia connect — Register this OpenClaw instance via enrollment flow
#
# Usage: connect.sh <kemia-url>
#
# Resumable two-step design:
#   First call (no state):    POST /enroll → persist enrollment.json → show URL → EXIT
#   User clicks URL, confirms in browser, returns to OpenClaw.
#   Second call (state present): poll once →
#       pending   → "still waiting, try again in a moment"
#       completed → save config.json, export agents, clean up
#       expired   → clean up, tell user to re-run
#
# No long-running polling process — survives OpenClaw/Exec killing the shell.
# =============================================================================

KEMIA_URL_ARG="${1:-}"

WORKSPACE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
SKILL_DIR="${WORKSPACE}/skills/kemia"
CONFIG_FILE="${SKILL_DIR}/config.json"
STATE_FILE="${SKILL_DIR}/enrollment.json"
INSTANCE_NAME="${OPENCLAW_INSTANCE_NAME:-$(hostname)}"
AGENT_NAME="${OPENCLAW_AGENT_NAME:-CyberClaw}"

command -v jq >/dev/null 2>&1 || { echo "ERROR: jq is required. Install with: apt-get install jq"; exit 1; }
command -v curl >/dev/null 2>&1 || { echo "ERROR: curl is required."; exit 1; }

mkdir -p "${SKILL_DIR}"

# ─── Helpers ───────────────────────────────────────────────────────────────

json_get() {
  # $1 = file, $2 = jq expression
  jq -r "$2 // empty" "$1" 2>/dev/null || true
}

now_epoch() { date -u +%s; }

sha256_stdin() {
  # Portable sha256 of stdin → hex digest (no filename suffix)
  if command -v sha256sum >/dev/null 2>&1; then
    sha256sum | awk '{print $1}'
  elif command -v shasum >/dev/null 2>&1; then
    shasum -a 256 | awk '{print $1}'
  else
    echo ""
  fi
}

compute_fingerprint() {
  # Stable per (hostname, workspace) pair. Used by kemia to offer Re-Auth
  # instead of silently creating a duplicate instance when /connect is re-run
  # on the same machine. Hash means no hostname leakage.
  local raw digest
  raw="$(hostname 2>/dev/null || echo unknown)::${WORKSPACE}"
  digest=$(printf "%s" "${raw}" | sha256_stdin)
  if [ -n "${digest}" ]; then
    printf "sha256:%s" "${digest}"
  fi
}

iso_to_epoch() {
  # Portable ISO-8601 → epoch (GNU date, BSD date fallback)
  if date -u -d "$1" +%s >/dev/null 2>&1; then
    date -u -d "$1" +%s
  else
    date -u -j -f "%Y-%m-%dT%H:%M:%S" "${1%.*}" +%s 2>/dev/null || echo "0"
  fi
}

export_agent_files() {
  # $1 = kemia base URL, $2 = api key → writes agentId back to config.json
  local base="$1" key="$2"
  local files_json="[]"

  for md_file in SOUL.md IDENTITY.md USER.md MEMORY.md AGENTS.md TOOLS.md HEARTBEAT.md; do
    local filepath="${WORKSPACE}/${md_file}"
    if [ -f "${filepath}" ]; then
      local content
      content=$(jq -Rs '.' < "${filepath}")
      files_json=$(echo "${files_json}" | jq --arg fn "${md_file}" --argjson ct "${content}" '. + [{"filename": $fn, "content": $ct}]')
      echo "  ✓ ${md_file}"
    fi
  done

  if [ "$(echo "${files_json}" | jq 'length')" = "0" ]; then
    echo "  (no workspace .md files found — skipping export)"
    return 0
  fi

  local payload
  payload=$(jq -n --arg name "${AGENT_NAME}" --argjson files "${files_json}" '{name: $name, files: $files}')

  local response
  response=$(curl -sf -X POST \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer ${key}" \
    -d "${payload}" \
    "${base}/api/v1/agents") || {
    echo "ERROR: Agent export failed (HTTP error). Connection is saved; you can re-run /connect to retry export."
    return 1
  }

  local agent_id
  agent_id=$(echo "${response}" | jq -r '.agentId // empty')
  if [ -n "${agent_id}" ]; then
    jq --arg aid "${agent_id}" '. + {agentId: $aid}' "${CONFIG_FILE}" > "${CONFIG_FILE}.tmp" && mv "${CONFIG_FILE}.tmp" "${CONFIG_FILE}"
    chmod 600 "${CONFIG_FILE}"
    echo "✓ Agent '${AGENT_NAME}' exported (id: ${agent_id})"
  fi
}

finish_enrollment() {
  # $1 = status response JSON (must be status=completed)
  local response="$1"
  local api_key instance_id kemia_url code
  api_key=$(echo "${response}" | jq -r '.apiKey // empty')
  instance_id=$(echo "${response}" | jq -r '.instanceId // empty')
  kemia_url=$(json_get "${STATE_FILE}" '.kemiaUrl')
  code=$(json_get "${STATE_FILE}" '.code')

  if [ -z "${api_key}" ] || [ -z "${instance_id}" ]; then
    echo "ERROR: Enrollment completed but credentials missing in response."
    echo "This can happen if the 5-minute key-retention window elapsed."
    echo "Remove ${STATE_FILE} and run /connect again."
    exit 1
  fi

  cat > "${CONFIG_FILE}" <<EOF
{
  "apiKey": "${api_key}",
  "instanceId": "${instance_id}",
  "baseUrl": "${kemia_url}"
}
EOF
  chmod 600 "${CONFIG_FILE}"

  # Ack the server so it clears the stored encrypted key immediately.
  # Best-effort: failure here is not fatal — the key will be cleared when
  # the 5-minute retention window elapses anyway.
  if [ -n "${code}" ]; then
    curl -sf -X POST "${kemia_url}/api/v1/enroll/${code}/ack" >/dev/null 2>&1 || true
  fi

  rm -f "${STATE_FILE}"

  echo "✓ Connected. Instance: ${instance_id}"
  echo ""
  echo "Exporting agent config files..."
  export_agent_files "${kemia_url}" "${api_key}" || true

  echo ""
  echo "Done. You're logged in at kemia via the enrollment link."
  echo "Run /kemia-link anytime you need a fresh login URL."
}

poll_once() {
  # Reads STATE_FILE, polls once, acts on result. Returns 0 on success/still-pending, 1 on fatal error.
  local kemia_url poll_url
  kemia_url=$(json_get "${STATE_FILE}" '.kemiaUrl')
  poll_url=$(json_get "${STATE_FILE}" '.pollUrl')

  if [ -z "${kemia_url}" ] || [ -z "${poll_url}" ]; then
    echo "ERROR: enrollment.json is malformed. Removing and starting over."
    rm -f "${STATE_FILE}"
    return 1
  fi

  local response
  response=$(curl -sf "${kemia_url}${poll_url}" 2>/dev/null) || {
    echo "ERROR: Could not reach ${kemia_url}. Check connectivity and try again."
    return 1
  }

  local status
  status=$(echo "${response}" | jq -r '.status // empty')

  case "${status}" in
    completed)
      finish_enrollment "${response}"
      ;;
    pending)
      local enroll_url expires_at
      enroll_url=$(json_get "${STATE_FILE}" '.enrollUrl')
      expires_at=$(json_get "${STATE_FILE}" '.expiresAt')
      echo "Enrollment still pending — the user has not yet confirmed in the browser."
      echo ""
      echo "  Link: ${enroll_url}"
      echo "  Expires: ${expires_at}"
      echo ""
      echo "After the user clicks and confirms, run /kemia connect again to complete."
      ;;
    expired)
      echo "Enrollment expired. Cleaning up."
      rm -f "${STATE_FILE}"
      echo "Run /kemia connect <kemia-url> to start a new enrollment."
      return 1
      ;;
    *)
      echo "ERROR: Unexpected enrollment status: ${status}"
      echo "Raw response: ${response}"
      return 1
      ;;
  esac
}

start_new_enrollment() {
  # $1 = kemia base URL
  local kemia_url="$1"
  echo "Starting enrollment with ${kemia_url}..."

  local fingerprint payload response
  fingerprint=$(compute_fingerprint)
  if [ -n "${fingerprint}" ]; then
    payload=$(jq -n --arg name "${INSTANCE_NAME}" --arg fp "${fingerprint}" \
      '{name: $name, orchestrator: "openclaw", fingerprint: $fp}')
  else
    payload=$(jq -n --arg name "${INSTANCE_NAME}" \
      '{name: $name, orchestrator: "openclaw"}')
  fi
  response=$(curl -sf -X POST \
    -H "Content-Type: application/json" \
    -d "${payload}" \
    "${kemia_url}/api/v1/enroll") || {
    echo "ERROR: Could not start enrollment. Check the URL and try again."
    exit 1
  }

  local enroll_url poll_url expires_at
  enroll_url=$(echo "${response}" | jq -r '.enrollUrl')
  poll_url=$(echo "${response}" | jq -r '.pollUrl')
  expires_at=$(echo "${response}" | jq -r '.expiresAt')

  if [ -z "${enroll_url}" ] || [ "${enroll_url}" = "null" ]; then
    echo "ERROR: Invalid response from kemia: ${response}"
    exit 1
  fi

  # Extract code from enrollUrl (last path segment)
  local code="${enroll_url##*/}"

  cat > "${STATE_FILE}" <<EOF
{
  "code": "${code}",
  "enrollUrl": "${enroll_url}",
  "pollUrl": "${poll_url}",
  "expiresAt": "${expires_at}",
  "kemiaUrl": "${kemia_url}"
}
EOF
  chmod 600 "${STATE_FILE}"

  echo ""
  echo "════════════════════════════════════════════"
  echo "  Open this link to connect:"
  echo ""
  echo "  ${enroll_url}"
  echo ""
  echo "  Expires: ${expires_at}"
  echo "════════════════════════════════════════════"
  echo ""
  echo "After the user confirms in the browser, run /kemia connect again"
  echo "(without arguments) to complete the setup."
}

# ─── Main dispatch ─────────────────────────────────────────────────────────

# Case A: already connected — verify and exit
if [ -f "${CONFIG_FILE}" ]; then
  BASE_URL=$(json_get "${CONFIG_FILE}" '.baseUrl')
  API_KEY=$(json_get "${CONFIG_FILE}" '.apiKey')

  if [ -n "${BASE_URL}" ] && [ -n "${API_KEY}" ]; then
    HTTP_CODE=$(curl -s -o /tmp/kemia-connect-probe.$$ -w "%{http_code}" \
      -H "Authorization: Bearer ${API_KEY}" \
      "${BASE_URL}/api/v1/status" 2>/dev/null || echo "000")

    case "${HTTP_CODE}" in
      200)
        INSTANCE_NAME_LIVE=$(jq -r '.instanceName // "unknown"' /tmp/kemia-connect-probe.$$ 2>/dev/null || echo "unknown")
        rm -f /tmp/kemia-connect-probe.$$
        echo "✓ Already connected to kemia at ${BASE_URL}"
        echo "  Instance: ${INSTANCE_NAME_LIVE}"
        echo ""
        echo "To start fresh, delete ${CONFIG_FILE} and run /kemia connect <url> again."
        exit 0
        ;;
      401|403)
        rm -f /tmp/kemia-connect-probe.$$
        echo "Config exists but API key is not accepted (HTTP ${HTTP_CODE}). Removing stale config."
        rm -f "${CONFIG_FILE}"
        ;;
      000|5*)
        rm -f /tmp/kemia-connect-probe.$$
        echo "ERROR: Could not reach ${BASE_URL} (HTTP ${HTTP_CODE}). Check connectivity."
        echo "Config is preserved. Try /kemia-status once kemia is reachable."
        exit 1
        ;;
      *)
        rm -f /tmp/kemia-connect-probe.$$
        echo "ERROR: Unexpected status check result (HTTP ${HTTP_CODE}). Config preserved."
        exit 1
        ;;
    esac
  fi
fi

# Case B: pending enrollment — resume by polling once
if [ -f "${STATE_FILE}" ]; then
  EXPIRES_AT=$(json_get "${STATE_FILE}" '.expiresAt')
  if [ -n "${EXPIRES_AT}" ]; then
    EXPIRES_EPOCH=$(iso_to_epoch "${EXPIRES_AT}")
    if [ "${EXPIRES_EPOCH}" != "0" ] && [ "$(now_epoch)" -gt "${EXPIRES_EPOCH}" ]; then
      echo "Previous enrollment expired (deadline: ${EXPIRES_AT}). Cleaning up."
      rm -f "${STATE_FILE}"
      # Fall through to Case C
    else
      poll_once
      exit $?
    fi
  fi
fi

# Case C: fresh enrollment — argument required
if [ -z "${KEMIA_URL_ARG}" ]; then
  echo "Usage: /kemia connect <kemia-url>"
  echo ""
  echo "Example: /kemia connect https://kemia.byte5.ai"
  exit 1
fi

start_new_enrollment "${KEMIA_URL_ARG%/}"
