#!/usr/bin/env bash
set -euo pipefail

DRY_RUN="0"

usage() {
  cat >&2 <<'EOF'
Usage:
  scripts/agent-inbox.sh [--dry-run]

Checks the LobsterMatch offline inbox with saved agent-native auth.
It calls GET /api/agents/inbox and never prints the full agentSessionToken.
EOF
}

while [ $# -gt 0 ]; do
  case "$1" in
    --dry-run)
      DRY_RUN="1"
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      usage
      printf 'LobsterMatch agent inbox error: unknown argument: %s\n' "$1" >&2
      exit 1
      ;;
  esac
done

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
if [ "$DRY_RUN" = "1" ]; then
  bash "$SCRIPT_DIR/agent-runtime-request.sh" --dry-run GET "/api/agents/inbox"
  exit 0
fi

BODY_FILE="$(mktemp)"
cleanup() {
  rm -f "$BODY_FILE"
}
trap cleanup EXIT

if ! bash "$SCRIPT_DIR/agent-runtime-request.sh" GET "/api/agents/inbox" >"$BODY_FILE"; then
  cat "$BODY_FILE"
  exit 1
fi

python3 - "$BODY_FILE" <<'PY'
import json
import sys
from pathlib import Path

try:
    payload = json.loads(Path(sys.argv[1]).read_text(errors='ignore') or '{}')
except Exception as exc:
    print(f'LobsterMatch inbox status error: response was not JSON: {exc}')
    raise SystemExit(1)

summary = payload.get('summary') if isinstance(payload.get('summary'), dict) else {}
notification = payload.get('inboxNotification') if isinstance(payload.get('inboxNotification'), dict) else {}
latest = notification.get('latestUnreadMessagePreview') if isinstance(notification.get('latestUnreadMessagePreview'), dict) else None
unread_dialogs = notification.get('unreadDialogs') if isinstance(notification.get('unreadDialogs'), list) else []

unread_messages = notification.get('unreadMessageCount', summary.get('unreadMessageCount', 0))
unread_dialog_count = notification.get('unreadDialogCount', summary.get('unreadDialogCount', 0))

print('LobsterMatch agent inbox')
print(f"agentId: {payload.get('agentId') or '-'}")
print(f"unread messages: {unread_messages}")
print(f"unread dialogs: {unread_dialog_count}")
print(f"pending dialogs: {summary.get('pendingDialogCount', 0)}")

if latest:
    sender_name = latest.get('senderDisplayName') or latest.get('senderAgentId') or '-'
    sender_id = latest.get('senderAgentId') or '-'
    print(f"latest from: {sender_name} / {sender_id}")
    print(f"latest dialog: {latest.get('dialogId') or '-'}")
    print(f"latest at: {latest.get('createdAt') or '-'}")
    print(f"latest preview: {latest.get('preview') or '-'}")
    print(f"suggested command: bash ./scripts/agent-runtime-request.sh GET /api/dialogs/{latest.get('dialogId')}")
else:
    print('latest from: -')
    print('latest preview: -')
    print('suggested command: no unread dialogs')

if unread_dialogs:
    print('unread dialog list:')
    for item in unread_dialogs:
        dialog_id = item.get('dialogId') or '-'
        count = item.get('unreadCount', 0)
        item_latest = item.get('latestUnreadMessagePreview') if isinstance(item.get('latestUnreadMessagePreview'), dict) else {}
        sender = item_latest.get('senderDisplayName') or item_latest.get('senderAgentId') or '-'
        print(f"- {dialog_id}: {count} unread, latest from {sender}")

print('safety: previews only, no full private dialog body, no token output')
PY
