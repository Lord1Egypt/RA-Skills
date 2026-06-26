#!/usr/bin/env bash
set -euo pipefail

commands=(nfc-list nfc-poll nfc-taginfo)
missing=()

for cmd in "${commands[@]}"; do
  if ! command -v "$cmd" >/dev/null 2>&1; then
    missing+=("$cmd")
  fi
done

if [ "${#missing[@]}" -gt 0 ]; then
  echo "[nfc-check] missing commands: ${missing[*]}"
  echo "[nfc-check] install libnfc/nfc-utils before continuing."
else
  echo "[nfc-check] all CLI tools present: ${commands[*]}"
fi

if command -v nfc-list >/dev/null 2>&1; then
  if nfc-list --help >/dev/null 2>&1; then
    echo "[nfc-check] nfc-list --help succeeded."
  else
    echo "[nfc-check] nfc-list --help failed; printing version if available."
    nfc-list --version 2>/dev/null || true
  fi
else
  echo "[nfc-check] nfc-list is not installed, skipping runtime check."
fi

echo "[nfc-check] environment check complete."
