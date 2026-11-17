#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
test -f SKILL.md
test -f scripts/run_task.py
python3 -m py_compile scripts/*.py
git --version >/dev/null
echo "gitea_repo_ingest skill is ready"
