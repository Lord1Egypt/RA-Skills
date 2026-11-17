#!/usr/bin/env bash
# Prepare workdir + optional venv for my-halala-sales-vp (private test).
set -euo pipefail

SKILL_DIR=$(cd -- "$(dirname -- "$0")/.." && pwd)
WORKDIR="${QIANLIMA_WORKDIR:-$HOME/.my-halala-sales-vp}"

mkdir -p "$WORKDIR"/{data,output,runtime}
chmod 700 "$WORKDIR" 2>/dev/null || true

if [[ ! -x "$WORKDIR/.venv/bin/python" ]]; then
  python3 -m venv "$WORKDIR/.venv"
  "$WORKDIR/.venv/bin/pip" install -U pip
  "$WORKDIR/.venv/bin/pip" install -r "$SKILL_DIR/requirements.txt"
fi

echo "QIANLIMA_WORKDIR=$WORKDIR"
echo "python=$WORKDIR/.venv/bin/python"
echo "Create $WORKDIR/.env (mode 600) with QIANLIMA_TOKEN and QIANLIMA_OPENID, or export them on the host."
