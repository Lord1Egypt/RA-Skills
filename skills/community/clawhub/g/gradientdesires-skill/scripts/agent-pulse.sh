#!/usr/bin/env bash
# Read-only state check. Pass the previous state token optionally.
# No credentials, task state, or schedules are written by this script.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec bash "${SCRIPT_DIR}/gradientdesires.sh" pulse "${1:-}"
