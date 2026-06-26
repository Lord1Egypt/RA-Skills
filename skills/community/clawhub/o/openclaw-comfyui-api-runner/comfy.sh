#!/usr/bin/env bash
set -euo pipefail

# ComfyUI Safe Connector entrypoint.
# Runs the Python runner from the skill root, regardless of the caller's CWD.

SKILL_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$SKILL_ROOT"

exec python3 scripts/run.py "$@"
