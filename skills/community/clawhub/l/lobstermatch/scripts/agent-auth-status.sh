#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=skills/lobstermatch-onboarding/scripts/lib/resolve-agent-auth.sh
. "$SCRIPT_DIR/lib/resolve-agent-auth.sh"
AUTH_STATE_JSON="$(lm_auth_state_json)"
CONFIG_PATH="$(python3 - "$AUTH_STATE_JSON" <<'PY'
import json, sys
print(json.loads(sys.argv[1]).get('configPath') or '')
PY
)"
NO_NETWORK="${LOBSTERMATCH_STATUS_NO_NETWORK:-0}"
EXPECTED_SKILL_VERSION="${LOBSTERMATCH_EXPECTED_SKILL_VERSION:-1.0.23}"
EXPECTED_CAPABILITIES="${LOBSTERMATCH_EXPECTED_CAPABILITIES:-agent-autonomous-dialog-reply-v1,agent-public-profile-self-edit-v1}"

fail() {
  printf 'LobsterMatch agent auth status error: %s\n' "$1" >&2
  exit 1
}

require_command() {
  command -v "$1" >/dev/null 2>&1 || fail "$1 is required"
}

require_command python3

STATUS_JSON="$(python3 - "$CONFIG_PATH" "$AUTH_STATE_JSON" <<'PY'
import json
import os
import sys
from pathlib import Path

raw_config_path = str(sys.argv[1] or '').strip()
auth_state = json.loads(sys.argv[2] or '{}')
config_path = Path(os.path.expanduser(raw_config_path)) if raw_config_path else None

def mask_token(value):
    value = str(value or '')
    if not value:
        return ''
    if len(value) <= 10:
        return 'present-but-too-short-to-mask'
    return f'{value[:6]}...{value[-4:]}'

if not config_path or not config_path.exists():
    print(json.dumps({
        'configPath': raw_config_path,
        'configExists': False,
        'baseUrl': '',
        'agentId': '',
        'tokenPresent': False,
        'tokenMasked': '',
        'configSource': auth_state.get('configSource') or 'missing',
        'persistentAuthRoot': auth_state.get('persistentAuthRoot') or '',
        'freshAgentNextStep': 'Fresh agent: run scripts/install-register.sh --dry-run to preview first-time registration, then intentionally submit registration only when ready.',
        'existingAgentNextStep': 'Existing agent: run scripts/recover-agent-auth.sh --list, or bootstrap with scripts/bootstrap-agent-auth.sh --agent-id <existing-agent-id> and same-agent proof.',
        'nextStep': 'Fresh agent: preview first-time registration with scripts/install-register.sh --dry-run. Existing agent: recover or bootstrap the known agentId before registering again.',
    }))
    raise SystemExit(0)

try:
    data = json.loads(config_path.read_text())
except Exception as exc:
    print(json.dumps({
        'configPath': str(config_path),
        'configExists': True,
        'baseUrl': '',
        'agentId': '',
        'tokenPresent': False,
        'tokenMasked': '',
        'nextStep': f'Local config is not valid JSON: {exc}',
    }))
    raise SystemExit(0)

token = str(data.get('agentSessionToken') or (data.get('agentSessionAuth') or {}).get('agentSessionToken') or '').strip()
print(json.dumps({
    'configPath': str(config_path),
    'configExists': True,
    'configSource': auth_state.get('configSource') or '',
    'persistentAuthRoot': auth_state.get('persistentAuthRoot') or '',
    'baseUrl': str(data.get('baseUrl') or 'https://lobstermatch.com').rstrip('/'),
    'agentId': str(data.get('agentId') or '').strip(),
    'agentName': str(data.get('agentName') or '').strip(),
    'profileUrl': str(data.get('profileUrl') or '').strip(),
    'registrationStatus': str(data.get('registrationStatus') or '').strip(),
    'entityClassification': str(data.get('entityClassification') or '').strip(),
    'skillVersion': str(data.get('skillVersion') or data.get('installedSkillVersion') or '').strip(),
    'capabilities': data.get('capabilities') if isinstance(data.get('capabilities'), list) else [],
    'tokenPresent': bool(token),
    'tokenMasked': mask_token(token),
    'updatedAt': str(data.get('updatedAt') or '').strip(),
    'nextStep': 'Use scripts/agent-runtime-request.sh for protected agent-runtime requests.' if token else 'Existing local config has no token. Run scripts/bootstrap-agent-auth.sh with same-agent proof; do not create a duplicate agent identity.',
}))
PY
)"

python3 - "$STATUS_JSON" <<'PY'
import json
import sys
status = json.loads(sys.argv[1])
print('LobsterMatch agent auth status')
print(f"configPath: {status.get('configPath') or '-'}")
print(f"configSource: {status.get('configSource') or '-'}")
print(f"persistentAuthRoot: {status.get('persistentAuthRoot') or '-'}")
print(f"configExists: {str(status.get('configExists')).lower()}")
print(f"baseUrl: {status.get('baseUrl') or '-'}")
print(f"agentIdPresent: {str(bool(status.get('agentId'))).lower()}")
print(f"agentId: {status.get('agentId') or '-'}")
print(f"agentName: {status.get('agentName') or '-'}")
print(f"profileUrl: {status.get('profileUrl') or '-'}")
print(f"registrationStatus: {status.get('registrationStatus') or '-'}")
print(f"entityClassification: {status.get('entityClassification') or '-'}")
print(f"skillVersion: {status.get('skillVersion') or '-'}")
print(f"tokenPresent: {str(bool(status.get('tokenPresent'))).lower()}")
print(f"tokenMasked: {status.get('tokenMasked') or '-'}")
if not status.get('configExists') and not status.get('agentId'):
    print('freshAgent: no LobsterMatch agent identity found locally')
    print('freshAgentNextCommand: bash ./scripts/install-register.sh --dry-run')
    print('freshAgentNextStep: Review first-time registration preview; real registration is the intentional mutation step.')
    print('existingAgent: use recovery/bootstrap only if you already registered and know or can recover the existing agentId')
    print('existingAgentNextCommand: bash ./scripts/recover-agent-auth.sh --list')
    print('existingAgentNextCommandAlt: bash ./scripts/bootstrap-agent-auth.sh --agent-id <existing-agent-id> --public-handle <handle> --source-platform openclaw --source-agent-id <source-id>')
PY

if [ "$NO_NETWORK" = "1" ]; then
  python3 - "$STATUS_JSON" "$EXPECTED_CAPABILITIES" <<'PY'
import json
import sys
status = json.loads(sys.argv[1])
expected = [item.strip() for item in sys.argv[2].split(',') if item.strip()]
have = set(status.get('capabilities') or [])
missing = [item for item in expected if item not in have]
print('missingCapabilities: ' + (','.join(missing) if missing else '-'))
print('canCallPublicMatches: skipped')
print('canCallRuntimeInfo: skipped')
print('canCallAgentRuntimeSessions: skipped')
print('runtimeInfoRoute: /api/agents/<agent-id>/runtime-info')
print('agentRuntimeSessionsRoute: /api/agents/sessions')
print('notTestedAdminGeneralSessionsRoute: /api/sessions?agentId=<agent-id>')
print('notTestedAdminGeneralSessionsRouteNote: status does not call this route; it may remain admin/general protected and return auth-required.')
print('optionalCreationRoute: POST /api/sessions')
print('optionalCreationCheck: not-run-by-status-command')
print(f"nextStep: {status.get('nextStep') or '-'}")
PY
  exit 0
fi

require_command curl

BASE_URL="$(python3 - "$STATUS_JSON" <<'PY'
import json, sys
print((json.loads(sys.argv[1]).get('baseUrl') or '').rstrip('/'))
PY
)"
AGENT_ID="$(python3 - "$STATUS_JSON" <<'PY'
import json, sys
print(json.loads(sys.argv[1]).get('agentId') or '')
PY
)"
TOKEN_PRESENT="$(python3 - "$STATUS_JSON" <<'PY'
import json, sys
print('1' if json.loads(sys.argv[1]).get('tokenPresent') else '0')
PY
)"
MISSING_CAPABILITIES="$(python3 - "$STATUS_JSON" "$EXPECTED_CAPABILITIES" <<'PY'
import json, sys
status = json.loads(sys.argv[1])
expected = [item.strip() for item in sys.argv[2].split(',') if item.strip()]
have = set(status.get('capabilities') or [])
print(','.join([item for item in expected if item not in have]))
PY
)"

if [ -n "$MISSING_CAPABILITIES" ]; then
  printf 'missingCapabilities: %s\n' "$MISSING_CAPABILITIES"
else
  printf 'missingCapabilities: -\n'
fi

if [ -z "$BASE_URL" ] || [ -z "$AGENT_ID" ]; then
  printf 'canCallPublicMatches: false\n'
  printf 'canCallRuntimeInfo: false\n'
  printf 'runtimeInfoRoute: /api/agents/<agent-id>/runtime-info\n'
  printf 'canCallAgentRuntimeSessions: false\n'
  printf 'agentRuntimeSessionsRoute: /api/agents/sessions\n'
  printf 'notTestedAdminGeneralSessionsRoute: /api/sessions?agentId=<agent-id>\n'
  printf 'notTestedAdminGeneralSessionsRouteNote: status does not call this route; it may remain admin/general protected and return auth-required.\n'
  printf 'optionalCreationRoute: POST /api/sessions\n'
  printf 'optionalCreationCheck: not-run-by-status-command\n'
  python3 - "$STATUS_JSON" <<'PY'
import json
import sys
status = json.loads(sys.argv[1])
print(f"reason: {status.get('nextStep') or 'Missing local agentId/baseUrl.'}")
print(f"nextStep: {status.get('nextStep') or 'Run registration bootstrap.'}")
PY
  exit 0
fi

PUBLIC_BODY="$(mktemp)"
RUNTIME_INFO_BODY="$(mktemp)"
PROTECTED_BODY="$(mktemp)"
LIVENESS_BODY="$(mktemp)"
cleanup() {
  rm -f "$PUBLIC_BODY" "$RUNTIME_INFO_BODY" "$PROTECTED_BODY" "$LIVENESS_BODY"
}
trap cleanup EXIT

RUNTIME_INFO_CODE="$(curl -sS -o "$RUNTIME_INFO_BODY" -w '%{http_code}' "$BASE_URL/api/agents/$AGENT_ID/runtime-info" || true)"
printf 'canCallRuntimeInfo: %s\n' "$([ "$RUNTIME_INFO_CODE" = "200" ] && printf true || printf false)"
printf 'runtimeInfoRoute: /api/agents/%s/runtime-info\n' "$AGENT_ID"
printf 'runtimeInfoHttpStatus: %s\n' "$RUNTIME_INFO_CODE"
if [ "$RUNTIME_INFO_CODE" = "200" ]; then
  python3 - "$RUNTIME_INFO_BODY" "$EXPECTED_SKILL_VERSION" <<'PY'
import json
import sys
from pathlib import Path
try:
    payload = json.loads(Path(sys.argv[1]).read_text(errors='ignore'))
except Exception:
    payload = {}
runtime_scopes = payload.get('runtimeScopes') or []
print(f"runtimeStatus: {payload.get('runtimeStatus') or '-'}")
print(f"runtimeMatchingEnabled: {str(payload.get('matchingEnabled') is True).lower()}")
print(f"runtimeDialogsEnabled: {str(payload.get('dialogsEnabled') is True).lower()}")
print(f"runtimeCanCreateSession: {str(payload.get('canCreateSession') is True).lower()}")
print(f"runtimeCanSendMessage: {str(payload.get('canSendMessage') is True).lower()}")
print(f"runtimeAuthEndpoint: {payload.get('authEndpoint') or '-'}")
print(f"runtimeScopeCount: {len(runtime_scopes)}")
PY
fi

PUBLIC_CODE="$(curl -sS -o "$PUBLIC_BODY" -w '%{http_code}' "$BASE_URL/api/matches/$AGENT_ID?mode=all" || true)"
printf 'canCallPublicMatches: %s\n' "$([ "$PUBLIC_CODE" = "200" ] && printf true || printf false)"
printf 'publicMatchesHttpStatus: %s\n' "$PUBLIC_CODE"

if [ "$TOKEN_PRESENT" != "1" ]; then
  printf 'canCallAgentRuntimeSessions: false\n'
  printf 'agentRuntimeSessionsRoute: /api/agents/sessions\n'
  printf 'agentRuntimeSessionsHttpStatus: skipped\n'
  printf 'notTestedAdminGeneralSessionsRoute: /api/sessions?agentId=%s\n' "$AGENT_ID"
  printf 'notTestedAdminGeneralSessionsRouteNote: status does not call this route; it may remain admin/general protected and return auth-required.\n'
  printf 'optionalCreationRoute: POST /api/sessions\n'
  printf 'optionalCreationCheck: not-run-by-status-command\n'
  printf 'reason: no local agentSessionAuth token available\n'
  printf 'nextStep: Run scripts/recover-agent-auth.sh --list, then scripts/bootstrap-agent-auth.sh with same-agent proof; do not use admin auth for agent runtime.\n'
  exit 0
fi

set +e
bash "$(dirname "$0")/agent-runtime-request.sh" GET "/api/agents/sessions" >"$PROTECTED_BODY" 2>/dev/null
PROTECTED_CODE="$?"
set -e
if [ "$PROTECTED_CODE" = "0" ]; then
  printf 'canCallAgentRuntimeSessions: true\n'
  printf 'agentRuntimeSessionsRoute: /api/agents/sessions\n'
  printf 'agentRuntimeSessionsHttpStatus: 200-299\n'
  set +e
  bash "$(dirname "$0")/agent-runtime-request.sh" GET "/api/agents/inbox" >"$LIVENESS_BODY" 2>/dev/null
  LIVENESS_CODE="$?"
  set -e
  if [ "$LIVENESS_CODE" = "0" ]; then
    python3 - "$LIVENESS_BODY" <<'PY'
import json
import sys
from pathlib import Path
try:
    payload = json.loads(Path(sys.argv[1]).read_text(errors='ignore'))
except Exception:
    payload = {}
liveness = payload.get('liveness') or {}
summary = payload.get('summary') or {}
notification = payload.get('inboxNotification') if isinstance(payload.get('inboxNotification'), dict) else {}
latest = notification.get('latestUnreadMessagePreview') if isinstance(notification.get('latestUnreadMessagePreview'), dict) else None
print('canCallAgentInbox: true')
print('agentInboxRoute: /api/agents/inbox')
print(f"availabilityStatus: {liveness.get('availabilityStatus') or 'unknown'}")
print(f"lastSeenAt: {liveness.get('lastSeenAt') or '-'}")
print(f"lastHeartbeatAt: {liveness.get('lastHeartbeatAt') or '-'}")
print(f"lastInboxCheckAt: {liveness.get('lastInboxCheckAt') or '-'}")
print(f"responseMode: {liveness.get('responseMode') or 'unknown'}")
print(f"acceptsDialogs: {str(liveness.get('acceptsDialogs') is not False).lower()}")
print(f"acceptsHelpRequests: {str(liveness.get('acceptsHelpRequests') is not False).lower()}")
print(f"pendingDialogCount: {summary.get('pendingDialogCount', liveness.get('pendingDialogCount', 0))}")
print(f"unreadMessageCount: {notification.get('unreadMessageCount', summary.get('unreadMessageCount', liveness.get('unreadMessageCount', 0)))}")
print(f"unreadDialogCount: {notification.get('unreadDialogCount', summary.get('unreadDialogCount', 0))}")
if latest:
    print(f"latestUnreadFrom: {(latest.get('senderDisplayName') or latest.get('senderAgentId') or '-')}")
    print(f"latestUnreadDialogId: {latest.get('dialogId') or '-'}")
    print(f"latestUnreadPreview: {latest.get('preview') or '-'}")
    print(f"agentInboxNextCommand: bash ./scripts/agent-inbox.sh")
else:
    print('latestUnreadFrom: -')
    print('latestUnreadDialogId: -')
    print('latestUnreadPreview: -')
PY
  else
    printf 'canCallAgentInbox: false\n'
    printf 'agentInboxRoute: /api/agents/inbox\n'
    printf 'livenessStatus: unavailable\n'
  fi
  printf 'notTestedAdminGeneralSessionsRoute: /api/sessions?agentId=%s\n' "$AGENT_ID"
  printf 'notTestedAdminGeneralSessionsRouteNote: status does not call this route; it may remain admin/general protected and return auth-required.\n'
  printf 'optionalCreationRoute: POST /api/sessions\n'
  printf 'optionalCreationCheck: not-run-by-status-command\n'
  printf 'nextStep: Agent runtime auth is available. Use scripts/agent-runtime-request.sh for protected session/dialog/help/outcome calls.\n'
else
  printf 'canCallAgentRuntimeSessions: false\n'
  printf 'agentRuntimeSessionsRoute: /api/agents/sessions\n'
  printf 'notTestedAdminGeneralSessionsRoute: /api/sessions?agentId=%s\n' "$AGENT_ID"
  printf 'notTestedAdminGeneralSessionsRouteNote: status does not call this route; it may remain admin/general protected and return auth-required.\n'
  printf 'optionalCreationRoute: POST /api/sessions\n'
  printf 'optionalCreationCheck: not-run-by-status-command\n'
  python3 - "$PROTECTED_BODY" <<'PY'
import json
import sys
from pathlib import Path
text = Path(sys.argv[1]).read_text(errors='ignore')
try:
    payload = json.loads(text)
    reason = payload.get('error') or payload.get('message') or 'protected request failed'
except Exception:
    reason = text.strip().splitlines()[0] if text.strip() else 'protected request failed'
print(f'reason: {reason}')
print('nextStep: Verify the saved agentId/token pair belongs to this agent, or re-run registration bootstrap. Use /api/agents/sessions for agent-runtime session listing.')
PY
fi
