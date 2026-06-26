#!/usr/bin/env bash
# =============================================================================
# remediate.sh — Monet Works QA → Remediation Auto-Fix Pipeline (Shell Wrapper)
# =============================================================================
#
# Usage:
#   remediate.sh --content draft.md --type financial
#   remediate.sh --content draft.md --verdict verdict.json --type financial
#   remediate.sh --content draft.md --type financial --out fixed.md
#   remediate.sh --content draft.md --type financial --out fixed.md --report report.json
#   remediate.sh --content draft.md --type financial --max-words 500
#
# Flags:
#   --content  / -c   Path to content file (required)
#   --verdict  / -v   Path to QA verdict JSON (optional; auto-detects issues if omitted)
#   --type     / -t   Content type: financial | investment | health | legal | general (default: general)
#   --out      / -o   Write fixed content to file instead of stdout
#   --report   / -r   Write change report JSON to file instead of stderr
#   --max-words       Truncate to N words max
#   --cta-variant     CTA template variant (default: default)
#   --no-banner       Suppress change report
#   --help     / -h   Show this help
#
# Exit codes:
#   0 — all issues auto-fixed
#   1 — partial (some issues require human review)
#   2 — failed / error
# =============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_DIR="$(dirname "$SCRIPT_DIR")"

# Default values
CONTENT_FILE=""
VERDICT_FILE=""
CONTENT_TYPE="general"
OUT_FILE=""
REPORT_FILE=""
MAX_WORDS=""
CTA_VARIANT="default"
NO_BANNER=""

# ---------------------------------------------------------------------------
# Parse arguments
# ---------------------------------------------------------------------------
while [[ $# -gt 0 ]]; do
  case "$1" in
    --content|-c)
      CONTENT_FILE="$2"; shift 2 ;;
    --verdict|-v)
      VERDICT_FILE="$2"; shift 2 ;;
    --type|-t)
      CONTENT_TYPE="$2"; shift 2 ;;
    --out|-o)
      OUT_FILE="$2"; shift 2 ;;
    --report|-r)
      REPORT_FILE="$2"; shift 2 ;;
    --max-words)
      MAX_WORDS="$2"; shift 2 ;;
    --cta-variant)
      CTA_VARIANT="$2"; shift 2 ;;
    --no-banner)
      NO_BANNER="--no-banner"; shift ;;
    --help|-h)
      grep '^#' "$0" | sed 's/^# \?//' | tail -n +2
      exit 0 ;;
    *)
      echo "ERROR: Unknown flag: $1" >&2
      exit 2 ;;
  esac
done

# ---------------------------------------------------------------------------
# Validate
# ---------------------------------------------------------------------------
if [[ -z "$CONTENT_FILE" ]]; then
  echo "ERROR: --content / -c is required." >&2
  exit 2
fi

if [[ ! -f "$CONTENT_FILE" ]]; then
  echo "ERROR: Content file not found: $CONTENT_FILE" >&2
  exit 2
fi

# ---------------------------------------------------------------------------
# Build command
# ---------------------------------------------------------------------------
CMD=(python3 "$SCRIPT_DIR/auto-remediate.py"
  --content "$CONTENT_FILE"
  --type "$CONTENT_TYPE"
  --cta-variant "$CTA_VARIANT"
)

if [[ -n "$VERDICT_FILE" ]]; then
  CMD+=(--verdict "$VERDICT_FILE")
fi

if [[ -n "$MAX_WORDS" ]]; then
  CMD+=(--max-words "$MAX_WORDS")
fi

if [[ -n "$NO_BANNER" ]]; then
  CMD+=("$NO_BANNER")
fi

# ---------------------------------------------------------------------------
# Run and capture output
# ---------------------------------------------------------------------------
TMPOUT=$(mktemp)
TMPERR=$(mktemp)
# shellcheck disable=SC2064
trap "rm -f $TMPOUT $TMPERR" EXIT

EXIT_CODE=0
"${CMD[@]}" >"$TMPOUT" 2>"$TMPERR" || EXIT_CODE=$?

# ---------------------------------------------------------------------------
# Deliver outputs
# ---------------------------------------------------------------------------
if [[ -n "$OUT_FILE" ]]; then
  cp "$TMPOUT" "$OUT_FILE"
  echo "✅ Fixed content written to: $OUT_FILE" >&2
else
  cat "$TMPOUT"
fi

if [[ -n "$REPORT_FILE" ]]; then
  cp "$TMPERR" "$REPORT_FILE"
  echo "📋 Change report written to: $REPORT_FILE" >&2
elif [[ -z "$NO_BANNER" ]]; then
  cat "$TMPERR" >&2
fi

# ---------------------------------------------------------------------------
# Human-review summary (only if stdout goes to a terminal or report file)
# ---------------------------------------------------------------------------
if [[ $EXIT_CODE -eq 1 && -z "$NO_BANNER" ]]; then
  echo "" >&2
  echo "⚠️  Some issues require human review. Check the change report above." >&2
fi

exit $EXIT_CODE
