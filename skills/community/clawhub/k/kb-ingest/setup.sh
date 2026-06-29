#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python3 -m pip install -r requirements.txt
python3 scripts/run_task.py --help >/dev/null
echo "kb_ingest skill is ready"
