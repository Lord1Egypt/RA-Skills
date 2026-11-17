#!/usr/bin/env bash
# Guard against pattern-count drift. The count is a derived fact, so it lives in
# exactly one user-facing place — the README "**NN pattern categories**" bullet —
# and this script asserts it matches SKILL.md's detection catalog. Run in CI so
# adding a pattern without bumping the README is a red check, not silent rot.
#
# Adapted from avoid-ai-writing's check-pattern-count.sh. Counts the `###`
# entries under "## What to remove or fix" / "## 该删除或修改的" (bilingual SKILL),
# minus writer-side tests that have no detectable form.
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
skill="$repo_root/SKILL.md"
readme="$repo_root/README.md"

# Detection categories = `###` entries under the bilingual detection section
# header, minus writer-side judgment tests (no detectable form).
detection_count="$(awk '
  /^## (What to remove or fix|该删除或修改的)/ { inside = 1; next }
  /^## / { inside = 0 }
  inside && /^### / {
    if ($0 ~ /\(structure test\)|\(content test\)|\(结构测试\)|\(内容测试\)/) next
    if ($0 ~ /^### (When to rewrite from scratch|何时重写而非修补)/) next
    n++
  }
  END { print n + 0 }
' "$skill")"

# The single user-facing count literal.
readme_count="$(sed -n 's/.*\*\*\([0-9][0-9]*\) pattern categories\*\*.*/\1/p' "$readme" | head -n1)"

if [ -z "$readme_count" ]; then
  echo "could not find the '**NN pattern categories**' bullet in README.md" >&2
  exit 1
fi

if [ "$detection_count" != "$readme_count" ]; then
  echo "pattern-count drift: SKILL.md has $detection_count detection categories, README says $readme_count" >&2
  echo "Update the '**NN pattern categories**' bullet in README.md to $detection_count (or fix SKILL.md)." >&2
  exit 1
fi

echo "pattern count in sync: $detection_count"
