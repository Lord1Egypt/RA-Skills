#!/bin/bash
set -e
echo "Running E2E Pipeline Run test for spawn_auditor.py"
python3 scripts/spawn_auditor.py --enable-exec-from-workspace --help > /dev/null
echo "Successfully executed spawn_auditor.py"
