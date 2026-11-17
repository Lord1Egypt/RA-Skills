#!/usr/bin/env bash
# 个股数据 Skill · 一键建 venv 并装依赖
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [ ! -d .venv ]; then
  python3 -m venv .venv
fi
# shellcheck disable=SC1091
source .venv/bin/activate
python -m pip install -r requirements.txt
echo ""
echo "OK: 依赖已装进 $ROOT/.venv"
echo "激活: source .venv/bin/activate"
echo "探针: python3 scripts/fetch.py --probe"
echo "取数: python3 scripts/fetch.py 603629 ./out/603629"
