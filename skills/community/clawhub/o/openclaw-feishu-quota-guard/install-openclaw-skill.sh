#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
if command -v python3 >/dev/null 2>&1; then
  python3 "$script_dir/install_openclaw_skill.py" "$@"
else
  python "$script_dir/install_openclaw_skill.py" "$@"
fi
