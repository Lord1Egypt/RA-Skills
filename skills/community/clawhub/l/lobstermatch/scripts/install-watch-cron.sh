#!/usr/bin/env bash
# Install one crontab line that polls unread and wakes the agent once per new batch.
# Running it again replaces the previous LobsterMatch watch line.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
INTERVAL="5"
TRIGGER_CMD=""
MARKER="# lobstermatch-agent-watch"

usage() {
  cat >&2 <<'EOF'
Usage:
  scripts/install-watch-cron.sh --trigger-cmd COMMAND [--interval MINUTES]

Installs an idempotent crontab entry for scripts/agent-watch.sh.
The command runs every 5 minutes and passes --trigger-cmd through.
A second run replaces the previous LobsterMatch watch line and leaves other crontab lines in place.

OpenClaw wake, from https://docs.openclaw.ai/cli/agent (a session selector is required):
  bash scripts/install-watch-cron.sh --trigger-cmd 'openclaw agent --agent main --message "Read unread LobsterMatch messages and reply"'

OpenClaw wake that returns when the Gateway accepts it, from https://docs.openclaw.ai/cli/system.
--mode now is required. The default mode waits for HEARTBEAT:
  bash scripts/install-watch-cron.sh --trigger-cmd 'openclaw system event --text "Read unread LobsterMatch messages and reply" --mode now'

Another runtime supplies its own command that starts one agent turn:
  bash scripts/install-watch-cron.sh --trigger-cmd 'your-agent turn --message "Read unread LobsterMatch messages and reply"'
EOF
}

fail() {
  printf 'LobsterMatch watch cron: %s\n' "$1" >&2
  exit 1
}

while [ $# -gt 0 ]; do
  case "$1" in
    --trigger-cmd)
      TRIGGER_CMD="${2:-}"
      shift 2
      ;;
    --interval)
      INTERVAL="${2:-}"
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

[ -n "$TRIGGER_CMD" ] || fail "--trigger-cmd is required. A flag-only cron does not wake the agent."
case "$INTERVAL" in
  ''|*[!0-9]*) fail "--interval must be a positive number of minutes" ;;
esac
if [ "$INTERVAL" -lt 1 ] || [ "$INTERVAL" -gt 1440 ]; then
  fail "--interval must be from 1 to 1440 minutes"
fi
command -v python3 >/dev/null 2>&1 || fail "python3 is required"

CRON_LINE="$(python3 - "$SKILL_DIR" "$TRIGGER_CMD" "$INTERVAL" <<'PY'
import shlex, sys
skill, trigger, interval = sys.argv[1:4]
watch = f"cd {shlex.quote(skill)} && bash scripts/agent-watch.sh --trigger-cmd {shlex.quote(trigger)}"
print(f"*/{int(interval)} * * * * {watch}")
PY
)"

EXISTING=""
if [ -n "${LOBSTERMATCH_CRONTAB_FILE:-}" ]; then
  if [ -f "$LOBSTERMATCH_CRONTAB_FILE" ]; then
    EXISTING="$(cat "$LOBSTERMATCH_CRONTAB_FILE")"
  fi
else
  command -v crontab >/dev/null 2>&1 || fail "crontab is required"
  EXISTING="$(crontab -l 2>/dev/null || true)"
fi

EXISTING_FILE="$(mktemp)"
chmod 600 "$EXISTING_FILE"
printf '%s' "$EXISTING" > "$EXISTING_FILE"
UPDATED="$(python3 - "$SKILL_DIR" "$MARKER" "$CRON_LINE" "$EXISTING_FILE" <<'PY'
import sys
from pathlib import Path
skill, marker, cron_line, existing_path = sys.argv[1:5]
text = Path(existing_path).read_text()
lines = text.splitlines()
kept = []
skip_next = False
for line in lines:
    if skip_next:
        skip_next = False
        if "agent-watch.sh" in line:
            continue
    if line.strip() == marker:
        skip_next = True
        continue
    if "agent-watch.sh" in line and skill in line:
        continue
    kept.append(line)
while kept and kept[-1] == "":
    kept.pop()
kept.extend([marker, cron_line])
print("\n".join(kept) + "\n")
PY
)"
rm -f "$EXISTING_FILE"

if [ -n "${LOBSTERMATCH_CRONTAB_FILE:-}" ]; then
  umask 077
  printf '%s' "$UPDATED" > "$LOBSTERMATCH_CRONTAB_FILE"
else
  tmp="$(mktemp)"
  chmod 600 "$tmp"
  printf '%s' "$UPDATED" > "$tmp"
  crontab "$tmp"
  rm -f "$tmp"
fi

printf '%s\n' "$CRON_LINE"
