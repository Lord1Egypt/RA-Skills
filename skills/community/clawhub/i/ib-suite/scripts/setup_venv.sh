#!/usr/bin/env bash
# Create the shared virtualenv and install ib-common (editable) + runtime deps.
# Idempotent: safe to re-run. The project requires Python >= 3.11, so this
# script picks the first >= 3.11 interpreter it finds instead of assuming the
# system `python3` qualifies (on many machines `python3` is still 3.9).
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

# Find a Python >= 3.11 interpreter from a portable candidate list.
find_python() {
  for cand in python3.13 python3.12 python3.11 /opt/miniconda3/bin/python python3; do
    if command -v "$cand" >/dev/null 2>&1 && \
       "$cand" -c 'import sys; sys.exit(0 if sys.version_info[:2] >= (3, 11) else 1)' 2>/dev/null; then
      echo "$cand"; return 0
    fi
  done
  return 1
}

PY="$(find_python)" || { echo "error: no Python >= 3.11 interpreter found on PATH" >&2; exit 1; }
echo "using interpreter: $PY ($("$PY" --version 2>&1))"

"$PY" -m venv .venv
# shellcheck disable=SC1091
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r ib-common/requirements.txt
echo "venv ready: $ROOT/.venv"
