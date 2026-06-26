#!/usr/bin/env bash
set -euo pipefail

VAULT_PATH="$(realpath -m "${1:-/root/obsidian-vault}")"
OBS_CMD="${OBS_CMD:-/usr/local/bin/obs}"
MARKER="skill verification $(date -u +%Y%m%d-%H%M%S)"
TMPDIR="$(mktemp -d)"
trap 'rm -rf "$TMPDIR"' EXIT

if [[ ! -x "$OBS_CMD" ]]; then
  echo "Wrapper not found: $OBS_CMD" >&2
  exit 1
fi

if [[ ! -d "$VAULT_PATH" ]]; then
  echo "Vault path not found: $VAULT_PATH" >&2
  exit 1
fi

echo "== help =="
"$OBS_CMD" help >"$TMPDIR/help.out" 2>&1
sed -n '1,20p' "$TMPDIR/help.out"

echo "== vault =="
"$OBS_CMD" vault

echo "== daily:path =="
"$OBS_CMD" daily:path

echo "== daily:append =="
"$OBS_CMD" daily:append content="$MARKER"

echo "== daily:read =="
"$OBS_CMD" daily:read | tail -n 20

echo "== search =="
"$OBS_CMD" search query="$MARKER"

echo "Verification complete for vault: $VAULT_PATH"
