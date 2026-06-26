#!/usr/bin/env bash
# Run all offline regression tests for openclaw-consensus.
#
# These are deterministic, do not invoke `openclaw`, and do not call any
# provider — they cost nothing to run.
#
# Optional live checks live elsewhere and must be invoked explicitly; see
# docs/COMMANDS.md.

set -euo pipefail

repo_root="$(cd "$(dirname "$0")/.." && pwd)"
cd "$repo_root"

failed=0
for f in validation/tests/cli-helpers.test.mjs \
         validation/tests/cli-extended.test.mjs \
         validation/tests/cli-cli.test.mjs; do
  echo "==> $f"
  if ! node "$f"; then
    failed=$((failed + 1))
  fi
done

if [ "$failed" -ne 0 ]; then
  echo "FAIL: $failed test file(s) reported failures."
  exit 1
fi
echo "All offline regression tests passed."
