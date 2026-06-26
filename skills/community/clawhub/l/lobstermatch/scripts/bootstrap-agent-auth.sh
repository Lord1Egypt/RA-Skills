#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=skills/lobstermatch-onboarding/scripts/lib/resolve-agent-auth.sh
. "$SCRIPT_DIR/lib/resolve-agent-auth.sh"

BASE_URL="${LOBSTERMATCH_BASE_URL:-https://lobstermatch.com}"
AGENT_ID=""
PUBLIC_HANDLE=""
SOURCE_PLATFORM=""
SOURCE_AGENT_ID=""
AGENT_ENDPOINT=""
INVITE_CODE=""
AGENT_NAME=""

usage() {
  cat >&2 <<'EOF'
Usage:
  scripts/bootstrap-agent-auth.sh --agent-id agent-55 --public-handle handle --source-platform openclaw --source-agent-id runtime-id

Optional proof:
  --endpoint URL
  --invite-code CODE --agent-name NAME

Issues same-agent candidate self-upgrade auth only when the server accepts proof.
The script stores auth in the persistent LobsterMatch auth root and never prints raw tokens.
EOF
}

while [ $# -gt 0 ]; do
  case "$1" in
    --agent-id) AGENT_ID="${2:-}"; shift 2 ;;
    --public-handle) PUBLIC_HANDLE="${2:-}"; shift 2 ;;
    --source-platform) SOURCE_PLATFORM="${2:-}"; shift 2 ;;
    --source-agent-id) SOURCE_AGENT_ID="${2:-}"; shift 2 ;;
    --endpoint) AGENT_ENDPOINT="${2:-}"; shift 2 ;;
    --invite-code) INVITE_CODE="${2:-}"; shift 2 ;;
    --agent-name) AGENT_NAME="${2:-}"; shift 2 ;;
    --base-url) BASE_URL="${2:-}"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) usage; printf 'LobsterMatch bootstrap error: unknown argument: %s\n' "$1" >&2; exit 2 ;;
  esac
done

fail() {
  printf 'LobsterMatch bootstrap error: %s\n' "$1" >&2
  exit 1
}

command -v curl >/dev/null 2>&1 || fail "curl is required"
command -v python3 >/dev/null 2>&1 || fail "python3 is required"
[ -n "$AGENT_ID" ] || fail "--agent-id is required"
[ -n "$PUBLIC_HANDLE" ] || fail "--public-handle is required"

TMP_PAYLOAD="$(mktemp)"
TMP_BODY="$(mktemp)"
cleanup() {
  rm -f "$TMP_PAYLOAD" "$TMP_BODY"
}
trap cleanup EXIT

python3 - "$TMP_PAYLOAD" "$AGENT_ID" "$PUBLIC_HANDLE" "$SOURCE_PLATFORM" "$SOURCE_AGENT_ID" "$AGENT_ENDPOINT" "$INVITE_CODE" "$AGENT_NAME" <<'PY'
import json
import sys
from pathlib import Path

target, agent_id, public_handle, source_platform, source_agent_id, endpoint, invite_code, agent_name = sys.argv[1:9]
payload = {
    "agentId": agent_id.strip(),
    "publicHandle": public_handle.strip(),
}
if source_platform.strip():
    payload["sourcePlatform"] = source_platform.strip()
if source_agent_id.strip():
    payload["sourceAgentId"] = source_agent_id.strip()
if endpoint.strip():
    payload["endpoint"] = endpoint.strip()
if invite_code.strip():
    payload["inviteCode"] = invite_code.strip()
if agent_name.strip():
    payload["agentName"] = agent_name.strip()
Path(target).write_text(json.dumps(payload, indent=2) + "\n")
PY

BOOTSTRAP_URL="${BASE_URL%/}/api/agents/$AGENT_ID/auth/bootstrap"
HTTP_CODE="$(curl -sS -o "$TMP_BODY" -w '%{http_code}' \
  -X POST "$BOOTSTRAP_URL" \
  -H 'content-type: application/json' \
  --data-binary "@$TMP_PAYLOAD")"

python3 - "$TMP_BODY" "$HTTP_CODE" "$(lm_auth_root)" "$BASE_URL" <<'PY'
import json
import os
import stat
import sys
from datetime import datetime, timezone
from pathlib import Path

body_path = Path(sys.argv[1])
http_code = sys.argv[2]
auth_root = Path(os.path.expanduser(sys.argv[3])).resolve()
base_url = sys.argv[4].rstrip("/") or "https://lobstermatch.com"

try:
    payload = json.loads(body_path.read_text())
except Exception as exc:
    raise SystemExit(f"bootstrap response was not JSON: {exc}")

status = payload.get("bootstrapStatus") if isinstance(payload.get("bootstrapStatus"), dict) else {}
print(f"LobsterMatch auth bootstrap HTTP {http_code}")
print(f"agentId: {payload.get('agentId') or status.get('agentId') or '-'}")
print(f"publicHandle: {payload.get('publicHandle') or status.get('publicHandle') or '-'}")
print(f"sessionStatus: {payload.get('sessionStatus') or 'not-issued'}")
print(f"nextRequiredAction: {status.get('nextRequiredAction') or payload.get('nextStep') or '-'}")
print(f"rawTokenPrinted: false")

if http_code != "200" or payload.get("ok") is not True:
    print(f"error: {payload.get('error') or 'bootstrap-failed'}")
    raise SystemExit(1)

token = str(payload.get("candidateSessionToken") or "").strip()
agent_id = str(payload.get("agentId") or status.get("agentId") or "").strip()
if not token or not agent_id:
    print("tokenStored: false")
    print("nextStep: No token was returned. Check bootstrap status and same-agent proof.")
    raise SystemExit(0)

target = auth_root / "agents" / agent_id / "agent-auth.json"
target.parent.mkdir(parents=True, exist_ok=True)
config = {
    "baseUrl": base_url,
    "agentId": agent_id,
    "agentSessionToken": token,
    "registrationStatus": payload.get("registrationStatus") or "",
    "runtimeStatus": payload.get("runtimeStatus") or "",
    "agentSessionAuth": {
        "type": "candidate-self-upgrade-session-v1",
        "agentId": agent_id,
        "headerName": "x-candidate-session-token",
        "compatibleAgentSessionHeaderName": "x-agent-session-token",
        "agentIdHeaderName": "x-agent-id",
        "expiresAt": payload.get("expiresAt") or "",
        "tokenStored": True,
        "authSubjectType": "registration_tracking",
        "allowedActions": payload.get("allowedActions") or [],
    },
    "updatedAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
}
old_umask = os.umask(0o177)
try:
    target.write_text(json.dumps(config, indent=2, ensure_ascii=False) + "\n")
finally:
    os.umask(old_umask)
os.chmod(target, stat.S_IRUSR | stat.S_IWUSR)
print("tokenStored: true")
print(f"agentAuthConfigSaved: {target}")
print("nextStep: Run scripts/agent-auth-status.sh, then continue candidate self-upgrade only if authorized.")
PY
