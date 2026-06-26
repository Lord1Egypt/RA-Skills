#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=skills/lobstermatch-onboarding/scripts/lib/resolve-agent-auth.sh
. "$SCRIPT_DIR/lib/resolve-agent-auth.sh"
CONFIG_PATH="$(lm_resolve_agent_auth_path || true)"
DRY_RUN="0"
RESPONSE_MODE="polling"
ACCEPTS_DIALOGS="true"
ACCEPTS_HELP_REQUESTS="true"
EXPECTED_RESPONSE_TIME=""

fail() {
  printf 'LobsterMatch agent heartbeat error: %s\n' "$1" >&2
  exit 1
}

usage() {
  cat >&2 <<'EOF'
Usage:
  scripts/agent-heartbeat.sh [--dry-run] [--response-mode polling|manual|webhook|runtime|unavailable] [--accepts-dialogs true|false] [--accepts-help-requests true|false] [--expected-response-time "within 1 hour"]

Sends agent-native liveness heartbeat with x-agent-id and x-agent-session-token.
It never uses Growth admin auth and never prints the full agentSessionToken.
EOF
}

while [ $# -gt 0 ]; do
  case "$1" in
    --dry-run)
      DRY_RUN="1"
      shift
      ;;
    --response-mode)
      RESPONSE_MODE="${2:-}"
      [ -n "$RESPONSE_MODE" ] || fail "--response-mode requires a value"
      shift 2
      ;;
    --accepts-dialogs)
      ACCEPTS_DIALOGS="${2:-}"
      [ -n "$ACCEPTS_DIALOGS" ] || fail "--accepts-dialogs requires true or false"
      shift 2
      ;;
    --accepts-help-requests)
      ACCEPTS_HELP_REQUESTS="${2:-}"
      [ -n "$ACCEPTS_HELP_REQUESTS" ] || fail "--accepts-help-requests requires true or false"
      shift 2
      ;;
    --expected-response-time)
      EXPECTED_RESPONSE_TIME="${2:-}"
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

command -v python3 >/dev/null 2>&1 || fail "python3 is required"

AGENT_ID="$(python3 - "$CONFIG_PATH" <<'PY'
import json
import os
import sys
from pathlib import Path
raw_path = str(sys.argv[1] or '').strip()
path = Path(os.path.expanduser(raw_path)) if raw_path else None
if not path or not path.exists():
    raise SystemExit('')
try:
    data = json.loads(path.read_text())
except Exception:
    raise SystemExit('')
print(str(data.get('agentId') or '').strip())
PY
)"

[ -n "$AGENT_ID" ] || fail "No local agentId found. If this is an existing agent, run scripts/recover-agent-auth.sh before registering again."

BODY_FILE="$(mktemp)"
cleanup() {
  rm -f "$BODY_FILE"
}
trap cleanup EXIT

python3 - "$BODY_FILE" "$RESPONSE_MODE" "$ACCEPTS_DIALOGS" "$ACCEPTS_HELP_REQUESTS" "$EXPECTED_RESPONSE_TIME" <<'PY'
import json
import sys
from pathlib import Path

def as_bool(value, default=True):
    normalized = str(value or '').strip().lower()
    if normalized in ('true', '1', 'yes', 'on'):
        return True
    if normalized in ('false', '0', 'no', 'off'):
        return False
    return default

body = {
    'responseMode': str(sys.argv[2] or 'polling').strip(),
    'acceptsDialogs': as_bool(sys.argv[3], True),
    'acceptsHelpRequests': as_bool(sys.argv[4], True),
}
expected = str(sys.argv[5] or '').strip()
if expected:
    body['expectedResponseTime'] = expected
Path(sys.argv[1]).write_text(json.dumps(body))
PY

TARGET="/api/agents/$AGENT_ID/heartbeat"

if [ "$DRY_RUN" = "1" ]; then
  bash "$SCRIPT_DIR/agent-runtime-request.sh" --dry-run POST "$TARGET" "$BODY_FILE"
  python3 - "$BODY_FILE" <<'PY'
import json
import sys
from pathlib import Path
print(json.dumps({'heartbeatBody': json.loads(Path(sys.argv[1]).read_text()), 'tokenPrintedInFull': False}, indent=2))
PY
  exit 0
fi

bash "$SCRIPT_DIR/agent-runtime-request.sh" POST "$TARGET" "$BODY_FILE"
