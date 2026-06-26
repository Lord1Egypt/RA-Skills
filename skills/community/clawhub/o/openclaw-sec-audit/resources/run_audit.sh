#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
RUNTIME_ROOT="${SCRIPT_DIR}/runtime"
PACKAGE_ROOT="${RUNTIME_ROOT}/openclaw_sec"

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 is required to run openclaw-sec-audit." >&2
  exit 127
fi

if [[ ! -f "${PACKAGE_ROOT}/__main__.py" ]]; then
  echo "Bundled runtime not found: ${PACKAGE_ROOT}" >&2
  echo "Rebuild it with: python3 scripts/build_skill_bundle.py" >&2
  exit 1
fi

export PYTHONPATH="${RUNTIME_ROOT}${PYTHONPATH:+:${PYTHONPATH}}"
exec python3 -m openclaw_sec audit "$@"
