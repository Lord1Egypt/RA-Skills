#!/bin/bash

set -euo pipefail

AGENT_ID="main"
SESSIONS_DIR="${HOME}/.openclaw/agents/${AGENT_ID}/sessions"
FILE=""

usage() {
  cat <<EOF
Usage: ./whoami.sh [--agent-id <id>] [--sessions-dir <path>] [--file <jsonl>]
Best-effort extraction of the most recent sender_id from session logs.
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --agent-id)
      AGENT_ID="$2"
      SESSIONS_DIR="${HOME}/.openclaw/agents/${AGENT_ID}/sessions"
      shift 2
      ;;
    --sessions-dir)
      SESSIONS_DIR="$2"
      shift 2
      ;;
    --file)
      FILE="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage
      exit 1
      ;;
  esac
done

if [[ -z "${FILE}" ]]; then
  FILE="$(ls -t "${SESSIONS_DIR}"/*.jsonl* 2>/dev/null | head -n 1 || true)"
fi

if [[ -z "${FILE}" || ! -f "${FILE}" ]]; then
  echo "No session file found. Try: ./whoami.sh --sessions-dir <path>" >&2
  exit 1
fi

if ! command -v rg >/dev/null 2>&1; then
  echo "ripgrep (rg) is required for whoami.sh" >&2
  exit 1
fi

SENDER_ID="$(rg -o '"sender_id":\\s*"[^"]+"' "${FILE}" | tail -n 1 | sed -E 's/.*"sender_id":\\s*"([^"]+)".*/\\1/')"

if [[ -z "${SENDER_ID}" ]]; then
  echo "sender_id not found in ${FILE}" >&2
  exit 1
fi

echo "${SENDER_ID}"
