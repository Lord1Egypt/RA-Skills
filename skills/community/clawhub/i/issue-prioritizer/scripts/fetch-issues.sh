#!/usr/bin/env bash
set -euo pipefail

# fetch-issues.sh — Fetch GitHub issues, detect linked PRs, split into batches.
# Keeps raw data out of the orchestrating agent's context window.
#
# Usage: fetch-issues.sh <owner/repo> [options]
#
# Options:
#   --limit N              Issues to fetch (default: 30)
#   --batch-size N         Issues per batch (default: 20)
#   --max-concurrency N    Max parallel agents per wave (default: 30)
#   --truncate N           Body truncation in chars (default: 500)
#   --full-body            Alias for --truncate 2000
#   --topic <keywords>     Search issues by topic (in:title,body)
#   --search <query>       Raw GitHub search query
#   --label <name>         Filter by label
#   --include-with-prs     Don't filter out issues with existing PRs
#   --workdir <path>       Output directory (overrides history-dir default)
#   --history-dir <path>   Runs history root (default: $XDG_STATE_HOME/issue-prioritizer/runs)
#   --retain N             Keep only N most recent runs in history-dir (default: 20, 0 = keep only current run)
#   --resume <run>         Resume from existing run dir or run id (folder name)
#   --diff-from <ref>      Incremental mode: reuse cached scores for unchanged issues
#                          <ref> = full path, run_id in history-dir, or "latest"
#
# Output files (in workdir):
#   manifest.json    Summary for the orchestrating agent (small, safe to read)
#   summary.json     Short run summary + key paths
#   issues.json      All fetched issues (raw, full bodies)
#   prs.json         Open PRs linked from the fetched issues (when PR filtering)
#   excluded.json    Issues excluded (have linked PRs, with detection method)
#   batches/batch-N.json  Issue batches for analysis agents (bodies truncated)
#   results/merged.json   Placeholder for merged analysis results
#   results/report.md     Placeholder report for this run
#
# stdout: Single-line JSON summary (~200 tokens, safe for agent context)

# ── Argument parsing ──────────────────────────────────────────────────────────

REPO=""
LIMIT=30
BATCH_SIZE=20
MAX_CONCURRENCY=30
TRUNCATE=500
TOPIC=""
SEARCH=""
LABEL=""
INCLUDE_WITH_PRS=false
WORKDIR=""
HISTORY_DIR="${XDG_STATE_HOME:-$HOME/.local/state}/issue-prioritizer/runs"
RETAIN=20
RESUME=""
DIFF_FROM=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --limit)
      if [[ $# -lt 2 || "$2" == --* ]]; then
        echo '{"error":"Missing value for --limit"}' >&2
        exit 1
      fi
      LIMIT="$2"; shift 2 ;;
    --batch-size)
      if [[ $# -lt 2 || "$2" == --* ]]; then
        echo '{"error":"Missing value for --batch-size"}' >&2
        exit 1
      fi
      BATCH_SIZE="$2"; shift 2 ;;
    --max-concurrency)
      if [[ $# -lt 2 || "$2" == --* ]]; then
        echo '{"error":"Missing value for --max-concurrency"}' >&2
        exit 1
      fi
      MAX_CONCURRENCY="$2"; shift 2 ;;
    --truncate)
      if [[ $# -lt 2 || "$2" == --* ]]; then
        echo '{"error":"Missing value for --truncate"}' >&2
        exit 1
      fi
      TRUNCATE="$2"; shift 2 ;;
    --full-body)        TRUNCATE=2000;         shift ;;
    --topic)
      if [[ $# -lt 2 || "$2" == --* ]]; then
        echo '{"error":"Missing value for --topic"}' >&2
        exit 1
      fi
      TOPIC="$2"; shift 2 ;;
    --search)
      if [[ $# -lt 2 || "$2" == --* ]]; then
        echo '{"error":"Missing value for --search"}' >&2
        exit 1
      fi
      SEARCH="$2"; shift 2 ;;
    --label)
      if [[ $# -lt 2 || "$2" == --* ]]; then
        echo '{"error":"Missing value for --label"}' >&2
        exit 1
      fi
      LABEL="$2"; shift 2 ;;
    --include-with-prs) INCLUDE_WITH_PRS=true; shift ;;
    --workdir)
      if [[ $# -lt 2 || "$2" == --* ]]; then
        echo '{"error":"Missing value for --workdir"}' >&2
        exit 1
      fi
      WORKDIR="$2"; shift 2 ;;
    --history-dir)
      if [[ $# -lt 2 || "$2" == --* ]]; then
        echo '{"error":"Missing value for --history-dir"}' >&2
        exit 1
      fi
      HISTORY_DIR="$2"; shift 2 ;;
    --retain)
      if [[ $# -lt 2 || "$2" == --* ]]; then
        echo '{"error":"Missing value for --retain"}' >&2
        exit 1
      fi
      RETAIN="$2"; shift 2 ;;
    --resume)
      if [[ $# -lt 2 || "$2" == --* ]]; then
        echo '{"error":"Missing value for --resume"}' >&2
        exit 1
      fi
      RESUME="$2"; shift 2 ;;
    --diff-from)
      if [[ $# -lt 2 || "$2" == --* ]]; then
        echo '{"error":"Missing value for --diff-from"}' >&2
        exit 1
      fi
      DIFF_FROM="$2"; shift 2 ;;
    --help|-h)
      sed -n '3,/^$/{ s/^# //; s/^#//; p }' "$0"
      exit 0 ;;
    --*)
      echo "{\"error\":\"Unknown option: $1\"}" >&2
      exit 1 ;;
    *)
      REPO="$1"; shift ;;
  esac
done

# ── Validation ────────────────────────────────────────────────────────────────

if [[ -z "$REPO" && -z "$RESUME" ]]; then
  echo '{"error":"Usage: fetch-issues.sh <owner/repo> [options] OR --resume <run_id|path> [options]"}' >&2
  exit 1
fi

if [[ -n "$REPO" ]] && ! [[ "$REPO" =~ ^[A-Za-z0-9._-]+/[A-Za-z0-9._-]+$ ]]; then
  echo "{\"error\":\"Invalid repo format: $REPO. Expected owner/repo\"}" >&2
  exit 1
fi

for cmd in gh jq; do
  if ! command -v "$cmd" &>/dev/null; then
    echo "{\"error\":\"$cmd not found\"}" >&2
    exit 1
  fi
done

# Validate numeric arguments
for _var in LIMIT BATCH_SIZE MAX_CONCURRENCY TRUNCATE; do
  _val="${!_var}"
  if ! [[ "$_val" =~ ^[0-9]+$ ]] || [[ "$_val" -eq 0 ]]; then
    echo "{\"error\":\"--${_var,,} must be a positive integer, got: $_val\"}" >&2
    exit 1
  fi
done
if ! [[ "$RETAIN" =~ ^[0-9]+$ ]]; then
  echo "{\"error\":\"--retain must be a non-negative integer, got: $RETAIN\"}" >&2
  exit 1
fi
unset _var _val

if [[ -n "$DIFF_FROM" && -n "$RESUME" ]]; then
  echo '{"error":"--diff-from and --resume are mutually exclusive"}' >&2
  exit 1
fi

OWNER="${REPO%%/*}"
NAME="${REPO##*/}"
GH_VERSION=$(gh --version | head -1 | grep -oP '\d+\.\d+\.\d+' || echo "unknown")

# ── Setup workdir ─────────────────────────────────────────────────────────────

mkdir -p "$HISTORY_DIR"
RESUME_MODE=false
if [[ -n "$RESUME" ]]; then
  RESUME_MODE=true
  if [[ -d "$RESUME" ]]; then
    WORKDIR="$RESUME"
  elif [[ -d "$HISTORY_DIR/$RESUME" ]]; then
    WORKDIR="$HISTORY_DIR/$RESUME"
  else
    echo "{\"error\":\"run not found for --resume: $RESUME\"}" >&2
    exit 1
  fi
else
  if [[ -z "$WORKDIR" ]]; then
    RUN_STAMP=$(date -u +"%Y%m%d-%H%M%S")
    WORKDIR="$HISTORY_DIR/${RUN_STAMP}_${OWNER}_${NAME}"
  fi
fi
mkdir -p "$WORKDIR" "$WORKDIR/batches" "$WORKDIR/results"
: > "$WORKDIR/errors.log"

MANIFEST_REPO=""
if [[ -f "$WORKDIR/manifest.json" ]]; then
  MANIFEST_REPO="$(jq -r '.repo // empty' "$WORKDIR/manifest.json")"
fi

if [[ "$RESUME_MODE" == "true" && -n "$REPO" && -n "$MANIFEST_REPO" && "$REPO" != "$MANIFEST_REPO" ]]; then
  echo "{\"error\":\"--resume repo mismatch: requested $REPO but run contains $MANIFEST_REPO\"}" >&2
  exit 1
fi
if [[ -z "$REPO" && -n "$MANIFEST_REPO" ]]; then
  REPO="$MANIFEST_REPO"
fi
if [[ -z "$REPO" ]]; then
  echo '{"error":"repo not provided and could not infer from manifest in --resume mode"}' >&2
  exit 1
fi
if ! [[ "$REPO" =~ ^[A-Za-z0-9._-]+/[A-Za-z0-9._-]+$ ]]; then
  echo "{\"error\":\"Invalid repo format: $REPO. Expected owner/repo\"}" >&2
  exit 1
fi
OWNER="${REPO%%/*}"
NAME="${REPO##*/}"

GENERATED_AT=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
RUN_ID="$(basename "$WORKDIR")"

# ── Resolve --diff-from baseline ─────────────────────────────────────────────

DIFF_MODE=false
DIFF_FROM_DIR=""
if [[ -n "$DIFF_FROM" ]]; then
  # Resolve path: full path, run_id in history-dir, or "latest" symlink
  if [[ "$DIFF_FROM" == "latest" ]]; then
    if [[ -L "$HISTORY_DIR/latest" ]]; then
      DIFF_FROM_DIR="$(readlink -f "$HISTORY_DIR/latest")"
    fi
  elif [[ -d "$DIFF_FROM" ]]; then
    DIFF_FROM_DIR="$DIFF_FROM"
  elif [[ -d "$HISTORY_DIR/$DIFF_FROM" ]]; then
    DIFF_FROM_DIR="$HISTORY_DIR/$DIFF_FROM"
  fi

  # Validate baseline has required files
  if [[ -z "$DIFF_FROM_DIR" ]]; then
    echo "warning: --diff-from target not found: $DIFF_FROM; falling back to full analysis" >> "$WORKDIR/errors.log"
  elif [[ ! -s "$DIFF_FROM_DIR/results/merged.json" ]] || ! jq -e 'type == "array" and length > 0' "$DIFF_FROM_DIR/results/merged.json" &>/dev/null; then
    echo "warning: --diff-from baseline has no valid results/merged.json; falling back to full analysis" >> "$WORKDIR/errors.log"
    DIFF_FROM_DIR=""
  elif [[ ! -f "$DIFF_FROM_DIR/issues.json" ]]; then
    echo "warning: --diff-from baseline has no issues.json; falling back to full analysis" >> "$WORKDIR/errors.log"
    DIFF_FROM_DIR=""
  fi

  # Validate baseline belongs to the same repo
  if [[ -n "$DIFF_FROM_DIR" && -f "$DIFF_FROM_DIR/manifest.json" ]]; then
    BASELINE_REPO="$(jq -r '.repo // empty' "$DIFF_FROM_DIR/manifest.json")"
    if [[ -n "$BASELINE_REPO" && "$BASELINE_REPO" != "$REPO" ]]; then
      echo "warning: --diff-from baseline is for $BASELINE_REPO, not $REPO; falling back to full analysis" >> "$WORKDIR/errors.log"
      DIFF_FROM_DIR=""
    fi
  fi

  # Prevent diffing against own workdir
  if [[ -n "$DIFF_FROM_DIR" ]] && [[ "$(readlink -f "$DIFF_FROM_DIR")" == "$(readlink -f "$WORKDIR")" ]]; then
    echo "warning: --diff-from resolves to current workdir; falling back to full analysis" >> "$WORKDIR/errors.log"
    DIFF_FROM_DIR=""
  fi

  if [[ -n "$DIFF_FROM_DIR" ]]; then
    DIFF_MODE=true
  fi
fi

# Determine source type and filter description
SOURCE="list"
FILTER_DESC=""
LINKING_MODE="disabled"
if [[ "$RESUME_MODE" == "true" ]]; then
  if [[ -f "$WORKDIR/manifest.json" ]]; then
    SOURCE="$(jq -r '.source // "resume"' "$WORKDIR/manifest.json")"
    FILTER_DESC="$(jq -r '.filter // "resume"' "$WORKDIR/manifest.json")"
    LINKING_MODE="$(jq -r '.linkingMode // "resume"' "$WORKDIR/manifest.json")"
  else
    SOURCE="resume"
    FILTER_DESC="resume:$RUN_ID"
    LINKING_MODE="resume"
  fi
else
  if [[ -n "$SEARCH" ]]; then
    SOURCE="search"
    FILTER_DESC="search:$SEARCH"
  elif [[ -n "$TOPIC" ]]; then
    SOURCE="search"
    FILTER_DESC="topic:$TOPIC"
  fi
  [[ -n "$LABEL" ]] && FILTER_DESC="${FILTER_DESC:+$FILTER_DESC }label:$LABEL"
  FILTER_DESC="${FILTER_DESC:-latest}"
  if [[ "$INCLUDE_WITH_PRS" == "false" ]]; then
    LINKING_MODE="github_link"
  fi
fi

# ── Step 1: Fetch issues ─────────────────────────────────────────────────────

if [[ "$RESUME_MODE" == "true" ]]; then
  if [[ ! -f "$WORKDIR/issues.json" ]]; then
    echo "{\"error\":\"cannot resume: missing $WORKDIR/issues.json\"}" >&2
    exit 1
  fi
  if [[ ! -f "$WORKDIR/filtered.json" ]]; then
    cp "$WORKDIR/issues.json" "$WORKDIR/filtered.json"
  fi
  if [[ ! -f "$WORKDIR/excluded.json" ]]; then
    echo '[]' > "$WORKDIR/excluded.json"
  fi
else
  GH_ISSUE_ARGS=(issue list --repo "$REPO" --state open --limit "$LIMIT"
    --json "number,title,body,labels,assignees,author,createdAt,updatedAt,comments,url")

  if [[ -n "$SEARCH" ]]; then
    GH_ISSUE_ARGS+=(--search "$SEARCH")
  elif [[ -n "$TOPIC" ]]; then
    GH_ISSUE_ARGS+=(--search "$TOPIC in:title,body")
  fi

  if [[ -n "$LABEL" ]]; then
    GH_ISSUE_ARGS+=(--label "$LABEL")
  fi

  if ! gh "${GH_ISSUE_ARGS[@]}" > "$WORKDIR/issues.json" 2>>"$WORKDIR/errors.log"; then
    ERR=$(cat "$WORKDIR/errors.log")
    echo "{\"error\":\"gh issue list failed\",\"detail\":$(echo "$ERR" | jq -Rs '.')}" >&2
    exit 1
  fi
fi

TOTAL_ISSUES=$(jq 'length' "$WORKDIR/issues.json")

# Warn if search may have hit GitHub's 1000-result ceiling
if [[ "$SOURCE" == "search" && "$TOTAL_ISSUES" -eq 1000 ]]; then
  echo "warning: search returned exactly 1000 results (GitHub ceiling). Consider slicing by date range." >> "$WORKDIR/errors.log"
fi

# ── Step 2: Linked PR detection ──────────────────────────────────────────────
# Primary:  GitHub's issue-side PR links (via GraphQL) — high fidelity
# Fallback: Regex for fixes/closes/resolves #N in title+body

EXCLUDED_COUNT=0

if [[ "$TOTAL_ISSUES" -eq 0 ]]; then
  echo '[]' > "$WORKDIR/filtered.json"
  echo '[]' > "$WORKDIR/excluded.json"
  echo '[]' > "$WORKDIR/prs.json"
  EXCLUDED_COUNT=0
elif [[ "$RESUME_MODE" == "true" ]]; then
  EXCLUDED_COUNT=$(jq 'length' "$WORKDIR/excluded.json")
elif [[ "$INCLUDE_WITH_PRS" == "false" ]]; then
  # Query only the fetched issues. Repository-wide PR pagination is both expensive and
  # incomplete on repositories with thousands of open PRs.
  PR_FETCH_OK=true
  GQL_ISSUE_BATCH_SIZE="${IP_GQL_ISSUE_BATCH_SIZE:-25}"
  if ! [[ "$GQL_ISSUE_BATCH_SIZE" =~ ^[0-9]+$ ]] || [[ "$GQL_ISSUE_BATCH_SIZE" -eq 0 ]]; then
    echo "warning: invalid IP_GQL_ISSUE_BATCH_SIZE=$GQL_ISSUE_BATCH_SIZE; defaulting to 25" >> "$WORKDIR/errors.log"
    GQL_ISSUE_BATCH_SIZE=25
  fi
  GQL_TRUNCATED=false
  echo '[]' > "$WORKDIR/issue-links-raw.json"
  mapfile -t ISSUE_NUMBERS < <(jq -r '.[].number' "$WORKDIR/issues.json")

  for ((offset = 0; offset < ${#ISSUE_NUMBERS[@]}; offset += GQL_ISSUE_BATCH_SIZE)); do
    ISSUE_FIELDS=""
    for number in "${ISSUE_NUMBERS[@]:offset:GQL_ISSUE_BATCH_SIZE}"; do
      ISSUE_FIELDS+="
    issue_$number: issue(number: $number) {
      number
      closedByPullRequestsReferences(first: 50) {
        pageInfo { hasNextPage }
        nodes { number title url state }
      }
      timelineItems(last: 50, itemTypes: [CROSS_REFERENCED_EVENT]) {
        pageInfo { hasPreviousPage }
        nodes {
          ... on CrossReferencedEvent {
            source {
              __typename
              ... on PullRequest { number title url state }
            }
          }
        }
      }
    }"
    done

    QUERY=$(cat <<GRAPHQL
query(\$owner: String!, \$name: String!) {
  repository(owner: \$owner, name: \$name) {
$ISSUE_FIELDS
  }
}
GRAPHQL
)

    GH_GQL_ARGS=(api graphql -f query="$QUERY" -f owner="$OWNER" -f name="$NAME")
    if ! RESULT=$(gh "${GH_GQL_ARGS[@]}" 2>>"$WORKDIR/errors.log"); then
      echo "warning: GraphQL issue-link fetch failed, falling back to REST" >> "$WORKDIR/errors.log"
      PR_FETCH_OK=false
      break
    fi

    LINKS=$(echo "$RESULT" | jq '
      [.data.repository | to_entries[] | .value as $issue |
        select($issue != null) |
        (
          ($issue.closedByPullRequestsReferences.nodes // []) +
          [($issue.timelineItems.nodes // [])[] | .source | select(.__typename == "PullRequest")]
        )[] |
        select(.state == "OPEN") |
        {
          issueNumber: $issue.number,
          prNumber: .number,
          prTitle: .title,
          prUrl: .url
        }
      ] | unique_by([.issueNumber, .prNumber])
    ')
    jq -s '.[0] + .[1]' "$WORKDIR/issue-links-raw.json" <(echo "$LINKS") > "$WORKDIR/issue-links-tmp.json"
    mv "$WORKDIR/issue-links-tmp.json" "$WORKDIR/issue-links-raw.json"

    if echo "$RESULT" | jq -e '
      [.data.repository | to_entries[].value | select(. != null) |
        .closedByPullRequestsReferences.pageInfo.hasNextPage,
        .timelineItems.pageInfo.hasPreviousPage] | any(. == true)
    ' >/dev/null; then
      GQL_TRUNCATED=true
    fi
  done

  if [[ "$PR_FETCH_OK" == "true" ]]; then
    if [[ "$GQL_TRUNCATED" == "true" ]]; then
      LINKING_MODE="partial_github_link"
      echo "warning: one or more issues have over 50 PR references; linking data may be partial" >> "$WORKDIR/errors.log"
    else
      LINKING_MODE="github_link"
    fi
    jq '
      group_by(.prNumber) |
      map({
        number: .[0].prNumber,
        title: .[0].prTitle,
        url: .[0].prUrl,
        body: "",
        closingIssues: (map(.issueNumber) | unique)
      })
    ' "$WORKDIR/issue-links-raw.json" > "$WORKDIR/prs.json"
  else
    if gh pr list --repo "$REPO" --state open --limit 500 \
      --json "number,title,body,url" > "$WORKDIR/prs-rest.json" 2>>"$WORKDIR/errors.log"; then
      LINKING_MODE="regex_only"
      echo "warning: using regex-only PR linking (GraphQL issue links unavailable)" >> "$WORKDIR/errors.log"
      jq '[.[] | {number, title, url, body, closingIssues: []}]' \
        "$WORKDIR/prs-rest.json" > "$WORKDIR/prs.json"
    else
      LINKING_MODE="skipped"
      echo '[]' > "$WORKDIR/prs.json"
      echo '[]' > "$WORKDIR/excluded.json"
      echo "warning: PR fetch failed entirely, skipping PR filter" >> "$WORKDIR/errors.log"
      cp "$WORKDIR/issues.json" "$WORKDIR/filtered.json"
    fi
  fi

  if [[ "$LINKING_MODE" != "skipped" ]]; then
    # 2b. Build linked PR map
    # Primary: closingIssuesReferences (GitHub's own link data)
    # Fallback: regex fixes/closes/resolves #N on title+body
    jq '
      # Primary: GitHub closing references
      [.[] | . as $pr |
        (.closingIssues // [])[] |
        {
          issueNumber: .,
          prNumber: $pr.number,
          prTitle: $pr.title,
          prUrl: $pr.url,
          method: "github_link"
        }
      ] as $github_links |

      # Fallback: regex on title+body for issues not caught by GitHub links
      ($github_links | [.[].issueNumber] | unique) as $already_linked |
      [.[] | . as $pr |
        (($pr.title // "") + " " + ($pr.body // "")) |
        [match("(?i)(?:fix(?:es|ed)?|close[sd]?|resolve[sd]?)\\s*#(\\d+)"; "g")
          | .captures[0].string | tonumber] | unique[] |
        select(. as $n | $already_linked | index($n) | not) |
        {
          issueNumber: .,
          prNumber: $pr.number,
          prTitle: $pr.title,
          prUrl: $pr.url,
          method: "regex_keyword"
        }
      ] as $regex_links |

      # Dedup: prefer github_link over regex_keyword per issue
      ($github_links + $regex_links) | group_by(.issueNumber) |
        map(sort_by(if .method == "github_link" then 0 else 1 end) | .[0])
    ' "$WORKDIR/prs.json" > "$WORKDIR/linked-prs.json"

    # Build excluded list (enriched with issue titles)
    jq --slurpfile links "$WORKDIR/linked-prs.json" '
      [ $links[0][] as $link |
        (. | map(select(.number == $link.issueNumber)) | .[0]) as $issue |
        select($issue != null) |
        {
          issueNumber: $link.issueNumber,
          issueTitle: $issue.title,
          prNumber: $link.prNumber,
          prTitle: $link.prTitle,
          prUrl: $link.prUrl,
          method: $link.method
        }
      ]
    ' "$WORKDIR/issues.json" > "$WORKDIR/excluded.json"

    EXCLUDED_COUNT=$(jq 'length' "$WORKDIR/excluded.json")

    # Filter: keep issues without linked PRs
    EXCLUDE_NUMS=$(jq '[.[].issueNumber]' "$WORKDIR/linked-prs.json")
    jq --argjson ex "$EXCLUDE_NUMS" '
      [.[] | select(.number as $n | $ex | index($n) | not)]
    ' "$WORKDIR/issues.json" > "$WORKDIR/filtered.json"
  fi

else
  LINKING_MODE="disabled"
  cp "$WORKDIR/issues.json" "$WORKDIR/filtered.json"
  echo '[]' > "$WORKDIR/excluded.json"
fi

REMAINING=$(jq 'length' "$WORKDIR/filtered.json")

# ── Step 2.5: Diff against baseline (incremental mode) ──────────────────────

DIFF_CACHED=0
DIFF_NEW=0
DIFF_MODIFIED=0
DIFF_REMOVED=0

if [[ "$DIFF_MODE" == "true" ]]; then
  # Single jq call: classify issues, extract delta + cached scores.
  # Uses O(1) object lookups instead of O(n) array index() for scalability.
  # Use baseline's filtered.json (analyzed issues only) if available; fall back to issues.json
  DIFF_PRIOR_ISSUES="$DIFF_FROM_DIR/issues.json"
  if [[ -s "$DIFF_FROM_DIR/filtered.json" ]]; then
    DIFF_PRIOR_ISSUES="$DIFF_FROM_DIR/filtered.json"
  fi

  DIFF_COMBINED="$WORKDIR/diff-combined.json"
  jq -n \
    --slurpfile current "$WORKDIR/filtered.json" \
    --slurpfile priorIssues "$DIFF_PRIOR_ISSUES" \
    --slurpfile priorScores "$DIFF_FROM_DIR/results/merged.json" \
    '
    # O(1) lookup maps
    ($priorIssues[0] | map({(.number | tostring): .updatedAt}) | add // {}) as $priorUpdated |
    ($priorScores[0] | map({(.number | tostring): .}) | add // {}) as $scoreMap |
    ($current[0] | map({(.number | tostring): true}) | add // {}) as $currentSet |

    # Classify current issues
    ($current[0] | map(
      (.number | tostring) as $key |
      if ($priorUpdated[$key] == null) then
        {number, classification: "new"}
      elif ($priorUpdated[$key] == .updatedAt and $scoreMap[$key] != null) then
        {number, classification: "unchanged"}
      else
        {number, classification: "modified"}
      end
    )) as $classified |

    # Build classification sets as O(1) maps
    ($classified | map(select(.classification != "unchanged")) | map({(.number | tostring): true}) | add // {}) as $deltaSet |
    ($classified | map(select(.classification == "unchanged")) | map({(.number | tostring): true}) | add // {}) as $cachedSet |

    # Removed: in prior scores but not in current filtered
    ($priorScores[0] | map(select((.number | tostring) as $k | $currentSet[$k] == null)) | length) as $removedCount |

    # Stats
    ($classified | map(select(.classification == "unchanged")) | length) as $cached |
    ($classified | map(select(.classification == "new")) | length) as $new |
    ($classified | map(select(.classification == "modified")) | length) as $modified |

    {
      classify: {
        stats: {cached: $cached, new: $new, modified: $modified, removed: $removedCount},
        classifications: $classified
      },
      delta: [$current[0][] | select((.number | tostring) as $k | $deltaSet[$k] != null)],
      cachedScores: [$priorScores[0][] | select((.number | tostring) as $k | $cachedSet[$k] != null)]
    }
    ' > "$DIFF_COMBINED"

  # Split combined output into individual files
  jq '.classify' "$DIFF_COMBINED" > "$WORKDIR/diff-classify.json"
  jq '.delta' "$DIFF_COMBINED" > "$WORKDIR/delta.json"
  jq '.cachedScores' "$DIFF_COMBINED" > "$WORKDIR/cached-scores.json"
  rm -f "$DIFF_COMBINED"

  DIFF_CACHED=$(jq '.stats.cached' "$WORKDIR/diff-classify.json")
  DIFF_NEW=$(jq '.stats.new' "$WORKDIR/diff-classify.json")
  DIFF_MODIFIED=$(jq '.stats.modified' "$WORKDIR/diff-classify.json")
  DIFF_REMOVED=$(jq '.stats.removed' "$WORKDIR/diff-classify.json")

  # Override REMAINING to delta count (drives batch splitting downstream)
  REMAINING=$(jq 'length' "$WORKDIR/delta.json")
fi

# ── Step 3: Truncate bodies ──────────────────────────────────────────────────

# In diff mode, truncate delta.json (only issues needing analysis); otherwise filtered.json
TRUNCATE_INPUT="$WORKDIR/filtered.json"
if [[ "$DIFF_MODE" == "true" ]]; then
  TRUNCATE_INPUT="$WORKDIR/delta.json"
fi

TRUNCATED_COUNT=$(jq --argjson t "$TRUNCATE" '
  [.[] | select((.body // "" | length) > $t)] | length
' "$TRUNCATE_INPUT")

jq --argjson t "$TRUNCATE" '
  [.[] | .body = (
    if (.body // "" | length) > $t
    then (.body[:$t] + "\n...[truncated]")
    else .body
    end
  )]
' "$TRUNCATE_INPUT" > "$WORKDIR/ready.json"

# ── Step 4: Split into batches (by size, not by count) ───────────────────────

rm -f "$WORKDIR"/batches/batch-*.json "$WORKDIR"/batch-*.json 2>/dev/null || true

if [[ "$REMAINING" -eq 0 ]]; then
  NUM_BATCHES=0
  WAVES_NEEDED=0
  BATCHES_JSON="[]"
else
  NUM_BATCHES=$(( (REMAINING + BATCH_SIZE - 1) / BATCH_SIZE ))
  WAVES_NEEDED=$(( (NUM_BATCHES + MAX_CONCURRENCY - 1) / MAX_CONCURRENCY ))

  BATCH_META=""
  for ((i = 0; i < NUM_BATCHES; i++)); do
    START=$((i * BATCH_SIZE))
    BFILE="batch-$((i + 1)).json"
    BPATH="batches/$BFILE"
    jq --argjson s "$START" --argjson sz "$BATCH_SIZE" \
      '.[$s : $s + $sz]' "$WORKDIR/ready.json" > "$WORKDIR/$BPATH"
    ln -sfn "$BPATH" "$WORKDIR/$BFILE"

    COUNT=$(jq 'length' "$WORKDIR/$BPATH")
    FIRST=$(jq '.[0].number' "$WORKDIR/$BPATH")
    LAST=$(jq '.[-1].number' "$WORKDIR/$BPATH")
    BATCH_META="${BATCH_META}{\"file\":\"$BPATH\",\"count\":$COUNT,\"firstIssue\":$FIRST,\"lastIssue\":$LAST},"
  done

  BATCHES_JSON="[${BATCH_META%,}]"
fi

# Ensure operational artifacts exist for downstream stages.
if [[ ! -f "$WORKDIR/results/merged.json" ]]; then
  echo '[]' > "$WORKDIR/results/merged.json"
fi
if [[ ! -f "$WORKDIR/results/report.md" ]]; then
  cat > "$WORKDIR/results/report.md" <<EOF
# Issue Prioritization Report

- Repo: $REPO
- Run: $RUN_ID
- Generated At: $GENERATED_AT

_Populate this file after analysis merge._
EOF
fi

# ── Step 5: Write manifest ───────────────────────────────────────────────────

if [[ "$RESUME_MODE" == "true" ]]; then
  RESUME_JSON=true
else
  RESUME_JSON=false
fi

if [[ "$DIFF_MODE" == "true" ]]; then
  DIFF_JSON=true
  DIFF_FROM_PATH="$DIFF_FROM_DIR"
else
  DIFF_JSON=false
  DIFF_FROM_PATH=""
fi

jq -n \
  --arg repo "$REPO" \
  --arg runId "$RUN_ID" \
  --arg wd "$WORKDIR" \
  --arg historyDir "$HISTORY_DIR" \
  --arg filter "$FILTER_DESC" \
  --arg source "$SOURCE" \
  --arg linkingMode "$LINKING_MODE" \
  --arg generatedAt "$GENERATED_AT" \
  --arg ghVersion "$GH_VERSION" \
  --argjson resumeMode "$RESUME_JSON" \
  --argjson diffMode "$DIFF_JSON" \
  --arg diffFrom "$DIFF_FROM_PATH" \
  --argjson diffCached "$DIFF_CACHED" \
  --argjson diffNew "$DIFF_NEW" \
  --argjson diffModified "$DIFF_MODIFIED" \
  --argjson diffRemoved "$DIFF_REMOVED" \
  --argjson totalFetched "$TOTAL_ISSUES" \
  --argjson excludedWithPRs "$EXCLUDED_COUNT" \
  --argjson remaining "$REMAINING" \
  --argjson batchSize "$BATCH_SIZE" \
  --argjson totalBatches "${NUM_BATCHES:-0}" \
  --argjson maxConcurrency "$MAX_CONCURRENCY" \
  --argjson wavesNeeded "${WAVES_NEEDED:-0}" \
  --argjson truncateChars "$TRUNCATE" \
  --argjson truncatedCount "${TRUNCATED_COUNT:-0}" \
  --argjson batches "$BATCHES_JSON" \
  --slurpfile excluded "$WORKDIR/excluded.json" \
  '{
    repo: $repo,
    runId: $runId,
    workdir: $wd,
    historyDir: $historyDir,
    resumeMode: $resumeMode,
    diffMode: $diffMode,
    diffFrom: (if $diffFrom == "" then null else $diffFrom end),
    diffStats: (if $diffMode then {cached: $diffCached, new: $diffNew, modified: $diffModified, removed: $diffRemoved} else null end),
    filter: $filter,
    source: $source,
    linkingMode: $linkingMode,
    generatedAt: $generatedAt,
    ghVersion: $ghVersion,
    paths: {
      batchesDir: "batches",
      resultsDir: "results",
      merged: "results/merged.json",
      report: "results/report.md",
      summary: "summary.json",
      cachedScores: (if $diffMode then "cached-scores.json" else null end)
    },
    stats: {
      totalFetched: $totalFetched,
      excludedWithPRs: $excludedWithPRs,
      remaining: $remaining,
      batchSize: $batchSize,
      totalBatches: $totalBatches,
      maxConcurrency: $maxConcurrency,
      wavesNeeded: $wavesNeeded,
      truncateChars: $truncateChars,
      truncatedCount: $truncatedCount
    },
    batches: $batches,
    excluded: $excluded[0]
  }' > "$WORKDIR/manifest.json"

# ── Step 6: Write summary + retention + stdout ───────────────────────────────

if [[ "$TOTAL_ISSUES" -eq 0 ]]; then
  STATUS="empty"
else
  STATUS="ok"
fi

SUMMARY_JSON=$(
  jq -nc \
    --arg status "$STATUS" \
    --arg repo "$REPO" \
    --arg runId "$RUN_ID" \
    --arg filter "$FILTER_DESC" \
    --arg source "$SOURCE" \
    --arg linkingMode "$LINKING_MODE" \
    --arg workdir "$WORKDIR" \
    --arg historyDir "$HISTORY_DIR" \
    --arg summary "summary.json" \
    --arg manifest "manifest.json" \
    --arg merged "results/merged.json" \
    --arg report "results/report.md" \
    --argjson totalFetched "$TOTAL_ISSUES" \
    --argjson excluded "$EXCLUDED_COUNT" \
    --argjson remaining "$REMAINING" \
    --argjson batches "${NUM_BATCHES:-0}" \
    --argjson waves "${WAVES_NEEDED:-0}" \
    --argjson batchSize "$BATCH_SIZE" \
    --argjson concurrency "$MAX_CONCURRENCY" \
    --argjson diffMode "$DIFF_JSON" \
    --argjson diffCached "$DIFF_CACHED" \
    --argjson diffNew "$DIFF_NEW" \
    --argjson diffModified "$DIFF_MODIFIED" \
    --argjson diffRemoved "$DIFF_REMOVED" \
    '{
      status: $status,
      repo: $repo,
      runId: $runId,
      filter: $filter,
      source: $source,
      linkingMode: $linkingMode,
      totalFetched: $totalFetched,
      excluded: $excluded,
      remaining: $remaining,
      batches: $batches,
      waves: $waves,
      batchSize: $batchSize,
      concurrency: $concurrency,
      diffMode: $diffMode,
      diffCached: $diffCached,
      diffNew: $diffNew,
      diffModified: $diffModified,
      diffRemoved: $diffRemoved,
      workdir: $workdir,
      historyDir: $historyDir,
      paths: {
        summary: $summary,
        manifest: $manifest,
        merged: $merged,
        report: $report
      }
    }'
)
echo "$SUMMARY_JSON" > "$WORKDIR/summary.json"

case "$WORKDIR" in
  "$HISTORY_DIR"/*)
    ln -sfn "$WORKDIR" "$HISTORY_DIR/latest"
    ;;
esac

if [[ -d "$HISTORY_DIR" ]]; then
  mapfile -t RUN_DIRS < <(
    find "$HISTORY_DIR" -mindepth 1 -maxdepth 1 -type d -printf '%T@ %p\n' \
      | sort -nr \
      | while IFS= read -r line; do
          printf '%s\n' "${line#* }"
        done
  )
  if [[ "${#RUN_DIRS[@]}" -gt "$RETAIN" ]]; then
    for ((i = RETAIN; i < ${#RUN_DIRS[@]}; i++)); do
      if [[ "${RUN_DIRS[$i]}" == "$WORKDIR" ]]; then
        continue
      fi
      rm -rf "${RUN_DIRS[$i]}"
    done
  fi
fi

echo "$SUMMARY_JSON"
