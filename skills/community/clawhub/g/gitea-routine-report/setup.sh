#!/usr/bin/env bash
# 文件用途：初始化本技能运行环境（虚拟环境、依赖安装、环境变量文件）。
# 输入：无命令行参数；依赖 requirements.txt 与 env-example.txt。
# 输出：创建 .venv 和 ~/.config/gitea-routine-report/.env，并在终端输出执行结果。
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
