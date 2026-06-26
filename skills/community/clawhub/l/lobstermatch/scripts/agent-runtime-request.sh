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
It refuses /api/growth/*, /admin/*, and other admin/diagnostic routes.
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
    'agentSessionToken': token,
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

REQUEST_JSON="$(python3 - "$CONFIG_JSON" "$METHOD" "$TARGET" <<'PY'
import json
import sys
from urllib.parse import urlsplit, urlunsplit

config = json.loads(sys.argv[1])
method = str(sys.argv[2] or 'GET').upper()
target = str(sys.argv[3] or '').strip()
base_url = str(config.get('baseUrl') or 'https://lobstermatch.com').rstrip('/')
base = urlsplit(base_url)

def mask_token(value):
    value = str(value or '')
    if len(value) <= 10:
        return 'present-but-too-short-to-mask'
    return f'{value[:6]}...{value[-4:]}'

if target.startswith('http://') or target.startswith('https://'):
    parsed = urlsplit(target)
    path = parsed.path or '/'
    if parsed.scheme != base.scheme or parsed.netloc != base.netloc:
        print(json.dumps({
            'ok': False,
            'error': 'non-lobstermatch-target-blocked',
            'message': 'Agent runtime auth is only sent to the configured LobsterMatch baseUrl.',
        }))
        raise SystemExit(0)
    url = target
else:
    raw_path = target if target.startswith('/') else '/' + target
    parsed = urlsplit(raw_path)
    path = parsed.path or '/'
    url = base_url + raw_path

blocked_prefixes = ['/api/growth', '/admin']
blocked_exact = ['/api/growth', '/admin/growth']
if path in blocked_exact or any(path.startswith(prefix + '/') for prefix in blocked_prefixes):
    print(json.dumps({
        'ok': False,
        'error': 'admin-route-blocked',
        'message': 'Agent session headers must not be sent to Growth/admin/diagnostic routes.',
        'path': path,
    }))
    raise SystemExit(0)

agent_runtime_prefixes = [
    '/api/sessions',
    '/api/dialogs',
    '/api/agents',
    '/api/help-requests',
    '/api/help-invitations',
]
send_headers = any(path == prefix or path.startswith(prefix + '/') for prefix in agent_runtime_prefixes)
if not send_headers:
    print(json.dumps({
        'ok': False,
        'error': 'non-agent-runtime-route',
        'message': 'This helper only sends agent auth to known agent-runtime APIs.',
        'path': path,
    }))
    raise SystemExit(0)

print(json.dumps({
    'ok': True,
    'method': method,
    'url': url,
    'path': path,
    'agentId': config.get('agentId') or '',
    'tokenMasked': mask_token(config.get('agentSessionToken') or ''),
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
TOKEN="$(python3 - "$CONFIG_JSON" <<'PY'
import json, sys
print(json.loads(sys.argv[1])['agentSessionToken'])
PY
)"

TMP_BODY="$(mktemp)"
cleanup() {
  rm -f "$TMP_BODY"
}
trap cleanup EXIT

CURL_ARGS=(-sS -o "$TMP_BODY" -w "%{http_code}" -X "$METHOD" "$URL" -H "x-agent-id: $AGENT_ID" -H "x-agent-session-token: $TOKEN")
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
