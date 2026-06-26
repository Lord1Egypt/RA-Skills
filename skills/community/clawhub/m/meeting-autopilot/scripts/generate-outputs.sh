#!/usr/bin/env bash
# generate-outputs.sh — Generate operational outputs from extracted items
# Usage: bash generate-outputs.sh <extracted_items.json> [meeting_title]
# Input:  JSON from extract-items.sh
# Output: Beautiful Markdown report to stdout
#
# Pass 3: Generate follow-up emails, ticket drafts, action table, decisions log
# Requires: ANTHROPIC_API_KEY or OPENAI_API_KEY env var

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

require_jq

EXTRACTED_FILE="${1:--}"
MEETING_TITLE="${2:-}"

# Read extracted items JSON
if [ "$EXTRACTED_FILE" = "-" ]; then
  EXTRACTED_JSON="$(cat)"
else
  [ -f "$EXTRACTED_FILE" ] || die "Extracted items file not found: $EXTRACTED_FILE"
  EXTRACTED_JSON="$(cat "$EXTRACTED_FILE")"
fi

[ -z "$EXTRACTED_JSON" ] && die "No extracted items to generate outputs from."

# Extract meeting title from JSON if not provided
if [ -z "$MEETING_TITLE" ]; then
  MEETING_TITLE=$(printf '%s' "$EXTRACTED_JSON" | jq -r '.meeting_title // "Untitled Meeting"')
fi

# ── Parse items by type ───────────────────────────────────
ITEMS=$(printf '%s' "$EXTRACTED_JSON" | jq '.items // []')
SUMMARY=$(printf '%s' "$EXTRACTED_JSON" | jq '.summary // {}')

DECISIONS=$(printf '%s' "$ITEMS" | jq '[.[] | select(.type == "decision")]')
ACTION_ITEMS=$(printf '%s' "$ITEMS" | jq '[.[] | select(.type == "action_item")]')
OPEN_QUESTIONS=$(printf '%s' "$ITEMS" | jq '[.[] | select(.type == "open_question")]')
PARKING_LOT=$(printf '%s' "$ITEMS" | jq '[.[] | select(.type == "parking_lot")]')
KEY_POINTS=$(printf '%s' "$ITEMS" | jq '[.[] | select(.type == "key_point")]')

NUM_DECISIONS=$(printf '%s' "$DECISIONS" | jq 'length')
NUM_ACTIONS=$(printf '%s' "$ACTION_ITEMS" | jq 'length')
NUM_QUESTIONS=$(printf '%s' "$OPEN_QUESTIONS" | jq 'length')
NUM_PARKING=$(printf '%s' "$PARKING_LOT" | jq 'length')
NUM_KEY_POINTS=$(printf '%s' "$KEY_POINTS" | jq 'length')
NUM_TOTAL=$(printf '%s' "$ITEMS" | jq 'length')

# ── Extract unique speakers ───────────────────────────────
SPEAKERS=$(printf '%s' "$ITEMS" | jq -r '[.[].speaker // empty] | unique | join(", ")')

log_step "Pass 3: Generating operational outputs..."

# ── LLM Call Helper (same as extract-items.sh) ────────────
call_llm() {
  local system_prompt="$1"
  local user_message
  user_message="$(cat)"

  if [ -n "${ANTHROPIC_API_KEY:-}" ]; then
    local anthropic_base
    anthropic_base="${ANTHROPIC_API_URL:-https://api.anthropic.com}"
    validate_http_url "$anthropic_base" "ANTHROPIC_API_URL"

    local request_body
    request_body=$(jq -n \
      --arg model "${ANTHROPIC_MODEL:-claude-sonnet-4-20250514}" \
      --arg system "$system_prompt" \
      --arg user "$user_message" \
      '{
        model: $model,
        max_tokens: 8192,
        system: $system,
        messages: [{role: "user", content: $user}]
      }')

    local response
    response=$(printf '%s' "$request_body" | curl -sS \
      "${anthropic_base%/}/v1/messages" \
      -H "Content-Type: application/json" \
      -H "x-api-key: ${ANTHROPIC_API_KEY}" \
      -H "anthropic-version: 2023-06-01" \
      -d @- 2>/dev/null)

    printf '%s' "$response" | jq -r '.content[0].text // empty' 2>/dev/null

  elif [ -n "${OPENAI_API_KEY:-}" ]; then
    local openai_base
    openai_base="${OPENAI_API_URL:-https://api.openai.com}"
    validate_http_url "$openai_base" "OPENAI_API_URL"

    local request_body
    request_body=$(jq -n \
      --arg model "${OPENAI_MODEL:-gpt-4o}" \
      --arg system "$system_prompt" \
      --arg user "$user_message" \
      '{
        model: $model,
        max_tokens: 8192,
        messages: [
          {role: "system", content: $system},
          {role: "user", content: $user}
        ]
      }')

    local response
    response=$(printf '%s' "$request_body" | curl -sS \
      "${openai_base%/}/v1/chat/completions" \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer ${OPENAI_API_KEY}" \
      -d @- 2>/dev/null)

    printf '%s' "$response" | jq -r '.choices[0].message.content // empty' 2>/dev/null
  else
    die "No LLM API key found." \
      "Set ANTHROPIC_API_KEY or OPENAI_API_KEY."
  fi
}

# ── Generate follow-up email and ticket drafts via LLM ────
OUTPUT_PROMPT_FILE="$SCRIPT_DIR/../templates/outputs-prompt.md"
[ -f "$OUTPUT_PROMPT_FILE" ] || die "Template not found: outputs-prompt.md"
OUTPUT_PROMPT="$(cat "$OUTPUT_PROMPT_FILE")"

# Prepare items summary for the LLM
ITEMS_SUMMARY=$(printf '%s' "$ITEMS" | jq -r '.[] |
  "[\(.type | ascii_upcase)] (\(.speaker // "Unknown")): \(.text)"
' 2>/dev/null)

OPERATIONAL_OUTPUTS=$(printf '%s' "Meeting: $MEETING_TITLE
Participants: $SPEAKERS

EXTRACTED ITEMS:
$ITEMS_SUMMARY" | call_llm "$OUTPUT_PROMPT")

if [ -z "$OPERATIONAL_OUTPUTS" ]; then
  log_warn "LLM returned empty for operational outputs. Generating report without email/ticket drafts."
  OPERATIONAL_OUTPUTS=""
fi

# ── Generate the Markdown report ──────────────────────────
REPORT_DATE="$(date '+%B %d, %Y at %H:%M')"

cat << 'HEADER'
<!-- Meeting Autopilot Report — Generated automatically. Do not edit above this line. -->
HEADER

echo ""
echo "# ✈️ Meeting Autopilot Report"
echo ""
echo "**$MEETING_TITLE**"
echo "📅 $REPORT_DATE"
[ -n "$SPEAKERS" ] && echo "👥 Participants: $SPEAKERS"
echo ""

# ── Overview bar ──────────────────────────────────────────
echo "---"
echo ""
echo "## 📊 Overview"
echo ""
echo "| Category | Count |"
echo "|----------|------:|"
echo "| ✅ Decisions | $NUM_DECISIONS |"
echo "| 📋 Action Items | $NUM_ACTIONS |"
echo "| ❓ Open Questions | $NUM_QUESTIONS |"
echo "| 🅿️ Parking Lot | $NUM_PARKING |"
echo "| 💡 Key Points | $NUM_KEY_POINTS |"
echo "| **Total Items** | **$NUM_TOTAL** |"
echo ""

# ── Decisions ─────────────────────────────────────────────
if [ "$NUM_DECISIONS" -gt 0 ]; then
  echo "---"
  echo ""
  echo "## ✅ Decisions"
  echo ""
  printf '%s' "$DECISIONS" | jq -r 'to_entries[] |
    "### Decision \(.key + 1)\n" +
    "> \(.value.text)\n\n" +
    "- **Decided by:** \(.value.speaker // "Not attributed")\n" +
    (if .value.timestamp and .value.timestamp != "" then "- **When:** \(.value.timestamp)\n" else "" end) +
    (if .value.rationale and .value.rationale != "" then "- **Rationale:** \(.value.rationale)\n" else "" end) +
    ""'
  echo ""
fi

# ── Action Items Table ────────────────────────────────────
if [ "$NUM_ACTIONS" -gt 0 ]; then
  echo "---"
  echo ""
  echo "## 📋 Action Items"
  echo ""
  echo "| # | Action | Owner | Deadline | Status |"
  echo "|:-:|--------|-------|----------|:------:|"
  printf '%s' "$ACTION_ITEMS" | jq -r 'to_entries[] |
    "| \(.key + 1) | \(.value.text) | \(.value.speaker // "Unassigned") | \(.value.deadline // "TBD") | ⬜ Open |"'
  echo ""
fi

# ── Open Questions ────────────────────────────────────────
if [ "$NUM_QUESTIONS" -gt 0 ]; then
  echo "---"
  echo ""
  echo "## ❓ Open Questions"
  echo ""
  printf '%s' "$OPEN_QUESTIONS" | jq -r 'to_entries[] |
    "\(.key + 1). **\(.value.text)**" +
    (if .value.speaker and .value.speaker != "" then "\n   - Raised by: \(.value.speaker)" else "" end)'
  echo ""
fi

# ── Parking Lot ───────────────────────────────────────────
if [ "$NUM_PARKING" -gt 0 ]; then
  echo "---"
  echo ""
  echo "## 🅿️ Parking Lot"
  echo ""
  echo "*Items deferred for future discussion:*"
  echo ""
  printf '%s' "$PARKING_LOT" | jq -r 'to_entries[] |
    "- \(.value.text)" +
    (if .value.speaker and .value.speaker != "" then " *(raised by \(.value.speaker))*" else "" end)'
  echo ""
fi

# ── Key Points ────────────────────────────────────────────
if [ "$NUM_KEY_POINTS" -gt 0 ]; then
  echo "---"
  echo ""
  echo "## 💡 Key Points"
  echo ""
  printf '%s' "$KEY_POINTS" | jq -r 'to_entries[] |
    "- \(.value.text)" +
    (if .value.speaker and .value.speaker != "" then " *(\(.value.speaker))*" else "" end)'
  echo ""
fi

# ── Operational Outputs (emails, tickets) ─────────────────
if [ -n "$OPERATIONAL_OUTPUTS" ]; then
  echo "---"
  echo ""
  echo "$OPERATIONAL_OUTPUTS"
  echo ""
fi

# ── Footer ────────────────────────────────────────────────
echo "---"
echo ""
echo "<sub>$BRAND_FOOTER | v$VERSION | Items stored locally for cross-meeting tracking.</sub>"
echo ""
echo "<sub>💡 *Tip: Install via \`meeting-autopilot\` for one-command meeting analysis.*</sub>"

log_ok "Report generated successfully"
