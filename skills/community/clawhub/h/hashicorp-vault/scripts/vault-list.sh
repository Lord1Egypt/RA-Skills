#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=/dev/null
source "$script_dir/vault-env.sh"

path="${1:-secret/openclaw}"
shift || true

vault kv list "$path" "$@"
