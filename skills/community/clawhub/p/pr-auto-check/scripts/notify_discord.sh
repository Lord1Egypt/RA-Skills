#!/usr/bin/env bash
# notify_discord.sh — Post PR auto-check result to Discord via webhook
# Usage: bash notify_discord.sh --webhook <url> --result <json-file> [--channel <channel-id>]
set -euo pipefail

WEBHOOK=""
RESULT_FILE=""
CHANNEL=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --webhook) WEBHOOK="$2"; shift 2 ;;
    --result)  RESULT_FILE="$2"; shift 2 ;;
    --channel) CHANNEL="$2"; shift 2 ;;
    *) echo "Unknown arg: $1"; exit 1 ;;
  esac
done

if [[ -z "$WEBHOOK" || -z "$RESULT_FILE" || ! -f "$RESULT_FILE" ]]; then
  echo "Usage: notify_discord.sh --webhook <url> --result <json-file>" >&2; exit 1
fi

# Parse JSON result
PR=$(jq -r '.pr' "$RESULT_FILE")
CI_PASS=$(jq -r '.ci.pass' "$RESULT_FILE")
CI_SUMMARY=$(jq -r '.ci.summary' "$RESULT_FILE")
DIFF_STATS=$(jq -r '.diff_stats' "$RESULT_FILE")
H_MAX=$(jq -r '.health.max_severity' "$RESULT_FILE")
H_SUMMARY=$(jq -r '.health.summary' "$RESULT_FILE")
TIMESTAMP=$(jq -r '.timestamp' "$RESULT_FILE")

# Build emoji indicators
CI_EMOJI="✅"; [[ "$CI_PASS" == "false" ]] && CI_EMOJI="❌"
H_EMOJI="✅"; [[ "$H_MAX" == "1" ]] && H_EMOJI="⚠️"; [[ "$H_MAX" -ge 2 ]] && H_EMOJI="❌"

# Build Discord embed payload
PAYLOAD=$(jq -n \
  --arg pr "$PR" \
  --arg ci_e "$CI_EMOJI" --arg ci_s "$CI_SUMMARY" \
  --arg diff "$DIFF_STATS" \
  --arg h_e "$H_EMOJI" --arg h_s "$H_SUMMARY" \
  --arg ts "$TIMESTAMP" \
  '{
    embeds: [{
      title: ("PR #" + $pr + " — Auto-Check Report"),
      color: (if $ci_e == "✅" and $h_e == "✅" then 3066993 elif $ci_e == "❌" or $h_e == "❌" then 15158332 else 16776960 end),
      fields: [
        { name: "CI/CD", value: ($ci_e + " " + $ci_s), inline: false },
        { name: "Diff", value: $diff, inline: true },
        { name: "Health", value: ($h_e + " " + $h_s), inline: true }
      ],
      footer: { text: ("pr-auto-check • " + $ts) }
    }]
  }')

curl -s -H "Content-Type: application/json" -d "$PAYLOAD" "$WEBHOOK" >/dev/null
echo "Discord notification sent for PR #$PR"
