#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=/dev/null
source "$script_dir/vault-env.sh"

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <secret-path> [vault-kv-get-args...]" >&2
  exit 2
fi

path="$1"
shift

vault kv get "$path" "$@"
