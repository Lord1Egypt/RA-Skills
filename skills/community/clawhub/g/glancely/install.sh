#!/usr/bin/env bash
# glancely — one-shot installer for macOS / Linux.
#
#     pip install glancely
#     glancely setup
#
# On macOS with Homebrew Python (PEP 668), use pipx instead:
#     brew install pipx && pipx install glancely && glancely setup
#
set -euo pipefail

PYTHON_BIN="${PYTHON:-python3}"

step() { printf "\n\033[1;36m==> %s\033[0m\n" "$*"; }

if ! "$PYTHON_BIN" -c "import sys; sys.exit(0 if sys.version_info >= (3,9) else 1)"; then
  echo "Need Python 3.9+; have $($PYTHON_BIN --version)"; exit 1
fi

# Prefer pip3, fall back to pip
if command -v pip3 &>/dev/null; then
  PIP_BIN=pip3
elif command -v pip &>/dev/null; then
  PIP_BIN=pip
else
  echo "pip not found. Install pip or pipx and try again."
  exit 1
fi

step "Installing glancely package"
if "$PIP_BIN" install glancely 2>/dev/null; then
  echo "Installed from PyPI."
elif [ -f "$(dirname "${BASH_SOURCE[0]}")/pyproject.toml" ]; then
  echo "PyPI not reachable; installing from local source..."
  "$PIP_BIN" install --break-system-packages "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)" 2>/dev/null || \
    "$PIP_BIN" install "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
else
  echo "glancely not found on PyPI and no local pyproject.toml. Clone the repo first:"
  echo "  git clone https://github.com/JunjieYu95/glancely.git && cd glancely && bash install.sh"
  exit 1
fi

step "Running setup (migrations only)"
glancely setup

cat <<EOF

Done. Try it:
  glancely list
  glancely version

To create your first tracker:
  Just tell your agent what you want to track!
EOF
