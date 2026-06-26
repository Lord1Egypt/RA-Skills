#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage:
  set-status.sh --run-dir <path> --file <baseline|validation|outcome|proposal> --status <value>

Updates the bullet under the relevant status section of an artifact file
without requiring the user to hand-edit markdown.

Valid status values:
  baseline.md, validation.md, outcome.md  : pass | fail | blocked | inconclusive
  proposal.md (Approval Status)           : pending | approved |
                                            "approved and implemented" |
                                            rejected | blocked
USAGE
}

RUN_DIR=""
FILE=""
STATUS=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --run-dir) RUN_DIR="${2:-}"; shift 2 ;;
    --file) FILE="${2:-}"; shift 2 ;;
    --status) STATUS="${2:-}"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown argument: $1" >&2; usage >&2; exit 1 ;;
  esac
done

if [[ -z "$RUN_DIR" || -z "$FILE" || -z "$STATUS" ]]; then
  usage >&2
  exit 1
fi

if [[ ! -d "$RUN_DIR" ]]; then
  echo "Run directory does not exist: $RUN_DIR" >&2
  exit 1
fi

case "$FILE" in
  baseline|validation|outcome)
    SECTION="## Status"
    case "$STATUS" in
      pass|fail|blocked|inconclusive) ;;
      *)
        echo "Invalid status '$STATUS' for $FILE.md" >&2
        echo "Allowed: pass, fail, blocked, inconclusive" >&2
        exit 1
        ;;
    esac
    TARGET="$RUN_DIR/${FILE}.md"
    ;;
  proposal)
    SECTION="## Approval Status"
    case "$STATUS" in
      pending|approved|"approved and implemented"|rejected|blocked) ;;
      *)
        echo "Invalid approval status '$STATUS' for proposal.md" >&2
        echo "Allowed: pending, approved, \"approved and implemented\", rejected, blocked" >&2
        exit 1
        ;;
    esac
    TARGET="$RUN_DIR/proposal.md"
    ;;
  *)
    echo "Unknown --file value: $FILE" >&2
    echo "Allowed: baseline, validation, outcome, proposal" >&2
    exit 1
    ;;
esac

if [[ ! -f "$TARGET" ]]; then
  echo "Target file does not exist: $TARGET" >&2
  exit 1
fi

# Replace the first bullet under the matching section heading.
# Uses awk for portability and to preserve UTF-8 characters intact.
TMP_FILE="$(mktemp)"
trap 'rm -f "$TMP_FILE"' EXIT

awk -v section="$SECTION" -v new_status="$STATUS" '
  BEGIN { in_section = 0; replaced = 0 }
  {
    if ($0 == section) {
      print
      in_section = 1
      next
    }
    if (in_section && /^## /) {
      in_section = 0
    }
    if (in_section && !replaced && /^- /) {
      print "- " new_status
      replaced = 1
      next
    }
    print
  }
  END {
    if (!replaced) {
      # Section had no bullet — emit one at end of file as a fallback.
      print ""
      print section
      print "- " new_status
    }
  }
' "$TARGET" > "$TMP_FILE"

mv "$TMP_FILE" "$TARGET"
echo "Updated $SECTION in $TARGET to: $STATUS"
