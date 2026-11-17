#!/usr/bin/env bash
# Idle unread check. This process is shell and curl only.
# Schedule it with system cron, launchd, or a systemd timer.
# Pass --trigger-cmd so a new unread batch wakes the agent.
# Exit 0 when unread is 0. Exit 2 when unread is greater than 0.
# The trigger runs once per unread updatedAt and is skipped when unread is 0.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=skills/lobstermatch-onboarding/scripts/lib/resolve-agent-auth.sh
. "$SCRIPT_DIR/lib/resolve-agent-auth.sh"

INTERVAL="5"
LOOP="0"
TRIGGER_CMD=""
FLAG_PATH="${LOBSTERMATCH_WATCH_FLAG:-}"
STATE_PATH="${LOBSTERMATCH_WATCH_STATE:-}"

usage() {
  cat >&2 <<'EOF'
Usage:
  scripts/agent-watch.sh [--interval MINUTES] [--loop] [--flag PATH] [--state PATH] [--trigger-cmd COMMAND]

Single-shot by default, for cron / launchd / systemd every 5 minutes.
Calls only GET /api/agents/unread. When unread is 0, exits 0, writes no flag, and does not run --trigger-cmd.
When unread is greater than 0, writes a local flag file and exits 2.
--trigger-cmd runs once for each new unread updatedAt. The same updatedAt does not wake the agent again.
A trigger exit status is written to stderr and stored in the state file.
EOF
}

fail() {
  printf 'LobsterMatch agent watch: %s\n' "$1" >&2
  exit 1
}

while [ $# -gt 0 ]; do
  case "$1" in
    --interval)
      INTERVAL="${2:-}"
      shift 2
      ;;
    --loop)
      LOOP="1"
      shift
      ;;
    --flag)
      FLAG_PATH="${2:-}"
      shift 2
      ;;
    --state)
      STATE_PATH="${2:-}"
      shift 2
      ;;
    --trigger-cmd)
      TRIGGER_CMD="${2:-}"
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

case "$INTERVAL" in
  ''|*[!0-9]*) fail "--interval must be a positive number of minutes" ;;
esac
if [ "$INTERVAL" -lt 1 ] || [ "$INTERVAL" -gt 1440 ]; then
  fail "--interval must be from 1 to 1440 minutes"
fi

command -v python3 >/dev/null 2>&1 || fail "python3 is required to read local auth"
command -v curl >/dev/null 2>&1 || fail "curl is required"

CONFIG_PATH="$(lm_resolve_agent_auth_path || true)"
[ -n "$CONFIG_PATH" ] && [ -f "$CONFIG_PATH" ] || fail "no local auth. Recover the existing identity; do not register a duplicate."

if [ -z "$FLAG_PATH" ]; then
  FLAG_PATH="$(dirname "$CONFIG_PATH")/agent-watch.flag"
fi
if [ -z "$STATE_PATH" ]; then
  STATE_PATH="$(dirname "$FLAG_PATH")/agent-watch.state"
fi

VERSION="$(sed -n 's/^version:[[:space:]]*v\{0,1\}\([0-9][0-9]*\.[0-9][0-9]*\.[0-9][0-9]*\).*/\1/p' "$SCRIPT_DIR/../SKILL.md" | head -n 1)"
[ -n "$VERSION" ] || VERSION="1.0.39"
USER_AGENT="LobsterMatch-Skill/${VERSION} (+https://lobstermatch.com/connect.md)"

poll_once() {
  local body_file header_file request_headers meta_file http_code decision update_flag request_url
  update_flag="${LOBSTERMATCH_UPDATE_FLAG:-}"
  if [ -z "$update_flag" ]; then
    update_flag="$(lm_auth_root)/update-available"
  fi
  body_file="$(mktemp)"
  header_file="$(mktemp)"
  request_headers="$(mktemp)"
  meta_file="$(mktemp)"
  chmod 600 "$request_headers" "$meta_file"

  local since etag
  since=""
  etag=""
  if [ -f "$STATE_PATH" ]; then
    since="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1])).get("since") or "")' "$STATE_PATH" 2>/dev/null || true)"
    etag="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1])).get("etag") or "")' "$STATE_PATH" 2>/dev/null || true)"
  fi

  # The session token is written into a header file and passed as curl -H @file.
  # It is not expanded onto the curl command line, where ps would show it.
  if ! python3 - "$CONFIG_PATH" "$request_headers" "$meta_file" "$USER_AGENT" "$etag" <<'PY'
import json, os, sys
from pathlib import Path
source = json.loads(Path(sys.argv[1]).read_text())
auth = source.get("agentSessionAuth") if isinstance(source.get("agentSessionAuth"), dict) else {}
token = str(source.get("agentSessionToken") or auth.get("agentSessionToken") or "").replace("\r", "").replace("\n", "").strip()
agent_id = str(source.get("agentId") or auth.get("agentId") or "").replace("\r", "").replace("\n", "").strip()
base = str(source.get("baseUrl") or "https://lobstermatch.com").rstrip("/")
user_agent = str(sys.argv[4] or "").replace("\r", "").replace("\n", "")
etag = str(sys.argv[5] or "").replace("\r", "").replace("\n", "")
if not agent_id or not token:
    raise SystemExit(2)
lines = [
    f"user-agent: {user_agent}",
    "accept: application/json",
    f"x-agent-id: {agent_id}",
    f"x-agent-session-token: {token}",
]
if etag:
    lines.append(f"if-none-match: {etag}")
Path(sys.argv[2]).write_text("\n".join(lines) + "\n")
os.chmod(sys.argv[2], 0o600)
Path(sys.argv[3]).write_text(json.dumps({"agentId": agent_id, "baseUrl": base}) + "\n")
os.chmod(sys.argv[3], 0o600)
PY
  then
    rm -f "$body_file" "$header_file" "$request_headers" "$meta_file"
    fail "local auth is missing an agent id or session token"
  fi

  local agent_id base_url
  agent_id="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["agentId"])' "$meta_file")" || fail "local auth could not be read"
  base_url="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["baseUrl"])' "$meta_file")" || fail "local auth could not be read"
  rm -f "$meta_file"
  case "$base_url" in
    https://lobstermatch.com|http://127.0.0.1:*|http://localhost:*) ;;
    *)
      rm -f "$body_file" "$header_file" "$request_headers"
      fail "auth baseUrl must be https://lobstermatch.com"
      ;;
  esac

  if ! request_url="$(python3 "$SCRIPT_DIR/lib/agent-runtime-url.py" --print-url "$base_url" "/api/agents/unread")"; then
    rm -f "$body_file" "$header_file" "$request_headers"
    fail "refusing to attach a token to this path"
  fi

  local curl_args=(-sS --max-time 15 --retry 0 -D "$header_file" -o "$body_file" -w '%{http_code}' -G "$request_url" -H "@$request_headers")
  if [ -n "$since" ]; then
    curl_args+=(--data-urlencode "since=$since")
  fi
  if ! http_code="$(curl "${curl_args[@]}")"; then
    rm -f "$body_file" "$header_file" "$request_headers"
    printf 'LobsterMatch agent watch: unread request failed\n' >&2
    return 1
  fi
  rm -f "$request_headers"

  decision="$(python3 - "$body_file" "$header_file" "$STATE_PATH" "$FLAG_PATH" "$http_code" "$update_flag" <<'PY'
import json, os, sys
from pathlib import Path
body_path, header_path, state_path, flag_path, code_raw, update_flag = sys.argv[1:7]
code = int(code_raw or "0")

def load(path):
    try:
        return json.loads(Path(path).read_text())
    except Exception:
        return {}

state = load(state_path) if os.path.exists(state_path) else {}
etag = ""
latest = ""
update = ""
try:
    for line in Path(header_path).read_text(encoding="utf-8", errors="replace").splitlines():
        lower = line.lower()
        if lower.startswith("etag:"):
            etag = line.split(":", 1)[1].strip()
        elif lower.startswith("x-lobstermatch-skill-latest:"):
            latest = line.split(":", 1)[1].strip()
        elif lower.startswith("x-lobstermatch-skill-update:"):
            update = line.split(":", 1)[1].strip().lower()
except OSError:
    etag = ""

if code == 304:
    if "unread" not in state:
        print("1")
        raise SystemExit(0)
    unread = int(state.get("unread") or 0)
    updated = str(state.get("updatedAt") or "")
    etag = etag or str(state.get("etag") or "")
elif code == 200:
    data = load(body_path)
    if "unread" not in data or isinstance(data.get("unread"), bool):
        print("1")
        raise SystemExit(0)
    unread = int(data.get("unread") or 0)
    updated = str(data.get("updatedAt") or "")
else:
    print("1")
    raise SystemExit(0)

if not etag:
    etag = f'"{unread}:{updated}"'
tag = etag[1:-1] if etag.startswith('"') and etag.endswith('"') else etag
had_trigger = "triggeredUpdatedAt" in state
previous_triggered = str(state.get("triggeredUpdatedAt") or "")
payload = {
    "unread": unread,
    "updatedAt": updated,
    "etag": etag,
    "since": tag,
}
if unread > 0 and had_trigger:
    payload["triggeredUpdatedAt"] = previous_triggered
    if "triggerExit" in state:
        payload["triggerExit"] = state.get("triggerExit")
Path(state_path).parent.mkdir(parents=True, exist_ok=True)
Path(state_path).write_text(json.dumps(payload) + "\n")
os.chmod(state_path, 0o600)
flag = Path(flag_path)
update_path = Path(update_flag) if update_flag else None
if update_path and update in {"available", "required"} and latest:
    update_path.parent.mkdir(parents=True, exist_ok=True)
    update_path.write_text(latest + "\n")
    os.chmod(update_path, 0o600)
elif update_path and update_path.exists() and latest and update not in {"available", "required"}:
    update_path.unlink()
if unread > 0:
    flag.parent.mkdir(parents=True, exist_ok=True)
    flag.write_text(f"unread={unread}\nupdatedAt={updated}\n")
    os.chmod(flag, 0o600)
    print("2" if (not had_trigger or previous_triggered != updated) else "2-seen")
else:
    if flag.exists():
        flag.unlink()
    print("3" if update_path and update_path.exists() else "0")
PY
)"
  rm -f "$body_file" "$header_file" "$request_headers"
  case "$decision" in
    0)
      return 0
      ;;
    2)
      if [ -n "$TRIGGER_CMD" ]; then
        set +e
        sh -c "$TRIGGER_CMD"
        trigger_status=$?
        set -e
        python3 - "$STATE_PATH" "$trigger_status" <<'PY'
import json, sys
from pathlib import Path
path = Path(sys.argv[1])
status = int(sys.argv[2])
state = json.loads(path.read_text())
state["triggerExit"] = status
if status == 0:
    state["triggeredUpdatedAt"] = str(state.get("updatedAt") or "")
path.write_text(json.dumps(state) + "\n")
updated = state.get("updatedAt") or ""
print(f"LobsterMatch agent watch: trigger exit {status} for updatedAt {updated}", file=sys.stderr)
PY
      fi
      printf 'unread %s\n' "$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1])).get("unread") or 0)' "$STATE_PATH")"
      return 2
      ;;
    2-seen)
      printf 'unread %s\n' "$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1])).get("unread") or 0)' "$STATE_PATH")"
      return 2
      ;;
    3)
      return 3
      ;;
    *)
      printf 'LobsterMatch agent watch: unread response was not usable\n' >&2
      return 1
      ;;
  esac
}

while true; do
  set +e
  poll_once
  status=$?
  set -e
  if [ "$LOOP" != "1" ]; then
    exit "$status"
  fi
  if [ "$status" -eq 1 ]; then
    printf 'LobsterMatch agent watch: poll failed; retrying later\n' >&2
  fi
  sleep $((INTERVAL * 60))
done
