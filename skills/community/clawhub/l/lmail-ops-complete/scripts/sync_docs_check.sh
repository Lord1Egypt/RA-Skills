#!/usr/bin/env bash
set -euo pipefail

PRIMARY="/opt/lmail/lmail-docs"
SECONDARY="/opt/lmail/apps/dashboard/public/lmail-docs"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --primary)
      PRIMARY="$2"
      shift 2
      ;;
    --secondary)
      SECONDARY="$2"
      shift 2
      ;;
    -h|--help)
      cat <<'USAGE'
Usage: sync_docs_check.sh [--primary DIR] [--secondary DIR]

Compares required shared LMail docs files between two directories.
USAGE
      exit 0
      ;;
    *)
      echo "Unknown arg: $1" >&2
      exit 1
      ;;
  esac
done

shared_files=(
  "AGENT_HANDOFF_PROMPT.md"
  "AGENT_QUICKSTART.md"
  "AGENT_TOOLS.json"
  "AGENT_SPEC.json"
  "AGENT_DOCS_INDEX.md"
)

status=0
for f in "${shared_files[@]}"; do
  p="$PRIMARY/$f"
  s="$SECONDARY/$f"

  if [[ ! -f "$p" ]]; then
    echo "[ERR] missing in primary: $p"
    status=1
    continue
  fi
  if [[ ! -f "$s" ]]; then
    echo "[ERR] missing in secondary: $s"
    status=1
    continue
  fi

  hp="$(sha256sum "$p" | awk '{print $1}')"
  hs="$(sha256sum "$s" | awk '{print $1}')"

  if [[ "$hp" == "$hs" ]]; then
    echo "[OK] synced: $f"
  else
    echo "[DIFF] mismatch: $f"
    status=1
  fi
done

if [[ "$status" -ne 0 ]]; then
  echo "[FAIL] docs are not synchronized"
  exit 1
fi

echo "[DONE] docs are synchronized"
