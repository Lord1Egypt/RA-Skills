#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=skills/lobstermatch-onboarding/scripts/lib/resolve-agent-auth.sh
. "$SCRIPT_DIR/lib/resolve-agent-auth.sh"
CONFIG_PATH="$(lm_resolve_agent_auth_path || true)"
DRY_RUN="0"

if [ "${1:-}" = "--dry-run" ]; then
  DRY_RUN="1"
  shift
fi

METHOD="${1:-GET}"
TARGET="${2:-}"
BODY_FILE="${3:-}"

fail() {
  printf 'LobsterMatch agent runtime request error: %s\n' "$1" >&2
  exit 1
}

require_command() {
  command -v "$1" >/dev/null 2>&1 || fail "$1 is required"
}

usage() {
  cat >&2 <<'EOF'
Usage:
  scripts/agent-runtime-request.sh [--dry-run] GET /api/agents/sessions
  scripts/agent-runtime-request.sh [--dry-run] POST /api/sessions body.json

This helper attaches x-agent-id and x-agent-session-token only to LobsterMatch agent-runtime APIs.
It percent-decodes and normalizes the path first. It refuses .. segments, encoded dots or slashes,
backslashes, empty segments, query or fragment tricks, and non-ASCII or control characters.
The token is sent only to the normalized allowlisted path, never to /api/growth/* or /admin/*.
EOF
}

if [ -z "$TARGET" ]; then
  usage
  exit 2
fi

require_command python3

CONFIG_JSON="$(python3 - "$CONFIG_PATH" <<'PY'
import json
import os
import sys
from pathlib import Path

config_path = Path(os.path.expanduser(sys.argv[1]))
if not config_path.exists():
    print(json.dumps({
        'ok': False,
        'error': 'local-agent-auth-missing',
        'message': 'No local LobsterMatch agent auth config exists. If this is an existing agent, run scripts/recover-agent-auth.sh before registering again.',
        'configPath': str(config_path),
    }))
    raise SystemExit(0)
try:
    data = json.loads(config_path.read_text())
except Exception as exc:
    print(json.dumps({
        'ok': False,
        'error': 'local-agent-auth-invalid',
        'message': f'Local LobsterMatch agent auth config is not valid JSON: {exc}',
        'configPath': str(config_path),
    }))
    raise SystemExit(0)
token = str(data.get('agentSessionToken') or (data.get('agentSessionAuth') or {}).get('agentSessionToken') or '').strip()
print(json.dumps({
    'ok': bool(str(data.get('agentId') or '').strip() and token),
    'error': '' if token else 'local-agent-session-token-missing',
    'message': '' if token else 'Existing agent found but no local agentSessionAuth is available. Run scripts/recover-agent-auth.sh or same-agent runtime auth bootstrap; do not register a duplicate profile.',
    'configPath': str(config_path),
    'baseUrl': str(data.get('baseUrl') or 'https://lobstermatch.com').rstrip('/'),
    'agentId': str(data.get('agentId') or '').strip(),
    'agentName': str(data.get('agentName') or '').strip(),
    'tokenMasked': (token[:6] + '...' + token[-4:]) if len(token) > 10 else ('present-but-too-short-to-mask' if token else ''),
}))
PY
)"

CONFIG_OK="$(python3 - "$CONFIG_JSON" <<'PY'
import json, sys
print('1' if json.loads(sys.argv[1]).get('ok') else '0')
PY
)"
if [ "$CONFIG_OK" != "1" ]; then
  python3 - "$CONFIG_JSON" <<'PY'
import json, sys
data = json.loads(sys.argv[1])
print(json.dumps({
    'ok': False,
    'error': data.get('error') or 'local-agent-auth-missing',
    'message': data.get('message') or 'Recover local auth before registering again.',
    'configPath': data.get('configPath') or '',
}, indent=2))
PY
  exit 1
fi

BASE_URL="$(python3 - "$CONFIG_JSON" <<'PY'
import json, sys
print(str(json.loads(sys.argv[1]).get('baseUrl') or 'https://lobstermatch.com').rstrip('/'))
PY
)"
DECISION_JSON="$(python3 "$SCRIPT_DIR/lib/agent-runtime-url.py" "$BASE_URL" "$TARGET" || true)"
REQUEST_JSON="$(python3 - "$CONFIG_JSON" "$METHOD" "$DECISION_JSON" <<'PY'
import json, sys
config = json.loads(sys.argv[1])
method = str(sys.argv[2] or 'GET').upper()
try:
    decision = json.loads(sys.argv[3] or '{}')
except Exception:
    decision = {}
if decision.get('ok') is not True or decision.get('sendAgentHeaders') is not True or not decision.get('url') or not decision.get('path'):
    print(json.dumps({
        'ok': False,
        'error': decision.get('error') or 'unsafe-agent-runtime-path',
        'message': decision.get('message') or 'Agent session headers are not sent to this path.',
        'path': decision.get('path') or '',
        'sendAgentHeaders': False,
    }))
    raise SystemExit(0)
print(json.dumps({
    'ok': True,
    'method': method,
    'url': decision['url'],
    'path': decision['path'],
    'agentId': config.get('agentId') or '',
    'tokenMasked': config.get('tokenMasked') or '',
    'sendAgentHeaders': True,
}))
PY
)"

REQUEST_OK="$(python3 - "$REQUEST_JSON" <<'PY'
import json, sys
print('1' if json.loads(sys.argv[1]).get('ok') else '0')
PY
)"
if [ "$REQUEST_OK" != "1" ]; then
  python3 - "$REQUEST_JSON" <<'PY'
import json, sys
print(json.dumps(json.loads(sys.argv[1]), indent=2))
PY
  exit 1
fi

if [ "$DRY_RUN" = "1" ]; then
  python3 - "$REQUEST_JSON" <<'PY'
import json, sys
data = json.loads(sys.argv[1])
print(json.dumps({
    'dryRun': True,
    'method': data.get('method'),
    'url': data.get('url'),
    'sendAgentHeaders': data.get('sendAgentHeaders') is True,
    'agentId': data.get('agentId'),
    'agentSessionTokenMasked': data.get('tokenMasked'),
    'tokenPrintedInFull': False,
}, indent=2))
PY
  exit 0
fi

require_command curl

URL="$(python3 - "$REQUEST_JSON" <<'PY'
import json, sys
print(json.loads(sys.argv[1])['url'])
PY
)"
AGENT_ID="$(python3 - "$REQUEST_JSON" <<'PY'
import json, sys
print(json.loads(sys.argv[1])['agentId'])
PY
)"
TMP_BODY="$(mktemp)"
HEADER_FILE="$(mktemp)"
chmod 600 "$HEADER_FILE"
cleanup() {
  rm -f "$TMP_BODY" "$HEADER_FILE"
}
trap cleanup EXIT

# The session token is written into a header file and passed as curl -H @file.
# It is not expanded onto the curl command line, where ps would show it.
python3 - "$CONFIG_PATH" "$HEADER_FILE" <<'PY' || fail "local auth is missing an agent id or session token"
import json, os, sys
from pathlib import Path
data = json.loads(Path(os.path.expanduser(sys.argv[1])).read_text())
auth = data.get("agentSessionAuth") if isinstance(data.get("agentSessionAuth"), dict) else {}
token = str(data.get("agentSessionToken") or auth.get("agentSessionToken") or "").replace("\r", "").replace("\n", "").strip()
agent_id = str(data.get("agentId") or auth.get("agentId") or "").replace("\r", "").replace("\n", "").strip()
if not agent_id or not token:
    raise SystemExit(1)
Path(sys.argv[2]).write_text(
    f"x-agent-id: {agent_id}\nx-agent-session-token: {token}\n"
)
os.chmod(sys.argv[2], 0o600)
PY

CURL_ARGS=(-sS -o "$TMP_BODY" -w "%{http_code}" -X "$METHOD" "$URL" -H "@$HEADER_FILE")
if [ -n "$BODY_FILE" ]; then
  [ -f "$BODY_FILE" ] || fail "body file not found: $BODY_FILE"
  CURL_ARGS+=(-H 'content-type: application/json' --data-binary "@$BODY_FILE")
fi

HTTP_CODE="$(curl "${CURL_ARGS[@]}")"
cat "$TMP_BODY"
case "$HTTP_CODE" in
  2*) exit 0 ;;
  *) exit 1 ;;
esac
