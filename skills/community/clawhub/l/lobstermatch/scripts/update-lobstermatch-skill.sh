#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
RUN_UPDATE="0"

usage() {
  cat >&2 <<'EOF'
Usage:
  scripts/update-lobstermatch-skill.sh
  scripts/update-lobstermatch-skill.sh --run-update

Backs up/migrates LobsterMatch agent auth outside the replaceable skill folder,
prints safe update instructions, and verifies auth status after update. It never
prints raw tokens.
EOF
}

while [ $# -gt 0 ]; do
  case "$1" in
    --run-update)
      RUN_UPDATE="1"
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      usage
      printf 'LobsterMatch skill update wrapper error: unknown argument: %s\n' "$1" >&2
      exit 2
      ;;
  esac
done

printf 'LobsterMatch skill update wrapper\n'
printf 'step: backup-and-migrate-auth\n'
bash "$SCRIPT_DIR/preserve-local-auth.sh" backup || true

if [ "$RUN_UPDATE" = "1" ]; then
  if command -v clawhub >/dev/null 2>&1; then
    printf 'step: running-clawhub-update\n'
    clawhub update lobstermatch
  elif command -v openclaw >/dev/null 2>&1; then
    printf 'step: running-openclaw-skill-update\n'
    openclaw skill update lobstermatch
  else
    printf 'step: update-command-not-found\n'
    printf 'runOneOf:\n'
    printf '  clawhub update lobstermatch\n'
    printf '  openclaw skill update lobstermatch\n'
  fi
else
  printf 'step: update-command-not-run\n'
  printf 'safeUpdateCommands:\n'
  printf '  clawhub update lobstermatch\n'
  printf '  openclaw skill update lobstermatch\n'
  printf 'note: persistent auth should survive folder replacement even if this wrapper is not used.\n'
fi

printf 'step: restore-or-confirm-persistent-auth\n'
bash "$SCRIPT_DIR/preserve-local-auth.sh" restore || true

printf 'step: auth-status\n'
bash "$SCRIPT_DIR/agent-auth-status.sh" || true

printf 'rawTokenPrinted: false\n'
