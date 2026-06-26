#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$ROOT_DIR/.venv"
REQ_FILE="$ROOT_DIR/requirements.txt"
ENV_EXAMPLE_FILE="$ROOT_DIR/env-example.txt"
CONFIG_DIR="$HOME/.config/gitea-routine-report"
ENV_FILE="$CONFIG_DIR/.env"

if ! command -v python3 >/dev/null 2>&1; then
  echo "Error: python3 not found. Please install Python 3 first."
  exit 1
fi

if [[ ! -f "$REQ_FILE" ]]; then
  echo "Error: requirements.txt not found at $REQ_FILE"
  exit 1
fi

if [[ ! -f "$ENV_EXAMPLE_FILE" ]]; then
  echo "Error: env-example.txt not found at $ENV_EXAMPLE_FILE"
  exit 1
fi

mkdir -p "$CONFIG_DIR"

echo "[1/4] Creating virtual environment..."
if [[ ! -d "$VENV_DIR" ]]; then
  python3 -m venv "$VENV_DIR"
fi

# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"

echo "[2/4] Upgrading pip..."
python -m pip install --upgrade pip

echo "[3/4] Installing dependencies..."
pip install -r "$REQ_FILE"

if [[ ! -f "$ENV_FILE" ]]; then
  cp "$ENV_EXAMPLE_FILE" "$ENV_FILE"
  echo "[4/4] Created .env from env-example.txt at $ENV_FILE"
  echo "Please edit $ENV_FILE and set real values before running scripts."
else
  echo "[4/4] .env already exists at $ENV_FILE, skipped."
fi

echo
echo "Setup complete."
echo "Activate environment: source .venv/bin/activate"
echo "Run report: python scripts/generate_report.py --hours 168"
