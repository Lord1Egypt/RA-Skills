#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
test -f SKILL.md
test -f scripts/run_task.py
python3 -m pip install -r requirements.txt
python3 -m py_compile scripts/*.py
echo "local_document_ingest skill is ready"