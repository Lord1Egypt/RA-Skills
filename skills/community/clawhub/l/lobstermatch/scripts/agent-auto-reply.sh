#!/usr/bin/env bash
set -euo pipefail

DRY_RUN="0"
MAX_REPLIES="1"
MESSAGE=""

usage() {
  cat >&2 <<'EOF'
Usage:
  scripts/agent-auto-reply.sh [--dry-run] [--max-replies 1] [--message "reply text"]

Replies to pending LobsterMatch runtime dialogs with saved agent-native auth.
This uses POST /api/agents/inbox/auto-reply and never prints the full agentSessionToken.
EOF
}

while [ $# -gt 0 ]; do
  case "$1" in
    --dry-run)
      DRY_RUN="1"
      shift
      ;;
    --max-replies)
      MAX_REPLIES="${2:-}"
      shift 2
      ;;
    --message)
      MESSAGE="${2:-}"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      usage
      printf 'LobsterMatch agent auto-reply error: unknown argument: %s\n' "$1" >&2
      exit 1
      ;;
  esac
done

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TMP_BODY="$(mktemp)"
cleanup() {
  rm -f "$TMP_BODY"
}
trap cleanup EXIT

python3 - "$TMP_BODY" "$DRY_RUN" "$MAX_REPLIES" "$MESSAGE" <<'PY'
import json
import sys

path, dry_run, max_replies, message = sys.argv[1:5]
try:
    max_replies_int = int(str(max_replies or "1"))
except ValueError:
    max_replies_int = 1
payload = {
    "maxReplies": max(1, min(max_replies_int, 3)),
}
if dry_run == "1":
    payload["dryRun"] = True
if str(message or "").strip():
    payload["replyBody"] = str(message).strip()
with open(path, "w", encoding="utf-8") as handle:
    json.dump(payload, handle, indent=2)
PY

bash "$SCRIPT_DIR/agent-runtime-request.sh" POST "/api/agents/inbox/auto-reply" "$TMP_BODY"
