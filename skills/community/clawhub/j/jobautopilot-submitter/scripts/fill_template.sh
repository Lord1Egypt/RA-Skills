#!/bin/bash
# fill_template.sh — Agent-generated form-fill script framework
#
# PURPOSE:
#   This file is a FRAMEWORK TEMPLATE. The agent generates the actual fill
#   commands at runtime (after taking a page snapshot to get current element
#   refs) and writes them into the marked section below.
#
# SECURITY:
#   - This script contains ONLY openclaw browser CLI commands (fill, select,
#     click, upload, snapshot). It does NOT use curl, wget, fetch, or any
#     network tools.
#   - It does NOT read or transmit passwords.
#   - It is NOT a pre-loaded script with hidden logic. Every fill command is
#     derived from a live browser snapshot taken immediately before execution,
#     so refs are always fresh and never stale.
#   - Scripts generated from this template are written to /tmp/fill_<timestamp>.sh
#     and executed once. They are ephemeral and not persisted.
#
# HOW THE AGENT USES THIS FILE:
#   1. Agent takes a page snapshot to identify visible form fields
#   2. Agent runs check_required_fields.js to find unfilled required fields
#   3. Agent writes concrete fill/select/click commands into the marked section
#   4. Agent executes the resulting script via: bash /tmp/fill_<timestamp>.sh
#   5. Agent re-runs check_required_fields.js to verify all fields are filled
#
# EXAMPLE of what the agent writes into the fill section:
#   SNAP=$(openclaw browser --browser-profile $PROFILE snapshot \
#     --target-id $TARGET_ID --limit 500 --efficient)
#   REF_FNAME=$(get_ref "$SNAP" "First Name")
#   REF_LNAME=$(get_ref "$SNAP" "Last Name")
#   openclaw browser --browser-profile $PROFILE fill \
#     --target-id $TARGET_ID \
#     --fields "[{\"ref\":\"$REF_FNAME\",\"value\":\"$USER_FIRST_NAME\"},
#                {\"ref\":\"$REF_LNAME\",\"value\":\"$USER_LAST_NAME\"}]"
#   check "ok" "fill_name" "First + Last Name"
#
# Based on snapshot: <timestamp>, targetId: <TARGET_ID>
# Fields to fill this run (from check_required_fields unfilled): <fields_list>

PROFILE="${OPENCLAW_PROFILE:-apply}"
TARGET_ID="<TARGET_ID>"
ERRORS=()

# Load variant matching helpers (fuzzy dropdown matching for non-standard labels)
# Source from the same directory as this script (not an external path)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/match_variant_options.sh"

# Error tracking helper
check() {
  local result=$1
  local ref=$2
  local label=$3
  if echo "$result" | grep -q '"ok":false'; then
    ERRORS+=("[$ref] $label: action failed, response: $result")
    echo "FAIL: $label"
    return 1
  fi
  echo "OK: $label"
  return 0
}

# Ref extraction helpers
# (snapshot is plain text output — use sed/grep, not jq)
get_ref() {
  local snap="$1"; local label="$2"
  echo "$snap" | grep -F "\"$label\"" | sed 's/.*\[ref=\([^]]*\)].*/\1/' | head -1
}
get_ref_fuzzy() {
  local snap="$1"; local keyword="$2"
  echo "$snap" | grep -i "$keyword" | sed 's/.*\[ref=\([^]]*\)].*/\1/' | head -1
}
count_label() {
  local snap="$1"; local label="$2"
  echo "$snap" | grep -cF "\"$label\""
}

# Step 1: Take a fresh snapshot to get current element refs
# (Refs change on every page load — never reuse refs from a previous snapshot)
SNAP=$(openclaw browser --browser-profile $PROFILE snapshot \
  --target-id $TARGET_ID --limit 500 --efficient)

# ── AGENT-GENERATED FILL STEPS ───────────────────────────────────────────────
# The agent writes the actual fill commands here at runtime.
# Each command is derived from the live snapshot above.
# This placeholder is replaced in full before the script is executed.
#
# Structure the agent follows:
#   1. Extract refs with get_ref / get_ref_fuzzy
#   2. Batch fill text fields with a single `fill --fields [...]` call
#   3. Handle dropdowns with select or open+snap+click pattern
#   4. Handle file uploads with `upload <path>` before clicking the upload button
#   5. Call check() after each action group to catch failures early
# ─────────────────────────────────────────────────────────────────────────────

# ── END OF FILL STEPS ────────────────────────────────────────────────────────

# Final: unified error report
if [ ${#ERRORS[@]} -gt 0 ]; then
  echo ""
  echo "===== FAILED — the following steps need attention ====="
  for ERR in "${ERRORS[@]}"; do
    echo "  - $ERR"
  done
  exit 1
else
  echo ""
  echo "===== ALL STEPS COMPLETED SUCCESSFULLY ====="
  exit 0
fi
