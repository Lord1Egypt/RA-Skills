#!/usr/bin/env bash
# 重建 Online_MinerU 的 Python venv 并安装依赖
set -e
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$DIR"
python3 -m venv .venv
./.venv/bin/pip install --quiet --upgrade pip || true
./.venv/bin/pip install --quiet pypdf requests
./.venv/bin/python -c "import pypdf, requests; print('deps ok:', pypdf.__version__, requests.__version__)"
echo "venv ready at $DIR/.venv"
