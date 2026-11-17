#!/usr/bin/env bash
# One command that reproduces CI's Python job locally.
#
#   ./scripts/check.sh              # lint + tests + validators (full CI equivalent)
#   ./scripts/check.sh --lint-only  # fast path used by .githooks/pre-push
#
# Why this exists: CI has twice gone red on main purely because `ruff check`
# was never run before pushing. The gate here is only worth having if it cannot
# disagree with CI, so the ruff version is read from the workflow itself.
set -euo pipefail

# Fail with a sentence, not git's "fatal: not a git repository" (which reads
# like the tool is broken when the real problem is the working directory).
if ! repo_root="$(git rev-parse --show-toplevel 2>/dev/null)"; then
  echo "check: not inside a git checkout; run this from the iterate-skill repository." >&2
  exit 2
fi
cd "$repo_root"

PYTHON="${PYTHON:-}"
if [ -z "$PYTHON" ]; then
  if [ -x .venv/bin/python ]; then
    PYTHON=.venv/bin/python
  else
    PYTHON=python3
  fi
fi

PIN=$(sed -nE 's/.*pip install pytest "ruff==([^"]+)".*/\1/p' .github/workflows/ci.yml)
if [ -z "$PIN" ]; then
  echo "check: could not read the ruff pin from .github/workflows/ci.yml" >&2
  exit 1
fi

# Find a ruff that reports exactly the pinned version. PATH first (a plain
# `pipx/brew install` or an activated venv), then the interpreter resolved
# above. Anything else risks the local gate disagreeing with CI, which is how
# main caught fire twice already.
RUFF=()
if [ "$(ruff --version 2>/dev/null | awk '{print $2}')" = "$PIN" ]; then
  RUFF=(ruff)
elif [ "$("$PYTHON" -m ruff --version 2>/dev/null | awk '{print $2}')" = "$PIN" ]; then
  RUFF=("$PYTHON" -m ruff)
fi
if [ ${#RUFF[@]} -eq 0 ]; then
  # Exit 3, not 1: the gate could not run, which is not the same claim as
  # "your code fails lint". Callers must not report a lint verdict here.
  echo "check: needs ruff==$PIN (found $(ruff --version 2>/dev/null | awk '{print $2}' || true) on PATH, $("$PYTHON" -m ruff --version 2>/dev/null | awk '{print $2}' || true) in $PYTHON)." >&2
  echo "  Remedy: $PYTHON -m pip install 'ruff==$PIN'   (or set PYTHON=/path/to/venv/bin/python)" >&2
  exit 3
fi

echo "check: ruff $PIN via '${RUFF[*]}'"
# Array, not a string: "$RUFF" word-splits `python -m ruff` and breaks on any
# interpreter path containing a space.
"${RUFF[@]}" check scripts/ tests/ iterate_cli/

if [ "${1:-}" = "--lint-only" ]; then
  exit 0
fi

"$PYTHON" -m pytest tests/ -q
"$PYTHON" scripts/validate.py config config/iterate.config.yaml
"$PYTHON" scripts/validate.py decisions templates/iterate-decisions.template.md
"$PYTHON" -c "import json; json.load(open('config/config.schema.json'))"

echo "check: every CI-equivalent gate passed"
