#!/usr/bin/env bash
# Run a pdfparse script with a Python interpreter that actually has PyMuPDF.
#
#   run.sh <script.py> [args...]
#
# Why this exists: `python3` on this machine resolves to /usr/bin/python3, which
# does not have PyMuPDF installed. PyMuPDF lives in the Homebrew interpreter.
# This wrapper finds the right one instead of assuming.
#
# Override with:  PYTHON=/path/to/python3 run.sh <script.py> ...
set -euo pipefail

if [ $# -lt 1 ]; then
    echo "usage: run.sh <script.py> [args...]" >&2
    exit 2
fi

SCRIPT="$1"
shift

if [ ! -f "$SCRIPT" ]; then
    echo "ERROR: script not found: $SCRIPT" >&2
    exit 2
fi

find_python() {
    local candidates=()
    [ -n "${PYTHON:-}" ] && candidates+=("$PYTHON")
    candidates+=(
        /opt/homebrew/bin/python3
        /usr/local/bin/python3
        "$(command -v python3.13 || true)"
        "$(command -v python3.12 || true)"
        "$(command -v python3.11 || true)"
        "$(command -v python3 || true)"
        /usr/bin/python3
    )

    local py
    for py in "${candidates[@]}"; do
        [ -n "$py" ] && [ -x "$py" ] || continue
        # The scripts use `X | None` annotations, which need Python 3.10+.
        "$py" -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)' \
            >/dev/null 2>&1 || continue
        # Accept either module name: pymupdf (new) or fitz (old).
        if "$py" -c 'import pymupdf' >/dev/null 2>&1 \
        || "$py" -c 'import fitz' >/dev/null 2>&1; then
            printf '%s\n' "$py"
            return 0
        fi
    done
    return 1
}

if ! PYBIN="$(find_python)"; then
    echo "ERROR: no Python 3.10+ interpreter with PyMuPDF found." >&2
    echo "  install it:  /opt/homebrew/bin/python3 -m pip install pymupdf" >&2
    echo "  or override: PYTHON=/path/to/python3 $0 $SCRIPT ..." >&2
    exit 127
fi

exec "$PYBIN" "$SCRIPT" "$@"
