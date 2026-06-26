#!/usr/bin/env bash
set -euo pipefail

: "${VAULT_ADDR:=http://192.168.1.101:8200}"
export VAULT_ADDR

token_file="${HOME}/.vault-token"
if [[ -z "${VAULT_TOKEN:-}" && -f "$token_file" ]]; then
  VAULT_TOKEN="$(< "$token_file")"
  export VAULT_TOKEN
fi

if [[ -z "${VAULT_TOKEN:-}" ]]; then
  echo "VAULT_TOKEN is not set and ${HOME}/.vault-token was not found" >&2
  exit 2
fi
