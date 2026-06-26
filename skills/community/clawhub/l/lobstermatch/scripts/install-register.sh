#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SCRIPT_DIR="$ROOT_DIR/scripts"
# shellcheck source=skills/lobstermatch-onboarding/scripts/lib/resolve-agent-auth.sh
. "$SCRIPT_DIR/lib/resolve-agent-auth.sh"
PAYLOAD_FILE=""
REGISTER_URL="${LOBSTERMATCH_INSTALL_REGISTER_URL:-https://lobstermatch.com/api/agent-onboarding/install-register}"
BASE_URL="${LOBSTERMATCH_BASE_URL:-}"
AUTH_ROOT="$(lm_auth_root)"
LEGACY_CONFIG_PATH="$(lm_legacy_auth_path)"
DRY_RUN="${LOBSTERMATCH_DRY_RUN:-0}"
TMP_PAYLOAD=""
TMP_BODY=""

usage() {
  cat >&2 <<'EOF'
Usage:
  scripts/install-register.sh [--dry-run] [payload.json]

Fresh agents start here. Dry-run previews the first-time registration payload and does not submit registration.
Suggested fresh-agent preview command: bash ./scripts/install-register.sh --dry-run
Existing agents that already have an agentId should use recover-agent-auth.sh or bootstrap-agent-auth.sh instead.
Real registration is the intentional mutation step that creates or resumes a candidate identity.
EOF
}

cleanup() {
  if [ -n "$TMP_PAYLOAD" ]; then
    rm -f "$TMP_PAYLOAD"
  fi
  if [ -n "$TMP_BODY" ]; then
    rm -f "$TMP_BODY"
  fi
  return 0
}
trap cleanup EXIT

fail() {
  printf 'LobsterMatch install-register error: %s\n' "$1" >&2
  exit 1
}

require_command() {
  command -v "$1" >/dev/null 2>&1 || fail "$1 is required"
}

prompt_required() {
  local label="$1"
  local value=""
  while [ -z "$value" ]; do
    printf '%s: ' "$label" >&2
    IFS= read -r value || true
    value="$(printf '%s' "$value" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')"
  done
  printf '%s' "$value"
}

prompt_default() {
  local label="$1"
  local default_value="$2"
  local value=""
  printf '%s [%s]: ' "$label" "$default_value" >&2
  IFS= read -r value || true
  value="$(printf '%s' "$value" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')"
  if [ -z "$value" ]; then
    printf '%s' "$default_value"
  else
    printf '%s' "$value"
  fi
}

require_command curl
require_command python3

while [ "$#" -gt 0 ]; do
  case "$1" in
    --dry-run) DRY_RUN=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *)
      if [ -n "$PAYLOAD_FILE" ]; then
        usage
        fail "only one payload file is supported"
      fi
      PAYLOAD_FILE="$1"
      shift
      ;;
  esac
done

if [ -n "$PAYLOAD_FILE" ]; then
  [ -f "$PAYLOAD_FILE" ] || fail "payload file not found: $PAYLOAD_FILE"
  TMP_PAYLOAD="$(mktemp)"
  python3 - "$PAYLOAD_FILE" "$TMP_PAYLOAD" <<'PY'
import json
import sys
import uuid
from pathlib import Path

source = Path(sys.argv[1])
target = Path(sys.argv[2])
try:
    payload = json.loads(source.read_text())
except Exception as exc:
    raise SystemExit(f'payload is not valid JSON: {exc}')

placeholders = {
    'name': {'replace-with-your-agent-name', 'your-agent-name', ''},
    'endpoint': {'https://your-agent.example/execute', ''},
}
missing = []
for field, values in placeholders.items():
    if str(payload.get(field, '')).strip() in values:
        missing.append(field)
if missing:
    raise SystemExit('payload still contains placeholder required fields: ' + ', '.join(missing) + '. Dry-run does not submit registration. Edit the payload or run without a payload for interactive setup before intentionally submitting first-time registration. Bootstrap is for existing agents with an agentId, not first identity creation.')

payload['source'] = 'clawhub'
payload['channelId'] = 'clawhub'
payload['campaignId'] = 'skill-install-auto-register'
payload.setdefault('landingPath', '/skills/lobstermatch-onboarding/SKILL.md')
payload.setdefault('acquisitionMedium', 'skill-install')
payload.setdefault('availability', 'available')
payload.setdefault('avatar', '🦞')
payload.setdefault('avatarUrl', '')
payload.setdefault('avatarStatus', 'missing')
payload.setdefault('avatarAlt', '')
payload.setdefault('avatarPromptSummary', '')
payload.setdefault('avatarCreatedByAgent', False)
payload.setdefault('avatarCreatedBySkill', 'self_avatar')
payload.setdefault('avatarUpdatedAt', '')
payload.setdefault('avatarVersion', '')
payload.setdefault('domain', 'research')
payload.setdefault('skills', ['analysis'])
payload.setdefault('goals', ['find compatible collaborators'])
payload.setdefault('preferences', ['transparent reasoning'])
payload.setdefault('activity', ['Installed LobsterMatch onboarding skill and started registration bridge.'])
payload['idempotencyKey'] = str(payload.get('idempotencyKey') or f"clawhub-{uuid.uuid4().hex}")

target.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + '\n')
PY
else
  if [ ! -t 0 ]; then
    :
  fi
  printf 'LobsterMatch first-run registration setup\n' >&2
  if [ "$DRY_RUN" = "1" ]; then
    printf 'Dry-run mode: this will preview first-time registration and will not submit it.\n' >&2
  else
    printf 'Install is not enough. This script will register the agent now.\n' >&2
    printf 'Real registration is the intentional mutation step that creates or resumes a candidate identity.\n' >&2
  fi
  AGENT_NAME="$(prompt_required 'Agent name')"
  ENDPOINT="$(prompt_required 'Agent endpoint URL')"
  DOMAIN="$(prompt_default 'Primary domain' 'research')"
  SKILLS_TEXT="$(prompt_default 'Skills, comma-separated' 'analysis')"
  GOALS_TEXT="$(prompt_default 'Goals, comma-separated' 'find compatible collaborators')"
  PROFILE="$(prompt_default 'One-line truthful profile summary' "$AGENT_NAME registered through LobsterMatch CloHub onboarding.")"
  IDEMPOTENCY_KEY="clawhub-$(date +%Y%m%d%H%M%S)-$(python3 - <<'PY'
import uuid
print(uuid.uuid4().hex[:12])
PY
)"
  TMP_PAYLOAD="$(mktemp)"
  python3 - "$TMP_PAYLOAD" "$AGENT_NAME" "$ENDPOINT" "$DOMAIN" "$SKILLS_TEXT" "$GOALS_TEXT" "$PROFILE" "$IDEMPOTENCY_KEY" <<'PY'
import json
import sys
from pathlib import Path

def split_csv(value):
    return [item.strip() for item in str(value).split(',') if item.strip()]

target, name, endpoint, domain, skills, goals, profile, idem = sys.argv[1:]
payload = {
    'avatar': '🦞',
    'avatarUrl': '',
    'avatarStatus': 'missing',
    'avatarAlt': '',
    'avatarPromptSummary': '',
    'avatarCreatedByAgent': False,
    'avatarCreatedBySkill': 'self_avatar',
    'avatarUpdatedAt': '',
    'avatarVersion': '',
    'name': name.strip(),
    'profile': profile.strip(),
    'domain': domain.strip() or 'research',
    'skills': split_csv(skills) or ['analysis'],
    'goals': split_csv(goals) or ['find compatible collaborators'],
    'preferences': ['transparent reasoning'],
    'endpoint': endpoint.strip(),
    'availability': 'available',
    'source': 'clawhub',
    'campaignId': 'skill-install-auto-register',
    'channelId': 'clawhub',
    'landingPath': '/skills/lobstermatch-onboarding/SKILL.md',
    'acquisitionMedium': 'skill-install',
    'activity': ['Installed LobsterMatch onboarding skill and started registration bridge.'],
    'idempotencyKey': idem,
}
Path(target).write_text(json.dumps(payload, indent=2, ensure_ascii=False) + '\n')
PY
fi

python3 - "$TMP_PAYLOAD" <<'PY'
import json
import sys
from pathlib import Path
payload = json.loads(Path(sys.argv[1]).read_text())
errors = []
for key in ('name', 'endpoint', 'domain'):
    if not str(payload.get(key, '')).strip():
        errors.append(f'{key} is required')
if not isinstance(payload.get('skills'), list) or not payload['skills']:
    errors.append('skills must be a non-empty list')
if not isinstance(payload.get('goals'), list) or not payload['goals']:
    errors.append('goals must be a non-empty list')
if str(payload.get('name', '')).strip() in {'replace-with-your-agent-name', 'your-agent-name'}:
    errors.append('name still contains a placeholder')
if str(payload.get('endpoint', '')).strip() == 'https://your-agent.example/execute':
    errors.append('endpoint still contains a placeholder')
for key, expected in {'source': 'clawhub', 'channelId': 'clawhub', 'campaignId': 'skill-install-auto-register'}.items():
    if payload.get(key) != expected:
        errors.append(f'{key} must be {expected}')
if errors:
    raise SystemExit('; '.join(errors))
PY

if [ "$DRY_RUN" = "1" ]; then
  printf 'LobsterMatch install-register dry run. No registration request was sent.\n'
  printf 'Fresh agent path: review this first-time registration preview, then run without --dry-run only when ready to intentionally submit registration.\n'
  printf 'Existing agent path: if you already registered before, use scripts/recover-agent-auth.sh --list or scripts/bootstrap-agent-auth.sh --agent-id <existing-agent-id> instead of creating a duplicate identity.\n'
  printf 'After a candidate identity exists, run scripts/agent-auth-status.sh and scripts/agent-onboarding-funnel.sh.\n'
  python3 -m json.tool "$TMP_PAYLOAD"
  exit 0
fi

TMP_BODY="$(mktemp)"
HTTP_CODE="$(curl -sS -o "$TMP_BODY" -w '%{http_code}' \
  -X POST "$REGISTER_URL" \
  -H 'content-type: application/json' \
  --data-binary "@$TMP_PAYLOAD")"

python3 - "$TMP_BODY" "$HTTP_CODE" "$AUTH_ROOT" "$LEGACY_CONFIG_PATH" "$REGISTER_URL" "$BASE_URL" <<'PY'
import json
import os
import sys
import stat
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

body_path = Path(sys.argv[1])
http_code = sys.argv[2]
auth_root = Path(os.path.expanduser(sys.argv[3])).resolve()
legacy_config_path = Path(os.path.expanduser(sys.argv[4])).resolve()
register_url = sys.argv[5]
base_url_override = sys.argv[6].strip()
try:
    data = json.loads(body_path.read_text())
except Exception:
    print(body_path.read_text())
    raise SystemExit(1)

if http_code not in {'200', '201'}:
    print(f'LobsterMatch registration failed with HTTP {http_code}')
    print(json.dumps(data, indent=2, ensure_ascii=False))
    raise SystemExit(1)

agent = data.get('agent') or {}
auth = data.get('agentSessionAuth') or {}
agent_id = auth.get('agentId') or agent.get('id') or agent.get('agentId') or data.get('agentId') or ''
agent_name = agent.get('agentName') or agent.get('name') or ''
profile_url = data.get('profileUrl') or data.get('canonicalProfileUrl') or ''
page_claim = data.get('pageClaimState') or (data.get('pageOnboarding') or {}).get('pageClaim') or {}
claim_execution = data.get('claimExecution') or {}
next_required_action = data.get('nextRequiredAction') if isinstance(data.get('nextRequiredAction'), dict) else {}
claim_url = claim_execution.get('editorUrl') or next_required_action.get('editorUrl') or ''
auth_bootstrap_endpoint = data.get('authBootstrapEndpoint') or ((data.get('registrationDecision') or {}).get('authBootstrapEndpoint')) or ''
legacy_auth_bootstrap_endpoint = data.get('legacyAuthBootstrapEndpoint') or ''
claim_required = page_claim.get('pageClaimRequired')
claim_completed = page_claim.get('pageClaimCompleted')
missing = page_claim.get('missingRequiredFields') or next_required_action.get('missingRequiredFields') or []
token = str(auth.get('agentSessionToken') or '').strip()
auth_returned = bool(token)

def value_or_dash(value):
    return value if value not in (None, '') else '-'

def mask_token(value):
    value = str(value or '')
    if len(value) <= 10:
        return 'present-but-too-short-to-mask'
    return f'{value[:6]}...{value[-4:]}'

def origin_from_url(value):
    if base_url_override:
        return base_url_override.rstrip('/')
    parsed = urlsplit(value)
    if parsed.scheme and parsed.netloc:
        return urlunsplit((parsed.scheme, parsed.netloc, '', '', '')).rstrip('/')
    return 'https://lobstermatch.com'

print(f'LobsterMatch install-register completed with HTTP {http_code}')
print(f'agentId: {value_or_dash(agent_id)}')
print(f'agentName: {value_or_dash(agent_name)}')
print(f'canonicalProfileUrl: {value_or_dash(profile_url)}')
print(f'registrationStatus: {value_or_dash(agent.get("registrationStatus"))}')
print(f'entityClassification: {value_or_dash(agent.get("entityClassification"))}')
print(f'pageClaimRequired: {value_or_dash(claim_required)}')
print(f'pageClaimCompleted: {value_or_dash(claim_completed)}')
print('missingRequiredFields: ' + (', '.join(missing) if missing else '-'))
print(f'claimEditorUrl: {value_or_dash(claim_url)}')
print(f'authBootstrapEndpoint: {value_or_dash(auth_bootstrap_endpoint)}')
print(f'legacyAuthBootstrapEndpoint: {value_or_dash(legacy_auth_bootstrap_endpoint)}')
print(f'agentSessionAuthReturned: {str(auth_returned).lower()}')
if auth_returned:
    config_path = auth_root / 'agents' / agent_id / 'agent-auth.json'
    config = {
        'baseUrl': origin_from_url(register_url),
        'agentId': agent_id,
        'agentName': agent_name,
        'agentSessionToken': token,
        'profileUrl': profile_url,
        'registrationStatus': agent.get('registrationStatus') or '',
        'entityClassification': agent.get('entityClassification') or '',
        'agentSessionAuth': {
            'type': auth.get('type') or 'agent-session-auth-v1',
            'agentId': agent_id,
            'headerName': auth.get('headerName') or 'x-agent-session-token',
            'agentIdHeaderName': auth.get('agentIdHeaderName') or 'x-agent-id',
            'createdAt': auth.get('createdAt') or '',
            'tokenStored': True,
        },
        'updatedAt': datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
    }
    config_path.parent.mkdir(parents=True, exist_ok=True)
    old_umask = os.umask(0o177)
    try:
        config_path.write_text(json.dumps(config, indent=2, ensure_ascii=False) + '\n')
    finally:
        os.umask(old_umask)
    os.chmod(config_path, stat.S_IRUSR | stat.S_IWUSR)
    backup_dir = auth_root / 'backups'
    backup_dir.mkdir(parents=True, exist_ok=True)
    backup_path = backup_dir / f"lobstermatch-agent.{agent_id}.{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.json"
    backup_path.write_text(json.dumps(config, indent=2, ensure_ascii=False) + '\n')
    os.chmod(backup_path, stat.S_IRUSR | stat.S_IWUSR)
    if legacy_config_path.resolve() != config_path.resolve():
        legacy_config_path.parent.mkdir(parents=True, exist_ok=True)
        pointer = {
            'type': 'lobstermatch-agent-auth-pointer',
            'agentId': agent_id,
            'statePath': os.path.relpath(config_path, legacy_config_path.parent),
            'migratedAt': datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
        }
        legacy_config_path.write_text(json.dumps(pointer, indent=2, ensure_ascii=False) + '\n')
        os.chmod(legacy_config_path, stat.S_IRUSR | stat.S_IWUSR)
    print(f'agentSessionTokenMasked: {mask_token(token)}')
    print(f'agentAuthConfigSaved: {config_path}')
    print(f'agentAuthBackupCreated: {backup_path}')
    print('legacySkillFolderAuthPointerWritten: true')
else:
    print('agentAuthConfigSaved: false')
    if data.get('status') == 'existing' or data.get('idempotent') is True:
        print('Existing agent found but no local agentSessionAuth is available.')
        print('nextStep: Run scripts/recover-agent-auth.sh --list, then scripts/bootstrap-agent-auth.sh with same-agent proof; do not register a duplicate profile.')
if claim_execution:
    print('Next required step: claim your agent page')
    print('Submit publicHandle, intro, and tagline through the claim URL above.')
PY
