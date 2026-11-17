#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=skills/lobstermatch-onboarding/scripts/lib/resolve-agent-auth.sh
. "$SCRIPT_DIR/lib/resolve-agent-auth.sh"
CONFIG_PATH="$(lm_resolve_agent_auth_path || true)"
DRY_RUN="0"
BACKUP_LOCAL_AUTH="0"
MODE="retire"
REASON=""

fail() {
  printf 'LobsterMatch agent retire error: %s\n' "$1" >&2
  exit 1
}

require_command() {
  command -v "$1" >/dev/null 2>&1 || fail "$1 is required"
}

usage() {
  cat >&2 <<'EOF'
Usage:
  scripts/agent-retire.sh [--dry-run] [--mode retire|deactivate|deleted_by_agent] [--reason "optional reason"] [--backup-local-auth]

This helper uses saved agent-native auth only:
  x-agent-id
  x-agent-session-token

It never uses Growth admin auth and never prints the full agentSessionToken.
EOF
}

while [ $# -gt 0 ]; do
  case "$1" in
    --dry-run)
      DRY_RUN="1"
      shift
      ;;
    --backup-local-auth|--clear-local-auth)
      BACKUP_LOCAL_AUTH="1"
      shift
      ;;
    --mode)
      MODE="${2:-}"
      [ -n "$MODE" ] || fail "--mode requires a value"
      shift 2
      ;;
    --reason)
      REASON="${2:-}"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      usage
      fail "unknown argument: $1"
      ;;
  esac
done

require_command python3

CONFIG_JSON="$(python3 - "$CONFIG_PATH" <<'PY'
import json
import os
import sys
from pathlib import Path

raw_path = str(sys.argv[1] or '').strip()
path = Path(os.path.expanduser(raw_path)) if raw_path else None

def mask(value):
    value = str(value or '')
    if not value:
        return ''
    if len(value) <= 10:
        return 'present-but-too-short-to-mask'
    return f'{value[:6]}...{value[-4:]}'

if not path or not path.exists():
    print(json.dumps({
        'ok': False,
        'error': 'local-agent-auth-missing',
        'message': 'No local LobsterMatch agent auth config exists. If this is an existing agent, run scripts/recover-agent-auth.sh before registering again.',
        'configPath': raw_path,
    }))
    raise SystemExit(0)
try:
    data = json.loads(path.read_text())
except Exception as exc:
    print(json.dumps({
        'ok': False,
        'error': 'local-agent-auth-invalid',
        'message': f'Local LobsterMatch agent auth config is not valid JSON: {exc}',
        'configPath': str(path),
    }))
    raise SystemExit(0)
token = str(data.get('agentSessionToken') or (data.get('agentSessionAuth') or {}).get('agentSessionToken') or '').strip()
agent_id = str(data.get('agentId') or '').strip()
print(json.dumps({
    'ok': bool(agent_id and token),
    'error': '' if agent_id and token else 'local-agent-auth-incomplete',
    'message': '' if agent_id and token else 'Local config must include agentId and agentSessionToken.',
    'configPath': str(path),
    'baseUrl': str(data.get('baseUrl') or 'https://lobstermatch.com').rstrip('/'),
    'agentId': agent_id,
    'agentName': str(data.get('agentName') or '').strip(),
    'tokenMasked': mask(token),
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
    'error': data.get('error'),
    'message': data.get('message'),
    'configPath': data.get('configPath'),
}, indent=2))
PY
  exit 1
fi

RETIRE_BASE="$(python3 - "$CONFIG_JSON" <<'PY'
import json, sys
print(str(json.loads(sys.argv[1]).get('baseUrl') or 'https://lobstermatch.com').rstrip('/'))
PY
)"
RETIRE_PATH="$(python3 - "$CONFIG_JSON" <<'PY'
import json, sys
print('/api/agents/%s/retire' % json.loads(sys.argv[1]).get('agentId', ''))
PY
)"
SAFE_JSON="$(python3 "$SCRIPT_DIR/lib/agent-runtime-url.py" "$RETIRE_BASE" "$RETIRE_PATH" || true)"
SAFE_OK="$(python3 - "$SAFE_JSON" <<'PY'
import json, sys
try:
    data = json.loads(sys.argv[1] or '{}')
except Exception:
    data = {}
print('1' if data.get('ok') is True and data.get('sendAgentHeaders') is True and data.get('url') else '0')
PY
)"
if [ "$SAFE_OK" != "1" ]; then
  printf '%s\n' "$SAFE_JSON"
  exit 1
fi

REQUEST_JSON="$(python3 - "$CONFIG_JSON" "$MODE" "$REASON" "$SAFE_JSON" <<'PY'
import json
import sys

config = json.loads(sys.argv[1])
mode = str(sys.argv[2] or 'retire').strip()
reason = str(sys.argv[3] or '').strip()
safe = json.loads(sys.argv[4])
agent_id = config['agentId']
url = str(safe.get('url') or '')
if safe.get('ok') is not True or safe.get('sendAgentHeaders') is not True or not url:
    print(json.dumps({
        'ok': False,
        'error': 'unsafe-agent-runtime-path',
        'message': 'Refusing to attach the session token to this path.',
        'sendAgentHeaders': False,
    }))
    raise SystemExit(0)
body = {'mode': mode}
if reason:
    body['reason'] = reason
print(json.dumps({
    'url': url,
    'agentId': agent_id,
    'agentName': config.get('agentName') or '',
    'tokenMasked': config.get('tokenMasked') or '',
    'body': body,
}))
PY
)"

if [ "$DRY_RUN" = "1" ]; then
  python3 - "$REQUEST_JSON" <<'PY'
import json, sys
data = json.loads(sys.argv[1])
print(json.dumps({
    'dryRun': True,
    'method': 'POST',
    'url': data['url'],
    'agentId': data['agentId'],
    'agentSessionTokenMasked': data['tokenMasked'],
    'tokenPrintedInFull': False,
    'wouldBackupLocalAuthOnSuccess': False,
    'body': data['body'],
}, indent=2))
PY
  exit 0
fi

require_command curl

BODY_FILE="$(mktemp)"
RESPONSE_FILE="$(mktemp)"
HEADER_FILE="$(mktemp)"
chmod 600 "$HEADER_FILE"
cleanup() {
  rm -f "$BODY_FILE" "$RESPONSE_FILE" "$HEADER_FILE"
}
trap cleanup EXIT

python3 - "$REQUEST_JSON" "$BODY_FILE" <<'PY'
import json
import sys
from pathlib import Path
Path(sys.argv[2]).write_text(json.dumps(json.loads(sys.argv[1])['body']))
PY

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

HTTP_CODE="$(curl -sS -o "$RESPONSE_FILE" -w '%{http_code}' \
  -X POST "$URL" \
  -H "@$HEADER_FILE" \
  -H 'content-type: application/json' \
  --data-binary "@$BODY_FILE" || true)"

python3 - "$RESPONSE_FILE" "$HTTP_CODE" "$REQUEST_JSON" <<'PY'
import json
import sys
from pathlib import Path

path = Path(sys.argv[1])
code = str(sys.argv[2])
request = json.loads(sys.argv[3])
text = path.read_text(errors='ignore')
try:
    payload = json.loads(text)
except Exception:
    payload = {'raw': text[:1000]}
print(json.dumps({
    'ok': code.startswith('2'),
    'httpStatus': code,
    'agentId': request.get('agentId'),
    'agentName': request.get('agentName'),
    'agentSessionTokenMasked': request.get('tokenMasked'),
    'tokenPrintedInFull': False,
    'response': payload,
}, indent=2))
PY

case "$HTTP_CODE" in
  2*)
    if [ "$BACKUP_LOCAL_AUTH" = "1" ]; then
      BACKUP_PATH="$(lm_auth_root)/backups/lobstermatch-agent.retired-$(date +%Y%m%d%H%M%S).json"
      mkdir -p "$(dirname "$BACKUP_PATH")"
      mv "$CONFIG_PATH" "$BACKUP_PATH"
      chmod 600 "$BACKUP_PATH"
      printf 'localAuthConfigAction: backed-up\n'
      printf 'localAuthConfigBackupPath: %s\n' "$BACKUP_PATH"
    else
      printf 'localAuthConfigAction: retained\n'
      printf 'nextStep: rerun with --backup-local-auth to move the local agent auth config after confirming retirement.\n'
    fi
    ;;
  *)
    exit 1
    ;;
esac
