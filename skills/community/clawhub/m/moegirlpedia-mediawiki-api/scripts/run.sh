#!/usr/bin/env bash
set -euo pipefail

base_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$base_dir"

if [[ ! -f dist/index.js ]]; then
    echo "Expected dist/index.js to exist!" >&2
    exit 1
fi

node dist/index.js "$@"
