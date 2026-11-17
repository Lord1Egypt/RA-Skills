#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FETCH_SCRIPT="$SCRIPT_DIR/../scripts/fetch-issues.sh"

TMPDIR="$(mktemp -d)"
cleanup() {
  rm -rf "$TMPDIR"
}
trap cleanup EXIT

MOCKBIN="$TMPDIR/mockbin"
mkdir -p "$MOCKBIN"

cat > "$MOCKBIN/gh" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

if [[ "${1:-}" == "--version" ]]; then
  echo "gh version 9.9.9"
  exit 0
fi

if [[ "${1:-}" == "issue" && "${2:-}" == "list" ]]; then
  cat <<JSON
[
  {
    "number": 1,
    "title": "Crash in parser",
    "body": "Repro: run X then Y.",
    "labels": [],
    "assignees": [],
    "author": {"login": "alice"},
    "createdAt": "2026-01-01T00:00:00Z",
    "updatedAt": "2026-01-02T00:00:00Z",
    "comments": 3,
    "url": "https://github.com/demo/repo/issues/1"
  },
  {
    "number": 2,
    "title": "Add docs",
    "body": "Improve docs for setup",
    "labels": [],
    "assignees": [],
    "author": {"login": "bob"},
    "createdAt": "2026-01-03T00:00:00Z",
    "updatedAt": "2026-01-04T00:00:00Z",
    "comments": 0,
    "url": "https://github.com/demo/repo/issues/2"
  }
]
JSON
  exit 0
fi

if [[ "${1:-}" == "api" && "${2:-}" == "graphql" ]]; then
  cat <<JSON
{
  "data": {
    "repository": {
      "issue_1": {
        "number": 1,
        "closedByPullRequestsReferences": {
          "pageInfo": { "hasNextPage": true },
          "nodes": [
            { "number": 99, "title": "Fix parser crash", "url": "https://github.com/demo/repo/pull/99", "state": "OPEN" }
          ]
        },
        "timelineItems": {
          "pageInfo": { "hasPreviousPage": false },
          "nodes": []
        }
      },
      "issue_2": {
        "number": 2,
        "closedByPullRequestsReferences": {
          "pageInfo": { "hasNextPage": false },
          "nodes": []
        },
        "timelineItems": {
          "pageInfo": { "hasPreviousPage": false },
          "nodes": []
        }
      }
    }
  }
}
JSON
  exit 0
fi

if [[ "${1:-}" == "pr" && "${2:-}" == "list" ]]; then
  echo '[]'
  exit 0
fi

echo "unexpected gh args: $*" >&2
exit 1
EOF
chmod +x "$MOCKBIN/gh"

assert_eq() {
  local expected="$1"
  local actual="$2"
  local context="$3"
  if [[ "$expected" != "$actual" ]]; then
    echo "FAIL: $context"
    echo "  expected: $expected"
    echo "  actual:   $actual"
    exit 1
  fi
}

assert_contains() {
  local haystack="$1"
  local needle="$2"
  local context="$3"
  if [[ "$haystack" != *"$needle"* ]]; then
    echo "FAIL: $context"
    echo "  missing: $needle"
    exit 1
  fi
}

export PATH="$MOCKBIN:$PATH"

# 1) Missing value for value-based option returns structured error.
set +e
OUT="$(bash "$FETCH_SCRIPT" demo/repo --limit 2>&1)"
EC=$?
set -e
assert_eq "1" "$EC" "missing option value should fail"
assert_contains "$OUT" '"error":"Missing value for --limit"' "missing value error should be JSON"

# 2) Issue-side links exclude open linked PRs and signal partial coverage.
HISTORY_DIR="$TMPDIR/history with spaces"
OUT="$(bash "$FETCH_SCRIPT" demo/repo --limit 2 --history-dir "$HISTORY_DIR" --retain 20)"
RUN_ID="$(echo "$OUT" | jq -r '.runId')"
WORKDIR="$(echo "$OUT" | jq -r '.workdir')"
MODE="$(jq -r '.linkingMode' "$WORKDIR/manifest.json")"
assert_eq "partial_github_link" "$MODE" "linkingMode should signal partial coverage"
assert_eq "1" "$(jq '.stats.excludedWithPRs' "$WORKDIR/manifest.json")" "linked issue should be excluded"
assert_eq "99" "$(jq '.excluded[0].prNumber' "$WORKDIR/manifest.json")" "excluded issue should name its open PR"
if ! grep -q "linking data may be partial" "$WORKDIR/errors.log"; then
  echo "FAIL: expected partial-link warning in errors.log"
  exit 1
fi

# 3) Resume must reject repo mismatch.
set +e
OUT="$(bash "$FETCH_SCRIPT" other/repo --resume "$RUN_ID" --history-dir "$HISTORY_DIR" 2>&1)"
EC=$?
set -e
assert_eq "1" "$EC" "--resume repo mismatch should fail"
assert_contains "$OUT" "--resume repo mismatch" "mismatch error should explain conflict"

# 4) --retain 0 keeps only current run.
bash "$FETCH_SCRIPT" demo/repo --limit 1 --include-with-prs --history-dir "$HISTORY_DIR" --retain 0 >/dev/null
sleep 1
bash "$FETCH_SCRIPT" demo/repo --limit 1 --include-with-prs --history-dir "$HISTORY_DIR" --retain 0 >/dev/null
COUNT="$(find "$HISTORY_DIR" -mindepth 1 -maxdepth 1 -type d | wc -l | tr -d ' ')"
assert_eq "1" "$COUNT" "--retain 0 should keep only one run directory"

# 5) errors.log should be reset each execution.
WORKDIR="$TMPDIR/shared-workdir"
bash "$FETCH_SCRIPT" demo/repo --limit 2 --workdir "$WORKDIR" --history-dir "$HISTORY_DIR" --retain 20 >/dev/null
if ! grep -q "linking data may be partial" "$WORKDIR/errors.log"; then
  echo "FAIL: expected warning in first run"
  exit 1
fi
bash "$FETCH_SCRIPT" demo/repo --limit 2 --include-with-prs --workdir "$WORKDIR" --history-dir "$HISTORY_DIR" --retain 20 >/dev/null
if grep -q "linking data may be partial" "$WORKDIR/errors.log"; then
  echo "FAIL: stale warning leaked into second run"
  exit 1
fi

# 6) --diff-from + --resume are mutually exclusive.
set +e
OUT="$(bash "$FETCH_SCRIPT" demo/repo --diff-from latest --resume somerun --history-dir "$HISTORY_DIR" 2>&1)"
EC=$?
set -e
assert_eq "1" "$EC" "--diff-from + --resume should fail"
assert_contains "$OUT" '"error":"--diff-from and --resume are mutually exclusive"' "mutual exclusion error"

# 7) --diff-from with missing merged.json falls back to full analysis.
BASELINE_DIR="$TMPDIR/baseline-empty"
mkdir -p "$BASELINE_DIR/results"
echo '[]' > "$BASELINE_DIR/issues.json"
: > "$BASELINE_DIR/results/merged.json"  # truly empty file (0 bytes, not valid baseline)
OUT="$(bash "$FETCH_SCRIPT" demo/repo --limit 2 --include-with-prs --diff-from "$BASELINE_DIR" --history-dir "$HISTORY_DIR" --retain 20)"
DIFF_MODE="$(echo "$OUT" | jq -r '.diffMode')"
assert_eq "false" "$DIFF_MODE" "--diff-from with empty merged.json should fallback (diffMode=false)"

# 8) --diff-from with valid baseline produces diff classification.
# Create a valid baseline with scores for issue #1 (unchanged) and issue #3 (removed)
BASELINE_DIR2="$TMPDIR/baseline-valid"
mkdir -p "$BASELINE_DIR2/results"
cat > "$BASELINE_DIR2/issues.json" <<'ISSUES'
[
  {"number": 1, "updatedAt": "2026-01-02T00:00:00Z"},
  {"number": 3, "updatedAt": "2026-01-05T00:00:00Z"}
]
ISSUES
cat > "$BASELINE_DIR2/results/merged.json" <<'SCORES'
[
  {"number": 1, "title": "Crash in parser", "adjustedScore": 2.5},
  {"number": 3, "title": "Old removed issue", "adjustedScore": 1.0}
]
SCORES
OUT="$(bash "$FETCH_SCRIPT" demo/repo --limit 2 --include-with-prs --diff-from "$BASELINE_DIR2" --history-dir "$HISTORY_DIR" --retain 20)"
DIFF_WD="$(echo "$OUT" | jq -r '.workdir')"
DIFF_MODE="$(echo "$OUT" | jq -r '.diffMode')"
assert_eq "true" "$DIFF_MODE" "--diff-from with valid baseline should enable diffMode"

# Issue 1: same updatedAt + has score → unchanged (cached)
CACHED="$(echo "$OUT" | jq '.diffCached')"
assert_eq "1" "$CACHED" "issue #1 should be cached (unchanged)"

# Issue 2: not in baseline → new
NEW="$(echo "$OUT" | jq '.diffNew')"
assert_eq "1" "$NEW" "issue #2 should be new"

# Issue 3: in baseline but not in current → removed
REMOVED="$(echo "$OUT" | jq '.diffRemoved')"
assert_eq "1" "$REMOVED" "issue #3 should be removed"

# cached-scores.json should contain issue #1's prior score
CACHED_COUNT="$(jq 'length' "$DIFF_WD/cached-scores.json")"
assert_eq "1" "$CACHED_COUNT" "cached-scores.json should have 1 entry"
CACHED_NUM="$(jq '.[0].number' "$DIFF_WD/cached-scores.json")"
assert_eq "1" "$CACHED_NUM" "cached score should be for issue #1"

# delta.json should contain only issue #2 (new)
DELTA_COUNT="$(jq 'length' "$DIFF_WD/delta.json")"
assert_eq "1" "$DELTA_COUNT" "delta.json should have 1 entry"
DELTA_NUM="$(jq '.[0].number' "$DIFF_WD/delta.json")"
assert_eq "2" "$DELTA_NUM" "delta should contain issue #2"

# remaining should reflect delta count (1), not total filtered (2)
REMAINING="$(echo "$OUT" | jq '.remaining')"
assert_eq "1" "$REMAINING" "remaining should be delta count in diff mode"

# 9) --diff-from classifies issues with changed updatedAt as "modified".
BASELINE_DIR3="$TMPDIR/baseline-modified"
mkdir -p "$BASELINE_DIR3/results"
cat > "$BASELINE_DIR3/issues.json" <<'ISSUES'
[
  {"number": 1, "updatedAt": "2025-12-31T00:00:00Z"},
  {"number": 2, "updatedAt": "2026-01-04T00:00:00Z"}
]
ISSUES
cat > "$BASELINE_DIR3/results/merged.json" <<'SCORES'
[
  {"number": 1, "title": "Crash in parser", "adjustedScore": 2.5},
  {"number": 2, "title": "Add docs", "adjustedScore": 1.0}
]
SCORES
OUT="$(bash "$FETCH_SCRIPT" demo/repo --limit 2 --include-with-prs --diff-from "$BASELINE_DIR3" --history-dir "$HISTORY_DIR" --retain 20)"
# Issue 1: updatedAt changed (2025-12-31 vs mock's 2026-01-02) → modified
# Issue 2: updatedAt same (2026-01-04) → unchanged
MODIFIED="$(echo "$OUT" | jq '.diffModified')"
assert_eq "1" "$MODIFIED" "issue #1 should be modified (updatedAt changed)"
CACHED="$(echo "$OUT" | jq '.diffCached')"
assert_eq "1" "$CACHED" "issue #2 should be cached (updatedAt same)"

# 10) --diff-from when all issues unchanged → remaining=0, delta empty.
BASELINE_DIR4="$TMPDIR/baseline-allcached"
mkdir -p "$BASELINE_DIR4/results"
cat > "$BASELINE_DIR4/issues.json" <<'ISSUES'
[
  {"number": 1, "updatedAt": "2026-01-02T00:00:00Z"},
  {"number": 2, "updatedAt": "2026-01-04T00:00:00Z"}
]
ISSUES
cat > "$BASELINE_DIR4/results/merged.json" <<'SCORES'
[
  {"number": 1, "title": "Crash in parser", "adjustedScore": 2.5},
  {"number": 2, "title": "Add docs", "adjustedScore": 1.0}
]
SCORES
OUT="$(bash "$FETCH_SCRIPT" demo/repo --limit 2 --include-with-prs --diff-from "$BASELINE_DIR4" --history-dir "$HISTORY_DIR" --retain 20)"
ALL_WD="$(echo "$OUT" | jq -r '.workdir')"
REMAINING="$(echo "$OUT" | jq '.remaining')"
assert_eq "0" "$REMAINING" "all-unchanged should have remaining=0"
CACHED="$(echo "$OUT" | jq '.diffCached')"
assert_eq "2" "$CACHED" "all-unchanged should cache both issues"
DELTA_LEN="$(jq 'length' "$ALL_WD/delta.json")"
assert_eq "0" "$DELTA_LEN" "delta.json should be empty when all cached"
CACHED_LEN="$(jq 'length' "$ALL_WD/cached-scores.json")"
assert_eq "2" "$CACHED_LEN" "cached-scores.json should have both entries"
BATCHES="$(echo "$OUT" | jq '.batches')"
assert_eq "0" "$BATCHES" "all-unchanged should produce 0 batches"

echo "PASS: fetch-issues regression checks"
