#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
if [ "$(uname -s)" != Linux ] || [ "$(id -u)" = 0 ]; then
  echo 'Full smoke test requires a non-root Linux user and working Chrome sandbox.' >&2
  exit 1
fi
for file in scripts/*.sh tests/smoke_test.sh; do bash -n "$file"; done
python3 -m unittest discover -s tests -p 'test_*.py'
npm test
npm run test:browser
python3 tests/linux_integration.py
