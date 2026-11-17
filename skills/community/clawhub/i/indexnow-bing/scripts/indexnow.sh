#!/bin/bash
set -e
script_dir=$(dirname -- "${BASH_SOURCE[0]}")
exec python3 "$script_dir/indexnow.py" "$@"
