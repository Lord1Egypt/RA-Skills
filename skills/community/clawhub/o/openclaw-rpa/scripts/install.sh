#!/usr/bin/env bash
# Install Python deps + Playwright Chromium (macOS / Linux).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 not found. Install Python 3.8+ from https://www.python.org/downloads/ or your OS package manager." >&2
  exit 1
fi

echo "==> venv: .venv"
python3 -m venv .venv
# shellcheck source=/dev/null
source .venv/bin/activate

echo "==> pip install -r requirements.txt"
python -m pip install -U pip
python -m pip install -r requirements.txt

echo "==> playwright install chromium"
python -m playwright install chromium

echo ""
echo "Done. Activate the venv before using this skill:"
echo "  source .venv/bin/activate"
echo "Then verify:"
echo "  python3 envcheck.py"
echo "  python3 rpa_manager.py env-check"
